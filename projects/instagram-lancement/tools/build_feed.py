"""KAÏRA — feed Instagram de lancement construit avec les rendus du studio.

Étapes : écrans TV éteints -> retouche « lumière du jour » (tools/retouch.py) -> mise en page HTML des
slides 1080 × 1350 (4:5) -> capture JPEG -> grille de prévisualisation (tuiles 3:4 comme le profil Instagram).
Usage : python3 tools/build_feed.py
"""
import json, pathlib, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from retouch import retouch  # noqa: E402

SRC = ROOT / "sources/recus"
DOS = ROOT.parent / "dossier-client"
B = ROOT / "build/feed"
RET = B / "img"
OUT = ROOT / "livrables/feed"
W, H = 1080, 1350

C = dict(ivory="#F7F3EC", paper="#FBF8F3", choc="#3B2A22", walnut="#6A4A36", oak="#A9825C",
         olive="#66704C", bordeaux="#7A2B38", mute="#8C7C6E", line="#D9CDBE")

# ------------------------------------------------------------------ sources
TV_QUADS = {"15": [(511, 665), (1025, 690), (1025, 962), (515, 1000)],
            "16": [(581, 582), (880, 632), (880, 822), (580, 826)]}
DOSSIER_TVOFF = {"03": "etage1-sejour-01", "10": "rdc-salon-04"}   # mêmes rendus, écran déjà éteint


def tv_off(im, quad):
    im = im.copy()
    xs, ys = [p[0] for p in quad], [p[1] for p in quad]
    w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
    yy, xx = np.mgrid[0:h, 0:w]
    refl = np.clip(1 - np.abs(xx / w - 0.35 - yy / h * 0.3) * 4, 0, 1)
    v = 14 + 8 * (1 - yy / h) + 10 * refl
    scr = Image.fromarray(np.dstack([v, v, v * 1.08]).clip(0, 255).astype(np.uint8))
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).polygon(quad, fill=255)
    layer = Image.new("RGB", im.size)
    layer.paste(scr, (min(xs), min(ys)))
    return Image.composite(layer, im, mask.filter(ImageFilter.GaussianBlur(0.8)))


def load(key):
    """key = '07' (rendu reçu) ou 'D:chambre-principale-03' (rendu du dossier villa)."""
    if key.startswith("D:"):
        name = key[2:]
        off = DOS / "build/tvoff" / f"{name}.png"
        if off.exists():
            return Image.open(off).convert("RGB")
        return Image.open(next((DOS / "sources").glob(f"*/{name}.png"))).convert("RGB")
    if key in DOSSIER_TVOFF:
        return load("D:" + DOSSIER_TVOFF[key])
    p = next(SRC.glob(f"{key}.*"))
    im = Image.open(p).convert("RGB")
    return tv_off(im, TV_QUADS[key]) if key in TV_QUADS else im


def img(key, crop=None, force=1.0):
    """Rendu retouché (mis en cache) ; crop = (x0, y0, x1, y1) en pixels de l'original."""
    tag = key.replace("D:", "D-") + ("" if crop is None else "-" + "-".join(map(str, crop)))
    out = RET / f"{tag}.jpg"
    if not out.exists():
        full = RET / f"{key.replace('D:', 'D-')}.full.jpg"
        if not full.exists():
            retouch(load(key), force).save(full, quality=95, subsampling=0)
        im = Image.open(full)
        if crop:
            im = im.crop(crop)
        im.save(out, quality=95, subsampling=0)
    return "img/" + out.name


# ------------------------------------------------------------------ gabarits de slides
FONTS = "".join(
    f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};src:url(fonts/{f})}}'
    for fam, w, st, f in [("Cormorant", 300, "normal", "cormorant-garamond-latin-300-normal.woff2"),
                          ("Cormorant", 400, "normal", "cormorant-garamond-latin-400-normal.woff2"),
                          ("Cormorant", 500, "normal", "cormorant-garamond-latin-500-normal.woff2"),
                          ("Cormorant", 300, "italic", "cormorant-garamond-latin-300-italic.woff2"),
                          ("Cormorant", 400, "italic", "cormorant-garamond-latin-400-italic.woff2"),
                          ("Jost", 300, "normal", "jost-latin-300-normal.woff2"),
                          ("Jost", 400, "normal", "jost-latin-400-normal.woff2")])
