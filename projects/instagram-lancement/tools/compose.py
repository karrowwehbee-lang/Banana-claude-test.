"""KAÏRA — compose les 9 publications (HTML -> JPEG 1080 × 1080) et la grille de prévisualisation.
Usage : python3 tools/compose.py   (les visuels Gemini doivent être dans build/raw/)
Les publications typographiques (01, 06) ne dépendent d'aucune image ; la 08 utilise build/raw/08-detail.*"""
import pathlib, shutil, subprocess, json, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
B, RAW, OUT = ROOT / "build", ROOT / "build/raw", ROOT / "livrables/visuels"
FONTS_SRC = ROOT.parent / "dossier-client/build/fonts"

C = {"ivory": "#F7F3EC", "chocolate": "#3B2A22", "walnut": "#5A3E2E", "oak": "#B08A64", "olive": "#5E6B47",
     "bordeaux": "#6E2433", "ink": "#2A211C"}

FONTFACE = "".join(
    f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};src:url(fonts/{f})}}'
    for fam, w, st, f in [("Cormorant", 300, "normal", "cormorant-garamond-latin-300-normal.woff2"),
                          ("Cormorant", 400, "normal", "cormorant-garamond-latin-400-normal.woff2"),
                          ("Cormorant", 300, "italic", "cormorant-garamond-latin-300-italic.woff2"),
                          ("Cormorant", 400, "italic", "cormorant-garamond-latin-400-italic.woff2"),
                          ("Jost", 300, "normal", "jost-latin-300-normal.woff2"),
                          ("Jost", 400, "normal", "jost-latin-400-normal.woff2"),
                          ("Jost", 500, "normal", "jost-latin-500-normal.woff2")])
BASE = FONTFACE + """
*{margin:0;padding:0;box-sizing:border-box} html,body{width:1080px;height:1080px;overflow:hidden}
body{font-family:Jost;font-weight:300;-webkit-font-smoothing:antialiased}
.serif{font-family:Cormorant;font-weight:300}
.caps{font-family:Jost;font-weight:400;text-transform:uppercase;letter-spacing:.32em}
.full{position:absolute;inset:0;background-size:cover;background-position:center}
.tag{position:absolute;left:56px;bottom:50px;color:#fff;font-size:15px;text-shadow:0 1px 14px rgba(0,0,0,.35)}
.tag b{font-family:Cormorant;font-weight:400;font-size:26px;letter-spacing:.42em;margin-right:22px;text-transform:none}
.shade{position:absolute;left:0;right:0;bottom:0;height:300px;background:linear-gradient(transparent,rgba(25,18,14,.42))}
"""


def raw(name):
    hits = sorted(RAW.glob(f"{name}.*g")) + sorted(RAW.glob(f"{name}.webp"))
    return hits[0].name if hits else None


def render_post(label, room):
    def f(img):
        return f"""<div class="full" style="background-image:url(raw/{img})"></div><div class="shade"></div>
<div class="tag caps"><b>KAÏRA</b>{label} · {room}</div>"""
    return f


