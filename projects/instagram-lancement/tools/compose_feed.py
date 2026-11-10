"""KAÏRA — feed Instagram composé avec les rendus ORIGINAUX du studio, sans aucun traitement.

Règle : chaque rendu est collé pixel pour pixel, à sa taille d'origine (aucun redimensionnement, recadrage,
retouche ni recoloration). Seul le fond et la typographie sont dessinés autour.
Les slides font 2160 × 2700 px (format Instagram 4:5, deux fois 1080 × 1350) pour accueillir les rendus
à 100 %. Sorties en PNG (sans perte), profil sRGB comme les originaux.
Chaque slide est vérifiée : la zone de l'image doit être identique à l'original, sinon le script s'arrête.

Usage : python3 tools/compose_feed.py
"""
import io, json, pathlib, shutil, subprocess
import numpy as np
from PIL import Image, ImageCms

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "sources/recus"
B = ROOT / "build/feed"
OUT = ROOT / "livrables/feed"
FONTS = ROOT.parent / "dossier-client/build/fonts"
W, H, M = 2160, 2700, 246
SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()

C = dict(ivory="#F7F3EC", paper="#FBF8F3", choc="#3B2A22", walnut="#6A4A36", oak="#A9825C",
         olive="#66704C", bordeaux="#7A2B38", mute="#8C7C6E", line="#D9CDBE")


def original(n):
    p = next(SRC.glob(f"{n}.*"))
    im = Image.open(p)
    return im.convert("RGB")          # PNG RGBA entièrement opaques -> RGB : pixels inchangés


# ------------------------------------------------------------------ typographie (HTML, sans image)
FACES = "".join(
    f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};src:url(fonts/{f})}}'
    for fam, w, st, f in [("Cormorant", 300, "normal", "cormorant-garamond-latin-300-normal.woff2"),
                          ("Cormorant", 400, "normal", "cormorant-garamond-latin-400-normal.woff2"),
                          ("Cormorant", 300, "italic", "cormorant-garamond-latin-300-italic.woff2"),
                          ("Jost", 300, "normal", "jost-latin-300-normal.woff2"),
                          ("Jost", 400, "normal", "jost-latin-400-normal.woff2")])
CSS = FACES + f"""
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{font-family:Jost;font-weight:300;color:{C['choc']};background:{C['ivory']};position:relative;-webkit-font-smoothing:antialiased}}
.serif{{font-family:Cormorant;font-weight:300}} i{{font-family:Cormorant;font-weight:300;font-style:italic}}
.caps{{font-family:Jost;font-weight:400;text-transform:uppercase;letter-spacing:.34em}}
.word{{font-family:Cormorant;font-weight:400;letter-spacing:.42em}}
.abs{{position:absolute}}
"""


def html(body, bg=None):
    st = f' style="background:{bg}"' if bg else ""
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body{st}>{body}</body></html>'


def brand(num, accent, bottom=200):
    return (f'<div class="abs" style="right:{M}px;bottom:{bottom}px;text-align:right">'
            f'<div style="width:92px;height:3px;background:{accent};margin:0 0 34px auto"></div>'
            f'<div class="word" style="font-size:48px;margin-right:-.42em">KAÏRA</div>'
            f'<div class="caps" style="font-size:22px;color:{C["mute"]};margin-top:12px">{num}</div></div>')


def cover_text(kicker, title, accent, num, top):
    return (f'<div class="abs" style="left:{M}px;top:{top}px">'
            f'<div class="caps" style="font-size:30px;color:{C["oak"]}">{kicker}</div>'
            f'<div class="serif" style="font-size:136px;line-height:1;margin-top:28px">{title}</div></div>'
            + brand(f"N° {num}", accent))


def inner_text(label, page):
    return (f'<div class="caps abs" style="left:{M}px;bottom:240px;font-size:26px;color:{C["mute"]}">{label}</div>'
            f'<div class="abs" style="right:{M}px;bottom:226px;text-align:right">'
            f'<div class="word" style="font-size:40px;margin-right:-.42em">KAÏRA</div>'
            f'<div class="caps" style="font-size:22px;color:{C["mute"]};margin-top:10px">{page}</div></div>')


