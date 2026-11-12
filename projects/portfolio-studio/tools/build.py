"""KAÏRA Interior Design — Studio portfolio (A4 landscape, editorial).

HD version: original render files, embedded losslessly (checked pixel by pixel).
Light version (WhatsApp / e-mail): same layout, images re-encoded as JPEG (no crop, no colour change).

Usage: python3 tools/build.py [--previews]
"""
import html
import json
import pathlib
import subprocess
import sys

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parent.parent
sys.path.insert(0, str(REPO / "projects/dossier-technique/tools"))
sys.path.insert(0, str(REPO / "projects/portfolio-enfants/tools"))
import views as TV          # villa technical drawings
from draw import PATTERNS   # hatch patterns used by those drawings
import pdata                # children's rooms
import pviews as KV

BUILD = ROOT / "build"
LIGHT = BUILD / "light"
FONTS = REPO / "projects/dossier-client/build/fonts"
LOGO = REPO / "projects/kaira-logo/logo/svg"
OUT_HD = REPO / "livrables/KAIRA-Portfolio-Studio-HD.pdf"
OUT_LIGHT = REPO / "livrables/KAIRA-Portfolio-Studio-light.pdf"

VILLA = REPO / "projects/dossier-client/sources"
OTHER = REPO / "projects/instagram-lancement/sources/recus"
KIDS = REPO / "projects/portfolio-enfants/sources/recus"

PW, PH, M = 297, 210, 14
INSTAGRAM = "@kaira.interior.design"

V = {  # villa renders (dossier-client/sources)
    "salon02": "01-rdc-salon-principal/rdc-salon-02.png", "salon05": "01-rdc-salon-principal/rdc-salon-05.png",
    "salon08": "01-rdc-salon-principal/rdc-salon-08.png", "salon09": "01-rdc-salon-principal/rdc-salon-09.png",
    "salon01": "01-rdc-salon-principal/rdc-salon-01.png", "salon10": "01-rdc-salon-principal/rdc-salon-10.png",
    "salon06": "01-rdc-salon-principal/rdc-salon-06.png", "salon11": "01-rdc-salon-principal/rdc-salon-11.png",
    "salon07": "01-rdc-salon-principal/rdc-salon-07.png",
    "et02": "04-etage1-sejour/etage1-sejour-02.png", "et08": "04-etage1-sejour/etage1-sejour-08.png",
    "et03": "04-etage1-sejour/etage1-sejour-03.png", "et01": "04-etage1-sejour/etage1-sejour-01.png",
    "pr05": "03-chambre-principale/chambre-principale-05.png", "pr03": "03-chambre-principale/chambre-principale-03.png",
    "pr01": "03-chambre-principale/chambre-principale-01.png", "pr04": "03-chambre-principale/chambre-principale-04.png",
    "am01": "02-chambre-amis/chambre-amis-01.png", "am03": "02-chambre-amis/chambre-amis-03.png",
}
O = {"liv19": "19.jpg", "liv13": "13.jpg", "ent21": "21.jpg", "kit20": "20.jpg", "off14": "14.jpg"}
NEW = ROOT / "sources/recus"
N = {"kitL": "01.jpg", "dinG": "02.jpg", "livG": "03.jpg", "off2": "04.jpg", "bar": "05.jpg", "dinB": "06.jpg",
     "tvOak": "07.jpg", "lounge": "08.jpg", "livW": "09.jpg", "rAudio": "12.jpg", "rAC": "13.jpg", "rHall": "14.jpg",
     "rTV": "15.jpg", "rMidea": "16.jpg", "rIsl": "10.jpg", "rBrands": "11.jpg"}

LIGHT_MODE = False
USED = {}


def src(key):
    if key in V:
        p = VILLA / V[key]
    elif key in O:
        p = OTHER / O[key]
    elif key in N:
        p = NEW / N[key]
    else:
        p = KIDS / key
    USED[key] = p
    if LIGHT_MODE:
        return (LIGHT / (key.replace("/", "_").rsplit(".", 1)[0] + ".jpg")).as_uri()
    return p.as_uri()


def size(key):
    src(key)
    return Image.open(USED[key]).size


PAGES = []


def page(body, cls="white", footer=True, section=None, toc=None):
    PAGES.append(dict(body=body, cls=cls, footer=footer, section=section, toc=toc))


def e(t):
    return html.escape(str(t))


def box(x, y, w, inner, h=None, cls=""):
    hh = f"height:{h:.1f}mm;" if h is not None else ""
    return f'<div class="b {cls}" style="left:{x:.1f}mm;top:{y:.1f}mm;width:{w:.1f}mm;{hh}">{inner}</div>'


def image(key, x, y, w=None, h=None, cls=""):
    """Whole image, never cropped: fits the given width or height keeping its ratio."""
    iw, ih = size(key)
    if w is None:
        w = h * iw / ih
    if h is None:
        h = w * ih / iw
    return (f'<div class="b img {cls}" style="left:{x:.1f}mm;top:{y:.1f}mm;width:{w:.1f}mm;height:{h:.1f}mm">'
            f'<img src="{src(key)}"></div>'), w, h


def crop(key, box_px, x, y, w):
    """Display crop for detail pages (the source file is untouched)."""
    iw, ih = size(key)
    x0, y0, x1, y1 = box_px
    s = w / (x1 - x0)
    h = (y1 - y0) * s
    return (f'<div class="b crop" style="left:{x:.1f}mm;top:{y:.1f}mm;width:{w:.1f}mm;height:{h:.1f}mm">'
            f'<img src="{src(key)}" style="width:{iw * s:.2f}mm;height:{ih * s:.2f}mm;left:{-x0 * s:.2f}mm;top:{-y0 * s:.2f}mm">'
            f'</div>'), h


def crop_fixed(key, box_px, x, y, w, h):
    """Display crop with a fixed frame w x h (mm): the source box is widened to the frame ratio around its centre."""
    iw, ih = size(key)
    x0, y0, x1, y1 = box_px
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    bw, bh = x1 - x0, y1 - y0
    r = w / h
    if bw / bh < r:
        bw = bh * r
    else:
        bh = bw / r
    bw, bh = min(bw, iw), min(bh, ih)
    x0 = min(max(cx - bw / 2, 0), iw - bw)
    y0 = min(max(cy - bh / 2, 0), ih - bh)
    return crop(key, (x0, y0, x0 + bw, y0 + bh), x, y, w)[0]


def svgbox(svg, x, y):
    return f'<div class="b" style="left:{x:.1f}mm;top:{y:.1f}mm">{svg}</div>'


def logo(name):
    return (LOGO / name).read_text()


def kicker(t, x=M, y=M + 2, cls=""):
    return box(x, y, 200, f'<div class="k {cls}">{e(t)}</div>')


