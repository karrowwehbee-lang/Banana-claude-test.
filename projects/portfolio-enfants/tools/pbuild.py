"""KAÏRA Interior Design — Portfolio « Chambres d'enfants » (PDF, 360 × 240 mm, 3:2 like the renders).

Usage: python3 tools/pbuild.py [--previews]
"""
import html
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pdata
import pviews as V

ROOT = HERE.parent
REPO = ROOT.parent.parent
SRC = ROOT / "sources/recus"
FONTS = REPO / "projects/dossier-client/build/fonts"
LOGO_DIR = REPO / "projects/kaira-logo/logo/svg"
BUILD = ROOT / "build"
OUT = REPO / "livrables/KAIRA-Portfolio-Chambres-enfants.pdf"

PW, PH = 360, 240
M = 20            # outer margin
INSTAGRAM = "@kaira.interior.design"

PAGES = []


def page(body, cls="", footer=True, header=None, toc=None):
    PAGES.append(dict(body=body, cls=cls, footer=footer, header=header, toc=toc))


def esc(t):
    return html.escape(str(t))


def img(p):
    return (SRC / p["img"]).as_uri()


def logo(name):
    return (LOGO_DIR / name).read_text()


def box(x, y, w, inner, cls="", h=None, style=""):
    hh = f"height:{h}mm;" if h is not None else ""
    return f'<div class="b {cls}" style="left:{x}mm;top:{y}mm;width:{w}mm;{hh}{style}">{inner}</div>'


def svgbox(svg, x, y):
    return f'<div class="b" style="left:{x:.1f}mm;top:{y:.1f}mm">{svg}</div>'


def caption_view(x, y, w, title, scale):
    return box(x, y, w, f'<div class="vt"><span>{esc(title)}</span><span class="sc">{scale}</span></div>')


# ============================================================================ front pages
def cover():
    p = pdata.PROJECTS[4]
    body = (f'<div class="b cover-img" style="left:118mm;top:20mm;width:222mm;height:148mm"><img src="{img(p)}"></div>'
            + box(M, 22, 86, f'<div class="cv-logo">{logo("kaira-2-alternative-stacked-chocolate.svg")}</div>')
            + box(M, 112, 92, '<div class="k">Portfolio — Collection 2026</div><h1 class="cv">Chambres<br>d\'enfants</h1>'
                              '<div class="cv-sub">Architecture intérieure · Mobilier sur mesure · Plans techniques</div>')
            + box(118, 176, 222, '<div class="cv-strip">' + "".join(
                f'<span><b>{q["num"]}</b> {esc(q["name"])}</span>' for q in pdata.PROJECTS) + '</div>')
            + box(M, 212, 120, f'<div class="cv-ig">{INSTAGRAM}</div>'))
    page(body, "cream", footer=False)


def studio():
    body = (box(M, 26, 120, '<div class="k">Le studio</div><h2 class="big">KAÏRA<br>Interior Design</h2>')
            + box(M, 92, 128, '<p class="lead">KAÏRA Interior Design conçoit des intérieurs sur mesure, de l\'intention '
                              'à l\'esquisse, du rendu 3D aux plans techniques. Chaque projet naît d\'une écoute attentive '
                              'et se construit autour d\'une idée simple, déclinée avec rigueur dans les volumes, les matières '
                              'et la lumière.</p><p>Pour les chambres d\'enfants, le studio cherche l\'équilibre entre '
                              'poésie et justesse : des formes douces qui rassurent, des matières naturelles et faciles à '
                              'vivre, une lumière indirecte qui accompagne le sommeil, et des rangements pensés pour '
                              'grandir avec l\'enfant.</p>')
            + box(176, 26, 150, f'<div class="emblem">{logo("kaira-3b-monogram-arch-emblem-olive.svg")}</div>')
            + box(176, 150, 164, '<div class="pillars">'
                  '<div><b>Concevoir</b><span>Concept, ambiance, palette et matières, présentés en planches.</span></div>'
                  '<div><b>Dessiner</b><span>Mobilier sur mesure, élévations, coupes et plans cotés.</span></div>'
                  '<div><b>Visualiser</b><span>Rendus 3D réalistes pour décider en confiance.</span></div></div>'))
    page(body, "white")


