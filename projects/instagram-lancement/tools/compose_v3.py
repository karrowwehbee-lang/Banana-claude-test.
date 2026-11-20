"""KAÏRA — feed Instagram v3 (12 publications) : blanc lumineux, olive, bordeaux, chocolat, touches de beige.

7 projets portés par les rendus du studio (entiers, jamais recadrés, retouchés ni agrandis : collés à 100 %
dans les slides HD 2160 × 2700) + 5 publications graphiques. 3 publications épinglées.
Sortie Instagram : 1080 × 1350 (slide HD réduite de moitié).
Usage : python3 tools/compose_v3.py
"""
import json, pathlib, shutil, subprocess, sys
import numpy as np
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import compose_feed12 as base
import compose_final as fin
from compose_feed12 import W, H, M, SRGB, original, size

ROOT = base.ROOT
B = ROOT / "build/v3"
OUT = ROOT / "livrables/instagram-v3"

K = dict(white="#FCFAF7", olive="#5F6A45", burgundy="#6E2234", choc="#3A2A22", beige="#D8C6AC",
         ink="#2E231D", mute="#8A7B6E", line="#E4DACB", ivory="#F7F3EC",
         olive_soft="#D5D9C1", burgundy_soft="#E9C9CF", choc_soft="#D8C6AC")
CSS = base.FACES + f"""
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{font-family:Jost;font-weight:300;position:relative;-webkit-font-smoothing:antialiased}}
.serif{{font-family:Cormorant;font-weight:300}} i{{font-family:Cormorant;font-weight:300;font-style:italic}}
.caps{{font-family:Jost;font-weight:400;text-transform:uppercase;letter-spacing:.34em}}
.word{{font-family:Cormorant;font-weight:400;letter-spacing:.42em}} .abs{{position:absolute}}
"""


def page(body, bg, ink):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body style="background:{bg};color:{ink}">{body}</body></html>'


def sl(html, imgs=()):
    return {"html": html, "imgs": list(imgs)}


THEMES = {  # fond, encre, accent, texte secondaire
    "white": (K["white"], K["ink"], K["burgundy"], K["mute"]),
    "olive": (K["olive"], K["ivory"], K["olive_soft"], "#E3E5D4"),
    "burgundy": (K["burgundy"], K["ivory"], K["burgundy_soft"], "#F0DCDF"),
    "choc": (K["choc"], K["ivory"], K["choc_soft"], "#E6DACB"),
}


def mark(theme, num, right=M, bottom=200, top=None):
    bg, ink, acc, sub = THEMES[theme]
    pos = f"top:{top}px" if top is not None else f"bottom:{bottom}px"
    return (f'<div class="abs" style="right:{right}px;{pos};text-align:right">'
            f'<div style="width:92px;height:3px;background:{acc};margin:0 0 34px auto"></div>'
            f'<div class="word" style="font-size:48px;margin-right:-.42em">KAÏRA</div>'
            f'<div class="caps" style="font-size:22px;color:{sub};margin-top:12px">{num}</div></div>')


def project_cover(n, theme, kick, title, num, layout="below"):
    """Rendu entier à 100 %, titre en bandeau — sur fond blanc, olive, bordeaux ou chocolat."""
    bg, ink, acc, sub = THEMES[theme]
    w, h = size(n)
    x = (W - w) // 2
    if layout == "below":
        y = M
        t = (f'<div class="abs" style="left:{x}px;top:{y + h + 96}px"><div class="caps" style="font-size:30px;color:{acc}">{kick}</div>'
             f'<div class="serif" style="font-size:136px;line-height:1;margin-top:28px">{title}</div></div>' + mark(theme, num, right=x))
    elif layout == "above":
        y = H - M - h
        t = (f'<div class="abs" style="left:{x}px;top:170px"><div class="caps" style="font-size:30px;color:{acc}">{kick}</div>'
             f'<div class="serif" style="font-size:136px;line-height:1;margin-top:28px">{title}</div></div>' + mark(theme, num, right=x, top=190))
    else:  # paysage
        y = M
        t = (f'<div class="abs" style="left:{x}px;right:{x}px;top:{y + h + 130}px"><div class="caps" style="font-size:30px;color:{acc}">{kick}</div>'
             f'<div class="serif" style="font-size:150px;line-height:1.02;margin-top:34px">{title}</div></div>' + mark(theme, num, right=x))
    return sl(page(t, bg, ink), [(n, x, y, w)])


