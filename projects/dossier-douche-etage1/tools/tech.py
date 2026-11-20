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
import views_dpe as V  # noqa: E402

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

PROJECT = "Villa — Douche principale – Étage 1"
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
  <h1>Douche principale<br>– Étage 1</h1>
  <div class="cv-sub">Villa · dossier indépendant</div>
  <div class="cv-list">Concept · Plans techniques cotés · Élévations · Rendus 3D · Détails décoratifs · Matériaux et finitions</div>
  <div class="cv-meta"><b>Indice {INDICE}</b> — {DATE}<br>Format A3 paysage · Cotes en centimètres</div>
  <div class="cv-warn draft">Document établi à partir du plan coté et des rendus 3D du projet. Chaque cote est classée :
  <span class="st-v">vérifiée</span>, <span class="st-d">≈ déduite</span> ou <span class="st-c">à confirmer</span>
  (planche 002). Aucune cote n'a été inventée.</div>
</div>"""
    sheet("000", "Page de garde", "Généralités", "—", body)
    sheet("001", "Sommaire", "Généralités", "—", "__TOC__")
    rlist = "".join(f"<li><b>Rendu {n}</b> ({T.RENDERS[n][0]}) — {esc(T.RENDERS[n][2])}</li>" for n in T.RENDER_ORDER)
    conv = f"""
