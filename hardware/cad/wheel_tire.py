#!/usr/bin/env python3
"""
Forcair — Pneu TPU pour robot outdoor DIY.

Concu pour impression 3D en TPU 95A (flexible).
Se clipse sur la jante du moyeu (wheel_hub.py) grace a une levre d'interference.
Sculpture transversale pour adherence sur paves mouilles et mousse.

Usage :
    python wheel_tire.py
"""
from __future__ import annotations

import math
from pathlib import Path

import cadquery as cq


# =============================================================================
# Parametres principaux (modifier ici pour personnaliser)
# =============================================================================

# Dimensions globales du pneu
TIRE_OD = 80.0               # Diametre exterieur total (mm)
TIRE_ID = 76.5                # Diametre interieur — assise jante (76mm) + 0.5mm tolerance TPU
TIRE_WIDTH = 25.0             # Largeur du pneu (mm)

# Epaisseur de paroi calculee
TIRE_WALL = (TIRE_OD - TIRE_ID) / 2  # ~6 mm

# Levre d'interference pour clipser sur la jante
LIP_HEIGHT = 1.0              # Saillie radiale de la levre vers l'interieur (mm)
LIP_WIDTH = 2.0               # Largeur axiale de la levre (mm)
LIP_OFFSET = 2.0              # Retrait axial depuis chaque bord (mm)

# Sculpture (tread pattern) — rainures transversales
GROOVE_DEPTH = 2.0            # Profondeur des rainures (mm)
GROOVE_WIDTH = 3.0            # Largeur axiale de chaque rainure (mm)
GROOVE_SPACING = 8.0          # Espacement entre rainures (pas, mm)

# Chanfreins sur les aretes de la bande de roulement (imprimabilite TPU)
TREAD_CHAMFER = 0.8           # Chanfrein lateral (mm)

# Impression 3D TPU
LAYER_HEIGHT = 0.2            # Hauteur de couche recommandee (mm) — info seulement
INFILL_PERCENT = 100          # Remplissage recommande (%) — info seulement

# Export
EXPORT_DIR = Path(__file__).resolve().parent
PART_NAME = "WT-001_wheel_tire"


# =============================================================================
# Fonctions utilitaires d'export (meme pattern que blindair/cad/cq/common.py)
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
# Construction du pneu
# =============================================================================

def _build_tire_body() -> cq.Workplane:
    """
    Corps principal du pneu : anneau cylindrique creux.

    Diametre exterieur = TIRE_OD, diametre interieur = TIRE_ID.
    Largeur = TIRE_WIDTH, extrude selon Z.
    """
    tire = (
        cq.Workplane("XY")
        .circle(TIRE_OD / 2)
        .circle(TIRE_ID / 2)
        .extrude(TIRE_WIDTH)
    )
    return tire


def _build_interference_lips() -> cq.Workplane:
    """
    Levres d'interference sur la surface interieure du pneu.

    Deux anneaux fins depassant vers l'interieur, places pres de chaque bord.
    Permettent un clipsage elastique sur la jante du moyeu.
    """
    lip_od = TIRE_ID  # Affleurant avec la surface interieure
    lip_id = TIRE_ID - 2 * LIP_HEIGHT  # Depasse vers l'interieur

    # Levre cote Z = LIP_OFFSET
    lip_bottom = (
        cq.Workplane("XY")
        .transformed(offset=(0, 0, LIP_OFFSET))
        .circle(lip_od / 2)
        .circle(lip_id / 2)
        .extrude(LIP_WIDTH)
    )

    # Levre cote Z = TIRE_WIDTH - LIP_OFFSET - LIP_WIDTH
    lip_top_z = TIRE_WIDTH - LIP_OFFSET - LIP_WIDTH
    lip_top = (
        cq.Workplane("XY")
        .transformed(offset=(0, 0, lip_top_z))
        .circle(lip_od / 2)
        .circle(lip_id / 2)
        .extrude(LIP_WIDTH)
    )

    return lip_bottom.union(lip_top)


