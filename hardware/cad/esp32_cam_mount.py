#!/usr/bin/env python3
"""
Forcair — Support equerre pour module ESP32-CAM.

Equerre en L qui maintient le module ESP32-CAM a la verticale avec une
inclinaison de 15 degres vers l'avant pour un meilleur angle camera.
Le module glisse par le haut dans des rainures laterales.

La base se fixe sur la platine du robot via 2x vis M3.
Un degagement circulaire en face avant laisse passer l'objectif camera.
Un canal a l'arriere preserve le passage de l'antenne PCB.

Materiau cible : PETG (conges >= 1 mm pour bonne imprimabilite).

Usage :
    python esp32_cam_mount.py
    -> genere esp32_cam_mount.step et esp32_cam_mount.stl dans le meme repertoire.
"""
from __future__ import annotations

import math
from pathlib import Path

import cadquery as cq


# =============================================================================
# Parametres — dimensions du module ESP32-CAM
# =============================================================================

# Module ESP32-CAM (PCB)
BOARD_WIDTH = 27.0          # Largeur du PCB (mm)
BOARD_HEIGHT = 40.0         # Hauteur du PCB (mm)
BOARD_THICKNESS = 5.0       # Epaisseur du PCB + composants (mm)

# Jeux d'insertion
SLOT_CLEARANCE = 0.5        # Jeu lateral pour glissement du PCB (mm)
SLOT_DEPTH = 2.0            # Profondeur des rainures laterales (mm)

# Camera
CAMERA_HOLE_DIA = 10.0      # Diametre du percage pour l'objectif (mm)
# Le module camera est en haut du PCB, centre environ a 6 mm du bord superieur
CAMERA_OFFSET_FROM_TOP = 6.0  # Distance du centre camera au bord superieur

# Antenne — canal arriere
ANTENNA_CHANNEL_WIDTH = 18.0   # Largeur du canal antenne (mm)
ANTENNA_CHANNEL_DEPTH = 1.5    # Profondeur du canal antenne (mm)
# L'antenne PCB est en bas du module ; le canal demarre a environ 5 mm du bas
ANTENNA_CHANNEL_HEIGHT = 12.0  # Hauteur du canal (mm)
ANTENNA_OFFSET_FROM_BOTTOM = 2.0  # Decalage depuis le bas du PCB


# =============================================================================
# Parametres — equerre de fixation
# =============================================================================

# Base horizontale
BASE_LENGTH = 50.0          # Longueur de la base (mm)
BASE_WIDTH = 35.0           # Largeur (profondeur) de la base (mm)
BASE_THICKNESS = 3.0        # Epaisseur de la base (mm)

# Fixation a la platine robot — 2x vis M3
M3_HOLE_DIA = 3.4           # Percage de passage M3 (mm)
M3_SPACING = 40.0           # Entraxe des 2 trous M3 (mm)

# Partie verticale (mur porteur)
WALL_THICKNESS = 3.0        # Epaisseur du mur vertical (mm)
WALL_HEIGHT_EXTRA = 5.0     # Depassement au-dessus du PCB (mm)

# Inclinaison vers l'avant
TILT_ANGLE = 15.0           # Angle d'inclinaison (degres)

# Imprimabilite
FILLET_RADIUS = 1.5         # Rayon de conge general (mm)
FILLET_BASE_JUNCTION = 3.0  # Conge a la jonction base/mur (mm)


# =============================================================================
# Dimensions derivees
# =============================================================================

_slot_width = BOARD_WIDTH + SLOT_CLEARANCE   # Largeur interieure entre rainures
_wall_total_height = BOARD_HEIGHT + WALL_HEIGHT_EXTRA  # Hauteur du mur vertical
# Position Z du centre camera par rapport au bas du mur
_camera_z = _wall_total_height - CAMERA_OFFSET_FROM_TOP - WALL_HEIGHT_EXTRA / 2.0


# =============================================================================
# Fonctions utilitaires d'export
# =============================================================================

def export_step(obj: cq.Workplane, path: str) -> None:
    """Exporte un solide CadQuery au format STEP."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(obj, path)


def export_stl(obj: cq.Workplane, path: str) -> None:
    """Exporte un solide CadQuery au format STL."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(obj, path)


# =============================================================================
# Construction du support
# =============================================================================