def sheet(kick, title, text, elements, chips, pg):
    bg, ink, acc, sub = THEMES["white"]
    li = "".join(f'<div style="padding:30px 0;border-top:2px solid {K["line"]};font-size:40px">{e}</div>' for e in elements)
    ch = "".join(f'<div><div style="height:220px;background:{h};border:2px solid {K["line"]}"></div>'
                 f'<div class="serif" style="font-size:36px;margin-top:18px">{nm}</div></div>' for nm, h in chips)
    return sl(page(f"""<div class="abs" style="left:200px;right:200px;top:220px"><div class="caps" style="font-size:30px;color:{acc}">{kick}</div>
 <div class="serif" style="font-size:150px;line-height:1;margin-top:40px">{title}</div>
 <div style="font-size:42px;line-height:1.6;color:{sub};margin-top:60px;max-width:1650px">{text}</div></div>
<div class="abs" style="left:200px;right:200px;top:1290px"><div class="caps" style="font-size:26px;color:{sub};margin-bottom:20px">Key elements</div>{li}</div>
<div class="abs" style="left:200px;right:200px;bottom:250px;display:grid;grid-template-columns:repeat(4,1fr);gap:40px">{ch}</div>
<div class="caps abs" style="right:200px;top:230px;font-size:22px;color:{sub}">{pg}</div>""", bg, ink))


def solid(theme, kick, title, body="", foot="", center=False, big=168):
    bg, ink, acc, sub = THEMES[theme]
    al = "text-align:center;" if center else ""
    return sl(page(f"""<div class="abs" style="left:200px;right:200px;top:{960 if center else 260}px;{al}">
 <div class="caps" style="font-size:30px;color:{acc}">{kick}</div>
 <div class="serif" style="font-size:{big}px;line-height:1.04;margin-top:80px">{title}</div>
 {f'<div style="width:144px;height:4px;background:{acc};margin:100px {"auto" if center else "0"} 70px"></div><div style="font-size:44px;line-height:1.6;color:{sub}">{body}</div>' if body else ''}</div>
{f'<div class="caps abs" style="left:200px;right:200px;bottom:300px;{al}font-size:28px;color:{acc}">{foot}</div>' if foot else ''}
<div class="word abs" style="{'left:0;right:0;text-align:center;' if center else 'right:200px;'}bottom:190px;font-size:48px;{'' if center else 'margin-right:-.42em;'}">KAÏRA</div>""", bg, ink))


def numbered(theme, kick, title, rows, size_t=92, pg=""):
    bg, ink, acc, sub = THEMES[theme]
    line = K["line"] if theme == "white" else "rgba(247,243,236,.28)"
    num_c = K["burgundy"] if theme == "white" else acc
    r = "".join(f'<div style="display:grid;grid-template-columns:92px 1fr;gap:40px;padding:50px 0;border-top:2px solid {line}">'
                f'<div class="serif" style="font-size:56px;color:{num_c}">0{k + 1}</div>'
                f'<div><div class="serif" style="font-size:{size_t}px;line-height:1.08">{t}</div>'
                + (f'<div style="font-size:38px;line-height:1.5;color:{sub};margin-top:12px">{d}</div>' if d else "") + '</div></div>'
                for k, (t, d) in enumerate(rows))
    return sl(page(f"""<div class="abs" style="left:200px;right:200px;top:240px"><div class="caps" style="font-size:30px;color:{num_c}">{kick}</div>
 <div class="serif" style="font-size:168px;line-height:1;margin-top:60px">{title}</div></div>
<div class="abs" style="left:200px;right:200px;bottom:290px">{r}</div>
<div class="word abs" style="right:200px;bottom:170px;font-size:44px;margin-right:-.42em">KAÏRA</div>
{f'<div class="caps abs" style="right:200px;top:250px;font-size:22px;color:{sub}">{pg}</div>' if pg else ''}""", bg, ink))


def intro_cover():
    bg, ink, acc, sub = THEMES["white"]
    return sl(page(f"""<div class="abs" style="inset:140px;border:3px solid {K['line']}"></div>
<div class="abs" style="top:430px;left:0;right:0;text-align:center">
 <div class="word" style="font-size:250px;margin-right:-.42em;color:{K['choc']}">KAÏRA</div>
 <div class="caps" style="font-size:38px;margin-top:24px;color:{K['olive']}">Interior Architecture</div></div>
<div class="abs" style="top:1190px;left:0;right:0;text-align:center">
 <div style="width:144px;height:4px;background:{K['burgundy']};margin:0 auto 110px"></div>
 <div class="serif" style="font-size:176px;line-height:1.03">The architecture<br><i style="color:{K['burgundy']}">of calm</i></div></div>
<div class="caps abs" style="bottom:300px;left:0;right:0;text-align:center;font-size:30px;color:{K['mute']}">Residences &nbsp;·&nbsp; Villas &nbsp;·&nbsp; Workspaces</div>""", bg, ink))


