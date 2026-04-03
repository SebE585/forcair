#!/usr/bin/env python3
"""
Assemblage du chassis Forcair — visualisation CAO.

Genere un fichier STEP montrant le robot assemble :
  - Cadre rectangulaire en profiles 2020 alu
  - Equerres de coin
  - Plateau de base (contreplaque / PETG)
  - Roues aux quatre coins
  - Mecanisme axe Z (tiges + platine IMS)

Usage:
    python assembly_chassis.py
"""
from __future__ import annotations

import cadquery as cq

# ─────────────────────────────────────────────
# Parametres globaux (dimensions en mm)
# ─────────────────────────────────────────────

# Profiles 2020 aluminium
PROFIL_SECTION = 20.0        # section carree 20x20
PROFIL_RAINURE = 6.0         # largeur de la rainure centrale
PROFIL_RAINURE_PROF = 6.0    # profondeur de la rainure
LONGUEUR_COTE = 300.0        # profiles lateraux (axe Y)
LONGUEUR_FACE = 250.0        # profiles avant/arriere (axe X)

# Equerres de coin
EQUERRE = 20.0               # taille du bloc L (20x20x20)
EQUERRE_EP = 4.0             # epaisseur des branches du L

# Plateau de base
PLATEAU_X = 280.0
PLATEAU_Y = 210.0
PLATEAU_Z = 5.0

# Roues
ROUE_DIAM = 80.0
ROUE_LARG = 25.0
ROUE_OFFSET = 15.0          # decalage vers l'exterieur du cadre

# Axe Z — tiges verticales
TIGE_DIAM = 8.0
TIGE_LONG = 50.0

# Platine IMS (bas de l'axe Z)
IMS_X = 100.0
IMS_Y = 80.0
IMS_Z = 5.0

# Ecart entre les deux tiges Z (centre a centre)
TIGE_ECART = 60.0

# Fichier de sortie
OUTPUT_STEP = "assembly_chassis.step"


# ─────────────────────────────────────────────
# Fonctions de construction des pieces
# ─────────────────────────────────────────────

def profil_2020(longueur: float) -> cq.Workplane:
    """Profile 2020 simplifie : section carree avec rainure sur chaque face."""
    # Section de base
    section = (
        cq.Workplane("XY")
        .rect(PROFIL_SECTION, PROFIL_SECTION)
    )
    profil = section.extrude(longueur)

    # Rainures sur les 4 faces (simplifiees comme des encoches)
    rainure = (
        cq.Workplane("XY")
        .rect(PROFIL_RAINURE, PROFIL_RAINURE_PROF)
        .extrude(longueur)
        .translate((0, (PROFIL_SECTION - PROFIL_RAINURE_PROF) / 2, 0))
    )
    for angle in [0, 90, 180, 270]:
        r = rainure.rotate((0, 0, 0), (0, 0, 1), angle)
        profil = profil.cut(r)

    return profil


def equerre_coin() -> cq.Workplane:
    """Equerre en L simplifiee 20x20x20."""
    # Bloc plein puis evidement pour former le L
    bloc = cq.Workplane("XY").box(EQUERRE, EQUERRE, EQUERRE)
    evidement = (
        cq.Workplane("XY")
        .box(EQUERRE - EQUERRE_EP, EQUERRE - EQUERRE_EP, EQUERRE + 1)
        .translate((EQUERRE_EP / 2, EQUERRE_EP / 2, 0))
    )
    return bloc.cut(evidement)


def plateau(lx: float, ly: float, lz: float) -> cq.Workplane:
    """Plaque rectangulaire."""
    return cq.Workplane("XY").box(lx, ly, lz)


def roue() -> cq.Workplane:
    """Roue simplifiee (cylindre)."""
    return (
        cq.Workplane("XY")
        .cylinder(ROUE_LARG, ROUE_DIAM / 2)
    )


def tige_verticale() -> cq.Workplane:
    """Tige lisse verticale (axe Z)."""
    return cq.Workplane("XY").cylinder(TIGE_LONG, TIGE_DIAM / 2)


# ─────────────────────────────────────────────
# Construction de l'assemblage
# ─────────────────────────────────────────────

