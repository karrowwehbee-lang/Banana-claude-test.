"""Views: plans, elevations, sections, key plans. Returns (svg, width_mm, height_mm)."""
import math
import data as D
from draw import (SVG, INK, GREY, OLIVE, BURG, LED, POCHE, FILL, STATUS_COL, dim_h, dim_v, level_mark,
                  bubble, fmt, dim_text)

# ================================================================= plans
class Plan:
    def __init__(self, xmin, xmax, ymin, ymax, scale, pad=(16, 16, 16, 16)):
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.m = 10.0 / scale
        self.pl, self.pt, self.pr, self.pb = pad
        self.w = (xmax - xmin) * self.m + self.pl + self.pr
        self.h = (ymax - ymin) * self.m + self.pt + self.pb
        self.s = SVG(self.w, self.h)

    def P(self, X, Y):
        return self.pl + (X - self.xmin) * self.m, self.pt + (self.ymax - Y) * self.m

    def rect(self, X0, Y0, X1, Y1, **kw):
        x0, y0 = self.P(X0, Y1)
        x1, y1 = self.P(X1, Y0)
        self.s.rect(x0, y0, x1 - x0, y1 - y0, **kw)

    def poly(self, pts, **kw):
        d = "M" + " L".join(f"{self.P(x, y)[0]:.2f},{self.P(x, y)[1]:.2f}" for x, y in pts) + " Z"
        self.s.path(d, **kw)

    def text(self, X, Y, t, **kw):
        x, y = self.P(X, Y)
        self.s.text(x, y, t, **kw)

    # dimension chain along X at plan level Yref, line placed off mm away (negative = below)
    def chain_x(self, pts, Yref, off):
        y_ext = self.P(0, Yref)[1]
        y = y_ext - off
        for (a, _), (b, st) in zip(pts, pts[1:]):
            xa, xb = self.P(a, 0)[0], self.P(b, 0)[0]
            dim_h(self.s, xa, xb, y, b - a, st, ext_y=y_ext, above=True)

    def chain_y(self, pts, Xref, off):
        x_ext = self.P(Xref, 0)[0]
        x = x_ext + off
        for (a, _), (b, st) in zip(pts, pts[1:]):
            ya, yb = self.P(0, a)[1], self.P(0, b)[1]
            dim_v(self.s, ya, yb, x, b - a, st, ext_x=x_ext, left=True)


def poly_area(pts):
    a = 0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        a += x1 * y2 - x2 * y1
    return abs(a) / 2 / 1e4


def _walls(level):
    if level == "RDC":
        return [(D.rect_rdc(x0, x1, y0, y1), k) for x0, x1, y0, y1, k in D.RDC_WALLS]
    return [(D.rect_et(x0, x1, y0, y1), k) for x0, x1, y0, y1, k in D.ET_WALLS]


def _openings(level):
    out = []
    src = D.RDC_OPENINGS if level == "RDC" else D.ET_OPENINGS
    for ax, a, b, band, kind, label, st in src:
        if level == "RDC":
            r = D.rect_rdc(a, b, band[0], band[1]) if ax == "h" else D.rect_rdc(band[0], band[1], a, b)
        else:
            r = D.rect_et(a, b, band[0], band[1]) if ax == "h" else D.rect_et(band[0], band[1], a, b)
        out.append((ax, r, kind, label, st))
    return out


OOS_RDC = [(267, 359, 157, 419), (267, 359, 438, 552), (378, 815, 157, 552), (834, 1031, 157, 258)]
OOS_ET = [(44, 679, 24, 205), (277, 679, 214, 356), (689, 875, 214, 356)]


