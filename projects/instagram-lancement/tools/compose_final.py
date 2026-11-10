"""KAÏRA — lancement Instagram final : 15 publications, 3 épinglées, 6 couvertures Highlights, photo de profil,
aperçus (grille, grille avec épinglés, profil complet).

Les 21 rendus du studio sont tous intégrés, toujours entiers, jamais recadrés, retouchés ni agrandis
(collés à 100 % dans les slides HD 2160 × 2700 ; les notes de matières montrent un rendu entier réduit).
Version à publier : 1080 × 1350 (slide HD réduite de moitié).
Usage : python3 tools/compose_final.py
"""
import json, pathlib, shutil, subprocess, sys
import numpy as np
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import compose_feed12 as base
import compose_feed_brand as brandfeed
from compose_feed12 import W, H, M, C, CSS, SRGB, page, brand, kicker, slide, original, size
from compose_feed_brand import COL

ROOT = base.ROOT
B = ROOT / "build/final"
OUT = ROOT / "livrables/instagram-final"


# ------------------------------------------------------------------ gabarits supplémentaires
def notes_slide(n, w, kick, title, notes, sentence, pg):
    """Rendu entier (réduit) à gauche, notes alignées sur les éléments, repères hors de l'image."""
    ow, oh = original(n).size
    s = w / ow
    h = round(oh * s)
    x, y = 150, 470
    marks = ""
    for k, (oy, t, d) in enumerate(notes, 1):
        yy = y + oy * s
        marks += (f'<div class="abs" style="left:{x + w + 30}px;top:{yy - 1}px;width:70px;height:2px;background:{C["oak"]}"></div>'
                  f'<div class="abs" style="left:{x + w + 120}px;top:{yy - 34}px;right:120px">'
                  f'<div style="display:flex;gap:24px;align-items:baseline"><span class="serif" style="font-size:34px;color:{C["oak"]}">0{k}</span>'
                  f'<span class="serif" style="font-size:48px;line-height:1.05">{t}</span></div>'
                  f'<div style="font-size:27px;color:{C["mute"]};margin:10px 0 0 62px;line-height:1.4">{d}</div></div>')
    t = (f'<div class="abs" style="left:{x}px;top:170px">{kicker(kick)}'
         f'<div class="serif" style="font-size:118px;line-height:1;margin-top:26px">{title}</div></div>' + marks
         + f'<div class="abs" style="left:{x}px;top:{y + h + 110}px;right:600px;font-size:36px;line-height:1.55;color:{C["mute"]}">{sentence}</div>'
         + f'<div class="abs" style="right:150px;bottom:226px;text-align:right"><div class="word" style="font-size:40px;margin-right:-.42em">KAÏRA</div>'
           f'<div class="caps" style="font-size:22px;color:{C["mute"]};margin-top:10px">{pg}</div></div>')
    return slide(page(t, C["white"]), [(n, x, y, w)])


LIB = [("Stone", "Veined marbles, pale stone and white marble-effect floors.", [("#E9E5DF", "White marble"), ("#D8CBB6", "Pale stone"), ("#3F3A2C", "Dark marble")]),
       ("Wood", "Natural oak, walnut and dark woods for panels, libraries and doors.", [("#B58B62", "Natural oak"), ("#6A4A36", "Walnut"), ("#3E2E24", "Dark wood")]),
       ("Textiles", "Bouclé, linen sheers, wool rugs and soft leathers.", [("#EDE6DA", "Bouclé"), ("#CFC6B8", "Linen"), ("#6F6259", "Taupe leather")]),
       ("Metals &amp; accents", "Brushed gold, black metal and a single note of colour.", [("#B8925A", "Brushed gold"), ("#1E1C1B", "Black metal"), ("#7A2B38", "Bordeaux")])]