# =============================================================================== pages
def cover():
    im, w, h = image("salon05", PW - 193, 0, h=PH)
    body = (im + box(M + 2, 22, 80, f'<div class="cv-logo">{logo("kaira-1-main-logo-chocolate.svg")}</div>')
            + box(M + 2, 96, 84, '<div class="k">Portfolio 2026</div><h1>Interior<br>Architecture<br>&amp; Design</h1>'
                                 '<div class="cv-sub">Residential interiors · Workspaces · Custom furniture</div>')
            + box(M + 2, 182, 84, f'<div class="cv-f"><b>Karen Wehbe</b> — Founder<br>{INSTAGRAM}</div>'))
    page(body, footer=False)


def about():
    im, w, h = image("et08", M, M, h=PH - 2 * M - 8)
    x = M + w + 16
    body = (im + kicker("About the studio", x, M + 2)
            + box(x, 30, PW - x - M, '<h2>A studio for calm,<br>measured interiors</h2>')
            + box(x, 66, PW - x - M,
                  '<p class="lead">KAÏRA Interior Design is an interior architecture studio founded by Karen Wehbe. '
                  'It designs bespoke residential and professional interiors, from the first sketch to the technical '
                  'drawings.</p>'
                  '<p>Each project starts with listening: how a family lives, how a team works, how light enters the '
                  'rooms. From there the studio builds a single, clear idea and carries it through every scale — the plan, '
                  'the wall, the piece of furniture, the joint between two materials.</p>'
                  '<p>The result is a quiet luxury: natural materials, integrated light, furniture drawn for the space, '
                  'and nothing that does not serve the way the place will be lived in.</p>')
            + box(x, 168, PW - x - M, '<div class="sig"><span>Karen Wehbe</span><em>Founder, KAÏRA Interior Design</em></div>'))
    page(body, section="About the studio")


def vision():
    im, w, h = image("pr03", PW - M - 128, M, h=PH - 2 * M - 8)
    body = (im + kicker("Creative vision")
            + box(M, 30, 128, '<blockquote>“Light, matter and measure — an interior is designed from the inside out.”'
                              '</blockquote>')
            + box(M, 82, 132, '<div class="pillars3">'
                  '<div><i>I</i><b>Light</b><span>Daylight first, then integrated lighting: coves, backlit niches and '
                  'panels, never a bare source in sight.</span></div>'
                  '<div><i>II</i><b>Matter</b><span>Oak, marble, travertine, lacquer and textured fabrics, chosen for how '
                  'they age and how they feel to the touch.</span></div>'
                  '<div><i>III</i><b>Measure</b><span>Every wall is composed: proportions, joints and custom furniture '
                  'are drawn together, as one piece of architecture.</span></div></div>'))
    page(body, section="Creative vision")


SERVICES = [
    ("Interior Design", "Concept, atmosphere and complete design of residential and professional interiors."),
    ("Space Planning", "Layouts that organise circulation, storage and uses, room by room."),
    ("2D Plans", "Furniture and layout plans, clear and dimensioned."),
    ("3D Visualization", "Realistic renders to see the project before it is built."),
    ("Custom Furniture", "TV walls, libraries, wardrobes, headboards and dressings drawn for each space."),
    ("Material Selection", "Woods, stones, lacquers, fabrics and finishes, presented as boards and samples."),
    ("Technical Drawings", "Elevations, sections and details for the workshops and the site."),
    ("Project Follow-up", "Coordination with the craftsmen and follow-up through to completion."),
]


def services():
    cells = "".join(f'<div class="svc"><i>{i + 1:02d}</i><b>{e(n)}</b><span>{e(d)}</span></div>'
                    for i, (n, d) in enumerate(SERVICES))
    body = (kicker("Services", cls="light") + box(M, 30, 120, '<h2 class="light">What the studio<br>designs for you</h2>')
            + box(M, 84, PW - 2 * M, f'<div class="svcs">{cells}</div>'))
    page(body, cls="olive", section="Services")


def projects_index():
    cards = [("01", "Villa", "Private residence — ground & first floor", "salon02"),
             ("02", "Selected Interiors", "Living spaces, kitchen, entrance, executive office", "liv19"),
             ("03", "Children's Rooms", "A collection of five residential concepts", "07.png")]
    out, x = "", M
    wcard = (PW - 2 * M - 2 * 8) / 3
    for n, t, s, key in cards:
        iw, ih = size(key)
        hh = 112
        im = (f'<div class="b img fit" style="left:{x:.1f}mm;top:50mm;width:{wcard:.1f}mm;height:{hh}mm">'
              f'<img src="{src(key)}"></div>')
        out += im + box(x, 50 + hh + 5, wcard, f'<div class="pc"><i>{n}</i><b>{e(t)}</b><span>{e(s)}</span></div>')
        x += wcard + 8
    page(kicker("Selected projects") + box(M, 26, 200, '<h2>Selected projects</h2>') + out, section="Selected projects",
         toc=("—", "Selected Projects"))


# ------------------------------------------------------------------------------- villa
VILLA_PALETTE = [("Light oak", "#6A5442"), ("Cream panels", "#978B80"), ("Dark wood", "#251B13"),
                 ("Veined marble", "#97887A"), ("Travertine", "#C2BAB2"), ("Burgundy art", "#5C2924"),
                 ("Khaki linen", "#3A3322")]


