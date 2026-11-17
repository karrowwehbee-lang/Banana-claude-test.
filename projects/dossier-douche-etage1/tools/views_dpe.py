"""Douche principale — Étage 1 : dessins (plan, plafond, élévations, coupes, mobilier). Unités papier : mm.

Graphisme identique au dossier de la villa (projects/dossier-technique/tools/draw.py) : cotes vérifiées en noir,
déduites en olive italique (≈), à confirmer en bordeaux tireté (À CONF.).
"""
import importlib.util
import pathlib

import geom as G

_p = pathlib.Path(__file__).resolve().parents[2] / "dossier-technique/tools/draw.py"
_s = importlib.util.spec_from_file_location("villa_draw", _p)
DR = importlib.util.module_from_spec(_s)
_s.loader.exec_module(DR)
SVG, INK, OLIVE, BURG, GREY, LED, POCHE, fmt = DR.SVG, DR.INK, DR.OLIVE, DR.BURG, DR.GREY, DR.LED, DR.POCHE, DR.fmt

PATTERNS = DR.PATTERNS.replace("</defs></svg>", """
<pattern id="d-trav" patternUnits="userSpaceOnUse" width="12" height="3.2"><rect width="12" height="3.2" fill="#F3EEE6"/>
 <path d="M0,1.1 C3,0.8 6,1.4 12,1.0 M0,2.4 C4,2.2 8,2.7 12,2.3" fill="none" stroke="#D9CDBC" stroke-width="0.07"/></pattern>
<pattern id="d-faience" patternUnits="userSpaceOnUse" width="3.85" height="8.85"><rect width="3.85" height="8.85" fill="#6B2430"/>
 <path d="M0,0 H3.85 M0,0 V8.85" stroke="#C9B3A8" stroke-width="0.12"/></pattern>
<pattern id="d-noyer" patternUnits="userSpaceOnUse" width="6" height="1.6"><rect width="6" height="1.6" fill="#5B3F30"/>
 <path d="M0,0.5 C2,0.3 4,0.7 6,0.5 M0,1.2 C2,1.1 4,1.35 6,1.2" fill="none" stroke="#7A5A47" stroke-width="0.08"/></pattern>
<pattern id="d-terrazzo" patternUnits="userSpaceOnUse" width="2.4" height="2.4"><rect width="2.4" height="2.4" fill="#ECE7DE"/>
 <circle cx="0.5" cy="0.6" r="0.16" fill="#B8AE9F"/><circle cx="1.7" cy="1.5" r="0.12" fill="#9C9184"/>
 <circle cx="1.1" cy="2.0" r="0.09" fill="#C9BFB0"/></pattern>
<pattern id="d-galets" patternUnits="userSpaceOnUse" width="6" height="6"><rect width="6" height="6" fill="#FFFFFF"/>
 <path d="M3,0 L3.5,0.5 L3,1 L2.5,0.5 Z M0,3 L0.5,3.5 L0,4 Z M6,3 L5.5,3.5 L6,4 Z M3,5 L3.5,5.5 L3,6 L2.5,5.5 Z" fill="#CFCFCF"/></pattern>
<pattern id="d-hors" patternUnits="userSpaceOnUse" width="2.2" height="2.2" patternTransform="rotate(45)"><rect width="2.2" height="2.2" fill="#FFFFFF"/>
 <path d="M0,1.1 H2.2" stroke="#D6D6D6" stroke-width="0.12"/></pattern>
</defs></svg>""")

FILL = {"trav": "url(#d-trav)", "faience": "url(#d-faience)", "noyer": "url(#d-noyer)", "terrazzo": "url(#d-terrazzo)",
        "verre": "url(#p-verre)", "miroir": "url(#p-miroir)", "blanc": "#FFFFFF", "noir": "#1E1E1E",
        "galets": "url(#d-galets)", "hors": "url(#d-hors)", "ceram": "#FBFBFA"}


def T(v, st):
    if st == "c" or v is None:
        return "À CONF."
    if st == "d":
        return "≈" + str(int(round(v)))
    return fmt(v)


def dh(s, x0, x1, y, v, st, ext_y=None, above=True, txt=None):
    DR.dim_h(s, x0, x1, y, v, st, ext_y=ext_y, txt=txt if txt is not None else T(v, st), above=above)


def dv(s, y0, y1, x, v, st, ext_x=None, left=True, txt=None):
    DR.dim_v(s, y0, y1, x, v, st, ext_x=ext_x, txt=txt if txt is not None else T(v, st), left=left)


def tag(s, x, y, t, size=1.75, col=INK, anchor="middle"):
    s.text(x, y, t, size, col, anchor)


# ================================================================ PLAN (1:20)
def plan(scale=20, mode="cote"):
    """mode: 'cote' (plan coté), 'equip' (repérage + revêtements), 'plafond' (plan de plafond)."""
    k = 10 / scale
    ml, mt = (34, 26) if mode != "key" else (8, 8)
    w = ml + (G.W_TOT + 40) * k + (40 if mode != "key" else 8)
    h = mt + (G.D_TOT + 40) * k + (34 if mode != "key" else 8)
    s = SVG(w, h)
    ox, oy = ml + 20 * k, mt + (G.D_TOT + 20) * k

    def P(X, Y):
        return ox + X * k, oy - Y * k

    # neighbour zone (hors dossier)
    nx0, ny1 = P(G.W_RET + G.WALL_T, G.D_TOT + 20)
    nx1, ny0 = P(G.W_TOT + 20, G.D_LARGE + G.WALL_T)
    s.rect(nx0, ny1, nx1 - nx0, ny0 - ny1, FILL["hors"], None)
    if mode != "key":
        s.wrap((nx0 + nx1) / 2, ny1 + (ny0 - ny1) * 0.62, "Pièce voisine — hors dossier", 50, 1.7, GREY)
    # walls (poché) then interior
    outer = [(-20, -20), (G.W_TOT + 20, -20), (G.W_TOT + 20, G.D_LARGE + 20), (G.W_RET + 20, G.D_LARGE + 20),
             (G.W_RET + 20, G.D_TOT + 20), (-20, G.D_TOT + 20)]
    inner = [(0, 0), (G.W_TOT, 0), (G.W_TOT, G.D_LARGE), (G.W_RET, G.D_LARGE), (G.W_RET, G.D_TOT), (0, G.D_TOT)]
    pth = lambda pts: "M" + " L".join(f"{P(*p)[0]:.2f},{P(*p)[1]:.2f}" for p in pts) + " Z"
    s.path(pth(outer), fill=POCHE, stroke=INK, sw=0.3)
    floor = FILL["galets"] if mode == "equip" else "#FFFFFF"
    s.path(pth(inner), fill=floor, stroke=INK, sw=0.3)
    # openings: windows (south) and door (north of the large part)
    for wdw in (G.W1, G.W2):
        x0, y0 = P(wdw["x0"], 0)
        x1, _ = P(wdw["x1"], -20)
        s.rect(x0, y0, x1 - x0, 20 * k, "#FFFFFF", None)
        for f in (0.0, 0.5, 1.0):
            s.line(x0, y0 + f * 20 * k, x1, y0 + f * 20 * k, 0.16 if f == 0.5 else 0.22)
        s.line(x0, y0, x0, y0 + 20 * k, 0.22)
        s.line(x1, y0, x1, y0 + 20 * k, 0.22)
    dx0, dy = P(G.DOOR_X[0], G.D_LARGE + 20)
    dx1, dy1 = P(G.DOOR_X[1], G.D_LARGE)
    s.rect(dx0, dy, dx1 - dx0, dy1 - dy, "#FFFFFF", None)
    s.line(dx0, dy, dx0, dy1, 0.25)
    s.line(dx1, dy, dx1, dy1, 0.25)
    r = 74 * k
    s.path(f"M{dx0:.2f},{dy1:.2f} L{dx0:.2f},{dy1 + r:.2f} A{r:.2f},{r:.2f} 0 0 0 {dx1:.2f},{dy1:.2f}", stroke=BURG,
           sw=0.15, dash="0.8 0.5")
    if mode == "plafond":
        _plan_ceiling(s, P, k)
    elif mode != "key":
        _plan_fixtures(s, P, k, mode)
    if mode == "cote":
        _plan_dims(s, P, k, ox, oy)
    if mode != "plafond":
        _markers(s, P, k)
    return s.svg(), w, h