<div class="conv">
 <div class="col">
  <h2>Statut des cotes</h2>
  <table class="lg">
   <tr><td class="st-v big">424</td><td><b>Cote vérifiée</b> — écrite sur le plan coté de la douche principale fourni par
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
  <h2>Méthode de relevé</h2>
  <ul class="nl">
   <li><b>Plan :</b> plan coté IMG_7771, partie gauche en L = la douche principale. Cotes écrites reprises telles quelles :
     374,80 · 234,10 · 137,00 · 164,80 · 66 · 74 · 70 · 116 · 40. Échelle du dessin 0,577 cm/px (contrôlée sur ses cotes).</li>
   <li><b>Équipements en plan :</b> vue de dessus IMG_7773 (caméra en perspective) recalée sur le plan coté :
     largeur du retour 164 relevée contre 164,80 écrite.</li>
   <li><b>Hauteurs :</b> rendus de face (perspective à un point) calibrés sur un mur de largeur connue : 02 (mur sud),
     06 (mur est, 234,10), 08 (fond de douche, 164,80). Contrôles croisés : plafond 289 / 289 / 288 ; porte 202 / 203 ;
     bord de porte 236 relevé contre 230,8 écrit ; coffrage 119 relevé contre 116 écrit.</li>
  </ul>
  <h2>Documents sources</h2>
  <ul class="nl"><li><b>Plan coté</b> (IMG_7771) — partie gauche en L, <b>identifiée par KAÏRA</b> sur le plan annoté
     (flèche sur la porte de 74)</li>{rlist}</ul>
  <h2>Documents écartés</h2>
  <ul class="nl">
   <li><b>Partie droite du plan coté</b> (chambre) : hors dossier — non mélangée aux dessins de la douche principale.</li>
   <li>Sur cette partie, la cote écrite <b>« 478 »</b> ne correspond pas au dessin (≈ 386 à l'échelle des autres cotes) :
     <span class="st-c">À VÉRIFIER</span>. Ni la cote ni le dessin ne sont corrigés sans confirmation.</li>
  </ul>
 </div>
</div>"""
    sheet("002", "Conventions, sources et méthode", "Généralités", "—", conv)


def concept():
    img, w = framed_render("06", AX, AY + 2, 200)
    t = """<div class="nh">Concept architectural et décoratif</div>
<p class="lead">La douche principale : un espace calme et chaleureux, où une base claire et minérale accueille trois accents francs :
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


# ---------------------------------------------------------------- 200: plans, elevations, sections, furniture
def place(svg, x, y):
    return f'<div class="v" style="left:{x:.1f}mm;top:{y:.1f}mm">{svg}</div>'


def vtitle(x, y, w, letter, title, scale):
    return (f'<div class="vt" style="left:{x:.1f}mm;top:{y:.1f}mm;width:{w:.1f}mm"><span class="vn">{letter}</span>'
            f'<span class="vtt">{esc(title)}</span><span class="vs">{scale}</span></div>')


def notes(items, title="Notes"):
    li = "".join(f"<li>{n}</li>" for n in items)
    return f'<div class="nh">{title}</div><ul class="nl">{li}</ul>'


def keyplan(x, y):
    svg, w, h = V.plan(scale=80, mode="key")
    return place(svg, x, y) + box(x, y + h - 2, w, '<div class="kpt">Plan de repérage des vues</div>'), w, h


def drawing_sheet(num, title, scale, svg_w_h, letter, vt, side_items, render=None, side_title="Notes"):
    svg, w, h = svg_w_h
    body = place(svg, AX, AY + 2) + vtitle(AX + 4, AY + 2 + h + 1, w - 8, letter, vt, scale)
    sx = AX + w + 6
    sw = AW - w - 6
    kp, kw, kh = keyplan(sx, AY + 4)
    body += kp
    y = AY + 4 + kh + 6
    if render:
        n, cap = render
        rw = min(sw - 2, 70)
        rh = rw * size(n)[1] / size(n)[0]
        body += (f'<div class="rimg" style="left:{sx:.1f}mm;top:{y:.1f}mm;width:{rw:.1f}mm;height:{rh:.1f}mm">'
                 f'<img src="{src(n).as_uri()}" style="width:100%;height:100%"></div>')
        body += box(sx, y + rh + 1.2, rw, f'<p class="small">Rendu {n} — {esc(cap)}</p>')
        y += rh + 10
    body += box(sx, y, sw - 2, notes(side_items, side_title))
    sheet(num, title, "Plans techniques", scale, body)


def series200():
    import geom as G
    common = ["Cotes en cm. <span class='st-v'>Noir</span> : écrite sur le plan coté ; <span class='st-d'><i>olive ≈</i></span> : "
              "relevée (tolérance ±3 cm en plan, ±5 cm en hauteur) ; <span class='st-c'>bordeaux</span> : à confirmer.",
              "Hauteurs depuis le sol fini. Hauteur sous plafond ≈ 289 (trois rendus : 289, 289, 288)."]
    # 201 — plan coté
    svg, w, h = V.plan(20, "cote")
    side = notes([
        "Contour de la douche principale : cotes écrites du plan coté IMG_7771 (partie gauche en L, identifiée par KAÏRA sur le "
        "plan annoté). La pièce voisine et la chambre ne font pas partie de ce dossier.",
        "Porte P1 de 74 : désignée par KAÏRA sur le plan annoté comme la porte de la douche principale.",
        "Mur nord de la partie large : 66 · porte 74 · 70 (cotes écrites). Coffrage du WC : 116 × 40 (cotes écrites).",
        "Équipements placés d'après la vue de dessus IMG_7773 recalée sur le plan coté, et contrôlés sur les rendus de face.",
        "Fenêtres F1, F2 : position relevée sur le plan coté, hauteurs sur le rendu 02.",
        "Épaisseur des murs ≈ 20 (relevée sur le plan coté).",
        "Sens d'ouverture de la porte P1 et de la porte de douche : À CONF.",
    ] + common)
    body = place(svg, AX, AY) + vtitle(AX + 4, AY + h - 2, w - 8, "1", "Plan d'aménagement coté", "1:20")
    body += box(AX + w + 4, AY + 4, AW - w - 6, side)
    sheet("201", "Plan d'aménagement coté", "Plans techniques", "1:20", body)
    # 202 — plan de repérage : équipements et revêtements de sol
    svg, w, h = V.plan(25, "equip")
    rows = "".join(f'<tr><td class="ref">{a}</td><td>{esc(b)}</td><td>{c}</td></tr>' for a, b, c in [
        ("E1", "Cabine de douche : paroi verrière d'angle, profilés noirs, porte", "≈ 122 × 90 · H ≈ 200"),
        ("E2", "Colonne de douche noire, mitigeur", "mur ouest · tête ≈ 220 · mitigeur ≈ 100"),
        ("E3", "Rangement de douche (niche ou étagère)", "fond de douche · H ≈ 105–175"),
        ("E4", "Coffrage WC, faïence bordeaux", "116 × 40 (cotes écrites) · H ≈ 145"),
        ("E5", "WC suspendu, plaque de commande noire", "axe ≈ 78 · saillie ≈ 57"),
        ("E6", "Commode en noyer (M2)", "≈ 84 × 50 · H ≈ 87"),
        ("E7", "Étagères en verre fumé (×3)", "≈ 100 · H ≈ 110 / 144 / 179"),
        ("E8", "Étagères d'angle en noyer (×2) et miroir grossissant", "≈ 51 · H ≈ 179 / 216"),
        ("E9", "Échelle porte-serviettes noire avec panier", "mur ouest · dimensions À CONF."),
        ("E10", "Meuble vasque suspendu en noyer (M1), plan terrazzo", "≈ 156 × 52 · dessus ≈ 83"),
        ("E11", "Vasque à poser, robinetterie noire 3 trous", "axe ≈ 137 depuis le mur sud"),
        ("E12", "Miroir rétroéclairé", "≈ 175 × 100"),
        ("E13", "Porte-serviettes à barres noir", "≈ 53 · H ≈ 78"),
        ("E14", "Suspensions à globe (4)", "H ≈ 123–144"),
        ("E15", "Patères noires (2)", "retour de la douche · H ≈ 180–197"),
    ])
    tbl = (f'<div class="nh">Équipements</div><table class="tb2 full"><tr><th>Repère</th><th>Élément</th>'
           f'<th>Dimensions, position</th></tr>{rows}</table>'
           f'<div class="nh" style="margin-top:3mm">Revêtement de sol</div><p class="small">Motif « galets » : grandes dalles '
           f'blanches veinées à angles arrondis et inserts noirs, sur toute la pièce et dans la douche. Format des dalles et '
           f'calepinage : À CONF.</p>')
    body = place(svg, AX, AY) + vtitle(AX + 4, AY + h - 2, w - 8, "2", "Plan de repérage — équipements et sol", "1:25")
    body += box(AX + w + 4, AY + 2, AW - w - 6, tbl)
    sheet("202", "Plan de repérage — équipements et revêtement de sol", "Plans techniques", "1:25", body)
    # 203 — plan de plafond
    svg, w, h = V.plan(25, "plafond")
    side = notes([
        "Faux plafond peint blanc, hauteur ≈ 289 depuis le sol fini (rendus 02, 06, 08).",
        "Gorge lumineuse LED continue le long des murs (rendus 01, 02, 04, 06). Retrait par rapport aux murs : relevé "
        "≈ 28 sur le rendu 02 et ≈ 9 sur le rendu 06 → <span class='st-c'>À CONF.</span>",
        "Suspensions à globe au-dessus du bord du plan vasque (rendus 01, 06) : 4 globes à H ≈ 123–144. Points d'accroche, "
        "modèle et puissance : À CONF.",
        "Miroir rétroéclairé : halo sur le pourtour (rendus 01, 06).",
        "Douche : aucun luminaire visible sur les rendus. Éclairage et indice de protection (IP) de la zone humide : À CONF.",
        "Température de couleur et intensité des LED : non mesurables sur les rendus — À CONF.",
    ], "Plafond et éclairage")
    body = place(svg, AX, AY) + vtitle(AX + 4, AY + h - 2, w - 8, "3", "Plan de plafond et d'éclairage", "1:25")
    body += box(AX + w + 4, AY + 4, AW - w - 6, side)
    sheet("203", "Plan de plafond et d'éclairage", "Plans techniques", "1:25", body)
    # elevations
    drawing_sheet("204", "Élévation A — mur sud (fenêtres)", "1:20", V.elev_A(), "A", "Élévation A — mur sud", [
        "Mur en panneaux effet travertin, coffrage du WC en faïence bordeaux (116 × 40, cotes écrites ; H ≈ 145).",
        "F1 au-dessus du coffrage : allège ≈ 157, haut ≈ 226. F2 haute et étroite : allège ≈ 13, haut ≈ 226.",
        "Commode noyer ≈ 84 × 50, dessus ≈ 87, socle en retrait ≈ 9 ; étagères en verre fumé à ≈ 110 / 144 / 179.",
        "Étagères d'angle en noyer à ≈ 179 / 216 ; WC suspendu, plaque de commande noire à ≈ 85–97.",
        "Relevé : rendu 02, de face, calibré sur les fenêtres du plan coté (contrôle : coffrage 119 relevé / 116 écrit).",
    ] + common[:1], render=("02", T.RENDERS["02"][1]))
    drawing_sheet("205", "Élévation B — mur est (meuble vasque)", "1:20", V.elev_B(), "B", "Élévation B — mur est", [
        "Meuble vasque suspendu en noyer ≈ 156 × 52 : 2 tiroirs (≈ 92) et niches ouvertes (≈ 64) ; dessous ≈ 34, dessus ≈ 83.",
        "Plan et crédence en terrazzo (crédence ≈ 16 de haut) ; vasque à poser ≈ 45 (largeur À CONF.) ; robinetterie noire 3 trous.",
        "Miroir rétroéclairé ≈ 175 × 100, de ≈ 99 à ≈ 199. Porte-serviettes à barres à ≈ 78.",
        "Suspensions : 4 globes, ≈ 123 et ≈ 144.",
        "Relevé : rendu 06, de face, calibré sur la largeur du mur (234,10 écrite).",
    ] + common[:1], render=("06", T.RENDERS["06"][1]))
    sv1, sv2 = V.elev_C(), V.elev_F()
    body = place(sv1[0], AX, AY + 2) + vtitle(AX + 4, AY + 2 + sv1[2] + 1, sv1[1] - 8, "C", "Élévation C — mur nord (porte)", "1:20")
    x2 = AX + sv1[1] + 4
    body += place(sv2[0], x2, AY + 2) + vtitle(x2 + 4, AY + 2 + sv2[2] + 1, sv2[1] - 8, "F", "Élévation F — retour de la douche", "1:20")
    body += box(AX, AY + max(sv1[2], sv2[2]) + 12, AW - 4, notes([
        "C : porte P1 de 74 entre deux trumeaux de 66 et 70 (cotes écrites) ; hauteur ≈ 202 (rendus 06 et 08). Porte sombre à "
        "inserts métalliques horizontaux, béquille métal ; sens d'ouverture À CONF.",
        "F : mur entre la douche et la pièce voisine (137, cote écrite). Deux patères noires, la première à ≈ 197 ; position de la "
        "seconde À CONF. (vue seulement de 3/4 sur le rendu 07).",
    ] + common[:1]))
    sheet("206", "Élévations C (mur nord, porte) et F (retour de la douche)", "Plans techniques", "1:20", body)
    drawing_sheet("207", "Élévation D — mur ouest", "1:20", V.elev_D(), "D", "Élévation D — mur ouest", [
        "Longueur 371,1 = 234,10 + 137,00 (cotes écrites).",
        "Coffrage du WC vu de côté (40, cote écrite). Échelle porte-serviettes noire avec panier : position ≈ (vue de dessus), "
        "hauteur et largeur À CONF.",
        "Douche : colonne noire (tête ≈ 220), mitigeur ≈ 100 et second robinet ≈ 88 ; seuil ≈ 8.",
        "Aucun rendu de face de ce mur : positions relevées sur la vue de dessus et le rendu 08.",
    ] + common[:1], render=("04", T.RENDERS["04"][1]))
    drawing_sheet("208", "Élévation E — fond de douche", "1:20", V.elev_E(), "E", "Élévation E — fond de douche", [
        "Faïence bordeaux brillante posée à la verticale, sur toute la hauteur et toute la largeur (164,80, cote écrite).",
        "Format relevé sur le coffrage : entraxe des joints ≈ 7,7 × 17,7 → format À CONF.",
        "Paroi verrière vue de face : ≈ 122 de large, de ≈ 8,5 à ≈ 209 ; 5 rangs de ≈ 40 ; montant à ≈ 70 ; poignée verticale.",
        "Rangement des produits à ≈ 105–175 : niche encastrée ou étagère, À CONF.",
        "Relevé : rendu 08, de face, calibré sur la largeur du fond (164,80).",
    ] + common[:1], render=("08", T.RENDERS["08"][1]))
    drawing_sheet("209", "Coupe AA — douche, WC et fenêtre F1", "1:20", V.section_AA(), "AA", "Coupe AA (X ≈ 92), vue vers l'est", [
        "Coupe nord-sud à travers le coffrage du WC, la pièce et la douche.",
        "Plancher, chape, receveur ou douche à l'italienne, pentes et évacuation : non visibles sur les documents — À CONF.",
        "Épaisseur du faux plafond et du plénum : À CONF.",
    ] + common)
    drawing_sheet("210", "Coupe BB — échelle, porte et meuble vasque", "1:20", V.section_BB(), "BB", "Coupe BB (Y ≈ 125), vue vers le nord", [
        "Coupe est-ouest à travers l'échelle porte-serviettes et le meuble vasque ; porte P1 au fond.",
        "Fixation du meuble suspendu, alimentation et évacuation de la vasque : À CONF.",
    ] + common)
    for num, ttl, fn, letter, cap in (("211", "Mobilier M1 — meuble vasque", V.furniture_M1, "M1", "Meuble vasque suspendu"),
                                      ("212", "Mobilier M2 — commode", V.furniture_M2, "M2", "Commode en noyer")):
        svg, w, h = fn()
        it = ([
            "Caisson et façades en noyer ; 2 tiroirs sans poignée apparente (gorge) ; niches ouvertes à 2 tablettes.",
            "Plan en terrazzo clair ≈ 3 d'épaisseur (À CONF.), crédence en terrazzo ≈ 16 de haut.",
            "Vasque à poser rectangulaire blanche ; mitigeur noir 3 trous (bec haut, 2 croisillons).",
            "Dimensions relevées sur les rendus 06 et 01 et la vue de dessus. Profondeur ≈ 52 (vue de dessus).",
            "Quincaillerie, coulisses, fixation murale, découpe de la vasque : À CONF.",
        ] if letter == "M1" else [
            "Caisson en noyer aux angles arrondis ; 2 tiroirs à poignées encastrées noires ; socle en retrait ≈ 9.",
            "Dimensions relevées sur le rendu 02 et la vue de dessus (largeur ≈ 84, profondeur ≈ 50, hauteur ≈ 87).",
            "Poignées : longueur ≈ 16, À CONF. ; finition du noyer (vernis, huile) : À CONF.",
        ]) + common[:1]
        body = place(svg, AX, AY + 4) + vtitle(AX + 4, AY + 4 + h + 1, w - 8, letter, cap, "1:10")
        body += box(AX, AY + h + 14, min(w, 220), notes(it))
        sheet(num, ttl, "Plans techniques", "1:10", body)


# ---------------------------------------------------------------- 500: materials, finishes, equipment
MATERIALS = [   # name, use, render, sample box (median colour), finish, format, extract (detail id or None)
    ("Panneaux effet travertin", "Murs de la pièce, retour de la douche", "02", (380, 170, 860, 530),
     "mat, veinage horizontal", "grand format, À CONF.", "D01"),
    ("Faïence bordeaux", "Fond de douche, coffrage du WC", "02", (960, 900, 1250, 1080),
     "brillante, pose verticale", "entraxe ≈ 7,7 × 17,7", "D02"),
    ("Dalle « galets » blanche", "Sol de la pièce et de la douche", "02", (60, 1700, 300, 1800),
     "veinée", "À CONF.", "D03"),
    ("Insert noir", "Sol, entre les dalles", "02", None, "mat", "À CONF.", None),
    ("Terrazzo clair", "Plan vasque, crédence", "06", (1000, 1065, 1400, 1100), "poli ?", "épaisseur ≈ 3, À CONF.", "D05"),
    ("Noyer", "Meuble vasque, commode, étagères d'angle", "06", (600, 1240, 1100, 1360), "satiné ?", "—", "D04"),
    ("Verre fumé", "Étagères murales", "02", None, "transparent teinté", "≈ 100 × 22", "D16"),
    ("Verre clair + acier noir", "Paroi de douche", "08", None, "profilés noirs mats", "rangs de ≈ 40", "D10"),
    ("Noir mat", "Robinetterie, colonne, porte-serviettes, patères, plaque WC", "06", None, "mat", "—", "D06"),
    ("Céramique blanche", "Vasque, WC", "06", (690, 1150, 860, 1180), "brillante", "—", None),
    ("Bois sombre + métal", "Porte P1", "06", (12, 650, 60, 850), "inserts métal horizontaux", "74 × ≈ 202", "D23"),
    ("Peinture blanche", "Faux plafond", "02", (300, 20, 1200, 80), "mate", "—", "D27"),
]


def median_hex(n, b):
    import numpy as np
    a = np.asarray(Image.open(src(n)).convert("RGB").crop(b)).reshape(-1, 3)
    m = np.median(a, axis=0).astype(int)
    return "#%02X%02X%02X" % tuple(m)


def dark_hex(n, b):
    import numpy as np
    a = np.asarray(Image.open(src(n)).convert("RGB").crop(b)).reshape(-1, 3)
    d = a[a.sum(1) < 200]
    return "#%02X%02X%02X" % tuple(np.median(d, axis=0).astype(int))


def series500():
    rows = ""
    cards = ""
    for name, use, n, b, fin, form, ext in MATERIALS:
        hexc = median_hex(n, b) if b else (dark_hex("02", (40, 1496, 520, 1816)) if name == "Insert noir" else None)
        chip = f'<span class="chip" style="background:{hexc}"></span>' if hexc else '<span class="chip none">—</span>'
        rows += (f'<tr><td>{chip}</td><td><b>{esc(name)}</b></td><td>{esc(use)}</td><td>{hexc or "—"}</td>'
                 f'<td>{esc(fin)}</td><td>{esc(form)}</td><td class="st-c">à confirmer</td></tr>')
        if ext:
            p, _ = crop(ext)
            cards += (f'<figure class="mc"><div class="mci"><img src="{p.as_uri()}"></div>'
                      f'<figcaption><span class="mcs" style="background:{hexc or "#fff"}"></span><b>{esc(name)}</b>'
                      f'<br><span class="small">{esc(use)} · {ext}, rendu {T.D[ext][3]}</span></figcaption></figure>')
    t = (f'<div class="nh">Matériaux et finitions — douche principale</div>'
         f'<table class="tb2 full mat"><tr><th></th><th>Matériau</th><th>Localisation</th><th>Teinte relevée</th>'
         f'<th>Finition observée</th><th>Format</th><th>Référence fabricant</th></tr>{rows}</table>')
    side = notes([
        "Matériaux identifiés sur les rendus 3D du projet ; aucune référence n'est inventée.",
        "Teinte relevée : médiane des pixels d'une zone du rendu. Indicative : elle dépend de l'éclairage de la scène.",
        "« — » : teinte non relevable sur le rendu (verre, reflets, métal).",
        "À valider avant commande : échantillons physiques, références, finitions, formats, calepinage et joints.",
        "Pièce humide : classement des revêtements (glissance du sol de douche, résistance à l'eau des panneaux muraux "
        "et du noyer) à vérifier avec les fournisseurs.",
    ])
    sheet("501", "Matériaux et finitions — nomenclature", "Matériaux et finitions",
          "—", box(AX + 2, AY + 2, 236, t) + box(AX + 244, AY + 2, 82, side))
    body = (box(AX + 2, AY + 2, AW - 4, '<div class="nh">Planche matériaux — extraits des rendus 3D</div>'
                f'<div class="mgrid">{cards}</div>'))
    sheet("502", "Planche matériaux et textures", "Matériaux et finitions", "—", body)
    rows = "".join(f'<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td>{c}</td><td class="st-c">à confirmer</td></tr>' for a, b, c in [
        ("WC suspendu, cuvette carrée blanche", "devant le coffrage, axe ≈ 78", "saillie ≈ 57"),
        ("Plaque de commande noire", "coffrage, H ≈ 85–97", "≈ 19 × 12"),
        ("Dérouleur noir", "coffrage, à droite de la plaque", "—"),
        ("Vasque à poser rectangulaire blanche", "plan vasque, axe ≈ 137 du mur sud", "≈ 45 de large"),
        ("Mitigeur lavabo noir, 3 trous", "plan vasque", "bec haut ≈ 16 au-dessus de la vasque"),
        ("Colonne de douche noire, tête ronde", "mur ouest de la douche", "tête ≈ 220"),
        ("Mitigeur / thermostatique de douche noir", "mur ouest de la douche", "≈ 100 et ≈ 88"),
        ("Paroi verrière d'angle, profilés noirs, porte", "douche", "≈ 122 × 90 · H ≈ 200"),
        ("Miroir rétroéclairé", "au-dessus du meuble vasque", "≈ 175 × 100"),
        ("Suspensions à globe (×4)", "au-dessus du bord du plan vasque", "H ≈ 123–144"),
        ("Gorge lumineuse LED", "périphérie du faux plafond", "retrait À CONF."),
        ("Échelle porte-serviettes noire + panier", "mur ouest", "À CONF."),
        ("Porte-serviettes à barres noir", "mur est, au nord du meuble", "≈ 53 · H ≈ 78"),
        ("Patères noires (×2)", "retour de la douche", "H ≈ 180–197"),
        ("Miroir grossissant rond", "étagère noyer d'angle", "—"),
    ])
    t = (f'<div class="nh">Sanitaires, robinetterie, luminaires et accessoires</div><table class="tb2 full"><tr><th>Élément</th>'
         f'<th>Emplacement</th><th>Dimensions relevées</th><th>Référence</th></tr>{rows}</table>')
    sheet("503", "Équipements — sanitaires, robinetterie, luminaires, accessoires", "Matériaux et finitions", "—",
          box(AX + 2, AY + 2, 236, t) + box(AX + 244, AY + 2, 82, notes([
              "Éléments identifiés sur les rendus ; marques et modèles non lisibles : aucune référence n'est inventée.",
              "Hauteurs de pose à valider avec le plombier et l'électricien (normes de la zone humide).",
          ])))


def recap():
    items = [
        ("Plan", "Sens d'ouverture de la porte P1 et de la porte de douche ; épaisseur réelle des murs (≈ 20 relevée)."),
        ("Plan", "Cote « 478 » du plan coté (partie chambre) : ≈ 386 à l'échelle — <b>À VÉRIFIER</b>, non corrigée."),
        ("Plan", "Rectangle de ≈ 196 × 192 tracé sur le plan coté contre les murs est et sud, sans cote ni équivalent sur les "
                 "rendus : non dessiné — <b>À VÉRIFIER</b>."),
        ("Douche", "Type de sol (receveur extra-plat ou douche à l'italienne), pentes, évacuation, hauteur du seuil (≈ 8,5)."),
        ("Douche", "Rangement des produits : niche encastrée ou étagère ; dimensions."),
        ("Douche", "Éclairage de la douche (aucun luminaire visible) et indices de protection."),
        ("Plafond", "Retrait de la gorge LED par rapport aux murs (≈ 28 ou ≈ 9 selon le rendu) ; épaisseur du faux plafond."),
        ("Mobilier", "Épaisseur du plan terrazzo ; largeur exacte de la vasque ; quincaillerie et fixations de M1."),
        ("Mobilier", "Poignées et finition de la commode M2."),
        ("Accessoires", "Dimensions de l'échelle porte-serviettes ; position de la seconde patère."),
        ("Matériaux", "Références, formats et finitions : travertin, faïence (entraxe ≈ 7,7 × 17,7), dalles « galets », terrazzo, noyer, verre fumé."),
        ("Équipements", "Marques et modèles : WC, plaque, robinetterie, colonne, paroi, miroir, suspensions, LED."),
    ]
    li = "".join(f"<tr><td><b>{esc(a)}</b></td><td>{b}</td></tr>" for a, b in items)
    body = box(AX + 2, AY + 2, 230, f'<div class="nh">Points à confirmer avant exécution</div>'
               f'<table class="tb2 full"><tr><th>Sujet</th><th>À confirmer</th></tr>{li}</table>')
    body += box(AX + 240, AY + 2, 86, notes([
        "Toutes les cotes « ≈ » sont des relevés sur les documents du projet : à vérifier sur site avant fabrication.",
        "Aucune cote n'a été inventée : sans source, la cote est marquée À CONF.",
    ]))
    sheet("900", "Points à confirmer", "Synthèse", "—", body)


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
.mgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:4mm 4mm;margin-top:2mm}
.mc{margin:0}.mci{height:44mm;overflow:hidden;border:.2mm solid #3A2A22}.mci img{width:100%;height:100%;object-fit:cover;display:block}
.mc figcaption{font-size:2.3mm;margin-top:1.2mm;line-height:1.35}
.mcs{display:inline-block;width:4mm;height:4mm;border:.15mm solid #999;vertical-align:-0.6mm;margin-right:1.2mm}
"""


def main():
    BUILD.mkdir(exist_ok=True)
    front()
    concept()
    series200()
    renders()
    index_sheet()
    for p in T.PLATES:
        detail_plate(*p)
    series500()
    recap()
    total = len(SHEETS)
    pages = [f'<section class="sheet"><div class="frame"></div>'
             f'{toc_html(total) if sh["body"] == "__TOC__" else sh["body"]}{title_block(sh, i, total)}</section>'
             for i, sh in enumerate(SHEETS, 1)]
    css = (VB.CSS + EXTRA_CSS).replace("FONTS/", FONTS.as_uri() + "/")
    doc = (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>KAÏRA — {PROJECT}</title>'
           f'<style>{css}</style></head><body>{V.PATTERNS}{"".join(pages)}</body></html>')
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