def draw_architecture(p, level, scope_rooms, label_oos=True):
    s = p.s
    # out of scope hatching
    if level == "RDC":
        for r in OOS_RDC:
            p.rect(*D.rect_rdc(*r), fill="url(#p-hors)", stroke=None)
        if label_oos:
            for (cx, cy) in [(596, 360)]:
                X, Y = D.rdc(cx, cy)
                p.text(X, Y, "HORS PÉRIMÈTRE", size=1.7, col=GREY, ls=0.3)
            X, Y = D.rdc(932, 215); p.text(X, Y, "HORS PÉRIMÈTRE", size=1.5, col=GREY)
            X, Y = D.rdc(905, 480); p.text(X, Y, "DÉGAGEMENT", size=1.6, col=GREY, ls=0.3)
    else:
        for u0, u1, v0, v1 in OOS_ET:
            p.rect(*D.rect_et(u0, u1, v0, v1), fill="url(#p-hors)", stroke=None)
        p.rect(*D.rect_et(277, 487, 443, 505), fill="url(#p-escalier)", stroke=None)
        p.rect(*D.rect_et(277, 371, 366, 443), fill="url(#p-escalier)", stroke=None)
        if label_oos:
            X, Y = D.et(360, 110); p.text(X, Y, "HORS PÉRIMÈTRE", size=1.8, col=GREY, ls=0.3)
            X, Y = D.et(478, 290); p.text(X, Y, "HORS PÉRIMÈTRE (circulation)", size=1.7, col=GREY)
            X, Y = D.et(782, 290); p.text(X, Y, "HORS PÉRIMÈTRE", size=1.6, col=GREY)
            X, Y = D.et(380, 478); p.text(X, Y, "ESCALIER / TRÉMIE", size=1.6, col=GREY)
            X, Y = D.et(380, 486); p.text(X, Y, "(à confirmer)", size=1.4, col=BURG, italic=True)
    # rooms in scope
    for key in scope_rooms:
        p.poly(D.ROOMS[key]["poly"], fill="#FBF8F3", stroke=None)
    if level == "RDC":   # closet "130" of the source plan, absent from the 3D model
        p.rect(*D.rect_rdc(1040, 1101, 157, 277), fill="none", stroke=BURG, sw=0.15, dash="1 0.6")
        X, Y = D.rdc(1070.5, 200)
        p.text(X, Y, "placard 130", size=1.3, col=BURG, italic=True)
        p.text(X, Y - 5.5, "(plan source,", size=1.2, col=BURG, italic=True)
        p.text(X, Y - 11, "absent maquette)", size=1.2, col=BURG, italic=True)
    # stair (RDC, existing)
    if level == "RDC":
        st = D.RDC_STAIR
        x0, x1 = st["x0"], st["x1"]
        for ya, yb in (st["y_up"], st["y_low"]):
            p.rect(*D.rect_rdc(x0, st["landing"][0], ya, yb), fill="#FFFFFF", stroke=GREY, sw=0.12)
            for t in st["treads"]:
                (X, Y0), (_, Y1) = D.rdc(t, ya), D.rdc(t, yb)
                p.s.line(*p.P(X, Y0), *p.P(X, Y1), 0.1, GREY)
        p.rect(*D.rect_rdc(x0, st["landing"][0], st["y_mid"][0], st["y_mid"][1]), fill="#FFFFFF", stroke=GREY, sw=0.12)
        p.rect(*D.rect_rdc(st["landing"][0], x1, st["y_up"][0], st["y_low"][1]), fill="#FFFFFF", stroke=GREY, sw=0.12)
        X, Y = D.rdc(1110, 532); p.text(X, Y, "ESCALIER EXISTANT", size=1.5, col=GREY)
        X, Y = D.rdc(955, 530); p.text(X, Y, "HAUT", size=1.5, col=GREY, anchor="end")
    # walls
    for (X0, Y0, X1, Y1), k in _walls(level):
        p.rect(X0, Y0, X1, Y1, fill=("#9A9A9A" if k == "oos" else POCHE), stroke=None)
    # openings
    for ax, (X0, Y0, X1, Y1), kind, label, st in _openings(level):
        x0, y0 = p.P(X0, Y1)
        x1, y1 = p.P(X1, Y0)
        if st == "c":
            s.rect(x0, y0, x1 - x0, y1 - y0, fill="#FFFFFF", stroke=BURG, sw=0.15, dash="0.8 0.5")
            continue
        s.rect(x0, y0, x1 - x0, y1 - y0, fill="#FFFFFF", stroke=None)
        if ax == "h":
            s.line(x0, y0, x0, y1, 0.25); s.line(x1, y0, x1, y1, 0.25)
            if kind in ("window", "glazed"):
                for f in (0.0, 0.5, 1.0) if kind == "window" else (0.0, 0.42, 0.58, 1.0):
                    yy = y0 + (y1 - y0) * f
                    s.line(x0, yy, x1, yy, 0.12 if f in (0.0, 1.0) else 0.18)
                if kind == "glazed":
                    s.line((x0 + x1) / 2, y0, (x0 + x1) / 2, y1, 0.12)
            elif kind == "door":
                s.line(x0, (y0 + y1) / 2, x1, (y0 + y1) / 2, 0.1, GREY, dash="0.6 0.4")
        else:
            s.line(x0, y0, x1, y0, 0.25); s.line(x0, y1, x1, y1, 0.25)
            if kind in ("window", "glazed"):
                for f in (0.0, 0.5, 1.0):
                    xx = x0 + (x1 - x0) * f
                    s.line(xx, y0, xx, y1, 0.12 if f in (0.0, 1.0) else 0.18)
            elif kind == "door":
                s.line((x0 + x1) / 2, y0, (x0 + x1) / 2, y1, 0.1, GREY, dash="0.6 0.4")


def draw_furniture(p, room, numbers=True):
    s = p.s
    for f in D.FURN[room]:
        if f[0] == "rect":
            (X0, Y0, X1, Y1), kind, label = f[1], f[2], f[3]
            if kind == "rug":
                p.rect(X0, Y0, X1, Y1, fill="none", stroke="#B9AE9F", sw=0.12, dash="1 0.6")
                continue
            fill = {"custom": "#EEF0E6", "sofa": "#F4F1EC", "table": "#F7F5F1", "bed": "#F4F1EC",
                    "chair": "#F4F1EC"}.get(kind, "#FFFFFF")
            p.rect(X0, Y0, X1, Y1, fill=fill, stroke=("#55603C" if kind == "custom" else "#6E6E6E"),
                   sw=(0.22 if kind == "custom" else 0.14))
            if kind == "custom" and numbers:
                x, y = p.P((X0 + X1) / 2, (Y0 + Y1) / 2)
                bubble(s, x, y, label, r=2.0, col=OLIVE, size=1.5)
            elif label and kind in ("sofa", "table", "bed"):
                x, y = p.P((X0 + X1) / 2, (Y0 + Y1) / 2)
                w = abs(p.P(X1, 0)[0] - p.P(X0, 0)[0])
                h = abs(p.P(0, Y1)[1] - p.P(0, Y0)[1])
                if w >= h:
                    s.text(x, y + 0.5, label, 1.35, "#6E6E6E")
                else:
                    s.text(x + 0.5, y, label, 1.35, "#6E6E6E", rot=-90)
        else:
            _, X, Y, r, kind, label = f
            x, y = p.P(X, Y)
            s.circle(x, y, r * p.m, "#FFFFFF", "#6E6E6E", 0.12)


