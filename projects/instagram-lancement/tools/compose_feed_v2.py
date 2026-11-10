"""KAÏRA — feed v2 construit à partir des rendus du studio (aucune image générée).

Usage : python3 tools/retouche_rendus.py   puis   python3 tools/compose_feed_v2.py
Entrée : rendus/retouches/  ·  Sortie : livrables/feed-v2/ (publications 1080 × 1350, grille, planche)
Le feed v1 (livrables/visuels, livrables/grille-feed.jpg, légendes) n'est pas modifié.
"""
import json, pathlib, shutil, subprocess
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
RET = ROOT / "rendus/retouches"
B = ROOT / "build-v2"
IMG = B / "img"
OUT = ROOT / "livrables/feed-v2"
FONTS_SRC = ROOT.parent / "dossier-client/build/fonts"
W, H = 1080, 1350

C = dict(paper="#FAF7F2", ivory="#F4EFE6", sage="#E5E6D8", choc="#3B2A22", walnut="#5A3E2E", oak="#B08A64",
         olive="#5E6B47", bord="#6E2433", muted="#8C7462")

FONTFACE = "".join(
    f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};src:url(fonts/{f})}}'
    for fam, w, st, f in [("Cormorant", 300, "normal", "cormorant-garamond-latin-300-normal.woff2"),
                          ("Cormorant", 400, "normal", "cormorant-garamond-latin-400-normal.woff2"),
                          ("Cormorant", 500, "normal", "cormorant-garamond-latin-500-normal.woff2"),
                          ("Cormorant", 300, "italic", "cormorant-garamond-latin-300-italic.woff2"),
                          ("Cormorant", 400, "italic", "cormorant-garamond-latin-400-italic.woff2"),
                          ("Jost", 300, "normal", "jost-latin-300-normal.woff2"),
                          ("Jost", 400, "normal", "jost-latin-400-normal.woff2"),
                          ("Jost", 500, "normal", "jost-latin-500-normal.woff2")])
CSS = FONTFACE + f"""
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{position:relative;font-family:Jost;font-weight:300;color:{C['choc']};-webkit-font-smoothing:antialiased}}
.serif{{font-family:Cormorant;font-weight:300}} .serif i{{font-style:italic;color:{C['bord']}}}
.caps{{font-family:Jost;font-weight:400;text-transform:uppercase;letter-spacing:.3em;font-size:13px}}
.abs{{position:absolute}} img{{display:block}}
.mark{{font-family:Cormorant;font-weight:400;letter-spacing:.42em;font-size:21px}}
"""

# ------------------------------------------------------------------ préparation des images


def src(name):
    return Image.open(RET / f"{name}.jpg").convert("RGB")


def crop_to(im, box, size):
    """Recadre `box`, puis ajuste au ratio de `size` (rognage centré minimal) et redimensionne."""
    im = im.crop(box) if box else im
    tw, th = size
    r, rt = im.width / im.height, tw / th
    if r > rt:                                   # trop large : rogne les côtés
        nw = round(im.height * rt); x = (im.width - nw) // 2
        im = im.crop((x, 0, x + nw, im.height))
    elif r < rt:                                 # trop haut : rogne haut et bas
        nh = round(im.width / rt); y = (im.height - nh) // 2
        im = im.crop((0, y, im.width, y + nh))
    return im.resize(size, Image.LANCZOS)


def fit(box_w, box_h, w, h):
    s = min(box_w / w, box_h / h)
    return round(w * s), round(h * s)


def prep(pid, name, box, size):
    IMG.mkdir(parents=True, exist_ok=True)
    crop_to(src(name), box, size).save(IMG / f"{pid}.jpg", quality=95, subsampling=0)
    return f"img/{pid}.jpg"


# ------------------------------------------------------------------ gabarits


def cover_band(pid, name, kicker, title, num, box=None):
    """Couverture : rendu complet en haut, bandeau papier avec titre éditorial."""
    ph = 1177
    url = prep(pid, name, box, (W, ph))
    return C["paper"], f"""
<img class="abs" src="{url}" style="left:0;top:0;width:{W}px;height:{ph}px">
<div class="abs" style="left:0;right:0;top:{ph}px;height:1px;background:{C['oak']};opacity:.55"></div>
<div class="abs" style="left:76px;top:{ph + 34}px">
  <div class="caps" style="color:{C['olive']}">{kicker}</div>
  <div class="serif" style="font-size:52px;line-height:1;margin-top:14px">{title}</div>
</div>
<div class="abs" style="right:76px;top:{ph + 40}px;text-align:right">
  <div class="mark">KAÏRA</div>
  <div class="caps" style="font-size:11px;color:{C['muted']};margin-top:14px">N° {num}</div>
</div>"""