def _plan_fixtures(s, P, k, mode):
    lab = mode == "cote"
    # shower: tray area, glass front + return, column, storage
    x0, y1 = P(0, G.D_TOT)
    x1, y0 = P(G.SHOWER["x1"], G.SHOWER["y0"])
    s.rect(x0, y1, x1 - x0, y0 - y1, "#F7F2EC" if mode != "equip" else "none", None)
    s.line(x0, y0, x1, y0, 0.5)
    s.line(x1, y0, x1, y1, 0.5)
    gx, _ = P(G.SHOWER["mullion"], 0)
    s.line(gx, y0 - 0.9, gx, y0 + 0.9, 0.3)
    cx, cy = P(0, G.SHOWER_COL["y"])
    s.circle(cx + 1.6, cy, 1.1, "#FFFFFF", INK, 0.2)
    s.line(cx, cy, cx + 1.6, cy, 0.3)
    nx0, ny = P(G.SHOWER_NICHE["x0"], G.D_TOT)
    nx1, _ = P(G.SHOWER_NICHE["x1"], 0)
    s.rect(nx0, ny, nx1 - nx0, 4 * k, "none", BURG, 0.15, "0.8 0.5")
    if lab:
        tag(s, (x0 + x1) / 2, (y0 + y1) / 2 - 1, "CABINE DE DOUCHE", 1.9)
        tag(s, (x0 + x1) / 2, (y0 + y1) / 2 + 1.6, "paroi verrière, profilés noirs", 1.45, GREY)
    # WC boxing + WC
    bx0, by1 = P(0, G.BOXING["y1"])
    bx1, by0 = P(G.BOXING["x1"], 0)
    s.rect(bx0, by1, bx1 - bx0, by0 - by1, FILL["faience"] if mode == "equip" else "#EFE3E3", INK, 0.25)
    wx0, wy1 = P(G.WC["ax"] - G.WC["w"] / 2, G.WC["y1"])
    wx1, wy0 = P(G.WC["ax"] + G.WC["w"] / 2, G.BOXING["y1"])
    s.rect(wx0, wy1, wx1 - wx0, wy0 - wy1, "#FFFFFF", INK, 0.22, rx=1.6)
    if lab:
        tag(s, (bx0 + bx1) / 2, (by0 + by1) / 2 + 0.6, "coffrage WC", 1.5)
        tag(s, (wx0 + wx1) / 2, (wy0 + wy1) / 2 + 0.6, "WC", 1.6)
    # commode, glass shelves (above, dashed), walnut shelves (above)
    cx0, cy1 = P(G.COMMODE["x0"], G.COMMODE["y1"])
    cx1, cy0 = P(G.COMMODE["x1"], 0)
    s.rect(cx0, cy1, cx1 - cx0, cy0 - cy1, FILL["noyer"] if mode == "equip" else "#FFFFFF", INK, 0.25)
    gx0, gy1 = P(G.GLASS_SHELVES["x0"], G.GLASS_SHELVES["depth"])
    gx1, _ = P(G.GLASS_SHELVES["x1"], 0)
    s.rect(gx0, gy1, gx1 - gx0, G.GLASS_SHELVES["depth"] * k, "none", GREY, 0.14, "0.6 0.4")
    if lab:
        tag(s, (cx0 + cx1) / 2, (cy0 + cy1) / 2 + 0.6, "commode", 1.5)
    # towel ladder (west wall)
    lx0, ly1 = P(0, G.LADDER["y1"])
    lx1, ly0 = P(G.LADDER["depth"], G.LADDER["y0"])
    s.rect(lx0, ly1, lx1 - lx0, ly0 - ly1, "none", INK, 0.18, "0.8 0.5")
    if lab:
        s.wrap((lx0 + lx1) / 2 + 1.5, (ly0 + ly1) / 2, "échelle porte-serviettes", 12, 1.4, GREY)
    # vanity (east wall), basin, towel bar, mirror line, pendants
    vx0, vy1 = P(G.W_TOT - G.VANITY["depth"], G.VANITY["y1"])
    vx1, vy0 = P(G.W_TOT, G.VANITY["y0"])
    s.rect(vx0, vy1, vx1 - vx0, vy0 - vy1, FILL["terrazzo"] if mode == "equip" else "#FFFFFF", INK, 0.3)
    bcx, bcy = P(G.W_TOT - G.VANITY["depth"] / 2 - 2, G.BASIN["ay"])
    s.rect(bcx - G.BASIN["d"] / 2 * k, bcy - G.BASIN["w"] / 2 * k, G.BASIN["d"] * k, G.BASIN["w"] * k, "#FFFFFF", INK,
           0.22, rx=1.0)
    tx0, ty1 = P(G.W_TOT - G.TOWEL_BAR["depth"], G.TOWEL_BAR["y1"])
    tx1, ty0 = P(G.W_TOT, G.TOWEL_BAR["y0"])
    s.rect(tx0, ty1, tx1 - tx0, ty0 - ty1, "none", INK, 0.2)
    mx, my1 = P(G.W_TOT - 1.5, G.MIRROR["y1"])
    _, my0 = P(0, G.MIRROR["y0"])
    s.line(mx, my1, mx, my0, 0.35, "#9FB0B5")
    for pnd in G.PENDANTS[::2]:
        px, py = P(G.PEND_X, pnd["y"])
        s.circle(px, py, 1.0, "none", INK, 0.16, "0.5 0.3")
    if lab:
        s.text(vx0 + 1.2, (vy0 + vy1) / 2, "meuble vasque suspendu", 1.5, INK, "middle", rot=-90)
    # hooks (arm east wall)
    for hk in G.HOOKS:
        hx, hy = P(G.W_RET, hk["y"])
        s.line(hx, hy, hx - 1.4, hy, 0.4)