def room_label(p, key, X, Y, area=True):
    r = D.ROOMS[key]
    s = p.s
    x, y = p.P(X, Y)
    s.text(x, y, r["short"].upper(), 2.1, INK, weight=500, ls=0.25)
    if area:
        a = poly_area(r["poly"])
        s.text(x, y + 2.9, f"S ≈ {a:.1f} m²".replace(".", ","), 1.8, OLIVE, italic=True)
        s.text(x, y + 5.5, f"HSP ≈ {r['height']} (sous faux-plafond)", 1.6, OLIVE, italic=True)


WALL_MARKS = {   # room -> wall -> (X, Y of marker in plan, direction angle deg: 0 = north, 90 = east)
    "sejour": {"A": (330, 360, 0), "B": (955, 215, 0), "C": (1095, 150, 90), "D": (560, 60, 180), "E": (60, 212, 270)},
    "amis": {"A": (1000, 815, 0), "B": (1095, 709, 90), "C": (1000, 610, 180), "D": (885, 709, 270)},
    "etsejour": {"A": (201, 460, 0), "B": (345, 262, 90), "C": (201, 45, 180), "D": (55, 262, 270)},
    "princ": {"A": (1430, 62, 90), "B": (930, 0, 270), "C": (1100, 200, 0), "D": (1100, -80, 180)},
}


def wall_marker(p, X, Y, ang, letter, col=INK):
    s = p.s
    x, y = p.P(X, Y)
    a = math.radians(ang)
    dx, dy = math.sin(a), -math.cos(a)
    tip = (x + dx * 4.2, y + dy * 4.2)
    l = (x + dx * 2.1 - dy * 1.9, y + dy * 2.1 + dx * 1.9)
    r = (x + dx * 2.1 + dy * 1.9, y + dy * 2.1 - dx * 1.9)
    s.path(f"M{tip[0]:.2f},{tip[1]:.2f} L{l[0]:.2f},{l[1]:.2f} L{r[0]:.2f},{r[1]:.2f} Z", fill=col, stroke=None)
    s.circle(x, y, 2.4, "#FFFFFF", col, 0.22)
    s.text(x, y + 0.75, letter, 2.1, col, weight=500)


SECTION_MARKS = {   # room -> list of (name, (X0, Y0), (X1, Y1), look angle)
    "sejour": [("AA", (300, -60), (300, 490), 270), ("BB", (-60, 150), (1215, 150), 0)],
    "amis": [("CC", (1080, 520), (1080, 900), 90)],
    "etsejour": [("DD", (300, -50), (300, 575), 90)],
    "princ": [("EE", (1330, -160), (1330, 285), 90)],
}


def section_marker(p, name, a, b, ang):
    s = p.s
    xa, ya = p.P(*a)
    xb, yb = p.P(*b)
    s.line(xa, ya, xb, yb, 0.18, INK, dash="3 1 0.6 1")
    rad = math.radians(ang)
    dx, dy = math.sin(rad), -math.cos(rad)
    for (x, y) in ((xa, ya), (xb, yb)):
        s.path(f"M{x:.2f},{y:.2f} l{dx*3.4 - dy*1.4:.2f},{dy*3.4 + dx*1.4:.2f} l{dy*2.8:.2f},{-dx*2.8:.2f} Z",
               fill=INK, stroke=None)
        s.text(x + dx * 5.6, y + dy * 5.6 + 0.8, name[0], 2.2, INK, weight=500)


# ----------------------------------------------------------------- general plans
def plan_rdc_general(scale=50, furniture=False):
    p = Plan(-40, 1190, -40, 935, scale, pad=(22, 22, 26, 26))
    draw_architecture(p, "RDC", ["sejour", "amis"])
    if furniture:
        draw_furniture(p, "sejour"); draw_furniture(p, "amis")
    room_label(p, "sejour", 330, 230)
    room_label(p, "amis", 1000, 690)
    # exterior chains (written dimensions of the source plan)
    p.chain_x([(0, None), (1122.1, "v")], -20.5, -9)
    p.chain_x([(-20.5, None), (1170.7, "d")], -20.5, -16)
    p.chain_x([(119.9, None), (591.8, "v")], 891.0, 9)
    p.chain_x([(834.8, None), (1150.2, "v")], 891.0, 15)
    p.chain_x([(-20.5, None), (1170.7, "d")], 891.0, 21)
    p.chain_y([(0, None), (424.4, "v")], -20.5, -9)
    p.chain_y([(443.9, None), (870.5, "v")], -20.5, -9)
    p.chain_y([(-20.5, None), (891.0, "d")], -20.5, -16)
    p.chain_y([(0, None), (32.4, "v"), (268.9, "v")], 1170.7, 9)
    p.chain_y([(548.6, None), (870.5, "v")], 1170.7, 9)
    p.chain_y([(-20.5, None), (891.0, "d")], 1170.7, 16)
    # interior written dimensions
    p.chain_x([(0, None), (378.1, "v"), (584.9, "v"), (654.7, "v")], 424.4, 5.5)
    p.chain_x([(759.2, None), (845.0, "v"), (987.0, "v"), (1150.2, "v")], 268.9, -6)
    p.chain_y([(567.0, None), (870.5, "v")], 0, 10)  # 303.6 strip (west)
    p.chain_y([(740.9, None), (870.5, "v")], 1101 * 0 + 900.7, 3)
    p.chain_y([(443.9, None), (870.5, "v")], 591.8, -4)
    return p.s.svg(), p.w, p.h