def contents():
    page("__TOC__", "cream")


def intro():
    body = (box(M, 26, 130, '<div class="k">La collection</div><h2 class="big">Cinq chambres,<br>une même écriture</h2>')
            + box(M, 92, 140, '<p class="lead">Arches, festons, nuages : la collection décline un vocabulaire de formes '
                              'douces, dessinées directement dans le mobilier sur mesure plutôt que rapportées en '
                              'décoration.</p><p>Chaque chambre possède sa palette — rose poudré, vert olive, caramel — '
                              'toujours ancrée dans des tons naturels, crème et bois clair. La lumière y est indirecte, '
                              'intégrée aux niches, aux arches et aux têtes de lit. Chaque projet est présenté comme un '
                              'concept complet : intention, matières, mobilier, plans, élévations et coupes.</p>')
            + box(176, 26, 164, '<div class="principles">'
                  '<div><i>01</i><b>Formes douces</b><span>Aucun angle vif à hauteur d\'enfant : arches, panneaux arrondis, '
                  'festons tapissés.</span></div>'
                  '<div><i>02</i><b>Palettes naturelles</b><span>Crème, bois clair et une couleur signature par chambre.</span></div>'
                  '<div><i>03</i><b>Lumière indirecte</b><span>LED 2700 K intégrées, sans source visible depuis le lit.</span></div>'
                  '<div><i>04</i><b>Rangements intégrés</b><span>Armoires, niches et bibliothèques dessinées avec les murs.</span></div>'
                  '<div><i>05</i><b>Chambres évolutives</b><span>Bureaux, lits gigognes et rangements qui suivent l\'âge.</span></div>'
                  '</div>')
            + box(M, 182, PW - 2 * M, '<div class="thumbs">' + "".join(
                f'<figure><img src="{img(q)}"><figcaption><b>{q["num"]}</b> {esc(q["name"])}</figcaption></figure>'
                for q in pdata.PROJECTS) + '</div>'))
    page(body, "white")


