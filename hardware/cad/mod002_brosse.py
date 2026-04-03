#!/usr/bin/env python3
"""
MOD-002 — Module Brosse Rotative pour le robot Forcair.

Module outil IMS (Interface Module Standard) embarquant un moteur DC
cylindrique dont l'axe pointe vers le bas pour entrainer une brosse rotative.

Face superieure : plots de centrage + trous M5 (interface IMS vers chariot Z).
Face inferieure : berceau moteur en U + passage d'arbre + poches connecteurs.

Materiau cible : PETG (impression 3D FDM).
Usage : python mod002_brosse.py
"""
from __future__ import annotations

from pathlib import Path

import cadquery as cq

# -----------------------------------------------------------------------------
# Parametres principaux (modifier ici)
# -----------------------------------------------------------------------------

# --- Plaque de base IMS ---
PLAQUE_LONGUEUR = 100.0          # mm — axe X
PLAQUE_LARGEUR = 80.0            # mm — axe Y
PLAQUE_EPAISSEUR = 8.0           # mm — axe Z (plus epais pour logement moteur)

# --- Trous de fixation M5 (traversants, patron IMS) ---
M5_DIAMETRE = 5.3                # mm — jeu pour passage libre M5
M5_ECART_X = 80.0                # mm — entraxe axe long
M5_ECART_Y = 60.0                # mm — entraxe axe court

# --- Trous de reception centrage (face superieure -> chariot Z) ---
CENTRAGE_DIAMETRE = 8.2          # mm — leger jeu pour insertion
CENTRAGE_PROFONDEUR = 6.0        # mm
CENTRAGE_ECART_X = 60.0          # mm — entraxe entre les deux trous
CENTRAGE_ECART_Y = 0.0           # mm — centres sur l'axe Y

# --- Berceau moteur (face inferieure) ---
MOTEUR_DIAMETRE = 35.0           # mm — diametre exterieur moteur (Telsa 80)
MOTEUR_RAYON = MOTEUR_DIAMETRE / 2
BERCEAU_PAROI = 2.0              # mm — epaisseur parois laterales du berceau
BERCEAU_HAUTEUR = 20.0           # mm — hauteur totale du berceau sous la plaque
BERCEAU_LONGUEUR = MOTEUR_DIAMETRE + 2 * BERCEAU_PAROI  # mm — largeur ext. du U

# Trous M3 pour sangle de serrage moteur (un de chaque cote du berceau)
M3_DIAMETRE = 3.2                # mm — jeu pour passage libre M3
M3_HAUTEUR_DEPUIS_BASE = 10.0    # mm — position verticale sur le berceau

# Passage d'arbre moteur (traverse la plaque, centre sous le moteur)
ARBRE_DIAMETRE = 12.0            # mm

# --- Poche connecteur XT60 (alimentation, bord +Y) ---
XT60_LARGEUR = 20.0              # mm — axe X
XT60_PROFONDEUR = 16.0           # mm — axe Y (enfoncement dans la plaque)
XT60_HAUTEUR = 8.0               # mm — axe Z
XT60_OFFSET_X = 10.0             # mm — decalage depuis le centre du bord

# --- Poche connecteur JST-XH (signal, bord +Y, a cote du XT60) ---
JST_LARGEUR = 12.0               # mm — axe X
JST_PROFONDEUR = 8.0             # mm — axe Y
JST_HAUTEUR = 6.0                # mm — axe Z
JST_OFFSET_X = -12.0             # mm — decalage depuis le centre du bord

# --- Conges pour imprimabilite ---
CONGE_EXTERIEUR = 1.5            # mm — aretes exterieures de la plaque
CONGE_BERCEAU = 1.0              # mm — aretes du berceau


# -----------------------------------------------------------------------------
# Construction de la piece
# -----------------------------------------------------------------------------