def villa():
    # opener
    im, w, h = image("salon02", M, M, h=PH - 2 * M - 8)
    x = M + w + 16
    body = (im + kicker("Project 01", x)
            + box(x, 26, PW - x - M, '<h2 class="xl">Villa</h2><div class="sub">Private residence — ground &amp; first floor</div>')
            + box(x, 70, PW - x - M,
                  '<p class="lead">A family villa conceived as a sequence of warm, quiet rooms, each organised around '
                  'one wall drawn as a piece of furniture.</p>'
                  '<table class="facts"><tr><td>Spaces</td><td>Living &amp; dining room, guest bedroom, first-floor living '
                  'room, master bedroom</td></tr><tr><td>Scope</td><td>Interior design, space planning, custom furniture, '
                  '3D visualization, technical drawings</td></tr><tr><td>Palette</td><td>Light oak, cream, dark wood, '
                  'veined marble, touches of burgundy and khaki</td></tr></table>'))
    page(body, section="Project 01 — Villa", toc=("01", "Villa"))
    # concept
    chips = "".join(f'<div class="chip"><span style="background:{c}"></span><b>{e(n)}</b><em>{c}</em></div>'
                    for n, c in VILLA_PALETTE)
    im1, w1, h1 = image("salon09", PW - M - 112, M, h=122)
    body = (kicker("Project concept") + box(M, 26, 150, '<h2>Warm minimalism,<br>written in oak and light</h2>')
            + box(M, 66, 146,
                  '<div class="nh">Concept</div><p>The villa is designed as a calm envelope: cream panels with shadow '
                  'joints, light oak columns and integrated lighting form a continuous backdrop from room to room. Against '
                  'it, a few strong pieces — a burgundy artwork, a dark marble band, a sculptural pendant — give each space '
                  'its character.</p>'
                  '<div class="nh">Inspirations &amp; intentions</div><p>Contemporary residential architecture with a '
                  'warm, tactile reading: wood that frames, stone that anchors, light that draws the volumes. Each room '
                  'receives one custom-designed wall — TV wall, library, headboard or dressing — so that storage, light '
                  'and decoration become architecture.</p>')
            + im1 + box(M, 168, PW - 2 * M, f'<div class="nh">Palette — sampled from the renders</div><div class="chips">{chips}</div>'))
    page(body, section="Project 01 — Villa")
    # space planning (two pages)
    svg, w, h = TV.plan_rdc_general(100, furniture=True)
    body = (kicker("Space planning") + box(M, 24, 160, '<h3>Ground floor — layout plan</h3>')
            + svgbox(svg, (PW - w) / 2 + 20, 34)
            + box(M, 40, 64, '<p class="small">Living and dining room organised around three custom walls — TV wall, '
                             'library and console — with the guest bedroom off the hall.</p>'
                             '<p class="small">Black dimensions: written on the architect\'s plan. Olive ≈ dimensions: '
                             'measured to scale. Full technical drawings in the KAÏRA technical dossier.</p>'
                             '<div class="scale">Scale 1:100 (A4)</div>'))
    page(body, section="Project 01 — Villa")
    svg, w, h = TV.plan_et_general(100, furniture=True)
    body = (kicker("Space planning") + box(M, 24, 160, '<h3>First floor — layout plan</h3>')
            + svgbox(svg, (PW - w) / 2 + 20, 34)
            + box(M, 40, 64, '<p class="small">First-floor living room and master bedroom with walk-in dressing. '
                             'Dimensions ≈ measured on the 3D model (1 m grid), to be confirmed on site.</p>'
                             '<div class="scale">Scale 1:100 (A4)</div>'))
    page(body, section="Project 01 — Villa")
    # 3D visualizations
    viz = [("Living room", "Graphic artwork wall framed by sheer curtains; modular sofas in cream and dark leather.",
            "salon11", "salon08", "Oak columns with backlit fluted bases and the dark wood entrance door."),
           ("Dining room", "Travertine table, bouclé chairs and a sculptural LED pendant under a lit ceiling cove.",
            "salon09", "salon01", "Asymmetric oak library, veined marble column and floating console."),
           ("First-floor living room", "Sage sofas, a marble coffee table and a burgundy-patterned artwork.",
            "et02", "et03", "Backlit oak library and a cognac leather pouf; sheer curtains filter the light."),
           ("Bedrooms", "Master bedroom: a dark veined marble band, backlit, between oak columns and mirrored panels.",
            "pr05", "am01", "Guest bedroom: upholstered platform bed against vertical oak slats and a slim mirror strip.")]
    for title, cap1, k1, k2, cap2 in viz:
        a, wa, ha = image(k1, M, M, h=PH - 2 * M - 8)
        hb = 112
        b, wb, hb = image(k2, PW - M - hb * size(k2)[0] / size(k2)[1], M, h=hb)
        xb = PW - M - wb
        body = (a + b + kicker("3D visualization", xb, M + hb + 6)
                + box(xb, M + hb + 13, wb, f'<h3>{e(title)}</h3><p class="cap">{e(cap1)}</p><p class="cap">{e(cap2)}</p>'))
        page(body, section="Project 01 — Villa")
    # materials & finishes (zooms allowed)
    mats = [("salon08", (610, 470, 730, 760), "Light oak", "Columns, panels and libraries", "#6A5442"),
            ("pr05", (720, 400, 1000, 760), "Dark veined marble", "Backlit headboard band", "#312A1B"),
            ("salon09", (780, 1360, 1150, 1480), "Travertine", "Dining table", "#C2BAB2"),
            ("salon08", (180, 650, 470, 1000), "Dark wood", "Entrance double door", "#251B13"),
            ("salon09", (1420, 640, 1640, 900), "Burgundy", "Dining-room artwork", "#5C2924"),
            ("et08", (1180, 640, 1500, 880), "Oak & light", "Backlit library, first floor", "#563C27")]
    out = ""
    wcell = (PW - 2 * M - 5 * 7) / 6
    for i, (k, bx, n, use, hexc) in enumerate(mats):
        x = M + i * (wcell + 7)
        ch = wcell * 1.32
        c = crop_fixed(k, bx, x, 52, wcell, ch)
        out += c + box(x, 52 + ch + 4, wcell, f'<div class="mat"><span style="background:{hexc}"></span><b>{e(n)}</b>'
                                              f'<em>{e(use)}</em><i>{hexc}</i></div>')
    body = (kicker("Materials & finishes") + box(M, 26, 200, '<h2>Materials &amp; finishes</h2>') + out
            + box(M, 182, 230, '<p class="small">Close-ups taken from the project renders; tints sampled on the renders. '
                               'Manufacturer references and final finishes are selected with the client on physical samples.</p>'))
    page(body, section="Project 01 — Villa")
    # furniture design
    pieces = [("sejour", "A", (100, 400, 0, 284), "TV wall — living room",
               "Fluted column, mirror strip, rounded backlit oak panels, lit niche column and a 259 cm floating cream unit."),
              ("princ", "A", (0, 377.3, 0, 292), "Headboard wall — master bedroom",
               "Backlit dark marble band, oak columns with fluted bases, mirrored panels and a wall-to-wall upholstered headboard."),
              ("etsejour", "B", (350, 524.4, 0, 289), "Library — first-floor living room",
               "Oak library with integrated lighting under each shelf, closed base, next to the double entrance door.")]
    for sc in (40, 50, 60, 75):
        views = [TV.elev_view(room, wall, scale=sc, crop=cr, show_dims=True, show_levels=False, margins=(4, 4, 4, 4))
                 for room, wall, cr, t, d in pieces]
        if sum(v[1] for v in views) + 2 * 10 <= PW - 2 * M:
            break
    gap = (PW - 2 * M - sum(v[1] for v in views)) / 2
    hmax = max(v[2] for v in views)
    out, x = "", M
    for (room, wall, cr, t, d), (svg, w, h) in zip(pieces, views):
        out += svgbox(svg, x, 44 + (hmax - h)) + box(x, 44 + hmax + 4, w, f'<h4>{e(t)}</h4><p class="cap">{e(d)}</p>')
        x += w + gap
    body = (kicker("Furniture design") + box(M, 26, 200, '<h2>Custom furniture</h2>') + out
            + box(M, 186, 240, f'<p class="small">Elevations at 1:{sc} (A4) from the KAÏRA technical dossier. ≈ dimensions are '
                               'measured on the plans and renders; final dimensions after site survey.</p>'))
    page(body, section="Project 01 — Villa")
    # interior details (zooms)
    det = [("pr05", (600, 380, 1150, 1000), "Backlit marble band between oak columns"),
           ("salon08", (1300, 860, 1560, 1180), "Fluted oak base with integrated LED"),
           ("salon09", (20, 300, 560, 960), "Library composition and objects"),
           ("salon01", (470, 380, 790, 860), "Veined marble column and floating console"),
           ("salon10", (960, 920, 1220, 1120), "Door hardware on dark wood"),
           ("pr05", (330, 980, 1330, 1480), "Upholstered headboard and bench")]
    out = ""
    wt, ht, gx, gy = 84, 62, 8.5, 18
    for i, (k, bx, cap) in enumerate(det):
        col, row = i % 3, i // 3
        x = M + col * (wt + gx)
        y = 38 + row * (ht + gy)
        out += crop_fixed(k, bx, x, y, wt, ht) + box(x, y + ht + 2, wt, f'<p class="cap c">{e(cap)}</p>')
    body = (kicker("Interior details") + box(M, 22, 200, '<h3>Interior details</h3>') + out)
    page(body, section="Project 01 — Villa")


