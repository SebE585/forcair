#!/usr/bin/env python3
"""
Forcair — Support moteur parametrique pour profil aluminium 2020.

Le support se monte SOUS un profil 2020 (20x20 mm) via 2x ecrous en T M5.
Le moteur DC cylindrique repose dans un berceau en U ; un chapeau superieur
se visse avec 2x vis M3 pour serrer le moteur.
L'axe du moteur est perpendiculaire a la direction du profil (vers l'exterieur
pour le montage de la roue).

Materiau cible : PETG (conges >= 1 mm pour bonne imprimabilite).

Usage :
    python motor_mount.py
    -> genere motor_mount.step et motor_mount.stl dans le meme repertoire.
"""
from __future__ import annotations

from pathlib import Path

import cadquery as cq


# =============================================================================
# Parametres — a adapter selon le moteur recupere
# =============================================================================

# Moteur DC cylindrique
MOTOR_DIAMETER = 28.0       # Diametre exterieur du moteur (mm)
MOTOR_LENGTH = 40.0         # Longueur du corps moteur (mm)
MOTOR_CLEARANCE = 0.4       # Jeu autour du moteur pour insertion facile

# Profil aluminium 2020
PROFILE_WIDTH = 20.0        # Largeur du profil (mm)
PROFILE_SLOT_WIDTH = 6.0    # Largeur de la rainure du profil
PROFILE_SLOT_DEPTH = 6.0    # Profondeur de la rainure (pour centrage)

# Fixation au profil — 2x ecrous en T M5
M5_HOLE_DIA = 5.3           # Percage de passage M5
M5_SPACING = 20.0           # Entraxe des 2 trous M5 (le long du profil)

# Fixation du chapeau — 2x vis M3
M3_HOLE_DIA = 3.4           # Percage de passage M3 (corps)
M3_TAP_DIA = 2.5            # Percage pour taraudage M3 (berceau)
M3_HEAD_DIA = 6.0           # Diametre de la tete fraisee / cylindrique M3
M3_HEAD_DEPTH = 3.5         # Logement de la tete M3

# Epaisseurs de paroi
WALL_THICKNESS = 3.5        # Epaisseur generale des parois
CRADLE_FLOOR = 3.0          # Epaisseur sous le moteur (fond du berceau)

# Imprimabilite
FILLET_RADIUS = 1.0         # Rayon de conge minimum


# =============================================================================
# Dimensions derivees
# =============================================================================

_motor_r = (MOTOR_DIAMETER + MOTOR_CLEARANCE) / 2.0

# Dimensions globales du berceau (partie basse)
CRADLE_WIDTH = MOTOR_DIAMETER + MOTOR_CLEARANCE + 2 * WALL_THICKNESS
CRADLE_DEPTH = MOTOR_LENGTH + MOTOR_CLEARANCE + 2 * WALL_THICKNESS
CRADLE_HEIGHT = _motor_r + CRADLE_FLOOR

# La platine de fixation au profil est au sommet du berceau
PLATE_WIDTH = max(CRADLE_WIDTH, M5_SPACING + M5_HOLE_DIA + 2 * WALL_THICKNESS)
PLATE_DEPTH = CRADLE_DEPTH
PLATE_HEIGHT = WALL_THICKNESS

# Chapeau (clamp superieur)
CAP_WIDTH = CRADLE_WIDTH
CAP_DEPTH = CRADLE_DEPTH
CAP_HEIGHT = _motor_r + WALL_THICKNESS

# Entraxe des vis M3 du chapeau (symetrique en profondeur)
M3_SPACING_DEPTH = MOTOR_LENGTH * 0.6


# =============================================================================
# Fonctions utilitaires d'export (meme patron que blindair/cad/cq/common.py)
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
# Construction du berceau (partie basse fixee au profil)
# =============================================================================