def material_library():
    rows = ""
    for name, d, chips in LIB:
        ch = "".join(f'<div style="text-align:center"><div style="width:150px;height:150px;border-radius:50%;background:{h};border:2px solid {C["line"]};margin:0 auto"></div>'
                     f'<div style="font-size:24px;color:{C["mute"]};margin-top:14px">{n}</div></div>' for h, n in chips)
        rows += (f'<div style="display:grid;grid-template-columns:1fr 600px;gap:40px;align-items:center;padding:84px 0;border-top:2px solid {C["line"]}">'
                 f'<div><div class="serif" style="font-size:92px">{name}</div><div style="font-size:36px;line-height:1.5;color:{C["mute"]};margin-top:10px">{d}</div></div>'
                 f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px">{ch}</div></div>')
    return slide(page(f"""<div class="abs" style="left:170px;right:170px;top:170px">{kicker("Materials &amp; textures")}
 <div class="serif" style="font-size:150px;line-height:1;margin-top:30px">The material <i style="color:{C['olive']}">library</i></div></div>
<div class="abs" style="left:170px;right:170px;top:640px">{rows}</div>
<div class="word abs" style="right:170px;bottom:170px;font-size:44px;margin-right:-.42em">KAÏRA</div>""", C["white"]))


def recolor(s, old, new):
    s = dict(s)
    s["html"] = s["html"].replace(f"background:{old}", f"background:{new}")
    return s


def posts():
    k = kicker
    living_sheet = brandfeed.project_sheet(
        "Featured project · Villa", "Living room",
        "A reception room composed around art, where cream panels, lit wood columns and a continuous cove of warm light set a calm, gallery-like rhythm.",
        ["Cream wall panels with fine shadow gaps", "Vertical wood columns with integrated light",
         "Low modular sofas in taupe leather and cream", "Large line drawing as the focal point"],
        [("Cream", "#EFE7DA"), ("Natural oak", "#B58B62"), ("Taupe", "#6F6259"), ("Charcoal", "#2E2A27")])
    dining_sheet = brandfeed.project_sheet(
        "Featured project · Villa", "Dining room",
        "Receiving under a line of light: a long pale stone table, bouclé chairs on dark wood frames and a deep bordeaux artwork that gives the room its character.",
        ["Pale stone table on a fluted dark base", "Eight chairs in bouclé and dark wood",
         "Sculptural pendant drawing a free line of light", "Bordeaux artwork and asymmetric wood library"],
        [("Pale stone", "#D8CBB6"), ("Ivory bouclé", "#EDE6DA"), ("Dark wood", "#3E2E24"), ("Bordeaux", "#7A2B38")])
    entrance_sheet = brandfeed.project_sheet(
        "Featured project", "Entrance",
        "A welcome drawn in walnut: full-height wood panels cut by fine black lines, a soft arched sideboard and a portrait artwork set against a pale wall.",
        ["Walnut wall panels with black reveals", "Sideboard with soft arched fronts",
         "Large marble-effect floor tiles", "Portrait artwork as the focal point"],
        [("Walnut", "#5A3E2E"), ("Black", "#1E1C1B"), ("Warm grey", "#D5D2CC"), ("White marble", "#E9E7E3")])
    master_notes = notes_slide("05", 1200, "Material notes", "Master bedroom",
                               [(440, "Dark veined marble", "Backlit band rising behind the bed"),
                                (700, "Lit wood slats", "Vertical rhythm, warm hidden light"),
                                (940, "Glass globe pendants", "Suspended on fine gold rods"),
                                (1350, "Olive bed linen", "The single note of colour"),
                                (1700, "Brushed-gold base", "Channel-tufted bench at the foot of the bed")],
                               "Five materials, one atmosphere: quiet, enveloping and warm.", "2 / 3")
    kitchen_notes = notes_slide("20", 1200, "Material notes", "Kitchen",
                                [(320, "Ceiling cove of light", "A warm line tracing the whole room"),
                                 (540, "Cream lacquered cabinetry", "Full-height, handle-free, luminous"),
                                 (780, "Veined stone splashback", "The same stone as the island"),
                                 (1000, "Black accents", "Fridge and glass-front tower"),
                                 (1260, "Waterfall stone island", "Seating along white stools"),
                                 (1480, "Light herringbone floor", "Pale wood, laid in chevrons")],
                                "A bright kitchen built around one stone.", "2 / 2")
    services = [recolor(s, C["blush"], C["blush"]) for s in base.services()]
    promise = recolor(brandfeed.promise(), COL["sand"], C["blush"])
    promise["html"] = promise["html"].replace("#C6AD8C", "#DCC8C2").replace(COL["sand_ink"], C["bordeaux"])
    return [
        ("01-welcome", [base.manifesto()]),
        ("02-villa-living-room", [base.cover_below("07", k("Featured project · Villa"), "Living room", C["olive"], "02"),
                                  base.inner("12", "Villa · Living room", "2 / 5"), base.inner("08", "Villa · Living room", "3 / 5"),
                                  base.inner("10", "Villa · Living room", "4 / 5"), living_sheet]),
        ("03-who-we-are", [brandfeed.who_we_are()]),
        ("04-kitchen", [base.cover_below("20", k("Featured project"), "Kitchen", C["olive"], "04"), kitchen_notes]),
        ("05-palette-and-materials", [base.palette(), material_library()]),
        ("06-villa-bedrooms", [base.cover_above("05", k("Featured project · Villa"), "The bedrooms", C["bordeaux"], "06"),
                               master_notes, base.inner("06", "Villa · Guest bedroom", "3 / 3")]),
        ("07-the-kaira-signature", [brandfeed.signature()]),
        ("08-villa-dining-room", [base.cover_above("09", k("Featured project · Villa"), "Dining room", C["bordeaux"], "08"),
                                  base.inner("11", "Villa · Dining room", "2 / 4"), base.inner("18", "Villa · Dining room", "3 / 4"), dining_sheet]),
        ("09-quote", [brandfeed.quote()]),
        ("10-entrance", [base.cover_below("21", k("Featured project"), "Entrance", C["olive"], "10"), entrance_sheet]),
        ("11-design-notes", brandfeed.tips()),
        ("12-villa-lounge", [base.cover_below("04", k("Featured project · Villa"), "First-floor lounge", C["bordeaux"], "12"),
                             base.inner("17", "Villa · First-floor lounge", "2 / 5"), base.inner("02", "Villa · First-floor lounge", "3 / 5"),
                             base.inner("01", "Villa · First-floor lounge", "4 / 5"), base.inner("03", "Villa · First-floor lounge", "5 / 5")]),
        ("13-services", services + [promise]),
        ("14-selected-projects", [base.cover_wide("13", k("Selected projects"), f"Residences <i style='color:{C['olive']}'>&amp; workspaces</i>",
                                                  "Light-filled living spaces, media walls and executive offices.", C["olive"], "14"),
                                  base.inner("19", "Selected projects · Open-plan living", "2 / 5"),
                                  base.inner("14", "Selected projects · Executive office", "3 / 5"),
                                  base.inner("16", "Selected projects · Media wall", "4 / 5"),
                                  base.inner("15", "Selected projects · Media wall", "5 / 5")]),
        ("15-lets-design-your-space", [brandfeed.contact()]),
    ]


PINNED = ["02-villa-living-room", "03-who-we-are", "13-services"]

# ------------------------------------------------------------------ Highlights (1080 × 1920) et photo de profil
ICONS = {
    "about": '<text x="0" y="118" text-anchor="middle" font-family="Cormorant" font-weight="300" font-size="330" fill="{ink}">K</text>',
    "projects": '<path d="M-110 170 V-30 A110 110 0 0 1 110 -30 V170" fill="none" stroke="{ink}" stroke-width="7"/>'
                '<line x1="-170" y1="170" x2="170" y2="170" stroke="{ink}" stroke-width="7"/>',
    "materials": '<rect x="-150" y="-60" width="170" height="170" rx="6" fill="none" stroke="{ink}" stroke-width="7"/>'
                 '<rect x="-80" y="-120" width="170" height="170" rx="6" fill="none" stroke="{ink}" stroke-width="7"/>'
                 '<rect x="-10" y="-180" width="170" height="170" rx="6" fill="none" stroke="{ink}" stroke-width="7"/>',
    "services": '<rect x="-160" y="-160" width="320" height="320" fill="none" stroke="{ink}" stroke-width="7"/>'
                '<path d="M-160 20 H-20 V160 M40 -160 V-40 H160" fill="none" stroke="{ink}" stroke-width="7"/>'
                '<path d="M-20 -40 A60 60 0 0 1 40 20" fill="none" stroke="{ink}" stroke-width="5"/>',
    "process": '<line x1="-150" y1="0" x2="150" y2="0" stroke="{ink}" stroke-width="5"/>'
               '<circle cx="-150" cy="0" r="34" fill="{bg}" stroke="{ink}" stroke-width="7"/><circle cx="0" cy="0" r="34" fill="{bg}" stroke="{ink}" stroke-width="7"/>'
               '<circle cx="150" cy="0" r="34" fill="{ink}" stroke="{ink}" stroke-width="7"/>',
    "contact": '<rect x="-170" y="-115" width="340" height="230" rx="8" fill="none" stroke="{ink}" stroke-width="7"/>'
               '<path d="M-170 -115 L0 30 L170 -115" fill="none" stroke="{ink}" stroke-width="7"/>',
}
HIGHLIGHTS = [("about", "About", COL["olive"], "#F7F3EC"), ("projects", "Projects", C["ivory"], C["choc"]),
              ("materials", "Materials", COL["sand"], C["choc"]), ("services", "Services", C["blush"], C["bordeaux"]),
              ("process", "Process", C["sage"], C["olive"]), ("contact", "Contact", COL["bordeaux"], "#F7F3EC")]


def highlight_html(key, bg, ink):
    icon = ICONS[key].format(ink=ink, bg=bg)
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{base.FACES}*{{margin:0}}html,body{{width:1080px;height:1920px;background:{bg}}}</style></head>'
            f'<body><svg width="1080" height="1920" viewBox="-540 -960 1080 1920">{icon}</svg></body></html>')


