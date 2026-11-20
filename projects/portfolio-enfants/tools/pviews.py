"""Technical drawings for the children's rooms portfolio (paper units: mm). Dimensions are proposed concept values."""
import json
import math
import pathlib
import random

HERE = pathlib.Path(__file__).resolve().parent
TEINTES = json.loads((HERE / "teintes.json").read_text())
TEINTES["01"]["velours_rose"] = "#BA7E69"   # lit area of the pouf (the first sample fell in its shadow)

INK = "#2B2622"
LINE = "#3B3430"
TAUPE = "#8A7B6E"
GREY = "#B4ABA2"
OLIVE = "#5F6A45"
LEDC = "#D9A441"
POCHE = "#3A332E"


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def fmt(v):
    r = round(v, 1)
    return str(int(round(r))) if abs(r - round(r)) < 0.05 else f"{r:.1f}".replace(".", ",")


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(h, other="#FFFFFF", t=0.5):
    a, b = hex2rgb(h), hex2rgb(other)
    return "#%02X%02X%02X" % tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3))


class SVG:
    def __init__(self, w, h):
        self.w, self.h, self.o, self.defs = w, h, [], []

    def add(self, s):
        self.o.append(s)

    def rect(self, x, y, w, h, fill="none", stroke=LINE, sw=0.18, dash=None, op=None, rx=0):
        if w < 0:
            x, w = x + w, -w
        if h < 0:
            y, h = y + h, -h
        st = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else 'stroke="none"'
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' fill-opacity="{op}"' if op is not None else ""
        r = f' rx="{rx}"' if rx else ""
        self.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}"{o} {st}{d}{r}/>')

    def line(self, x1, y1, x2, y2, sw=0.15, col=LINE, dash=None, op=None, cap="butt"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' stroke-opacity="{op}"' if op is not None else ""
        self.add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{col}" stroke-width="{sw}"'
                 f' stroke-linecap="{cap}"{d}{o}/>')

    def path(self, d, fill="none", stroke=LINE, sw=0.18, dash=None, op=None, sop=None, extra=""):
        st = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else 'stroke="none"'
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' fill-opacity="{op}"' if op is not None else ""
        so = f' stroke-opacity="{sop}"' if sop is not None else ""
        self.add(f'<path d="{d}" fill="{fill}"{o} {st}{ds}{so} {extra}/>')

    def circle(self, cx, cy, r, fill="none", stroke=LINE, sw=0.15, dash=None, op=None):
        st = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else 'stroke="none"'
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' fill-opacity="{op}"' if op is not None else ""
        self.add(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}"{o} {st}{d}/>')

    def text(self, x, y, t, size=1.8, col=INK, anchor="middle", weight=400, italic=False, rot=0, ls=0, fam="Jost"):
        tr = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot else ""
        it = ' font-style="italic"' if italic else ""
        l = f' letter-spacing="{ls}"' if ls else ""
        self.add(f'<text x="{x:.2f}" y="{y:.2f}" font-family="{fam}" font-size="{size}" fill="{col}" text-anchor="{anchor}"'
                 f' font-weight="{weight}"{it}{l}{tr}>{esc(t)}</text>')

    def svg(self):
        defs = f"<defs>{''.join(self.defs)}</defs>" if self.defs else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w:.2f}mm" height="{self.h:.2f}mm" '
                f'viewBox="0 0 {self.w:.2f} {self.h:.2f}" style="overflow:visible">{defs}{"".join(self.o)}</svg>')


# ------------------------------------------------------------------------ colours & patterns
def color_of(proj, key):
    if key.startswith("#"):
        return key
    return TEINTES[proj["img"][:2]][key]


