"""KAÏRA — Douche principale, Étage 1 : dossier technique A3 paysage (document de travail, non finalisé).

Même identité que le dossier technique de la villa (projects/dossier-technique) : feuille A3, cadre, cartouche, polices.
Usage : python3 tools/build.py [--previews]   ->  build/dossier-douche-etage1.html, build/…pdf, build/prev-NN.png
"""
import html
import importlib.util
import pathlib
import subprocess
import sys

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import details as T  # noqa: E402

ROOT = HERE.parent
REPO = ROOT.parent.parent
SRC = ROOT / "sources"
BUILD = ROOT / "build"
CROPS = BUILD / "crops"
OUT_PDF = BUILD / "KAIRA-Douche-principale-Etage1-A3-document-de-travail.pdf"

# the villa dossier's stylesheet, logo and fonts (same identity)
_spec = importlib.util.spec_from_file_location("villa_build", REPO / "projects/dossier-technique/tools/build.py")
VB = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(VB)
LOGO, FONTS = VB.LOGO, VB.FONTS

PROJECT = "Villa — Douche principale, Étage 1"
DOC = "Dossier technique d'architecture intérieure"
DATE = "17.11.2026"
INDICE = "0"
STATUS = "Document de travail — non finalisé"
AX, AY, AW, AH = 12, 12, 328, 272
INK, BURG, OLIVE = "#1E1E1E", "#6E2234", "#55603C"

SHEETS = []


def sheet(num, title, group, scale, body):
    SHEETS.append(dict(num=num, title=title, group=group, scale=scale, body=body))


def src(n):
    return SRC / f"{n}.png"


def size(n):
    return Image.open(src(n)).size


def box(x, y, w, inner, cls="tx"):
    return f'<div class="{cls}" style="left:{x:.1f}mm;top:{y:.1f}mm;width:{w:.1f}mm">{inner}</div>'


def esc(s):
    return html.escape(s)


def plate_of(d):
    return next(p[0] for p in T.PLATES if d in p[3])


# ---------------------------------------------------------------- render with numbered frames (the image is untouched)
def framed_render(n, x, y, h, marks=(), label_size=46):
    w_px, h_px = size(n)
    w = h * w_px / h_px
    svg = ""
    for d in marks:
        x0, y0, x1, y1 = T.D[d][4]
        lw, lh = label_size * 2.3, label_size * 1.25
        pos = T.LABEL_POS.get(d, "tl")
        bx = max(x0, 4) if pos in ("tl", "bl") else x1 - lw - 3
        by = max(y0, 4) if pos in ("tl", "tr") else y1 - lh - 3
        svg += (f'<rect x="{x0 + 3}" y="{y0 + 3}" width="{x1 - x0 - 6}" height="{y1 - y0 - 6}" fill="none" '
                f'stroke="#FFFFFF" stroke-width="9"/>'
                f'<rect x="{x0 + 3}" y="{y0 + 3}" width="{x1 - x0 - 6}" height="{y1 - y0 - 6}" fill="none" '
                f'stroke="{BURG}" stroke-width="5"/>'
                f'<rect x="{bx:.0f}" y="{by:.0f}" width="{lw:.0f}" height="{lh:.0f}" fill="{BURG}"/>'
                f'<text x="{bx + label_size * 1.15:.0f}" y="{by + label_size * 0.92:.0f}" text-anchor="middle" '
                f'font-family="Jost" font-weight="500" font-size="{label_size}" fill="#fff">{d}</text>')
    return (f'<div class="rimg" style="left:{x:.1f}mm;top:{y:.1f}mm;width:{w:.1f}mm;height:{h:.1f}mm">'
            f'<img src="{src(n).as_uri()}" style="width:100%;height:100%">'
            f'<svg class="ov" viewBox="0 0 {w_px} {h_px}" preserveAspectRatio="none">{svg}</svg></div>'), w


