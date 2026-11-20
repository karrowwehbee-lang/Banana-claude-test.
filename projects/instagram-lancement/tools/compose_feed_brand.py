"""KAÏRA — feed de marque en 12 publications : 3 publications avec les rendus du studio, 9 publications de marque
(présentation, palette, signature, citation, conseils, services, promesse, contact).

Rendus : toujours entiers, jamais recadrés, retouchés ni agrandis (collés à 100 % dans les slides HD).
Slides HD 2160 × 2700 ; version Instagram 1080 × 1350 = slide HD réduite de moitié.
Usage : python3 tools/compose_feed_brand.py
"""
import json, pathlib, shutil, subprocess, sys
import numpy as np
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import compose_feed12 as base  # gabarits communs (typographie, couvertures, palette, services…)
from compose_feed12 import W, H, M, C, CSS, SRGB, page, brand, kicker, slide, original

ROOT = base.ROOT
B = ROOT / "build/feed-brand"
OUT = ROOT / "livrables/feed-marque"

COL = dict(olive="#6B7350", bordeaux="#7A2B38", sand="#DCC7A9", ink_on_dark="#F7F3EC",
           olive_soft="#D6D8C2", bordeaux_soft="#E6C6CA", sand_ink="#7A5A3E")


def statement(bg, kick, title, body, foot="", ink=None, accent=None, kick_color=None, body_color=None):
    ink = ink or C["choc"]
    return slide(page(f"""<div class="abs" style="left:200px;right:200px;top:240px;color:{ink}">
 <div class="caps" style="font-size:30px;color:{kick_color or C['oak']}">{kick}</div>
 <div class="serif" style="font-size:168px;line-height:1.03;margin-top:70px">{title}</div></div>
<div class="abs" style="left:200px;right:200px;bottom:330px;color:{ink}">
 <div style="width:144px;height:4px;background:{accent or C['oak']};margin-bottom:70px"></div>
 <div style="font-size:42px;line-height:1.6;color:{body_color or ink};max-width:1560px">{body}</div>
 {f'<div class="caps" style="font-size:26px;margin-top:70px;color:{kick_color or C["oak"]}">{foot}</div>' if foot else ''}</div>
<div class="word abs" style="right:200px;bottom:190px;font-size:44px;margin-right:-.42em;color:{ink}">KAÏRA</div>""", bg))


def who_we_are():
    return statement(COL["olive"], "Who we are",
                     f"An interior architecture studio <i style='color:{COL['olive_soft']}'>devoted to calm</i>",
                     "KAÏRA designs residences, villas and workspaces where light, proportion and honest materials come first. "
                     "Each project is drawn from the way you live, then detailed with care, from the first sketch to the last bespoke piece.",
                     "Interior design · Space planning · Bespoke furniture",
                     ink=COL["ink_on_dark"], accent=COL["olive_soft"], kick_color=COL["olive_soft"], body_color="#E9E8DA")


def signature():
    items = [("Layered light", "Daylight first, then hidden lines of warm light in ceilings, niches and joinery."),
             ("Stone &amp; wood", "Veined marbles, natural oak and dark woods, chosen to age with grace."),
             ("Bespoke joinery", "Libraries, wall panels and furniture drawn for one place only."),
             ("Art at the heart", "Every room is composed around one strong piece.")]
    rows = "".join(f'<div style="display:grid;grid-template-columns:92px 1fr;gap:40px;padding:54px 0;border-top:2px solid {C["line"]}">'
                   f'<div class="serif" style="font-size:56px;color:{C["bordeaux"]}">0{k + 1}</div>'
                   f'<div><div class="serif" style="font-size:92px">{t}</div>'
                   f'<div style="font-size:38px;line-height:1.5;color:{C["mute"]};margin-top:12px">{d}</div></div></div>'
                   for k, (t, d) in enumerate(items))
    return slide(page(f"""<div class="abs" style="left:200px;right:200px;top:240px">{kicker("The KAÏRA signature")}
 <div class="serif" style="font-size:150px;line-height:1.02;margin-top:60px">Four constants <i style="color:{C['bordeaux']}">in every project</i></div></div>
<div class="abs" style="left:200px;right:200px;bottom:230px">{rows}</div>""", C["cream"]))


def quote():
    return slide(page(f"""<div class="abs" style="left:220px;right:220px;top:520px;text-align:center;color:{COL['ink_on_dark']}">
 <div class="serif" style="font-size:360px;line-height:.5;color:{COL['bordeaux_soft']}">&ldquo;</div>
 <div class="serif" style="font-size:176px;line-height:1.06;margin-top:80px">True luxury is a space <i style="color:{COL['bordeaux_soft']}">that lets you breathe.</i></div>
 <div style="width:144px;height:4px;background:{COL['bordeaux_soft']};margin:110px auto 60px"></div>
 <div class="caps" style="font-size:30px;color:{COL['bordeaux_soft']}">KAÏRA Interior Design</div></div>""", COL["bordeaux"]))