def manifesto():
    return html(f"""<div class="abs" style="inset:140px;border:3px solid {C['line']}"></div>
<div class="abs" style="top:400px;left:0;right:0;text-align:center">
 <div class="word" style="font-size:248px;margin-right:-.42em">KAÏRA</div>
 <div class="caps" style="font-size:38px;margin-top:20px;color:{C['walnut']}">Interior Design</div></div>
<div class="abs" style="top:1180px;left:0;right:0;text-align:center">
 <div style="width:144px;height:4px;background:{C['olive']};margin:0 auto 120px"></div>
 <div class="serif" style="font-size:184px;line-height:1.02">The architecture<br><i style="color:{C['bordeaux']}">of calm</i></div></div>
<div class="caps abs" style="bottom:300px;left:0;right:0;text-align:center;font-size:32px;color:{C['walnut']}">Space &nbsp;·&nbsp; Material &nbsp;·&nbsp; Light</div>""")


def approach():
    items = [("Proportion", "Volumes drawn to human scale, generous circulation, sightlines that breathe."),
             ("Material", "Stone, wood and textiles chosen for their truth and the way they age."),
             ("Light", "Daylight first, then warm layers of indirect light that shape the room.")]
    rows = "".join(f'<div style="display:flex;gap:80px;padding:60px 0;border-top:2px solid {C["line"]}">'
                   f'<div class="serif" style="font-size:56px;color:{C["oak"]};width:92px">0{k + 1}</div>'
                   f'<div><div class="serif" style="font-size:92px">{t}</div>'
                   f'<div style="font-size:42px;line-height:1.55;color:{C["mute"]};margin-top:16px">{d}</div></div></div>'
                   for k, (t, d) in enumerate(items))
    return html(f"""<div class="abs" style="left:192px;right:192px;top:240px">
 <div class="caps" style="font-size:32px;color:{C['oak']}">Our approach</div>
 <div class="serif" style="font-size:176px;line-height:1;margin-top:60px">Three words,<br><i style="color:{C['olive']}">one intention</i></div></div>
<div class="abs" style="left:192px;right:192px;bottom:260px">{rows}</div>""", C["paper"])


def services():
    items = ["Interior design", "Space planning", "Bespoke furniture &amp; joinery", "Materials &amp; lighting", "3D visualisation"]
    rows = "".join(f'<div style="display:flex;align-items:baseline;gap:80px;padding:52px 0;border-top:2px solid {C["line"]}">'
                   f'<span class="serif" style="font-size:56px;color:{C["oak"]};width:92px">0{k + 1}</span>'
                   f'<span class="serif" style="font-size:100px">{t}</span></div>' for k, t in enumerate(items))
    return html(f"""<div class="abs" style="left:192px;right:192px;top:240px">
 <div class="caps" style="font-size:32px;color:{C['oak']}">KAÏRA Interior Design</div>
 <div class="serif" style="font-size:192px;line-height:1;margin-top:60px">Our <i style="color:{C['bordeaux']}">services</i></div></div>
<div class="abs" style="left:192px;right:192px;bottom:300px">{rows}
 <div class="caps" style="font-size:28px;color:{C['mute']};padding-top:72px;border-top:2px solid {C['line']}">Residences · Villas · Workspaces</div></div>""")


# ------------------------------------------------------------------ publications
def slide_img(n, text_fn):
    """Slide avec un rendu original centré horizontalement, en haut, à 100 %."""
    w, h = original(n).size
    x, y = (W - w) // 2, M
    return {"img": n, "xy": (x, y), "html": html(text_fn(y + h))}


def cover(n, kicker, title, accent, num):
    return slide_img(n, lambda bottom: cover_text(kicker, title, accent, num, bottom + 96))


def inner(n, label, page):
    return slide_img(n, lambda bottom: inner_text(label, page))


def cover_wide(n, kicker, title, sub, accent, num):
    def t(bottom):
        return (f'<div class="abs" style="left:{M}px;right:{M}px;top:{bottom + 130}px">'
                f'<div class="caps" style="font-size:30px;color:{C["oak"]}">{kicker}</div>'
                f'<div class="serif" style="font-size:150px;line-height:1.02;margin-top:34px">{title}</div>'
                f'<div style="font-size:42px;color:{C["mute"]};margin-top:44px;line-height:1.5;max-width:1300px">{sub}</div></div>'
                + brand(f"N° {num}", accent))
    return slide_img(n, t)