def avatar_html():
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}html,body{{width:1080px;height:1080px}}</style></head>'
            f'<body style="background:{C["ivory"]}"><div class="abs" style="inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center">'
            f'<div class="word" style="font-size:190px;margin-right:-.42em">KAÏRA</div>'
            f'<div style="width:90px;height:3px;background:{C["olive"]};margin:34px 0 30px"></div>'
            f'<div class="caps" style="font-size:34px;color:{C["walnut"]}">Interior Design</div></div></body></html>')


BIO = """KAÏRA Interior Design
Interior architecture studio
Residences · Villas · Workspaces
Calm spaces, honest materials, layered light.
Message us to start your project."""


# ------------------------------------------------------------------ construction
def main():
    B.mkdir(parents=True, exist_ok=True)
    shutil.copytree(base.FONTS, B / "fonts", dirs_exist_ok=True)
    posts_dir, hd_dir = OUT / "posts-1080x1350", OUT / "hd-2160x2700"
    P, plan, jobs = posts(), [], []
    for name, slides in P:
        for d in (posts_dir, hd_dir):
            (d / name).mkdir(parents=True, exist_ok=True)
        for i, s in enumerate(slides, 1):
            h = B / f"{name}-{i}.html"
            h.write_text(s["html"], encoding="utf-8")
            jobs.append([str(h), str(B / f"{name}-{i}.bg.png")])
            plan.append((name, i, s["imgs"], B / f"{name}-{i}.bg.png"))
    (B / "jobs.json").write_text(json.dumps({"w": W, "h": H, "jobs": jobs}))
    subprocess.run(["node", str(ROOT / "tools/shoot.js"), str(B / "jobs.json")], check=True)
    # highlights + avatar
    (OUT / "highlights").mkdir(parents=True, exist_ok=True)
    (OUT / "profil").mkdir(parents=True, exist_ok=True)
    hj = []
    for n, (key, label, bg, ink) in enumerate(HIGHLIGHTS, 1):
        f = B / f"hl-{key}.html"
        f.write_text(highlight_html(key, bg, ink), encoding="utf-8")
        hj.append([str(f), str(OUT / "highlights" / f"{n}-{label.lower()}.png")])
    (B / "hl.json").write_text(json.dumps({"w": 1080, "h": 1920, "jobs": hj}))
    subprocess.run(["node", str(ROOT / "tools/shoot.js"), str(B / "hl.json")], check=True)
    (B / "avatar.html").write_text(avatar_html(), encoding="utf-8")
    (B / "av.json").write_text(json.dumps({"w": 1080, "h": 1080, "jobs": [[str(B / "avatar.html"), str(OUT / "profil/photo-de-profil.png")]]}))
    subprocess.run(["node", str(ROOT / "tools/shoot.js"), str(B / "av.json")], check=True)
    (OUT / "profil/bio.txt").write_text(BIO + "\n")
    # collage des rendus + vérification
    report, used = [], set()
    for name, i, imgs, bg in plan:
        canvas = Image.open(bg).convert("RGB")
        notes = []
        for n, x, y, w in imgs:
            src = original(n)
            used.add(n)
            if w == src.width:
                canvas.paste(src, (x, y))
                assert np.array_equal(np.asarray(canvas)[y:y + src.height, x:x + src.width], np.asarray(src)), name
                notes.append(f"rendu {n} entier à 100 %, identique à l'original")
            else:
                assert w < src.width
                canvas.paste(src.resize((w, round(src.height * w / src.width)), Image.LANCZOS), (x, y))
                notes.append(f"rendu {n} entier, réduit à {w / src.width:.0%} (sans recadrage)")
        canvas.save(hd_dir / name / f"{name}-{i}.png", icc_profile=SRGB, optimize=True)
        canvas.resize((1080, 1350), Image.LANCZOS).save(posts_dir / name / f"{name}-{i}.png", icc_profile=SRGB, optimize=True)
        report.append(f"{name}-{i} : " + ("; ".join(notes) if notes else "visuel de marque"))
    all_renders = sorted(p.stem for p in (ROOT / "sources/recus").glob("*.*") if p.suffix in (".png", ".jpg"))
    missing = [r for r in all_renders if r not in used]
    report.append(f"\nRendus intégrés : {len(used)} / {len(all_renders)}" + (f" — manquants : {missing}" if missing else " (tous)"))
    (OUT / "verification.txt").write_text("\n".join(report) + "\n")
    previews(P)
    print("\n".join(report[-3:]))