# ------------------------------------------------------------------------------- selected interiors
def interiors():
    im, w, h = image("liv19", M, M, w=190)
    x = M + w + 12
    body = (im + kicker("Project 02", x)
            + box(x, 26, PW - x - M, '<h2 class="xl">Selected<br>Interiors</h2>')
            + box(x, 70, PW - x - M, '<p class="lead">A selection of spaces designed by the studio: living areas, '
                                     'a kitchen, an entrance and an executive office.</p>'
                                     '<p class="cap">Open living space — white and grey modular sofas, oak-clad columns, '
                                     'a dark wall unit and lit ceiling coves, with the dining area beyond.</p>'))
    page(body, section="Project 02 — Selected Interiors", toc=("02", "Selected Interiors"))
    a, wa, ha = image("liv13", M, M + 6, w=(PW - 2 * M - 10) * 0.56)
    b, wb, hb = image("ent21", PW - M - 112 * 1468 / 1600, M + 6, h=112)
    xb = PW - M - wb
    body = (a + b + box(M, M + 6 + ha + 5, wa, '<h4>Living room &amp; staircase</h4><p class="cap">A luminous living '
                                                'area opening onto a sculptural white staircase; arched sideboard, '
                                                'recessed lighting and a graphic artwork.</p>')
            + box(xb, M + 6 + hb + 5, wb, '<h4>Entrance</h4><p class="cap">Walnut wall panelling with black reveals, an '
                                          'arched-front sideboard, a portrait artwork and marble-effect flooring.</p>'))
    page(body, section="Project 02 — Selected Interiors")
    im, w, h = image("kit20", M, M, h=PH - 2 * M - 8)
    x = M + w + 14
    body = (im + kicker("Kitchen", x) + box(x, 26, PW - x - M, '<h3>Kitchen</h3><p>Cream lacquered units rise to the '
            'ceiling around a waterfall island in boldly veined stone. Black appliances and a smoked-glass display cabinet '
            'add contrast; a herringbone floor and layered ceiling coves bring warmth.</p>'))
    page(body, section="Project 02 — Selected Interiors")
    im, w, h = image("off14", PW - M - (PH - 2 * M - 8) * 1468 / 1600, M, h=PH - 2 * M - 8)
    body = (im + kicker("Workspace") + box(M, 26, PW - 2 * M - w - 14, '<h3>Executive office</h3><p>An executive office '
            'facing a panoramic city view: walnut desk and meeting table, backlit green onyx panels framing the shelving, '
            'and a lounge corner in soft leather. Marble-effect flooring and a perimeter light cove keep the space bright '
            'and calm.</p>'))
    page(body, section="Project 02 — Selected Interiors")