def plan_et_general(scale=75, furniture=False):
    X0, Y0 = D.et(35, 584)
    X1, Y1 = D.et(885, 14)
    p = Plan(X0 - 20, X1 + 20, Y0 - 20, Y1 + 20, scale, pad=(22, 22, 26, 26))
    draw_architecture(p, "ET", ["etsejour", "princ"])
    if furniture:
        draw_furniture(p, "etsejour"); draw_furniture(p, "princ")
    room_label(p, "etsejour", 201, 300)
    room_label(p, "princ", 1150, 50)
    p.chain_x([(X0, None), (X1, "d")], Y0, -10)
    p.chain_x([(X0, None), (0, "d"), (402.5, "d"), (D.et(496.5, 0)[0], "d"), (1499.5, "d"), (X1, "d")], Y0, -4)
    p.chain_y([(Y0, None), (Y1, "d")], X0, -10)
    p.chain_y([(Y0, None), (-126.4, "d"), (0, "d"), (524.4, "d"), (D.et(0, 14)[1] - 18, "d")], X1, 8)
    return p.s.svg(), p.w, p.h


# ----------------------------------------------------------------- room plans
ROOM_VIEW = {
    "sejour": dict(level="RDC", box=(-22, 1172, -45, 470), scale=40, pad=(16, 14, 18, 22)),
    "amis": dict(level="RDC", box=(580, 1190, 515, 905), scale=25),
    "etsejour": dict(level="ET", box=(-40, 445, -40, 565), scale=30),
    "princ": dict(level="ET", box=(570, 1540, -170, 290), scale=40),
}


def plan_room(key):
    cfg = ROOM_VIEW[key]
    x0, x1, y0, y1 = cfg["box"]
    p = Plan(x0, x1, y0, y1, cfg["scale"], pad=cfg.get("pad", (20, 20, 20, 22)))
    p.s.add(f'<clipPath id="clip-{key}"><rect x="{p.pl - 6}" y="{p.pt - 6}" width="{p.w - p.pl - p.pr + 12}" '
            f'height="{p.h - p.pt - p.pb + 12}"/></clipPath><g clip-path="url(#clip-{key})">')
    draw_architecture(p, cfg["level"], [key], label_oos=False)
    draw_furniture(p, key)
    p.s.add("</g>")
    for L, (X, Y, ang) in WALL_MARKS[key].items():
        wall_marker(p, X, Y, ang, L)
    for name, a, b, ang in SECTION_MARKS[key]:
        section_marker(p, name, a, b, ang)
    room_dims(p, key)
    return p.s.svg(), p.w, p.h


def room_dims(p, key):
    if key == "sejour":
        p.chain_x([(0, None), (1122.1, "v")], 0, -14)
        p.chain_x([(0, None), (367.7, "d"), (530.8, "d"), (635.0, "d"), (707.4, "d"), (823.0, "d"), (937.4, "d"),
                   (1122.1, "d")], 0, -8)
        p.chain_x([(0, None), (378.1, "v"), (584.9, "v"), (654.7, "v"), (672.8, "d"), (759.2, "d")], 424.4, 5)
        p.chain_x([(759.2, None), (845.0, "v"), (987.0, "v"), (1150.2, "v")], 268.9, -5)
        p.chain_x([(0, None), (117.7, "d"), (377.0, "d")], 424.4, 10)
        p.chain_y([(0, None), (2.2, "d"), (68.0, "d"), (356.4, "d"), (422.3, "d"), (424.4, "d")], 0, -6)
        p.chain_y([(0, None), (424.4, "v")], 0, -12)
        p.chain_y([(0, None), (32.4, "v"), (268.9, "v")], 1150.2, 7)
        p.chain_y([(380.2, None), (424.4, "d")], 654.5, -3)
    elif key == "amis":
        p.chain_x([(834.8, None), (1150.2, "v")], 870.5, 11)
        p.chain_x([(612.4, None), (662.0, "d"), (746.3, "d"), (834.8, "d")], 740.9, 10)
        p.chain_x([(856.4, None), (1150.2, "d")], 548.6, -11)
        p.chain_x([(662.0, None), (746.3, "d")], 600.5, -4)
        p.chain_y([(548.6, None), (870.5, "v")], 1150.2, 18)
        p.chain_y([(548.6, None), (719.3, "d"), (841.3, "d"), (870.5, "d")], 1150.2, 11)
        p.chain_y([(600.5, None), (740.9, "d")], 612.4, -6)
        X0, Y0, X1, Y1 = D.rect_tv(647, 757, 65, 185)
        p.chain_x([(834.8, None), (X0, "d"), (X1, "d"), (1150.2, "d")], Y0, -5)
        p.chain_y([(Y0, None), (Y1, "d"), (870.5, "d")], X1, 5)
    elif key == "etsejour":
        p.chain_x([(0, None), (402.5, "d")], 0, -12)
        p.chain_x([(0, None), (62.3, "d"), (343.9, "d"), (402.5, "d")], 524.4, 9)
        p.chain_y([(0, None), (524.4, "d")], 0, -10)
        p.chain_y([(0, None), (161.8, "d"), (300.8, "d"), (457.3, "d"), (524.4, "d")], 402.5, 7)
        X0, Y0, X1, Y1 = D.rect_et(75, 245, 410, 464)
        p.chain_y([(0, None), (Y0, "d"), (Y1, "d")], X0, -4)
        p.chain_x([(0, None), (X0, "d"), (X1, "d")], Y0, -5)
    elif key == "princ":
        p.chain_x([(816.3, None), (1499.5, "d")], -126.4, -10)
        p.chain_x([(605.6, None), (816.3, "d"), (1499.5, "d")], 250.9, 6)
        p.chain_y([(-126.4, None), (250.9, "d")], 1499.5, 8)
        p.chain_y([(-126.4, None), (-122.7, "d"), (108.3, "d"), (128.2, "d")], 816.3, -6)
        p.chain_y([(128.2, None), (250.9, "d")], 605.6, -6)
        X0, Y0, X1, Y1 = D.rect_et(730, 867, 405, 537)
        p.chain_y([(-126.4, None), (Y0, "d"), (Y1, "d"), (250.9, "d")], X0, -4)
        p.chain_x([(816.3, None), (887.6, "d")], -126.4, -4)


