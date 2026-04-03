#!/usr/bin/env python3
"""
Forcair — Moyeu de roue pour robot outdoor DIY.

Concu pour impression 3D en PETG.
Accepte un roulement 608ZZ en emmanchement serre (press-fit).
Le pneu TPU vient se clipser autour de la jante grace aux levres de retention.

Usage :
    python wheel_hub.py
"""
from __future__ import annotations

import math
from pathlib import Path

import cadquery as cq


# =============================================================================
# Parametres principaux (modifier ici pour personnaliser)
# =============================================================================

# Dimensions globales du moyeu
HUB_OUTER_DIAMETER = 80.0   # Diametre exterieur total (mm)
HUB_WIDTH = 20.0             # Largeur totale du moyeu (mm)

# Roulement 608ZZ
BEARING_OD = 22.0            # Diametre exterieur du roulement
BEARING_ID = 8.0             # Diametre interieur du roulement
BEARING_THICKNESS = 7.0      # Epaisseur du roulement
BEARING_PRESS_FIT = 0.05     # Serrage pour emmanchement (negatif = jeu)

# Jante et retention du pneu TPU
RIM_LIP_HEIGHT = 3.0         # Hauteur de la levre de retention de chaque cote
RIM_LIP_THICKNESS = 2.0      # Epaisseur de la levre de retention
TIRE_SEAT_DIAMETER = 76.0    # Diametre d'assise du pneu (entre les levres)

# Rayons (spokes)
SPOKE_COUNT = 6              # Nombre de rayons
SPOKE_WIDTH = 6.0            # Largeur angulaire du rayon (mm au rayon moyen)
SPOKE_THICKNESS = 4.0        # Epaisseur des rayons (dans la largeur du moyeu)

# Imprimabilite
FILLET_MIN = 1.0             # Conge minimum pour imprimabilite
FILLET_SPOKE = 1.5           # Conge a la base des rayons
WALL_MIN = 2.0               # Epaisseur de paroi minimum

# Export
EXPORT_DIR = Path(__file__).resolve().parent
PART_NAME = "WH-001_wheel_hub"


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
# Construction du moyeu
# =============================================================================

def _build_hub_core() -> cq.Workplane:
    """
    Noyau central du moyeu : cylindre plein avec logement pour le roulement.
    Le logement est centre dans la largeur du moyeu.
    """
    # Diametre du noyau = diametre du roulement + paroi minimum de chaque cote
    hub_core_od = BEARING_OD + 2 * WALL_MIN
    bearing_pocket_d = BEARING_OD + BEARING_PRESS_FIT  # Serrage

    # Cylindre plein du noyau
    core = (
        cq.Workplane("XY")
        .circle(hub_core_od / 2)
        .extrude(HUB_WIDTH)
    )

    # Logement du roulement (poche borgne centree)
    pocket_depth = BEARING_THICKNESS
    pocket_offset = (HUB_WIDTH - BEARING_THICKNESS) / 2  # Centrage

    # Poche cote face avant
    core = (
        core
        .faces(">Z")
        .workplane()
        .circle(bearing_pocket_d / 2)
        .cutBlind(-pocket_depth)
    )

    # Alesage central traversant pour l'axe
    core = (
        core
        .faces(">Z")
        .workplane()
        .circle(BEARING_ID / 2)
        .cutThruAll()
    )

    return core


