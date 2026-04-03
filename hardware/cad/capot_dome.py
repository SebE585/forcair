#!/usr/bin/env python3
"""
Forcair — Capot dome de protection electronique.

Coque protectrice en forme de dome aplati (flat-top) avec bords arrondis.
Se pose par-dessus la plaque de base pour couvrir l'electronique embarquee.
Prevu pour impression en PETG translucide bleu.

Caracteristiques :
  - Coque creuse (epaisseur de paroi parametrique)
  - Fond ouvert, fixation par 4 clips snap-fit
  - Fentes de ventilation avec lamelles inclinees (anti-pluie)
  - Passage de cable a l'arriere

Materiau cible : PETG translucide (conges partout pour imprimabilite).

Usage :
    python capot_dome.py
    -> genere capot_dome.step et capot_dome.stl dans le meme repertoire.
"""
from __future__ import annotations

from pathlib import Path

import cadquery as cq


# =============================================================================
# Parametres generaux
# =============================================================================

# Dimensions de l'empreinte au sol (mm)
BASE_LENGTH = 220.0         # Longueur (axe X)
BASE_WIDTH = 150.0          # Largeur (axe Y)
DOME_HEIGHT = 45.0          # Hauteur totale du capot

# Epaisseur de coque
WALL_THICKNESS = 2.0        # Epaisseur de paroi (mm)

# Conges (arrondis)
FILLET_TOP = 15.0           # Rayon de conge sur les aretes du dessus
FILLET_BOTTOM = 8.0         # Rayon de conge sur les aretes du bas
FILLET_INNER = 1.0          # Conge interieur pour imprimabilite

# =============================================================================
# Clips snap-fit (4x, face interne du bord inferieur)
# =============================================================================
CLIP_WIDTH = 5.0            # Largeur du clip (mm)
CLIP_HEIGHT = 3.0           # Hauteur du crochet (mm)
CLIP_DEPTH = 2.0            # Profondeur de la languette (mm)
CLIP_RAMP = 1.5             # Hauteur de la rampe d'insertion
CLIP_INSET = 30.0           # Distance des clips depuis les coins (le long du grand cote)

# =============================================================================
# Fentes de ventilation (face courte, cote +X)
# =============================================================================
VENT_COUNT = 6              # Nombre de fentes
VENT_WIDTH = 3.0            # Largeur de chaque fente (mm)
VENT_LENGTH = 20.0          # Longueur verticale de chaque fente (mm)
VENT_SPACING = 6.0          # Espacement entre fentes (centre a centre = VENT_WIDTH + VENT_SPACING)
VENT_Z_OFFSET = 10.0        # Decalage vertical depuis le bas
VENT_LOUVER_OFFSET = 2.0    # Decalage des lamelles (inclinaison anti-pluie)

# =============================================================================
# Passage de cable (face arriere, cote -X)
# =============================================================================
CABLE_WIDTH = 20.0          # Largeur du passage (mm)
CABLE_HEIGHT = 10.0         # Hauteur du passage (mm)
CABLE_Z_OFFSET = 5.0        # Distance depuis le bord inferieur
CABLE_FILLET = 1.5          # Conge du passage de cable


# =============================================================================
# Construction du capot
# =============================================================================

def _build_outer_shell() -> cq.Workplane:
    """Construit le volume exterieur du dome avec conges."""
    outer = (
        cq.Workplane("XY")
        .box(BASE_LENGTH, BASE_WIDTH, DOME_HEIGHT, centered=(True, True, False))
    )
    # Conges sur les aretes verticales d'abord
    outer = outer.edges("|Z").fillet(FILLET_BOTTOM)
    # Conges sur les aretes du dessus
    outer = outer.edges(">Z").fillet(FILLET_TOP)
    return outer


def _build_inner_cavity() -> cq.Workplane:
    """Construit le volume interieur (a soustraire) pour creer la coque."""
    inner_l = BASE_LENGTH - 2 * WALL_THICKNESS
    inner_w = BASE_WIDTH - 2 * WALL_THICKNESS
    inner_h = DOME_HEIGHT  # On depasse vers le bas pour ouvrir le fond

    inner = (
        cq.Workplane("XY")
        .box(inner_l, inner_w, inner_h, centered=(True, True, False))
    )
    # Conges interieurs harmonises (un peu plus petits que l'exterieur)
    fillet_v = max(FILLET_BOTTOM - WALL_THICKNESS, FILLET_INNER)
    fillet_t = max(FILLET_TOP - WALL_THICKNESS, FILLET_INNER)
    inner = inner.edges("|Z").fillet(fillet_v)
    inner = inner.edges(">Z").fillet(fillet_t)
    # Decaler vers le bas pour ouvrir le fond
    inner = inner.translate((0, 0, -WALL_THICKNESS))
    return inner


