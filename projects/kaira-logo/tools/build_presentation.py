"""KAÏRA — visual identity presentation (16:9 pages → PNG + PDF). Uses the SVG masters from logo/svg."""
import json, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import geometry as G
import build_logo as BL

ROOT = HERE.parent
SVG = ROOT / "logo/svg"
OUT = ROOT / "logo/presentation"
B = ROOT / "build/pres"
C = BL.COLORS
INK, MUTE, LINE = "#2E231D", "#8A7B6E", "#E4DACB"


def svg(name, color, height=None, width=None):
    s = (SVG / f"kaira-{name}-{color}.svg").read_text()
    size = (f'style="height:{height}px;width:auto;display:block"' if height else f'style="width:{width}px;height:auto;display:block"')
    return s.replace("<svg ", f"<svg {size} ", 1)


FACES = "".join(f'@font-face{{font-family:"{f}";font-weight:{w};font-style:{st};src:url(fonts/{n})}}' for f, w, st, n in [
    ("Cormorant", 300, "normal", "cormorant-garamond-latin-300-normal.woff2"), ("Cormorant", 300, "italic", "cormorant-garamond-latin-300-italic.woff2"),
    ("Cormorant", 400, "normal", "cormorant-garamond-latin-400-normal.woff2"),
    ("Jost", 300, "normal", "jost-latin-300-normal.woff2"), ("Jost", 400, "normal", "jost-latin-400-normal.woff2")])
CSS = FACES + f"""*{{margin:0;padding:0;box-sizing:border-box}}
.page{{width:1920px;height:1080px;position:relative;overflow:hidden;background:{C['ivory']};color:{INK};font-family:Jost;font-weight:300;page-break-after:always}}
.k{{font:400 15px Jost;letter-spacing:.34em;text-transform:uppercase;color:{C['olive']}}}
h2{{font:300 64px/1.05 Cormorant;margin-top:18px}} h2 i{{color:{C['burgundy']}}}
p{{font-size:20px;line-height:1.6;color:{MUTE}}}
.num{{position:absolute;right:90px;bottom:60px;font:400 13px Jost;letter-spacing:.3em;color:{MUTE}}}
.brand{{position:absolute;left:90px;bottom:56px}}
.c{{display:flex;align-items:center;justify-content:center}}"""


def footer(n):
    return f'<div class="brand">{svg("5-wordmark-only", "chocolate", height=22)}</div><div class="num">{n:02d} — KAÏRA VISUAL IDENTITY</div>'


