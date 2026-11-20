"""KAÏRA — feed de lancement en 12 publications (direction artistique complète).

Règles pour les rendus du studio : image toujours entière, proportions exactes, jamais recadrée, jamais
retouchée, jamais agrandie. Les slides sont conçues en HD 2160 × 2700 (4:5) : les rendus en pleine page y sont
collés pixel pour pixel (100 %). La version Instagram 1080 × 1350 est la slide HD réduite de moitié.
Tout le reste (fonds, typographie, palette, filets) est dessiné.

Usage : python3 tools/compose_feed12.py
"""
import json, pathlib, shutil, subprocess
import numpy as np
from PIL import Image, ImageCms

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "sources/recus"
B = ROOT / "build/feed12"
OUT = ROOT / "livrables/feed-12"
FONTS = ROOT.parent / "dossier-client/build/fonts"
W, H, M = 2160, 2700, 246
SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()

C = dict(white="#FDFBF8", ivory="#F7F3EC", cream="#F1E9DC", sage="#E8E9DD", blush="#F4EAE6",
         choc="#3B2A22", walnut="#6A4A36", oak="#A9825C", olive="#66704C", bordeaux="#7A2B38",
         mute="#8C7C6E", line="#D9CDBE")


def original(n):
    return Image.open(next(SRC.glob(f"{n}.*"))).convert("RGB")   # PNG opaques / JPEG sRGB : pixels inchangés


def size(n, w=None):
    ow, oh = original(n).size
    w = w or ow
    return w, round(oh * w / ow)


# ------------------------------------------------------------------ typographie
FACES = "".join(
    f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};src:url(fonts/{f})}}'
    for fam, w, st, f in [("Cormorant", 300, "normal", "cormorant-garamond-latin-300-normal.woff2"),
                          ("Cormorant", 400, "normal", "cormorant-garamond-latin-400-normal.woff2"),
                          ("Cormorant", 500, "normal", "cormorant-garamond-latin-500-normal.woff2"),
                          ("Cormorant", 300, "italic", "cormorant-garamond-latin-300-italic.woff2"),
                          ("Jost", 300, "normal", "jost-latin-300-normal.woff2"),
                          ("Jost", 400, "normal", "jost-latin-400-normal.woff2")])
CSS = FACES + f"""
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{font-family:Jost;font-weight:300;color:{C['choc']};position:relative;-webkit-font-smoothing:antialiased}}
.serif{{font-family:Cormorant;font-weight:300}} i{{font-family:Cormorant;font-weight:300;font-style:italic}}
.caps{{font-family:Jost;font-weight:400;text-transform:uppercase;letter-spacing:.34em}}
.word{{font-family:Cormorant;font-weight:400;letter-spacing:.42em}}
.abs{{position:absolute}}
"""


def page(body, bg):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body style="background:{bg}">{body}</body></html>'


def brand(num, accent, right=M, bottom=200, top=None):
    pos = f"top:{top}px" if top is not None else f"bottom:{bottom}px"
    return (f'<div class="abs" style="right:{right}px;{pos};text-align:right">'
            f'<div style="width:92px;height:3px;background:{accent};margin:0 0 34px auto"></div>'
            f'<div class="word" style="font-size:48px;margin-right:-.42em">KAÏRA</div>'
            f'<div class="caps" style="font-size:22px;color:{C["mute"]};margin-top:12px">{num}</div></div>')


def kicker(t, color=None):
    return f'<div class="caps" style="font-size:30px;color:{color or C["oak"]}">{t}</div>'


def slide(html, imgs=()):
    return {"html": html, "imgs": list(imgs)}


# ------------------------------------------------------------------ gabarits avec rendus
def cover_below(n, kick, title, accent, num):
    """Rendu à 100 % en haut, titre dessous."""
    w, h = size(n)
    x, y = (W - w) // 2, M
    t = (f'<div class="abs" style="left:{x}px;top:{y + h + 96}px">{kick}'
         f'<div class="serif" style="font-size:136px;line-height:1;margin-top:28px">{title}</div></div>'
         + brand(f"N° {num}", accent, right=x))
    return slide(page(t, C["white"]), [(n, x, y, w)])


def cover_above(n, kick, title, accent, num):
    """Titre en haut, rendu à 100 % dessous."""
    w, h = size(n)
    x, y = (W - w) // 2, H - M - h
    t = (f'<div class="abs" style="left:{x}px;top:170px">{kick}'
         f'<div class="serif" style="font-size:136px;line-height:1;margin-top:28px">{title}</div></div>'
         + brand(f"N° {num}", accent, right=x, top=190))
    return slide(page(t, C["white"]), [(n, x, y, w)])