def _plan_ceiling(s, P, k):
    """Ceiling: perimeter LED line (offset to confirm), pendants, mirror backlight, ceiling height."""
    off = 20
    pts = [(off, off), (G.W_TOT - off, off), (G.W_TOT - off, G.D_LARGE - off), (G.W_RET - off, G.D_LARGE - off),
           (G.W_RET - off, G.D_TOT - off), (off, G.D_TOT - off)]
    d = "M" + " L".join(f"{P(*p)[0]:.2f},{P(*p)[1]:.2f}" for p in pts) + " Z"
    s.path(d, stroke=LED, sw=0.5, dash="1.2 0.6")
    cx, cy = P(G.W_TOT * 0.45, G.D_LARGE * 0.5)
    s.text(cx, cy - 2, "FAUX PLAFOND", 2.0, INK, weight=500, ls=0.3)
    s.text(cx, cy + 1.2, "peint blanc · H ≈ 289 sous plafond", 1.6, OLIVE, italic=True)
    s.text(cx, cy + 4.0, "gorge LED en périphérie — retrait : À CONF.", 1.6, BURG)
    for pnd in G.PENDANTS[::2]:
        px, py = P(G.PEND_X, pnd["y"])
        s.circle(px, py, 1.3, "#FFFFFF", INK, 0.2)
        s.line(px - 0.9, py, px + 0.9, py, 0.15)
        s.line(px, py - 0.9, px, py + 0.9, 0.15)
    mx, my1 = P(G.W_TOT - 1.5, G.MIRROR["y1"])
    _, my0 = P(0, G.MIRROR["y0"])
    s.line(mx, my1, mx, my0, 0.6, LED)
    # shower: no light visible in the renders
    sx, sy = P(G.SHOWER["x1"] / 2, (G.SHOWER["y0"] + G.D_TOT) / 2)
    s.wrap(sx, sy, "Douche : aucun luminaire visible sur les rendus — éclairage À CONF.", 40, 1.45, BURG)
    vx0, vy1 = P(G.W_TOT - G.VANITY["depth"], G.VANITY["y1"])
    vx1, vy0 = P(G.W_TOT, G.VANITY["y0"])
    s.rect(vx0, vy1, vx1 - vx0, vy0 - vy1, "none", GREY, 0.14, "0.6 0.4")
    x0, y1 = P(0, G.D_TOT)
    x1, y0 = P(G.SHOWER["x1"], G.SHOWER["y0"])
    s.rect(x0, y1, x1 - x0, y0 - y1, "none", GREY, 0.14, "0.6 0.4")


def _plan_dims(s, P, k, ox, oy):
    # south: window chain (d) and overall (v)
    yb = oy + 20 * k + 7
    chain = [0, G.W1["x0"], G.W1["x1"], G.W2["x0"], G.W2["x1"], G.W_TOT]
    for a, b in zip(chain, chain[1:]):
        dh(s, P(a, 0)[0], P(b, 0)[0], yb, b - a, "d", ext_y=oy + 20 * k, above=False)
    dh(s, P(0, 0)[0], P(G.W_TOT, 0)[0], yb + 7, G.W_TOT, "v", ext_y=oy + 20 * k, above=False)
    # north: arm (v) and the 66 / 74 / 70 chain (v)
    yt = P(0, G.D_TOT)[1] - 20 * k - 6
    dh(s, P(0, 0)[0], P(G.W_RET, 0)[0], yt, G.W_RET, "v", ext_y=P(0, G.D_TOT)[1] - 20 * k)
    yn = P(0, G.D_LARGE + 20)[1] - 5
    xs = [G.W_RET, G.DOOR_X[0], G.DOOR_X[1], G.W_TOT]
    for a, b, v in zip(xs, xs[1:], G.NORD):
        dh(s, P(a, 0)[0], P(b, 0)[0], yn, v, "v", ext_y=P(0, G.D_LARGE + 20)[1])
    # west: 234,1 + 137 (v) and total
    xl = P(0, 0)[0] - 20 * k - 7
    dv(s, P(0, 0)[1], P(0, G.D_LARGE)[1], xl, G.D_LARGE, "v", ext_x=P(0, 0)[0] - 20 * k)
    dv(s, P(0, G.D_LARGE)[1], P(0, G.D_TOT)[1], xl, G.D_RET, "v", ext_x=P(0, 0)[0] - 20 * k)
    dv(s, P(0, 0)[1], P(0, G.D_TOT)[1], xl - 7, G.D_TOT, "v", ext_x=P(0, 0)[0] - 20 * k)
    # east: wall 234,1 (v) + vanity chain (d)
    xr = P(G.W_TOT, 0)[0] + 20 * k + 7
    dv(s, P(0, 0)[1], P(0, G.D_LARGE)[1], xr + 7, G.D_LARGE, "v", ext_x=P(G.W_TOT, 0)[0] + 20 * k, left=False)
    ys = [0, G.VANITY["y0"], G.VANITY["y1"], G.D_LARGE]
    for a, b in zip(ys, ys[1:]):
        dv(s, P(0, a)[1], P(0, b)[1], xr, b - a, "d", ext_x=P(G.W_TOT, 0)[0] + 20 * k, left=False)
    # interior: boxing (v), WC axis, commode, shower, vanity depth
    dh(s, P(0, 0)[0], P(G.BOXING["x1"], 0)[0], P(0, G.BOXING["y1"])[1] - 2.2, G.BOXING["x1"], "v")
    dv(s, P(0, 0)[1], P(0, G.BOXING["y1"])[1], P(G.BOXING["x1"], 0)[0] + 2.4, G.BOXING["y1"], "v", left=False)
    dh(s, P(0, 0)[0], P(G.WC["ax"], 0)[0], P(0, G.WC["y1"])[1] - 2.0, G.WC["ax"], "d", txt="axe ≈78")
    dv(s, P(0, G.BOXING["y1"])[1], P(0, G.WC["y1"])[1], P(G.WC["ax"] + G.WC["w"] / 2, 0)[0] + 2.4, 57, "d", left=False)
    dh(s, P(G.COMMODE["x0"], 0)[0], P(G.COMMODE["x1"], 0)[0], P(0, G.COMMODE["y1"])[1] - 2.0,
       G.COMMODE["x1"] - G.COMMODE["x0"], "d")
    dv(s, P(0, 0)[1], P(0, G.COMMODE["y1"])[1], P(G.COMMODE["x1"], 0)[0] + 2.4, G.COMMODE["y1"], "d", left=False)
    dh(s, P(0, 0)[0], P(G.SHOWER["x1"], 0)[0], P(0, G.SHOWER["y0"])[1] + 3.2, G.SHOWER["x1"], "d", above=False)
    dv(s, P(0, G.SHOWER["y0"])[1], P(0, G.D_TOT)[1], P(G.SHOWER["x1"], 0)[0] + 2.4, G.D_TOT - G.SHOWER["y0"], "d",
       left=False)
    dh(s, P(G.W_TOT - G.VANITY["depth"], 0)[0], P(G.W_TOT, 0)[0], P(0, G.VANITY["y1"])[1] - 2.2, G.VANITY["depth"], "d")
    # notes on openings
    for wdw, nm in ((G.W1, "F1"), (G.W2, "F2")):
        x = P((wdw["x0"] + wdw["x1"]) / 2, 0)[0]
        s.text(x, P(0, 0)[1] + 20 * k + 2.4, f'{nm} · allège ≈{wdw["z0"]} · haut ≈{wdw["z1"]}', 1.45, OLIVE, italic=True)
    x = P(sum(G.DOOR_X) / 2, 0)[0]
    s.text(x, P(0, G.D_LARGE)[1] + 3.0, "P1 · H ≈202 · sens d'ouverture À CONF.", 1.45, BURG)