def full_bleed(pid, name, box):
    url = prep(pid, name, box, (W, H))
    return "#000", f'<img class="abs" src="{url}" style="left:0;top:0;width:{W}px;height:{H}px">'


def detail(pid, name, box, kicker, title, text, maxh=930):
    """Détail cadré sur papier, légende courte en dessous."""
    x0, y0, x1, y1 = box
    w, h = fit(928, maxh, x1 - x0, y1 - y0)
    url = prep(pid, name, box, (w, h))
    cap_h = 190
    top = max(92, (H - (h + 56 + cap_h)) // 2)
    left = (W - w) // 2
    return C["paper"], f"""
<img class="abs" src="{url}" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px">
<div class="abs" style="left:{left}px;top:{top + h + 50}px;width:{max(w, 600)}px">
  <div class="caps" style="color:{C['olive']}">{kicker}</div>
  <div class="serif" style="font-size:42px;line-height:1.05;margin-top:12px">{title}</div>
  <div style="font-size:18px;line-height:1.55;color:{C['walnut']};margin-top:12px;max-width:640px">{text}</div>
</div>
<div class="abs mark" style="right:76px;bottom:64px;font-size:17px;color:{C['muted']}">KAÏRA</div>"""


def cover_landscape(pid, name, kicker, title, num, foot):
    ih = 853
    url = prep(pid, name, None, (W, ih))
    return C["paper"], f"""
<div class="abs" style="left:76px;top:96px">
  <div class="caps" style="color:{C['olive']}">{kicker}</div>
  <div class="serif" style="font-size:64px;line-height:1;margin-top:16px">{title}</div>
</div>
<div class="abs" style="right:76px;top:104px;text-align:right">
  <div class="mark">KAÏRA</div>
  <div class="caps" style="font-size:11px;color:{C['muted']};margin-top:14px">N° {num}</div>
</div>
<img class="abs" src="{url}" style="left:0;top:282px;width:{W}px;height:{ih}px">
<div class="abs caps" style="left:76px;right:76px;top:{282 + ih + 62}px;font-size:12px;color:{C['walnut']};text-align:center">{foot}</div>"""


def manifesto():
    return C["ivory"], f"""
<div class="abs" style="inset:64px;border:1.5px solid {C['oak']}"></div>
<div class="abs" style="top:190px;left:0;right:0;text-align:center">
  <div class="serif" style="font-size:124px;letter-spacing:.28em;margin-left:.28em;font-weight:400">KAÏRA</div>
  <div class="caps" style="font-size:18px;margin-top:8px;color:{C['walnut']}">Interior Design</div>
</div>
<div class="abs" style="top:600px;left:0;right:0;text-align:center">
  <div style="width:72px;height:2px;background:{C['olive']};margin:0 auto 60px"></div>
  <div class="serif" style="font-size:96px;line-height:1.02">The architecture<br><i>of calm</i></div>
</div>
<div class="abs caps" style="bottom:150px;left:0;right:0;text-align:center;font-size:15px;color:{C['walnut']}">
  Space &nbsp;·&nbsp; Material &nbsp;·&nbsp; Light</div>"""


SWATCHES = [  # (rendu, zone carrée, nom, usage) — échantillons découpés dans les rendus du studio
    ("05-salle-a-manger-detail", (1310, 1348, 1470, 1508), "Travertine", "Dining table"),
    ("02-salon-mur-tv", (620, 1440, 920, 1740), "Natural oak", "Flooring"),
    ("03-chambre-marbre", (560, 380, 840, 660), "Green marble", "Headboard wall"),
    ("05-salle-a-manger-detail", (1420, 1600, 1620, 1800), "Bouclé", "Dining chairs"),
    ("03-chambre-marbre", (820, 1170, 1060, 1410), "Olive", "Bed throw"),
    ("05-salle-a-manger-detail", (1375, 720, 1655, 1000), "Bordeaux", "Artwork"),
]


def palette():
    cells, s, gap, x0, y0 = [], 272, 40, 0, 430
    x0 = (W - (3 * s + 2 * gap)) // 2
    for i, (name, box, label, use) in enumerate(SWATCHES):
        url = prep(f"sw{i}", name, box, (s, s))
        cx, cy = x0 + (i % 3) * (s + gap), y0 + (i // 3) * (s + 150)
        cells.append(f"""<img class="abs" src="{url}" style="left:{cx}px;top:{cy}px;width:{s}px;height:{s}px">
<div class="abs" style="left:{cx}px;top:{cy + s + 20}px"><div class="serif" style="font-size:30px;font-weight:400">{label}</div>
<div class="caps" style="font-size:11px;color:{C['muted']};margin-top:6px">{use}</div></div>""")
    return C["paper"], f"""
<div class="abs" style="left:{x0}px;top:120px">
  <div class="caps" style="color:{C['olive']}">Drawn from our projects</div>
  <div class="serif" style="font-size:84px;line-height:1;margin-top:18px">The KAÏRA <i>palette</i></div>
</div>
{''.join(cells)}
<div class="abs caps" style="left:0;right:0;bottom:84px;text-align:center;font-size:12px;color:{C['walnut']}">
  Warm whites &nbsp;·&nbsp; natural wood &nbsp;·&nbsp; stone &nbsp;·&nbsp; olive &nbsp;·&nbsp; bordeaux</div>"""


def services():
    items = [("01", "Interior design"), ("02", "Space planning"), ("03", "Bespoke furniture"),
             ("04", "Materials &amp; lighting"), ("05", "3D visualisation")]
    rows = "".join(f'<div style="display:flex;align-items:baseline;gap:36px;padding:24px 0;border-top:1px solid rgba(94,107,71,.35)">'
                   f'<span class="serif" style="font-size:28px;color:{C["bord"]};width:44px;font-weight:400">{n}</span>'
                   f'<span class="serif" style="font-size:46px">{t}</span></div>' for n, t in items)
    return C["sage"], f"""
<div class="abs" style="left:96px;top:120px">
  <div class="caps" style="color:{C['olive']}">KAÏRA Interior Design</div>
  <div class="serif" style="font-size:104px;line-height:1;margin-top:26px">Our <i>services</i></div>
</div>
<div class="abs" style="left:96px;right:96px;top:470px">{rows}
  <div style="border-top:1px solid rgba(94,107,71,.35)"></div></div>
<div class="abs" style="left:96px;right:96px;bottom:110px;display:flex;justify-content:space-between;align-items:baseline">
  <div class="caps" style="font-size:12px;color:{C['walnut']}">Residences · Villas · Apartments</div>
  <div class="caps" style="font-size:12px;color:{C['olive']}">Enquiries by direct message</div>
</div>"""


# ------------------------------------------------------------------ le feed (ordre de publication)

POSTS = [
    ("01-manifesto", [lambda: manifesto()]),
    ("02-living-room", [
        lambda: cover_band("02a", "01-salon-tableau-bordeaux", "Living Room · Concept", "Quiet <i>living</i>", "02"),
        lambda: detail("02b", "01-salon-tableau-bordeaux", (150, 330, 1010, 1405), "Detail",
                       "Light in the <i>joinery</i>", "Integrated lighting traces each shelf, and a bordeaux artwork answers the warmth of the wood."),
        lambda: detail("02c", "01-salon-tableau-bordeaux", (560, 1020, 1520, 1800), "Detail",
                       "Stone &amp; <i>dark wood</i>", "A marble pedestal table beside a slim dark-wood table, set on a woven rug."),
        lambda: detail("02d", "02-salon-mur-tv", (0, 330, 590, 1068), "The media wall",
                       "Backlit <i>niches</i>", "Natural wood shelving with concealed lighting and a stone-clad fin."),
    ]),
    ("03-bedroom-marble", [
        lambda: cover_band("03a", "03-chambre-marbre", "Master Bedroom · Concept", "The marble <i>suite</i>", "03"),
        lambda: detail("03b", "03-chambre-marbre", (110, 100, 1010, 1225), "Detail",
                       "A wall of <i>marble</i>", "A single panel of green marble, framed by backlit lacquer and fluted wood."),
        lambda: detail("03c", "03-chambre-marbre", (800, 1230, 1667, 1816), "Detail",
                       "Soft <i>contrasts</i>", "A channel-tufted bench on a brushed brass base, with an olive throw over ivory linen."),
    ]),
    ("04-bedroom-ivory", [
        lambda: cover_band("04a", "04-chambre-claire", "Bedroom · Concept", "Soft <i>ivory</i>", "04"),
        lambda: detail("04b", "04-chambre-claire", (40, 250, 880, 1300), "Detail",
                       "Vertical <i>rhythm</i>", "Slatted wood and two halo pendants draw the eye up towards the light cove."),
        lambda: detail("04c", "04-chambre-claire", (420, 1050, 1667, 1816), "Detail",
                       "Low and <i>enveloping</i>", "A platform bed upholstered in an ivory weave, grounded on a pale rug."),
    ]),
    ("05-palette", [lambda: palette()]),
    ("06-dining-room", [
        lambda: cover_band("06a", "06-salle-a-manger", "Dining Room · Concept", "Around the <i>table</i>", "06"),
        lambda: full_bleed("06b", "05-salle-a-manger-detail", (110, 0, 1563, 1816)),
        lambda: detail("06c", "05-salle-a-manger-detail", (380, 1180, 1667, 1816), "Detail",
                       "Travertine &amp; <i>bouclé</i>", "A travertine table surrounded by bouclé chairs with dark wood frames."),
    ]),
    ("07-open-plan", [
        lambda: cover_landscape("07a", "07-sejour-ouvert", "Living &amp; Dining · Concept", "Open-plan <i>living</i>", "07",
                                "Warm whites &nbsp;·&nbsp; natural wood &nbsp;·&nbsp; pale stone"),
        lambda: detail("07b", "07-sejour-ouvert", (620, 300, 1600, 1000), "Detail",
                       "Wood as <i>structure</i>", "Tall wood-clad volumes separate living and dining while keeping the view through to the garden."),
    ]),
    ("08-kitchen", [
        lambda: cover_band("08a", "08-cuisine", "Kitchen · Concept", "The stone <i>island</i>", "08"),
        lambda: detail("08b", "08-cuisine", (500, 800, 1330, 1600), "Detail",
                       "Stone at the <i>centre</i>", "A waterfall island in veined stone, set on herringbone flooring."),
    ]),
    ("09-services", [lambda: services()]),
]

# Grille du profil une fois les 9 publiées (la 01 en bas à droite, la 09 en haut à gauche)
GRID = [["09-services", "08-kitchen", "07-open-plan"],
        ["06-dining-room", "05-palette", "04-bedroom-ivory"],
        ["03-bedroom-marble", "02-living-room", "01-manifesto"]]


def main():
    shutil.copytree(FONTS_SRC, B / "fonts", dirs_exist_ok=True)
    jobs = []
    for post, slides in POSTS:
        (OUT / "posts" / post).mkdir(parents=True, exist_ok=True)
        for i, make in enumerate(slides, 1):
            bg, body = make()
            html = B / f"{post}-{i:02d}.html"
            html.write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
                            f'<body style="background:{bg}">{body}</body></html>', encoding="utf-8")
            jobs.append({"html": str(html), "out": str(OUT / "posts" / post / f"{i:02d}.jpg")})
    (B / "jobs.json").write_text(json.dumps({"width": W, "height": H, "jobs": jobs}))
    subprocess.run(["node", str(ROOT / "tools/shoot_v2.js"), str(B / "jobs.json")], check=True)

    # Grille telle que le profil l'affiche : vignettes 3:4 recadrées au centre des publications 4:5
    cw, ch, gap = 360, 480, 4
    grid = Image.new("RGB", (3 * cw + 2 * gap, 3 * ch + 2 * gap), "#FFFFFF")
    for r, row in enumerate(GRID):
        for c, post in enumerate(row):
            cover = Image.open(OUT / "posts" / post / "01.jpg")
            grid.paste(crop_to(cover, None, (cw, ch)), (c * (cw + gap), r * (ch + gap)))
    grid.save(OUT / "grille-feed.jpg", quality=92)

    # Planche des carrousels (une ligne par publication)
    tw, th, pad = 216, 270, 14
    n = max(len(s) for _, s in POSTS)
    sheet = Image.new("RGB", (pad + n * (tw + pad) + 190, pad + len(POSTS) * (th + pad)), C["paper"])
    d = ImageDraw.Draw(sheet)
    for r, (post, slides) in enumerate(POSTS):
        y = pad + r * (th + pad)
        d.text((pad, y + th // 2 - 6), post, fill=C["choc"])
        for i in range(len(slides)):
            im = Image.open(OUT / "posts" / post / f"{i + 1:02d}.jpg").resize((tw, th), Image.LANCZOS)
            sheet.paste(im, (190 + i * (tw + pad), y))
    sheet.save(OUT / "planche-carrousels.jpg", quality=90)
    print(f"{len(jobs)} visuels ->", OUT)


if __name__ == "__main__":
    main()