# ------------------------------------------------------------------------------- children's rooms
def kids():
    P = {p["key"]: p for p in pdata.PROJECTS}
    im, w, h = image("07.png", 0, 0, w=PW)
    body = (im + box(M, h + 2, 200, '<div class="k">Project 03 — Children\'s rooms</div>'))
    page(body, footer=False, section="Project 03 — Children's Rooms", toc=("03", "Children's Rooms"))
    body = (kicker("Project 03") + box(M, 22, 150, '<h2>Children\'s rooms</h2>')
            + box(M, 50, 112, '<p class="lead">Arches, scallops and clouds: a collection of five residential concepts '
                              'where soft shapes are drawn into the custom furniture itself.</p><p>Each room has its own '
                              'palette — powder pink, olive, caramel — always rooted in cream and light wood, with indirect '
                              'light integrated into niches, arches and headboards.</p>'))
    order = [("lapin", "Douceur Lapin", "Nursery — powder pink"), ("jungle", "Jungle Douce", "Evolving nursery — olive"),
             ("nuages", "Nuages", "Early-childhood room — olive"), ("ourson", "Ourson Caramel", "Early-childhood room — caramel")]
    wcell, hcell = 70, 70 / 1.5
    for i, (k, n, s) in enumerate(order):
        x = 140 + (i % 2) * (wcell + 6)
        y = 30 + (i // 2) * (hcell + 22)
        im, w, h = image(P[k]["img"], x, y, w=wcell)
        body += im + box(x, y + h + 2.5, wcell, f'<div class="pc s"><b>{e(n)}</b><span>{e(s)}</span></div>')
    page(body, section="Project 03 — Children's Rooms")
    p = P["nuageolive"]
    svg, w, h = KV.elevation(p, "A", 25)
    body = (kicker("Design drawings") + box(M, 22, 200, '<h3>From render to drawing</h3>')
            + svgbox(svg, (PW - w) / 2, 38) + box((PW - w) / 2, 38 + h + 3, w,
                                                  '<p class="cap">Nuage Olive — elevation of the decorative wall, 1:25 (A4): '
                                                  'wardrobe, olive storage column, fluted wall with backlit cloud, upholstered '
                                                  'headboard, trundle bed and floating desk. Proposed concept dimensions in cm.</p>'))
    page(body, section="Project 03 — Children's Rooms")


# ------------------------------------------------------------------------------- process & contact
STEPS = [("Listening", "Brief, uses, budget and expectations; visit of the space."),
         ("Site survey", "Measurements and photographs; existing plans collected."),
         ("Concept", "Atmosphere, palette, materials and first layout options."),
         ("Space planning", "2D layout plan validated with the client."),
         ("3D visualization", "Realistic renders of each key space."),
         ("Technical drawings", "Elevations, sections and custom furniture details."),
         ("Material selection", "Samples, finishes and manufacturer references."),
         ("Follow-up", "Coordination with workshops and craftsmen until completion.")]


def process():
    steps = "".join(f'<div class="st"><i>{i + 1:02d}</i><b>{e(t)}</b><span>{e(d)}</span></div>' for i, (t, d) in enumerate(STEPS))
    body = (kicker("Design process") + box(M, 26, 200, '<h2>From the first visit<br>to the finished space</h2>')
            + box(M, 86, PW - 2 * M, f'<div class="steps">{steps}</div>'))
    page(body, section="Design process", toc=("—", "Design Process"))


def contact():
    body = (box(0, 0, PW, f'<div class="ct-logo">{logo("kaira-2-alternative-stacked-ivory.svg")}</div>', h=118)
            + box(54, 126, PW - 108, '<div class="ct-grid">'
                  '<div><label>Founder</label><b>Karen Wehbe</b></div>'
                  f'<div><label>Instagram</label><b>{INSTAGRAM}</b></div>'
                  '<div><label>E-mail</label><b class="todo">to be completed</b></div>'
                  '<div><label>Phone / WhatsApp</label><b class="todo">to be completed</b></div>'
                  '<div><label>Website</label><b class="todo">to be completed</b></div>'
                  '<div><label>Studio</label><b>KAÏRA Interior Design</b></div></div>'))
    page(body, cls="burgundy", footer=False, toc=("—", "Contact"))


def contents():
    page("__TOC__", section="Contents")


CSS = """
@font-face{font-family:Jost;font-weight:300;src:url(FONTS/jost-latin-300-normal.woff2)}
@font-face{font-family:Jost;font-weight:400;src:url(FONTS/jost-latin-400-normal.woff2)}
@font-face{font-family:Jost;font-weight:500;src:url(FONTS/jost-latin-500-normal.woff2)}
@font-face{font-family:Cormorant;font-weight:300;src:url(FONTS/cormorant-garamond-latin-300-normal.woff2)}
@font-face{font-family:Cormorant;font-weight:400;src:url(FONTS/cormorant-garamond-latin-400-normal.woff2)}
@font-face{font-family:Cormorant;font-weight:300;font-style:italic;src:url(FONTS/cormorant-garamond-latin-300-italic.woff2)}
@font-face{font-family:Cormorant;font-weight:400;font-style:italic;src:url(FONTS/cormorant-garamond-latin-400-italic.woff2)}
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;font-family:Jost;font-weight:300;color:#2E2420}
.pg{position:relative;width:297mm;height:210mm;overflow:hidden;page-break-after:always;background:#FFFFFF}
.pg.olive{background:#5F6A45;color:#FAF7F2}.pg.burgundy{background:#6E2234;color:#FAF7F2}
.b{position:absolute}
.img img{width:100%;height:100%;display:block}
.img.fit{display:flex;align-items:center;justify-content:center;background:#FFFFFF}.img.fit img{width:auto;height:auto;max-width:100%;max-height:100%}
.crop{overflow:hidden}.crop img{position:absolute;display:block;max-width:none}
.k{font-size:2.15mm;letter-spacing:.34em;text-transform:uppercase;color:#6E2234;font-weight:400}
.k.light{color:#E7D9B8}
h1{font-family:Cormorant;font-weight:300;font-size:14mm;line-height:.98;margin:4mm 0 5mm}
h2{font-family:Cormorant;font-weight:300;font-size:10.5mm;line-height:1.04;margin:0}
h2.xl{font-size:17mm;line-height:.95}h2.light{color:#FAF7F2}
h3{font-family:Cormorant;font-weight:300;font-size:8.2mm;line-height:1.05;margin:0 0 3mm}
h4{font-family:Cormorant;font-weight:400;font-size:5.2mm;margin:0 0 1.2mm}
.sub{font-size:2.6mm;letter-spacing:.2em;text-transform:uppercase;color:#5F6A45;margin-top:3mm}
p{font-size:2.75mm;line-height:1.62;margin:0 0 2.8mm}
p.lead{font-family:Cormorant;font-size:5mm;line-height:1.36;font-weight:400}
p.cap{font-size:2.45mm;line-height:1.5;color:#5B4F46;margin:0 0 1.6mm}p.cap.c{text-align:left}
p.small{font-size:2.3mm;line-height:1.5;color:#8A7B6E}
.cv-logo svg{width:76mm;height:auto}
.cv-sub{font-size:2.6mm;line-height:1.6;color:#5F6A45;letter-spacing:.05em}
.cv-f{font-size:2.5mm;line-height:1.7;letter-spacing:.08em;color:#5B4F46;border-top:.25mm solid #2E2420;padding-top:2.5mm}
.cv-f b{font-weight:500;color:#2E2420}
.sig{border-top:.25mm solid #2E2420;padding-top:2.5mm}.sig span{display:block;font-family:Cormorant;font-size:6mm}
.sig em{font-style:normal;font-size:2.3mm;letter-spacing:.2em;text-transform:uppercase;color:#8A7B6E}
blockquote{margin:0;font-family:Cormorant;font-style:italic;font-weight:300;font-size:9mm;line-height:1.15;color:#2E2420}
.pillars3 div{display:grid;grid-template-columns:12mm 1fr;border-top:.2mm solid #D9CFC2;padding:3.5mm 0}
.pillars3 i{grid-row:span 2;font-family:Cormorant;font-style:italic;font-size:7mm;color:#6E2234;line-height:1}
.pillars3 b{font-family:Cormorant;font-weight:400;font-size:5.4mm}.pillars3 span{font-size:2.55mm;line-height:1.55;color:#5B4F46}
.svcs{display:grid;grid-template-columns:repeat(4,1fr);gap:9mm 8mm}
.svc{border-top:.25mm solid rgba(250,247,242,.6);padding-top:2.6mm}
.svc i{display:block;font-family:Cormorant;font-style:italic;font-size:6mm;color:#E7D9B8}
.svc b{display:block;font-family:Cormorant;font-weight:400;font-size:5.6mm;margin:1mm 0 1.2mm}
.svc span{font-size:2.45mm;line-height:1.5;opacity:.88}
.pc i{font-family:Cormorant;font-style:italic;font-size:6mm;color:#6E2234;margin-right:2mm}
.pc b{font-family:Cormorant;font-weight:400;font-size:6mm}.pc span{display:block;font-size:2.4mm;letter-spacing:.06em;color:#5B4F46;margin-top:1mm}
.pc.s b{font-size:4.4mm}.pc.s span{font-size:2.2mm}
table.facts{border-collapse:collapse;width:100%;font-size:2.5mm;margin-top:4mm}
table.facts td{border-top:.2mm solid #D9CFC2;padding:2.2mm 0;vertical-align:top;line-height:1.5}
table.facts td:first-child{width:24mm;font-size:2.1mm;letter-spacing:.2em;text-transform:uppercase;color:#6E2234;padding-top:2.6mm}
.nh{font-size:2.15mm;letter-spacing:.3em;text-transform:uppercase;color:#5F6A45;font-weight:500;margin:0 0 1.6mm}
.chips{display:flex;gap:4mm}.chip{flex:1}.chip span{display:block;height:9mm}
.chip b{display:block;font-weight:400;font-size:2.3mm;margin-top:1.4mm}.chip em{font-style:normal;font-size:2mm;color:#8A7B6E}
.scale{font-size:2.2mm;letter-spacing:.2em;text-transform:uppercase;color:#6E2234;margin-top:3mm}
.mat span{display:block;height:3mm;margin-bottom:2mm}.mat b{display:block;font-family:Cormorant;font-weight:400;font-size:4.6mm}
.mat em{display:block;font-style:normal;font-size:2.3mm;color:#5B4F46;line-height:1.4}.mat i{font-style:normal;font-size:2mm;color:#8A7B6E}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:9mm 8mm}
.st{border-top:.25mm solid #2E2420;padding-top:2.6mm}.st i{display:block;font-family:Cormorant;font-style:italic;font-size:6mm;color:#6E2234}
.st b{display:block;font-family:Cormorant;font-weight:400;font-size:5.4mm;margin:1mm 0 1.2mm}.st span{font-size:2.45mm;line-height:1.5;color:#5B4F46}
.ct-logo{display:flex;align-items:flex-end;justify-content:center;height:112mm}.ct-logo svg{width:84mm;height:auto}
.ct-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:6mm 10mm;border-top:.25mm solid rgba(250,247,242,.6);padding-top:5mm}
.ct-grid label{display:block;font-size:2mm;letter-spacing:.3em;text-transform:uppercase;opacity:.75;margin-bottom:1.2mm}
.ct-grid b{font-family:Cormorant;font-weight:400;font-size:5.6mm}.ct-grid b.todo{font-family:Jost;font-weight:300;font-size:2.6mm;
 letter-spacing:.12em;opacity:.7;border-bottom:.25mm dashed rgba(250,247,242,.7);padding-bottom:1mm;display:inline-block;min-width:52mm}
.hdr{position:absolute;right:14mm;top:9mm;font-size:2mm;letter-spacing:.3em;text-transform:uppercase;color:#8A7B6E}
.ftr{position:absolute;left:14mm;right:14mm;bottom:7mm;display:flex;justify-content:space-between;font-size:2mm;
 letter-spacing:.3em;text-transform:uppercase;color:#8A7B6E}
.pg.olive .ftr,.pg.olive .hdr{color:#E7D9B8}
.toc{position:absolute;left:14mm;top:24mm;width:269mm}
.toc .row{display:grid;grid-template-columns:16mm 1fr 14mm;align-items:baseline;border-bottom:.2mm solid #D9CFC2;padding:3.4mm 0}
.toc .row i{font-family:Cormorant;font-style:italic;font-size:6.5mm;color:#6E2234}
.toc .row b{font-family:Cormorant;font-weight:300;font-size:8mm}.toc .row em{font-style:normal;text-align:right;font-size:2.8mm}
"""


def toc_html():
    rows = [("—", "About the Studio", 3), ("—", "Creative Vision", 4), ("—", "Services", 5)]
    for i, pg in enumerate(PAGES, 1):
        if pg["toc"]:
            rows.append((pg["toc"][0], pg["toc"][1], i))
    return ('<div class="toc"><div class="k">Contents</div><div style="height:5mm"></div>'
            + "".join(f'<div class="row"><i>{n}</i><b>{e(t)}</b><em>{p:02d}</em></div>' for n, t, p in rows) + "</div>")


def assemble():
    PAGES.clear()
    cover(); contents(); about(); vision(); services(); projects_index(); villa(); interiors(); kids(); process(); contact()
    out = []
    for i, pg in enumerate(PAGES, 1):
        body = toc_html() if pg["body"] == "__TOC__" else pg["body"]
        hdr = f'<div class="hdr">{e(pg["section"])}</div>' if pg["section"] and pg["footer"] else ""
        ftr = (f'<div class="ftr"><span>KAÏRA Interior Design</span><span>{i:02d}</span></div>' if pg["footer"] else "")
        out.append(f'<section class="pg {pg["cls"]}">{body}{hdr}{ftr}</section>')
    css = CSS.replace("FONTS/", FONTS.as_uri() + "/")
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>KAÏRA Interior Design — Portfolio</title>'
            f'<style>{css}</style></head><body>{PATTERNS}{"".join(out)}</body></html>')