def fill_of(s, proj, mat, light=0.55):
    ck, pat = proj["mats"].get(mat, ("#FFFFFF", "flat"))
    base = mix(color_of(proj, ck), "#FFFFFF", light)
    if pat == "flat":
        return base
    pid = f"p-{proj['key']}-{mat}-{int(light * 100)}"
    if pid not in "".join(s.defs):
        dark = mix(base, "#5A4A3E", 0.22)
        if pat == "flutes":
            body = f'<rect width="1.1" height="4" fill="{base}"/><path d="M0.55,0 V4" stroke="{dark}" stroke-width="0.12"/>'
            s.defs.append(f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="1.1" height="4">{body}</pattern>')
        elif pat == "wood":
            body = (f'<rect width="1.8" height="9" fill="{base}"/><path d="M0.4,0 V9 M1.3,0 V4 M1.3,5 V9" stroke="{dark}" '
                    f'stroke-width="0.06"/>')
            s.defs.append(f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="1.8" height="9">{body}</pattern>')
        elif pat == "velvet":
            body = f'<rect width="2.4" height="2.4" fill="{base}"/><path d="M0,1.2 H2.4" stroke="{mix(base, "#FFFFFF", 0.35)}" stroke-width="0.07"/>'
            s.defs.append(f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="2.4" height="2.4" '
                          f'patternTransform="rotate(45)">{body}</pattern>')
        elif pat == "sheer":
            body = f'<rect width="1.4" height="4" fill="{base}" fill-opacity="0.55"/><path d="M0.7,0 V4" stroke="{dark}" stroke-width="0.07" stroke-opacity="0.6"/>'
            s.defs.append(f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="1.4" height="4">{body}</pattern>')
        else:
            return base
    return f"url(#{pid})"


def glow_path(s, d, sw=0.3):
    s.path(d, stroke=LEDC, sw=sw * 4, sop=0.18, fill="none")
    s.path(d, stroke=LEDC, sw=sw, fill="none", dash="0.6 0.35")


def arch_d(x0, x1, ytop, ybot):
    """SVG path (paper coordinates, y down) for a rectangle with a semicircular top."""
    r = (x1 - x0) / 2
    yc = ytop + r
    if yc > ybot:
        yc = ybot
    return (f"M{x0:.2f},{ybot:.2f} V{yc:.2f} A{r:.2f},{r:.2f} 0 0 1 {x1:.2f},{yc:.2f} V{ybot:.2f} Z")


UNIT_CLOUD = [(0.20, 0.20, 0.20), (0.42, 0.33, 0.27), (0.68, 0.30, 0.22), (0.85, 0.18, 0.15)]


def cloud_shapes(x0, x1, ybot, ytop):
    """Circles (as ellipses) + base rectangle approximating a cloud, in paper coordinates."""
    w, h = x1 - x0, ybot - ytop
    sx, sy = w, h / 0.6
    shapes = [f'<ellipse cx="{x0 + cx * sx:.2f}" cy="{ybot - cy * sy:.2f}" rx="{r * sx:.2f}" ry="{r * sy:.2f}"/>'
              for cx, cy, r in UNIT_CLOUD]
    shapes.append(f'<rect x="{x0 + 0.2 * sx:.2f}" y="{ybot - 0.2 * sy:.2f}" width="{0.65 * sx:.2f}" height="{0.2 * sy:.2f}"/>')
    return "".join(shapes)


def draw_cloud(s, x0, x1, ybot, ytop, fill="#FFFFFF", led=False, ghost=False):
    sh = cloud_shapes(x0, x1, ybot, ytop)
    if led:
        s.add(f'<g fill="none" stroke="{LEDC}" stroke-width="1.6" stroke-opacity="0.22">{sh}</g>')
    s.add(f'<g fill="none" stroke="{GREY if ghost else LINE}" stroke-width="0.4">{sh}</g>')
    s.add(f'<g fill="{fill}" stroke="none">{sh}</g>')


def bubble(s, x, y, label, r=2.2, col=OLIVE, size=1.5):
    s.circle(x, y, r, "#FFFFFF", col, 0.2)
    s.text(x, y + size * 0.36, label, size, col, weight=500)


# ------------------------------------------------------------------------ dimensions
def dim_h(s, x0, x1, y, txt, ext_y=None, size=1.7, col=INK):
    s.line(x0 - 0.9, y, x1 + 0.9, y, 0.1, TAUPE)
    for x in (x0, x1):
        if ext_y is not None:
            s.line(x, ext_y + (0.6 if ext_y < y else -0.6), x, y + (0.9 if ext_y < y else -0.9), 0.08, TAUPE)
        s.line(x - 0.7, y + 0.7, x + 0.7, y - 0.7, 0.22, INK)
    w = x1 - x0
    if len(txt) * size * 0.5 < w - 0.4:
        s.text((x0 + x1) / 2, y - 0.6, txt, size, col)
    else:
        s.text((x0 + x1) / 2, y + size + 0.5, txt, size * 0.9, col)


def dim_v(s, y0, y1, x, txt, ext_x=None, size=1.7, col=INK):
    a, b = min(y0, y1), max(y0, y1)
    s.line(x, a - 0.9, x, b + 0.9, 0.1, TAUPE)
    for y in (y0, y1):
        if ext_x is not None:
            s.line(ext_x + (0.6 if ext_x < x else -0.6), y, x + (0.9 if ext_x < x else -0.9), y, 0.08, TAUPE)
        s.line(x - 0.7, y + 0.7, x + 0.7, y - 0.7, 0.22, INK)
    if len(txt) * size * 0.5 < b - a - 0.4:
        s.text(x - 0.6, (a + b) / 2, txt, size, col, rot=-90)
    else:
        s.text(x + size + 0.4, (a + b) / 2, txt, size * 0.9, col, rot=-90)


# ======================================================================== ELEVATIONS
def elevation(proj, wall, scale=25, crop=None, dims=True, labels=True, margins=(14, 12, 10, 8)):
    E = proj["walls"][wall]
    H = proj["room"]["H"]
    W = E["W"]
    cx0, cx1, cz0, cz1 = crop if crop else (0, W, 0, H)
    m = 10 / scale
    ml, mr, mt, mb = margins
    chains = E["dims"] if dims else []
    if crop:
        def inside(pts):
            return [(a, b) for a, b in zip(pts, pts[1:]) if a >= cx0 - 0.2 and b <= cx1 + 0.2]
        hch = [c for c in chains if c[0] in ("h", "t") and inside(c[1])]
        vch = [c for c in chains if c[0] == "v" and cx0 - 0.2 <= c[2] <= cx1 + 0.2]
        nb, nt, nv = len(hch), 0, len(vch)
    else:
        nb = max([c[2] for c in chains if c[0] == "h"] + [0])
        nt = max([c[2] for c in chains if c[0] == "t"] + [0])
        nv = len([c for c in chains if c[0] == "v" and c[2] >= W - 0.1])
    mb += nb * 5.6
    mt += nt * 5.6
    mr += nv * 5.6 if not crop else nv * 5.6
    w = (cx1 - cx0) * m + ml + mr
    h = (cz1 - cz0) * m + mt + mb
    s = SVG(w, h)
    X = lambda x: ml + (x - cx0) * m
    Z = lambda z: mt + (cz1 - z) * m
    cid = f"c-{proj['key']}-{wall}-{int(cx0)}-{int(cx1)}-{int(cz0)}"
    s.defs.append(f'<clipPath id="{cid}"><rect x="{X(cx0):.2f}" y="{Z(cz1):.2f}" width="{(cx1 - cx0) * m:.2f}" '
                  f'height="{(cz1 - cz0) * m:.2f}"/></clipPath>')
    s.add(f'<g clip-path="url(#{cid})">')
    s.rect(X(0), Z(H), W * m, H * m, "#FBF9F6", None)
    for el in E["els"]:
        draw_el(s, proj, el, X, Z, m, H, labels)
    s.add("</g>")
    if crop:
        s.rect(X(cx0), Z(cz1), (cx1 - cx0) * m, (cz1 - cz0) * m, "none", GREY, 0.1, dash="0.8 0.6")
    else:
        s.rect(X(0), Z(H), W * m, H * m, "none", LINE, 0.4)
        s.rect(X(0) - 1.8, Z(0), W * m + 3.6, 1.3, "#FFFFFF", LINE, 0.15)
        for k in range(int((W * m + 3.6) / 1.2)):
            xx = X(0) - 1.8 + k * 1.2
            s.line(xx, Z(0) + 1.3, xx + 1.2, Z(0), 0.06, GREY)
        for xx in (X(0) - 1.8, X(W)):
            s.rect(xx, Z(H) - 2.5, 1.8, H * m + 2.5, POCHE, None)
        s.line(X(0), Z(H), X(W), Z(H), 0.45, LINE)
        s.text(X(0) - 3.2, Z(0) + 0.6, "±0", 1.6, TAUPE, anchor="end")
        s.text(X(0) - 3.2, Z(H) + 0.6, f"+{fmt(H)}", 1.6, TAUPE, anchor="end")
    if dims:
        lvl = 0
        for c in chains:
            kind, pts = c[0], c[1]
            if kind in ("h", "t"):
                segs = list(zip(pts, pts[1:]))
                if crop:
                    segs = [(a, b) for a, b in segs if a >= cx0 - 0.2 and b <= cx1 + 0.2]
                    if not segs:
                        continue
                    lvl += 1
                    y = Z(cz0) + 1.5 + lvl * 5.4
                    ext = Z(cz0)
                elif kind == "h":
                    y = Z(0) + 1.5 + c[2] * 5.4
                    ext = Z(0) + 1.3
                else:
                    y = Z(H) - 2.6 - c[2] * 5.4
                    ext = Z(H) - 2.5
                for a, b in segs:
                    dim_h(s, X(a), X(b), y, fmt(b - a), ext_y=ext)
        vl = 0
        for c in chains:
            if c[0] != "v":
                continue
            pts, xref = c[1], c[2]
            if crop and not (cx0 - 0.2 <= xref <= cx1 + 0.2):
                continue
            if crop:
                vl += 1
                xx = X(cx1) + 3.0 + (vl - 1) * 5.4
            elif xref >= W - 0.1:
                vl += 1
                xx = X(W) + 3.5 + (vl - 1) * 5.4
            else:
                xx = X(xref) + 2.6
            for a, b in zip(pts, pts[1:]):
                if crop and not (a >= cz0 - 0.2 and b <= cz1 + 0.2):
                    continue
                dim_v(s, Z(a), Z(b), xx, fmt(b - a), ext_x=X(min(xref, cx1)))
    return s.svg(), w, h


def draw_el(s, proj, el, X, Z, m, H, labels=True, ghost=False):
    t = el[0]
    stroke = GREY if ghost else LINE
    if t == "rect":
        _, x0, x1, z0, z1, mat, o = el
        if z1 - z0 > 0.6:
            s.rect(X(x0), Z(z1), (x1 - x0) * m, (z1 - z0) * m, fill_of(s, proj, mat), stroke, 0.16)
        for xx in o.get("lines", []):
            s.line(X(xx), Z(z1), X(xx), Z(z0), 0.12, stroke)
        for zz in o.get("hsplits", []):
            s.line(X(x0), Z(zz), X(x1), Z(zz), 0.12, stroke)
        for (kx, kz, kr, km) in o.get("knobs", []):
            s.circle(X(kx), Z(kz), kr * m, fill_of(s, proj, km, 0.2) if km in proj["mats"] else "#C9A27A", stroke, 0.12)
        for (gx, gz0, gz1) in o.get("grips", []):
            if gz1 - gz0 < 1:
                s.line(X(gx) - 2.2, Z(gz0), X(gx) + 2.2, Z(gz0), 0.35, TAUPE, cap="round")
            else:
                s.line(X(gx), Z(gz0), X(gx), Z(gz1), 0.35, TAUPE, cap="round")
        if labels and o.get("label"):
            bubble(s, (X(x0) + X(x1)) / 2, Z(z1) + 3.2 if (z1 - z0) * m > 8 else Z(z1) - 3.2, o["label"])
    elif t == "arch":
        _, x0, x1, z0, ztop, mat, o = el
        d = arch_d(X(x0), X(x1), Z(ztop), Z(z0))
        s.path(d, fill_of(s, proj, mat), stroke, 0.2)
        if o.get("led"):
            inset = 0.7
            glow_path(s, arch_d(X(x0) + inset, X(x1) - inset, Z(ztop) + inset, Z(z0)))
        if labels and o.get("label"):
            bubble(s, (X(x0) + X(x1)) / 2, Z(ztop) + 4.2, o["label"])
    elif t == "scallops":
        _, x0, x1, z0, tops, mat = el
        n = len(tops)
        wd = (x1 - x0) / n
        for i, zt in enumerate(tops):
            a = x0 + i * wd
            s.path(arch_d(X(a), X(a + wd), Z(zt), Z(z0)), fill_of(s, proj, mat), stroke, 0.2)
    elif t == "cloud":
        _, x0, x1, z0, z1, mat, led = el
        draw_cloud(s, X(x0), X(x1), Z(z0), Z(z1), fill_of(s, proj, mat, 0.3), led, ghost)
    elif t == "crib":
        _, x0, x1, z0, z1, zm = el
        s.rect(X(x0), Z(15), 3.5 * m, 15 * m, "#FFFFFF", stroke, 0.15)
        s.rect(X(x1 - 3.5), Z(15), 3.5 * m, 15 * m, "#FFFFFF", stroke, 0.15)
        s.rect(X(x0), Z(z1), (x1 - x0) * m, (z1 - 15) * m, "#FFFFFF", stroke, 0.2, rx=0.8)
        s.rect(X(x0 + 4), Z(zm), (x1 - x0 - 8) * m, (zm - 30) * m, "#F3EFE9", stroke, 0.1)
        xx = x0 + 9
        while xx < x1 - 8:
            s.line(X(xx), Z(z1 - 5), X(xx), Z(zm), 0.1, stroke)
            xx += 8.5
        s.line(X(x0 + 3.5), Z(z1 - 5), X(x1 - 3.5), Z(z1 - 5), 0.12, stroke)
    elif t == "canopy":
        _, cx, zc, x0, x1 = el
        s.line(X(cx), Z(zc + 12), X(cx), Z(H), 0.12, stroke)
        d = (f"M{X(cx - 26):.2f},{Z(zc):.2f} Q{X(cx - 40):.2f},{Z(zc * 0.5):.2f} {X(x0):.2f},{Z(0):.2f} "
             f"L{X(x1):.2f},{Z(0):.2f} Q{X(cx + 40):.2f},{Z(zc * 0.5):.2f} {X(cx + 26):.2f},{Z(zc):.2f} Z")
        s.path(d, "#FFFFFF", stroke, 0.12, dash="0.8 0.5", op=0.35)
        s.rect(X(cx - 28), Z(zc + 12), 56 * m, 12 * m, "#FFFFFF", stroke, 0.15, rx=1.2)
        for k in range(5):
            s.circle(X(cx - 22 + k * 11), Z(zc + 1), 4.5 * m, "#FFFFFF", stroke, 0.1)
    elif t == "window":
        _, x0, x1, z0, z1 = el
        s.rect(X(x0), Z(z1), (x1 - x0) * m, (z1 - z0) * m, "#EEF3F4", stroke, 0.3)
        s.line(X((x0 + x1) / 2), Z(z1), X((x0 + x1) / 2), Z(z0), 0.15, stroke)
        for k in range(1, 4):
            xx = X(x0) + (x1 - x0) * m * k / 4
            s.line(xx - 2, Z(z1) + 3, xx + 4, Z(z1) + 9, 0.06, GREY)
    elif t == "curtain":
        _, x0, x1, z0, z1, mat = el
        s.rect(X(x0), Z(z1), (x1 - x0) * m, (z1 - z0) * m, fill_of(s, proj, mat, 0.45), stroke, 0.1)
        s.line(X(x0) - 1, Z(z1), X(x1) + 1, Z(z1), 0.3, stroke)
    elif t == "motif":
        _, x0, x1, z0, z1, label = el
        s.rect(X(x0), Z(z1), (x1 - x0) * m, (z1 - z0) * m, fill_of(s, proj, "fond", 0.75), TAUPE, 0.12, dash="1 0.7")
        if labels:
            leaf(s, X(x0) + 8, Z(z1) + 10, 7, stroke)
            leaf(s, X(x1) - 10, Z(z0 + 80), 8, stroke)
            leaf(s, X(x0) + 14, Z(z0 + 70), 6, stroke)
            s.text((X(x0) + X(x1)) / 2, Z(z1) + 6, label, 1.55, TAUPE, italic=True)
    elif t == "bear":
        _, cx, cz, r, mat = el
        f = fill_of(s, proj, mat, 0.25)
        for ex in (-0.72, 0.72):
            s.circle(X(cx + ex * r), Z(cz + 0.72 * r), 0.36 * r * m, f, stroke, 0.18)
        s.circle(X(cx), Z(cz), r * m, f, stroke, 0.22)
        s.add(f'<ellipse cx="{X(cx):.2f}" cy="{Z(cz - 0.3 * r):.2f}" rx="{0.36 * r * m:.2f}" ry="{0.26 * r * m:.2f}" '
              f'fill="#F6EEE6" stroke="{stroke}" stroke-width="0.12"/>')
        for ex in (-0.32, 0.32):
            s.circle(X(cx + ex * r), Z(cz + 0.12 * r), 0.07 * r * m, INK, None)
        s.circle(X(cx), Z(cz - 0.2 * r), 0.08 * r * m, INK, None)
        s.circle(X(cx), Z(cz), r * m + 0.6, "none", LEDC, 0.25)
    elif t == "bunny":
        _, cx, cz, wd = el
        for ex in (-0.16, 0.16):
            s.add(f'<ellipse cx="{X(cx + ex * wd):.2f}" cy="{Z(cz + 0.45 * wd):.2f}" rx="{0.1 * wd * m:.2f}" '
                  f'ry="{0.3 * wd * m:.2f}" fill="#FFFFFF" stroke="{stroke}" stroke-width="0.15"/>')
        draw_cloud(s, X(cx - wd / 2), X(cx + wd / 2), Z(cz - 0.15 * wd), Z(cz + 0.25 * wd), "#FFFFFF", True)
    elif t == "shelf":
        _, x0, x1, z, led = el
        s.rect(X(x0), Z(z), (x1 - x0) * m, 3 * m, "#FFFFFF", stroke, 0.15)
        if led:
            s.line(X(x0) + 0.5, Z(z - 3) + 0.4, X(x1) - 0.5, Z(z - 3) + 0.4, 0.9, LEDC, op=0.22)
            s.line(X(x0) + 0.5, Z(z - 3) + 0.35, X(x1) - 0.5, Z(z - 3) + 0.35, 0.22, LEDC, dash="0.6 0.35")
    elif t == "ledh":
        _, x0, x1, z = el
        s.line(X(x0), Z(z), X(x1), Z(z), 0.9, LEDC, op=0.22)
        s.line(X(x0), Z(z), X(x1), Z(z), 0.25, LEDC, dash="0.6 0.35")
    elif t == "ledv":
        _, x, z0, z1 = el
        s.line(X(x), Z(z0), X(x), Z(z1), 0.9, LEDC, op=0.22)
        s.line(X(x), Z(z0), X(x), Z(z1), 0.25, LEDC, dash="0.6 0.35")
    elif t == "sconce":
        _, cx, cz = el
        s.rect(X(cx) - 0.5, Z(cz + 22), 1.0, 26 * m, "#C9A27A", stroke, 0.1)
        for zz in (cz, cz + 18):
            s.circle(X(cx), Z(zz), 6 * m + 1.0, LEDC, None, op=0.18)
            s.circle(X(cx), Z(zz), 6 * m, "#FFF8E8", stroke, 0.15)
    elif t == "cloudlamp":
        _, x0, x1, z0, z1 = el
        s.line(X((x0 + x1) / 2), Z(z1), X((x0 + x1) / 2), Z(H), 0.1, stroke)
        draw_cloud(s, X(x0), X(x1), Z(z0), Z(z1), "#FFFFFF", True, ghost)
    elif t == "dome":
        _, cx, zb, r = el
        s.line(X(cx), Z(zb + 0.75 * r), X(cx), Z(H), 0.1, stroke)
        d = (f"M{X(cx - r):.2f},{Z(zb):.2f} Q{X(cx - r):.2f},{Z(zb + 0.75 * r):.2f} {X(cx):.2f},{Z(zb + 0.75 * r):.2f} "
             f"Q{X(cx + r):.2f},{Z(zb + 0.75 * r):.2f} {X(cx + r):.2f},{Z(zb):.2f} Z")
        s.path(d, "#F7F2EA", stroke, 0.18)
        s.line(X(cx - r) + 0.5, Z(zb) + 0.4, X(cx + r) - 0.5, Z(zb) + 0.4, 0.9, LEDC, op=0.25)
    elif t == "mattress":
        _, x0, x1, z0, z1 = el
        s.rect(X(x0), Z(z1), (x1 - x0) * m, (z1 - z0) * m, "#FFFFFF", stroke, 0.12, rx=0.6)
    elif t == "spot":
        _, x = el
        s.path(f"M{X(x) - 1.1:.2f},{Z(H):.2f} L{X(x):.2f},{Z(H) + 1.3:.2f} L{X(x) + 1.1:.2f},{Z(H):.2f}", "#FFFFFF", stroke, 0.12)


def leaf(s, x, y, size, col):
    s.path(f"M{x:.2f},{y + size:.2f} Q{x - size * 0.6:.2f},{y:.2f} {x:.2f},{y - size:.2f} "
           f"Q{x + size * 0.6:.2f},{y:.2f} {x:.2f},{y + size:.2f} Z", "none", TAUPE, 0.12, dash="0.6 0.4")
    s.line(x, y + size, x, y - size * 0.8, 0.08, TAUPE)


# ======================================================================== PLAN
def plan(proj, scale=25, labels=True):
    R = proj["room"]
    W, Dd = R["W"], R["D"]
    P = proj["plan"]
    m = 10 / scale
    t = 15
    pad = (24, 22, 20, 22)   # left, right, top, bottom (mm)
    w = (W + 2 * t) * m + pad[0] + pad[1]
    h = (Dd + 2 * t) * m + pad[2] + pad[3]
    s = SVG(w, h)
    X = lambda x: pad[0] + (x + t) * m
    Y = lambda y: pad[2] + (Dd + t - y) * m
    s.rect(X(-t), Y(Dd + t), (W + 2 * t) * m, (Dd + 2 * t) * m, POCHE, None)
    s.rect(X(0), Y(Dd), W * m, Dd * m, "#FBF9F6", None)
    # openings
    for side, a, b in P["windows"]:
        _opening(s, side, a, b, X, Y, W, Dd, t, m, "window")
    for side, a, b, hinge in P["doors"]:
        _opening(s, side, a, b, X, Y, W, Dd, t, m, "door", hinge)
    # items
    for it in P["items"]:
        kind = it[0]
        if kind == "rect":
            (x0, y0, x1, y1), k, lab = it[1], it[2], it[3]
            if k == "built":
                s.rect(X(x0), Y(y1), (x1 - x0) * m, (y1 - y0) * m, "#E6E8DE", OLIVE, 0.22)
                if lab.startswith("M"):
                    bubble(s, (X(x0) + X(x1)) / 2, (Y(y0) + Y(y1)) / 2, lab, 2.0, size=1.4)
            elif k == "dash":
                s.rect(X(x0), Y(y1), (x1 - x0) * m, (y1 - y0) * m, "none", TAUPE, 0.12, dash="0.8 0.5")
            else:
                s.rect(X(x0), Y(y1), (x1 - x0) * m, (y1 - y0) * m, "#F4EFE8", TAUPE, 0.16, rx=0.6)
                if lab:
                    s.text((X(x0) + X(x1)) / 2, (Y(y0) + Y(y1)) / 2 + 0.5, lab, 1.45, TAUPE)
        else:
            (cx, cy), r, k, lab = it[1], it[2], it[3], it[4]
            if k == "rug":
                s.circle(X(cx), Y(cy), r * m, "none", TAUPE, 0.14, dash="1 0.6")
            elif k == "ceil":
                s.circle(X(cx), Y(cy) , r * m - 1.2, "none", LEDC, 0.3, dash="2 0.6 0.4 0.6")
            else:
                s.circle(X(cx), Y(cy), r * m, "#F4EFE8", TAUPE, 0.16)
    for x, y, txt in P.get("labels", []):
        s.text(X(x), Y(y) + 0.5, txt, 1.45, TAUPE, italic=True)
    # wall markers (elevations) and section line
    for wall in proj["walls"]:
        _wall_marker(s, wall, X, Y, W, Dd, m)
    sec = proj["section"]
    xs = sec["cut_x"]
    look_west = "ouest" in sec["title"]
    s.line(X(xs), Y(-t - 12), X(xs), Y(Dd + t + 12), 0.2, INK, dash="3 1 0.6 1")
    for yy in (Y(-t - 12), Y(Dd + t + 12)):
        dx = -1 if look_west else 1
        s.path(f"M{X(xs):.2f},{yy - 1.6:.2f} l{dx * 3.2:.2f},1.6 l{-dx * 3.2:.2f},1.6 Z", INK, None)
        s.text(X(xs) + dx * 5.2, yy + 0.7, "A", 2.0, INK, weight=500)
    # dims
    for d in P["dims"]:
        kind, pts, ref, off = d
        if kind == "x":
            y_ext = Y(ref) + (-t * m if ref >= Dd - 0.1 else (t * m if ref <= 0.1 else 0))
            y = y_ext - off
            for a, b in zip(pts, pts[1:]):
                dim_h(s, X(a), X(b), y, fmt(b - a), ext_y=y_ext)
        else:
            x_ext = X(ref) + (t * m if ref >= W - 0.1 else (-t * m if ref <= 0.1 else 0))
            x = x_ext + off
            for a, b in zip(pts, pts[1:]):
                dim_v(s, Y(a), Y(b), x, fmt(b - a), ext_x=x_ext)
    return s.svg(), w, h


def _opening(s, side, a, b, X, Y, W, Dd, t, m, kind, hinge=None):
    if side in ("N", "S"):
        y_in = Y(Dd) if side == "N" else Y(0)
        y_out = Y(Dd + t) if side == "N" else Y(-t)
        s.rect(X(a), min(y_in, y_out), (b - a) * m, t * m, "#FFFFFF", None)
        s.line(X(a), y_in, X(a), y_out, 0.25, LINE)
        s.line(X(b), y_in, X(b), y_out, 0.25, LINE)
        if kind == "window":
            for f in (0.0, 0.5, 1.0):
                yy = y_in + (y_out - y_in) * f
                s.line(X(a), yy, X(b), yy, 0.12 if f != 0.5 else 0.2, LINE)
        else:
            sgn = 1 if side == "S" else -1
            hx = X(a) if hinge == "left" else X(b)
            ox = X(b) if hinge == "left" else X(a)
            L = (b - a) * m
            s.line(hx, y_in, hx, y_in - sgn * L, 0.25, LINE)
            sweep = 1 if (hinge == "left") == (side == "S") else 0
            s.path(f"M{hx:.2f},{y_in - sgn * L:.2f} A{L:.2f},{L:.2f} 0 0 {sweep} {ox:.2f},{y_in:.2f}", "none", TAUPE, 0.1,
                   dash="0.8 0.5")
    else:
        x_in = X(0) if side == "W" else X(W)
        x_out = X(-t) if side == "W" else X(W + t)
        s.rect(min(x_in, x_out), Y(b), t * m, (b - a) * m, "#FFFFFF", None)
        s.line(x_in, Y(a), x_out, Y(a), 0.25, LINE)
        s.line(x_in, Y(b), x_out, Y(b), 0.25, LINE)
        for f in (0.0, 0.5, 1.0):
            xx = x_in + (x_out - x_in) * f
            s.line(xx, Y(a), xx, Y(b), 0.12 if f != 0.5 else 0.2, LINE)


def _wall_marker(s, wall, X, Y, W, Dd, m):
    pos = {"A": (W / 2, Dd - 28, 0), "B": (W - 28, Dd / 2, 90), "C": (W / 2, 28, 180), "D": (28, Dd / 2, 270)}[wall]
    x, y = X(pos[0]), Y(pos[1])
    a = math.radians(pos[2])
    dx, dy = math.sin(a), -math.cos(a)
    tip = (x + dx * 4.0, y + dy * 4.0)
    l = (x + dx * 2.0 - dy * 1.8, y + dy * 2.0 + dx * 1.8)
    r = (x + dx * 2.0 + dy * 1.8, y + dy * 2.0 - dx * 1.8)
    s.path(f"M{tip[0]:.2f},{tip[1]:.2f} L{l[0]:.2f},{l[1]:.2f} L{r[0]:.2f},{r[1]:.2f} Z", INK, None)
    s.circle(x, y, 2.3, "#FFFFFF", INK, 0.2)
    s.text(x, y + 0.75, wall, 2.0, INK, weight=500)


# ======================================================================== SECTION
def section(proj, scale=25, crop=None):
    S = proj["section"]
    D_, H = S["D"], S["H"]
    m = 10 / scale
    t, slab = 15, 20
    ml, mr, mt, mb = 26, 14, 14, 20
    if crop:
        c0, c1, cz0, cz1 = crop
        ml, mr, mt, mb = 6, 14, 6, 14
        w = (c1 - c0) * m + ml + mr
        h = (cz1 - cz0) * m + mt + mb
        X = lambda x: ml + (x - c0) * m
        Z = lambda z: mt + (cz1 - z) * m
    else:
        w = (D_ + 2 * t) * m + ml + mr
        h = (H + 2 * slab) * m + mt + mb
        X = lambda x: ml + (x + t) * m
        Z = lambda z: mt + (H + slab - z) * m
    s = SVG(w, h)
    if crop:
        cid = f"sc-{proj['key']}"
        s.defs.append(f'<clipPath id="{cid}"><rect x="{X(c0):.2f}" y="{Z(cz1):.2f}" width="{(c1 - c0) * m:.2f}" '
                      f'height="{(cz1 - cz0) * m:.2f}"/></clipPath>')
        s.add(f'<g clip-path="url(#{cid})">')
    s.rect(X(0), Z(H), D_ * m, H * m, "#FBF9F6", None)
    ceil = S.get("ceiling")
    for el in S["els"]:
        k = el[0]
        if k == "ghost":
            _, a, b, z0, z1, lab = el
            s.rect(X(a), Z(z1), (b - a) * m, (z1 - z0) * m, "none", GREY, 0.14, dash="1 0.6")
            if lab:
                s.text((X(a) + X(b)) / 2, Z(z1) - 1.0, lab, 1.4, GREY, italic=True)
        elif k == "ghostline":
            _, a, b, z = el
            s.line(X(a), Z(z), X(b), Z(z), 0.14, GREY, dash="1 0.6")
        elif k == "ghostwin":
            _, a, b, z0, z1 = el
            s.rect(X(a), Z(z1), (b - a) * m, (z1 - z0) * m, "none", GREY, 0.12)
            s.line(X(a), Z(z1), X(b), Z(z0), 0.08, GREY)
            s.text((X(a) + X(b)) / 2, Z(z1) - 1.0, "baie (au-delà)", 1.4, GREY, italic=True)
    # walls, slabs
    for x0 in (-t, D_):
        s.rect(X(x0), Z(H + slab), t * m, (H + 2 * slab) * m, POCHE, None)
    for z0 in (-slab, H):
        s.rect(X(-t), Z(z0 + slab), (D_ + 2 * t) * m, slab * m, "#FFFFFF", LINE, 0.2)
        for k_ in range(int((D_ + 2 * t) * m / 1.4)):
            xx = X(-t) + k_ * 1.4
            s.line(xx, Z(z0), xx + slab * m, Z(z0 + slab), 0.06, GREY)
    if ceil:
        a, b, zl = ceil
        s.rect(X(0), Z(H), a * m, (H - zl) * m, "#FFFFFF", LINE, 0.25)
        s.rect(X(b), Z(H), (D_ - b) * m, (H - zl) * m, "#FFFFFF", LINE, 0.25)
        for xx in (X(a), X(b)):
            s.circle(xx, Z(zl) - 0.8, 0.7, LEDC, None)
        s.text((X(a) + X(b)) / 2, Z(H) + 3.0, f"Gorge circulaire Ø {fmt(b - a)} — LED", 1.5, TAUPE, italic=True)
    for el in S["els"]:
        k = el[0]
        if k == "recess":
            _, a, b, z0, z1, lab = el
            s.rect(X(-b), Z(z1), (b - a) * m, (z1 - z0) * m, "#FFFFFF", LINE, 0.2)
            s.line(X(-b) + 0.4, Z(z1), X(-b) + 0.4, Z(z0), 0.25, LEDC, dash="0.6 0.35")
            s.text(X(0) + 1.5, Z(z1) + 2.2, lab, 1.4, TAUPE, anchor="start", italic=True)
        elif k == "prof":
            _, a, b, z0, z1, mat, lab = el
            fill = fill_of(s, proj, mat, 0.4) if mat in proj["mats"] else "#F4EFE8"
            s.rect(X(a), Z(z1), (b - a) * m, (z1 - z0) * m, fill, LINE, 0.3)
            if lab:
                if lab.startswith("M"):
                    bubble(s, (X(a) + X(b)) / 2, Z(z1) - 3.0, lab)
                else:
                    s.text((X(a) + X(b)) / 2, Z(z1) - 1.0, lab, 1.45, TAUPE)
        elif k == "mattress":
            _, a, b, z0, z1 = el
            s.rect(X(a), Z(z1), (b - a) * m, (z1 - z0) * m, "#FFFFFF", LINE, 0.18, rx=0.5)
        elif k == "canopy":
            _, sc, zc = el
            s.line(X(sc), Z(zc + 12), X(sc), Z(H), 0.12, LINE)
            s.rect(X(sc - 22), Z(zc + 12), 44 * m, 12 * m, "#FFFFFF", LINE, 0.15, rx=1)
            s.path(f"M{X(sc - 22):.2f},{Z(zc):.2f} Q{X(sc - 30):.2f},{Z(zc * 0.5):.2f} {X(max(sc - 34, 1)):.2f},{Z(0):.2f}",
                   "none", TAUPE, 0.12, dash="0.8 0.5")
            s.path(f"M{X(sc + 22):.2f},{Z(zc):.2f} Q{X(sc + 40):.2f},{Z(zc * 0.5):.2f} {X(sc + 46):.2f},{Z(0):.2f}",
                   "none", TAUPE, 0.12, dash="0.8 0.5")
            s.text(X(sc + 26), Z(zc + 6), "Ciel de lit", 1.4, TAUPE, anchor="start", italic=True)
        elif k == "spotc":
            _, sc = el
            s.path(f"M{X(sc) - 1.1:.2f},{Z(H):.2f} L{X(sc):.2f},{Z(H) + 1.3:.2f} L{X(sc) + 1.1:.2f},{Z(H):.2f}", "#FFFFFF", LINE, 0.12)
        elif k == "led":
            _, sc, z = el
            s.circle(X(sc), Z(z), 0.8, LEDC, None)
        elif k == "cloudlamp":
            _, a, b, z0, z1 = el
            s.line(X((a + b) / 2), Z(z1), X((a + b) / 2), Z(ceil[2] if ceil else H), 0.1, LINE)
            draw_cloud(s, X(a), X(b), Z(z0), Z(z1), "#FFFFFF", True)
        elif k == "dome":
            _, sc, zb, r = el
            s.line(X(sc), Z(zb + 0.75 * r), X(sc), Z(H), 0.1, LINE)
            d = (f"M{X(sc - r):.2f},{Z(zb):.2f} Q{X(sc - r):.2f},{Z(zb + 0.75 * r):.2f} {X(sc):.2f},{Z(zb + 0.75 * r):.2f} "
                 f"Q{X(sc + r):.2f},{Z(zb + 0.75 * r):.2f} {X(sc + r):.2f},{Z(zb):.2f} Z")
            s.path(d, "#F7F2EA", LINE, 0.18)
    if crop:
        s.add("</g>")
        s.rect(X(c0), Z(cz1), (c1 - c0) * m, (cz1 - cz0) * m, "none", GREY, 0.12, dash="0.8 0.6")
        hp = [v for v in S["dims"][0][1] if c0 <= v <= c1]
        for a_, b_ in zip(hp, hp[1:]):
            dim_h(s, X(a_), X(b_), Z(cz0) + 5, fmt(b_ - a_), ext_y=Z(0))
        vp = [v for v in S["dims"][1][1] if cz0 <= v <= cz1]
        for a_, b_ in zip(vp, vp[1:]):
            dim_v(s, Z(a_), Z(b_), X(c1) + 5, fmt(b_ - a_), ext_x=X(c1))
        return s.svg(), w, h
    for c in S["dims"]:
        kind, pts, ref = c
        if kind == "h":
            y = Z(-slab) + 3 + (ref - 1) * 5.4
            for a, b in zip(pts, pts[1:]):
                dim_h(s, X(a), X(b), y, fmt(b - a), ext_y=Z(0))
        else:
            xx = X(-t) - 4.0
            for a, b in zip(pts, pts[1:]):
                dim_v(s, Z(a), Z(b), xx, fmt(b - a), ext_x=X(-t))
    s.text(X(-t / 2), Z(H + slab) - 1.5, "Mur A", 1.6, INK)
    s.text(X(D_ + t / 2), Z(H + slab) - 1.5, "Mur C", 1.6, INK)
    return s.svg(), w, h


# ======================================================================== CUSTOM PIECE (front + side)
def side_profile(P_, H_, levels, plinth, scale):
    m = 10 / scale
    ml, mr, mt, mb = 4, 10, 6, 10
    w = P_ * m + ml + mr
    h = H_ * m + mt + mb
    s = SVG(w, h)
    X = lambda x: ml + x * m
    Z = lambda z: mt + (H_ - z) * m
    s.rect(X(0), Z(H_), P_ * m, H_ * m, "#F4EFE8", LINE, 0.3)
    if plinth:
        s.rect(X(P_ - 8), Z(plinth), 8 * m, plinth * m, "#FFFFFF", LINE, 0.2)
        s.line(X(P_ - 8) + 0.3, Z(plinth / 2), X(P_ - 8) + 0.3, Z(plinth / 2), 0.6, LEDC)
    for z in levels:
        if 0 < z < H_:
            s.line(X(0), Z(z), X(P_), Z(z), 0.12, LINE)
    s.rect(X(0) - 1.2, Z(H_), 1.2, H_ * m, POCHE, None)
    dim_h(s, X(0), X(P_), Z(0) + 4.5, fmt(P_), ext_y=Z(0))
    dim_v(s, Z(0), Z(H_), X(P_) + 4.0, fmt(H_), ext_x=X(P_))
    s.text(X(P_ / 2), Z(H_) - 2.0, "Profil", 1.5, TAUPE, italic=True)
    return s.svg(), w, h


# ======================================================================== MATERIAL TEXTURE TILES
def texture_tile(hexc, pat, size=34, seed=1):
    s = SVG(size, size)
    base = hexc
    light = mix(base, "#FFFFFF", 0.22)
    dark = mix(base, "#2B2015", 0.22)
    gid = f"g{seed}{pat}{base[1:]}"
    s.defs.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{light}"/>'
                  f'<stop offset="1" stop-color="{dark}"/></linearGradient>')
    s.rect(0, 0, size, size, f"url(#{gid})", None)
    rnd = random.Random(seed)
    if pat == "flutes":
        k = 0
        while k * 2.4 < size:
            x = k * 2.4
            s.rect(x, 0, 1.2, size, mix(base, "#FFFFFF", 0.32), None, op=0.55)
            s.line(x + 2.3, 0, x + 2.3, size, 0.18, dark, op=0.5)
            k += 1
    elif pat == "wood":
        for k in range(26):
            y = rnd.uniform(0, size)
            s.path(f"M0,{y:.2f} C{size * 0.3:.2f},{y + rnd.uniform(-1.5, 1.5):.2f} {size * 0.7:.2f},{y + rnd.uniform(-1.5, 1.5):.2f} "
                   f"{size:.2f},{y + rnd.uniform(-1, 1):.2f}", "none", dark, 0.12, sop=0.35)
    elif pat == "velvet":
        rid = f"r{seed}{base[1:]}"
        s.defs.append(f'<radialGradient id="{rid}" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFFFFF" '
                      f'stop-opacity="0.35"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>')
        s.rect(0, 0, size, size, f"url(#{rid})", None)
    elif pat == "sheer":
        for k in range(int(size / 1.6)):
            x = k * 1.6 + rnd.uniform(-0.3, 0.3)
            s.line(x, 0, x + rnd.uniform(-0.6, 0.6), size, 0.35, "#FFFFFF", op=0.35)
    elif pat == "dots":
        for k in range(420):
            s.circle(rnd.uniform(0, size), rnd.uniform(0, size), rnd.uniform(0.25, 0.6),
                     mix(base, "#FFFFFF", rnd.uniform(0.15, 0.45)), None, op=0.8)
    elif pat == "leaf":
        for k in range(7):
            x, y, sz = rnd.uniform(4, size - 4), rnd.uniform(4, size - 4), rnd.uniform(3, 6)
            ang = rnd.uniform(0, 180)
            s.add(f'<g transform="rotate({ang:.0f} {x:.2f} {y:.2f})"><path d="M{x:.2f},{y + sz:.2f} Q{x - sz * 0.6:.2f},{y:.2f} '
                  f'{x:.2f},{y - sz:.2f} Q{x + sz * 0.6:.2f},{y:.2f} {x:.2f},{y + sz:.2f} Z" fill="{mix(base, "#FFFFFF", 0.2)}" '
                  f'stroke="{dark}" stroke-width="0.12"/></g>')
    return s.svg()
