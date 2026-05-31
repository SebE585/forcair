#!/usr/bin/env python3
"""
Forcair — Jauge de press-fit roulement 608ZZ (maquette de faisabilite).

Barrette de coupons-test : chaque coupon reproduit le logement du roulement
du moyeu (wheel_hub.py) avec un diametre de poche different. On insere un
608ZZ dans chaque coupon ; celui qui donne le bon ajustement indique la
valeur a reporter dans BEARING_PRESS_FIT de wheel_hub.py.

Fidelite : paroi autour de la poche = WALL_MIN (2 mm), identique au moyeu reel,
pour que la rigidite radiale ressentie soit representative.

Chaque coupon :
  - poche borgne pour le roulement (profondeur = epaisseur 608ZZ)
  - trou d'ejection sous la poche (pour chasser le roulement apres test)
  - valeur de press-fit (en centiemes de mm) gravee devant lui sur la base

Imprimer en PLA (fond de bobine suffit) AVEC le meme nombre de perimetres
que le moyeu final, pour que le serrage soit comparable.

> Attention PLA vs PETG : la valeur trouvee en PLA est une excellente premiere
> approximation, a re-confirmer sur le vrai moyeu PETG (retrait et ductilite
> differents ; le PLA peut fendre si le serrage est trop fort, c'est normal).

Usage :
    python bearing_fit_test.py
"""
from __future__ import annotations

from pathlib import Path

import cadquery as cq

# =============================================================================
# Parametres
# =============================================================================

# Roulement 608ZZ (doit correspondre a wheel_hub.py)
BEARING_OD = 22.0            # Diametre exterieur du roulement
BEARING_ID = 8.0            # Diametre interieur (= diametre trou d'ejection)
BEARING_THICKNESS = 7.0     # Epaisseur du roulement

# Paroi autour de la poche (identique au moyeu : WALL_MIN)
WALL_MIN = 2.0

# Valeurs de press-fit testees (ajoutees a BEARING_OD ; negatif = serrage)
# -> poches : 21.80 / 21.90 / 22.00 / 22.05 / 22.10
PRESS_FITS = [-0.20, -0.10, 0.00, 0.05, 0.10]

# Geometrie coupon
COUPON_OD = BEARING_OD + 2 * WALL_MIN   # 26 mm (fidele au noyau du moyeu)
POCKET_DEPTH = BEARING_THICKNESS        # 7 mm
FLOOR = 2.0                             # fond sous la poche
COUPON_H = POCKET_DEPTH + FLOOR         # 9 mm
EJECT_DIA = BEARING_ID + 0.5           # trou d'ejection legerement > axe

# Base / barrette
BASE_T = 2.5
PITCH = 32.0
COUPON_Y = 6.0          # decalage coupon vers l'arriere
LABEL_Y = -10.0        # zone de gravure devant le coupon
LABEL_SIZE = 4.5
LABEL_DEPTH = 0.8

# Export
EXPORT_DIR = Path(__file__).resolve().parent
PART_NAME = "FIT-001_bearing_gauge"


# =============================================================================
# Export utils (meme pattern que les autres pieces)
# =============================================================================

def export_step(obj: cq.Workplane, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(obj, path)


def export_stl(obj: cq.Workplane, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(obj, path)


def _label(fit: float) -> str:
    """Etiquette en centiemes de mm : -0.20 -> '-20', 0.05 -> '+05', 0.0 -> '0'."""
    c = round(fit * 100)
    if c == 0:
        return "0"
    return f"+{c:02d}" if c > 0 else f"-{abs(c):02d}"


# =============================================================================
# Construction
# =============================================================================

def build_gauge() -> cq.Workplane:
    n = len(PRESS_FITS)
    base_l = PITCH * n
    base_w = 36.0
    top_z = BASE_T + COUPON_H

    # Base plate (de z=0 a z=BASE_T)
    result = (
        cq.Workplane("XY")
        .box(base_l, base_w, BASE_T, centered=(True, True, False))
    )

    for i, fit in enumerate(PRESS_FITS):
        cx = -base_l / 2 + PITCH * (i + 0.5)

        # Coupon cylindrique pose sur la base
        coupon = (
            cq.Workplane("XY")
            .workplane(offset=BASE_T)
            .center(cx, COUPON_Y)
            .circle(COUPON_OD / 2)
            .extrude(COUPON_H)
        )
        result = result.union(coupon)

        # Poche du roulement (borgne, depuis le haut)
        pocket_d = BEARING_OD + fit
        pocket = (
            cq.Workplane("XY")
            .workplane(offset=top_z - POCKET_DEPTH)
            .center(cx, COUPON_Y)
            .circle(pocket_d / 2)
            .extrude(POCKET_DEPTH + 0.1)
        )
        result = result.cut(pocket)

        # Trou d'ejection (du bas jusqu'au fond de la poche)
        eject = (
            cq.Workplane("XY")
            .center(cx, COUPON_Y)
            .circle(EJECT_DIA / 2)
            .extrude(top_z - POCKET_DEPTH + 0.1)
        )
        result = result.cut(eject)

        # Gravure de la valeur devant le coupon
        txt = _label(fit)
        try:
            engrave = (
                cq.Workplane("XY")
                .workplane(offset=BASE_T)
                .center(cx, LABEL_Y)
                .text(txt, LABEL_SIZE, -LABEL_DEPTH)
            )
            result = result.cut(engrave)
        except Exception:
            # Fallback infaillible : (i+1) rainures = index du coupon.
            # Correspondance imprimee dans la doc/console.
            for k in range(i + 1):
                groove = (
                    cq.Workplane("XY")
                    .workplane(offset=BASE_T)
                    .center(cx - (i) * 1.6 + k * 3.2, LABEL_Y)
                    .box(1.2, 6.0, LABEL_DEPTH * 2, centered=(True, True, True))
                )
                result = result.cut(groove)

    return result


# =============================================================================
# Point d'entree
# =============================================================================

if __name__ == "__main__":
    print(f"Construction de la jauge press-fit Forcair ({PART_NAME}) ...")
    print(f"  Roulement : 608ZZ (OD {BEARING_OD} x ep {BEARING_THICKNESS} mm)")
    print("  Coupons (valeur BEARING_PRESS_FIT -> diametre poche modele) :")
    for fit in PRESS_FITS:
        print(f"    {_label(fit):>4}  ->  {BEARING_OD + fit:.2f} mm")

    gauge = build_gauge()

    step_path = str(EXPORT_DIR / "step" / f"{PART_NAME}.step")
    stl_path = str(EXPORT_DIR / "stl" / f"{PART_NAME}.stl")
    export_step(gauge, step_path)
    export_stl(gauge, stl_path)
    print(f"  -> STEP : {step_path}")
    print(f"  -> STL  : {stl_path}")
    print("Termine.")