def _build_clip(index: int) -> cq.Workplane:
    """
    Construit un clip snap-fit individuel.

    Les clips sont positionnes sur les grands cotes (axe X),
    index 0-1 sur le cote -Y, index 2-3 sur le cote +Y.
    """
    # Profil du clip : une languette avec un crochet en bas
    # Le clip pend depuis le bord inferieur vers l'interieur
    clip = (
        cq.Workplane("XZ")
        .moveTo(0, 0)
        .lineTo(CLIP_DEPTH, 0)
        .lineTo(CLIP_DEPTH, -(CLIP_HEIGHT + CLIP_RAMP))
        .lineTo(0, -CLIP_HEIGHT)
        .close()
        .extrude(CLIP_WIDTH)
        .translate((0, 0, -CLIP_WIDTH / 2))
    )

    # Rotation pour orienter vers l'interieur du capot
    # et positionnement selon l'index
    half_l = BASE_LENGTH / 2 - CLIP_INSET
    half_w = BASE_WIDTH / 2 - WALL_THICKNESS

    positions = [
        (-half_l, -half_w, 0, 0),    # Coin avant-gauche
        (half_l, -half_w, 0, 0),     # Coin avant-droit
        (-half_l, half_w, 0, 180),   # Coin arriere-gauche
        (half_l, half_w, 0, 180),    # Coin arriere-droit
    ]

    x, y, z, angle = positions[index]

    if angle == 180:
        clip = clip.mirror("XZ")

    clip = clip.translate((x, y, z))
    return clip


def _build_vent_slot(slot_index: int) -> cq.Workplane:
    """
    Construit une fente de ventilation avec lamelle inclinee.

    Les fentes sont placees sur la face courte +X.
    La lamelle est decalee pour empecher l'entree d'eau.
    """
    # Calcul de la position Y centree
    total_span = (VENT_COUNT - 1) * (VENT_WIDTH + VENT_SPACING)
    y_start = -total_span / 2
    y_pos = y_start + slot_index * (VENT_WIDTH + VENT_SPACING)

    z_bottom = VENT_Z_OFFSET
    z_top = VENT_Z_OFFSET + VENT_LENGTH

    # Decoupe traversante (a travers la paroi) avec forme de parallelogramme
    # pour l'effet lamelle inclinee
    slot = (
        cq.Workplane("YZ")
        .moveTo(y_pos, z_bottom)
        .lineTo(y_pos + VENT_WIDTH, z_bottom + VENT_LOUVER_OFFSET)
        .lineTo(y_pos + VENT_WIDTH, z_top + VENT_LOUVER_OFFSET)
        .lineTo(y_pos, z_top)
        .close()
        .extrude(WALL_THICKNESS * 3)  # Assez pour traverser la paroi
    )
    # Positionner sur la face +X
    slot = slot.translate((BASE_LENGTH / 2 - WALL_THICKNESS * 1.5, 0, 0))
    return slot


def _build_cable_cutout() -> cq.Workplane:
    """
    Construit le passage de cable sur la face arriere (-X).
    """
    cutout = (
        cq.Workplane("YZ")
        .rect(CABLE_WIDTH, CABLE_HEIGHT)
        .extrude(WALL_THICKNESS * 3)
    )
    # Conge sur les aretes pour reduire les concentrations de contrainte
    try:
        cutout = cutout.edges().fillet(CABLE_FILLET)
    except Exception:
        pass

    # Centrer sur la face -X, decale du bas
    cutout = cutout.translate((
        -(BASE_LENGTH / 2 - WALL_THICKNESS * 1.5),
        0,
        CABLE_Z_OFFSET + CABLE_HEIGHT / 2,
    ))
    return cutout


def build_capot_dome() -> cq.Workplane:
    """
    Assemblage complet du capot dome.

    Etapes :
      1. Volume exterieur avec conges
      2. Evidement interieur (coque)
      3. Ajout des clips snap-fit
      4. Decoupe des fentes de ventilation
      5. Decoupe du passage de cable
    """
    # --- 1. Coque de base ---
    capot = _build_outer_shell()
    cavity = _build_inner_cavity()
    capot = capot.cut(cavity)

    # --- 2. Clips snap-fit (4x) ---
    for i in range(4):
        clip = _build_clip(i)
        capot = capot.union(clip)

    # --- 3. Fentes de ventilation (6x) ---
    for i in range(VENT_COUNT):
        slot = _build_vent_slot(i)
        capot = capot.cut(slot)

    # --- 4. Passage de cable ---
    cable = _build_cable_cutout()
    capot = capot.cut(cable)

    # --- 5. Conges finaux pour imprimabilite ---
    try:
        capot = capot.edges("<Z").fillet(FILLET_INNER)
    except Exception:
        pass  # Certaines aretes peuvent etre trop courtes pour le conge

    return capot


# =============================================================================
# Export
# =============================================================================

def _export(obj: cq.Workplane, name: str) -> None:
    """Exporte en STEP et STL dans le repertoire du script."""
    out_dir = Path(__file__).parent
    step_path = out_dir / f"{name}.step"
    stl_path = out_dir / f"{name}.stl"

    step_path.parent.mkdir(parents=True, exist_ok=True)

    cq.exporters.export(obj, str(step_path))
    print(f"  STEP -> {step_path}")

    cq.exporters.export(obj, str(stl_path), exportType="STL")
    print(f"  STL  -> {stl_path}")


if __name__ == "__main__":
    print("Forcair — Construction du capot dome...")
    capot = build_capot_dome()
    _export(capot, "capot_dome")
    print("Termine.")