CSS = FONTS + f"""
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{font-family:Jost;font-weight:300;color:{C['choc']};background:{C['ivory']};position:relative;-webkit-font-smoothing:antialiased}}
.serif{{font-family:Cormorant;font-weight:300}} i{{font-family:Cormorant;font-style:italic}}
.caps{{font-family:Jost;font-weight:400;text-transform:uppercase;letter-spacing:.34em}}
.ph{{position:absolute;background-size:cover;background-repeat:no-repeat}}
.word{{font-family:Cormorant;font-weight:400;letter-spacing:.42em}}
"""


def cover(src, pos, kicker, title, accent, num):
    """Couverture éditoriale : rendu dans un passe-partout ivoire, titre sous l'image."""
    return f"""<div class="ph" style="left:84px;right:84px;top:84px;height:1000px;background-image:url({src});background-position:{pos}"></div>
<div style="position:absolute;left:84px;right:84px;top:1122px;display:flex;justify-content:space-between;align-items:flex-end">
 <div><div class="caps" style="font-size:15px;color:{C['oak']}">{kicker}</div>
  <div class="serif" style="font-size:68px;line-height:1;margin-top:14px">{title}</div></div>
 <div style="text-align:right"><div style="width:46px;height:2px;background:{accent};margin:0 0 18px auto"></div>
  <div class="word" style="font-size:24px;margin-right:-.42em">KAÏRA</div>
  <div class="caps" style="font-size:11px;color:{C['mute']};margin-top:6px;letter-spacing:.3em">N° {num}</div></div>
</div>"""


def cover_wide(src, kicker, title, sub, accent, num):
    """Couverture pour rendu paysage : image pleine largeur en haut, texte en dessous."""
    return f"""<div class="ph" style="left:0;right:0;top:0;height:853px;background-image:url({src});background-position:50% 50%"></div>
<div style="position:absolute;left:84px;right:84px;top:930px">
 <div class="caps" style="font-size:15px;color:{C['oak']}">{kicker}</div>
 <div class="serif" style="font-size:76px;line-height:1.02;margin-top:18px">{title}</div>
 <div style="font-size:21px;color:{C['mute']};margin-top:22px;line-height:1.5;max-width:640px">{sub}</div></div>
<div style="position:absolute;right:84px;bottom:84px;text-align:right">
 <div style="width:46px;height:2px;background:{accent};margin:0 0 18px auto"></div>
 <div class="word" style="font-size:24px;margin-right:-.42em">KAÏRA</div>
 <div class="caps" style="font-size:11px;color:{C['mute']};margin-top:6px">N° {num}</div></div>"""


def full(src, pos="50% 50%"):
    return f'<div class="ph" style="inset:0;background-image:url({src});background-position:{pos}"></div>'


def matted(src, caption):
    """Slide intérieure : image détail sur fond ivoire avec légende discrète."""
    return f"""<div class="ph" style="left:84px;right:84px;top:84px;bottom:190px;background-image:url({src});background-position:50% 50%"></div>
<div class="caps" style="position:absolute;left:84px;bottom:108px;font-size:14px;color:{C['mute']}">{caption}</div>
<div class="word" style="position:absolute;right:84px;bottom:102px;font-size:20px;margin-right:-.42em">KAÏRA</div>"""


def page(body, bg=None):
    style = f' style="background:{bg}"' if bg else ""
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body{style}>{body}</body></html>'