def tips_cover():
    bg, ink, acc, sub = THEMES["burgundy"]
    return sl(page(f"""<div class="abs" style="left:200px;right:200px;top:260px"><div class="caps" style="font-size:30px;color:{acc}">Design notes</div></div>
<div class="abs" style="left:200px;right:200px;top:700px">
 <div class="serif" style="font-size:560px;line-height:.8;color:{acc}">5</div>
 <div class="serif" style="font-size:180px;line-height:1.02;margin-top:150px">keys to a <i style="color:{acc}">calm interior</i></div></div>
<div class="caps abs" style="left:200px;bottom:230px;font-size:28px;color:{acc}">Swipe &nbsp;→</div>
<div class="word abs" style="right:200px;bottom:220px;font-size:48px;margin-right:-.42em">KAÏRA</div>""", bg, ink))


def tip(k, t, d):
    bg, ink, acc, sub = THEMES["white"]
    return sl(page(f"""<div class="abs" style="left:200px;right:200px;top:260px"><div class="caps" style="font-size:30px;color:{K['burgundy']}">Design notes · {k} / 5</div></div>
<div class="abs" style="left:200px;right:200px;top:700px">
 <div class="serif" style="font-size:320px;line-height:.8;color:{K['burgundy']}">0{k}</div>
 <div class="serif" style="font-size:150px;line-height:1.04;margin-top:90px">{t}</div>
 <div style="width:144px;height:4px;background:{K['beige']};margin:90px 0 70px"></div>
 <div style="font-size:46px;line-height:1.6;color:{K['mute']};max-width:1500px">{d}</div></div>
<div class="word abs" style="right:200px;bottom:220px;font-size:44px;margin-right:-.42em">KAÏRA</div>""", bg, ink))


def quote():
    bg, ink, acc, sub = THEMES["olive"]
    return sl(page(f"""<div class="abs" style="left:220px;right:220px;top:520px;text-align:center">
 <div class="serif" style="font-size:360px;line-height:.5;color:{acc}">&ldquo;</div>
 <div class="serif" style="font-size:176px;line-height:1.06;margin-top:80px">True luxury is a space <i style="color:{acc}">that lets you breathe.</i></div>
 <div style="width:144px;height:4px;background:{acc};margin:110px auto 60px"></div>
 <div class="caps" style="font-size:30px;color:{acc}">KAÏRA Interior Design</div></div>""", bg, ink))


def palette():
    s = base.palette()
    s["html"] = s["html"].replace("Brand palette", "Our palette").replace(
        "Luminous whites and natural wood as the base; olive and bordeaux as single, deliberate accents.",
        "Luminous white as the base; olive, burgundy and chocolate as deliberate accents; beige as a soft touch.")
    return sl(s["html"])


PALETTE_V3 = [("White", "#FCFAF7"), ("Beige", "#D8C6AC"), ("Natural oak", "#B58B62"),
              ("Olive green", "#5F6A45"), ("Burgundy", "#6E2234"), ("Chocolate", "#3A2A22")]


def palette_v3():
    bg, ink, acc, sub = THEMES["white"]
    big = "".join(f'<div><div style="height:{h}px;background:{c};border:2px solid {K["line"]}"></div>'
                  f'<div class="serif" style="font-size:46px;margin-top:22px">{n}</div>'
                  f'<div class="caps" style="font-size:22px;color:{sub};margin-top:8px">{c}</div></div>'
                  for (n, c), h in zip(PALETTE_V3, [900, 520, 520, 900, 900, 900]))
    return sl(page(f"""<div class="abs" style="left:170px;right:170px;top:200px"><div class="caps" style="font-size:30px;color:{K['olive']}">Our palette</div>
 <div class="serif" style="font-size:150px;line-height:1;margin-top:30px">White light, <i style="color:{K['burgundy']}">deep accents</i></div></div>
<div class="abs" style="left:170px;right:170px;top:720px;display:grid;grid-template-columns:repeat(6,1fr);gap:28px;align-items:end">{big}</div>
<div class="abs" style="left:170px;bottom:200px;font-size:34px;color:{sub};max-width:1400px;line-height:1.5">Luminous white as the base; olive, burgundy and chocolate as deliberate accents; beige as a soft touch.</div>
<div class="word abs" style="right:170px;bottom:200px;font-size:44px;margin-right:-.42em">KAÏRA</div>""", bg, ink))