def crop(d):
    """Pixel crop of the original render, saved losslessly (no resampling, no retouch)."""
    CROPS.mkdir(parents=True, exist_ok=True)
    n, b = T.D[d][3], T.D[d][4]
    im = Image.open(src(n)).convert("RGB").crop(b)
    p = CROPS / f"{d}.png"
    im.save(p)
    return p, im.size


# ---------------------------------------------------------------- front matter
def front():
    logo = LOGO.read_text()
    body = f"""
<div class="cover-img"><img src="{src('01').as_uri()}"></div>
<div class="cover-txt">
  <div class="cv-logo">{logo}</div>
  <div class="cv-k">{DOC}</div>
  <h1>Douche principale<br>Étage 1</h1>
  <div class="cv-sub">Villa — salle d'eau principale</div>
  <div class="cv-list">Concept · Plans techniques cotés · Élévations · Rendus 3D · Détails décoratifs · Matériaux et finitions</div>
  <div class="cv-meta"><b>Indice {INDICE}</b> — {DATE}<br>Format A3 paysage · Cotes en centimètres</div>
  <div class="cv-warn draft">{STATUS}. Les plans cotés et les planches matériaux seront ajoutés à réception des
  documents de la salle d'eau. Aucune cote n'est inventée : <span class="st-c">COTE À CONFIRMER</span> sinon.</div>
</div>"""
    sheet("000", "Page de garde", "Généralités", "—", body)
    sheet("001", "Sommaire", "Généralités", "—", "__TOC__")
    rlist = "".join(f"<li><b>Rendu {n}</b> ({T.RENDERS[n][0]}) — {esc(T.RENDERS[n][2])}</li>" for n in T.RENDER_ORDER)
    conv = f"""
<div class="conv">
 <div class="col">
  <h2>Statut des cotes</h2>
  <table class="lg">
   <tr><td class="st-v big">424</td><td><b>Cote vérifiée</b> — écrite sur un plan coté de la salle d'eau fourni par
     KAÏRA. Reportée telle quelle.</td></tr>
   <tr><td class="st-d big"><i>≈ 59</i></td><td><b>Cote déduite</b> — relevée à l'échelle sur un document du projet
     (vue de dessus de la maquette 3D, rendu de face calibré sur une cote connue). Arrondie au centimètre.</td></tr>
   <tr><td class="st-c big">À CONF.</td><td><b>COTE À CONFIRMER</b> — aucune source dans les documents du projet.
     Dessinée sans valeur. Aucune cote n'est inventée.</td></tr>
  </table>
  <h2>Détails décoratifs (série 400)</h2>
  <ul class="nl">
   <li>Chaque détail est un <b>agrandissement signalé</b> : une zone du rendu 3D original, extraite sans retouche
     ni modification de couleur, et affichée plus grand.</li>
   <li>Sur chaque planche, le rendu entier reste présenté en grand ; la zone agrandie y est encadrée et numérotée
     (<span class="tag">D01</span> … <span class="tag">D29</span>).</li>
   <li>Le facteur d'agrandissement est indiqué sous chaque extrait, par rapport au rendu de la même planche.</li>
   <li>Les rendus de la série 300 sont les fichiers originaux, insérés entiers, sans recadrage ni retouche.</li>
  </ul>
 </div>
 <div class="col">
  <h2>Documents sources</h2>
  <ul class="nl">{rlist}</ul>
  <h2>Documents écartés</h2>
  <ul class="nl">
   <li><b>Plan coté IMG_7771</b> — ne correspond pas à la salle d'eau (chambres) : <b>non utilisé</b>, il n'est mélangé
     à aucun dessin de ce dossier.</li>
   <li>Sur ce plan, la cote écrite <b>« 478 »</b> ne correspond pas au dessin (≈ 386 cm à l'échelle des autres cotes) :
     <span class="st-c">À VÉRIFIER</span>. Ni la cote ni le dessin ne sont corrigés sans confirmation.</li>
  </ul>
  <h2>En attente</h2>
  <ul class="nl">
   <li>Plan de la salle d'eau (coté si possible) et son emplacement à l'étage 1 → série 200 : plan d'aménagement coté,
     élévations de chaque mur, coupes.</li>
   <li>Références réellement prévues (faïence, sol, terrazzo, robinetterie, vasque, miroir, luminaires, paroi) → série
     500 : planches matériaux et finitions.</li>
  </ul>
 </div>
</div>"""
    sheet("002", "Conventions, sources et méthode", "Généralités", "—", conv)