def cover_wide(n, kick, title, sub, accent, num):
    w, h = size(n)
    x, y = (W - w) // 2, M
    t = (f'<div class="abs" style="left:{x}px;right:{x}px;top:{y + h + 130}px">{kick}'
         f'<div class="serif" style="font-size:150px;line-height:1.02;margin-top:34px">{title}</div>'
         f'<div style="font-size:42px;color:{C["mute"]};margin-top:44px;line-height:1.5;max-width:1300px">{sub}</div></div>'
         + brand(f"N° {num}", accent, right=x))
    return slide(page(t, C["white"]), [(n, x, y, w)])


def inner(n, label, pg):
    w, h = size(n)
    x, y = (W - w) // 2, M
    t = (f'<div class="caps abs" style="left:{x}px;bottom:240px;font-size:26px;color:{C["mute"]}">{label}</div>'
         f'<div class="abs" style="right:{x}px;bottom:226px;text-align:right">'
         f'<div class="word" style="font-size:40px;margin-right:-.42em">KAÏRA</div>'
         f'<div class="caps" style="font-size:22px;color:{C["mute"]};margin-top:10px">{pg}</div></div>')
    return slide(page(t, C["white"]), [(n, x, y, w)])


def material_notes():
    """Rendu 05 entier (réduit), notes de matières alignées à droite, repères hors de l'image."""
    n, w = "05", 1200
    _, h = size(n, w)
    x, y, s = 150, 470, w / 1667
    notes = [(440, "Dark veined marble", "Backlit band rising behind the bed"),
             (700, "Lit wood slats", "Vertical rhythm, warm hidden light"),
             (940, "Glass globe pendants", "Suspended on fine gold rods"),
             (1350, "Olive bed linen", "The single note of colour"),
             (1700, "Brushed-gold base", "Channel-tufted bench at the foot of the bed")]
    marks = ""
    for k, (oy, t, d) in enumerate(notes, 1):
        yy = y + oy * s
        marks += (f'<div class="abs" style="left:{x + w + 30}px;top:{yy - 1}px;width:70px;height:2px;background:{C["oak"]}"></div>'
                  f'<div class="abs" style="left:{x + w + 120}px;top:{yy - 34}px;right:150px">'
                  f'<div style="display:flex;gap:24px;align-items:baseline"><span class="serif" style="font-size:34px;color:{C["oak"]}">0{k}</span>'
                  f'<span class="serif" style="font-size:50px;line-height:1.05">{t}</span></div>'
                  f'<div style="font-size:27px;color:{C["mute"]};margin:10px 0 0 62px;line-height:1.4">{d}</div></div>')
    t = (f'<div class="abs" style="left:{x}px;top:170px">{kicker("Material notes")}'
         f'<div class="serif" style="font-size:118px;line-height:1;margin-top:26px">Master bedroom</div></div>'
         + marks
         + f'<div class="abs" style="left:{x}px;top:{y + h + 110}px;right:600px;font-size:36px;line-height:1.55;color:{C["mute"]}">'
           f'Five materials, one atmosphere: quiet, enveloping and warm.</div>'
         + f'<div class="abs" style="right:150px;bottom:226px;text-align:right"><div class="word" style="font-size:40px;margin-right:-.42em">KAÏRA</div>'
           f'<div class="caps" style="font-size:22px;color:{C["mute"]};margin-top:10px">2 / 2</div></div>')
    return slide(page(t, C["white"]), [(n, x, y, w)])


def detail():
    """Rendu 11 entier (réduit) + titre éditorial."""
    n, w = "11", 1360
    _, h = size(n, w)
    x, y = 150, 150
    t = (f'<div class="abs" style="left:{x + w + 70}px;top:{y}px;width:{h}px;height:120px;transform-origin:0 0;transform:translateX(120px) rotate(90deg)">'
         f'<div class="caps" style="font-size:28px;color:{C["oak"]};line-height:120px">Our approach &nbsp;—&nbsp; the detail</div></div>'
         f'<div class="abs" style="left:{x}px;top:{y + h + 120}px;right:150px">'
         f'<div class="serif" style="font-size:150px;line-height:1">The detail <i style="color:{C["bordeaux"]}">makes the space</i></div>'
         f'<div style="font-size:38px;color:{C["mute"]};margin-top:46px;line-height:1.55;max-width:1300px">'
         f'A veined marble column, a sculpture, a floating console and a wood library rising to the ceiling. '
         f'Every junction is drawn before it is built.</div></div>'
         + brand("N° 09", C["bordeaux"], right=150))
    return slide(page(t, C["ivory"]), [(n, x, y, w)])