def contact():
    bg, ink, acc, sub = THEMES["burgundy"]
    return sl(page(f"""<div class="abs" style="inset:140px;border:3px solid rgba(247,243,236,.3)"></div>
<div class="abs" style="left:0;right:0;top:600px;text-align:center">
 <div class="caps" style="font-size:30px;color:{acc}">Your project</div>
 <div class="serif" style="font-size:200px;line-height:1.02;margin-top:80px">Let's design<br><i style="color:{acc}">your space</i></div>
 <div style="width:144px;height:4px;background:{acc};margin:110px auto 80px"></div>
 <div style="font-size:44px;line-height:1.6;color:{sub}">Residences · Villas · Workspaces<br>Send us a message to begin.</div></div>
<div class="word abs" style="left:0;right:0;bottom:300px;text-align:center;font-size:72px">KAÏRA</div>""", bg, ink))


# ------------------------------------------------------------------ les 12 publications (ordre de publication)
def posts():
    who = solid("olive", "Who we are", "An interior architecture studio <i style='color:#D5D9C1'>devoted to calm</i>",
                "KAÏRA designs residences, villas and workspaces where light, proportion and honest materials come first. "
                "Each project is drawn from the way you live, then detailed with care, from the first sketch to the last bespoke piece.",
                "Interior design · Space planning · Bespoke furniture", big=160)
    services = numbered("burgundy", "KAÏRA Interior Design", "Our <i style='color:#E9C9CF'>services</i>",
                        [("Interior design", ""), ("Space planning", ""), ("Bespoke furniture &amp; joinery", ""),
                         ("Materials &amp; lighting", ""), ("3D visualisation", "")], size_t=96)
    expect = numbered("white", "Working with KAÏRA", "What you <i style='color:#6E2234'>can expect</i>",
                      [("Your space visualised in 3D before anything is built", ""), ("Bespoke pieces designed for your home only", ""),
                       ("Materials and lighting chosen with you", ""), ("A calm, structured process from brief to detail", "")], size_t=76, pg="2 / 3")
    process_cover = solid("olive", "Our process", "From brief <i style='color:#D5D9C1'>to detail</i>",
                          "Five steps, one calm and structured path for every project.", "Swipe &nbsp;→", center=True, big=210)
    steps = numbered("white", "Our process", "Five <i style='color:#5F6A45'>steps</i>",
                     [("Listen", "Your way of living, your brief, your site."), ("Concept", "Mood, palette and a clear spatial idea."),
                      ("Plan", "Layouts, circulation and furniture placement."), ("Design", "Materials, lighting, bespoke pieces and 3D views."),
                      ("Detail", "Drawings and specifications for the makers.")], size_t=84, pg="2 / 2")
    tips = [tips_cover()] + [tip(k, t, d) for k, (t, d) in enumerate(fin.brandfeed.TIPS, 1)]
    sheets = dict(
        living=sheet("Featured project · Villa", "Living room",
                     "A reception room composed around art, where cream panels, lit wood columns and a continuous cove of warm light set a calm, gallery-like rhythm.",
                     ["Cream wall panels with fine shadow gaps", "Vertical wood columns with integrated light",
                      "Low modular sofas in taupe leather and cream", "Large line drawing as the focal point"],
                     [("Cream", "#EFE7DA"), ("Natural oak", "#B58B62"), ("Taupe", "#6F6259"), ("Charcoal", "#2E2A27")], "2 / 2"),
        dining=sheet("Featured project · Villa", "Dining room",
                     "Receiving under a line of light: a long pale stone table, bouclé chairs on dark wood frames and a deep burgundy artwork that gives the room its character.",
                     ["Pale stone table on a fluted dark base", "Eight chairs in bouclé and dark wood",
                      "Sculptural pendant drawing a free line of light", "Burgundy artwork and asymmetric wood library"],
                     [("Pale stone", "#D8CBB6"), ("Ivory bouclé", "#EDE6DA"), ("Dark wood", "#3E2E24"), ("Burgundy", "#6E2234")], "2 / 2"),
        entrance=sheet("Featured project", "Entrance",
                       "A welcome drawn in walnut: full-height wood panels cut by fine black lines, a soft arched sideboard and a portrait artwork set against a pale wall.",
                       ["Walnut wall panels with black reveals", "Sideboard with soft arched fronts",
                        "Large marble-effect floor tiles", "Portrait artwork as the focal point"],
                       [("Walnut", "#5A3E2E"), ("Black", "#1E1C1B"), ("Warm grey", "#D5D2CC"), ("White marble", "#E9E7E3")], "2 / 2"),
        lounge=sheet("Featured project · Villa", "First-floor lounge",
                     "A more intimate living room filled with daylight, where a large red-and-white organic artwork answers the lit wood shelving.",
                     ["Taupe corner sofa and lounge chair", "Oval veined-marble coffee table",
                      "Lit wood shelving, full height", "Cognac leather accents and woven rug"],
                     [("Taupe", "#7A7064"), ("White marble", "#E7E3DD"), ("Natural oak", "#B58B62"), ("Red", "#A8352F")], "2 / 2"),
        openplan=sheet("Featured project", "Open-plan living",
                       "Light everywhere: pale floors, cream wall panels with fine shadow gaps and low modular sofas, around a white staircase and a graphic artwork in warm earth tones.",
                       ["Large pale floor tiles", "Cream wall panels with shadow gaps",
                        "Low modular sofas in white and grey", "Sideboard with arched fronts"],
                       [("Pale stone", "#E6E2DB"), ("Cream", "#EFE9DF"), ("Grey", "#8E8C88"), ("Terracotta", "#B5643C")], "2 / 2"),
    )
    master_notes = fin.notes_slide("05", 1200, "Material notes", "Master bedroom",
                                   [(440, "Dark veined marble", "Backlit band rising behind the bed"),
                                    (700, "Lit wood slats", "Vertical rhythm, warm hidden light"),
                                    (940, "Glass globe pendants", "Suspended on fine gold rods"),
                                    (1350, "Olive bed linen", "The single note of colour"),
                                    (1700, "Brushed-gold base", "Channel-tufted bench at the foot of the bed")],
                                   "Five materials, one atmosphere: quiet, enveloping and warm.", "2 / 2")
    kitchen_notes = fin.notes_slide("20", 1200, "Material notes", "Kitchen",
                                    [(320, "Ceiling cove of light", "A warm line tracing the whole room"),
                                     (540, "Cream lacquered cabinetry", "Full-height, handle-free, luminous"),
                                     (780, "Veined stone splashback", "The same stone as the island"),
                                     (1000, "Black accents", "Fridge and glass-front tower"),
                                     (1260, "Waterfall stone island", "Seating along white stools"),
                                     (1480, "Light herringbone floor", "Pale wood, laid in chevrons")],
                                    "A bright kitchen built around one stone.", "2 / 2")
    return [
        ("01-kaira", [intro_cover(), who, palette_v3()]),
        ("02-services", [services, expect, contact()]),
        ("03-master-bedroom", [project_cover("05", "choc", "Featured project · Villa", "Master bedroom", "03", "above"), master_notes]),
        ("04-first-floor-lounge", [project_cover("04", "white", "Featured project · Villa", "First-floor lounge", "04"), sheets["lounge"]]),
        ("05-our-process", [process_cover, steps]),
        ("06-open-plan-living", [project_cover("13", "white", "Featured project", "Open-plan living", "06", "wide"), sheets["openplan"]]),
        ("07-dining-room", [project_cover("09", "choc", "Featured project · Villa", "Dining room", "07", "above"), sheets["dining"]]),
        ("08-living-room", [project_cover("07", "white", "Featured project · Villa", "Living room", "08"), sheets["living"]]),
        ("09-design-notes", tips),
        ("10-entrance", [project_cover("21", "white", "Featured project", "Entrance", "10"), sheets["entrance"]]),
        ("11-quote", [quote()]),
        ("12-kitchen", [project_cover("20", "white", "Featured project", "Kitchen", "12"), kitchen_notes]),
    ]