def concept():
    img, w = framed_render("06", AX, AY + 2, 200)
    t = """<div class="nh">Concept architectural et décoratif</div>
<p class="lead">Une salle d'eau calme et chaleureuse, où une base claire et minérale accueille trois accents francs :
le noyer, le bordeaux et le noir.</p>
<ul class="nl">
 <li><b>Une enveloppe minérale :</b> murs entièrement habillés de panneaux effet travertin à veinage horizontal, du sol
   au plafond.</li>
 <li><b>Un sol graphique :</b> grandes dalles blanches veinées aux angles arrondis et inserts noirs, un motif « galets »
   qui se poursuit dans la douche.</li>
 <li><b>Le bordeaux en accent :</b> faïence brillante posée à la verticale, réservée au fond de la douche et au coffrage
   du WC.</li>
 <li><b>Le bois :</b> meuble vasque suspendu, commode et petites étagères en noyer.</li>
 <li><b>Le noir en ligne :</b> paroi verrière, robinetterie, colonne de douche, porte-serviettes et patères.</li>
 <li><b>La lumière :</b> gorge LED en périphérie du plafond, miroir rétroéclairé et suspensions à globe.</li>
</ul>
<p class="small">Texte établi à partir des rendus 3D du projet ; à valider par KAÏRA.</p>"""
    body = img + box(AX + w + 8, AY + 4, AW - w - 10, t)
    body += box(AX, AY + 206, w, f'<p class="cap"><b>Rendu 06</b> — {esc(T.RENDERS["06"][1])}</p>')
    sheet("100", "Concept architectural et décoratif", "Présentation du projet", "—", body)


# ---------------------------------------------------------------- 300: renders, large format
def renders():
    for i, n in enumerate(T.RENDER_ORDER):
        name, cap, view = T.RENDERS[n]
        img, w = framed_render(n, AX, AY, AH)
        dets = [d for d in T.D if T.D[d][3] == n]
        li = "".join(f"<li><b>{d}</b> {esc(T.D[d][0])} <span class='small'>· pl. {plate_of(d)}</span></li>" for d in dets)
        side = (f'<div class="nh">Rendu {n}</div><p class="cap">{esc(cap)}</p><p class="small">{esc(view)} · fichier '
                f'{name}.png ({size(n)[0]} × {size(n)[1]} px) — rendu original KAÏRA, inséré en entier, sans recadrage '
                f'ni retouche.</p>' + (f'<div class="nh" style="margin-top:4mm">Détails extraits de ce rendu</div>'
                                       f'<ul class="nl">{li}</ul>' if li else ""))
        sheet(f"30{i + 1}", f"Rendu 3D {n} — {view}", "Rendus 3D", "—", img + box(AX + w + 6, AY + 4, AW - w - 6, side))


# ---------------------------------------------------------------- 400: details
def index_sheet():
    rows = ""
    for d, (title, desc, cat, n, b) in T.D.items():
        rows += (f'<tr><td class="ref">{d}</td><td><b>{esc(title)}</b><br><span class="small">{esc(desc)}</span></td>'
                 f'<td>{esc(cat)}</td><td>Rendu {n}</td><td>{plate_of(d)}</td></tr>')
    half = (len(T.D) + 1) // 2
    keys = list(T.D)

    def table(ks):
        r = "".join(rows.split("</tr>")[keys.index(k)] + "</tr>" for k in ks)
        return (f'<table class="tb2 full"><tr><th>N°</th><th>Élément</th><th>Catégorie</th><th>Source</th>'
                f'<th>Pl.</th></tr>{r}</table>')
    cats = "".join(f"<li><b>{esc(c)}</b> — {', '.join(d for d in T.D if T.D[d][2] == c)}</li>" for c in T.CATEGORIES)
    body = (box(AX + 2, AY + 2, 160, '<div class="nh">Index des détails décoratifs</div>' + table(keys[:half]))
            + box(AX + 168, AY + 9.5, 160, table(keys[half:]))
            + box(AX + 2, AY + 222, 326, f'<div class="nh">Par catégorie</div><ul class="nl cols2">{cats}</ul>'))
    sheet("400", "Index des détails décoratifs", "Détails décoratifs", "—", body)