def _markers(s, P, k):
    """Elevation markers A–F (wall seen) and section lines AA, BB."""
    def mark(X, Y, ang, letter):
        x, y = P(X, Y)
        DR.bubble(s, x, y, letter, r=2.2)
        dx, dy = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}[ang]
        s.path(f"M{x + dx * 2.2 + dy * 1.2:.2f},{y + dy * 2.2 - dx * 1.2:.2f} L{x + dx * 4.2:.2f},{y + dy * 4.2:.2f} "
               f"L{x + dx * 2.2 - dy * 1.2:.2f},{y + dy * 2.2 + dx * 1.2:.2f} Z", fill=INK, stroke=None)
    mark(200, 95, "S", "A")
    mark(275, 120, "E", "B")
    mark(268, 190, "N", "C")
    mark(70, 160, "W", "D")
    mark(60, 250, "N", "E")
    mark(145, 300, "E", "F")
    # sections
    for (X0, Y0, X1, Y1, nm, ang) in ((92, -34, 92, G.D_TOT + 34, "AA", "E"), (-34, 125, G.W_TOT + 34, 125, "BB", "N")):
        a, b = P(X0, Y0), P(X1, Y1)
        s.line(a[0], a[1], b[0], b[1], 0.18, INK, "3 0.8 0.6 0.8")
        for (x, y) in (a, b):
            s.text(x + (2.6 if ang == "E" else 0), y + (0.6 if ang == "E" else -1.6), nm[0], 2.2, INK, weight=500)


# ================================================================ ELEVATIONS (1:20)
class Elev:
    """Elevation of a wall seen from inside. u: from the left end (cm); z: from the finished floor (cm)."""

    def __init__(self, width, scale=20, height=G.H_PLAF, left_note="", right_note=""):
        self.k = k = 10 / scale
        self.W, self.H = width, height
        self.ml, self.mb, self.mt = 26, 22, 12
        self.w = self.ml + (width + 40) * k + 30
        self.h = self.mt + (height + 25) * k + self.mb
        self.s = SVG(self.w, self.h)
        self.ox, self.oy = self.ml + 20 * k, self.mt + (height + 20) * k
        s = self.s
        # cut side walls, slab and floor
        s.rect(self.ox - 20 * k, self.oy - (height + 20) * k, 20 * k, (height + 25) * k, POCHE, None)
        s.rect(self.ox + width * k, self.oy - (height + 20) * k, 20 * k, (height + 25) * k, POCHE, None)
        s.rect(self.ox - 20 * k, self.oy - (height + 20) * k, (width + 40) * k, 20 * k, "#FFFFFF", INK, 0.2)
        s.rect(self.ox - 20 * k, self.oy - (height + 20) * k, (width + 40) * k, 20 * k, FILL["hors"], None)
        s.line(self.ox - 20 * k, self.oy, self.ox + (width + 20) * k, self.oy, 0.5)
        if left_note:
            s.text(self.ox - 10 * k, self.oy + 4.2, left_note, 1.5, GREY)
        if right_note:
            s.text(self.ox + (width + 10) * k, self.oy + 4.2, right_note, 1.5, GREY)

    def X(self, u):
        return self.ox + u * self.k

    def Z(self, z):
        return self.oy - z * self.k

    def box(self, u0, u1, z0, z1, fill="none", stroke=INK, sw=0.22, dash=None, rx=0):
        self.s.rect(self.X(u0), self.Z(z1), (u1 - u0) * self.k, (z1 - z0) * self.k, fill, stroke, sw, dash, rx)

    def finish(self, u0, u1, z0, z1, mat):
        self.s.rect(self.X(u0), self.Z(z1), (u1 - u0) * self.k, (z1 - z0) * self.k, FILL[mat], None)

    def note(self, u, z, t, col=INK, size=1.5, anchor="middle"):
        self.s.text(self.X(u), self.Z(z), t, size, col, anchor)

    def wrap(self, u, z, t, width_mm, col=INK, size=1.45):
        self.s.wrap(self.X(u), self.Z(z), t, width_mm, size, col)

    def led(self, u0, u1, z):
        self.s.line(self.X(u0), self.Z(z), self.X(u1), self.Z(z), 0.45, LED, "1.2 0.6")

    def window(self, u0, u1, z0, z1):
        self.box(u0, u1, z0, z1, "#FFFFFF", INK, 0.3)
        self.box(u0 + 4, u1 - 4, z0 + 4, z1 - 4, "#EEF2F3", INK, 0.15)

    def chain_h(self, pts, sts, z=None, below=True, gap=6):
        y = self.oy + gap if below else self.Z(self.H) - gap
        for (a, b), st in zip(zip(pts, pts[1:]), sts):
            dh(self.s, self.X(a), self.X(b), y, b - a, st, ext_y=self.oy if below else self.Z(self.H), above=not below)

    def chain_v(self, pts, sts, right=True, gap=8, u=None):
        x = (self.X(self.W) + 20 * self.k + gap) if right else (self.X(0) - 20 * self.k - gap)
        if u is not None:
            x = self.X(u)
        for (a, b), st in zip(zip(pts, pts[1:]), sts):
            dv(self.s, self.Z(a), self.Z(b), x, b - a, st, ext_x=None, left=not right)

    def level(self, z, label, st="d", right=True):
        x = self.X(self.W) + 20 * self.k + 3 if right else self.X(0) - 20 * self.k - 3
        DR.level_mark(self.s, x, self.Z(z), label, st, right)

    def svg(self):
        return self.s.svg(), self.s.w, self.s.h


