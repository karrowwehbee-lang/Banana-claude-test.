"""KAÏRA — Instagram Stories for the 6 Highlights (1080 × 1920).

Reuses the 29 feed visuals of `livrables/instagram-v3` (read only, never modified): each one is placed whole,
scaled proportionally, in an editorial Story frame. Adds an opening slide per Highlight and two Contact slides.
Text stays inside Instagram's safe zone (y 270–1680). Output: livrables/stories-highlights/<n-highlight>/NN.png
Usage: python3 tools/compose_stories.py
"""
import json, pathlib, shutil, subprocess, sys
from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import compose_feed12 as base
import compose_final as fin
from compose_feed12 import SRGB

ROOT = base.ROOT
V3 = ROOT / "livrables/instagram-v3"
B = ROOT / "build/stories"
OUT = ROOT / "livrables/stories-highlights"
W2, H2 = 2160, 3840                       # rendu typographique en 2x, réduit à 1080 × 1920
PW, PH, PX, PY = 920, 1150, 80, 380       # visuel du feed dans la story (taille finale)

INK, MUTE, LINE, WHITE = "#2E231D", "#8A7B6E", "#E4DACB", "#FCFAF7"
HL = {  # même couleurs que les couvertures Highlights existantes
    "about": ("#6B7350", "#F7F3EC", "#D5D9C1"), "projects": ("#F7F3EC", "#3A2A22", "#A9825C"),
    "materials": ("#DCC7A9", "#3A2A22", "#7A5A3E"), "services": ("#F4EAE6", "#6E2234", "#6E2234"),
    "process": ("#E8E9DD", "#5F6A45", "#5F6A45"), "contact": ("#7A2B38", "#F7F3EC", "#E9C9CF"),
}
CSS = base.FACES + f"""*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:{W2}px;height:{H2}px;overflow:hidden}}
body{{font-family:Jost;font-weight:300;position:relative;-webkit-font-smoothing:antialiased}}
.serif{{font-family:Cormorant;font-weight:300}} i{{font-family:Cormorant;font-weight:300;font-style:italic}}
.caps{{font-family:Jost;font-weight:400;text-transform:uppercase;letter-spacing:.34em}}
.word{{font-family:Cormorant;font-weight:400;letter-spacing:.42em}} .abs{{position:absolute}}"""


def page(body, bg, ink):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body style="background:{bg};color:{ink}">{body}</body></html>'


def v3(name):
    """Chemin d'un visuel du feed v3 (posts ou slides complémentaires des épinglés)."""
    post = name.rsplit("-", 1)[0]
    p = V3 / "posts-1080x1350" / post / f"{name}.png"
    return p if p.exists() else V3 / "epingles/slides-complementaires" / f"{name}.png"


# ------------------------------------------------------------------ gabarits
def framed(label, k, n, line, accent):
    """Fond blanc lumineux : en-tête KAÏRA + Highlight, visuel du feed au centre, ligne de texte dessous."""
    return page(f"""<div class="abs" style="left:160px;right:160px;top:560px;display:flex;justify-content:space-between;align-items:center">
 <div class="word" style="font-size:52px;margin-right:-.42em">KAÏRA</div>
 <div class="caps" style="font-size:30px;color:{MUTE}">{label} &nbsp;·&nbsp; {k:02d} / {n:02d}</div></div>
<div class="abs" style="left:{PX * 2 - 2}px;top:{PY * 2 - 2}px;width:{PW * 2 + 4}px;height:{PH * 2 + 4}px;border:2px solid {LINE}"></div>
<div class="abs" style="left:160px;right:160px;top:{(PY + PH) * 2 + 90}px">
 <div style="width:96px;height:4px;background:{accent};margin-bottom:44px"></div>
 <div class="serif" style="font-size:76px;line-height:1.15">{line}</div></div>""", WHITE, INK)


def opener(key, title, sub, items=()):
    bg, ink, acc = HL[key]
    icon = fin.ICONS[key].format(ink=ink, bg=bg)
    li = "".join(f'<div style="padding:30px 0;border-top:2px solid {acc}55;font-size:46px">{t}</div>' for t in items)
    return page(f"""<div class="abs" style="left:0;right:0;top:640px;text-align:center"><div class="word" style="font-size:64px;margin-right:-.42em">KAÏRA</div></div>
<div class="abs" style="left:0;right:0;top:900px;display:flex;justify-content:center">
 <svg width="560" height="560" viewBox="-240 -240 480 480">{icon}</svg></div>
<div class="abs" style="left:200px;right:200px;top:1560px;text-align:center">
 <div class="caps" style="font-size:34px;color:{acc}">{key.upper()}</div>
 <div class="serif" style="font-size:150px;line-height:1.04;margin-top:50px">{title}</div>
 <div style="width:120px;height:4px;background:{acc};margin:80px auto 60px"></div>
 <div style="font-size:46px;line-height:1.55;color:{acc if key != 'contact' else '#F0DCDF'}">{sub}</div>
 {f'<div style="margin-top:90px;text-align:left">{li}<div style="border-top:2px solid {acc}55"></div></div>' if items else ''}</div>
<div class="caps abs" style="left:0;right:0;top:3240px;text-align:center;font-size:28px;color:{acc}">Tap to continue &nbsp;→</div>""", bg, ink)