def detail_plate(num, title, n, ds):
    BASE_H = 240
    img, w = framed_render(n, AX, AY + 2, BASE_H, ds)
    mm_per_px_base = w / size(n)[0]
    body = img + box(AX, AY + BASE_H + 4, w,
                     f'<p class="cap"><b>Rendu {n}</b> ({T.RENDERS[n][0]}) — rendu original entier. '
                     f'Les cadres numérotés repèrent les zones agrandies à droite.</p>')
    cx, cw = AX + w + 7, AW - w - 7
    cell_h = (AH - 2) / 3
    for j, d in enumerate(ds):
        title_d, desc, cat, _, _ = T.D[d]
        p, (pw, ph) = crop(d)
        max_w, max_h = cw, cell_h - 21
        s = min(max_w / pw, max_h / ph)                 # mm per px of the extract
        iw, ih = pw * s, ph * s
        y = AY + 1 + j * cell_h
        f = s / mm_per_px_base
        body += (f'<div class="zoom" style="left:{cx:.1f}mm;top:{y:.1f}mm;width:{iw:.1f}mm;height:{ih:.1f}mm">'
                 f'<img src="{p.as_uri()}"><span class="ztag">{d}</span></div>')
        body += box(cx, y + ih + 1.6, cw,
                    f'<p class="zt"><b>{d} · {esc(title_d)}</b></p><p class="zd">{esc(desc)}</p>'
                    f'<p class="zs">{esc(cat)} · extrait du rendu {n} · agrandissement ×{f:.1f}'.replace(".", ",")
                    + '</p>')
    sheet(num, f"Détails — {title}", "Détails décoratifs", "—", body)


# ---------------------------------------------------------------- title block, toc, page
def title_block(sh, page, total):
    logo = LOGO.read_text()
    return f"""<div class="tb">
 <div class="tb-logo">{logo}</div>
 <div class="tb-firm">KAÏRA INTERIOR DESIGN<span>Architecture intérieure</span></div>
 <div class="tb-sec"><label>Projet</label><div>{PROJECT}</div></div>
 <div class="tb-sec"><label>Document</label><div>{DOC}</div></div>
 <div class="tb-sec"><label>Série</label><div>{esc(sh['group'])}</div></div>
 <div class="tb-sec tb-title"><label>Titre de la planche</label><div>{esc(sh['title'])}</div></div>
 <div class="tb-grid">
  <div><label>Échelle</label>{sh['scale']}</div><div><label>Format</label>A3</div>
  <div><label>Date</label>{DATE}</div><div><label>Indice</label>{INDICE}</div>
 </div>
 <div class="tb-legend">
  <div><span class="st-v">424</span> cote vérifiée (plan source)</div>
  <div><span class="st-d"><i>≈ 59</i></span> cote déduite (relevé)</div>
  <div><span class="st-c">À CONF.</span> cote à confirmer</div>
 </div>
 <div class="tb-status">{STATUS}</div>
 <div class="tb-note">Cotes en cm. Ne pas mesurer sur le dessin. Toutes les cotes sont à vérifier sur site avant exécution.</div>
 <div class="tb-num"><label>N° de dessin</label><div>KAI-DPE-{sh['num']}</div></div>
 <div class="tb-page">Planche {page} / {total}</div>
</div>"""