# ------------------------------------------------------------------ les 9 publications
def manifesto():
    s1 = f"""<div style="position:absolute;inset:70px;border:1.5px solid {C['line']}"></div>
<div style="position:absolute;top:190px;left:0;right:0;text-align:center">
 <div class="word" style="font-size:124px;margin-right:-.42em">KAÏRA</div>
 <div class="caps" style="font-size:19px;margin-top:10px;color:{C['walnut']}">Interior Design</div></div>
<div style="position:absolute;top:585px;left:0;right:0;text-align:center">
 <div style="width:72px;height:2px;background:{C['olive']};margin:0 auto 60px"></div>
 <div class="serif" style="font-size:92px;line-height:1.02">The architecture<br><i style="color:{C['bordeaux']}">of calm</i></div></div>
<div class="caps" style="position:absolute;bottom:150px;left:0;right:0;text-align:center;font-size:16px;color:{C['walnut']}">Space &nbsp;·&nbsp; Material &nbsp;·&nbsp; Light</div>"""
    items = [("Proportion", "Volumes drawn to human scale, generous circulation, sightlines that breathe."),
             ("Material", "Stone, wood and textiles chosen for their truth and the way they age."),
             ("Light", "Daylight first, then warm layers of indirect light that shape the room.")]
    s2 = f"""<div style="position:absolute;left:96px;right:96px;top:120px">
 <div class="caps" style="font-size:16px;color:{C['oak']}">Our approach</div>
 <div class="serif" style="font-size:88px;line-height:1;margin-top:30px">Three words,<br><i style="color:{C['olive']}">one intention</i></div></div>
<div style="position:absolute;left:96px;right:96px;bottom:130px">
 {''.join(f'<div style="display:flex;gap:40px;padding:30px 0;border-top:1px solid {C["line"]}"><div class="serif" style="font-size:28px;color:{C["oak"]};width:46px">0{k + 1}</div><div><div class="serif" style="font-size:46px">{t}</div><div style="font-size:21px;line-height:1.55;color:{C["mute"]};margin-top:8px">{d}</div></div></div>' for k, (t, d) in enumerate(items))}</div>"""
    services = ["Interior design", "Space planning", "Bespoke furniture &amp; joinery", "Materials &amp; lighting", "3D visualisation"]
    s3 = f"""<div style="position:absolute;left:96px;right:96px;top:120px">
 <div class="caps" style="font-size:16px;color:{C['oak']}">KAÏRA Interior Design</div>
 <div class="serif" style="font-size:96px;line-height:1;margin-top:30px">Our <i style="color:{C['bordeaux']}">services</i></div></div>
<div style="position:absolute;left:96px;right:96px;bottom:150px">
 {''.join(f'<div style="display:flex;align-items:baseline;gap:40px;padding:26px 0;border-top:1px solid {C["line"]}"><span class="serif" style="font-size:28px;color:{C["oak"]};width:46px">0{k + 1}</span><span class="serif" style="font-size:50px">{t}</span></div>' for k, t in enumerate(services))}
 <div class="caps" style="font-size:14px;color:{C['mute']};padding-top:36px;border-top:1px solid {C['line']}">Residences · Villas · Workspaces</div></div>"""
    return [page(s1), page(s2, C["paper"]), page(s3)]


SWATCHES = [  # (rendu, recadrage, nom) — échantillons pris dans les rendus du studio
    ("05", (600, 440, 820, 660), "Dark veined marble"),
    ("D:chambre-amis-02", (880, 160, 1240, 520), "White veined marble"),
    ("04", (1470, 700, 1630, 860), "Sheer curtains"),
    ("08", (600, 480, 735, 615), "Natural oak"),
    ("08", (150, 620, 370, 840), "Dark wood"),
    ("11", (800, 1640, 940, 1780), "Bouclé"),
    ("05", (700, 1240, 880, 1420), "Olive textile"),
    ("08", (1000, 1160, 1140, 1300), "Taupe leather"),
    ("04", (0, 640, 200, 840), "Bordeaux art"),
]


def materials():
    cells = "".join(
        f'<div><div style="width:100%;aspect-ratio:1;background:url({img(k, c)}) center/cover"></div>'
        f'<div class="serif" style="font-size:24px;margin-top:10px">{n}</div></div>' for k, c, n in SWATCHES)
    s = f"""<div style="position:absolute;left:84px;right:84px;top:84px">
 <div class="caps" style="font-size:15px;color:{C['oak']}">Material story</div>
 <div class="serif" style="font-size:72px;line-height:1;margin-top:16px">The KAÏRA <i style="color:{C['olive']}">palette</i></div></div>
<div style="position:absolute;left:84px;right:84px;top:290px;display:grid;grid-template-columns:repeat(3,262px);justify-content:space-between;gap:30px 0">{cells}</div>
<div class="word" style="position:absolute;right:84px;bottom:58px;font-size:20px;margin-right:-.42em">KAÏRA</div>"""
    return [page(s)]


def detail():
    s = f"""<div class="ph" style="left:230px;width:620px;top:96px;height:775px;background-image:url({img('11', (380, 380, 1000, 1155))});background-position:center"></div>
<div style="position:absolute;left:96px;right:96px;top:930px;text-align:center">
 <div class="caps" style="font-size:15px;color:{C['oak']}">Our approach</div>
 <div class="serif" style="font-size:74px;line-height:1.02;margin-top:18px">The detail <i style="color:{C['bordeaux']}">makes the space</i></div>
 <div style="font-size:20px;color:{C['mute']};margin-top:22px;line-height:1.55">A veined marble column, a sculpture, a floating console.<br>Every junction is drawn before it is built.</div></div>"""
    return [page(s)]