# ------------------------------------------------------------------ gabarits typographiques
def manifesto():
    return slide(page(f"""<div class="abs" style="inset:140px;border:3px solid {C['line']}"></div>
<div class="abs" style="top:400px;left:0;right:0;text-align:center">
 <div class="word" style="font-size:248px;margin-right:-.42em">KAÏRA</div>
 <div class="caps" style="font-size:38px;margin-top:20px;color:{C['walnut']}">Interior Design</div></div>
<div class="abs" style="top:1180px;left:0;right:0;text-align:center">
 <div style="width:144px;height:4px;background:{C['olive']};margin:0 auto 120px"></div>
 <div class="serif" style="font-size:184px;line-height:1.02">The architecture<br><i style="color:{C['bordeaux']}">of calm</i></div></div>
<div class="caps abs" style="bottom:300px;left:0;right:0;text-align:center;font-size:32px;color:{C['walnut']}">Space &nbsp;·&nbsp; Material &nbsp;·&nbsp; Light</div>""", C["ivory"]))


PALETTE = [("Luminous white", "#FBF8F3"), ("Ivory", "#F3EDE3"), ("Cream", "#E9DFCF"),
           ("Natural oak", "#B58B62"), ("Olive", "#6B7350"), ("Bordeaux", "#7A2B38"), ("Chocolate", "#3B2A22")]


def palette():
    big = "".join(f'<div><div style="height:640px;background:{h};border:2px solid {C["line"]}"></div>'
                  f'<div class="serif" style="font-size:50px;margin-top:26px">{n}</div>'
                  f'<div class="caps" style="font-size:22px;color:{C["mute"]};margin-top:8px">{h}</div></div>' for n, h in PALETTE[:3])
    small = "".join(f'<div><div style="height:420px;background:{h}"></div>'
                    f'<div class="serif" style="font-size:44px;margin-top:22px">{n}</div>'
                    f'<div class="caps" style="font-size:22px;color:{C["mute"]};margin-top:8px">{h}</div></div>' for n, h in PALETTE[3:])
    return slide(page(f"""<div class="abs" style="left:170px;right:170px;top:170px">{kicker("Brand palette")}
 <div class="serif" style="font-size:150px;line-height:1;margin-top:30px">Light first, <i style="color:{C['olive']}">colour second</i></div></div>
<div class="abs" style="left:170px;right:170px;top:620px;display:grid;grid-template-columns:repeat(3,1fr);gap:50px">{big}</div>
<div class="abs" style="left:170px;right:170px;top:1560px;display:grid;grid-template-columns:repeat(4,1fr);gap:40px">{small}</div>
<div class="abs" style="left:170px;bottom:200px;font-size:34px;color:{C['mute']};max-width:1300px;line-height:1.5">
 Luminous whites and natural wood as the base; olive and bordeaux as single, deliberate accents.</div>
<div class="word abs" style="right:170px;bottom:200px;font-size:44px;margin-right:-.42em">KAÏRA</div>""", C["white"]))


def belief():
    return slide(page(f"""<div class="abs" style="left:200px;right:200px;top:300px">{kicker("Our belief", C['bordeaux'])}
 <div class="serif" style="font-size:300px;line-height:.6;color:{C['bordeaux']};margin-top:110px">&ldquo;</div>
 <div class="serif" style="font-size:150px;line-height:1.06;margin-top:10px">A home should calm the mind <i style="color:{C['bordeaux']}">before it impresses the eye.</i></div></div>
<div class="abs" style="left:200px;right:200px;bottom:330px">
 <div style="width:144px;height:4px;background:{C['bordeaux']};margin-bottom:70px"></div>
 <div style="font-size:40px;line-height:1.6;color:{C['walnut']};max-width:1500px">Every KAÏRA project starts with how a space should feel: the light at different hours, the touch of materials, the rhythm of a day. Only then do we draw.</div></div>
<div class="word abs" style="right:200px;bottom:200px;font-size:44px;margin-right:-.42em">KAÏRA</div>""", C["cream"]))