def build_assembly() -> cq.Assembly:
    """Construit l'assemblage complet du chassis Forcair."""

    asm = cq.Assembly()

    # --------------------------------------------------
    # Repere : origine = coin avant-gauche du cadre exterieur
    # X = largeur (face), Y = profondeur (cote), Z = hauteur
    # Les profiles sont centres sur leur section ;
    # on les place de sorte que le cadre exterieur va de (0,0) a (LONGUEUR_FACE, LONGUEUR_COTE).
    # --------------------------------------------------

    demi = PROFIL_SECTION / 2  # 10 mm

    # --- Profiles lateraux (axe Y) : gauche et droit ---
    profil_cote = profil_2020(LONGUEUR_COTE)
    # Rotation pour aligner l'extrusion le long de Y
    profil_cote_y = profil_cote.rotate((0, 0, 0), (1, 0, 0), 90)

    # Cote gauche : x = 10 (centre du profil), y va de 0 a 300
    asm.add(
        profil_cote_y.translate((demi, LONGUEUR_COTE / 2, demi)),
        name="profil_cote_gauche",
    )
    # Cote droit : x = 250 - 10 = 240
    asm.add(
        profil_cote_y.translate((LONGUEUR_FACE - demi, LONGUEUR_COTE / 2, demi)),
        name="profil_cote_droit",
    )

    # --- Profiles avant/arriere (axe X) ---
    # Longueur interieure entre les profiles lateraux
    long_int_x = LONGUEUR_FACE - 2 * PROFIL_SECTION  # 210 mm
    profil_face = profil_2020(long_int_x)
    # Deja extrude le long de Z ; rotation pour aligner le long de X
    profil_face_x = profil_face.rotate((0, 0, 0), (0, 1, 0), -90)

    # Avant (y = 10)
    asm.add(
        profil_face_x.translate((LONGUEUR_FACE / 2, demi, demi)),
        name="profil_face_avant",
    )
    # Arriere (y = 300 - 10 = 290)
    asm.add(
        profil_face_x.translate((LONGUEUR_FACE / 2, LONGUEUR_COTE - demi, demi)),
        name="profil_face_arriere",
    )

    # --- Equerres de coin ---
    coins = [
        (demi, demi, demi),                                        # avant-gauche
        (LONGUEUR_FACE - demi, demi, demi),                       # avant-droit
        (demi, LONGUEUR_COTE - demi, demi),                       # arriere-gauche
        (LONGUEUR_FACE - demi, LONGUEUR_COTE - demi, demi),      # arriere-droit
    ]
    eq = equerre_coin()
    for i, (cx, cy, cz) in enumerate(coins):
        asm.add(eq.translate((cx, cy, cz)), name=f"equerre_{i}")

    # --- Plateau de base ---
    # Pose sur le dessus des profiles (z = PROFIL_SECTION + epaisseur/2)
    z_plateau = PROFIL_SECTION + PLATEAU_Z / 2
    asm.add(
        plateau(PLATEAU_X, PLATEAU_Y, PLATEAU_Z).translate(
            (LONGUEUR_FACE / 2, LONGUEUR_COTE / 2, z_plateau)
        ),
        name="plateau_base",
    )

    # --- Roues ---
    # Positionnees aux 4 coins, axe de rotation le long de X,
    # decalees vers l'exterieur du cadre.
    r = roue()
    # La roue est creee cylindre vertical (axe Z) ; rotation pour axe X
    r_x = r.rotate((0, 0, 0), (0, 1, 0), 90)

    positions_roues = [
        # (x, y) — z centre sur l'axe des profiles
        (-ROUE_OFFSET - ROUE_LARG / 2,           demi,                   ROUE_DIAM / 2),  # avant-gauche
        (LONGUEUR_FACE + ROUE_OFFSET + ROUE_LARG / 2, demi,              ROUE_DIAM / 2),  # avant-droit
        (-ROUE_OFFSET - ROUE_LARG / 2,           LONGUEUR_COTE - demi,   ROUE_DIAM / 2),  # arriere-gauche
        (LONGUEUR_FACE + ROUE_OFFSET + ROUE_LARG / 2, LONGUEUR_COTE - demi, ROUE_DIAM / 2),  # arriere-droit
    ]
    for i, (wx, wy, wz) in enumerate(positions_roues):
        asm.add(r_x.translate((wx, wy, wz)), name=f"roue_{i}")

    # --- Mecanisme axe Z ---
    # Deux tiges verticales suspendues sous le plateau, centrees en X,
    # decalees vers l'avant (y ~ 1/3 du cadre).
    y_axe_z = LONGUEUR_COTE * 0.3      # zone avant-centre
    x_centre = LONGUEUR_FACE / 2
    z_haut_tige = 0                      # part du bas du cadre
    z_centre_tige = z_haut_tige - TIGE_LONG / 2

    tige = tige_verticale()
    asm.add(
        tige.translate((x_centre - TIGE_ECART / 2, y_axe_z, z_centre_tige)),
        name="tige_z_gauche",
    )
    asm.add(
        tige.translate((x_centre + TIGE_ECART / 2, y_axe_z, z_centre_tige)),
        name="tige_z_droite",
    )

    # Platine IMS en bas des tiges
    z_ims = z_haut_tige - TIGE_LONG - IMS_Z / 2
    asm.add(
        plateau(IMS_X, IMS_Y, IMS_Z).translate((x_centre, y_axe_z, z_ims)),
        name="platine_ims",
    )

    return asm


# ─────────────────────────────────────────────
# Point d'entree
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("Construction de l'assemblage Forcair...")
    asm = build_assembly()

    # Export STEP
    asm.save(OUTPUT_STEP)
    print(f"Assemblage exporte : {OUTPUT_STEP}")