def build_mount() -> cq.Workplane:
    """
    Construit le support equerre ESP32-CAM.

    Orientation :
    - La base est dans le plan XY, epaisseur selon Z.
    - Le mur vertical part du bord arriere (Y-) de la base et monte en Z.
    - L'inclinaison de 15 degres se fait autour de l'axe X (le mur penche
      vers Y+ / avant).
    - Le PCB est oriente face camera vers Y+ (avant du robot).
    """

    # --- 1. Base horizontale ---
    base = (
        cq.Workplane("XY")
        .box(BASE_LENGTH, BASE_WIDTH, BASE_THICKNESS)
        # Repositionner pour que le dessous soit a Z=0
        .translate((0, 0, BASE_THICKNESS / 2.0))
    )

    # Trous M3 dans la base (traversants)
    base = (
        base
        .faces(">Z")
        .workplane()
        .pushPoints([(-M3_SPACING / 2.0, 0), (M3_SPACING / 2.0, 0)])
        .hole(M3_HOLE_DIA, BASE_THICKNESS + 1)
    )

    # --- 2. Mur vertical (avant inclinaison) ---
    # Le mur est construit droit puis incline.
    # Largeur du mur = largeur necessaire pour les rainures + epaisseur exterieure
    mur_width = _slot_width + 2 * SLOT_DEPTH + 2 * WALL_THICKNESS
    mur_depth = WALL_THICKNESS + BOARD_THICKNESS + SLOT_DEPTH

    # Bloc principal du mur (construit a l'origine puis deplace)
    mur = (
        cq.Workplane("XY")
        .box(mur_width, mur_depth, _wall_total_height)
    )

    # --- 3. Rainures laterales pour glissement du PCB ---
    # Deux rainures symetriques, ouvertes vers le haut
    # Chaque rainure : profondeur SLOT_DEPTH, largeur = epaisseur du PCB + jeu
    slot_x_offset = _slot_width / 2.0 + SLOT_DEPTH / 2.0
    slot_y_offset = 0.0  # Centree en Y dans le mur

    for side in [-1, +1]:
        slot = (
            cq.Workplane("XY")
            .box(SLOT_DEPTH, BOARD_THICKNESS + SLOT_CLEARANCE, _wall_total_height + 2)
            .translate((side * slot_x_offset, slot_y_offset, 0))
        )
        mur = mur.cut(slot)

    # Evidement central entre les rainures (espace pour le PCB, ouvert devant)
    # On enleve la matiere entre les 2 rainures cote avant (Y+) pour que la
    # camera voie a travers et que le PCB soit accessible
    pcb_pocket = (
        cq.Workplane("XY")
        .box(_slot_width, BOARD_THICKNESS + SLOT_CLEARANCE, _wall_total_height + 2)
        .translate((0, 0, 0))
    )
    mur = mur.cut(pcb_pocket)

    # --- 4. Ouverture camera (percage circulaire cote avant) ---
    camera_z = _camera_z - _wall_total_height / 2.0  # Relatif au centre du mur
    camera_hole = (
        cq.Workplane("XZ")
        .center(0, -camera_z)
        .circle(CAMERA_HOLE_DIA / 2.0)
        .extrude(mur_depth, both=True)
    )
    mur = mur.cut(camera_hole)

    # --- 5. Canal antenne (face arriere, Y-) ---
    antenna_z = (ANTENNA_OFFSET_FROM_BOTTOM + ANTENNA_CHANNEL_HEIGHT / 2.0
                 - _wall_total_height / 2.0)
    antenna_channel = (
        cq.Workplane("XY")
        .box(ANTENNA_CHANNEL_WIDTH, ANTENNA_CHANNEL_DEPTH * 2, ANTENNA_CHANNEL_HEIGHT)
        .translate((0, -mur_depth / 2.0, antenna_z))
    )
    mur = mur.cut(antenna_channel)

    # --- 6. Conges sur le mur ---
    try:
        mur = mur.edges("|Z").fillet(FILLET_RADIUS)
    except Exception:
        pass

    # --- 7. Inclinaison du mur ---
    # Rotation autour de l'axe X de TILT_ANGLE degres (penche vers l'avant)
    # Puis translation pour poser sur le bord arriere de la base
    tilt_rad = math.radians(TILT_ANGLE)

    # Position du mur : le bas du mur repose sur la face superieure de la base,
    # au bord arriere (Y = -BASE_WIDTH/2 + mur_depth/2)
    mur_y = -BASE_WIDTH / 2.0 + mur_depth / 2.0
    mur_z = BASE_THICKNESS + _wall_total_height / 2.0

    # Appliquer la rotation autour de l'axe X passant par le pied du mur
    # 1) Translater le mur pour que le pied soit a l'origine
    # 2) Tourner
    # 3) Retranslater
    mur = (
        mur
        .translate((0, 0, _wall_total_height / 2.0))   # pied a Z=0
        .rotate((0, 0, 0), (1, 0, 0), TILT_ANGLE)      # inclinaison
        .translate((0, mur_y, BASE_THICKNESS))           # positionner sur la base
    )

    # --- 8. Assemblage base + mur ---
    mount = base.union(mur)

    # --- 9. Conge a la jonction base/mur pour solidite et imprimabilite ---
    try:
        mount = mount.edges("|X").edges("<Z").fillet(FILLET_BASE_JUNCTION)
    except Exception:
        # Le selecteur peut echouer selon la geometrie ; on tente un conge global
        try:
            mount = mount.edges().fillet(FILLET_RADIUS * 0.5)
        except Exception:
            pass

    return mount


# =============================================================================
# Point d'entree — generation des fichiers
# =============================================================================

if __name__ == "__main__":
    script_dir = str(Path(__file__).resolve().parent)

    print("=== Forcair — Generation du support ESP32-CAM ===")
    print(f"  Module ESP32-CAM : {BOARD_WIDTH}x{BOARD_HEIGHT}x{BOARD_THICKNESS} mm")
    print(f"  Inclinaison      : {TILT_ANGLE} degres")
    print(f"  Base             : {BASE_LENGTH}x{BASE_WIDTH}x{BASE_THICKNESS} mm")
    print(f"  Entraxe M3       : {M3_SPACING} mm")
    print(f"  Rainure PCB      : {_slot_width} mm (jeu {SLOT_CLEARANCE} mm)")
    print(f"  Percage camera   : diam {CAMERA_HOLE_DIA} mm")

    mount = build_mount()

    step_path = f"{script_dir}/esp32_cam_mount.step"
    stl_path = f"{script_dir}/esp32_cam_mount.stl"

    export_step(mount, step_path)
    print(f"  -> {step_path}")

    export_stl(mount, stl_path)
    print(f"  -> {stl_path}")

    print("=== Termine ===")