# ================================================================= elevations
def _box(s, x, y, w, h, mat, ghost=False, dash=None, rx=0):
    fill = FILL.get(mat, "#FFFFFF")
    s.rect(x, y, w, h, fill=fill, stroke=(GREY if ghost else INK), sw=(0.1 if ghost else 0.15), dash=dash, rx=rx,
           op=(0.35 if ghost else None))


def elev_view(room, key, scale=25, crop=None, ghost=False, show_dims=True, show_levels=True, labels=True,
              margins=(16, 14, 12, 12)):
    E = D.ELEV[room][key]
    H = D.ROOMS[room]["height"]
    W = E["width"]
    cx0, cx1, cz0, cz1 = crop if crop else (0, W, 0, H)
    m = 10.0 / scale
    nb = max([c[2] for c in E["dims"] if c[0] == "h"] + [0]) if show_dims and not crop else 0
    nt = max([c[2] for c in E["dims"] if c[0] == "t"] + [0]) if show_dims and not crop else 0
    nv = len([c for c in E["dims"] if c[0] == "v" and len(c) == 3]) if show_dims and not crop else 0
    ml, mr, mt, mb = margins
    ml = ml + (6 if crop else 0)
    if crop and show_dims:
        nb = sum(1 for c in E["dims"] if c[0] in ("h", "t") and any(
            a_ >= cx0 - 0.2 and b_ <= cx1 + 0.2 for (a_, _), (b_, _) in zip(c[1], c[1][1:])))
        nv = sum(1 for c in E["dims"] if c[0] == "v" and (len(c) == 3 or cx0 - 0.2 <= c[3] <= cx1 + 0.2))
    mb = mb + nb * 6.5 + (8 if crop else 0)
    mt = mt + nt * 6.5
    mr = mr + nv * 6.5
    w = (cx1 - cx0) * m + ml + mr
    h = (cz1 - cz0) * m + mt + mb
    s = SVG(w, h)
    X = lambda x: ml + (x - cx0) * m
    Z = lambda z: mt + (cz1 - z) * m
    col = GREY if ghost else INK
    if crop:
        s.add(f'<clipPath id="c-{room}{key}{int(cx0)}{int(cx1)}"><rect x="{X(cx0)}" y="{Z(cz1)}" width="{(cx1-cx0)*m}" '
              f'height="{(cz1-cz0)*m}"/></clipPath><g clip-path="url(#c-{room}{key}{int(cx0)}{int(cx1)})">')
    for el in E["els"]:
        t = el[0]
        if t == "zone":
            _, x0, x1, z0, z1, mat = el
            if mat in ("enduit", "panneau"):
                s.rect(X(x0), Z(z1), (x1 - x0) * m, (z1 - z0) * m, fill=FILL[mat], stroke=None)
            else:
                _box(s, X(x0), Z(z1), (x1 - x0) * m, (z1 - z0) * m, mat, ghost)
        elif t == "rzone":
            _, x0, x1, z0, z1, mat, corners = el
            r = 10 * m
            x_0, x_1, y_0, y_1 = X(x0), X(x1), Z(z1), Z(z0)
            tl, tr, br, bl = [(r if c in corners.split() else 0) for c in ("tl", "tr", "br", "bl")]
            d = (f"M{x_0 + tl:.2f},{y_0:.2f} H{x_1 - tr:.2f} Q{x_1:.2f},{y_0:.2f} {x_1:.2f},{y_0 + tr:.2f} "
                 f"V{y_1 - br:.2f} Q{x_1:.2f},{y_1:.2f} {x_1 - br:.2f},{y_1:.2f} H{x_0 + bl:.2f} "
                 f"Q{x_0:.2f},{y_1:.2f} {x_0:.2f},{y_1 - bl:.2f} V{y_0 + tl:.2f} Q{x_0:.2f},{y_0:.2f} {x_0 + tl:.2f},{y_0:.2f} Z")
            s.path(d, fill=FILL[mat], stroke=col, sw=0.18, extra=('fill-opacity="0.35"' if ghost else ""))
            if not ghost:
                s.path(d, fill="none", stroke=LED, sw=0.25, dash="0.4 0.4")
        elif t == "open":
            _, x0, x1, z0, z1, kind, label = el
            if z0 is None:
                for xx in (x0, x1):
                    s.line(X(xx), Z(0), X(xx), Z(H), 0.18, GREY if ghost else BURG, dash="1 0.6")
                if labels:
                    s.wrap((X(x0) + X(x1)) / 2, Z(H / 2), f"{label} — allège et linteau à confirmer",
                           max(10, (x1 - x0) * m), 1.6, BURG, italic=True)
                continue
            x_0, y_0, ww, hh = X(x0), Z(z1), (x1 - x0) * m, (z1 - z0) * m
            if kind in ("window", "glazed"):
                s.rect(x_0, y_0, ww, hh, fill="url(#p-verre)", stroke=col, sw=0.3)
                s.rect(x_0 + 0.6, y_0 + 0.6, ww - 1.2, hh - 1.2, fill="none", stroke=col, sw=0.12)
            elif kind in ("door", "door2"):
                s.rect(x_0, y_0, ww, hh, fill=("#5A4A3F" if not ghost else "#D8D2CC"), stroke=col, sw=0.3)
                if kind == "door2":
                    s.line(x_0 + ww / 2, y_0, x_0 + ww / 2, y_0 + hh, 0.18, "#D9CFC4")
            elif kind == "passage":
                s.rect(x_0, y_0, ww, hh, fill="#FFFFFF", stroke=col, sw=0.3)
                s.line(x_0, y_0, x_0 + ww, y_0 + hh, 0.1, GREY); s.line(x_0 + ww, y_0, x_0, y_0 + hh, 0.1, GREY)
            if labels and label:
                s.wrap(x_0 + ww / 2, y_0 + 3.2, label, max(10, ww - 2), 1.5,
                       "#F2ECE6" if kind in ("door", "door2") and not ghost else col)
        elif t == "tv":
            _, x0, x1, z0, z1 = el
            s.rect(X(x0) - 0.4, Z(z1) - 0.4, (x1 - x0) * m + 0.8, (z1 - z0) * m + 0.8, fill="none", stroke=LED, sw=0.3,
                   dash="0.5 0.4")
            s.rect(X(x0), Z(z1), (x1 - x0) * m, (z1 - z0) * m, fill=("#2E2E2E" if not ghost else "#BDBDBD"), stroke=col, sw=0.2)
            if labels:
                s.text((X(x0) + X(x1)) / 2, (Z(z0) + Z(z1)) / 2 + 0.6, "TV 75\" (≈ 167 × 93)", 1.7, "#E8E8E8")
        elif t == "box":
            _, x0, x1, z0, z1, mat, label = el
            _box(s, X(x0), Z(z1), (x1 - x0) * m, (z1 - z0) * m, mat, ghost)
            if labels and label:
                lab = label.split(" — ")[0]
                if lab.startswith("M"):
                    bubble(s, (X(x0) + X(x1)) / 2, Z(z1) + 2.6 if (z1 - z0) * m > 6 else Z(z1) - 2.6, lab, 2.0,
                           col=OLIVE, size=1.5)
        elif t == "vline":
            _, x, z0, z1, kind = el
            s.line(X(x), Z(z0), X(x), Z(z1), 0.28 if kind == "led" else 0.1, LED if kind == "led" else GREY,
                   dash=("0.6 0.4" if kind == "led" else None))
        elif t == "hline":
            _, z, x0, x1, kind = el
            s.line(X(x0), Z(z), X(x1), Z(z), 0.28 if kind == "led" else 0.1, LED if kind == "led" else GREY,
                   dash=("0.6 0.4" if kind == "led" else None))
        elif t == "art":
            _, x0, x1, z0, z1, label = el
            s.rect(X(x0), Z(z1), (x1 - x0) * m, (z1 - z0) * m, fill="#FFFFFF", stroke=col, sw=0.18)
            s.rect(X(x0) + 0.7, Z(z1) + 0.7, (x1 - x0) * m - 1.4, (z1 - z0) * m - 1.4, fill="none", stroke=GREY, sw=0.08)
            if labels:
                s.wrap((X(x0) + X(x1)) / 2, (Z(z0) + Z(z1)) / 2, label, (x1 - x0) * m - 2, 1.6, GREY, italic=True)
        elif t == "dash":
            _, x0, x1, z0, z1, label = el
            s.rect(X(x0), Z(z1), (x1 - x0) * m, (z1 - z0) * m, fill="none", stroke=GREY if ghost else BURG, sw=0.15,
                   dash="1 0.6")
            if labels:
                s.wrap((X(x0) + X(x1)) / 2, (Z(z0) + Z(z1)) / 2, label, max(12, (x1 - x0) * m - 1), 1.5, BURG, italic=True)
        elif t == "note":
            _, x, z, txt = el
            if labels:
                s.wrap(X(x), Z(z), txt, min(70, W * m * 0.8), 1.7, BURG, italic=True)
    # wall frame: floor, soffit, side walls (cut)
    s.rect(X(0), Z(H), W * m, H * m, fill="none", stroke=col, sw=0.45)
    if crop:
        s.add("</g>")
        s.rect(X(cx0), Z(cz1), (cx1 - cx0) * m, (cz1 - cz0) * m, fill="none", stroke=GREY, sw=0.1, dash="1 0.8")
    else:
        s.rect(X(0) - 2.2, Z(0), W * m + 4.4, 1.6, fill="url(#p-dalle)", stroke=col, sw=0.15)
        for xx in (X(0) - 2.2, X(W)):
            s.rect(xx, Z(H) - 3.5, 2.2, H * m + 3.5, fill=POCHE if not ghost else "#BBBBBB", stroke=None)
        s.line(X(0), Z(H) - 3.5, X(W), Z(H) - 3.5, 0.12, BURG, dash="1 0.6")
        if labels:
            s.text(X(W / 2), Z(H) - 4.4, "Plafond central (au-dessus de la gorge lumineuse) : hauteur à confirmer", 1.6,
                   BURG, italic=True)
    if show_levels and not crop:
        level_mark(s, X(0) - 6.5, Z(0), "±0,00", "v", right=False)
        level_mark(s, X(0) - 6.5, Z(H), f"≈ +{H / 100:.2f}".replace(".", ","), "d", right=False)
    if show_dims and crop:
        lvl = 0
        for c in E["dims"]:
            if c[0] not in ("h", "t"):
                continue
            segs = [((a_, b_), st) for (a_, _), (b_, st) in zip(c[1], c[1][1:]) if a_ >= cx0 - 0.2 and b_ <= cx1 + 0.2]
            if not segs:
                continue
            lvl += 1
            y = Z(cz0) + 2.0 + lvl * 6.2
            for (a_, b_), st in segs:
                dim_h(s, X(a_), X(b_), y, b_ - a_, st, ext_y=Z(cz0))
        vl = 0
        for c in E["dims"]:
            if c[0] != "v":
                continue
            xref = c[3] if len(c) > 3 else W
            if not (cx0 - 0.2 <= xref <= cx1 + 0.2) and len(c) > 3:
                continue
            vl += 1
            xx = X(cx1) + 4.0 + (vl - 1) * 6.2
            for (a_, _), (b_, st) in zip(c[1], c[1][1:]):
                if a_ >= cz0 - 0.2 and b_ <= cz1 + 0.2:
                    dim_v(s, Z(a_), Z(b_), xx, b_ - a_, st, ext_x=X(min(xref, cx1)))
    if show_dims and not crop:
        for c in E["dims"]:
            kind, pts, lvl = c[0], c[1], c[2]
            if kind in ("h", "t"):
                y = Z(0) + 2.0 + lvl * 6.2 if kind == "h" else Z(H) - 4.0 - lvl * 6.2 - 2.5
                ext = Z(0) if kind == "h" else Z(H) - 3.5
                for (a, _), (b, st) in zip(pts, pts[1:]):
                    dim_h(s, X(a), X(b), y, b - a, st, ext_y=ext)
            else:
                xref = c[3] if len(c) > 3 else W
                xx = X(W) + 4.0 + (lvl - 1) * 6.2 if len(c) == 3 else X(xref) + 3.5
                for (a, _), (b, st) in zip(pts, pts[1:]):
                    dim_v(s, Z(a), Z(b), xx, b - a, st, ext_x=X(xref))
    return s.svg(), w, h