def contact_brief():
    rows = [("Your project", "Residence, villa or workspace"), ("The spaces", "The rooms you would like us to design"),
            ("Location &amp; timing", "Where the project is, and when you would like to start"),
            ("Inspiration", "A few images of interiors you love")]
    r = "".join(f'<div style="display:grid;grid-template-columns:110px 1fr;gap:30px;padding:46px 0;border-top:2px solid {LINE}">'
                f'<div class="serif" style="font-size:60px;color:#6E2234">0{k + 1}</div>'
                f'<div><div class="serif" style="font-size:84px">{t}</div><div style="font-size:42px;color:{MUTE};margin-top:12px">{d}</div></div></div>'
                for k, (t, d) in enumerate(rows))
    return page(f"""<div class="abs" style="left:160px;right:160px;top:560px;display:flex;justify-content:space-between;align-items:center">
 <div class="word" style="font-size:52px;margin-right:-.42em">KAÏRA</div><div class="caps" style="font-size:30px;color:{MUTE}">Contact &nbsp;·&nbsp; 03 / 04</div></div>
<div class="abs" style="left:200px;right:200px;top:900px">
 <div class="caps" style="font-size:32px;color:#6E2234">Start your project</div>
 <div class="serif" style="font-size:150px;line-height:1.02;margin-top:50px">Send us <i style="color:#6E2234">a message with</i></div>
 <div style="margin-top:110px">{r}<div style="border-top:2px solid {LINE}"></div></div></div>""", WHITE, INK)


def contact_dm():
    bg, ink, acc = HL["contact"]
    return page(f"""<div class="abs" style="left:0;right:0;top:640px;text-align:center"><div class="word" style="font-size:64px;margin-right:-.42em">KAÏRA</div></div>
<div class="abs" style="left:200px;right:200px;top:1180px;text-align:center">
 <div class="caps" style="font-size:34px;color:{acc}">Contact &nbsp;·&nbsp; 04 / 04</div>
 <div class="serif" style="font-size:170px;line-height:1.02;margin-top:60px">We would love<br><i style="color:{acc}">to hear from you</i></div>
 <div style="width:120px;height:4px;background:{acc};margin:90px auto 70px"></div>
 <div style="font-size:48px;line-height:1.6;color:#F0DCDF">Send us a direct message<br>to start your project.</div></div>
<div class="abs caps" style="left:520px;right:520px;top:2700px;height:200px;border:3px solid {acc};border-radius:100px;display:flex;align-items:center;justify-content:center;font-size:34px;color:#F7F3EC">Send a message</div>
<div class="caps abs" style="left:0;right:0;top:3000px;text-align:center;font-size:26px;color:{acc}">Residences &nbsp;·&nbsp; Villas &nbsp;·&nbsp; Workspaces</div>""", bg, ink)


