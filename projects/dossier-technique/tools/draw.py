"""SVG drawing primitives for the technical dossier. Paper units: millimetres."""
import html
import math

INK = "#1E1E1E"
GREY = "#8C8C8C"
OLIVE = "#55603C"       # deduced dimensions
BURG = "#8A1F35"        # dimensions to confirm
LED = "#C8962E"
POCHE = "#2B2B2B"

STATUS_COL = {"v": INK, "d": OLIVE, "c": BURG, None: INK}

PATTERNS = """
<svg width="0" height="0" style="position:absolute"><defs>
<pattern id="p-chene" patternUnits="userSpaceOnUse" width="1.4" height="6"><rect width="1.4" height="6" fill="#F1E6D8"/>
 <path d="M0.3,0 V6 M1.0,0 V2.6 M1.0,3.4 V6" stroke="#CDB59A" stroke-width="0.07"/></pattern>
<pattern id="p-lames" patternUnits="userSpaceOnUse" width="1.0" height="4"><rect width="1.0" height="4" fill="#E9D9C5"/>
 <path d="M0.5,0 V4" stroke="#9C7D60" stroke-width="0.1"/></pattern>
<pattern id="p-cannelure" patternUnits="userSpaceOnUse" width="0.9" height="4"><rect width="0.9" height="4" fill="#F4F0EA"/>
 <path d="M0.45,0 V4" stroke="#B3A595" stroke-width="0.08"/></pattern>
<pattern id="p-miroir" patternUnits="userSpaceOnUse" width="3" height="3" patternTransform="rotate(45)"><rect width="3" height="3" fill="#EEF2F3"/>
 <path d="M0,0.6 H3 M0,1.0 H3" stroke="#9FB0B5" stroke-width="0.06"/></pattern>
<pattern id="p-verre" patternUnits="userSpaceOnUse" width="2.4" height="2.4" patternTransform="rotate(45)"><rect width="2.4" height="2.4" fill="#EDF3F5"/>
 <path d="M0,1.2 H2.4" stroke="#A9BBC0" stroke-width="0.06"/></pattern>
<pattern id="p-marbre_clair" patternUnits="userSpaceOnUse" width="9" height="9"><rect width="9" height="9" fill="#F6F3EF"/>
 <path d="M0,7 C2,5 3,6 5,3 S8,1 9,0 M1,9 C3,8 4,7.5 6,8" fill="none" stroke="#D2C4B2" stroke-width="0.08"/></pattern>
<pattern id="p-marbre_fonce" patternUnits="userSpaceOnUse" width="9" height="9"><rect width="9" height="9" fill="#7C7866"/>
 <path d="M0,7 C2,5 3,6 5,3 S8,1 9,0 M1,9 C3,8 4,7.5 6,8" fill="none" stroke="#B9B39C" stroke-width="0.09"/></pattern>
<pattern id="p-tissu" patternUnits="userSpaceOnUse" width="1.2" height="1.2"><rect width="1.2" height="1.2" fill="#EFEAE3"/>
 <circle cx="0.6" cy="0.6" r="0.09" fill="#B9AE9F"/></pattern>
<pattern id="p-hors" patternUnits="userSpaceOnUse" width="2.2" height="2.2" patternTransform="rotate(45)"><rect width="2.2" height="2.2" fill="#FFFFFF"/>
 <path d="M0,1.1 H2.2" stroke="#D2D2D2" stroke-width="0.12"/></pattern>
<pattern id="p-dalle" patternUnits="userSpaceOnUse" width="1.6" height="1.6" patternTransform="rotate(45)"><rect width="1.6" height="1.6" fill="#FFFFFF"/>
 <path d="M0,0.8 H1.6" stroke="#8C8C8C" stroke-width="0.09"/></pattern>
<pattern id="p-escalier" patternUnits="userSpaceOnUse" width="3" height="3" patternTransform="rotate(-45)"><rect width="3" height="3" fill="#FAFAFA"/>
 <path d="M0,1.5 H3" stroke="#E2E2E2" stroke-width="0.1"/></pattern>
</defs></svg>
"""

FILL = {
    "enduit": "#FFFFFF", "panneau": "#FBF9F6", "laque": "#F8F4EE", "niche": "#FFF3DA",
    "chene": "url(#p-chene)", "lames": "url(#p-lames)", "cannelure": "url(#p-cannelure)",
    "miroir": "url(#p-miroir)", "verre": "url(#p-verre)", "marbre_clair": "url(#p-marbre_clair)",
    "marbre_fonce": "url(#p-marbre_fonce)", "tissu": "url(#p-tissu)", "bois_fonce": "#4A3B31",
}


def esc(t):
    return html.escape(str(t), quote=True)


def fmt(v):
    """French number: 378,1 ; integers without decimals."""
    if v is None:
        return "?"
    r = round(v, 1)
    if abs(r - round(r)) < 0.05:
        return str(int(round(r)))
    return f"{r:.1f}".replace(".", ",")


GIVEN = [1122, 472, 315.8, 426.6, 424, 303.6, 130, 322.2, 378.1, 206.8, 69.8, 85.8, 142, 163, 237, 32]


def dim_text(v, status):
    if status == "c" or v is None:
        return "À CONF."
    if status == "d":
        return "≈" + str(int(round(v)))
    best = min(GIVEN, key=lambda g: abs(g - v))
    return fmt(best if abs(best - v) <= 1.5 else v)   # verified: the value written on the source plan