def tile(name, tw=360, th=480):
    im = Image.open(OUT / "hd-2160x2700" / name / f"{name}-1.png").convert("RGB")
    cw = int(H * 3 / 4)
    return im.crop(((W - cw) // 2, 0, (W - cw) // 2 + cw, H)).resize((tw, th), Image.LANCZOS)


def grid_image(order, tw=360, th=480, gap=4):
    rows = [order[i:i + 3] for i in range(0, len(order), 3)]
    g = Image.new("RGB", (3 * tw + 2 * gap, len(rows) * th + (len(rows) - 1) * gap), "#FFFFFF")
    for r, row in enumerate(rows):
        for c, name in enumerate(row):
            g.paste(tile(name, tw, th), (c * (tw + gap), r * (th + gap)))
    return g


def previews(P):
    names = [n for n, _ in P]
    newest_first = names[::-1]
    grid_image(newest_first).save(OUT / "apercu-grille.jpg", quality=92)
    pinned_order = PINNED + [n for n in newest_first if n not in PINNED]
    grid_image(pinned_order).save(OUT / "apercu-grille-avec-epingles.jpg", quality=92)
    # profil complet (aperçu) : en-tête, bio, highlights, grille avec épinglés
    hl = sorted((OUT / "highlights").glob("*.png"))
    for f in hl:
        im = Image.open(f).convert("RGB")
        im.crop((0, 420, 1080, 1500)).resize((200, 200), Image.LANCZOS).save(B / f"hlc-{f.stem}.png")
    Image.open(OUT / "profil/photo-de-profil.png").convert("RGB").resize((240, 240), Image.LANCZOS).save(B / "avc.png")
    grid_image(pinned_order, 360, 480, 4).save(B / "grid-prev.jpg", quality=92)
    circles = "".join(f'<div style="text-align:center;width:150px"><img src="hlc-{f.stem}.png" style="width:128px;height:128px;border-radius:50%;border:2px solid #E3DDD4;padding:4px;background:#fff">'
                      f'<div style="font:400 20px Jost;margin-top:10px;color:#2A211C">{f.stem.split("-", 1)[1].capitalize()}</div></div>' for f in hl)
    bio = "<br>".join(BIO.splitlines()[1:])
    stats = len(P)
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{base.FACES}*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1088px;background:#fff;font-family:Jost;color:#2A211C}}</style></head><body>
<div style="display:flex;gap:56px;align-items:center;padding:56px 48px 28px">
 <img src="avc.png" style="width:200px;height:200px;border-radius:50%;border:2px solid #E3DDD4">
 <div><div style="font:400 34px Jost">kaira.interiordesign</div>
  <div style="display:flex;gap:46px;margin-top:22px;font:400 24px Jost"><span><b>{stats}</b> posts</span><span><b>—</b> followers</span><span><b>—</b> following</span></div></div></div>
<div style="padding:0 48px 30px;font:300 24px/1.5 Jost"><div style="font-weight:400">KAÏRA Interior Design</div><div style="color:#8C7C6E">Interior designer</div>{bio}</div>
<div style="display:flex;gap:18px;padding:10px 40px 40px">{circles}</div>
<img src="grid-prev.jpg" style="width:1088px;display:block"></body></html>"""
    (B / "profil.html").write_text(html, encoding="utf-8")
    (B / "pr.json").write_text(json.dumps({"w": 1088, "h": 600, "jobs": []}))
    subprocess.run(["node", "-e", f"""
const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage({{ viewport: {{ width: 1088, height: 800 }} }});
 await p.goto('file://{B / "profil.html"}', {{ waitUntil: 'networkidle' }}); await p.evaluate(() => document.fonts.ready);
 await p.screenshot({{ path: '{OUT / "apercu-profil.jpg"}', type: 'jpeg', quality: 92, fullPage: true }}); await b.close(); }})();"""],
                   check=True, cwd=str(ROOT / "tools"))


if __name__ == "__main__":
    main()
