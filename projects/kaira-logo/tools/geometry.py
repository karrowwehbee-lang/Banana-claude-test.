"""KAÏRA — custom letterforms (vector), drawn from geometry.

Concept « the shadow gap » : in KAÏRA interiors, a fine recessed joint separates two materials.
In the wordmark, the same joint separates strokes: the arm of the K floats beside its stem,
the bar of the A floats between its legs, the leg of the R floats under its bowl.

All units: cap height = 200. y grows downwards (SVG).
"""
import pathlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

CAP = 200
T = 26          # thick stroke
t = 4           # hairline
GAP = 8         # the shadow gap
SER = 14        # serif overhang


def poly(*pts):
    return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"


def rect(x0, y0, x1, y1):
    return poly((x0, y0), (x1, y0), (x1, y1), (x0, y1))


def serif(xc0, xc1, top=True):
    """Hairline serif from x xc0..xc1 at cap line or baseline."""
    return rect(xc0, 0, xc1, t) if top else rect(xc0, CAP - t, xc1, CAP)


def lerp_x(p, q, y):
    (x0, y0), (x1, y1) = p, q
    return x0 + (x1 - x0) * (y - y0) / (y1 - y0)


def paths_svg(paths):
    return "".join(f'<path d="{d}"{" fill-rule=\"evenodd\"" if d.count("M") > 1 else ""}/>' for d in paths)


# ------------------------------------------------------------------ letters (each returns (paths, advance))
def K(gap=GAP):
    arm_bot, arm_top = (T + gap, 128), (150, 0)
    arm_w = 7
    p = [rect(0, 0, T, CAP),
         poly(arm_bot, (arm_bot[0] + arm_w, arm_bot[1]), (arm_top[0] + arm_w, 0), arm_top)]
    edge = lambda y: lerp_x((arm_bot[0] + arm_w, arm_bot[1]), (arm_top[0] + arm_w, 0), y)
    p.append(poly((edge(112), 112), (edge(72), 72), (178, CAP), (142, CAP)))
    p += [serif(-SER, T + SER), serif(-SER, T + SER, False), serif(136, 172), serif(128, 194, False)]
    return p, 194


def A(gap=GAP, bar_y=140):
    lw, rw = 7, 32
    apex_l, apex_r = 82, 82 + rw
    p = [poly((0, CAP), (lw, CAP), (apex_l + lw, 0), (apex_l, 0)),
         poly((apex_l, 0), (apex_r, 0), (apex_r + 84, CAP), (apex_l + 84, CAP))]
    xl = lerp_x((lw, CAP), (apex_l + lw, 0), bar_y) + gap
    xr = lerp_x((apex_l + 84, CAP), (apex_l, 0), bar_y) - gap
    p.append(rect(xl, bar_y - t / 2, xr, bar_y + t / 2))
    p += [serif(-SER, 26, False), serif(apex_l + 66, apex_r + 84 + SER, False)]
    return p, apex_r + 84 + SER


def I(dots=False):
    p = [rect(0, 0, T, CAP), serif(-SER, T + SER), serif(-SER, T + SER, False)]
    if dots:   # diaeresis: two lozenges, an inlay motif
        for cx in (T / 2 - 24, T / 2 + 24):
            cy, r = -40, 10
            p.append(poly((cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)))
    return p, T + SER


def R(gap=GAP):
    bowl = ("M0,0 H96 C141,0 154,24 154,52 C154,80 141,104 96,104 H0 Z "
            f"M{T},{t} V{104 - t} H92 C118,{104 - t} 126,80 126,52 C126,24 118,{t} 92,{t} Z")
    p = [rect(0, 0, T, CAP), bowl,
         poly((70, 104 + gap), (104, 104 + gap), (176, CAP), (142, CAP))]
    p += [serif(-SER, T), serif(-SER, T + SER, False), serif(128, 192, False)]
    return p, 192


def wordmark(track=74):
    """KAÏRA. Returns (svg path list, width, top, bottom)."""
    out, x = [], 0
    for fn, kw in ((K, {}), (A, {}), (I, {"dots": True}), (R, {}), (A, {})):
        paths, adv = fn(**kw)
        out.append(f'<g transform="translate({x + SER},0)">{paths_svg(paths)}</g>')
        x += SER + adv + track
    return out, x - track, -50, CAP


# ------------------------------------------------------------------ monograms
def mono_ligature(bar_y=124):
    """K and A sharing one diagonal: the arm of the K is the left leg of the A.
    The bar of the A passes behind the leg of the K, separated from it by two shadow gaps."""
    g = GAP
    arm_bot, apex_l = (T + g, 150), 128
    lw, rw = 7, 32
    rleg = ((apex_l, 0), (apex_l + 92, CAP))
    p = [rect(0, 0, T, CAP),
         poly(arm_bot, (arm_bot[0] + lw, arm_bot[1]), (apex_l + lw, 0), (apex_l, 0)),
         poly((apex_l, 0), (apex_l + rw, 0), (apex_l + rw + 92, CAP), (apex_l + 92, CAP))]
    edge = lambda y: lerp_x((arm_bot[0] + lw, arm_bot[1]), (apex_l + lw, 0), y)
    a_, b_ = (edge(124), 124), (edge(88), 88)
    c_, d_ = (156, CAP), (120, CAP)
    p.append(poly(a_, b_, c_, d_))
    legL = lambda y: lerp_x(a_, d_, y)
    legR = lambda y: lerp_x(b_, c_, y)
    y0, y1 = bar_y - t / 2, bar_y + t / 2
    xl = edge(bar_y) + g
    xr = lerp_x((apex_l + 92, CAP), (apex_l, 0), bar_y) - g
    if legL(bar_y) - g > xl:
        p.append(rect(xl, y0, legL(bar_y) - g, y1))
    p.append(rect(legR(bar_y) + g, y0, xr, y1))
    p += [serif(-SER, T + SER), serif(-SER, T + SER, False), serif(106, 170, False),
          serif(apex_l + 74, apex_l + rw + 92 + SER, False)]
    return p, apex_l + rw + 92 + SER + SER


def arch(w, h, stroke=4, gap=GAP):
    """Thin portal: two jambs and a semicircular head, open at the threshold."""
    r = w / 2
    return (f'<path d="M0,{h} V{r} A{r},{r} 0 0 1 {w},{r} V{h}" fill="none" stroke-width="{stroke}"/>')