# ============================================================================ project pages
def project(p):
    head = f'{p["num"]} — {p["name"]}'
    # a. opener: the render, full page, untouched
    page(f'<div class="b full"><img src="{img(p)}"></div>', "black", footer=False, toc=(p["num"], p["name"], p["type"]))
    # b. concept
    facts = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in p["facts"])
    chips = "".join(f'<div class="chip"><span style="background:{V.color_of(p, k)}"></span><em>{V.color_of(p, k)}</em></div>'
                    for k in p["palette"])
    body = (box(M, 24, 120, f'<div class="num">{p["num"]}</div><h2 class="pname">{esc(p["name"])}</h2>'
                            f'<div class="k">{esc(p["type"])}</div><p class="tag">{esc(p["tagline"])}</p>')
            + box(M, 132, 120, f'<table class="facts">{facts}</table>')
            + box(158, 24, 182, '<div class="nh">Concept</div>' + "".join(f"<p>{esc(t)}</p>" for t in p["concept"])
                  + f'<div class="nh">Ambiance</div><p>{esc(p["ambiance"])}</p>'
                  + f'<div class="nh">Lumière</div><p>{esc(p["lumiere"])}</p>')
            + box(158, 176, 182, f'<div class="nh">Palette relevée sur le rendu</div><div class="chips">{chips}</div>'))
    page(body, "cream", header=head)
    # c. materials board
    tiles = ""
    for i, (name, use, ck, pat) in enumerate(p["materials"]):
        col = V.color_of(p, ck)
        tiles += (f'<div class="tile">{V.texture_tile(col, pat, 34, seed=i + 3)}<b>{esc(name)}</b><span>{esc(use)}</span>'
                  f'<em>{col}</em></div>')
    body = (box(M, 22, 300, '<div class="k">Matériaux, couleurs et textures</div><h3 class="sec">La matière de la chambre</h3>')
            + box(M, 52, PW - 2 * M, f'<div class="tiles">{tiles}</div>')
            + box(M, 214, 300, '<p class="small">Teintes relevées directement sur le rendu 3D (valeur médiane d\'une zone de '
                               'la matière) ; textures en représentation graphique. Références fabricants et finitions '
                               'définitives à valider sur échantillons.</p>'))
    page(body, "white", header=head)
    # d. custom furniture cards
    cards = ""
    for ref, name, dims, desc, front, side in p["furniture"]:
        wall, x0, x1, z0, z1 = front
        Pd, Hd, lev, pl = side
        best = None
        for sc in (10, 15, 20, 25, 30, 40, 50):
            f_svg, fw, fh = V.elevation(p, wall, scale=sc, crop=(x0, x1, z0, z1), dims=True, labels=False,
                                        margins=(4, 4, 4, 4))
            s_svg, sw_, sh_ = V.side_profile(Pd, Hd, lev, pl, sc) if Pd >= 8 else ("", 0, 0)
            if fw + sw_ + 4 <= 96 and max(fh, sh_) <= 68:
                best = (sc, f_svg, fw, fh, s_svg, sw_, sh_)
                break
        sc, f_svg, fw, fh, s_svg, sw_, sh_ = best or (sc, f_svg, fw, fh, s_svg, sw_, sh_)
        cards += (f'<div class="card"><div class="cd"><div class="fr">{f_svg}</div><div class="sd">{s_svg}</div></div>'
                  f'<div class="ct"><span class="ref">{ref}</span><b>{esc(name)}</b><span class="sc">1:{sc}</span></div>'
                  f'<div class="dm">{esc(dims)}</div><p>{esc(desc)}</p></div>')
    body = (box(M, 22, 300, '<div class="k">Mobilier sur mesure</div><h3 class="sec">Dessiné pour la chambre</h3>')
            + box(M, 50, PW - 2 * M, f'<div class="cards">{cards}</div>'))
    page(body, "white", header=head)
    # e. architecture & decor
    els = "".join(f"<li><i>{i + 1:02d}</i>{esc(e)}</li>" for i, e in enumerate(p["elements"]))
    body = (f'<div class="b framed" style="left:{M}mm;top:34mm;width:204mm;height:136mm"><img src="{img(p)}"></div>'
            + box(M, 174, 204, f'<p class="small">{esc(p["name"])} — rendu 3D original, présenté en entier.</p>')
            + box(236, 30, 104, '<div class="k">Architecture et décor</div><h3 class="sec">Les éléments du projet</h3>'
                                f'<ol class="els">{els}</ol>'))
    page(body, "cream", header=head)
    # f. plan
    for sc in (25, 30, 40):
        svg, w, h = V.plan(p, sc)
        if w <= 234 and h <= 192:
            break
    legend = "".join(f'<tr><td class="ref">{r}</td><td>{esc(n)}</td><td>{esc(d)}</td></tr>' for r, n, d, *_ in p["furniture"])
    R = p["room"]
    body = (svgbox(svg, M + (234 - w) / 2, 24 + (192 - h) / 2)
            + caption_view(M, 218, 234, f"Plan d'aménagement — {p['name']}", f"1:{sc}")
            + box(262, 24, 78, '<div class="k">Plan d\'aménagement</div>'
                               f'<h3 class="sec">{R["W"]} × {R["D"]} cm</h3>'
                               f'<p class="small">Surface proposée {R["W"] * R["D"] / 1e4:.1f} m² · hauteur sous plafond {R["H"]}.'
                               .replace(".", ",", 1) + '</p>'
                               f'<table class="leg">{legend}</table>'
                               '<p class="note">Dimensions proposées pour le concept, cohérentes avec le mobilier du rendu. '
                               'À adapter aux mesures réelles après relevé du site. Cotes en cm.</p>'))
    page(body, "white", header=head)
    # g. main elevation
    E = p["walls"]["A"]
    for sc in (20, 25, 30):
        svg, w, h = V.elevation(p, "A", sc)
        if w <= PW - 2 * M and h <= 168:
            break
    body = (svgbox(svg, (PW - w) / 2, 24)
            + caption_view(M, 24 + h + 3, PW - 2 * M, f"Élévation — {E['title']}", f"1:{sc}")
            + box(M, 24 + h + 14, PW - 2 * M, '<p class="note">Élévation du mur décoratif. Dimensions proposées pour le concept '
                                                '(cm), à confirmer après relevé. Les tracés dorés indiquent les éclairages LED '
                                                'intégrés (2700 K proposé).</p>'))
    page(body, "white", header=head)
    # h. section (+ second elevation when there is one)
    others = [k for k in p["walls"] if k != "A"]
    if others:
        k = others[0]
        for scs in (30, 40):
            sv, sw_, sh_ = V.section(p, scs)
            ev, ew, eh = V.elevation(p, k, scs)
            if sw_ + ew + 8 <= PW - 2 * M:
                break
        gap = (PW - 2 * M - sw_ - ew) / 3
        yb = 30 + max(sh_, eh)
        body = (svgbox(sv, M + gap, yb - sh_) + caption_view(M + gap, yb + 2, sw_, p["section"]["title"], f"1:{scs}")
                + svgbox(ev, M + 2 * gap + sw_, yb - eh)
                + caption_view(M + 2 * gap + sw_, yb + 2, ew, f"Élévation — {p['walls'][k]['title']}", f"1:{scs}"))
    else:
        sv, sw_, sh_ = V.section(p, 30)
        dv, dw, dh = V.section(p, 10, crop=(-15, 95, -10, 130))
        gap = (PW - 2 * M - sw_ - dw) / 3
        yb = 24 + max(sh_, dh)
        body = (svgbox(sv, M + gap, yb - sh_) + caption_view(M + gap, yb + 2, sw_, p["section"]["title"], "1:30")
                + svgbox(dv, M + 2 * gap + sw_, yb - dh)
                + caption_view(M + 2 * gap + sw_, yb + 2, dw, "Détail — lit, tête de lit et mur", "1:10"))
    body += box(M, 206, PW - 2 * M, '<p class="note">Coupe de principe : hauteurs, profondeurs du mobilier et éclairages. '
                                    'Structure, épaisseurs de dalle et réseaux à définir avec le relevé du site. Dimensions '
                                    'proposées pour le concept, en cm.</p>')
    page(body, "white", header=head)