def elev_A():
    """Mur sud (fenêtres). Vu de l'intérieur vers le sud : gauche = est, droite = ouest. u = 374,8 − X."""
    e = Elev(G.W_TOT, left_note="mur est", right_note="mur ouest")
    U = lambda X: G.W_TOT - X
    e.finish(0, G.W_TOT, 0, G.H_PLAF, "trav")
    e.finish(U(G.BOXING["x1"]), U(0), 0, G.BOXING["h"], "faience")
    e.box(U(G.BOXING["x1"]), U(0), 0, G.BOXING["h"], "none", INK, 0.25)
    for wdw in (G.W1, G.W2):
        e.window(U(wdw["x1"]), U(wdw["x0"]), wdw["z0"], wdw["z1"])
    # WC (front), flush plate
    e.box(U(G.WC["ax"] + 19), U(G.WC["ax"] - 19), 16, 40, FILL["ceram"], INK, 0.22, rx=1.5)
    e.box(U(G.FLUSH["ax"] + 9.5), U(G.FLUSH["ax"] - 9.5), G.FLUSH["z0"], G.FLUSH["z1"], FILL["noir"], None)
    # commode
    e.box(U(G.COMMODE["x1"]), U(G.COMMODE["x0"]), G.COMMODE["z0"], G.COMMODE["z1"], FILL["noyer"], INK, 0.25)
    zm = (G.COMMODE["z0"] + G.COMMODE["z1"]) / 2
    e.s.line(e.X(U(G.COMMODE["x1"])), e.Z(zm), e.X(U(G.COMMODE["x0"])), e.Z(zm), 0.15, "#D6C7B8")
    for zz in (zm + 25, zm - 14):
        e.box(U((G.COMMODE["x0"] + G.COMMODE["x1"]) / 2 + 8), U((G.COMMODE["x0"] + G.COMMODE["x1"]) / 2 - 8), zz, zz + 2.2,
              FILL["noir"], None)
    # glass and walnut shelves
    for z in G.GLASS_SHELVES["levels"]:
        e.box(U(G.GLASS_SHELVES["x1"]), U(G.GLASS_SHELVES["x0"]), z - 1, z, "#9AA3A5", INK, 0.15)
    for z in G.WALNUT_SHELVES["levels"]:
        e.box(U(G.WALNUT_SHELVES["x1"]), U(G.WALNUT_SHELVES["x0"]), z - 3, z, FILL["noyer"], INK, 0.15)
    e.led(4, G.W_TOT - 4, G.H_PLAF - 1)
    # labels
    e.wrap(U(58), 120, "coffrage faïence bordeaux", 22, "#FFFFFF")
    e.note(U(78), 20, "WC suspendu", INK, 1.35)
    e.note(U(182), 48, "commode noyer", "#FFFFFF", 1.4)
    e.wrap(U(190), 196, "étagères en verre fumé", 26, INK, 1.4)
    e.wrap(U(25), 232, "étagères noyer", 12, INK, 1.3)
    e.note(U(83.4), 236, "F1", INK, 1.6)
    e.note(U(283.8), 236, "F2", INK, 1.6)
    # dims: horizontal (X order reversed on paper)
    pts = sorted({U(x) for x in (0, G.W1["x0"], G.W1["x1"], G.W2["x0"], G.W2["x1"], G.W_TOT)})
    e.chain_h(pts, ["d"] * (len(pts) - 1), gap=6)
    e.chain_h([0, G.W_TOT], ["v"], gap=12)
    pts2 = sorted({U(x) for x in (G.BOXING["x1"], 0)})
    dh(e.s, e.X(pts2[0]), e.X(pts2[1]), e.Z(G.BOXING["h"]) - 2.0, G.BOXING["x1"], "v")
    dh(e.s, e.X(U(G.COMMODE["x1"])), e.X(U(G.COMMODE["x0"])), e.Z(G.COMMODE["z1"]) - 2.0,
       G.COMMODE["x1"] - G.COMMODE["x0"], "d")
    # heights (right): F1 sill/head, boxing, ceiling
    e.chain_v([0, G.BOXING["h"], G.W1["z0"], G.W1["z1"], G.H_PLAF], ["d"] * 4, right=True)
    e.chain_v([0, G.W2["z0"], G.W2["z1"], G.H_PLAF], ["d"] * 3, right=False)
    e.chain_v([0, G.COMMODE["z0"], G.COMMODE["z1"]], ["d", "d"], u=U(G.COMMODE["x0"]) + 4)
    e.chain_v([G.COMMODE["z1"], *G.GLASS_SHELVES["levels"]], ["d"] * 3, u=U(G.GLASS_SHELVES["x0"]) + 4)
    return e.svg()


def elev_B():
    """Mur est (meuble vasque). Vu vers l'est : gauche = nord (Y 234,1), droite = sud (Y 0). u = 234,1 − Y."""
    e = Elev(G.D_LARGE, left_note="mur nord", right_note="mur sud")
    U = lambda Y: G.D_LARGE - Y
    v = G.VANITY
    e.finish(0, G.D_LARGE, 0, G.H_PLAF, "trav")
    e.finish(U(G.SPLASH["y1"]), U(G.SPLASH["y0"]), v["z1"], G.SPLASH["z1"], "terrazzo")
    e.box(U(G.MIRROR["y1"]), U(G.MIRROR["y0"]), G.MIRROR["z0"], G.MIRROR["z1"], FILL["miroir"], INK, 0.25)
    e.s.rect(e.X(U(G.MIRROR["y1"])) - 0.5, e.Z(G.MIRROR["z1"]) - 0.5, (G.MIRROR["y1"] - G.MIRROR["y0"]) * e.k + 1,
             (G.MIRROR["z1"] - G.MIRROR["z0"]) * e.k + 1, "none", LED, 0.35, "1.2 0.6")
    # vanity: top (terrazzo 3 cm), drawers, niches
    e.box(U(v["y1"]), U(v["y0"]), v["z1"] - 3, v["z1"], FILL["terrazzo"], INK, 0.25)
    e.box(U(v["y1"]), U(v["split"]), v["z0"], v["z1"] - 3, FILL["noyer"], INK, 0.25)
    zm = (v["z0"] + v["z1"] - 3) / 2
    e.s.line(e.X(U(v["y1"])), e.Z(zm), e.X(U(v["split"])), e.Z(zm), 0.18, "#D6C7B8")
    e.box(U(v["split"]), U(v["y0"]), v["z0"], v["z1"] - 3, FILL["noyer"], INK, 0.25)
    e.box(U(v["split"]) + 2.5, U(v["y0"]) - 2.5, v["z0"] + 2.5, zm - 1, "#2E211A", None)
    e.box(U(v["split"]) + 2.5, U(v["y0"]) - 2.5, zm + 1, v["z1"] - 5.5, "#2E211A", None)
    # basin and taps
    b = G.BASIN
    e.box(U(b["ay"] + b["w"] / 2), U(b["ay"] - b["w"] / 2), v["z1"], b["z1"], FILL["ceram"], INK, 0.22, rx=1.2)
    for dy in (-11, 0, 11):
        zt = b["z1"] + (16 if dy == 0 else 9)
        e.box(U(b["ay"] + dy) - 0.8, U(b["ay"] + dy) + 0.8, G.SPLASH["z1"] - 2, zt, FILL["noir"], None)
    # towel bar, pendants
    t = G.TOWEL_BAR
    e.box(U(t["y1"]), U(t["y0"]), t["z"] - 1.5, t["z"], FILL["noir"], None)
    e.box(U(t["y1"]) + 3, U(t["y0"]) - 3, t["z"] - 45, t["z"] - 1.5, "#F4F2EE", GREY, 0.12)
    for p in G.PENDANTS:
        x = e.X(U(p["y"]))
        e.s.line(x, e.Z(G.H_PLAF), x, e.Z(p["z"] + 3), 0.1, INK)
        e.s.circle(x, e.Z(p["z"]), 3 * e.k, "#FFF7E6", INK, 0.15)
    e.led(4, G.D_LARGE - 4, G.H_PLAF - 1)
    # labels
    e.note(U((v["y1"] + v["split"]) / 2), zm + 3, "2 tiroirs noyer", "#FFFFFF", 1.4)
    e.note(U((v["split"] + v["y0"]) / 2), v["z0"] - 4, "niches ouvertes", INK, 1.35)
    e.note(U(95), (G.MIRROR["z0"] + G.MIRROR["z1"]) / 2, "miroir rétroéclairé", INK, 1.5)
    e.note(U(95), v["z1"] + 6.5, "crédence terrazzo", INK, 1.3)
    e.wrap(U(205), t["z"] + 8, "porte-serviettes", 12, INK, 1.3)
    e.wrap(U(36), 110, "suspensions", 10, INK, 1.3)
    # dims
    pts = sorted({U(y) for y in (G.D_LARGE, t["y1"], t["y0"], v["y1"], v["y0"], 0)})
    e.chain_h(pts, ["d"] * (len(pts) - 1), gap=6)
    e.chain_h([0, G.D_LARGE], ["v"], gap=12)
    dh(e.s, e.X(U(v["y1"])), e.X(U(v["split"])), e.Z(v["z0"]) + 3.2, v["y1"] - v["split"], "d", above=False)
    dh(e.s, e.X(U(v["split"])), e.X(U(v["y0"])), e.Z(v["z0"]) + 3.2, v["split"] - v["y0"], "d", above=False)
    dh(e.s, e.X(U(G.MIRROR["y1"])), e.X(U(G.MIRROR["y0"])), e.Z(G.MIRROR["z1"]) - 2.2,
       G.MIRROR["y1"] - G.MIRROR["y0"], "d")
    e.chain_v([0, v["z0"], v["z1"], G.SPLASH["z1"], G.MIRROR["z1"], G.H_PLAF], ["d"] * 5, right=True)
    e.chain_v([0, t["z"]], ["d"], right=False)
    e.chain_v([0, 123, 144], ["d", "d"], u=U(36) - 1)
    return e.svg()