TIPS = [("Start with light", "Plan daylight first, then add warm, indirect layers of light: ceiling coves, lit niches, joinery."),
        ("Limit the palette", "Three calm base tones and a single accent are enough to give a room its character."),
        ("Choose honest materials", "Stone, solid wood, linen and wool age beautifully. They make a space feel lasting."),
        ("Hide what you don't need to see", "Flush doors, integrated storage and concealed lighting free the eye and the mind."),
        ("Give art a wall of its own", "One strong piece, well lit and with space around it, does more than ten small ones.")]


def tips():
    cover = slide(page(f"""<div class="abs" style="left:200px;right:200px;top:240px">{kicker("Design notes", C['olive'])}</div>
<div class="abs" style="left:200px;right:200px;top:760px">
 <div class="serif" style="font-size:520px;line-height:.8;color:{C['olive']}">5</div>
 <div class="serif" style="font-size:176px;line-height:1.02;margin-top:150px">keys to a <i style="color:{C['olive']}">calm interior</i></div></div>
<div class="caps abs" style="left:200px;bottom:230px;font-size:28px;color:#6E7262">Swipe &nbsp;→</div>
<div class="word abs" style="right:200px;bottom:220px;font-size:44px;margin-right:-.42em">KAÏRA</div>""", C["sage"]))
    out = [cover]
    for k, (t, d) in enumerate(TIPS, 1):
        out.append(slide(page(f"""<div class="abs" style="left:200px;right:200px;top:240px">{kicker(f"Design notes · {k} / 5", C['olive'])}</div>
<div class="abs" style="left:200px;right:200px;top:700px">
 <div class="serif" style="font-size:300px;line-height:.8;color:{C['olive']}">0{k}</div>
 <div class="serif" style="font-size:150px;line-height:1.04;margin-top:80px">{t}</div>
 <div style="width:144px;height:4px;background:{C['olive']};margin:90px 0 70px"></div>
 <div style="font-size:46px;line-height:1.6;color:#5E6252;max-width:1500px">{d}</div></div>
<div class="word abs" style="right:200px;bottom:220px;font-size:44px;margin-right:-.42em">KAÏRA</div>""", C["sage"])))
    return out


def project_sheet(kick, title, text, materials, chips):
    li = "".join(f'<div style="padding:30px 0;border-top:2px solid {C["line"]};font-size:40px">{m}</div>' for m in materials)
    ch = "".join(f'<div><div style="height:220px;background:{h};border:2px solid {C["line"]}"></div>'
                 f'<div class="serif" style="font-size:36px;margin-top:18px">{n}</div></div>' for n, h in chips)
    return slide(page(f"""<div class="abs" style="left:200px;right:200px;top:220px">{kicker(kick)}
 <div class="serif" style="font-size:150px;line-height:1;margin-top:40px">{title}</div>
 <div style="font-size:42px;line-height:1.6;color:{C['walnut']};margin-top:60px;max-width:1650px">{text}</div></div>
<div class="abs" style="left:200px;right:200px;top:1290px">
 <div class="caps" style="font-size:26px;color:{C['mute']};margin-bottom:20px">Key elements</div>{li}</div>
<div class="abs" style="left:200px;right:200px;bottom:250px;display:grid;grid-template-columns:repeat(4,1fr);gap:40px">{ch}</div>""", C["ivory"]))


def promise():
    items = ["Your space visualised in 3D before anything is built",
             "Bespoke pieces designed for your home only",
             "Materials and lighting chosen with you",
             "A calm, structured process from brief to detail"]
    rows = "".join(f'<div style="display:grid;grid-template-columns:92px 1fr;gap:40px;padding:50px 0;border-top:2px solid #C6AD8C">'
                   f'<span class="serif" style="font-size:56px;color:{COL["sand_ink"]}">0{k + 1}</span>'
                   f'<span class="serif" style="font-size:80px;line-height:1.1">{t}</span></div>' for k, t in enumerate(items))
    return slide(page(f"""<div class="abs" style="left:200px;right:200px;top:240px">{kicker("Working with KAÏRA", COL['sand_ink'])}
 <div class="serif" style="font-size:176px;line-height:1;margin-top:60px">What you <i style="color:{COL['sand_ink']}">can expect</i></div></div>
<div class="abs" style="left:200px;right:200px;bottom:300px">{rows}</div>
<div class="word abs" style="right:200px;bottom:180px;font-size:44px;margin-right:-.42em">KAÏRA</div>""", COL["sand"]))


def contact():
    return slide(page(f"""<div class="abs" style="inset:140px;border:3px solid rgba(247,243,236,.35)"></div>
<div class="abs" style="left:0;right:0;top:560px;text-align:center;color:{COL['ink_on_dark']}">
 <div class="caps" style="font-size:30px;color:{COL['olive_soft']}">Your project</div>
 <div class="serif" style="font-size:200px;line-height:1.02;margin-top:80px">Let's design<br><i style="color:{COL['olive_soft']}">your space</i></div>
 <div style="width:144px;height:4px;background:{COL['olive_soft']};margin:110px auto 80px"></div>
 <div style="font-size:44px;line-height:1.6;color:#E9E8DA">Residences · Villas · Workspaces<br>Send us a message to begin.</div></div>
<div class="abs" style="left:0;right:0;bottom:300px;text-align:center;color:{COL['ink_on_dark']}">
 <div class="word" style="font-size:72px;margin-right:-.42em">KAÏRA</div>
 <div class="caps" style="font-size:24px;margin-top:16px;color:{COL['olive_soft']}">Interior Design</div></div>""", COL["olive"]))