def _build_rim_ring() -> cq.Workplane:
    """
    Anneau de jante avec levres de retention pour le pneu TPU.

    La section du pneu s'enroule autour de la jante. Les levres empechent
    le pneu de glisser lateralement.
    """
    outer_r = HUB_OUTER_DIAMETER / 2
    tire_seat_r = TIRE_SEAT_DIAMETER / 2

    # Corps principal de la jante (zone d'assise du pneu)
    rim_body_width = HUB_WIDTH - 2 * RIM_LIP_HEIGHT
    rim = (
        cq.Workplane("XY")
        .circle(outer_r)
        .circle(tire_seat_r)
        .extrude(HUB_WIDTH)
    )

    # Levres de retention — on les construit comme des anneaux supplementaires
    # Levre cote Z=0
    lip_bottom = (
        cq.Workplane("XY")
        .circle(outer_r)
        .circle(outer_r - RIM_LIP_THICKNESS)
        .extrude(RIM_LIP_HEIGHT)
    )

    # Levre cote Z=HUB_WIDTH
    lip_top = (
        cq.Workplane("XY")
        .circle(outer_r)
        .circle(outer_r - RIM_LIP_THICKNESS)
        .extrude(RIM_LIP_HEIGHT)
        .translate((0, 0, HUB_WIDTH - RIM_LIP_HEIGHT))
    )

    rim = rim.union(lip_bottom).union(lip_top)
    return rim


def _build_spokes() -> cq.Workplane:
    """
    Rayons reliant le noyau central a la jante.

    Les rayons sont des barres rectangulaires disposees radialement,
    centrees dans l'epaisseur du moyeu.
    """
    hub_core_od = BEARING_OD + 2 * WALL_MIN
    inner_r = hub_core_od / 2
    outer_r = TIRE_SEAT_DIAMETER / 2  # Les rayons rejoignent l'assise du pneu
    spoke_length = outer_r - inner_r

    # Epaisseur du rayon centree dans la largeur du moyeu
    spoke_z_offset = (HUB_WIDTH - SPOKE_THICKNESS) / 2

    # Construction d'un rayon unique (oriente selon +X)
    single_spoke = (
        cq.Workplane("XY")
        .transformed(offset=(inner_r + spoke_length / 2, 0, spoke_z_offset))
        .box(spoke_length, SPOKE_WIDTH, SPOKE_THICKNESS, centered=(True, True, False))
    )

    # Rotation pour creer tous les rayons
    all_spokes = single_spoke
    angle_step = 360.0 / SPOKE_COUNT
    for i in range(1, SPOKE_COUNT):
        rotated = single_spoke.rotate((0, 0, 0), (0, 0, 1), angle_step * i)
        all_spokes = all_spokes.union(rotated)

    return all_spokes


def build_wheel_hub() -> cq.Workplane:
    """
    Assemblage complet du moyeu de roue.

    Etapes :
    1. Construire le noyau central (logement roulement)
    2. Construire la jante avec levres
    3. Construire les rayons
    4. Union de l'ensemble
    5. Ajout des conges pour imprimabilite
    """
    core = _build_hub_core()
    rim = _build_rim_ring()
    spokes = _build_spokes()

    # Union des trois composants
    hub = core.union(rim).union(spokes)

    # Conges pour imprimabilite
    # On applique un conge global conservateur ; si ca echoue on continue sans
    if FILLET_MIN > 0:
        try:
            hub = hub.edges().fillet(FILLET_MIN)
        except Exception:
            # Le fillet global peut echouer sur certaines aretes complexes.
            # On essaie un conge plus petit en dernier recours.
            try:
                hub = hub.edges().fillet(FILLET_MIN * 0.5)
            except Exception:
                print("[AVERTISSEMENT] Conges non appliques — geometrie trop complexe.")

    return hub


# =============================================================================
# Point d'entree
# =============================================================================

if __name__ == "__main__":
    print(f"Construction du moyeu Forcair ({PART_NAME}) ...")
    print(f"  Diametre exterieur : {HUB_OUTER_DIAMETER} mm")
    print(f"  Largeur : {HUB_WIDTH} mm")
    print(f"  Roulement : 608ZZ ({BEARING_OD}x{BEARING_ID}x{BEARING_THICKNESS} mm)")
    print(f"  Rayons : {SPOKE_COUNT}")

    hub = build_wheel_hub()

    step_path = str(EXPORT_DIR / "step" / f"{PART_NAME}.step")
    stl_path = str(EXPORT_DIR / "stl" / f"{PART_NAME}.stl")

    export_step(hub, step_path)
    print(f"  -> STEP : {step_path}")

    export_stl(hub, stl_path)
    print(f"  -> STL  : {stl_path}")

    print("Termine.")