POSTS = [  # ordre de publication 01 -> 09
    ("01-manifesto", [{"html": manifesto()}]),
    ("02-villa-living-room", [cover("07", "Villa · Ground floor", "Living room", C["olive"], "02"),
                              inner("12", "Villa · Living room", "2 / 3"),
                              inner("08", "Villa · Living room", "3 / 3")]),
    ("03-villa-master-bedroom", [cover("05", "Villa · First floor", "Master bedroom", C["bordeaux"], "03")]),
    ("04-villa-guest-bedroom", [cover("06", "Villa · Ground floor", "Guest bedroom", C["olive"], "04")]),
    ("05-our-approach", [{"html": approach()}]),
    ("06-villa-lounge", [cover("04", "Villa · First floor", "Lounge", C["bordeaux"], "06"),
                         inner("02", "Villa · First-floor lounge", "2 / 3"),
                         inner("01", "Villa · First-floor lounge", "3 / 3")]),
    ("07-selected-projects", [cover_wide("13", "Selected projects", f"Residences <i style='color:{C['olive']}'>&amp; workspaces</i>",
                                         "Light-filled living spaces and executive offices.", C["olive"], "07"),
                              inner("14", "Selected projects · Executive office", "2 / 2")]),
    ("08-villa-dining-room", [cover("09", "Villa · Ground floor", "Dining room", C["bordeaux"], "08"),
                              inner("11", "Villa · Dining room", "2 / 2")]),
    ("09-our-services", [{"html": services()}]),
]
GRID = [["09-our-services", "08-villa-dining-room", "07-selected-projects"],
        ["06-villa-lounge", "05-our-approach", "04-villa-guest-bedroom"],
        ["03-villa-master-bedroom", "02-villa-living-room", "01-manifesto"]]


def main():
    B.mkdir(parents=True, exist_ok=True)
    shutil.copytree(FONTS, B / "fonts", dirs_exist_ok=True)
    jobs, plan = [], []
    for name, slides in POSTS:
        (OUT / name).mkdir(parents=True, exist_ok=True)
        for k, s in enumerate(slides, 1):
            h = B / f"{name}-{k}.html"
            h.write_text(s["html"], encoding="utf-8")
            bg = B / f"{name}-{k}.bg.png"
            jobs.append([str(h), str(bg)])
            plan.append((name, k, s.get("img"), s.get("xy"), bg))
    (B / "jobs.json").write_text(json.dumps({"w": W, "h": H, "jobs": jobs}))
    subprocess.run(["node", str(ROOT / "tools/shoot.js"), str(B / "jobs.json")], check=True)
    report = []
    for name, k, n, xy, bg in plan:
        canvas = Image.open(bg).convert("RGB")
        assert canvas.size == (W, H)
        if n:
            src = original(n)
            canvas.paste(src, xy)                         # collage pixel pour pixel, aucune transformation
            x, y = xy
            region = np.asarray(canvas)[y:y + src.height, x:x + src.width]
            same = np.array_equal(region, np.asarray(src))
            assert same, f"{name}-{k} : image modifiée !"
            report.append(f"{name}-{k}.png : rendu {n} collé à 100 % ({src.width} × {src.height}) — identique à l'original")
        else:
            report.append(f"{name}-{k}.png : slide typographique")
        canvas.save(OUT / name / f"{name}-{k}.png", icc_profile=SRGB, optimize=True)
    (ROOT / "livrables/verification.txt").write_text("\n".join(report) + "\n")
    # aperçu de la grille (réduit, tuiles 3:4 comme le profil Instagram) — fichier d'aperçu uniquement
    tw, th, gap = 360, 480, 4
    grid = Image.new("RGB", (3 * tw + 2 * gap, 3 * th + 2 * gap), "#FFFFFF")
    cw = int(H * 3 / 4)
    for r, row in enumerate(GRID):
        for c, name in enumerate(row):
            im = Image.open(OUT / name / f"{name}-1.png").convert("RGB")
            im = im.crop(((W - cw) // 2, 0, (W - cw) // 2 + cw, H)).resize((tw, th), Image.LANCZOS)
            grid.paste(im, (c * (tw + gap), r * (th + gap)))
    grid.save(ROOT / "livrables/apercu-grille.jpg", quality=92)
    print("\n".join(report))


if __name__ == "__main__":
    main()