def approach():
    items = [("Proportion", "Volumes drawn to human scale, generous circulation, sightlines that breathe."),
             ("Material", "Stone, wood and textiles chosen for their truth and the way they age."),
             ("Light", "Daylight first, then warm layers of indirect light that shape the room.")]
    rows = "".join(f'<div style="display:flex;gap:80px;padding:64px 0;border-top:2px solid #C9CBB8">'
                   f'<div class="serif" style="font-size:56px;color:{C["olive"]};width:92px">0{k + 1}</div>'
                   f'<div><div class="serif" style="font-size:100px">{t}</div>'
                   f'<div style="font-size:40px;line-height:1.55;color:#6E7262;margin-top:16px">{d}</div></div></div>'
                   for k, (t, d) in enumerate(items))
    return slide(page(f"""<div class="abs" style="left:200px;right:200px;top:240px">{kicker("Our approach", C['olive'])}
 <div class="serif" style="font-size:176px;line-height:1;margin-top:60px">Three words,<br><i style="color:{C['olive']}">one intention</i></div></div>
<div class="abs" style="left:200px;right:200px;bottom:260px">{rows}</div>""", C["sage"]))


def services():
    items = ["Interior design", "Space planning", "Bespoke furniture &amp; joinery", "Materials &amp; lighting", "3D visualisation"]
    rows = "".join(f'<div style="display:flex;align-items:baseline;gap:80px;padding:52px 0;border-top:2px solid #DCC8C2">'
                   f'<span class="serif" style="font-size:56px;color:{C["bordeaux"]};width:92px">0{k + 1}</span>'
                   f'<span class="serif" style="font-size:100px">{t}</span></div>' for k, t in enumerate(items))
    s1 = page(f"""<div class="abs" style="left:200px;right:200px;top:240px">{kicker("KAÏRA Interior Design", C['bordeaux'])}
 <div class="serif" style="font-size:192px;line-height:1;margin-top:60px">Our <i style="color:{C['bordeaux']}">services</i></div></div>
<div class="abs" style="left:200px;right:200px;bottom:300px">{rows}
 <div class="caps" style="font-size:28px;color:{C['mute']};padding-top:72px;border-top:2px solid #DCC8C2">Residences · Villas · Workspaces</div></div>""", C["blush"])
    steps = [("Listen", "Your way of living, your brief, your site."), ("Concept", "Mood, palette and a clear spatial idea."),
             ("Plan", "Layouts, circulation and furniture placement."), ("Design", "Materials, lighting, bespoke pieces and 3D views."),
             ("Detail", "Drawings and specifications for the makers.")]
    srows = "".join(f'<div style="display:grid;grid-template-columns:92px 420px 1fr;gap:40px;align-items:baseline;padding:48px 0;border-top:2px solid #DCC8C2">'
                    f'<span class="serif" style="font-size:56px;color:{C["bordeaux"]}">0{k + 1}</span>'
                    f'<span class="serif" style="font-size:88px">{t}</span>'
                    f'<span style="font-size:36px;line-height:1.5;color:{C["mute"]}">{d}</span></div>' for k, (t, d) in enumerate(steps))
    s2 = page(f"""<div class="abs" style="left:200px;right:200px;top:240px">{kicker("Our process", C['bordeaux'])}
 <div class="serif" style="font-size:176px;line-height:1;margin-top:60px">From brief <i style="color:{C['bordeaux']}">to detail</i></div></div>
<div class="abs" style="left:200px;right:200px;bottom:300px">{srows}</div>
<div class="word abs" style="right:200px;bottom:170px;font-size:40px;margin-right:-.42em">KAÏRA</div>""", C["blush"])
    return [slide(s1), slide(s2)]


