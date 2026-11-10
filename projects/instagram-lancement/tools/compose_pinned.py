"""KAÏRA — les 3 publications épinglées (1080 × 1350) : 01 The Project · 02 Meet KAÏRA · 03 Our Services.

Le rendu de « The Project » est collé entier, proportions exactes, réduit directement depuis l'original
à la largeur du post (aucun recadrage, aucune retouche, aucun agrandissement).
Les fonds et la typographie sont dessinés en 2160 × 2700 puis réduits à 1080 × 1350.
Les couvertures 01-03 du feed v3 sont remplacées par ces visuels, et l'aperçu du profil est régénéré.
Usage : python3 tools/compose_pinned.py
"""
import json, pathlib, shutil, subprocess, sys
import numpy as np
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import compose_feed12 as base
import compose_v3 as v3
from compose_v3 import K, CSS, page
from compose_feed12 import SRGB, original

ROOT = base.ROOT
B = ROOT / "build/pinned"
V3 = ROOT / "livrables/instagram-v3"
OUT = V3 / "epingles"
W2, H2 = 2160, 2700
RENDER = "05"                       # chambre principale de la villa
WHITE_TXT = "#FBF8F3"


def the_project_html(img_h):
    """Fond chocolat ; zone du rendu en haut (pleine largeur), bandeau titre dessous."""
    band = H2 - img_h
    return page(f"""<div class="abs" style="left:0;right:0;top:0;height:{img_h}px;background:{K['choc']}"></div>
<div class="abs" style="left:150px;right:150px;top:{img_h + 74}px;display:flex;justify-content:space-between;align-items:flex-end">
 <div><div class="caps" style="font-size:28px;color:{K['choc_soft']}">01 &nbsp;—&nbsp; The Project</div>
  <div class="serif" style="font-size:96px;line-height:1;margin-top:24px">Villa <i style="color:{K['choc_soft']}">·</i> Master bedroom</div></div>
 <div style="text-align:right"><div style="width:80px;height:3px;background:{K['choc_soft']};margin:0 0 26px auto"></div>
  <div class="word" style="font-size:46px;margin-right:-.42em">KAÏRA</div></div>
</div>""", K["choc"], K["ivory"])


def meet_html():
    return page(f"""<div class="abs" style="inset:120px;border:2px solid {K['line']}"></div>
<div class="abs" style="inset:146px;border:1px solid {K['line']}"></div>
<div class="caps abs" style="top:250px;left:0;right:0;text-align:center;font-size:28px;color:{K['mute']}">02 &nbsp;—&nbsp; Meet KAÏRA</div>
<div class="abs" style="top:720px;left:0;right:0;text-align:center">
 <div class="word" style="font-size:280px;line-height:1;margin-right:-.42em;color:{K['choc']}">KAÏRA</div>
 <div style="display:flex;align-items:center;justify-content:center;gap:40px;margin-top:46px">
  <div style="width:150px;height:2px;background:{K['olive']}"></div>
  <div class="caps" style="font-size:34px;color:{K['olive']}">Interior Architecture</div>
  <div style="width:150px;height:2px;background:{K['olive']}"></div></div></div>
<div class="abs" style="top:1420px;left:0;right:0;text-align:center">
 <div class="serif" style="font-size:150px;line-height:1.05;color:{K['ink']}"><i style="color:{K['burgundy']}">The architecture of calm.</i></div>
 <div style="width:120px;height:4px;background:{K['burgundy']};margin:110px auto 90px"></div>
 <div style="font-size:44px;line-height:1.6;color:{K['mute']}">An interior architecture studio for residences,<br>villas and workspaces.</div></div>
<div class="caps abs" style="bottom:270px;left:0;right:0;text-align:center;font-size:28px;color:#B39B7C">Space &nbsp;·&nbsp; Material &nbsp;·&nbsp; Light</div>""",
                K["white"], K["ink"])


SERVICES = [("Interior design", "Concept, mood and identity of every space"),
            ("Space planning", "Layouts, circulation, furniture placement"),
            ("Bespoke furniture &amp; joinery", "Pieces drawn for one place only"),
            ("Materials &amp; lighting", "Finishes, textures and lighting scenes"),
            ("3D visualisation", "See your space before it is built")]


def services_html():
    rows = "".join(f'<div style="display:grid;grid-template-columns:110px 1fr;gap:30px;padding:46px 0;border-top:2px solid rgba(251,248,243,.22)">'
                   f'<div class="serif" style="font-size:54px;color:{K["burgundy_soft"]}">0{k + 1}</div>'
                   f'<div><div class="serif" style="font-size:92px;line-height:1.05">{t}</div>'
                   f'<div style="font-size:34px;color:#EBD3D7;margin-top:12px">{d}</div></div></div>'
                   for k, (t, d) in enumerate(SERVICES))
    return page(f"""<div class="abs" style="left:190px;right:190px;top:230px">
 <div class="caps" style="font-size:28px;color:{K['burgundy_soft']}">03 &nbsp;—&nbsp; Our Services</div>
 <div class="serif" style="font-size:190px;line-height:1;margin-top:60px">Our <i style="color:{K['burgundy_soft']}">services</i></div></div>
<div class="abs" style="left:190px;right:190px;top:840px">{rows}
 <div style="border-top:2px solid rgba(251,248,243,.22)"></div></div>
<div class="abs" style="left:190px;right:190px;bottom:200px;display:flex;justify-content:space-between;align-items:flex-end">
 <div><div class="caps" style="font-size:26px;color:{K['burgundy_soft']}">Residences · Villas · Workspaces</div>
  <div style="font-size:36px;color:#EBD3D7;margin-top:18px">Send us a message to start your project.</div></div>
 <div class="word" style="font-size:52px;margin-right:-.42em">KAÏRA</div></div>""", K["burgundy"], WHITE_TXT)