# ------------------------------------------------------------------ contenu des 6 Highlights
def highlights():
    acc = {"about": "#5F6A45", "projects": "#A9825C", "materials": "#7A5A3E", "services": "#6E2234", "process": "#5F6A45", "contact": "#6E2234"}
    H = {
        "1-about": ("about", opener("about", "Meet <i>KAÏRA</i>", "An interior architecture studio<br>for residences, villas and workspaces."), [
            ("01-kaira-1", "The architecture of calm."),
            ("01-kaira-2", "Light, proportion and honest materials come first."),
            ("11-quote-1", "The luxury we design for."),
            ("01-kaira-3", "White light, deep accents: our palette.")]),
        "2-projects": ("projects", opener("projects", "Featured <i>projects</i>", "A selection of our interiors.",
                                          ["Villa · Master bedroom", "Villa · Living room", "Villa · Dining room", "Villa · First-floor lounge",
                                           "Kitchen", "Entrance", "Open-plan living"]), [
            ("03-master-bedroom-1", "Villa — Master bedroom."),
            ("08-living-room-1", "Villa — Living room."),
            ("07-dining-room-1", "Villa — Dining room."),
            ("04-first-floor-lounge-1", "Villa — First-floor lounge."),
            ("12-kitchen-1", "Kitchen."),
            ("10-entrance-1", "Entrance."),
            ("06-open-plan-living-1", "Open-plan living.")]),
        "3-materials": ("materials", opener("materials", "Materials <i>&amp; textures</i>", "Stone, wood, textiles and light:<br>the palette of each project."), [
            ("01-kaira-3", "Our palette: white light, deep accents."),
            ("03-master-bedroom-2", "Material notes — Master bedroom."),
            ("12-kitchen-2", "Material notes — Kitchen."),
            ("08-living-room-2", "Project palette — Living room."),
            ("07-dining-room-2", "Project palette — Dining room."),
            ("04-first-floor-lounge-2", "Project palette — First-floor lounge."),
            ("10-entrance-2", "Project palette — Entrance."),
            ("06-open-plan-living-2", "Project palette — Open-plan living.")]),
        "4-services": ("services", opener("services", "Our <i>services</i>", "From the first idea<br>to the last bespoke piece."), [
            ("02-services-1", "Five services, one studio."),
            ("02-services-2", "What you can expect when working with us."),
            ("02-services-3", "Let's design your space.")]),
        "5-process": ("process", opener("process", "Our <i>process</i>", "How we work, and the ideas<br>that guide every project."), [
            ("05-our-process-1", "From brief to detail."),
            ("05-our-process-2", "Listen, concept, plan, design, detail."),
            ("09-design-notes-1", "Design notes: 5 keys to a calm interior."),
            ("09-design-notes-2", "Design note 01."),
            ("09-design-notes-3", "Design note 02."),
            ("09-design-notes-4", "Design note 03."),
            ("09-design-notes-5", "Design note 04."),
            ("09-design-notes-6", "Design note 05.")]),
        "6-contact": ("contact", opener("contact", "Let's design <i>your space</i>", "Residences · Villas · Workspaces"), [
            ("02-services-3", "Send us a message to begin."),
            ("@brief", None), ("@dm", None)]),
    }
    return H, acc


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    B.mkdir(parents=True, exist_ok=True)
    shutil.copytree(base.FONTS, B / "fonts", dirs_exist_ok=True)
    H, acc = highlights()
    jobs, plan = [], []
    for folder, (key, cover, items) in H.items():
        (OUT / folder).mkdir(parents=True)
        slides = [("@open", cover)] + items
        n = len(slides)
        for k, item in enumerate(slides, 1):
            if item[0] == "@open":
                html, src = item[1], None
            elif item[0] == "@brief":
                html, src = contact_brief(), None
            elif item[0] == "@dm":
                html, src = contact_dm(), None
            else:
                html, src = framed(key.capitalize(), k, n, item[1], acc[key]), v3(item[0])
                assert src.exists(), src
            h = B / f"{folder}-{k:02d}.html"
            h.write_text(html, encoding="utf-8")
            jobs.append([str(h), str(B / f"{folder}-{k:02d}.png")])
            plan.append((folder, k, src, B / f"{folder}-{k:02d}.png", item[0]))
    (B / "jobs.json").write_text(json.dumps({"w": W2, "h": H2, "jobs": jobs}))
    subprocess.run(["node", str(ROOT / "tools/shoot.js"), str(B / "jobs.json")], check=True)
    used, lines = set(), []
    for folder, k, src, bg, ref in plan:
        im = Image.open(bg).convert("RGB").resize((1080, 1920), Image.LANCZOS)
        if src:
            v = Image.open(src).convert("RGB")
            im.paste(v.resize((PW, PH), Image.LANCZOS), (PX, PY))
            used.add(ref)
        im.save(OUT / folder / f"{k:02d}.png", icc_profile=SRGB, optimize=True)
        lines.append((folder, k, ref))
    # copie des couvertures Highlights existantes dans chaque dossier
    covers = sorted((ROOT / "livrables/instagram-final/highlights").glob("*.png"))
    for c in covers:
        folder = next(f for f in H if f.split("-", 1)[0] == c.stem.split("-", 1)[0])
        shutil.copy(c, OUT / folder / "_cover.png")
    all_v = sorted(p.stem for p in (V3 / "posts-1080x1350").glob("*/*.png")) + \
        sorted(p.stem for p in (V3 / "epingles/slides-complementaires").glob("*.png"))
    missing = [v for v in all_v if v not in used]
    (OUT / "_used.json").write_text(json.dumps({"used": sorted(used), "missing": missing, "slides": lines}, indent=1))
    previews(H)
    print(f"{len(lines)} stories · feed visuals used {len(used)}/{len(all_v)}" + (f" · missing {missing}" if missing else ""))


def previews(H):
    """Planche par Highlight + planche générale (aperçu uniquement)."""
    tw, th, gap = 216, 384, 12
    rows = []
    for folder in H:
        files = sorted((OUT / folder).glob("[0-9][0-9].png"))
        cover = Image.open(OUT / folder / "_cover.png").convert("RGB").crop((0, 420, 1080, 1500)).resize((160, 160), Image.LANCZOS)
        row = Image.new("RGB", (220 + len(files) * (tw + gap), th + 70), "#FFFFFF")
        mask = Image.new("L", (160, 160), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, 159, 159), fill=255)
        row.paste(cover, (30, 60), mask)
        d = ImageDraw.Draw(row)
        d.text((60, 240), folder.split("-", 1)[1].upper(), fill="#2E231D")
        for i, f in enumerate(files):
            row.paste(Image.open(f).convert("RGB").resize((tw, th), Image.LANCZOS), (220 + i * (tw + gap), 30))
            d.text((220 + i * (tw + gap), th + 38), f.name, fill="#8A7B6E")
        row.save(OUT / folder / "_apercu.jpg", quality=90)
        rows.append(row)
    wmax = max(r.width for r in rows)
    sheet = Image.new("RGB", (wmax, sum(r.height for r in rows)), "#FFFFFF")
    y = 0
    for r in rows:
        sheet.paste(r, (0, y))
        y += r.height
    sheet.save(OUT / "apercu-stories.jpg", quality=88)


if __name__ == "__main__":
    main()