# ============================================================================ closing pages
def notes():
    body = (box(M, 26, 140, '<div class="k">Notes</div><h2 class="big">Du concept<br>à la réalisation</h2>')
            + box(176, 30, 164, '<div class="nh">Dimensions</div><p>Les cotes de ce portfolio sont des dimensions '
                                'proposées pour chaque concept, établies à partir des proportions du mobilier visible sur '
                                'les rendus et de dimensions courantes (lit bébé 60 × 120, couchage 90 × 200, armoires de '
                                '60 de profondeur, bibliothèques de 35). Elles ne constituent pas un relevé : pour chaque '
                                'réalisation, elles sont ajustées aux mesures réelles de la pièce.</p>'
                                '<div class="nh">Sécurité et confort</div><p>Fixation murale de tous les meubles hauts, '
                                'angles arrondis, LED basse tension dans des profilés fermés, peintures et vernis à très '
                                'faibles émissions (étiquette A+), textiles adaptés aux enfants.</p>'
                                '<div class="nh">Étapes</div><p>Relevé du site · validation du concept et des '
                                'échantillons · plans d\'exécution du mobilier sur mesure · coordination de la fabrication '
                                'et de la pose.</p>'))
    page(body, "white")


def final():
    body = (box(0, 0, PW, f'<div class="fin-logo">{logo("kaira-2-alternative-stacked-ivory.svg")}</div>', h=150)
            + box(0, 156, PW, '<div class="fin-t">Architecture intérieure · Chambres d\'enfants</div>'
                              f'<div class="fin-ig">{INSTAGRAM}</div>'
                              '<div class="fin-s">instagram.com/kaira.interior.design</div>'))
    page(body, "olive", footer=False)


