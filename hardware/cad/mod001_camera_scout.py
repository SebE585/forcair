#!/usr/bin/env python3
"""
MOD-001 — Camera Scout : module GoPro pour le robot Forcair.

Module outil interchangeable qui se fixe sur la plaque IMS (chariot Z).
Support GoPro 3 doigts incline a 15° vers l'avant pour un meilleur
angle de vue lors de l'inspection.

Materiau cible : PETG (impression 3D FDM).
Usage : python mod001_camera_scout.py
"""
from __future__ import annotations

import math
from pathlib import Path

import cadquery as cq

# -----------------------------------------------------------------------------
# Parametres IMS (doivent correspondre a ims_plate.py)
# -----------------------------------------------------------------------------

# Plaque de base
PLAQUE_LONGUEUR = 100.0          # mm — axe X
PLAQUE_LARGEUR = 80.0            # mm — axe Y
PLAQUE_EPAISSEUR = 5.0           # mm — axe Z

# Trous de fixation M5 traversants (bolt pattern IMS)
M5_DIAMETRE = 5.3                # mm — jeu pour passage libre M5
M5_ECART_X = 80.0                # mm — entraxe sur l'axe long
M5_ECART_Y = 60.0                # mm — entraxe sur l'axe court

# Trous de reception pour plots de centrage IMS
CENTRAGE_DIAMETRE = 8.2          # mm — jeu pour insertion
CENTRAGE_PROFONDEUR = 6.0        # mm
CENTRAGE_ECART_X = 60.0          # mm — entraxe entre les deux trous
CENTRAGE_ECART_Y = 0.0           # mm — centres sur l'axe Y

# -----------------------------------------------------------------------------
# Parametres support GoPro (standard 3 doigts)
# -----------------------------------------------------------------------------

# Doigts du support (2 doigts exterieurs, l'espace central accueille le doigt GoPro)
DOIGT_EPAISSEUR = 3.0            # mm — epaisseur de chaque doigt
DOIGT_HAUTEUR = 15.0             # mm — hauteur utile
DOIGT_LARGEUR = 10.0             # mm — profondeur du doigt (axe Y)
DOIGT_ESPACEMENT = 8.0           # mm — espace entre les deux doigts (standard GoPro)

# Trou M5 dans les doigts pour le boulon GoPro
GOPRO_TROU_DIAMETRE = 5.3        # mm — passage libre M5

# Embase sous les doigts (raccord avec la plaque)
EMBASE_LONGUEUR = 30.0           # mm — axe X
EMBASE_LARGEUR = 20.0            # mm — axe Y
EMBASE_HAUTEUR = 5.0             # mm — axe Z

# Inclinaison du support vers l'avant
INCLINAISON_DEG = 15.0           # degres — angle vers +X

# -----------------------------------------------------------------------------
# Conges pour imprimabilite
# -----------------------------------------------------------------------------

CONGE_PLAQUE = 1.0               # mm — aretes de la plaque
CONGE_EMBASE = 1.5               # mm — raccord embase/plaque
CONGE_DOIGTS = 0.6               # mm — aretes des doigts


# -----------------------------------------------------------------------------
# Construction de la plaque de base
# -----------------------------------------------------------------------------

def _build_plaque() -> cq.Workplane:
    """Construit la plaque de base avec trous IMS."""

    # Plaque centree sur l'origine
    plaque = (
        cq.Workplane("XY")
        .box(PLAQUE_LONGUEUR, PLAQUE_LARGEUR, PLAQUE_EPAISSEUR)
    )

    # Trous de fixation M5 traversants (4 trous, symetriques)
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

    # Trous de reception centrage sur la face superieure
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

    return plaque


# -----------------------------------------------------------------------------
# Construction du support GoPro
# -----------------------------------------------------------------------------

