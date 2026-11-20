"""KAÏRA Interior Design — logo system build.

Outputs (projects/kaira-logo/logo/):
  svg/   vector masters (every lockup × colour)
  png/   transparent PNGs, 4000 px wide (lockups) / 3000 px (symbols)
  social/  Instagram profile pictures, story/post avatars, favicon, website header
  presentation/  identity presentation (PDF + PNG pages)
Usage: python3 tools/build_logo.py
"""
import json, pathlib, shutil, subprocess, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import geometry as G

ROOT = HERE.parent
OUT = ROOT / "logo"
B = ROOT / "build"
FONTS = ROOT.parent / "dossier-client/build/fonts"
NODE_CWD = ROOT.parent / "instagram-lancement/tools"      # playwright is resolved from there

COLORS = {"chocolate": "#3A2A22", "olive": "#5F6A45", "burgundy": "#6E2234", "ivory": "#F7F3EC",
          "black": "#000000", "white": "#FFFFFF"}


# ------------------------------------------------------------------ « INTERIOR DESIGN » outlined (Jost, OFL)
def text_outline(text, size, width=None, font="jost-latin-400-normal.woff2", tracking=0.5):
    f = TTFont(FONTS / font)
    gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    upm = f["head"].unitsPerEm
    s = size / upm
    glyphs = [cmap[ord(c)] for c in text]
    adv = [hmtx[g][0] * s for g in glyphs]
    if width is not None:      # justify: tracking so that the line spans exactly `width`
        ink = sum(adv[:-1]) + gs[glyphs[-1]].width * s
        tr = (width - ink) / (len(text) - 1)
    else:
        tr = tracking * size
    pen = SVGPathPen(gs)
    x = 0
    for g, a in zip(glyphs, adv):
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, 0)))
        x += a + tr
    return pen.getCommands(), x - tr


# ------------------------------------------------------------------ components (local units)
def wordmark_g():
    paths, w, top, bot = G.wordmark()
    return "".join(paths), w, top, bot            # x 0..w, y top..bot


def mono_g():
    p, w = G.mono_ligature()
    return f'<g transform="translate({G.SER},0)">{G.paths_svg(p)}</g>', w, 0, G.CAP


def emblem_g(stroke=5):
    m, mw, _, _ = mono_g()
    aw, ah = mw + 120, 520
    r = aw / 2
    mx, my = (aw - mw) / 2, ah - 60 - G.CAP
    arch = (f'<path d="M0,{ah} V{r} A{r},{r} 0 0 1 {aw},{r} V{ah}" fill="none" stroke="currentColor" stroke-width="{stroke}"/>')
    return f'{arch}<g transform="translate({mx:.1f},{my:.1f})">{m}</g>', aw, 0, ah


def tagline(width):
    d, w = text_outline("INTERIOR DESIGN", 46, width=width)
    return f'<path d="{d}"/>', w


# ------------------------------------------------------------------ lockups: (svg inner, w, h) with origin top-left
def lockup_main():
    """Primary: custom wordmark over INTERIOR DESIGN, justified to the wordmark width."""
    wm, w, top, bot = wordmark_g()
    tl, _ = tagline(w)
    gap = 92
    h = (bot - top) + gap + 34
    return f'<g transform="translate(0,{-top})">{wm}</g><g transform="translate(0,{bot - top + gap + 34})">{tl}</g>', w, h


def lockup_stacked():
    """Alternative: arch emblem above the primary lockup."""
    em, ew, _, eh = emblem_g(stroke=6)
    main, mw, mh = lockup_main()
    sc = 0.78
    gap = 110
    w = max(mw, ew * sc)
    return (f'<g transform="translate({(w - ew * sc) / 2:.1f},0) scale({sc})">{em}</g>'
            f'<g transform="translate({(w - mw) / 2:.1f},{eh * sc + gap:.1f})">{main}</g>'), w, eh * sc + gap + mh


def lockup_horizontal():
    em, ew, _, eh = emblem_g(stroke=6)
    main, mw, mh = lockup_main()
    sc = (mh * 1.55) / eh
    gap = 120
    eh2, ew2 = eh * sc, ew * sc
    h = max(eh2, mh)
    x_div = ew2 + gap
    return (f'<g transform="translate(0,{(h - eh2) / 2:.1f}) scale({sc:.4f})">{em}</g>'
            f'<rect x="{x_div:.1f}" y="{(h - mh * 1.2) / 2:.1f}" width="3" height="{mh * 1.2:.1f}"/>'
            f'<g transform="translate({x_div + 3 + gap:.1f},{(h - mh) / 2:.1f})">{main}</g>'), x_div + 3 + gap + mw, h


def lockup_wordmark():
    wm, w, top, bot = wordmark_g()
    return f'<g transform="translate(0,{-top})">{wm}</g>', w, bot - top


def symbol_monogram():
    m, w, _, h = mono_g()
    return m, w, h


def symbol_emblem():
    em, w, _, h = emblem_g()
    return em, w, h


