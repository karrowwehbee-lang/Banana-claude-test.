"""Build the KAÏRA website.
  index.html  — artifact version (page content; the artifact host adds the document head)
  dist/       — standalone website for any static host / own domain: index.html (full document), img/, favicon.png
Usage: python3 build.py
"""
import json, pathlib, re, shutil
ROOT = pathlib.Path(__file__).resolve().parent
LOGO = ROOT.parent / "kaira-logo/logo"


def inline(name):
    s = (LOGO / "svg" / name).read_text()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    pad = float(re.search(r'translate\(([\d.]+),', s).group(1))
    w, h = vb[2] - 2 * pad, vb[3] - 2 * pad
    s = re.sub(r'<svg [^>]*>', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{pad} {pad} {w:.1f} {h:.1f}" width="100%" '
               f'role="img" aria-label="KAÏRA Interior Design" style="display:block;height:auto">', s, count=1)
    return s.replace('fill="#3A2A22"', 'fill="currentColor"').replace('color="#3A2A22"', 'color="currentColor"')


sizes = json.loads((ROOT / "img/sizes.json").read_text())
for f in (ROOT / "img").glob("draw-*.svg"):
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', f.read_text()).group(1).split()]
    sizes[f.stem] = [vb[2], vb[3]]
used = set(re.findall(r'"((?:rdc|etage1|chambre)-[a-z]+-\d\d|[nkr]\d\d|draw-[a-z]+)"', (ROOT / "src/site.html").read_text()))
missing = [u for u in used if u not in sizes]
assert not missing, missing
body = (ROOT / "src/site.html").read_text()
body = body.replace("__WORDMARK__", inline("kaira-5-wordmark-only-chocolate.svg")).replace("__SIZES__", json.dumps({k: sizes[k] for k in sorted(used)}))
fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@300;400;500&display=swap">')
desc = "KAÏRA Interior Design — interior architecture studio founded by Karen Wehbe: residences, workspaces, hospitality and retail."
(ROOT / "index.html").write_text('<title>KAÏRA Interior Design</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n' + fonts + "\n" + body)
dist = ROOT / "dist"
if dist.exists():
    shutil.rmtree(dist)
(dist / "img").mkdir(parents=True)
for u in used:
    src = ROOT / "img" / (u + (".svg" if u.startswith("draw-") else ".jpg"))
    shutil.copy2(src, dist / "img" / src.name)
shutil.copy2(LOGO / "social/kaira-favicon-512.png", dist / "favicon.png")
shutil.copy2(ROOT / "img/rdc-salon-05.jpg", dist / "og-image.jpg")
head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>KAÏRA Interior Design</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:title" content="KAÏRA Interior Design">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="og-image.jpg">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" type="image/png" href="favicon.png">
{fonts}
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}[hidden]{{display:none!important}}</style>
</head>
<body>
"""
(dist / "index.html").write_text(head + body + "\n</body>\n</html>\n")
print("index.html", len(body), "bytes;", len(used), "images;", "dist ready")