# ------------------------------------------------------------------ les 12 publications (ordre de publication)
def posts():
    k = lambda t: kicker(t)
    return [
        ("01-manifesto", [manifesto()]),
        ("02-villa-living-room", [cover_below("07", k("Villa · Ground floor"), "Living room", C["olive"], "02"),
                                  inner("12", "Villa · Living room", "2 / 3"), inner("08", "Villa · Living room", "3 / 3")]),
        ("03-brand-palette", [palette()]),
        ("04-villa-master-bedroom", [cover_above("05", k("Villa · First floor"), "Master bedroom", C["bordeaux"], "04"),
                                     material_notes()]),
        ("05-our-belief", [belief()]),
        ("06-villa-guest-bedroom", [cover_below("06", k("Villa · Ground floor"), "Guest bedroom", C["olive"], "06")]),
        ("07-our-approach", [approach()]),
        ("08-villa-dining-room", [cover_above("09", k("Villa · Ground floor"), "Dining room", C["bordeaux"], "08")]),
        ("09-the-detail", [detail()]),
        ("10-villa-lounge", [cover_below("04", k("Villa · First floor"), "Lounge", C["bordeaux"], "10"),
                             inner("02", "Villa · First-floor lounge", "2 / 3"), inner("01", "Villa · First-floor lounge", "3 / 3")]),
        ("11-our-services", services()),
        ("12-selected-projects", [cover_wide("13", k("Selected projects"), f"Residences <i style='color:{C['olive']}'>&amp; workspaces</i>",
                                             "Light-filled living spaces and executive offices.", C["olive"], "12"),
                                  inner("14", "Selected projects · Executive office", "2 / 2")]),
    ]


def grid_order(names):
    """Profil Instagram : la publication la plus récente en haut à gauche, 3 colonnes."""
    rev = names[::-1]
    return [rev[i:i + 3] for i in range(0, len(rev), 3)]


def main():
    B.mkdir(parents=True, exist_ok=True)
    shutil.copytree(FONTS, B / "fonts", dirs_exist_ok=True)
    hd_dir, ig_dir = OUT / "hd-2160x2700", OUT / "instagram-1080x1350"
    plan, jobs = [], []
    P = posts()
    for name, slides in P:
        for d in (hd_dir, ig_dir):
            (d / name).mkdir(parents=True, exist_ok=True)
        for i, s in enumerate(slides, 1):
            h = B / f"{name}-{i}.html"
            h.write_text(s["html"], encoding="utf-8")
            bg = B / f"{name}-{i}.bg.png"
            jobs.append([str(h), str(bg)])
            plan.append((name, i, s["imgs"], bg))
    (B / "jobs.json").write_text(json.dumps({"w": W, "h": H, "jobs": jobs}))
    subprocess.run(["node", str(ROOT / "tools/shoot.js"), str(B / "jobs.json")], check=True)
    report = []
    for name, i, imgs, bg in plan:
        canvas = Image.open(bg).convert("RGB")
        notes = []
        for n, x, y, w in imgs:
            src = original(n)
            if w == src.width:
                canvas.paste(src, (x, y))
                same = np.array_equal(np.asarray(canvas)[y:y + src.height, x:x + src.width], np.asarray(src))
                assert same, f"{name}-{i}: rendu {n} modifié"
                notes.append(f"rendu {n} entier à 100 % ({src.width} × {src.height}), identique à l'original")
            else:
                assert w < src.width, "jamais d'agrandissement"
                hh = round(src.height * w / src.width)
                canvas.paste(src.resize((w, hh), Image.LANCZOS), (x, y))
                notes.append(f"rendu {n} entier, réduit à {w / src.width:.0%} (proportions conservées, sans recadrage)")
        canvas.save(hd_dir / name / f"{name}-{i}.png", icc_profile=SRGB, optimize=True)
        canvas.resize((1080, 1350), Image.LANCZOS).save(ig_dir / name / f"{name}-{i}.png", icc_profile=SRGB, optimize=True)
        report.append(f"{name}-{i} : " + ("; ".join(notes) if notes else "visuel graphique (aucun rendu)"))
    (OUT / "verification.txt").write_text(
        "HD 2160 × 2700 : rendus collés tels quels. Instagram 1080 × 1350 : la slide HD entière réduite de moitié.\n\n"
        + "\n".join(report) + "\n")
    # grille de prévisualisation (tuiles 3:4 comme le profil)
    rows = grid_order([n for n, _ in P])
    tw, th, gap = 360, 480, 4
    grid = Image.new("RGB", (3 * tw + 2 * gap, len(rows) * th + (len(rows) - 1) * gap), "#FFFFFF")
    cw = int(H * 3 / 4)
    for r, row in enumerate(rows):
        for c, name in enumerate(row):
            im = Image.open(hd_dir / name / f"{name}-1.png").convert("RGB")
            im = im.crop(((W - cw) // 2, 0, (W - cw) // 2 + cw, H)).resize((tw, th), Image.LANCZOS)
            grid.paste(im, (c * (tw + gap), r * (th + gap)))
    grid.save(OUT / "apercu-grille-12.jpg", quality=92)
    print("\n".join(report))


if __name__ == "__main__":
    main()