def piece_dims_view(room, key, crop, scale=20, title_dims=None):
    """Cropped elevation of a custom piece with overall dimensions."""
    svg, w, h = elev_view(room, key, scale=scale, crop=crop, show_dims=False, show_levels=False)
    return svg, w, h


# ================================================================= sections
SECTIONS = {
    "sejour": [
        dict(name="AA", title="Coupe AA — salon (nord-sud, vue vers l'ouest)", far=("sejour", "E"), width=424.4,
             left="Mur sud (façade)", right="Mur nord (mur TV)", soffit=(50, "d"), wst="v",
             profiles=[("right", 0, 32, 19.8, 53.7, "laque", "M1"), ("right", 0, 5, 60.7, 225.2, "chene", "")],
             scale=50),
        dict(name="BB", title="Coupe BB — séjour (est-ouest, vue vers le nord)", far=None, width=1150.2,
             left="Mur ouest (façade)", right="Mur est (façade)", soffit=(50, "d"), profiles=[], scale=50,
             fars=[(0, ("sejour", "A")), (759.2, ("sejour", "B"))], division=536),
    ],
    "amis": [dict(name="CC", title="Coupe CC — chambre d'amis (nord-sud, vue vers l'est)", far=("amis", "B"),
                  width=321.9, left="Mur nord (tête de lit)", right="Mur sud (TV)", soffit=(None, "c"), wst="v",
                  profiles=[("right", 0, 39, 48.8, 72.4, "chene", "M6")], scale=25)],
    "etsejour": [dict(name="DD", title="Coupe DD — séjour de l'étage (nord-sud, vue vers l'est)", far=("etsejour", "B"),
                      width=524.4, left="Mur nord (TV)", right="Mur sud (baies)", soffit=(None, "c"),
                      profiles=[("left", 0, 32, 17, 49, "chene", "M9a")], scale=25)],
    "princ": [dict(name="EE", title="Coupe EE — chambre principale (nord-sud, vue vers l'est)", far=("princ", "A"),
                   width=377.3, left="Mur nord (baie vitrée)", right="Mur sud (baies)", soffit=(None, "c"),
                   profiles=[], scale=25)],
}