CAPTIONS = {
    "01-the-project": """The Project — Villa master bedroom.

A suite built around a single gesture: a band of dark veined marble, backlit, rising behind a wraparound headboard with soft, rounded lines. Lit wood slats, glass globe pendants on fine gold rods and olive bed linen complete a quiet, enveloping atmosphere.

Designed by KAÏRA Interior Design.

#KAIRAInteriorDesign #MasterBedroom #LuxuryBedroom #BedroomDesign #MarbleWall #VillaInterior #QuietLuxury #InteriorArchitecture""",
    "02-meet-kaira": """Meet KAÏRA — the architecture of calm.

KAÏRA is an interior architecture studio for residences, villas and workspaces. We design calm spaces where light, proportion and honest materials come first, and where every line has a reason to exist.

Welcome to our studio.

#KAIRAInteriorDesign #InteriorArchitecture #InteriorDesignStudio #InteriorDesign #LuxuryInteriors #QuietLuxury #ArchitectureInterieure #InteriorArchitect""",
    "03-our-services": """Our services.

01 · Interior design: concept, mood and identity of every space.
02 · Space planning: layouts, circulation and furniture placement.
03 · Bespoke furniture & joinery: pieces drawn for one place only.
04 · Materials & lighting: finishes, textures and lighting scenes.
05 · 3D visualisation: see your space before it is built.

For residences, villas and workspaces. Send us a direct message to start your project.

#KAIRAInteriorDesign #InteriorDesignServices #BespokeFurniture #SpacePlanning #3DVisualization #LuxuryInteriorDesign #InteriorArchitecture #InteriorDesigner""",
}


def main():
    B.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copytree(base.FONTS, B / "fonts", dirs_exist_ok=True)
    src = original(RENDER)
    rw = 1080
    rh = round(src.height * rw / src.width)                # 1080 × 1177, proportions exactes
    pages = {"01-the-project": the_project_html(rh * 2), "02-meet-kaira": meet_html(), "03-our-services": services_html()}
    jobs = []
    for n, html in pages.items():
        (B / f"{n}.html").write_text(html, encoding="utf-8")
        jobs.append([str(B / f"{n}.html"), str(B / f"{n}.png")])
    (B / "jobs.json").write_text(json.dumps({"w": W2, "h": H2, "jobs": jobs}))
    subprocess.run(["node", str(ROOT / "tools/shoot.js"), str(B / "jobs.json")], check=True)
    report = []
    for n in pages:
        im = Image.open(B / f"{n}.png").convert("RGB").resize((1080, 1350), Image.LANCZOS)
        if n == "01-the-project":
            r = src.resize((rw, rh), Image.LANCZOS)
            im.paste(r, (0, 0))
            assert abs(rw / rh - src.width / src.height) < 0.002
            report.append(f"{n}.png : rendu {RENDER} entier ({src.width} × {src.height} → {rw} × {rh}), proportions exactes, sans recadrage ni retouche")
        else:
            report.append(f"{n}.png : visuel graphique")
        im.save(OUT / f"{n}.png", icc_profile=SRGB, optimize=True)
        (OUT / f"{n}.txt").write_text(CAPTIONS[n] + "\n")
    (OUT / "verification.txt").write_text("\n".join(report) + "\n")
    # remplace les couvertures 01-03 du feed v3 (posts 1080) et met à jour l'aperçu du profil
    mapping = {"01-the-project": "03-master-bedroom", "02-meet-kaira": "01-kaira", "03-our-services": "02-services"}
    for new, post in mapping.items():
        shutil.copy(OUT / f"{new}.png", V3 / "posts-1080x1350" / post / f"{post}-1.png")
        shutil.copy(OUT / f"{new}.png", V3 / "couvertures" / f"{post}.png")
        (V3 / "posts-1080x1350" / post / "caption.txt").write_text(CAPTIONS[new] + "\n")
        hd = V3 / "hd-2160x2700" / post / f"{post}-1.png"
        if new == "01-the-project":
            hd.unlink(missing_ok=True)          # pas de version HD : le rendu ne serait pas à 100 %
        else:
            Image.open(B / f"{new}.png").convert("RGB").save(hd, icc_profile=SRGB, optimize=True)
            (V3 / "hd-2160x2700" / post / "caption.txt").write_text(CAPTIONS[new] + "\n")

    def tile(name, tw=360, th=480):
        im = Image.open(V3 / "posts-1080x1350" / name / f"{name}-1.png").convert("RGB")
        cw = 1012
        return im.crop(((1080 - cw) // 2, 0, (1080 - cw) // 2 + cw, 1350)).resize((tw, th), Image.LANCZOS)
    v3.tile = tile
    v3.previews([(p.name, None) for p in sorted((V3 / "posts-1080x1350").iterdir())])
    shutil.copy(V3 / "apercu-profil.jpg", OUT / "apercu-profil.jpg")
    shutil.copy(V3 / "grille-profil.jpg", OUT / "grille-profil.jpg")
    # rangée des épinglés, légendée
    row = Image.new("RGB", (3 * 360 + 8, 480), "#FFFFFF")
    for k, n in enumerate(["03-master-bedroom", "01-kaira", "02-services"]):
        row.paste(tile(n), (k * 364, 0))
    row.save(OUT / "ordre-epingles.jpg", quality=93)
    print("\n".join(report))


if __name__ == "__main__":
    main()
