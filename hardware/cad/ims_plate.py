#!/usr/bin/env python3
"""
IMS — Interface Module Standard pour le robot Forcair.

Plaque standardisee qui connecte les modules outils interchangeables
(brosse, camera, spray) au chariot de l'axe Z.

Materiau cible : PETG (impression 3D FDM).
Usage : python ims_plate.py
"""
from __future__ import annotations

from pathlib import Path

import cadquery as cq

# -----------------------------------------------------------------------------
# Parametres principaux (modifier ici)
# -----------------------------------------------------------------------------

# Plaque de base
PLAQUE_LONGUEUR = 100.0       # mm — axe X
PLAQUE_LARGEUR = 80.0         # mm — axe Y
PLAQUE_EPAISSEUR = 5.0        # mm — axe Z

# Trous de fixation M5 (boulons a ailettes)
M5_DIAMETRE = 5.3             # mm — jeu pour M5 (passage libre)
M5_ECART_X = 80.0             # mm — entraxe sur l'axe long
M5_ECART_Y = 60.0             # mm — entraxe sur l'axe court

# Plots de centrage (face superieure -> chariot Z)
PLOT_DIAMETRE = 8.0            # mm
PLOT_HAUTEUR = 6.0             # mm
PLOT_ECART_X = 60.0            # mm — entraxe entre les deux plots
PLOT_ECART_Y = 0.0             # mm — centres sur l'axe Y

# Trous de reception centrage (face inferieure -> modules)
RECEPTION_DIAMETRE = 8.2       # mm — leger jeu pour insertion
RECEPTION_PROFONDEUR = 6.0     # mm
RECEPTION_ECART_X = 60.0       # mm
RECEPTION_ECART_Y = 0.0        # mm

# Passage connecteur XT60 (alimentation)
XT60_LARGEUR = 30.0            # mm — axe X
XT60_HAUTEUR = 15.0            # mm — axe Y
XT60_OFFSET_X = 0.0            # mm — decalage lateral depuis le centre du bord

# Passage connecteur JST-XH 3 broches (signal)
JST_LARGEUR = 10.0             # mm — axe X
JST_HAUTEUR = 8.0              # mm — axe Y
JST_OFFSET_X = -15.0           # mm — decale vers la gauche par rapport au centre

# Conges pour imprimabilite
CONGE_ARETES = 1.0             # mm


# -----------------------------------------------------------------------------
# Construction de la piece
# -----------------------------------------------------------------------------

def build_ims_plate() -> cq.Workplane:
    """Construit la plaque IMS complete."""

    # --- Plaque de base centree sur l'origine ---
    plaque = (
        cq.Workplane("XY")
        .box(PLAQUE_LONGUEUR, PLAQUE_LARGEUR, PLAQUE_EPAISSEUR)
    )

    # --- Trous de fixation M5 (traversants, symetriques) ---
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

    # --- Plots de centrage sur la face superieure ---
    positions_plots = [
        ( PLOT_ECART_X / 2, PLOT_ECART_Y / 2),
        (-PLOT_ECART_X / 2, -PLOT_ECART_Y / 2),
    ]
    plaque = (
        plaque
        .faces(">Z")
        .workplane()
        .pushPoints(positions_plots)
        .circle(PLOT_DIAMETRE / 2)
        .extrude(PLOT_HAUTEUR)
    )

    # --- Trous de reception centrage sur la face inferieure ---
    positions_reception = [
        ( RECEPTION_ECART_X / 2, RECEPTION_ECART_Y / 2),
        (-RECEPTION_ECART_X / 2, -RECEPTION_ECART_Y / 2),
    ]
    plaque = (
        plaque
        .faces("<Z")
        .workplane()
        .pushPoints(positions_reception)
        .hole(RECEPTION_DIAMETRE, RECEPTION_PROFONDEUR)
    )

    # --- Decoupes connecteurs sur le bord court (+Y) ---
    bord_y = PLAQUE_LARGEUR / 2  # position du bord

    # Passage XT60 — decoupe rectangulaire traversante sur le bord
    xt60 = (
        cq.Workplane("XY")
        .box(XT60_LARGEUR, XT60_HAUTEUR, PLAQUE_EPAISSEUR)
        .translate((XT60_OFFSET_X, bord_y - XT60_HAUTEUR / 2, 0))
    )
    plaque = plaque.cut(xt60)

    # Passage JST-XH — decoupe rectangulaire traversante sur le meme bord
    jst = (
        cq.Workplane("XY")
        .box(JST_LARGEUR, JST_HAUTEUR, PLAQUE_EPAISSEUR)
        .translate((JST_OFFSET_X, bord_y - JST_HAUTEUR / 2, 0))
    )
    plaque = plaque.cut(jst)

    # --- Conges sur toutes les aretes pour imprimabilite ---
    if CONGE_ARETES > 0:
        try:
            plaque = plaque.edges().fillet(CONGE_ARETES)
        except Exception:
            # Certaines aretes tres courtes peuvent refuser le conge ;
            # on tente un rayon reduit en fallback.
            try:
                plaque = plaque.edges().fillet(CONGE_ARETES / 2)
            except Exception:
                pass  # on garde la geometrie sans conge plutot que de planter

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
    print("Construction de la plaque IMS Forcair...")
    piece = build_ims_plate()

    out_dir = Path(__file__).parent
    _export(piece, str(out_dir / "ims_plate.step"))
    _export(piece, str(out_dir / "ims_plate.stl"))
    print("Termine.")