def build_cradle() -> cq.Workplane:
    """
    Construit le berceau en U + platine de fixation au profil 2020.

    La platine est en haut (contre le profil) ; le berceau pend vers le bas.
    Le moteur est oriente selon l'axe Y (perpendiculaire au profil qui suit X).
    """

    # --- Bloc de base : platine + corps du berceau ---
    total_height = PLATE_HEIGHT + CRADLE_HEIGHT
    part = (
        cq.Workplane("XY")
        .box(PLATE_WIDTH, PLATE_DEPTH, total_height)
    )

    # --- Alésage cylindrique pour le moteur ---
    # Le cylindre moteur est oriente selon Y, centre dans le berceau.
    # Le centre du cylindre est a mi-hauteur du berceau (sous la platine).
    cylinder_center_z = -(PLATE_HEIGHT / 2.0) + (CRADLE_HEIGHT - _motor_r)
    # On perce a travers toute la profondeur
    motor_hole = (
        cq.Workplane("XZ")
        .center(0, -cylinder_center_z)
        .circle(_motor_r)
        .extrude(PLATE_DEPTH / 2.0, both=True)
    )
    part = part.cut(motor_hole)

    # --- Ouverture du U : enlever la matiere au-dessus du moteur ---
    # On decoupe un rectangle au-dessus du cylindre pour creer la forme en U
    cut_width = MOTOR_DIAMETER + MOTOR_CLEARANCE
    cut_height = total_height - PLATE_HEIGHT - (_motor_r - _motor_r * 0.3)
    if cut_height > 0:
        u_cut = (
            cq.Workplane("XY")
            .center(0, 0)
            .rect(cut_width, MOTOR_LENGTH + MOTOR_CLEARANCE)
            .extrude(cut_height)
            .translate((0, 0, total_height / 2.0 - PLATE_HEIGHT - cut_height))
        )
        part = part.cut(u_cut)

    # --- Trous M5 pour fixation au profil (sur la face superieure) ---
    part = (
        part
        .faces(">Z")
        .workplane()
        .pushPoints([(- M5_SPACING / 2.0, 0), (M5_SPACING / 2.0, 0)])
        .hole(M5_HOLE_DIA, PLATE_HEIGHT + CRADLE_FLOOR + 2)
    )

    # --- Ergot de centrage dans la rainure du profil ---
    # Un petit tenon rectangulaire sur la face superieure s'insere dans
    # la rainure du 2020 pour un positionnement precis.
    key_height = 2.0
    key_clearance = 0.3
    key_width = PROFILE_SLOT_WIDTH - key_clearance
    key_length = M5_SPACING + M5_HOLE_DIA + 4
    key = (
        cq.Workplane("XY")
        .box(key_length, key_width, key_height)
        .translate((0, 0, total_height / 2.0 + key_height / 2.0))
    )
    part = part.union(key)

    # --- Trous de vis M3 (taraudage) pour le chapeau ---
    # Places de chaque cote du berceau, traversant les oreilles laterales
    m3_x = CRADLE_WIDTH / 2.0  # au bord des parois laterales
    m3_points = [
        (m3_x, -M3_SPACING_DEPTH / 2.0),
        (m3_x, M3_SPACING_DEPTH / 2.0),
        (-m3_x, -M3_SPACING_DEPTH / 2.0),
        (-m3_x, M3_SPACING_DEPTH / 2.0),
    ]
    # Les trous M3 partent du bas du berceau vers le haut, dans les oreilles
    part = (
        part
        .faces("<Z")
        .workplane()
        .pushPoints(m3_points)
        .hole(M3_TAP_DIA, CRADLE_HEIGHT)
    )

    # --- Conges pour imprimabilite ---
    try:
        part = part.edges("|Y").fillet(FILLET_RADIUS)
    except Exception:
        pass

    return part


# =============================================================================
# Construction du chapeau (clamp superieur)
# =============================================================================

def build_cap() -> cq.Workplane:
    """
    Construit le chapeau qui vient serrer le moteur par le dessous.

    Le chapeau se visse sur le berceau avec 4x vis M3.
    Il contient un demi-cylindre concave qui epouse le moteur.
    """

    part = (
        cq.Workplane("XY")
        .box(CAP_WIDTH, CAP_DEPTH, CAP_HEIGHT)
    )

    # --- Demi-cylindre concave pour le moteur ---
    cap_cyl_z = CAP_HEIGHT / 2.0 - WALL_THICKNESS
    motor_cut = (
        cq.Workplane("XZ")
        .center(0, -cap_cyl_z)
        .circle(_motor_r)
        .extrude(CAP_DEPTH / 2.0, both=True)
    )
    part = part.cut(motor_cut)

    # --- Trous de passage M3 avec logement de tete ---
    m3_x = CRADLE_WIDTH / 2.0
    m3_points = [
        (m3_x, -M3_SPACING_DEPTH / 2.0),
        (m3_x, M3_SPACING_DEPTH / 2.0),
        (-m3_x, -M3_SPACING_DEPTH / 2.0),
        (-m3_x, M3_SPACING_DEPTH / 2.0),
    ]
    part = (
        part
        .faces(">Z")
        .workplane()
        .pushPoints(m3_points)
        .hole(M3_HOLE_DIA, CAP_HEIGHT + 1)
    )

    # Logements de tete M3 (lamages)
    part = (
        part
        .faces(">Z")
        .workplane()
        .pushPoints(m3_points)
        .hole(M3_HEAD_DIA, M3_HEAD_DEPTH)
    )

    # --- Conges pour imprimabilite ---
    try:
        part = part.edges("|Y").fillet(FILLET_RADIUS)
    except Exception:
        pass

    return part


# =============================================================================
# Point d'entree — generation des fichiers
# =============================================================================

if __name__ == "__main__":
    script_dir = str(Path(__file__).resolve().parent)

    print("=== Forcair — Generation du support moteur ===")
    print(f"  Moteur : diam {MOTOR_DIAMETER} mm, long {MOTOR_LENGTH} mm")
    print(f"  Profil : 2020 ({PROFILE_WIDTH}x{PROFILE_WIDTH} mm)")

    # --- Berceau ---
    cradle = build_cradle()
    cradle_step = f"{script_dir}/motor_mount_cradle.step"
    cradle_stl = f"{script_dir}/motor_mount_cradle.stl"
    export_step(cradle, cradle_step)
    export_stl(cradle, cradle_stl)
    print(f"  -> {cradle_step}")
    print(f"  -> {cradle_stl}")

    # --- Chapeau ---
    cap = build_cap()
    cap_step = f"{script_dir}/motor_mount_cap.step"
    cap_stl = f"{script_dir}/motor_mount_cap.stl"
    export_step(cap, cap_step)
    export_stl(cap, cap_stl)
    print(f"  -> {cap_step}")
    print(f"  -> {cap_stl}")

    print("=== Termine ===")