LOCKUPS = {"1-main-logo": lockup_main, "2-alternative-stacked": lockup_stacked, "3-monogram": symbol_monogram,
           "3b-monogram-arch-emblem": symbol_emblem, "4-horizontal": lockup_horizontal, "5-wordmark-only": lockup_wordmark}


def svg_doc(inner, w, h, color, pad_ratio=0.12, bg=None):
    pad = max(w, h) * pad_ratio
    W, H = w + 2 * pad, h + 2 * pad
    bgr = f'<rect width="{W:.1f}" height="{H:.1f}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}" width="{W:.0f}" height="{H:.0f}">'
            f'{bgr}<g fill="{color}" color="{color}" transform="translate({pad:.1f},{pad:.1f})">{inner}</g></svg>'), W, H


def render(jobs):
    """jobs: [svg_path, png_path, px_width, transparent]"""
    (B / "render.json").write_text(json.dumps(jobs))
    js = f"""const {{ chromium }} = require('playwright'); const fs = require('fs');
(async () => {{ const jobs = JSON.parse(fs.readFileSync('{B / "render.json"}','utf8')); const b = await chromium.launch();
 for (const [svg, png, w, tr] of jobs) {{
  const src = fs.readFileSync(svg, 'utf8'); const m = src.match(/viewBox="0 0 ([\\d.]+) ([\\d.]+)"/);
  const vw = parseFloat(m[1]), vh = parseFloat(m[2]); const h = Math.round(w * vh / vw);
  const p = await b.newPage({{ viewport: {{ width: w, height: h }} }});
  const html = `<html><body style="margin:0;background:transparent">${{src.replace(/width="[\\d.]+" height="[\\d.]+"/, `width="${{w}}" height="${{h}}"`)}}</body></html>`;
  await p.setContent(html); await p.screenshot({{ path: png, omitBackground: tr, clip: {{ x: 0, y: 0, width: w, height: h }} }}); await p.close(); }}
 await b.close(); }})();"""
    subprocess.run(["node", "-e", js], check=True, cwd=str(NODE_CWD))


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    for d in ("svg", "png", "social", "presentation"):
        (OUT / d).mkdir(parents=True)
    B.mkdir(exist_ok=True)
    jobs = []
    variants = ["chocolate", "olive", "burgundy", "ivory", "black", "white"]
    for name, fn in LOCKUPS.items():
        inner, w, h = fn()
        for c in variants:
            doc, W, H = svg_doc(inner, w, h, COLORS[c])
            sp = OUT / "svg" / f"kaira-{name}-{c}.svg"
            sp.write_text(doc)
            px = 3000 if name.startswith("3") else 4000
            jobs.append([str(sp), str(OUT / "png" / f"kaira-{name}-{c}-transparent.png"), px, True])
    # social & web
    social = [
        ("instagram-profile-olive", symbol_emblem, "ivory", "olive", 1080, 0.30),
        ("instagram-profile-ivory", symbol_emblem, "chocolate", "ivory", 1080, 0.30),
        ("instagram-profile-burgundy", symbol_emblem, "ivory", "burgundy", 1080, 0.30),
        ("favicon-512", symbol_monogram, "ivory", "chocolate", 512, 0.28),
        ("website-header-ivory", lockup_horizontal, "chocolate", "ivory", 2400, 0.10),
        ("website-header-chocolate", lockup_horizontal, "ivory", "chocolate", 2400, 0.10),
        ("document-letterhead-logo", lockup_main, "chocolate", None, 2400, 0.08),
        ("instagram-post-logo-olive", lockup_stacked, "ivory", "olive", 1080, 0.22),
    ]
    for name, fn, fg, bg, px, pad in social:
        inner, w, h = fn()
        if name.startswith("instagram-profile") or name.startswith("favicon") or name.startswith("instagram-post"):
            side = max(w, h)
            if name.startswith("instagram-post"):
                W0, H0 = side * 1.0, side * 1.25          # 4:5
            else:
                W0 = H0 = side
            padx, pady = (W0 - w) / 2 + side * pad, (H0 - h) / 2 + side * pad
            Wt, Ht = W0 + 2 * side * pad, H0 + 2 * side * pad
            doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wt:.1f} {Ht:.1f}" width="{Wt:.0f}" height="{Ht:.0f}">'
                   f'<rect width="{Wt:.1f}" height="{Ht:.1f}" fill="{COLORS[bg]}"/><g fill="{COLORS[fg]}" color="{COLORS[fg]}" '
                   f'transform="translate({padx:.1f},{pady:.1f})">{inner}</g></svg>')
        else:
            doc, _, _ = svg_doc(inner, w, h, COLORS[fg], pad, COLORS[bg] if bg else None)
        sp = B / f"{name}.svg"
        sp.write_text(doc)
        jobs.append([str(sp), str(OUT / "social" / f"kaira-{name}.png"), px, bg is None])
    render(jobs)
    (OUT / "lockups.json").write_text(json.dumps({k: list(v()[1:]) for k, v in LOCKUPS.items()}))
    print(len(jobs), "files rendered")


if __name__ == "__main__":
    main()