# ============================================================================ assembly
CSS = """
@font-face{font-family:Jost;font-weight:300;src:url(FONTS/jost-latin-300-normal.woff2)}
@font-face{font-family:Jost;font-weight:400;src:url(FONTS/jost-latin-400-normal.woff2)}
@font-face{font-family:Jost;font-weight:500;src:url(FONTS/jost-latin-500-normal.woff2)}
@font-face{font-family:Cormorant;font-weight:300;src:url(FONTS/cormorant-garamond-latin-300-normal.woff2)}
@font-face{font-family:Cormorant;font-weight:400;src:url(FONTS/cormorant-garamond-latin-400-normal.woff2)}
@font-face{font-family:Cormorant;font-weight:300;font-style:italic;src:url(FONTS/cormorant-garamond-latin-300-italic.woff2)}
@font-face{font-family:Cormorant;font-weight:400;font-style:italic;src:url(FONTS/cormorant-garamond-latin-400-italic.woff2)}
@page{size:360mm 240mm;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;font-family:Jost;font-weight:300;color:#2B2622}
.pg{position:relative;width:360mm;height:240mm;overflow:hidden;page-break-after:always}
.pg.white{background:#FFFFFF}.pg.cream{background:#F6F1EA}.pg.black{background:#F6F1EA}.pg.olive{background:#5F6A45;color:#F6F1EA}
.b{position:absolute}
.full{left:0;top:0;width:360mm;height:240mm}.full img{width:100%;height:100%;display:block;object-fit:contain}
.framed,.cover-img{display:flex;align-items:center;justify-content:center}.framed img,.cover-img img{max-width:100%;max-height:100%;display:block}
.k{font-size:2.5mm;letter-spacing:.32em;text-transform:uppercase;color:#8A7B6E;font-weight:400}
h1.cv{font-family:Cormorant;font-weight:300;font-size:21mm;line-height:.95;margin:4mm 0 6mm;color:#2B2622}
.cv-logo svg{width:62mm;height:auto}
.cv-sub{font-size:3mm;line-height:1.6;color:#5F6A45;letter-spacing:.04em}
.cv-strip{display:flex;justify-content:space-between;border-top:.25mm solid #2B2622;padding-top:2.5mm;font-size:2.5mm;
 letter-spacing:.14em;text-transform:uppercase;color:#5B4F46}.cv-strip b{color:#5F6A45;font-weight:500;margin-right:1.2mm}
.cv-ig{font-size:3mm;letter-spacing:.2em;color:#5F6A45}
h2.big{font-family:Cormorant;font-weight:300;font-size:15mm;line-height:1.02;margin:4mm 0 0}
p{font-size:3.05mm;line-height:1.62;margin:0 0 3.2mm}
p.lead{font-family:Cormorant;font-size:5.6mm;line-height:1.38;font-weight:400;color:#2B2622}
.emblem svg{width:70mm;height:auto;opacity:.9;display:block;margin:0 auto}
.pillars{display:flex;gap:7mm}.pillars div{flex:1;border-top:.3mm solid #5F6A45;padding-top:3mm}
.pillars b,.principles b{display:block;font-family:Cormorant;font-weight:400;font-size:5.6mm;margin-bottom:1.5mm}
.pillars span,.principles span{font-size:2.8mm;line-height:1.55;color:#5B4F46}
.principles div{display:grid;grid-template-columns:12mm 1fr;grid-template-rows:auto auto;border-top:.2mm solid #D9CFC2;padding:2.6mm 0}
.principles i{grid-row:span 2;font-family:Cormorant;font-style:italic;font-size:6mm;color:#5F6A45}
.thumbs{display:flex;gap:4mm}.thumbs figure{margin:0;flex:1}.thumbs img{width:100%;display:block}
.thumbs figcaption{font-size:2.4mm;letter-spacing:.16em;text-transform:uppercase;margin-top:1.6mm;color:#5B4F46}
.thumbs b{color:#5F6A45;font-weight:500;margin-right:1mm}
.num{font-family:Cormorant;font-style:italic;font-weight:300;font-size:20mm;line-height:1;color:#5F6A45}
h2.pname{font-family:Cormorant;font-weight:300;font-size:17mm;line-height:1;margin:2mm 0 4mm}
p.tag{font-family:Cormorant;font-style:italic;font-size:5.4mm;line-height:1.35;margin-top:5mm;color:#3B3430}
table.facts{border-collapse:collapse;width:100%;font-size:2.8mm}
table.facts td{padding:1.9mm 0;border-bottom:.2mm solid #D9CFC2;vertical-align:top}
table.facts td:first-child{color:#8A7B6E;letter-spacing:.12em;text-transform:uppercase;font-size:2.2mm;width:42mm;padding-top:2.3mm}
.nh{font-size:2.4mm;letter-spacing:.28em;text-transform:uppercase;color:#5F6A45;font-weight:500;margin:0 0 1.8mm}
.chips{display:flex;gap:4mm}.chip{flex:1}.chip span{display:block;height:16mm;border-radius:.6mm}
.chip em{display:block;font-style:normal;font-size:2.2mm;letter-spacing:.1em;color:#8A7B6E;margin-top:1.4mm}
h3.sec{font-family:Cormorant;font-weight:300;font-size:10mm;line-height:1.05;margin:2.5mm 0 0}
.tiles{display:grid;grid-template-columns:repeat(5,1fr);gap:7mm 6mm}
.tile svg{display:block;width:34mm;height:34mm;border-radius:.6mm}
.tile b{display:block;font-family:Cormorant;font-weight:400;font-size:4.6mm;margin:2.4mm 0 .6mm;line-height:1.1}
.tile span{display:block;font-size:2.45mm;line-height:1.45;color:#5B4F46}
.tile em{display:block;font-style:normal;font-size:2.1mm;letter-spacing:.1em;color:#8A7B6E;margin-top:.8mm}
.small{font-size:2.45mm;color:#8A7B6E;line-height:1.5}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:7mm 7mm}
.card{border-top:.3mm solid #2B2622;padding-top:2.5mm}
.cd{height:70mm;display:flex;align-items:flex-end;gap:3mm}.cd svg{display:block}
.ct{display:flex;align-items:baseline;gap:2mm;margin-top:2mm}.ct b{font-family:Cormorant;font-weight:400;font-size:4.6mm;flex:1}
.ref{font-size:2.3mm;font-weight:500;color:#5F6A45;border:.25mm solid #5F6A45;border-radius:3mm;padding:.2mm 1.6mm}
.ct .sc{font-size:2.2mm;color:#8A7B6E}
.dm{font-size:2.6mm;letter-spacing:.06em;color:#5F6A45;margin:.8mm 0 1.2mm}
.card p{font-size:2.5mm;line-height:1.5;color:#5B4F46;margin:0}
ol.els{list-style:none;padding:0;margin:6mm 0 0}ol.els li{display:grid;grid-template-columns:9mm 1fr;font-size:2.85mm;line-height:1.5;
 padding:1.9mm 0;border-bottom:.2mm solid #D9CFC2}ol.els i{font-family:Cormorant;font-style:italic;font-size:4.4mm;color:#5F6A45;line-height:1}
.vt{display:flex;justify-content:space-between;border-top:.35mm solid #2B2622;padding-top:1.2mm;font-size:2.35mm;
 letter-spacing:.16em;text-transform:uppercase}.vt .sc{color:#8A7B6E;letter-spacing:.08em}
table.leg{border-collapse:collapse;width:100%;font-size:2.45mm;margin:4mm 0}
table.leg td{padding:1.6mm 1mm 1.6mm 0;border-bottom:.2mm solid #E4DACB;vertical-align:top;line-height:1.4}
table.leg td.ref{font-weight:500;color:#5F6A45;width:9mm}
.note{font-size:2.45mm;line-height:1.5;color:#5B4F46;border-left:.5mm solid #5F6A45;padding-left:2.5mm}
.hdr{position:absolute;left:20mm;top:9mm;font-size:2.3mm;letter-spacing:.3em;text-transform:uppercase;color:#8A7B6E}
.ftr{position:absolute;left:20mm;right:20mm;bottom:8mm;display:flex;justify-content:space-between;font-size:2.2mm;
 letter-spacing:.3em;text-transform:uppercase;color:#8A7B6E}
.fin-logo{display:flex;align-items:flex-end;justify-content:center;height:150mm}.fin-logo svg{width:110mm;height:auto}
.fin-t{text-align:center;font-size:2.8mm;letter-spacing:.34em;text-transform:uppercase;opacity:.85}
.fin-ig{text-align:center;font-family:Cormorant;font-weight:300;font-size:11mm;margin-top:9mm}
.fin-s{text-align:center;font-size:2.5mm;letter-spacing:.2em;opacity:.7;margin-top:2mm}
.toc{position:absolute;left:20mm;top:26mm;width:320mm}
.toc .row{display:grid;grid-template-columns:18mm 1fr 60mm 14mm;align-items:baseline;border-bottom:.2mm solid #D9CFC2;padding:3.1mm 0}
.toc .row i{font-family:Cormorant;font-style:italic;font-size:7mm;color:#5F6A45}
.toc .row b{font-family:Cormorant;font-weight:300;font-size:8mm}.toc .row span{font-size:2.5mm;letter-spacing:.2em;
 text-transform:uppercase;color:#8A7B6E}.toc .row em{font-style:normal;text-align:right;font-size:3mm}
"""