def section_view(room, sec):
    H = D.ROOMS[room]["height"]
    W = sec["width"]
    sc = sec["scale"]
    m = 10.0 / sc
    ml, mr, mt, mb = 26, 26, 22, 22
    wall = 20
    w = (W + 2 * wall) * m + ml + mr
    h = (H + 20 + 45) * m + mt + mb
    s = SVG(w, h)
    X = lambda x: ml + (x + wall) * m
    Z = lambda z: mt + (H + 45 - z) * m
    # far elevations in projection (ghost)
    fars = sec.get("fars") or ([(0, sec["far"])] if sec["far"] else [])
    for off, (r, k) in fars:
        svg, ew, eh = elev_view(r, k, scale=sc, ghost=True, show_dims=False, show_levels=False, labels=False,
                                margins=(0, 0, 0, 0))
        s.add(f'<g transform="translate({X(off):.2f},{Z(D.ROOMS[r]["height"]):.2f})">' +
              svg.split(">", 1)[1].rsplit("</svg>", 1)[0] + "</g>")
    # slab
    s.rect(X(-wall), Z(0), (W + 2 * wall) * m, 20 * m, fill="url(#p-dalle)", stroke=INK, sw=0.3)
    s.text(X(W / 2), Z(0) + 20 * m / 2 + 0.7, "Dalle — épaisseur à confirmer", 1.7, BURG, italic=True)
    # cut walls
    for x0 in (-wall, W):
        s.rect(X(x0), Z(H + 45), wall * m, (H + 45) * m, fill=POCHE, stroke=None)
    # soffit bands
    sw_, st = sec["soffit"]
    swv = sw_ if sw_ else 40
    for x0, x1 in ((0, swv), (W - swv, W)):
        s.rect(X(x0), Z(H + 12), (x1 - x0) * m, 12 * m, fill="#FFFFFF", stroke=INK, sw=0.3,
               dash=(None if st == "d" else "1 0.6"))
    s.line(X(swv), Z(H + 22), X(W - swv), Z(H + 22), 0.3, BURG, dash="1.2 0.8")
    s.text(X(W / 2), Z(H + 22) - 1.2, "Plafond central — hauteur à confirmer", 1.8, BURG, italic=True)
    s.text(X(W / 2), Z(H + 45) + 3.0, "Structure / plancher haut — à confirmer", 1.6, GREY, italic=True)
    for x in (X(swv), X(W - swv)):
        s.circle(x, Z(H + 5), 0.6, LED, None)
    if sec.get("division"):
        xd = sec["division"]
        s.rect(X(xd) - 0.4, Z(H + 22), 0.8, 22 * m, fill=INK, stroke=None)
        s.text(X(xd), Z(H + 22) - 4.2, "Profil noir : séparation des deux caissons (≈ position)", 1.6, OLIVE, italic=True)
    # profiles (custom furniture cut)
    for side, d0, d1, z0, z1, mat, lab in sec["profiles"]:
        if side == "right":
            x0, x1 = W - d1, W - d0
        else:
            x0, x1 = d0, d1
        s.rect(X(x0), Z(z1), (x1 - x0) * m, (z1 - z0) * m, fill=FILL.get(mat, "#FFFFFF"), stroke=INK, sw=0.3)
        if lab:
            bubble(s, (X(x0) + X(x1)) / 2, Z(z1) - 3, lab, 1.9, col=OLIVE, size=1.4)
    # dims
    dim_v(s, Z(0), Z(H), X(-wall) - 6, H, "d", ext_x=X(-wall))
    if sw_:
        dim_h(s, X(0), X(swv), Z(H + 12) - 3.0, swv, st, ext_y=Z(H + 12))
    else:
        dim_h(s, X(0), X(swv), Z(H + 12) - 3.0, None, "c", ext_y=Z(H + 12), txt="largeur à conf.")
    dim_h(s, X(0), X(W), Z(0) + 20 * m + 6, W, sec.get("wst", "d"), ext_y=Z(0) + 20 * m)
    for side, d0, d1, z0, z1, mat, lab in sec["profiles"][:1]:
        x0, x1 = (W - d1, W) if side == "right" else (0, d1)
        dim_h(s, X(x0), X(x1), Z(z0) + 4, d1 - d0, "d", ext_y=Z(z0))
        xx = X(x1) + 3 if side == "left" else X(x0) - 3
        dim_v(s, Z(0), Z(z0), xx, z0, "d", ext_x=X(x0) if side == "right" else X(x1))
        dim_v(s, Z(z0), Z(z1), xx, z1 - z0, "d", ext_x=X(x0) if side == "right" else X(x1))
    level_mark(s, X(-wall) - 12, Z(0), "±0,00", "v", right=False)
    level_mark(s, X(-wall) - 12, Z(H), f"≈ +{H / 100:.2f}".replace(".", ","), "d", right=False)
    s.text(X(-wall / 2), Z(H + 45) - 2, sec["left"], 1.7, INK, anchor="start" if False else "middle")
    s.text(X(W + wall / 2), Z(H + 45) - 2, sec["right"], 1.7, INK)
    return s.svg(), w, h