def _cut_tread_grooves(tire: cq.Workplane) -> cq.Workplane:
    """
    Decoupe des rainures transversales dans la bande de roulement.

    Les rainures sont des entailles radiales sur la surface exterieure,
    reparties regulierement le long de la circonference.
    Chaque rainure est une fente qui traverse toute la largeur du pneu.
    """
    outer_r = TIRE_OD / 2
    groove_bottom_r = outer_r - GROOVE_DEPTH

    # Nombre de rainures sur la circonference
    circumference = math.pi * TIRE_OD
    num_grooves = int(circumference / GROOVE_SPACING)

    # Construction d'une rainure unique : petite boite radiale
    # On la place a la surface exterieure et on la duplique par rotation
    groove_radial_length = GROOVE_DEPTH + 1.0  # Debordement pour coupe propre
    groove_center_r = outer_r - GROOVE_DEPTH / 2 + 0.5

    single_groove = (
        cq.Workplane("XY")
        .transformed(offset=(groove_center_r, 0, TIRE_WIDTH / 2))
        .box(groove_radial_length, GROOVE_WIDTH, TIRE_WIDTH, centered=(True, True, True))
    )

    # Decoupe de toutes les rainures par rotation
    angle_step = 360.0 / num_grooves
    for i in range(num_grooves):
        groove_i = single_groove.rotate((0, 0, 0), (0, 0, 1), angle_step * i)
        tire = tire.cut(groove_i)

    return tire


def _apply_tread_chamfers(tire: cq.Workplane) -> cq.Workplane:
    """
    Chanfreins sur les aretes laterales de la bande de roulement.

    Facilite l'impression TPU et evite le decollement des bords.
    On chanfreine les aretes circulaires aux deux extremites du pneu,
    cote exterieur uniquement.
    """
    outer_r = TIRE_OD / 2

    try:
        # Selectionner les aretes circulaires sur les faces Z extremes,
        # filtrees par rayon (aretes exterieures seulement)
        tire = (
            tire
            .faces(">Z").edges("%Circle")
            .filter(lambda e: abs(e.radius() - outer_r) < 1.0)
            .chamfer(TREAD_CHAMFER)
        )
    except Exception:
        pass

    try:
        tire = (
            tire
            .faces("<Z").edges("%Circle")
            .filter(lambda e: abs(e.radius() - outer_r) < 1.0)
            .chamfer(TREAD_CHAMFER)
        )
    except Exception:
        pass

    return tire


def build_wheel_tire() -> cq.Workplane:
    """
    Assemblage complet du pneu TPU.

    Etapes :
    1. Construire le corps annulaire principal
    2. Ajouter les levres d'interference interieures
    3. Decouper la sculpture (rainures transversales)
    4. Appliquer les chanfreins pour imprimabilite
    """
    # 1 — Corps principal
    tire = _build_tire_body()

    # 2 — Levres d'interference
    lips = _build_interference_lips()
    tire = tire.union(lips)

    # 3 — Sculpture transversale
    tire = _cut_tread_grooves(tire)

    # 4 — Chanfreins sur les bords de la bande de roulement
    tire = _apply_tread_chamfers(tire)

    return tire


# =============================================================================
# Point d'entree
# =============================================================================

if __name__ == "__main__":
    print(f"Construction du pneu Forcair ({PART_NAME}) ...")
    print(f"  Diametre exterieur : {TIRE_OD} mm")
    print(f"  Diametre interieur : {TIRE_ID} mm")
    print(f"  Epaisseur de paroi : {TIRE_WALL} mm")
    print(f"  Largeur : {TIRE_WIDTH} mm")
    print(f"  Materiau : TPU 95A")
    print(f"  Sculpture : rainures {GROOVE_WIDTH} mm x {GROOVE_DEPTH} mm, pas {GROOVE_SPACING} mm")
    print(f"  Levres d'interference : saillie {LIP_HEIGHT} mm")

    tire = build_wheel_tire()

    step_path = str(EXPORT_DIR / "step" / f"{PART_NAME}.step")
    stl_path = str(EXPORT_DIR / "stl" / f"{PART_NAME}.stl")

    export_step(tire, step_path)
    print(f"  -> STEP : {step_path}")

    export_stl(tire, stl_path)
    print(f"  -> STL  : {stl_path}")

    print("Termine.")