class SVG:
    def __init__(self, w, h):
        self.w, self.h, self.out = w, h, []

    def add(self, s):
        self.out.append(s)

    def line(self, x1, y1, x2, y2, w=0.18, col=INK, dash=None, cap="butt"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{col}" '
                 f'stroke-width="{w}" stroke-linecap="{cap}"{d}/>')

    def rect(self, x, y, w, h, fill="none", stroke=INK, sw=0.18, dash=None, rx=0, op=None):
        if w < 0:
            x, w = x + w, -w
        if h < 0:
            y, h = y + h, -h
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' fill-opacity="{op}"' if op is not None else ""
        r = f' rx="{rx:.2f}"' if rx else ""
        st = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else 'stroke="none"'
        self.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}"{o} {st}{d}{r}/>')

    def path(self, d, fill="none", stroke=INK, sw=0.18, dash=None, extra=""):
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        st = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else 'stroke="none"'
        self.add(f'<path d="{d}" fill="{fill}" {st}{ds} {extra}/>')

    def circle(self, cx, cy, r, fill="none", stroke=INK, sw=0.18, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        st = f'stroke="{stroke}" stroke-width="{sw}"' if stroke else 'stroke="none"'
        self.add(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}" {st}{d}/>')

    def text(self, x, y, t, size=2.0, col=INK, anchor="middle", weight=400, italic=False, rot=0, ls=0, family="Jost"):
        tr = f' transform="rotate({rot:.1f} {x:.2f} {y:.2f})"' if rot else ""
        it = ' font-style="italic"' if italic else ""
        l = f' letter-spacing="{ls}"' if ls else ""
        self.add(f'<text x="{x:.2f}" y="{y:.2f}" font-family="{family}" font-size="{size}" fill="{col}" '
                 f'text-anchor="{anchor}" font-weight="{weight}"{it}{l}{tr}>{esc(t)}</text>')

    def wrap(self, x, y, t, width, size=1.9, col=INK, anchor="middle", italic=False, lh=1.3):
        """Naive word wrap (Jost average advance ≈ 0.5 em)."""
        words, lines, cur = str(t).split(), [], ""
        maxc = max(8, int(width / (size * 0.5)))
        for w_ in words:
            if len(cur) + len(w_) + 1 > maxc and cur:
                lines.append(cur)
                cur = w_
            else:
                cur = (cur + " " + w_).strip()
        if cur:
            lines.append(cur)
        y0 = y - (len(lines) - 1) * size * lh / 2
        for i, l in enumerate(lines):
            self.text(x, y0 + i * size * lh, l, size, col, anchor, italic=italic)
        return len(lines)

    def svg(self, extra_style=""):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w:.2f}mm" height="{self.h:.2f}mm" '
                f'viewBox="0 0 {self.w:.2f} {self.h:.2f}" style="overflow:visible;{extra_style}">' + "".join(self.out) + "</svg>")


# ---------------------------------------------------------------- dimensions
def tick(s, x, y, col, size=0.9):
    s.line(x - size, y + size, x + size, y - size, 0.25, col)


def dim_h(s, x0, x1, y, val, status, ext_y=None, txt=None, above=True, size=1.85):
    """Horizontal dimension between paper x0..x1 at paper y. ext_y: y where extension lines start."""
    col = STATUS_COL[status]
    dash = "0.8 0.5" if status == "c" else None
    s.line(x0 - 1.0, y, x1 + 1.0, y, 0.12, col, dash)
    for x in (x0, x1):
        if ext_y is not None:
            s.line(x, ext_y + (0.8 if ext_y < y else -0.8), x, y + (1.0 if ext_y < y else -1.0), 0.1, col)
        tick(s, x, y, col)
    t = txt if txt is not None else dim_text(val, status)
    w = x1 - x0
    ty = y - 0.7 if above else y + size + 0.4
    if len(t) * size * 0.52 < w - 0.6:
        s.text((x0 + x1) / 2, ty, t, size, col, italic=(status == "d"))
    else:   # too small: put text beside, slightly lifted
        s.text((x0 + x1) / 2, ty - (size + 0.6 if above else -(size + 0.6)), t, size * 0.92, col, italic=(status == "d"))


def dim_v(s, y0, y1, x, val, status, ext_x=None, txt=None, left=True, size=1.85):
    col = STATUS_COL[status]
    dash = "0.8 0.5" if status == "c" else None
    a, b = min(y0, y1), max(y0, y1)
    s.line(x, a - 1.0, x, b + 1.0, 0.12, col, dash)
    for y in (y0, y1):
        if ext_x is not None:
            s.line(ext_x + (0.8 if ext_x < x else -0.8), y, x + (1.0 if ext_x < x else -1.0), y, 0.1, col)
        tick(s, x, y, col)
    t = txt if txt is not None else dim_text(val, status)
    h = b - a
    tx = x - 0.7 if left else x + size + 0.3
    if len(t) * size * 0.52 < h - 0.6:
        s.text(tx, (a + b) / 2, t, size, col, rot=-90, italic=(status == "d"))
    else:
        s.text(tx - (size + 0.4 if left else -(size + 0.4)), (a + b) / 2, t, size * 0.92, col, rot=-90, italic=(status == "d"))


def level_mark(s, x, y, label, status="d", right=True):
    """Level symbol (triangle on a line) + text."""
    col = STATUS_COL[status]
    s.path(f"M{x:.2f},{y:.2f} l-1.1,-1.6 h2.2 z", fill=col, stroke=None)
    s.line(x - 3, y, x + 3, y, 0.15, col)
    s.text(x + (3.6 if right else -3.6), y - 0.6, label, 1.8, col, "start" if right else "end", italic=(status == "d"))


def bubble(s, x, y, label, r=2.1, fill="#FFFFFF", col=INK, size=1.7):
    s.circle(x, y, r, fill, col, 0.18)
    s.text(x, y + size * 0.36, label, size, col, weight=500)