POSTS = {
 "01-manifeste": dict(bg=C["ivory"], html=f"""
  <div style="position:absolute;inset:64px;border:1.5px solid {C['oak']}"></div>
  <div style="position:absolute;top:150px;left:0;right:0;text-align:center;color:{C['chocolate']}">
    <div class="serif" style="font-size:118px;letter-spacing:.28em;margin-left:.28em;font-weight:400">KAÏRA</div>
    <div class="caps" style="font-size:19px;margin-top:6px;color:{C['walnut']}">Interior Design</div>
  </div>
  <div style="position:absolute;top:470px;left:0;right:0;text-align:center;color:{C['chocolate']}">
    <div style="width:70px;height:2px;background:{C['olive']};margin:0 auto 54px"></div>
    <div class="serif" style="font-size:84px;line-height:1.04">L'architecture<br><i style="color:{C['bordeaux']}">du calme</i></div>
  </div>
  <div class="caps" style="position:absolute;bottom:118px;left:0;right:0;text-align:center;font-size:16px;color:{C['walnut']}">
    Espace &nbsp;·&nbsp; Matière &nbsp;·&nbsp; Lumière</div>""", needs=None),
 "02-salon": dict(bg="#000", html=render_post("Concept", "Salon"), needs="02-salon"),
 "03-matieres": dict(bg="#000", html=lambda img: f"""<div class="full" style="background-image:url(raw/{img})"></div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:150px;background:{C['ivory']};display:flex;align-items:center;justify-content:space-between;padding:0 64px">
   <div class="serif" style="font-size:52px;color:{C['chocolate']}">La palette <i style="color:{C['olive']}">KAÏRA</i></div>
   <div class="caps" style="font-size:14px;color:{C['walnut']};text-align:right;line-height:1.9">Chêne · Noyer · Travertin<br>Marbre · Velours · Laiton</div>
  </div>""", needs="03-matieres"),
 "04-chambre": dict(bg="#000", html=render_post("Concept", "Chambre principale"), needs="04-chambre"),
 "05-cuisine": dict(bg="#000", html=render_post("Concept", "Cuisine"), needs="05-cuisine"),
 "06-services": dict(bg=C["bordeaux"], html=f"""
  <div style="position:absolute;top:96px;left:96px;color:{C['ivory']}">
   <div class="caps" style="font-size:16px;opacity:.75">KAÏRA Interior Design</div>
   <div class="serif" style="font-size:96px;line-height:1;margin-top:26px">Nos <i>services</i></div>
  </div>
  <div style="position:absolute;left:96px;right:96px;bottom:110px;color:{C['ivory']}">
   {''.join(f'<div style="display:flex;align-items:baseline;gap:34px;padding:22px 0;border-top:1px solid rgba(247,243,236,.35)"><span class="serif" style="font-size:30px;opacity:.7;width:44px">{n}</span><span class="serif" style="font-size:42px">{t}</span></div>'
            for n, t in [("01", "Conception d'intérieurs"), ("02", "Plans d'aménagement"), ("03", "Mobilier sur mesure"),
                         ("04", "Matériaux &amp; éclairage"), ("05", "Visualisations 3D")])}
  </div>""", needs=None),
 "07-dressing": dict(bg="#000", html=render_post("Concept", "Dressing sur mesure"), needs="07-dressing"),
 "08-approche": dict(bg=C["chocolate"], html=lambda img: f"""
  <div class="full" style="right:auto;width:470px;background-image:url(raw/{img})"></div>
  <div style="position:absolute;left:540px;top:100px;right:84px;color:{C['ivory']}">
   <div class="caps" style="font-size:15px;color:{C['oak']}">Notre approche</div>
   <div class="serif" style="font-size:74px;line-height:1.02;margin-top:30px">Le détail<br><i style="color:#C9B08E">fait l'espace</i></div>
  </div>
  <div style="position:absolute;left:540px;right:84px;bottom:96px;color:{C['ivory']}">
   {''.join(f'<div style="padding:20px 0;border-top:1px solid rgba(247,243,236,.28)"><div class="serif" style="font-size:34px">{t}</div><div style="font-size:17px;opacity:.72;margin-top:6px;line-height:1.5">{d}</div></div>'
            for t, d in [("Proportion", "des volumes pensés à l'échelle du corps"), ("Matière", "pierre, bois et textiles authentiques"),
                         ("Lumière", "naturelle d'abord, puis sculptée")])}
  </div>""", needs="08-detail"),
 "09-salle-de-bain": dict(bg="#000", html=render_post("Concept", "Salle de bain"), needs="09-salle-de-bain"),
}

# Position dans la grille (ligne, colonne) telle qu'affichée, une fois les 9 publiées (01 = publiée en premier, en bas à droite)
GRID = [["09-salle-de-bain", "08-approche", "07-dressing"],
        ["06-services", "05-cuisine", "04-chambre"],
        ["03-matieres", "02-salon", "01-manifeste"]]


def main():
    shutil.copytree(FONTS_SRC, B / "fonts", dirs_exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    jobs, missing = [], []
    for name, p in POSTS.items():
        img = raw(p["needs"]) if p["needs"] else None
        if p["needs"] and not img:
            missing.append(name)
            continue
        body = p["html"](img) if callable(p["html"]) else p["html"]
        (B / f"{name}.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE}</style></head>'
                                        f'<body style="background:{p["bg"]};position:relative">{body}</body></html>', encoding="utf-8")
        jobs.append(name)
    (B / "jobs.json").write_text(json.dumps({"build": str(B), "out": str(OUT), "jobs": jobs}))
    subprocess.run(["node", str(ROOT / "tools/shoot.js"), str(B / "jobs.json")], check=True)
    # grille de prévisualisation (style profil Instagram)
    from PIL import Image, ImageDraw
    cell, gap = 360, 4
    grid = Image.new("RGB", (3 * cell + 2 * gap, 3 * cell + 2 * gap), "#FFFFFF")
    for r, row in enumerate(GRID):
        for c, name in enumerate(row):
            f = OUT / f"{name}.jpg"
            tile = Image.open(f).resize((cell, cell), Image.LANCZOS) if f.exists() else Image.new("RGB", (cell, cell), "#E7E1D8")
            if not f.exists():
                ImageDraw.Draw(tile).text((20, 170), f"{name}\n(en attente Gemini)", fill="#8C7462")
            grid.paste(tile, (c * (cell + gap), r * (cell + gap)))
    grid.save(ROOT / "livrables/grille-feed.jpg", quality=92)
    print("visuels :", jobs, "| en attente :", missing)


if __name__ == "__main__":
    main()
