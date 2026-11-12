"""Build the KAÏRA website (v2, cinematic "House" direction).
  index.html  — artifact version (page content; the artifact host adds the document head; libraries from CDNs)
  dist/       — standalone website for any static host / own domain: full HTML document, img/, fonts/, vendor/ (no CDN needed)
Usage: python3 tools/images.py   (once, or when renders change)   then   python3 build.py
"""
import json, pathlib, re, shutil
ROOT = pathlib.Path(__file__).resolve().parent
LOGO = ROOT.parent / "kaira-logo/logo"
FONTS = ROOT.parent / "dossier-client/build/fonts"
SRC = ROOT / "src/site.html"
GUIDE = ROOT / "deploy/LISEZ-MOI.md"


def wordmark():
    s = (LOGO / "svg/kaira-5-wordmark-only-chocolate.svg").read_text()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    pad = float(re.search(r'translate\(([\d.]+),', s).group(1))
    w, h = vb[2] - 2 * pad, vb[3] - 2 * pad
    s = re.sub(r'<svg [^>]*>', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{pad} {pad} {w:.1f} {h:.1f}" width="100%" '
               f'role="img" aria-label="KAÏRA Interior Design" style="display:block;height:auto">', s, count=1)
    s = re.sub(r'<g transform="translate\((\d+),0\)">', r'<g class="lt" transform="translate(\1,0)">', s)  # one group per letter
    return s.replace('fill="#3A2A22"', 'fill="currentColor"').replace('color="#3A2A22"', 'color="currentColor"')


sizes = json.loads((ROOT / "img/sizes.json").read_text())
for f in (ROOT / "img").glob("draw-*.svg"):
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', f.read_text()).group(1).split()]
    sizes[f.stem] = [vb[2], vb[3]]
src = SRC.read_text()
used = set(re.findall(r'(?<![\w-])((?:rdc|etage1|chambre)-[a-z]+-\d\d|[nkr]\d\d|draw-[a-z]+)(?![\w-])', src))
missing = sorted(u for u in used if u not in sizes)
assert not missing, missing
wm = wordmark()
assert wm.count('class="lt"') == 5, "wordmark letters"
body = src.replace("__WORDMARK__", wm).replace("__SIZES__", json.dumps({k: sizes[k] for k in sorted(used)}))
gfonts = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
          '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@300;400;500&display=swap">')
(ROOT / "index.html").write_text(body.replace("<title>KAÏRA Interior Design</title>", "<title>KAÏRA Interior Design</title>\n" + gfonts, 1))

# ---------------------------------------------------------------- dist (own domain)
dist = ROOT / "dist"
if dist.exists():
    shutil.rmtree(dist)
for d in ("img", "fonts", "vendor"):
    (dist / d).mkdir(parents=True)
for u in sorted(used):
    f = ROOT / "img" / (u + (".svg" if u.startswith("draw-") else ".jpg"))
    shutil.copy2(f, dist / "img" / f.name)
faces = []
for f in sorted(FONTS.glob("*.woff2")):
    shutil.copy2(f, dist / "fonts" / f.name)
    m = re.match(r"(cormorant-garamond|jost)-latin-(\d+)-(normal|italic)", f.stem)
    fam = "Cormorant Garamond" if m.group(1).startswith("cormorant") else "Jost"
    faces.append(f'@font-face{{font-family:"{fam}";font-style:{m.group(3)};font-weight:{m.group(2)};font-display:swap;src:url(fonts/{f.name}) format("woff2")}}')
for f in (ROOT / "vendor").glob("*.js"):
    shutil.copy2(f, dist / "vendor" / f.name)
local = body
for url in re.findall(r'<script src="(https://[^"]+)"></script>', body):
    name = url.rsplit("/", 1)[1]
    assert (dist / "vendor" / name).exists(), name
    local = local.replace(url, "vendor/" + name)
shutil.copy2(LOGO / "social/kaira-favicon-512.png", dist / "favicon.png")
shutil.copy2(ROOT / "img/rdc-salon-02.jpg", dist / "og-image.jpg")
desc = "KAÏRA Interior Design, interior architecture studio founded by Karen Wehbe: residences, workspaces, hospitality and retail."
head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:title" content="KAÏRA Interior Design">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="og-image.jpg">
<meta name="theme-color" content="#15110E">
<link rel="icon" type="image/png" href="favicon.png">
<style>{"".join(faces)}:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}[hidden]{{display:none!important}}</style>
"""
local = local.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
title_end = local.index("</title>") + len("</title>")
(dist / "index.html").write_text(head + local[:title_end] + "\n</head>\n<body>\n" + local[title_end:] + "\n</body>\n</html>\n")
if GUIDE.exists():
    shutil.copy2(GUIDE, dist / "LISEZ-MOI.md")
total = sum(f.stat().st_size for f in dist.rglob("*") if f.is_file())
print(f"index.html {len(body)} bytes · {len(used)} images · dist {total / 1e6:.1f} MB (self-contained: fonts + libraries)")