def elev_C():
    """Mur nord de la partie large (porte). Vu vers le nord : gauche = ouest (X 164,8), droite = est (X 374,8)."""
    wd = G.W_TOT - G.W_RET
    e = Elev(wd, left_note="angle du retour", right_note="mur est")
    e.finish(0, wd, 0, G.H_PLAF, "trav")
    d0, d1 = G.DOOR_X[0] - G.W_RET, G.DOOR_X[1] - G.W_RET
    e.box(d0, d1, 0, G.H_DOOR, "#3A332E", INK, 0.3)
    e.box(d0 - 4, d1 + 4, 0, G.H_DOOR + 4, "none", INK, 0.18)
    for z in (40, 80, 120, 160):
        e.s.line(e.X(d0 + 4), e.Z(z), e.X(d1 - 4), e.Z(z), 0.25, "#A7A39F")
    e.box(d0 + 4, d0 + 12, 103, 105, "#A7A39F", None)
    e.led(4, wd - 4, G.H_PLAF - 1)
    e.wrap((d0 + d1) / 2, 220, "P1 — porte sombre à inserts métalliques · sens d'ouverture À CONF.", 40, INK, 1.4)
    e.chain_h([0, d0, d1, wd], ["v", "v", "v"], gap=6)
    e.chain_h([0, wd], ["v"], gap=12)
    e.chain_v([0, G.H_DOOR, G.H_PLAF], ["d", "d"], right=True)
    return e.svg()


def elev_D():
    """Mur ouest. Vu vers l'ouest : gauche = sud (Y 0), droite = nord (Y 371,1). u = Y."""
    e = Elev(G.D_TOT, left_note="mur sud", right_note="mur nord")
    e.finish(0, G.D_TOT, 0, G.H_PLAF, "trav")
    # boxing seen from its side (40 deep)
    e.box(0, G.BOXING["y1"], 0, G.BOXING["h"], FILL["faience"], INK, 0.25)
    # ladder (dims to confirm)
    l = G.LADDER
    e.box(l["y0"], l["y0"] + 3, 0, 185, FILL["noir"], None)
    e.box(l["y1"] - 3, l["y1"], 0, 185, FILL["noir"], None)
    for z in (95, 140, 175):
        e.box(l["y0"], l["y1"], z, z + 1.5, FILL["noir"], None)
    e.box(l["y0"] + 4, l["y1"] - 4, 70, 85, "#2B2B2B", None)
    # shower zone: travertine inside, glass return seen edge-on → shown by its frame line, column + mixer
    s0 = G.SHOWER["y0"]
    e.box(s0, s0 + 1.2, G.SHOWER["curb"], G.SHOWER["glass_top"], FILL["noir"], None)
    e.box(s0, G.D_TOT, 0, G.SHOWER["curb"], "#EDEDED", INK, 0.15)
    c = G.SHOWER_COL
    x = c["y"]
    e.box(x - 1, x + 1, 95, c["head_z"], FILL["noir"], None)
    e.box(x - 14, x + 1, c["head_z"] - 1, c["head_z"] + 1, FILL["noir"], None)
    e.s.circle(e.X(x - 14), e.Z(c["head_z"] - 4), 9 * e.k, FILL["noir"], None)
    e.s.circle(e.X(x), e.Z(c["mixer_z"]), 3 * e.k, "#FFFFFF", INK, 0.25)
    e.s.circle(e.X(x + 10), e.Z(c["mixer2_z"]), 2.5 * e.k, "#FFFFFF", INK, 0.25)
    e.wrap(20, 165, "coffrage WC (côté)", 14, INK, 1.3)
    e.wrap((l["y0"] + l["y1"]) / 2, 200, "échelle porte-serviettes", 16, INK, 1.3)
    e.wrap((s0 + G.D_TOT) / 2, 250, "douche : colonne et mitigeur", 22, INK, 1.3)
    e.chain_h([0, G.BOXING["y1"], l["y0"], l["y1"], s0, G.D_TOT], ["v", "d", "d", "d", "d"], gap=6)
    e.chain_h([0, G.D_LARGE, G.D_TOT], ["v", "v"], gap=12)
    e.chain_v([0, G.BOXING["h"], G.H_PLAF], ["d", "d"], right=False)
    e.chain_v([0, G.SHOWER["curb"], c["mixer_z"], c["head_z"], G.H_PLAF], ["d"] * 4, right=True)
    e.note((l["y0"] + l["y1"]) / 2, 20, "hauteur et largeur : À CONF.", BURG, 1.3)
    return e.svg()


def elev_E():
    """Fond de douche : mur nord du retour, vu vers le nord. Gauche = ouest (X 0), droite = X 164,8."""
    e = Elev(G.W_RET, left_note="mur ouest", right_note="retour")
    e.finish(0, G.W_RET, 0, G.H_PLAF, "faience")
    n = G.SHOWER_NICHE
    e.box(n["x0"], n["x1"], n["z0"], n["z1"], "none", BURG, 0.25, "0.8 0.5")
    sh = G.SHOWER
    e.box(0, sh["x1"], 0, sh["curb"], "#EDEDED", INK, 0.15)
    e.box(0, sh["x1"], sh["curb"], sh["glass_top"], "url(#p-verre)", None)
    e.s.rect(e.X(0), e.Z(sh["glass_top"]), sh["x1"] * e.k, (sh["glass_top"] - sh["curb"]) * e.k, "none", INK, 0.45)
    for z in sh["rows"][1:-1]:
        e.s.line(e.X(0), e.Z(z), e.X(sh["x1"]), e.Z(z), 0.35)
    e.s.line(e.X(sh["mullion"]), e.Z(sh["curb"]), e.X(sh["mullion"]), e.Z(sh["glass_top"]), 0.45)
    e.box(sh["mullion"] - 2.5, sh["mullion"] - 1.5, 95, 125, FILL["noir"], None)
    e.wrap(n["x0"] + 13, n["z1"] + 8, "rangement : niche ou étagère À CONF.", 14, BURG, 1.25)
    e.wrap(40, 240, "faïence bordeaux brillante, pose verticale, toute hauteur", 40, "#FFFFFF", 1.35)
    e.chain_h([0, sh["mullion"], sh["x1"], G.W_RET], ["d", "d", "d"], gap=6)
    e.chain_h([0, G.W_RET], ["v"], gap=12)
    e.chain_v(list(sh["rows"]) + [G.H_PLAF], ["d"] * 6, right=False)
    e.chain_v([0, n["z0"], n["z1"], G.H_PLAF], ["d"] * 3, right=True)
    return e.svg()