def toc_html(total):
    out, cur = "", None
    for i, sh in enumerate(SHEETS, 1):
        if sh["group"] != cur:
            out += f'<div class="lv">{esc(sh["group"])}</div>'
            cur = sh["group"]
        out += (f'<div class="r"><b>KAI-DPE-{sh["num"]}</b><span class="t">{esc(sh["title"])}</span>'
                f'<span class="s">{sh["scale"]}</span><span class="p">{i}</span></div>')
    out += ('<div class="lv">À venir</div>'
            '<div class="r"><b>KAI-DPE-2xx</b><span class="t">Plans techniques : plan d\'aménagement coté, élévations de '
            'chaque mur, coupes — à réception du plan de la salle d\'eau</span><span class="s"></span><span class="p"></span></div>'
            '<div class="r"><b>KAI-DPE-5xx</b><span class="t">Matériaux et finitions : planches matériaux, textures, '
            'couleurs</span><span class="s"></span><span class="p"></span></div>')
    return f'<div class="toc">{out}</div>'


EXTRA_CSS = """
.rimg .ov{position:absolute;left:0;top:0;width:100%;height:100%}
.rimg{overflow:hidden}
.zoom{position:absolute;border:.25mm solid #3A2A22;overflow:hidden;background:#fff}
.zoom img{width:100%;height:100%;display:block;image-rendering:auto}
.ztag{position:absolute;left:0;top:0;background:#6E2234;color:#fff;font-weight:500;font-size:2.4mm;letter-spacing:.06em;
 padding:.6mm 1.6mm}
.zt{margin:0;font-size:2.55mm;color:#1E1E1E}
.zd{margin:.4mm 0 0;font-size:2.2mm;line-height:1.35;color:#3A2A22}
.zs{margin:.5mm 0 0;font-size:1.85mm;letter-spacing:.06em;text-transform:uppercase;color:#8A7B6E}
.tag{display:inline-block;background:#6E2234;color:#fff;font-weight:500;font-size:2mm;padding:0 1.2mm}
.lead{font-family:Cormorant;font-size:5.2mm;line-height:1.25;margin:0 0 4mm;color:#1E1E1E}
.cv-sub{font-size:3.2mm;letter-spacing:.14em;text-transform:uppercase;color:#3A2A22;margin:-2mm 0 6mm}
.cv-warn.draft{border-left-color:#6E2234}
.tb-status{font-size:2.05mm;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:#6E2234;
 border:.25mm solid #6E2234;padding:1.2mm 1.6mm;text-align:center}
.nl.cols2{columns:2;column-gap:8mm}
"""


def main():
    BUILD.mkdir(exist_ok=True)
    front()
    concept()
    renders()
    index_sheet()
    for p in T.PLATES:
        detail_plate(*p)
    total = len(SHEETS)
    pages = [f'<section class="sheet"><div class="frame"></div>'
             f'{toc_html(total) if sh["body"] == "__TOC__" else sh["body"]}{title_block(sh, i, total)}</section>'
             for i, sh in enumerate(SHEETS, 1)]
    css = (VB.CSS + EXTRA_CSS).replace("FONTS/", FONTS.as_uri() + "/")
    doc = (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>KAÏRA — {PROJECT}</title>'
           f'<style>{css}</style></head><body>{"".join(pages)}</body></html>')
    out_html = BUILD / "dossier-douche-etage1.html"
    out_html.write_text(doc, encoding="utf-8")
    print(total, "planches")
    js = f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage();
 await p.goto('file://{out_html}', {{ waitUntil: 'networkidle' }});
 await p.evaluate(() => document.fonts.ready);
 await p.pdf({{ path: '{OUT_PDF}', width: '420mm', height: '297mm', printBackground: true, preferCSSPageSize: true }});
 if (process.argv[1]) {{
  await p.setViewportSize({{ width: 1588, height: 1123 }});
  const els = await p.$$('section.sheet');
  for (let i = 0; i < els.length; i++) await els[i].screenshot({{ path: '{BUILD}/prev-' + String(i + 1).padStart(2, '0') + '.png' }});
 }}
 await b.close(); }})();"""
    args = ["node", "-e", js] + (["prev"] if "--previews" in sys.argv else [])
    subprocess.run(args, check=True, cwd=str(REPO / "projects/instagram-lancement/tools"))
    print(OUT_PDF)


if __name__ == "__main__":
    main()