POSTS = [  # ordre de publication 01 -> 09
    ("01-manifesto", manifesto),
    ("02-villa-living-room", lambda: [page(cover(img("07"), "50% 50%", "Villa · Ground floor", "Living room", C["olive"], "02")),
                                      page(full(img("12"), "42% 50%")), page(full(img("08"), "50% 50%")),
                                      page(full(img("10"), "45% 50%"))]),
    ("03-villa-master-bedroom", lambda: [page(cover(img("05"), "50% 50%", "Villa · First floor", "Master bedroom", C["bordeaux"], "03")),
                                         page(matted(img("05", (140, 0, 900, 950)), "Backlit marble · fluted oak · pendant light")),
                                         page(full(img("D:chambre-principale-03"), "50% 50%")),
                                         page(full(img("D:chambre-principale-04"), "50% 50%"))]),
    ("04-villa-guest-bedroom", lambda: [page(cover(img("06"), "45% 50%", "Villa · Ground floor", "Guest bedroom", C["olive"], "04")),
                                        page(full(img("D:chambre-amis-01"), "50% 50%")),
                                        page(full(img("D:chambre-amis-02"), "55% 50%"))]),
    ("05-material-palette", materials),
    ("06-villa-lounge", lambda: [page(cover(img("04"), "22% 50%", "Villa · First floor", "Lounge", C["bordeaux"], "06")),
                                 page(full(img("02"), "55% 50%")), page(full(img("03"), "50% 50%"))]),
    ("07-selected-projects", lambda: [page(cover_wide(img("13"), "Selected projects", "Residences <i style='color:#66704C'>&amp; workspaces</i>",
                                                      "Light-filled living spaces, bespoke joinery and executive offices.", C["olive"], "07")),
                                      page(full(img("14"), "40% 50%")), page(full(img("16"), "55% 50%")),
                                      page(full(img("15"), "50% 50%"))]),
    ("08-villa-dining-room", lambda: [page(cover(img("09"), "50% 50%", "Villa · Ground floor", "Dining room", C["bordeaux"], "08")),
                                      page(full(img("11"), "50% 50%")), page(full(img("D:rdc-salon-06"), "25% 50%"))]),
    ("09-the-detail", detail),
]
# position sur le profil une fois les 9 publiées (la plus récente en haut à gauche)
GRID = [["09-the-detail", "08-villa-dining-room", "07-selected-projects"],
        ["06-villa-lounge", "05-material-palette", "04-villa-guest-bedroom"],
        ["03-villa-master-bedroom", "02-villa-living-room", "01-manifesto"]]


def main():
    RET.mkdir(parents=True, exist_ok=True)
    shutil.copytree(DOS / "build/fonts", B / "fonts", dirs_exist_ok=True)
    jobs = []
    for name, fn in POSTS:
        (OUT / name).mkdir(parents=True, exist_ok=True)
        for k, html in enumerate(fn(), 1):
            f = B / f"{name}-{k}.html"
            f.write_text(html, encoding="utf-8")
            jobs.append([str(f), str(OUT / name / f"{name}-{k}.jpg")])
    (B / "jobs.json").write_text(json.dumps({"w": W, "h": H, "jobs": jobs}))
    subprocess.run(["node", str(ROOT / "tools/shoot.js"), str(B / "jobs.json")], check=True)
    # grille : tuiles 3:4 (recadrage centré, comme l'affiche le profil Instagram)
    tw, th, gap = 360, 480, 4
    grid = Image.new("RGB", (3 * tw + 2 * gap, 3 * th + 2 * gap), "#FFFFFF")
    for r, row in enumerate(GRID):
        for c, name in enumerate(row):
            im = Image.open(OUT / name / f"{name}-1.jpg")
            cw = int(H * 3 / 4)
            im = im.crop(((W - cw) // 2, 0, (W - cw) // 2 + cw, H)).resize((tw, th), Image.LANCZOS)
            grid.paste(im, (c * (tw + gap), r * (th + gap)))
    grid.save(ROOT / "livrables/grille-feed.jpg", quality=93)
    print(len(jobs), "slides")


if __name__ == "__main__":
    main()