def build_mod002() -> cq.Workplane:
    """Construit le module brosse MOD-002 complet."""

    # --- 1. Plaque de base centree sur l'origine ---
    plaque = (
        cq.Workplane("XY")
        .box(PLAQUE_LONGUEUR, PLAQUE_LARGEUR, PLAQUE_EPAISSEUR)
    )

    # --- 2. Trous de fixation M5 (traversants, 4 coins symetriques) ---
    positions_m5 = [
        ( M5_ECART_X / 2,  M5_ECART_Y / 2),
        (-M5_ECART_X / 2,  M5_ECART_Y / 2),
        ( M5_ECART_X / 2, -M5_ECART_Y / 2),
        (-M5_ECART_X / 2, -M5_ECART_Y / 2),
    ]
    plaque = (
        plaque
        .faces(">Z")
        .workplane()
        .pushPoints(positions_m5)
        .hole(M5_DIAMETRE)
    )

    # --- 3. Trous de reception centrage (face superieure) ---
    positions_centrage = [
        ( CENTRAGE_ECART_X / 2, CENTRAGE_ECART_Y / 2),
        (-CENTRAGE_ECART_X / 2, -CENTRAGE_ECART_Y / 2),
    ]
    plaque = (
        plaque
        .faces(">Z")
        .workplane()
        .pushPoints(positions_centrage)
        .hole(CENTRAGE_DIAMETRE, CENTRAGE_PROFONDEUR)
    )

    # --- 4. Passage d'arbre moteur (trou traversant, centre) ---
    plaque = (
        plaque
        .faces(">Z")
        .workplane()
        .hole(ARBRE_DIAMETRE)
    )

    # --- 5. Berceau moteur en U (face inferieure) ---
    # Le berceau est un bloc rectangulaire avec un alesage cylindrique
    # Semi-circulaire : le moteur repose dans le demi-cylindre inferieur

    berceau_ext_x = BERCEAU_LONGUEUR          # largeur exterieure
    berceau_ext_y = MOTEUR_RAYON + BERCEAU_PAROI  # profondeur (demi-moteur + paroi)
    berceau_ext_z = BERCEAU_HAUTEUR

    # Bloc massif du berceau, accole sous la plaque
    berceau_solid = (
        cq.Workplane("XY")
        .box(berceau_ext_x, berceau_ext_y * 2, berceau_ext_z)
        .translate((0, 0, -(PLAQUE_EPAISSEUR / 2 + berceau_ext_z / 2)))
    )

    # Cavite cylindrique pour le moteur (axe vertical Z)
    berceau_cavity = (
        cq.Workplane("XY")
        .cylinder(berceau_ext_z + 1, MOTEUR_RAYON)
        .translate((0, 0, -(PLAQUE_EPAISSEUR / 2 + berceau_ext_z / 2)))
    )

    # Assemblage : ajouter le bloc puis retirer le cylindre
    plaque = plaque.union(berceau_solid)
    plaque = plaque.cut(berceau_cavity)

    # --- 6. Trous M3 pour sangle de serrage (un de chaque cote du berceau) ---
    z_m3 = -(PLAQUE_EPAISSEUR / 2 + M3_HAUTEUR_DEPUIS_BASE)
    offset_y_m3 = berceau_ext_y  # au milieu de la paroi

    for signe in [1, -1]:
        trou_m3 = (
            cq.Workplane("XZ")
            .circle(M3_DIAMETRE / 2)
            .extrude(berceau_ext_y * 2 + 10)
            .translate((0, -(berceau_ext_y + 5), z_m3))
        )
        # Trou traversant dans l'axe Y a travers le berceau
        plaque = plaque.cut(trou_m3)

    # --- 7. Poche connecteur XT60 (bord +Y, encastree dans la plaque) ---
    bord_y = PLAQUE_LARGEUR / 2
    xt60 = (
        cq.Workplane("XY")
        .box(XT60_LARGEUR, XT60_PROFONDEUR, XT60_HAUTEUR)
        .translate((
            XT60_OFFSET_X,
            bord_y - XT60_PROFONDEUR / 2,
            -(PLAQUE_EPAISSEUR / 2 - XT60_HAUTEUR / 2)
        ))
    )
    plaque = plaque.cut(xt60)

    # --- 8. Poche connecteur JST-XH (bord +Y, a cote du XT60) ---
    jst = (
        cq.Workplane("XY")
        .box(JST_LARGEUR, JST_PROFONDEUR, JST_HAUTEUR)
        .translate((
            JST_OFFSET_X,
            bord_y - JST_PROFONDEUR / 2,
            -(PLAQUE_EPAISSEUR / 2 - JST_HAUTEUR / 2)
        ))
    )
    plaque = plaque.cut(jst)

    # --- 9. Conges pour imprimabilite ---
    if CONGE_EXTERIEUR > 0:
        try:
            # Conges sur les aretes principales de la plaque
            plaque = (
                plaque
                .edges("|Z")
                .fillet(CONGE_EXTERIEUR)
            )
        except Exception:
            try:
                plaque = plaque.edges("|Z").fillet(CONGE_EXTERIEUR / 2)
            except Exception:
                pass  # on garde la geometrie brute plutot que de planter

    if CONGE_BERCEAU > 0:
        try:
            # Conges sur les aretes horizontales du berceau
            plaque = (
                plaque
                .edges("<Z")
                .fillet(CONGE_BERCEAU)
            )
        except Exception:
            pass

    return plaque


# -----------------------------------------------------------------------------
# Export STL + STEP
# -----------------------------------------------------------------------------

def _export(obj: cq.Workplane, path: str) -> None:
    """Exporte un objet CadQuery vers le chemin indique (cree les dossiers)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(obj, str(p))
    print(f"  -> {p}")


if __name__ == "__main__":
    print("Construction du module brosse MOD-002 Forcair...")
    piece = build_mod002()

    out_dir = Path(__file__).parent
    _export(piece, str(out_dir / "mod002_brosse.step"))
    _export(piece, str(out_dir / "mod002_brosse.stl"))
    print("Termine.")