def toc_html():
    rows = [("—", "Le studio", "KAÏRA Interior Design", 2), ("—", "La collection", "Cinq chambres, une même écriture", 4)]
    for i, pg in enumerate(PAGES, 1):
        if pg["toc"]:
            n, name, typ = pg["toc"]
            rows.append((n, name, typ, i))
    rows.append(("—", "Notes", "Du concept à la réalisation", len(PAGES) - 1))
    return ('<div class="toc"><div class="k">Sommaire</div><div style="height:6mm"></div>' + "".join(
        f'<div class="row"><i>{n}</i><b>{esc(t)}</b><span>{esc(s)}</span><em>{p:02d}</em></div>' for n, t, s, p in rows)
        + "</div>")


def main():
    BUILD.mkdir(exist_ok=True)
    cover(); studio(); contents(); intro()
    for p in pdata.PROJECTS:
        project(p)
    notes(); final()
    out = []
    for i, pg in enumerate(PAGES, 1):
        body = toc_html() if pg["body"] == "__TOC__" else pg["body"]
        hdr = f'<div class="hdr">{esc(pg["header"])}</div>' if pg["header"] else ""
        ftr = (f'<div class="ftr"><span>KAÏRA Interior Design — Chambres d\'enfants</span><span>{i:02d}</span></div>'
               if pg["footer"] else "")
        out.append(f'<section class="pg {pg["cls"]}">{body}{hdr}{ftr}</section>')
    css = CSS.replace("FONTS/", FONTS.as_uri() + "/")
    doc = (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>KAÏRA Interior Design — Chambres d\'enfants</title>'
           f'<style>{css}</style></head><body>{"".join(out)}</body></html>')
    (BUILD / "portfolio.html").write_text(doc, encoding="utf-8")
    print(len(PAGES), "pages")
    js = f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage();
 await p.goto('file://{BUILD / "portfolio.html"}', {{ waitUntil: 'networkidle' }}); await p.evaluate(() => document.fonts.ready);
 await p.pdf({{ path: '{OUT}', width: '360mm', height: '240mm', printBackground: true, preferCSSPageSize: true }});
 if (process.argv[1]) {{ await p.setViewportSize({{ width: 1361, height: 907 }});
  const els = await p.$$('section.pg');
  for (let i = 0; i < els.length; i++) await els[i].screenshot({{ path: '{BUILD}/p-' + String(i + 1).padStart(2, '0') + '.png' }}); }}
 await b.close(); }})();"""
    subprocess.run(["node", "-e", js] + (["prev"] if "--previews" in sys.argv else []), check=True,
                   cwd=str(REPO / "projects/instagram-lancement/tools"))
    print(OUT)


if __name__ == "__main__":
    main()