# ================================================================= key plan (small)
def key_plan(room, highlight=None, arrow=None, size=(46, 34)):
    poly = D.ROOMS[room]["poly"]
    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
    W, Hh = max(xs) - min(xs), max(ys) - min(ys)
    m = min((size[0] - 8) / W, (size[1] - 8) / Hh)
    s = SVG(size[0], size[1])
    ox = (size[0] - W * m) / 2
    oy = (size[1] - Hh * m) / 2
    P = lambda x, y: (ox + (x - min(xs)) * m, oy + (max(ys) - y) * m)
    d = "M" + " L".join(f"{P(x, y)[0]:.2f},{P(x, y)[1]:.2f}" for x, y in poly) + " Z"
    s.path(d, fill="#F4F1EC", stroke=INK, sw=0.35)
    if highlight:
        X, Y, ang = WALL_MARKS[room][highlight[0]]
        x, y = P(X, Y)
        a = math.radians(ang)
        dx, dy = math.sin(a), -math.cos(a)
        s.line(x - dx * 3, y - dy * 3, x + dx * 3.5, y + dy * 3.5, 0.35, BURG)
        s.path(f"M{x + dx * 5:.2f},{y + dy * 5:.2f} l{-dx * 2 - dy * 1.3:.2f},{-dy * 2 + dx * 1.3:.2f} "
               f"l{dy * 2.6:.2f},{-dx * 2.6:.2f} Z", fill=BURG, stroke=None)
        s.text(x - dx * 4.8, y - dy * 4.8 + 0.7, highlight, 2.0, BURG, weight=500)
    return s.svg(), size[0], size[1]
