"""Surfaces of wall finishes, computed on a 1 cm grid from the villa elevations (projects/dossier-technique/tools/data.py).

Zones painted in order; later finishes override earlier ones; openings with a known height are removed; full-height
furniture boxes (bibliothèques, dressing) are removed from the cladding they stand in front of. All results are
≈ (heights and most widths are relevés). Openings without a height cannot be removed: they are reported.
"""
import importlib.util
import pathlib
import sys

import numpy as np

VT = pathlib.Path(__file__).resolve().parents[2] / "dossier-technique/tools"
sys.path.insert(0, str(VT))
_s = importlib.util.spec_from_file_location("villa_data", VT / "data.py")
D = importlib.util.module_from_spec(_s)
_s.loader.exec_module(D)

BASE = {"enduit": "panneau", "panneau": "panneau"}
FULL_BOX_REMOVE = {"M3 — bibliothèque", "", "M10 — bibliothèque éclairée", "M12 — dressing", "M9b — étagère éclairée"}


def wall(room, key):
    E = D.ELEV[room][key]
    H = int(round(D.ROOMS[room]["height"]))
    W = int(round(E["width"]))
    g = np.full((H, W), "", dtype=object)
    unknown_open = []

    def fill(x0, x1, z0, z1, v):
        a, b = int(round(x0)), int(round(x1))
        c, d = int(round(z0)), int(round(min(z1, H)))
        g[c:d, a:b] = v
    for el in E["els"]:
        t = el[0]
        if t == "zone":
            fill(el[1], el[2], el[3], el[4], BASE.get(el[5], el[5]))
        elif t == "rzone":
            fill(el[1], el[2], el[3], el[4], "panneau_chene_arrondi")
    for el in E["els"]:
        t = el[0]
        if t == "open":
            if el[3] is None:
                unknown_open.append((el[6], round(el[2] - el[1], 1)))
                continue
            fill(el[1], el[2], el[3], el[4], "ouverture")
        elif t == "box" and el[4] >= H - 1 and el[3] <= 1 and el[6] in FULL_BOX_REMOVE and el[5] in ("chene",):
            fill(el[1], el[2], el[3], el[4], "mobilier")
    out = {}
    for v in np.unique(g):
        if v and v not in ("ouverture", "mobilier"):
            out[v] = float((g == v).sum()) / 1e4
    return out, unknown_open, E.get("sparse", False), W, H


if __name__ == "__main__":
    for room in D.ELEV:
        for k in D.ELEV[room]:
            s, u, sp, W, H = wall(room, k)
            print(room, k, W, H, {a: round(b, 2) for a, b in s.items()}, u, "sparse" if sp else "")