def _build_gopro_mount() -> cq.Workplane:
    """
    Construit le support GoPro 3 doigts avec inclinaison.

    Le support est compose de :
    - une embase rectangulaire qui fait la transition avec la plaque
    - deux doigts paralleles perces d'un trou M5
    Le tout est incline de INCLINAISON_DEG vers l'avant (+X).
    """

    # --- Embase de raccord ---
    embase = (
        cq.Workplane("XY")
        .box(EMBASE_LONGUEUR, EMBASE_LARGEUR, EMBASE_HAUTEUR,
             centered=(True, True, False))
    )

    # --- Deux doigts exterieurs ---
    # Largeur totale occupee par les doigts : 2 * epaisseur + espacement
    largeur_totale = 2 * DOIGT_EPAISSEUR + DOIGT_ESPACEMENT

    # Position X de chaque doigt (centre par rapport a l'embase)
    doigt_x1 = -largeur_totale / 2                            # doigt gauche
    doigt_x2 = largeur_totale / 2 - DOIGT_EPAISSEUR           # doigt droit

    doigt_gauche = (
        cq.Workplane("XY")
        .box(DOIGT_EPAISSEUR, DOIGT_LARGEUR, DOIGT_HAUTEUR,
             centered=(False, True, False))
        .translate((doigt_x1, 0, EMBASE_HAUTEUR))
    )

    doigt_droit = (
        cq.Workplane("XY")
        .box(DOIGT_EPAISSEUR, DOIGT_LARGEUR, DOIGT_HAUTEUR,
             centered=(False, True, False))
        .translate((doigt_x2, 0, EMBASE_HAUTEUR))
    )

    # Assemblage embase + doigts
    support = embase.union(doigt_gauche).union(doigt_droit)

    # --- Trou M5 traversant les deux doigts (axe X) ---
    # Le trou est a mi-hauteur des doigts
    trou_z = EMBASE_HAUTEUR + DOIGT_HAUTEUR / 2
    trou = (
        cq.Workplane("YZ")
        .workplane(offset=-largeur_totale)
        .center(0, trou_z)
        .circle(GOPRO_TROU_DIAMETRE / 2)
        .extrude(largeur_totale * 2)
    )
    support = support.cut(trou)

    # --- Conges sur les doigts ---
    if CONGE_DOIGTS > 0:
        try:
            support = support.edges().fillet(CONGE_DOIGTS)
        except Exception:
            try:
                support = support.edges().fillet(CONGE_DOIGTS / 2)
            except Exception:
                pass

    # --- Inclinaison vers l'avant ---
    # Rotation autour de l'axe Y, pivot a la base de l'embase (z=0)
    if INCLINAISON_DEG != 0:
        support = support.rotate((0, 0, 0), (0, 1, 0), INCLINAISON_DEG)

    return support


# -----------------------------------------------------------------------------
# Assemblage final
# -----------------------------------------------------------------------------

def build_mod001() -> cq.Workplane:
    """Construit le module MOD-001 Camera Scout complet."""

    plaque = _build_plaque()

    # Positionner le support GoPro au centre de la plaque, sur la face superieure
    support = _build_gopro_mount()
    support = support.translate((0, 0, PLAQUE_EPAISSEUR / 2))

    # Union plaque + support
    piece = plaque.union(support)

    # Conges sur les aretes de la plaque de base
    if CONGE_PLAQUE > 0:
        try:
            # On applique les conges uniquement sur les aretes horizontales
            # de la plaque pour ne pas casser la geometrie du support
            piece = (
                piece
                .edges("|Z")
                .fillet(CONGE_PLAQUE)
            )
        except Exception:
            try:
                piece = piece.edges("|Z").fillet(CONGE_PLAQUE / 2)
            except Exception:
                pass

    return piece


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
    print("Construction du module MOD-001 Camera Scout...")
    piece = build_mod001()

    out_dir = Path(__file__).parent
    _export(piece, str(out_dir / "mod001_camera_scout.step"))
    _export(piece, str(out_dir / "mod001_camera_scout.stl"))
    print("Termine.")