def make_light():
    LIGHT.mkdir(parents=True, exist_ok=True)
    for key, p in USED.items():
        out = LIGHT / (key.replace("/", "_").rsplit(".", 1)[0] + ".jpg")
        im = Image.open(p).convert("RGB")
        im.thumbnail((1500, 1500), Image.LANCZOS)
        im.save(out, quality=80, optimize=True, progressive=True)


def pdf(html_path, out, previews=False):
    js = f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage();
 await p.goto('file://{html_path}', {{ waitUntil: 'networkidle' }}); await p.evaluate(() => document.fonts.ready);
 await p.pdf({{ path: '{out}', width: '297mm', height: '210mm', printBackground: true, preferCSSPageSize: true }});
 if (process.argv[1]) {{ await p.setViewportSize({{ width: 1123, height: 794 }});
  const els = await p.$$('section.pg');
  for (let i = 0; i < els.length; i++) await els[i].screenshot({{ path: '{BUILD}/v-' + String(i + 1).padStart(2, '0') + '.png' }}); }}
 await b.close(); }})();"""
    subprocess.run(["node", "-e", js] + (["prev"] if previews else []), check=True,
                   cwd=str(REPO / "projects/instagram-lancement/tools"))


def main():
    global LIGHT_MODE
    BUILD.mkdir(exist_ok=True)
    LIGHT_MODE = False
    doc = assemble()
    (BUILD / "portfolio-hd.html").write_text(doc, encoding="utf-8")
    print(len(PAGES), "pages")
    pdf(BUILD / "portfolio-hd.html", OUT_HD, "--previews" in sys.argv)
    make_light()
    LIGHT_MODE = True
    doc = assemble()
    (BUILD / "portfolio-light.html").write_text(doc, encoding="utf-8")
    pdf(BUILD / "portfolio-light.html", OUT_LIGHT)
    (BUILD / "used.json").write_text(json.dumps({k: str(v) for k, v in USED.items()}, indent=1))
    for f in (OUT_HD, OUT_LIGHT):
        print(f.name, f"{f.stat().st_size / 1e6:.1f} MB")


# =============================================================================== v2 — new chapters
def spread(k1, k2, kick, title, cap1, cap2, section, toc=None, col=92):
    """Large image on the left, smaller image and text on the right. Whole images, never cropped."""
    iw, ih = size(k1)
    wa = PW - 2 * M - col - 10
    ha = wa * ih / iw
    if ha > PH - 2 * M - 8:
        ha = PH - 2 * M - 8
        wa = ha * iw / ih
    a, wa, ha = image(k1, M, M, w=wa)
    xb = M + wa + 10
    wb = PW - M - xb
    jw, jh = size(k2)
    hb = min(wb * jh / jw, 112)
    b, wb, hb = image(k2, xb, M, h=hb)
    body = (a + b + kicker(kick, xb, M + hb + 6)
            + box(xb, M + hb + 13, PW - M - xb, f'<h3>{e(title)}</h3><p class="cap">{e(cap1)}</p><p class="cap">{e(cap2)}</p>'))
    page(body, section=section, toc=toc)


CHAPTERS = [("01", "Villa", "Private residence — ground & first floor", "salon02"),
            ("02", "Residential Interiors", "Living rooms, dining rooms, kitchens, entrance", "livG"),
            ("03", "Workspaces", "Executive and private offices", "off14"),
            ("04", "Rooftop Bar & Lounge", "Hospitality space with a city view", "bar"),
            ("05", "Retail Showroom", "Home appliances & electronics", "rAC"),
            ("06", "Children's Rooms", "A collection of five residential concepts", "07.png")]


def projects_index():
    wcard, hcard, gx = (PW - 2 * M - 2 * 9) / 3, 54, 9
    out = ""
    for i, (n, t, sub, key) in enumerate(CHAPTERS):
        x = M + (i % 3) * (wcard + gx)
        y = 36 + (i // 3) * (hcard + 30)
        out += (f'<div class="b img fit" style="left:{x:.1f}mm;top:{y:.1f}mm;width:{wcard:.1f}mm;height:{hcard}mm">'
                f'<img src="{src(key)}"></div>'
                + box(x, y + hcard + 3.5, wcard, f'<div class="pc"><i>{n}</i><b>{e(t)}</b><span>{e(sub)}</span>'
                                                 f'<em class="pn">p. {{{{p:{t}}}}}</em></div>'))
    page(kicker("Selected projects") + box(M, 22, 200, '<h2>Selected projects</h2>') + out, section="Selected projects")


def residential():
    sec = "Project 02 — Residential Interiors"
    im, w, h = image("livG", M, M, w=190)
    x = M + w + 12
    body = (im + kicker("Project 02", x)
            + box(x, 26, PW - x - M, '<h2 class="xl">Residential<br>Interiors</h2>')
            + box(x, 70, PW - x - M, '<p class="lead">Living rooms, dining rooms, kitchens and entrances designed by the '
                                     'studio for private homes.</p>'
                                     '<p class="cap">Living room — sculptural white bouclé seating, a curved sofa and arched '
                                     'armchairs, against taupe wall panels framed by walnut fluted strips; track lighting, a '
                                     'lit display cabinet and a large monochrome artwork.</p>'))
    page(body, section=sec, toc=("02", "Residential Interiors"))
    spread("dinG", "dinB", "Dining rooms", "Dining rooms",
           "The adjoining dining room becomes a gallery: a white marble table and walnut armchairs under a cluster of "
           "glass globe pendants, facing three expressive portraits.",
           "Another home: a marble table on a black marble base, black and ivory armchairs, linen curtains, a geometric "
           "artwork and terracotta jars.", sec)
    spread("livW", "tvOak", "Living rooms", "Living rooms",
           "Tall walnut cabinetry with a lit black niche, a stone-clad TV wall, a floating walnut console and layered ceiling "
           "coves, in taupe, cognac and sage.",
           "An oak-panelled TV wall with black reveals and vertical battens, a backlit screen and a floating cabinet with a "
           "dark stone top, framed by full-height curtains.", sec)
    spread("kitL", "kit20", "Kitchens", "Kitchens",
           "An L-shaped kitchen in greige matt lacquer, black veined marble worktop and splashback, lit open shelves and "
           "handle-less fronts under a perimeter light cove.",
           "Cream lacquered units around a waterfall island in boldly veined stone, black appliances and a herringbone floor.",
           sec)
    wl, hl, he = 99, 99 * 1264 / 1600, 128
    we = he * 1468 / 1600
    x0 = M + (PW - 2 * M - (wl + 10 + we)) / 2
    a1, _, _ = image("liv19", x0, M, w=wl)
    a2, _, _ = image("liv13", x0, M + hl + 9, w=wl)
    xe = x0 + wl + 10
    c1, we, he = image("ent21", xe, M, h=he)
    body = (a1 + a2 + c1
            + box(x0, M + hl + 1.5, wl, '<p class="cap">Open living space — modular sofas, oak-clad columns, dining area beyond.</p>')
            + box(x0, M + 2 * hl + 10.5, wl, '<p class="cap">Living room opening onto a sculptural white staircase.</p>')
            + kicker("Living & entrance", xe, M + he + 5)
            + box(xe, M + he + 12, we, '<h3>Living &amp; entrance</h3><p class="cap">Two luminous living areas in white, '
                                       'grey and light oak, with recessed lighting, an arched sideboard and graphic artworks. '
                                       'The entrance: walnut wall panelling with black reveals, an arched-front sideboard and '
                                       'a portrait artwork on marble-effect flooring.</p>'))
    page(body, section=sec)
    det = [("tvOak", (150, 1000, 525, 1350), "Oak panelling, black reveal and vertical battens"),
           ("kitL", (500, 470, 880, 700), "Black marble splashback and lit open shelves"),
           ("dinG", (690, 430, 1010, 640), "Cluster of glass globe pendants"),
           ("livG", (1180, 230, 1560, 640), "Walnut fluted strip and taupe wall panels"),
           ("bar", (330, 900, 1050, 1250), "Walnut battens and recessed LED line"),
           ("off2", (600, 720, 1260, 1000), "Oak desk with a black fluted front")]
    out = ""
    wt, ht, gx, gy = 84, 62, 8.5, 18
    for i, (k, bx, cap) in enumerate(det):
        x = M + (i % 3) * (wt + gx)
        y = 38 + (i // 3) * (ht + gy)
        out += crop_fixed(k, bx, x, y, wt, ht) + box(x, y + ht + 2, wt, f'<p class="cap c">{e(cap)}</p>')
    page(kicker("Interior details") + box(M, 22, 200, '<h3>Interior details — selected projects</h3>') + out, section=sec)


def workspaces():
    spread("off14", "off2", "Project 03 — Workspaces", "Workspaces",
           "Executive office facing a panoramic city view: walnut desk and meeting table, backlit green onyx panels framing "
           "the shelving, a lounge corner in soft leather and a perimeter light cove.",
           "Private office: an oak desk with a black fluted front, a black open bookcase with oak accents and lit shelves, "
           "under a curved ceiling cove.", "Project 03 — Workspaces", toc=("03", "Workspaces"))


def rooftop():
    spread("bar", "lounge", "Project 04 — Hospitality", "Rooftop bar & lounge",
           "A bar counter clad in vertical walnut battens, with a dark green marble top and a recessed LED line, facing the "
           "city skyline.",
           "The lounge: woven armchairs with ivory cushions, brass and black bar stools, white marble-effect floor and a "
           "framed light line in the ceiling.", "Project 04 — Rooftop Bar & Lounge", toc=("04", "Rooftop Bar & Lounge"))


def retail():
    sec = "Project 05 — Retail Showroom"
    im, w, h = image("rAC", M, M, w=190)
    x = M + w + 12
    body = (im + kicker("Project 05", x)
            + box(x, 26, PW - x - M, '<h2 class="xl">Retail<br>Showroom</h2>')
            + box(x, 70, PW - x - M, '<p class="lead">A showroom for home appliances and consumer electronics, organised '
                                     'in brand zones and product families.</p>'
                                     '<p class="cap">Graphite display walls with walnut shelves and plinths, LED-outlined '
                                     'niches and brand headers, poster panels, and a bright marble-effect floor under a '
                                     'continuous light line.</p>'
                                     '<p class="cap">Shown: air-conditioning wall — split and light-commercial units.</p>'))
    page(body, section=sec, toc=("05", "Retail Showroom"))
    y1, h1, g = 30, 47, 8
    row1 = [("rBrands", "Brand zones — overview"), ("rIsl", "TV and air-conditioning islands"), ("rAudio", "Audio islands")]
    w1 = (PW - 2 * M - 2 * g) / 3
    body = kicker("Retail showroom") + box(M, 20, 200, '<h3>Display design</h3>')
    x = M
    for k, cap in row1:
        im, w, h = image(k, x, y1, w=w1)
        body += im + box(x, y1 + h + 1.5, w, f'<p class="cap">{e(cap)}</p>')
        x += w + g
    y2 = y1 + w1 * 900 / 1600 + 11
    row2 = [("rHall", "Appliance hall — refrigerator wall"), ("rTV", "TV wall and lit island"),
            ("rMidea", "Display units with LED outlines")]
    ratio = sum(size(k)[0] / size(k)[1] for k, _ in row2)
    h2 = min(PH - 18 - y2 - 8, (PW - 2 * M - 2 * g) / ratio)
    tot = ratio * h2 + 2 * g
    x = M + (PW - 2 * M - tot) / 2
    for k, cap in row2:
        im, w, h = image(k, x, y2, h=h2)
        body += im + box(x, y2 + h + 1.5, w, f'<p class="cap">{e(cap)}</p>')
        x += w + g
    page(body, section=sec)


def kids():
    P = {p["key"]: p for p in pdata.PROJECTS}
    sec = "Project 06 — Children's Rooms"
    im, w, h = image("07.png", 104, 18, w=179)
    order = [("lapin", "Douceur Lapin"), ("jungle", "Jungle Douce"), ("nuages", "Nuages"), ("ourson", "Ourson Caramel")]
    th = ""
    wt = (179 - 3 * 5) / 4
    for i, (k, n) in enumerate(order):
        t, tw, thh = image(P[k]["img"], 104 + i * (wt + 5), 18 + h + 7, w=wt)
        th += t + box(104 + i * (wt + 5), 18 + h + 7 + thh + 1.5, wt, f'<p class="cap">{e(n)}</p>')
    body = (kicker("Project 06") + box(M, 26, 82, '<h2>Children\'s<br>rooms</h2>')
            + box(M, 56, 82, '<p class="lead">Arches, scallops and clouds: five residential concepts where soft shapes are '
                             'drawn into the custom furniture itself.</p><p>Each room has its own palette — powder pink, olive, '
                             'caramel — rooted in cream and light wood, with indirect light integrated into niches, arches and '
                             'headboards.</p><p class="cap">Large image: Nuage Olive.</p>')
            + im + th)
    page(body, section=sec, toc=("06", "Children's Rooms"))
    p = P["nuageolive"]
    svg, w, h = KV.elevation(p, "A", 25)
    body = (kicker("Design drawings") + box(M, 22, 200, '<h3>From render to drawing</h3>')
            + svgbox(svg, (PW - w) / 2, 38) + box((PW - w) / 2, 38 + h + 3, w,
                                                  '<p class="cap">Nuage Olive — elevation of the decorative wall, 1:25 (A4): '
                                                  'wardrobe, olive storage column, fluted wall with backlit cloud, upholstered '
                                                  'headboard, trundle bed and floating desk. Proposed concept dimensions in cm.</p>'))
    page(body, section=sec)


def assemble():
    PAGES.clear()
    cover(); about(); vision(); services(); projects_index(); villa(); residential(); workspaces(); rooftop(); retail()
    kids(); process(); contact()
    where = {pg["toc"][1]: i for i, pg in enumerate(PAGES, 1) if pg["toc"]}
    out = []
    for i, pg in enumerate(PAGES, 1):
        body = pg["body"]
        for t, n in where.items():
            body = body.replace("{{p:" + t + "}}", f"{n:02d}")
        hdr = f'<div class="hdr">{e(pg["section"])}</div>' if pg["section"] and pg["footer"] else ""
        ftr = (f'<div class="ftr"><span>KAÏRA Interior Design</span><span>{i:02d}</span></div>' if pg["footer"] else "")
        out.append(f'<section class="pg {pg["cls"]}">{body}{hdr}{ftr}</section>')
    css = CSS.replace("FONTS/", FONTS.as_uri() + "/") + ".pc em.pn{display:block;font-style:normal;font-size:2.2mm;letter-spacing:.2em;color:#6E2234;margin-top:1.2mm}"
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>KAÏRA Interior Design — Portfolio</title>'
            f'<style>{css}</style></head><body>{PATTERNS}{"".join(out)}</body></html>')



if __name__ == "__main__":
    main()