def pages():
    P = []
    # 1 cover
    P.append(f"""<div class="page c" style="flex-direction:column">{svg("2-alternative-stacked", "chocolate", height=560)}
<div class="k" style="margin-top:40px;color:{MUTE}">Visual identity · 2026</div></div>""")
    # 2 concept
    k, kw = G.K()
    a, aw = G.A()
    r, rw = G.R()

    def glyph(paths, w, label):
        return (f'<div style="text-align:center"><svg viewBox="-30 -20 {w + 60} 250" style="height:230px"><g fill="{C["chocolate"]}">{G.paths_svg(paths)}</g></svg>'
                f'<div class="k" style="margin-top:22px;color:{C["burgundy"]}">{label}</div></div>')
    P.append(f"""<div class="page"><div style="position:absolute;left:90px;top:90px;width:640px">
<div class="k">Concept</div><h2>The <i>shadow gap</i></h2>
<p style="margin-top:34px">In every KAÏRA interior, a fine recessed joint separates two materials: stone from wood, a panel from the ceiling.
This shadow gap is the signature of the studio's architecture.</p>
<p style="margin-top:20px">The wordmark is drawn on the same principle. The arm of the K floats beside its stem, the bar of the A floats between its legs,
the leg of the R stands free under its bowl. The two dots of the Ï are lozenges, like an inlay in a stone floor.</p>
<p style="margin-top:20px">High-contrast strokes and hairline serifs give the editorial elegance; the gaps give the architecture.</p></div>
<div style="position:absolute;left:820px;right:90px;top:260px;display:flex;justify-content:space-between">{glyph(k, kw, 'K · floating arm')}{glyph(a, aw, 'A · floating bar')}{glyph(r, rw, 'R · free leg')}</div>
{footer(2)}</div>""")
    # 3 primary logo
    P.append(f"""<div class="page"><div style="position:absolute;left:90px;top:90px"><div class="k">01 · Main logo</div><h2>Primary <i>lockup</i></h2>
<p style="margin-top:20px;width:520px">The custom wordmark over INTERIOR DESIGN, set in Jost and justified to the full width of the name. For the website, documents and signage.</p></div>
<div class="c" style="position:absolute;left:700px;top:120px;width:1130px;height:420px;background:#FCFAF7">{svg("1-main-logo", "chocolate", width=760)}</div>
<div class="c" style="position:absolute;left:700px;top:560px;width:555px;height:380px;background:{C['chocolate']}">{svg("1-main-logo", "ivory", width=420)}</div>
<div class="c" style="position:absolute;left:1275px;top:560px;width:555px;height:380px;background:{C['olive']}">{svg("1-main-logo", "ivory", width=420)}</div>
{footer(3)}</div>""")
    # 4 alternative + horizontal
    P.append(f"""<div class="page"><div style="position:absolute;left:90px;top:90px"><div class="k">02 · Alternative &amp; 04 · Horizontal</div><h2>Two more <i>lockups</i></h2>
<p style="margin-top:20px;width:520px">Stacked, with the arch emblem, for covers, presentations and signage. Horizontal, for the website header, email signatures and narrow formats.</p></div>
<div class="c" style="position:absolute;left:90px;top:430px;width:620px;height:520px;background:#FCFAF7">{svg("2-alternative-stacked", "chocolate", height=400)}</div>
<div class="c" style="position:absolute;left:740px;top:120px;width:1090px;height:400px;background:#FCFAF7">{svg("4-horizontal", "chocolate", width=860)}</div>
<div class="c" style="position:absolute;left:740px;top:550px;width:1090px;height:400px;background:{C['burgundy']}">{svg("4-horizontal", "ivory", width=860)}</div>
{footer(4)}</div>""")
    # 5 monogram
    tiles = "".join(f'<div class="c" style="width:400px;height:400px;background:{bg}">{svg("3b-monogram-arch-emblem", fg, height=300)}</div>'
                    for bg, fg in ((C['olive'], "ivory"), (C['burgundy'], "ivory"), (C['chocolate'], "ivory"), ("#FCFAF7", "olive")))
    P.append(f"""<div class="page"><div style="position:absolute;left:90px;top:90px;width:600px"><div class="k">03 · Monogram</div><h2>K and A, <i>one stroke</i></h2>
<p style="margin-top:20px">The arm of the K becomes the left leg of the A; the bar of the A passes behind the K, separated by two shadow gaps.
Set inside an open arch, the doorway of every interior, it becomes the studio's emblem: profile picture, stamp, packaging, embossing.</p></div>
<div class="c" style="position:absolute;left:90px;top:480px;width:600px;height:470px;background:#FCFAF7">{svg("3-monogram", "chocolate", height=300)}</div>
<div style="position:absolute;left:740px;top:120px;display:grid;grid-template-columns:400px 400px;gap:20px 30px;transform:scale(1.04);transform-origin:0 0">{tiles}</div>
{footer(5)}</div>""")
    # 6 colours
    pal = [("Olive green", C['olive'], "95 · 106 · 69"), ("Burgundy", C['burgundy'], "110 · 34 · 52"),
           ("Chocolate", C['chocolate'], "58 · 42 · 34"), ("Warm ivory", C['ivory'], "247 · 243 · 236")]
    sw = "".join(f'<div style="flex:1"><div style="height:520px;background:{h};border:1px solid {LINE}"></div><div style="font:300 34px Cormorant;margin-top:22px">{n}</div>'
                 f'<div class="k" style="color:{MUTE};margin-top:8px;font-size:13px">{h} · RGB {rgb}</div></div>' for n, h, rgb in pal)
    P.append(f"""<div class="page"><div style="position:absolute;left:90px;top:90px"><div class="k">Colours</div><h2>Four colours, <i>one atmosphere</i></h2></div>
<div style="position:absolute;left:90px;right:90px;top:300px;display:flex;gap:30px">{sw}</div>{footer(6)}</div>""")
    # 7 typography
    P.append(f"""<div class="page"><div style="position:absolute;left:90px;top:90px"><div class="k">Typography</div><h2>A custom name, <i>two companions</i></h2></div>
<div style="position:absolute;left:90px;right:90px;top:330px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:60px">
 <div><div class="k" style="color:{C['burgundy']}">Wordmark</div><div style="margin:40px 0 30px">{svg("5-wordmark-only", "chocolate", width=440)}</div><p>Custom drawn letters, not a font: high contrast, hairline serifs and shadow gaps. Never retyped.</p></div>
 <div><div class="k" style="color:{C['burgundy']}">Headings</div><div style="font:300 92px/1 Cormorant;margin:30px 0 26px">Aa <i>Aa</i></div><p>Cormorant Garamond — titles, quotes, editorial headings.</p></div>
 <div><div class="k" style="color:{C['burgundy']}">Text &amp; labels</div><div style="font:300 92px/1 Jost;margin:30px 0 26px">Aa <span style="font-size:30px;letter-spacing:.34em">CAPS</span></div><p>Jost — INTERIOR DESIGN, labels, body text, captions.</p></div></div>{footer(7)}</div>""")
    # 8 clear space & sizes
    P.append(f"""<div class="page"><div style="position:absolute;left:90px;top:90px;width:560px"><div class="k">Usage</div><h2>Clear space &amp; <i>minimum sizes</i></h2>
<p style="margin-top:24px">Keep an empty margin around the logo equal to half the height of the name KAÏRA (x on the diagram).</p>
<p style="margin-top:20px">Main logo: minimum 35 mm wide in print, 160 px on screen. Monogram: minimum 10 mm, 32 px. Below that, use the monogram without the arch.</p>
<p style="margin-top:20px">Do not stretch, rotate, outline, add shadows or retype the name.</p></div>
<div class="c" style="position:absolute;left:760px;top:150px;width:1070px;height:620px;background:#FCFAF7">
 <div style="position:relative;padding:80px;border:1px dashed {C['burgundy']}"><div style="position:absolute;left:0;top:0;width:80px;height:80px;display:flex;align-items:center;justify-content:center;font:400 18px Jost;color:{C['burgundy']}">x</div>{svg("1-main-logo", "chocolate", width=640)}</div></div>
<div style="position:absolute;left:760px;top:800px;display:flex;gap:60px;align-items:flex-end">
 <div>{svg("1-main-logo", "chocolate", width=160)}<div class="k" style="color:{MUTE};margin-top:12px;font-size:12px">160 px · 35 mm</div></div>
 <div>{svg("3-monogram", "chocolate", height=32)}<div class="k" style="color:{MUTE};margin-top:12px;font-size:12px">32 px · 10 mm</div></div></div>{footer(8)}</div>""")
    # 9 applications
    avatar = svg("3b-monogram-arch-emblem", "ivory", height=150)
    P.append(f"""<div class="page"><div style="position:absolute;left:90px;top:90px"><div class="k">Applications</div><h2>The identity <i>at work</i></h2></div>
<div style="position:absolute;left:90px;top:300px;width:520px;height:640px;background:#fff;border:1px solid {LINE};padding:40px">
 <div style="display:flex;gap:28px;align-items:center"><div class="c" style="width:150px;height:150px;border-radius:50%;background:{C['olive']}">{svg("3b-monogram-arch-emblem", "ivory", height=104)}</div>
 <div><div style="font:400 22px Jost">kaira.interiordesign</div><div style="font:300 16px Jost;color:{MUTE};margin-top:8px">KAÏRA Interior Design<br>Interior architecture studio</div></div></div>
 <div style="display:flex;gap:16px;margin-top:40px">{"".join(f'<div class="c" style="width:66px;height:66px;border-radius:50%;background:{b}">{svg("3-monogram", f, height=22)}</div>' for b, f in ((C["olive"], "ivory"), (C["burgundy"], "ivory"), (C["chocolate"], "ivory"), ("#EDE6DA", "chocolate"), ("#E8E9DD", "olive")))}</div>
 <div class="k" style="margin-top:40px;color:{MUTE}">Instagram profile &amp; highlights</div></div>
<div style="position:absolute;left:650px;top:300px;display:flex;flex-direction:column;gap:30px">
 <div style="display:flex;gap:30px">
  <div class="c" style="width:510px;height:300px;background:{C['chocolate']};box-shadow:0 18px 40px rgba(0,0,0,.12)">{svg("2-alternative-stacked", "ivory", height=180)}</div>
  <div style="width:510px;height:300px;background:#FCFAF7;box-shadow:0 18px 40px rgba(0,0,0,.12);position:relative;padding:44px">
   {svg("4-horizontal", "chocolate", width=250)}<div style="position:absolute;left:44px;bottom:44px;font:300 17px/1.6 Jost;color:{MUTE}">Interior architect<br>Residences · Villas · Workspaces</div>
   <div style="position:absolute;right:0;top:0;bottom:0;width:14px;background:{C['burgundy']}"></div></div></div>
 <div style="width:1050px;height:310px;background:#FCFAF7;box-shadow:0 18px 40px rgba(0,0,0,.12);display:flex;align-items:center;justify-content:space-between;padding:0 50px">
  {svg("4-horizontal", "chocolate", width=360)}<div style="display:flex;gap:40px;font:400 14px Jost;letter-spacing:.3em;color:{INK}">PROJECTS<span>STUDIO</span><span>SERVICES</span><span>CONTACT</span></div></div>
 <div class="k" style="color:{MUTE}">Business card · website header</div></div>{footer(9)}</div>""")
    # 10 colour versions
    vs = [("chocolate", "#FCFAF7"), ("olive", "#FCFAF7"), ("burgundy", "#FCFAF7"), ("ivory", C['chocolate']), ("ivory", C['olive']), ("ivory", C['burgundy'])]
    grid = "".join(f'<div class="c" style="height:300px;background:{bg}">{svg("1-main-logo", fg, width=400)}</div>' for fg, bg in vs)
    P.append(f"""<div class="page"><div style="position:absolute;left:90px;top:90px"><div class="k">Colour versions</div><h2>Always on <i>calm grounds</i></h2></div>
<div style="position:absolute;left:90px;right:90px;top:290px;display:grid;grid-template-columns:repeat(3,1fr);gap:20px">{grid}</div>{footer(10)}</div>""")
    return P


def main():
    import shutil
    B.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copytree(BL.FONTS, B / "fonts", dirs_exist_ok=True)
    P = pages()
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}@page{{size:1920px 1080px;margin:0}}</style></head><body>{"".join(P)}</body></html>'
    (B / "presentation.html").write_text(html, encoding="utf-8")
    js = f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage({{ viewport: {{ width: 1920, height: 1080 }} }});
 await p.goto('file://{B / "presentation.html"}', {{ waitUntil: 'networkidle' }}); await p.evaluate(() => document.fonts.ready);
 await p.pdf({{ path: '{OUT / "KAIRA-visual-identity.pdf"}', width: '1920px', height: '1080px', printBackground: true }});
 const els = await p.$$('.page'); for (let i = 0; i < els.length; i++) await els[i].screenshot({{ path: '{OUT}/page-' + String(i + 1).padStart(2, '0') + '.png' }});
 await b.close(); }})();"""
    subprocess.run(["node", "-e", js], check=True, cwd=str(BL.NODE_CWD))
    print(len(P), "pages")


if __name__ == "__main__":
    main()