PINNED = ["03-master-bedroom", "01-kaira", "02-services"]   # ordre affiché en haut du profil


def main():
    B.mkdir(parents=True, exist_ok=True)
    shutil.copytree(base.FONTS, B / "fonts", dirs_exist_ok=True)
    posts_dir, hd_dir = OUT / "posts-1080x1350", OUT / "hd-2160x2700"
    for d in (posts_dir, hd_dir):
        if d.exists():
            shutil.rmtree(d)
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
        report.append(f"{name}-{i} : " + ("; ".join(notes) if notes else "visuel graphique"))
    report.append(f"\nRendus utilisés : {len(used)} ({', '.join(sorted(used))}) — entiers, sans recadrage ni retouche")
    (OUT / "verification.txt").write_text("\n".join(report) + "\n")
    # highlights, photo de profil et bio : identiques au kit final
    for sub in ("highlights", "profil"):
        shutil.copytree(ROOT / "livrables/instagram-final" / sub, OUT / sub, dirs_exist_ok=True)
    previews(P)
    print("\n".join(report[-1:]))


def tile(name, tw=360, th=480):
    im = Image.open(OUT / "hd-2160x2700" / name / f"{name}-1.png").convert("RGB")
    cw = int(H * 3 / 4)
    return im.crop(((W - cw) // 2, 0, (W - cw) // 2 + cw, H)).resize((tw, th), Image.LANCZOS)


def previews(P):
    names = [n for n, _ in P]
    order = PINNED + [n for n in names[::-1] if n not in PINNED]
    tw, th, gap = 360, 480, 4
    g = Image.new("RGB", (3 * tw + 2 * gap, 4 * th + 3 * gap), "#FFFFFF")
    for k, name in enumerate(order):
        g.paste(tile(name), ((k % 3) * (tw + gap), (k // 3) * (th + gap)))
    g.save(OUT / "grille-profil.jpg", quality=93)
    g.save(B / "grid.jpg", quality=93)
    hl = sorted((OUT / "highlights").glob("*.png"))
    for f in hl:
        Image.open(f).convert("RGB").crop((0, 420, 1080, 1500)).resize((200, 200), Image.LANCZOS).save(B / f"hlc-{f.stem}.png")
    Image.open(OUT / "profil/photo-de-profil.png").convert("RGB").resize((240, 240), Image.LANCZOS).save(B / "avc.png")
    pins = "".join(f'<div style="position:absolute;left:{(k % 3) * 364 + 334}px;top:5px;width:22px;height:22px;border-radius:50%;background:rgba(255,255,255,.9);'
                   f'font:400 12px Jost;display:flex;align-items:center;justify-content:center;color:#2A211C">&#x1F4CC;</div>' for k in range(3))
    circles = "".join(f'<div style="text-align:center;width:150px"><img src="hlc-{f.stem}.png" style="width:128px;height:128px;border-radius:50%;border:2px solid #E3DDD4;padding:4px;background:#fff">'
                      f'<div style="font:400 20px Jost;margin-top:10px;color:#2A211C">{f.stem.split("-", 1)[1].capitalize()}</div></div>' for f in hl)
    bio = "<br>".join(fin.BIO.splitlines()[1:])
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{base.FACES}*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1088px;background:#fff;font-family:Jost;color:#2A211C}}</style></head><body>
<div style="display:flex;gap:56px;align-items:center;padding:56px 48px 28px">
 <img src="avc.png" style="width:200px;height:200px;border-radius:50%;border:2px solid #E3DDD4">
 <div><div style="font:400 34px Jost">kaira.interiordesign</div>
  <div style="display:flex;gap:46px;margin-top:22px;font:400 24px Jost"><span><b>12</b> posts</span><span><b>—</b> followers</span><span><b>—</b> following</span></div></div></div>
<div style="padding:0 48px 30px;font:300 24px/1.5 Jost"><div style="font-weight:400">KAÏRA Interior Design</div><div style="color:#8A7B6E">Interior designer</div>{bio}</div>
<div style="display:flex;gap:18px;padding:10px 40px 40px">{circles}</div>
<div style="position:relative"><img src="grid.jpg" style="width:1088px;display:block">{pins}</div></body></html>"""
    (B / "profil.html").write_text(html, encoding="utf-8")
    subprocess.run(["node", "-e", f"""
const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage({{ viewport: {{ width: 1088, height: 800 }} }});
 await p.goto('file://{B / "profil.html"}', {{ waitUntil: 'networkidle' }}); await p.evaluate(() => document.fonts.ready);
 await p.screenshot({{ path: '{OUT / "apercu-profil.jpg"}', type: 'jpeg', quality: 92, fullPage: true }}); await b.close(); }})();"""],
                   check=True, cwd=str(ROOT / "tools"))


if __name__ == "__main__":
    main()