def posts():
    k = lambda t: kicker(t)
    living = project_sheet("Featured project · Villa", "Living room",
                           "A reception room composed around art, where cream panels, lit wood columns and a continuous cove of warm light set a calm, gallery-like rhythm.",
                           ["Cream wall panels with fine shadow gaps", "Vertical wood columns with integrated light",
                            "Low modular sofas in taupe leather and cream", "Large line drawing as the focal point"],
                           [("Cream", "#EFE7DA"), ("Natural oak", "#B58B62"), ("Taupe", "#6F6259"), ("Charcoal", "#2E2A27")])
    dining = project_sheet("Featured project · Villa", "Dining room",
                           "Receiving under a line of light: a long pale stone table, bouclé chairs on dark wood frames and a deep bordeaux artwork that gives the room its character.",
                           ["Pale stone table on a fluted dark base", "Eight chairs in bouclé and dark wood",
                            "Sculptural pendant drawing a free line of light", "Bordeaux artwork and wood library"],
                           [("Pale stone", "#D8CBB6"), ("Ivory bouclé", "#EDE6DA"), ("Dark wood", "#3E2E24"), ("Bordeaux", "#7A2B38")])
    return [
        ("01-welcome", [base.manifesto()]),
        ("02-featured-living-room", [base.cover_below("07", k("Featured project · Villa"), "Living room", C["olive"], "02"), living]),
        ("03-who-we-are", [who_we_are()]),
        ("04-brand-palette", [base.palette()]),
        ("05-the-kaira-signature", [signature()]),
        ("06-featured-master-bedroom", [base.cover_above("05", k("Featured project · Villa"), "Master bedroom", C["bordeaux"], "06"),
                                        base.material_notes()]),
        ("07-quote", [quote()]),
        ("08-design-notes", tips()),
        ("09-our-services", base.services()),
        ("10-featured-dining-room", [base.cover_below("09", k("Featured project · Villa"), "Dining room", C["bordeaux"], "10"), dining]),
        ("11-what-you-can-expect", [promise()]),
        ("12-lets-design-your-space", [contact()]),
    ]


def main():
    B.mkdir(parents=True, exist_ok=True)
    shutil.copytree(base.FONTS, B / "fonts", dirs_exist_ok=True)
    hd_dir, ig_dir = OUT / "hd-2160x2700", OUT / "instagram-1080x1350"
    P, plan, jobs = posts(), [], []
    for name, slides in P:
        for d in (hd_dir, ig_dir):
            (d / name).mkdir(parents=True, exist_ok=True)
        for i, s in enumerate(slides, 1):
            h = B / f"{name}-{i}.html"
            h.write_text(s["html"], encoding="utf-8")
            jobs.append([str(h), str(B / f"{name}-{i}.bg.png")])
            plan.append((name, i, s["imgs"], B / f"{name}-{i}.bg.png"))
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
                assert np.array_equal(np.asarray(canvas)[y:y + src.height, x:x + src.width], np.asarray(src)), name
                notes.append(f"rendu {n} entier à 100 %, identique à l'original")
            else:
                assert w < src.width
                canvas.paste(src.resize((w, round(src.height * w / src.width)), Image.LANCZOS), (x, y))
                notes.append(f"rendu {n} entier, réduit à {w / src.width:.0%} (sans recadrage)")
        canvas.save(hd_dir / name / f"{name}-{i}.png", icc_profile=SRGB, optimize=True)
        canvas.resize((1080, 1350), Image.LANCZOS).save(ig_dir / name / f"{name}-{i}.png", icc_profile=SRGB, optimize=True)
        report.append(f"{name}-{i} : " + ("; ".join(notes) if notes else "visuel de marque (aucun rendu)"))
    (OUT / "verification.txt").write_text("\n".join(report) + "\n")
    rows = base.grid_order([n for n, _ in P])
    tw, th, gap = 360, 480, 4
    grid = Image.new("RGB", (3 * tw + 2 * gap, len(rows) * th + (len(rows) - 1) * gap), "#FFFFFF")
    cw = int(H * 3 / 4)
    for r, row in enumerate(rows):
        for c, name in enumerate(row):
            im = Image.open(hd_dir / name / f"{name}-1.png").convert("RGB")
            grid.paste(im.crop(((W - cw) // 2, 0, (W - cw) // 2 + cw, H)).resize((tw, th), Image.LANCZOS), (c * (tw + gap), r * (th + gap)))
    grid.save(OUT / "apercu-grille.jpg", quality=92)
    print("\n".join(report))


if __name__ == "__main__":
    main()