def elev_F():
    """Retour de la douche (mur X = 164,8), vu vers l'est. Gauche = nord (Y 371,1), droite = sud (Y 234,1)."""
    e = Elev(G.D_RET, left_note="fond de douche", right_note="partie large")
    U = lambda Y: G.D_TOT - Y
    e.finish(0, G.D_RET, 0, G.H_PLAF, "trav")
    e.finish(0, 1.5, 0, G.H_PLAF, "faience")
    gy = G.D_TOT - G.SHOWER["y0"]
    e.box(gy - 0.6, gy + 0.6, G.SHOWER["curb"], G.SHOWER["glass_top"], FILL["noir"], None)
    for hk in G.HOOKS:
        x = U(hk["y"])
        e.box(x - 1, x + 1, hk["z"] - 6, hk["z"], FILL["noir"], None)
        e.box(x - 9, x + 9, hk["z"] - 95, hk["z"] - 6, "#F4F2EE", GREY, 0.12, rx=2)
    e.wrap(U(264), 80, "patères noires et peignoirs", 14, INK, 1.3)
    e.chain_h([0, gy, U(G.HOOKS[0]["y"]), U(G.HOOKS[1]["y"]), G.D_RET], ["d", "d", "c", "d"], gap=6)
    e.chain_h([0, G.D_RET], ["v"], gap=12)
    e.chain_v([0, G.HOOKS[1]["z"], G.HOOKS[0]["z"], G.H_PLAF], ["c", "d", "d"], right=True)
    return e.svg()


# ================================================================ SECTIONS (1:20)
def section_AA():
    """Coupe AA (X ≈ 92), vue vers l'est : gauche = sud (Y 0), droite = nord (Y 371,1)."""
    e = Elev(G.D_TOT + 0, left_note="mur sud (coupé)", right_note="mur nord (coupé)")
    # seen beyond the cut (looking east): east wall with the vanity and mirror (Y < 234,1), commode in front,
    # the corner of the return at Y = 234,1, then the return wall (X = 164,8) with the hooks
    e.finish(0, G.D_TOT, 0, G.H_PLAF, "trav")
    v = G.VANITY
    e.box(G.MIRROR["y0"], G.MIRROR["y1"], G.MIRROR["z0"], G.MIRROR["z1"], FILL["miroir"], GREY, 0.15)
    e.box(v["y0"], v["y1"], v["z0"], v["z1"], FILL["noyer"], GREY, 0.15)
    e.box(G.COMMODE["y0"], G.COMMODE["y1"], G.COMMODE["z0"], G.COMMODE["z1"], FILL["noyer"], INK, 0.22)
    e.s.line(e.X(G.D_LARGE), e.Z(0), e.X(G.D_LARGE), e.Z(G.H_PLAF), 0.3)
    for hk in G.HOOKS:
        e.box(hk["y"] - 1, hk["y"] + 1, hk["z"] - 6, hk["z"], FILL["noir"], None)
    e.box(G.SHOWER["y0"], G.D_TOT, G.SHOWER["curb"], G.SHOWER["glass_top"], "url(#p-verre)", GREY, 0.12)
    # boxing cut (Y 0–40, h 145), WC
    e.box(0, G.BOXING["y1"], 0, G.BOXING["h"], POCHE, None)
    e.box(G.BOXING["y1"], G.WC["y1"], 30, 42, FILL["ceram"], INK, 0.22, rx=1.5)
    # window F1 in the south wall (cut) : show opening in the left wall band
    e.s.rect(e.X(-20), e.Z(G.W1["z1"]), 20 * e.k, (G.W1["z1"] - G.W1["z0"]) * e.k, "#FFFFFF", INK, 0.2)
    # shower: curb, glass front (cut, Y 281), column beyond (west wall is behind the viewer: not seen)
    sh = G.SHOWER
    e.box(sh["y0"], G.D_TOT, 0, sh["curb"], "#EDEDED", INK, 0.15)
    e.box(sh["y0"] - 0.6, sh["y0"] + 0.6, sh["curb"], sh["glass_top"], FILL["noir"], None)
    e.finish(G.D_TOT - 1.5, G.D_TOT, 0, G.H_PLAF, "faience")
    e.led(4, G.D_LARGE - 4, G.H_PLAF - 1)
    e.wrap(20, 165, "coffrage WC (coupé)", 14, INK, 1.3)
    e.wrap((sh["y0"] + G.D_TOT) / 2, 230, "douche : paroi coupée, retour vitré au-delà", 22, INK, 1.3)
    e.wrap(95, 215, "au fond : meuble vasque, miroir, commode", 26, GREY, 1.3)
    e.wrap(255, 230, "retour, patères", 14, GREY, 1.3)
    e.chain_h([0, G.BOXING["y1"], G.WC["y1"], sh["y0"], G.D_LARGE, G.D_TOT], ["v", "d", "d", "d", "v"], gap=6)
    e.chain_v([0, G.BOXING["h"], G.W1["z0"], G.W1["z1"], G.H_PLAF], ["d"] * 4, right=False)
    e.chain_v([0, sh["curb"], sh["glass_top"], G.H_PLAF], ["d"] * 3, right=True)
    return e.svg()


def section_BB():
    """Coupe BB (Y ≈ 125), vue vers le nord : gauche = ouest (X 0), droite = est (X 374,8)."""
    e = Elev(G.W_TOT, left_note="mur ouest (coupé)", right_note="mur est (coupé)")
    e.finish(0, G.W_TOT, 0, G.H_PLAF, "trav")
    d0, d1 = G.DOOR_X
    e.box(d0, d1, 0, G.H_DOOR, "#3A332E", INK, 0.25)
    e.box(0, G.W_RET, 0, G.H_PLAF, "none", GREY, 0.15, "0.8 0.5")
    e.note(G.W_RET / 2, 150, "retour de la douche (au-delà)", GREY, 1.4)
    # ladder on the west wall (cut, leaning), vanity cut on the east wall
    e.s.line(e.X(2), e.Z(185), e.X(G.LADDER["depth"]), e.Z(0), 0.6)
    v = G.VANITY
    x0 = G.W_TOT - v["depth"]
    e.box(x0, G.W_TOT, v["z1"] - 3, v["z1"], POCHE, None)
    e.box(x0 + 1, G.W_TOT, v["z0"], v["z1"] - 3, "#6B4E3D", INK, 0.2)
    e.box(G.W_TOT - 4, G.W_TOT, v["z1"], G.SPLASH["z1"], FILL["terrazzo"], INK, 0.15)
    e.box(G.W_TOT - 1.5, G.W_TOT, G.MIRROR["z0"], G.MIRROR["z1"], FILL["miroir"], INK, 0.15)
    e.box(x0 + 8, x0 + 8 + G.BASIN["d"], v["z1"], G.BASIN["z1"], FILL["ceram"], INK, 0.2, rx=1)
    for p in G.PENDANTS[:2]:
        x = e.X(G.PEND_X)
        e.s.line(x, e.Z(G.H_PLAF), x, e.Z(p["z"] + 3), 0.1)
        e.s.circle(x, e.Z(p["z"]), 3 * e.k, "#FFF7E6", INK, 0.15)
    e.led(4, G.W_TOT - 4, G.H_PLAF - 1)
    e.wrap(18, 205, "échelle (coupe)", 12, INK, 1.3)
    e.wrap(G.W_TOT - 40, 230, "meuble vasque (coupé), crédence, miroir", 26, INK, 1.3)
    e.chain_h([0, G.W_RET, d0, d1, x0, G.W_TOT], ["v", "v", "v", "d", "d"], gap=6)
    e.chain_v([0, v["z0"], v["z1"], G.SPLASH["z1"], G.MIRROR["z1"], G.H_PLAF], ["d"] * 5, right=True)
    e.chain_v([0, G.H_DOOR, G.H_PLAF], ["d", "d"], right=False)
    return e.svg()


# ================================================================ FURNITURE (1:10)
def furniture_M1():
    """Meuble vasque : vue de face (1:10) et coupe."""
    k = 1.0
    v = G.VANITY
    L, H = v["y1"] - v["y0"], v["z1"] - v["z0"]
    w = 30 + L * k + 30 + v["depth"] * k + 40
    h = 22 + (G.SPLASH["z1"] - v["z0"] + 12) * k + 26
    s = SVG(w, h)
    ox, oy = 30, 22 + (G.SPLASH["z1"] - v["z0"] + 8) * k
    Z = lambda z: oy - (z - v["z0"]) * k
    X = lambda u: ox + u * k
    s.rect(X(0), Z(v["z1"]), L * k, 3 * k, FILL["terrazzo"], INK, 0.25)
    s.rect(X(0), Z(v["z1"] - 3), (v["y1"] - v["split"]) * k, (H - 3) * k, FILL["noyer"], INK, 0.25)
    zm = (v["z0"] + v["z1"] - 3) / 2
    s.line(X(0), Z(zm), X(v["y1"] - v["split"]), Z(zm), 0.2, "#D6C7B8")
    s.rect(X(v["y1"] - v["split"]), Z(v["z1"] - 3), (v["split"] - v["y0"]) * k, (H - 3) * k, FILL["noyer"], INK, 0.25)
    s.rect(X(v["y1"] - v["split"] + 2.5), Z(zm - 1), (v["split"] - v["y0"] - 5) * k, (zm - 1 - v["z0"] - 2.5) * k, "#2E211A", None)
    s.rect(X(v["y1"] - v["split"] + 2.5), Z(v["z1"] - 5.5), (v["split"] - v["y0"] - 5) * k, (v["z1"] - 5.5 - zm - 1) * k,
           "#2E211A", None)
    bx = v["y1"] - G.BASIN["ay"]
    s.rect(X(0), Z(G.SPLASH["z1"]), L * k, (G.SPLASH["z1"] - v["z1"]) * k, FILL["terrazzo"], GREY, 0.12)
    s.rect(X(bx - G.BASIN["w"] / 2), Z(G.BASIN["z1"]), G.BASIN["w"] * k, (G.BASIN["z1"] - v["z1"]) * k, FILL["ceram"], INK,
           0.22, rx=1.5)
    s.text(X(L / 2), Z(v["z0"]) + 16, "M1 — MEUBLE VASQUE SUSPENDU · FACE", 2.0, INK, weight=500, ls=0.2)
    yb = Z(v["z0"]) + 6
    dh(s, X(0), X(v["y1"] - v["split"]), yb, v["y1"] - v["split"], "d", above=False)
    dh(s, X(v["y1"] - v["split"]), X(L), yb, v["split"] - v["y0"], "d", above=False)
    dh(s, X(0), X(L), yb + 6, L, "d", above=False)
    dh(s, X(bx - G.BASIN["w"] / 2), X(bx + G.BASIN["w"] / 2), Z(G.BASIN["z1"]) - 2, G.BASIN["w"], "c")
    dv(s, Z(v["z0"]), Z(v["z1"]), X(0) - 6, H, "d")
    dv(s, Z(v["z1"]), Z(G.SPLASH["z1"]), X(0) - 6, G.SPLASH["z1"] - v["z1"], "d")
    dv(s, Z(v["z1"] - 3), Z(v["z1"]), X(L) + 4, 3, "c", left=False)
    # section (side)
    sx = X(L) + 26
    s.rect(sx, Z(v["z1"]), v["depth"] * k, 3 * k, FILL["terrazzo"], INK, 0.25)
    s.rect(sx + 2, Z(v["z1"] - 3), (v["depth"] - 2) * k, (H - 3) * k, "#6B4E3D", INK, 0.25)
    s.rect(sx + v["depth"] * k, Z(G.SPLASH["z1"] + 6), 2 * k, (G.SPLASH["z1"] + 6 - v["z0"]) * k, POCHE, None)
    s.rect(sx + (v["depth"] - 2) * k, Z(G.SPLASH["z1"]), 2 * k, (G.SPLASH["z1"] - v["z1"]) * k, FILL["terrazzo"], INK, 0.15)
    s.text(sx + v["depth"] * k / 2, Z(v["z0"]) + 16, "COUPE", 2.0, INK, weight=500, ls=0.2)
    dh(s, sx, sx + v["depth"] * k, yb, v["depth"], "d", above=False)
    dv(s, Z(v["z0"]) + 0, Z(v["z0"]) + 0.01, sx - 3, 0, "d", txt="")
    s.text(sx + v["depth"] * k + 4, Z(v["z0"]) + 1, f"sol fini → dessous du meuble ≈{v['z0']}", 1.5, OLIVE, "start",
           italic=True)
    return s.svg(), w, h


def furniture_M2():
    c = G.COMMODE
    k = 1.0
    L, H = c["x1"] - c["x0"], c["z1"] - c["z0"]
    w = 30 + L * k + 26 + (c["y1"] - c["y0"]) * k + 40
    h = 20 + (H + 20) * k + 26
    s = SVG(w, h)
    ox, oy = 30, 20 + (H + 12) * k
    X = lambda u: ox + u * k
    Z = lambda z: oy - z * k
    s.rect(X(0), Z(c["z1"]), L * k, H * k, FILL["noyer"], INK, 0.25, rx=1.2)
    zm = (c["z0"] + c["z1"]) / 2
    s.line(X(0), Z(zm), X(L), Z(zm), 0.2, "#D6C7B8")
    for zz in (zm + 25, zm - 14):
        s.rect(X(L / 2 - 8), Z(zz + 2.2), 16 * k, 2.2 * k, FILL["noir"], None)
    s.line(X(-5), Z(0), X(L + 5), Z(0), 0.4)
    s.text(X(L / 2), Z(0) + 16, "M2 — COMMODE NOYER · FACE", 2.0, INK, weight=500, ls=0.2)
    dh(s, X(0), X(L), Z(0) + 6, L, "d", above=False)
    dv(s, Z(0), Z(c["z0"]), X(0) - 6, c["z0"], "d")
    dv(s, Z(c["z0"]), Z(c["z1"]), X(0) - 6, H, "d")
    dh(s, X(L / 2 - 8), X(L / 2 + 8), Z(zm + 27.2) - 1.6, 16, "c")
    sx = X(L) + 26
    s.rect(sx, Z(c["z1"]), (c["y1"] - c["y0"]) * k, H * k, "#6B4E3D", INK, 0.25, rx=1.2)
    s.line(sx - 3, Z(0), sx + (c["y1"] - c["y0"]) * k + 5, Z(0), 0.4)
    s.rect(sx + (c["y1"] - c["y0"]) * k, Z(c["z1"] + 10), 2 * k, (c["z1"] + 10) * k, POCHE, None)
    s.text(sx + (c["y1"] - c["y0"]) * k / 2, Z(0) + 16, "CÔTÉ", 2.0, INK, weight=500, ls=0.2)
    dh(s, sx, sx + (c["y1"] - c["y0"]) * k, Z(0) + 6, c["y1"] - c["y0"], "d", above=False)
    return s.svg(), w, h
