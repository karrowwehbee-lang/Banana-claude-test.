"""KAÏRA — Douche principale – Étage 1 : dossier complet de conception et d'architecture intérieure (A3 paysage).

Deux gabarits, une identité :
- pages de conception (sections 1–4 et 6–9) : mise en page éditoriale du dossier de conception de la villa
  (papier crème, Cormorant et Jost, folio KAÏRA avec n° de planche) ;
- planches techniques (section 5 et plans d'éclairage) : cadre et cartouche du dossier technique de la villa.
Rendus : fichiers originaux, insérés entiers (contain), jamais recadrés ni retouchés ; les détails sont des extraits
signalés (zone encadrée et numérotée sur le rendu entier). Aucune référence ni dimension inventée.

Usage : python3 tools/build.py [--previews]  ->  build/dossier-douche-etage1.html, build/…pdf, build/prev-NN.png
"""
import html
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import details as T  # noqa: E402
import geom as G  # noqa: E402
import palette as PA  # noqa: E402
import tech as X  # noqa: E402
import views_dpe as V  # noqa: E402

ROOT, REPO = X.ROOT, X.REPO
SRC, BUILD = X.SRC, X.BUILD
CROPS = BUILD / "crops"
OUT_PDF = BUILD / "KAIRA-Douche-principale-Etage1-Dossier-A3.pdf"
LOGO, FONTS = X.LOGO, X.FONTS

PROJECT = "Villa — Douche principale – Étage 1"
DOC = "Dossier de conception et d'architecture intérieure"
DATE = "18.11.2026"
INDICE = "0"
STATUS = "Document de travail — non finalisé"
W, H, M = 420, 297, 18          # editorial page and margin (mm)
AX, AY, AW, AH = X.AX, X.AY, X.AW, X.AH

PAGES = []
SECTIONS = []


def esc(s):
    return html.escape(str(s))


def page(num, title, section, body, kind="ed", scale="—", cls=""):
    PAGES.append(dict(num=num, title=title, section=section, body=body, kind=kind, scale=scale, cls=cls))


def src(n):
    return SRC / f"{n}.png"


def size(n):
    return Image.open(src(n)).size


def box(x, y, w, inner, cls="ebox"):
    return f'<div class="{cls}" style="left:{x:.1f}mm;top:{y:.1f}mm;width:{w:.1f}mm">{inner}</div>'


def whole(n, x, y, w, h, align="center"):
    """A render shown whole inside the box (never cropped). Returns html and the image rectangle."""
    iw, ih = size(n)
    s = min(w / iw, h / ih)
    dw, dh = iw * s, ih * s
    ox = x + (w - dw) / 2 if align == "center" else (x if align == "left" else x + w - dw)
    oy = y + (h - dh) / 2
    return (f'<div class="rw" style="left:{ox:.2f}mm;top:{oy:.2f}mm;width:{dw:.2f}mm;height:{dh:.2f}mm">'
            f'<img src="{src(n).as_uri()}"></div>'), (ox, oy, dw, dh)


def pins(n, x, y, w, h, marks):
    """Numbered pins over a whole render (SVG overlay, the image itself is untouched)."""
    iw, ih = size(n)
    svg = ""
    for code, (px, py) in marks:
        svg += (f'<circle cx="{px}" cy="{py}" r="34" fill="#FFFFFF" fill-opacity="0.92" stroke="#6E2234" stroke-width="5"/>'
                f'<text x="{px}" y="{py + 13}" text-anchor="middle" font-family="Jost" font-weight="500" font-size="36" '
                f'fill="#6E2234">{code}</text>')
    return (f'<svg class="ov" style="left:{x:.2f}mm;top:{y:.2f}mm;width:{w:.2f}mm;height:{h:.2f}mm" '
            f'viewBox="0 0 {iw} {ih}" preserveAspectRatio="none">{svg}</svg>')


def cut(n, b, name):
    """Extract of an original render (pixel crop, saved losslessly, no retouch)."""
    CROPS.mkdir(parents=True, exist_ok=True)
    p = CROPS / f"{name}.png"
    if not p.exists():
        Image.open(src(n)).convert("RGB").crop(b).save(p)
    return p


def ext(p, x, y, w, h, tag=None, fit="cover", cls="ex"):
    t = f'<span class="etag">{esc(tag)}</span>' if tag else ""
    return (f'<div class="{cls}" style="left:{x:.2f}mm;top:{y:.2f}mm;width:{w:.2f}mm;height:{h:.2f}mm">'
            f'<img src="{p.as_uri()}" style="object-fit:{fit}">{t}</div>')


def dcut(d):
    title, desc, cat, n, b = T.D[d]
    return cut(n, b, d)


def hexc(sample):
    n, b, mode = sample
    a = np.asarray(Image.open(src(n)).convert("RGB").crop(b)).reshape(-1, 3).astype(int)
    s = a.sum(1)
    if mode == "light":
        a = a[s > np.percentile(s, 40)]
    elif mode == "dark":
        a = a[s < np.percentile(s, 6)]
    elif mode == "glow":
        a = a[s >= np.percentile(s, 99)]
    r, g, bl = np.median(a, axis=0).astype(int)
    return "#%02X%02X%02X" % (r, g, bl), (int(r), int(g), int(bl))


COL = {k: hexc(v[2]) for k, v in PA.COLOURS.items()}


def mat_hex(k):
    c = PA.MATERIALS[k][6]
    return COL[c][0] if c else None


def plate_of(d):
    return next(p[0] for p in T.PLATES if d in p[3])


def kicker(t):
    return f'<div class="kick">{esc(t)}</div>'


def head(num, kick, title, x=M, y=M, w=250):
    return box(x, y, w, f'<div class="snum">{num}</div>{kicker(kick)}<h2>{title}</h2>')


# ================================================================ 0 — FRONT
def front():
    logo = LOGO.read_text()
    img, r = whole("01", 0, 0, 272, H, "left")
    body = img + f"""
<div class="cv-panel" style="left:{r[2] + 14:.1f}mm;width:{W - r[2] - 30:.1f}mm">
  <div class="cv-logo">{logo}</div>
  <div class="cv-mid"><div class="kick">{DOC}</div>
   <h1>Douche principale<br><em>– Étage 1</em></h1><div class="rule"></div>
   <p class="cv-proj">Villa · Étage 1</p>
   <p class="cv-list">Concept · Couleurs · Matériaux et finitions · Détails décoratifs · Dossier technique ·
   Éclairage · Mobilier et équipements · Rendus 3D · Synthèse</p></div>
  <div class="cv-foot">Indice {INDICE} — {DATE}<br>Format A3 paysage · cotes en centimètres<br><span>{STATUS}</span></div>
</div>"""
    page("000", "Couverture", "Couverture", body, cls="p-cover")
    page("001", "Sommaire", "Sommaire", "__TOC__")
    rl = "".join(f"<li><b>Rendu {n}</b> — {esc(T.RENDERS[n][0])} · {esc(T.RENDERS[n][2])}</li>" for n in T.RENDER_ORDER)
    body = head("", "À propos de ce dossier", "Méthode, sources <em>et conventions</em>", w=380)
    body += box(M, 52, 120, f"""<h3>Les cotes</h3>
<table class="lg"><tr><td class="st-v big">374,8</td><td><b>Cote vérifiée</b> — écrite sur le plan coté fourni par KAÏRA,
 reprise telle quelle.</td></tr>
<tr><td class="st-d big"><i>≈ 156</i></td><td><b>Cote déduite</b> — relevée à l'échelle sur la vue de dessus ou sur un rendu
 de face calibré sur une cote écrite. Arrondie au centimètre ; tolérance ±3 cm en plan, ±5 cm en hauteur.</td></tr>
<tr><td class="st-c big">À CONF.</td><td><b>À CONFIRMER</b> — aucune source dans les documents du projet. Jamais inventée.</td></tr></table>
<h3>Les couleurs et les matériaux</h3>
<p>Chaque teinte est la médiane des pixels d'une zone du rendu : un code HEX indicatif, qui dépend de l'éclairage de la scène.
Les matières sont nommées comme elles apparaissent ; quand leur nature réelle n'est pas connue, elles sont dites
« effet … ». Aucune référence commerciale n'est indiquée : à confirmer avant commande.</p>""")
    body += box(M + 132, 52, 120, f"""<h3>Les rendus et les détails</h3>
<p>Les rendus 3D sont les fichiers originaux, insérés en entier, sans recadrage, retouche ni modification de couleur.</p>
<p>Les vues rapprochées sont des <b>extraits signalés</b> : une zone du rendu, agrandie, numérotée de <span class="tag">D01</span>
à <span class="tag">D39</span> et encadrée sur le rendu entier présenté sur la même planche.</p>
<h3>Méthode de relevé</h3>
<p><b>Plan :</b> plan coté IMG_7771, partie gauche en L, identifiée par KAÏRA sur le plan annoté (flèche sur la porte de 74).
Cotes écrites reprises : 374,80 · 234,10 · 137,00 · 164,80 · 66 · 74 · 70 · 116 · 40.</p>
<p><b>Équipements :</b> vue de dessus de la maquette recalée sur le plan coté. <b>Hauteurs :</b> rendus de face calibrés
sur un mur de largeur écrite (contrôles : plafond 289 / 289 / 288 ; porte 202 / 203).</p>""")
    body += box(M + 264, 52, 120, f"""<h3>Documents sources</h3><ul class="nl">
<li><b>Plan coté</b> IMG_7771 et sa version annotée — partie douche principale</li>{rl}</ul>
<h3>Documents écartés</h3><ul class="nl">
<li>Partie droite du plan coté (chambre) : hors dossier, jamais mélangée aux dessins.</li>
<li>Cote écrite « 478 » de cette partie : ≈ 386 à l'échelle — <span class="st-c">À VÉRIFIER</span>, non corrigée.</li></ul>
<h3>Numérotation</h3><p>KAI-DPE-<b>N</b>xx : le premier chiffre est le numéro de section (1 à 9).</p>""")
    page("002", "Méthode, sources et conventions", "À propos", body)


def opener(num, kick, title, text, render, items=None):
    SECTIONS.append((num, kick, title, f"{num}00"))
    img, r = whole(render, W - 272, 0, 272, H, "right")
    li = "".join(f"<li>{esc(i)}</li>" for i in items or [])
    body = img + box(M, 40, r[0] - M - 18, f"""<div class="bignum">0{num}</div>{kicker(kick)}
<h2 class="xl">{title}</h2><div class="rule"></div><p class="lead">{text}</p>{f'<ul class="olist">{li}</ul>' if li else ''}""")
    page(f"{num}00", kick, kick, body, cls="p-open")


# ================================================================ 1 — CONCEPT
def s1():
    opener("1", "Concept architectural et décoratif", "Une douche <em>minérale et chaleureuse</em>",
           "La douche principale de l'étage réunit, dans une pièce en L, la cabine de douche, l'espace vasque, le coin WC et "
           "les rangements. Une enveloppe claire et minérale, un sol graphique et trois accents — le noyer, le bordeaux et "
           "le noir — composent un espace calme, chaleureux et affirmé.", "06",
           ["Présentation du concept", "Intention architecturale", "Ambiance recherchée", "Style et principes de conception",
            "Description de l'aménagement", "Univers et moodboard"])
    # 101 presentation
    img, r = whole("02", W - 190, M, 172, 252)
    surf = (G.W_TOT * G.D_LARGE + G.W_RET * G.D_RET) / 1e4
    body = head("1.1", "Présentation du concept", "Une pièce d'eau <em>pensée comme un lieu de vie</em>", w=r[0] - M - 14)
    body += box(M, 66, r[0] - M - 16, f"""<p class="lead">La lumière indirecte, les matières et le rangement y comptent autant que
les équipements.</p>
<p>La pièce s'organise en L. Dans le retour, à l'abri de la porte, la cabine de douche s'adosse à un mur de faïence
bordeaux, derrière une paroi verrière à profilés noirs. La partie principale accueille, face à face, le meuble vasque
suspendu sous un grand miroir rétroéclairé et, le long des fenêtres, la commode en noyer, les étagères et le coin WC.</p>
<p>Tous les murs portent le même revêtement effet travertin, à veinage horizontal ; le sol « galets » blanc et noir unifie
la pièce et la douche. Les équipements noirs dessinent des lignes nettes ; le noyer et le bordeaux réchauffent l'ensemble.</p>
<div class="facts">
 <div><span>Niveau</span>Étage 1 de la villa</div>
 <div><span>Surface</span>≈ {surf:.1f} m² — calculée d'après les cotes écrites du plan</div>
 <div><span>Hauteur sous plafond</span>≈ 289 cm — relevée sur trois rendus</div>
 <div><span>Programme</span>Cabine de douche · meuble vasque suspendu · WC suspendu · commode · étagères · rangements</div>
 <div><span>Signature</span>Effet travertin · sol « galets » · noyer · bordeaux · noir mat · lumière indirecte</div>
</div>""".replace(".", ",", 0)) + img
    body = body.replace(f"≈ {surf:.1f} m²", f"≈ {surf:.1f} m²".replace(".", ","))
    sw_ = (r[0] - M - 16 - 2 * 6) / 3
    for j, d in enumerate(("D04", "D13", "D10")):
        x = M + j * (sw_ + 6)
        body += ext(dcut(d), x, 206, sw_, 52, d)
        body += box(x, 260, sw_, f'<p class="src">{esc(T.D[d][0])}</p>')
    page("101", "Présentation du concept", "Concept", body)
    # 102 intention
    pill = [("D01", "Une enveloppe unique", "Un même revêtement effet travertin habille tous les murs, du sol au plafond. "
             "Sans changement de matière, la pièce paraît plus grande et plus calme ; le veinage horizontal l'étire."),
            ("D03", "Un sol qui unifie", "Les dalles « galets » blanches et leurs inserts noirs couvrent toute la pièce, "
             "douche comprise. Le motif, à grande échelle, donne du mouvement sans surcharger."),
            ("D13", "La couleur à sa juste place", "Le bordeaux est réservé à deux volumes : le fond de la douche et le "
             "coffrage du WC. Il signale les deux zones d'eau et donne au projet son caractère."),
            ("D10", "Des équipements dessinés", "Paroi verrière, robinetterie, colonne, porte-serviettes, patères : tout est "
             "noir mat. Ces lignes nettes se détachent sur le fond clair.")]
    body = head("1.2", "Intention architecturale", "Une architecture <em>de matière et de lumière</em>", w=380)
    cw = (W - 2 * M - 3 * 9) / 4
    for i, (d, t, txt) in enumerate(pill):
        x = M + i * (cw + 9)
        body += ext(dcut(d), x, 70, cw, 120, d)
        body += box(x, 196, cw, f'<h3>{t}</h3><p>{txt}</p><p class="src">Extrait {d} — rendu {T.D[d][3]}</p>')
    body += box(M, 262, 384, '<p class="quote">Le mobilier suspendu libère le sol ; la lumière, indirecte, vient des bords : '
                'la pièce reste légère malgré la densité de son programme.</p>')
    page("102", "Intention architecturale", "Concept", body)
    # 103 ambiance
    amb = [("D31", "Calme", "Des surfaces claires et mates, une lumière indirecte qui glisse sur les murs, aucune source "
            "éblouissante. Le regard se pose."),
           ("D37", "Chaleur", "Le noyer à hauteur de main, le linge blanc roulé et plié, la lumière ambrée : un confort "
            "presque hôtelier, simple et soigné."),
           ("D33", "Caractère", "Le bordeaux brillant, les profilés noirs et le sol graphique donnent à la pièce une signature "
            "affirmée, loin de la salle d'eau impersonnelle.")]
    body = head("1.3", "Ambiance recherchée", "Calme, chaleur <em>et caractère</em>", w=380)
    cw = (W - 2 * M - 2 * 12) / 3
    for i, (d, t, txt) in enumerate(amb):
        x = M + i * (cw + 12)
        body += ext(dcut(d), x, 70, cw, 130, d)
        body += box(x, 206, cw, f'<div class="word">{t}</div><p>{txt}</p><p class="src">Extrait {d} — rendu {T.D[d][3]}</p>')
    body += box(M, 258, 384, '<p class="quote">Mat et brillant, horizontal et vertical, clair et sombre : l\'ambiance naît '
                'de contrastes maîtrisés.</p>')
    page("103", "Ambiance recherchée", "Concept", body)
    # 104 style & principles
    img, r = whole("04", W - 190, M, 172, 252)
    pr = [("Une palette restreinte", "Trois couleurs principales pour les grandes surfaces, trois secondaires pour le mobilier, "
           "trois accents (planches 2.1 à 2.5)."),
          ("Le contraste mat / brillant", "Murs mats effet travertin, faïence bordeaux brillante, céramique émaillée."),
          ("Des lignes horizontales et verticales", "Veinage horizontal des murs, faïence en pose verticale, trame orthogonale "
           "de la verrière."),
          ("Un mobilier suspendu", "Meuble vasque et WC suspendus : le sol reste continu et facile d'entretien."),
          ("Une lumière indirecte", "Gorge LED en périphérie, halo du miroir, suspensions : aucune source nue au plafond."),
          ("Des rangements ordonnés", "Niches, étagères et commode : le linge et les objets participent au décor.")]
    li = "".join(f'<div class="pr"><span>0{i + 1}</span><div><b>{a}</b><p>{b}</p></div></div>' for i, (a, b) in enumerate(pr))
    body = head("1.4", "Style et principes de conception", "Contemporain, <em>chaleureux et graphique</em>", w=r[0] - M - 14)
    body += box(M, 66, r[0] - M - 16, f"""<p class="lead">Un style contemporain nourri de références : la verrière d'atelier pour
la douche, la faïence émaillée en pose verticale, le confort du linge roulé et des peignoirs.</p><div class="prs">{li}</div>""")
    page("104", "Style et principes de conception", "Concept", body + img)
    # 105 description of the layout
    svg, w, h = V.plan(22, "zones")
    zl = [("1", "Entrée", "Porte de 74 cm (cote écrite) dans le mur nord de la partie principale. En entrant : le meuble vasque "
           "à gauche, les fenêtres en face, la douche à droite, en retrait dans le retour."),
          ("2", "Espace vasque", "Le long du mur est : meuble vasque suspendu en noyer ≈ 156 cm, plan et crédence effet "
           "terrazzo, miroir rétroéclairé ≈ 175 × 100 cm, quatre suspensions, porte-serviettes à barres."),
          ("3", "Coin WC", "Dans l'angle sud-ouest : coffrage en faïence bordeaux 116 × 40 cm (cotes écrites), WC suspendu, "
           "plaque de commande noire ; petite fenêtre F1 au-dessus."),
          ("4", "Rangements", "Mur sud : commode en noyer ≈ 84 cm, trois étagères en verre fumé, étagères d'angle en noyer. "
           "Mur ouest : échelle porte-serviettes noire avec panier."),
          ("5", "Cabine de douche", "Dans le retour de 164,80 × 137 cm (cotes écrites) : cabine d'angle ≈ 122 × 90 cm, paroi "
           "verrière, colonne noire, fond en faïence bordeaux ; patères sur le retour.")]
    li = "".join(f'<div class="zn"><span>{n}</span><div><b>{t}</b><p>{x}</p></div></div>' for n, t, x in zl)
    body = head("1.5", "Description de l'aménagement", "Cinq zones, <em>une circulation libre</em>", w=380)
    body += f'<div class="v" style="left:{M:.1f}mm;top:58mm">{svg}</div>'
    body += box(M + w + 10, 62, W - 2 * M - w - 10, li + '<p class="src" style="margin-top:4mm">Le centre de la pièce reste '
                'libre, de la porte aux fenêtres. Plan au 1:22 — cotes et repérage : planches 501 et 502.</p>')
    page("105", "Description de l'aménagement", "Concept", body)
    # 106 moodboard
    mb = [("D13", 18, 52, 118, 150), ("D30", 140, 52, 128, 72), ("D03", 272, 52, 130, 72), ("D37", 140, 128, 62, 74),
          ("D36", 206, 128, 62, 74), ("D10", 272, 128, 64, 74), ("D04", 340, 128, 62, 74), ("D32", 18, 206, 70, 66),
          ("D01", 92, 206, 120, 66), ("D33", 216, 206, 60, 66), ("D02", 280, 206, 122, 66)]
    body = head("1.6", "Moodboard", "L'univers <em>de la douche principale</em>", w=380, y=M - 4)
    for d, x, y, w_, h_ in mb:
        body += ext(dcut(d), x, y, w_, h_, d)
    body += box(M, 276, 384, '<p class="src">Extraits des rendus du projet ; légendes et rendus d\'origine : index des détails, '
                'planche 401.</p>')
    page("106", "Moodboard", "Concept", body)


# ================================================================ 2 — COLOURS
def s2():
    opener("2", "Palette de couleurs", "Neuf teintes, <em>trois rôles</em>",
           "Les couleurs sont relevées directement dans les rendus : trois couleurs principales pour les grandes surfaces, "
           "trois secondaires pour le mobilier et les matières, trois accents qui donnent le caractère.", "02",
           ["Palette générale", "Couleurs principales", "Couleurs secondaires", "Couleurs d'accent", "Les couleurs dans l'espace"])
    groups = [("principale", "Couleurs principales", "Les grandes surfaces"),
              ("secondaire", "Couleurs secondaires", "Le mobilier et les matières"),
              ("accent", "Couleurs d'accent", "Le caractère")]
    body = head("2.1", "Palette générale", "Les couleurs <em>du projet</em>", w=380)
    x = M
    widths = {"principale": 150, "secondaire": 120, "accent": 102}
    for role, ttl, sub in groups:
        ks = [k for k, v in PA.COLOURS.items() if v[1] == role]
        gw = widths[role]
        bw = gw / len(ks)
        body += box(x, 60, gw, f'<div class="kick">{ttl}</div><p class="small">{sub}</p>')
        for j, k in enumerate(ks):
            hx, rgb = COL[k]
            ink = "#FFFFFF" if sum(rgb) < 380 else "#2B2622"
            body += (f'<div class="bar" style="left:{x + j * bw:.1f}mm;top:78mm;width:{bw:.1f}mm;height:150mm;background:{hx};'
                     f'color:{ink}"><span>{k}</span><b>{hx}</b></div>')
            body += box(x + j * bw + 1.5, 232, bw - 3, f'<div class="bn">{esc(PA.COLOURS[k][0])}</div>')
        x += gw + 8
    body += box(M, 252, 384, '<p class="src">Codes HEX : médiane des pixels d\'une zone de chaque rendu (zones et méthode en '
                'planche 002). Valeurs indicatives, dépendantes de l\'éclairage des scènes : à valider sur échantillons physiques.</p>')
    page("201", "Palette générale", "Couleurs", body)
    for i, (role, ttl, sub) in enumerate(groups):
        ks = [k for k, v in PA.COLOURS.items() if v[1] == role]
        body = head(f"2.{i + 2}", ttl, f"{sub.split(' ')[0]} {' '.join(sub.split(' ')[1:-1])} <em>{sub.split(' ')[-1]}</em>", w=380)
        cw = (W - 2 * M - 2 * 10) / 3
        for j, k in enumerate(ks):
            name, _, sample, visual, usage = PA.COLOURS[k]
            hx, rgb = COL[k]
            x = M + j * (cw + 10)
            body += f'<div class="sw" style="left:{x:.1f}mm;top:62mm;width:{cw:.1f}mm;height:108mm;background:{hx}"></div>'
            p = cut(visual[0], visual[1], f"col-{k}")
            body += ext(p, x, 172, cw, 58, f"extrait — rendu {visual[0]}")
            body += box(x, 234, cw, f'<div class="cname"><span>{k}</span>{esc(name)}</div>'
                        f'<div class="ccode">{hx} · RVB {rgb[0]} {rgb[1]} {rgb[2]}</div><p>{esc(usage)}</p>'
                        + ('<p class="src">Teinte de la lumière telle que rendue ; température de couleur (K) : '
                           '<span class="st-c">À CONFIRMER</span>.</p>' if k == "C9" else ""))
        page(f"20{i + 2}", ttl, "Couleurs", body)
    # 205 colours in space
    body = head("2.5", "Les couleurs dans l'espace", "Où se trouve <em>chaque couleur</em>", w=380, y=M - 4)
    marks = {"02": [("C1", (600, 330)), ("C3", (700, 30)), ("C9", (1000, 56)), ("C2", (160, 1700)), ("C4", (590, 1420)),
                    ("C6", (470, 700)), ("C7", (1150, 960)), ("C8", (1060, 1110))],
             "06": [("C1", (900, 300)), ("C4", (850, 1300)), ("C5", (1060, 1110)), ("C8", (790, 1070)),
                    ("C9", (1470, 640)), ("C2", (740, 1180))]}
    x = M
    for n in ("02", "06"):
        img, r = whole(n, x, 52, 186, 200)
        body += img + pins(n, *r, marks[n]) + box(r[0], r[1] + r[3] + 2, r[2], f'<p class="src">Rendu {n} — '
                                                   f'{esc(T.RENDERS[n][2])}</p>')
        x += 198
    page("205", "Les couleurs dans l'espace", "Couleurs", body)


# ================================================================ 3 — MATERIALS
def s3():
    opener("3", "Palette de matériaux et finitions", "Matières <em>et finitions</em>",
           "Dix-huit matières et finitions identifiées sur les rendus, classées par famille. Chacune a son visuel, son nom, "
           "sa finition observée et son emplacement ; leur nature exacte et leurs références restent à confirmer.", "07",
           PA.FAMILIES)
    body = head("3.1", "Vue d'ensemble", "Les matières <em>du projet</em>", w=380, y=M - 4)
    ks = list(PA.MATERIALS)
    cw, ch = (W - 2 * M - 5 * 6) / 6, 56
    for i, k in enumerate(ks):
        x, y = M + (i % 6) * (cw + 6), 50 + (i // 6) * (ch + 22)
        name, fam, fin, loc, n, b, ck, note = PA.MATERIALS[k]
        body += ext(cut(n, b, f"mat-{k}"), x, y, cw, ch, k)
        body += box(x, y + ch + 1.5, cw, f'<div class="mn">{esc(name)}</div><div class="mf">{esc(fam)}</div>')
    page("301", "Vue d'ensemble des matériaux", "Matériaux", body)
    for i, fam in enumerate(PA.FAMILIES):
        ks = [k for k, v in PA.MATERIALS.items() if v[1] == fam]
        words = fam.split(" ")
        body = head(f"3.{i + 2}", "Palette de matériaux", f"{' '.join(words[:-1])} <em>{words[-1]}</em>", w=380)
        n_ = len(ks)
        cw = (W - 2 * M - (n_ - 1) * 12) / n_
        for j, k in enumerate(ks):
            name, _, fin, loc, n, b, ck, note = PA.MATERIALS[k]
            x = M + j * (cw + 12)
            hx = mat_hex(k)
            body += ext(cut(n, b, f"mat-{k}"), x, 62, cw, 140 if n_ < 3 else 124, k)
            chip = f'<span class="chip" style="background:{hx}"></span>{hx} ({ck})' if hx else "teinte non relevable (verre, métal, reflets)"
            body += box(x, 208 if n_ < 3 else 192, cw, f"""<div class="cname"><span>{k}</span>{esc(name)}</div>
<table class="mt"><tr><th>Finition observée</th><td>{esc(fin)}</td></tr>
<tr><th>Emplacement</th><td>{esc(loc)}</td></tr><tr><th>Teinte relevée</th><td>{chip}</td></tr>
<tr><th>Nature, référence</th><td class="st-c">{esc(note)}</td></tr>
<tr><th>Visuel</th><td>extrait du rendu {n}</td></tr></table>""")
        page(f"30{i + 2}", fam, "Matériaux", body)
    rows = ""
    for k, (name, fam, fin, loc, n, b, ck, note) in PA.MATERIALS.items():
        hx = mat_hex(k)
        chip = f'<span class="chip" style="background:{hx}"></span>' if hx else '<span class="chip none">—</span>'
        rows += (f'<tr><td>{chip}</td><td class="ref">{k}</td><td><b>{esc(name)}</b></td><td>{esc(fam)}</td><td>{esc(fin)}</td>'
                 f'<td>{esc(loc)}</td><td>{hx or "—"}</td><td class="st-c">à confirmer</td></tr>')
    body = head("3.9", "Nomenclature", "Matériaux <em>et finitions</em>", w=380, y=M - 4)
    body += box(M, 50, 384, f'<table class="tb3"><tr><th></th><th>Code</th><th>Matériau</th><th>Famille</th><th>Finition '
                f'observée</th><th>Emplacement</th><th>Teinte</th><th>Référence</th></tr>{rows}</table>')
    page("309", "Nomenclature des matériaux", "Matériaux", body)


# ================================================================ 4 — DETAILS
def framed(n, x, y, h, ds):
    return X.framed_render(n, x, y, h, ds)


def s4():
    opener("4", "Planches de détails décoratifs", "Vues rapprochées, <em>détail par détail</em>",
           "Trente-neuf extraits agrandis des rendus, numérotés D01 à D39. Sur chaque planche, le rendu original reste "
           "présenté en entier ; la zone agrandie y est encadrée et porte le même numéro.", "08",
           T.CATEGORIES[:11])
    rows = ""
    for c in T.CATEGORIES:
        ds = [d for d in T.D if T.D[d][2] == c]
        rows += f'<div class="ic"><div class="kick">{esc(c)}</div>' + "".join(
            f'<div class="ir"><b>{d}</b><span>{esc(T.D[d][0])}</span><i>pl. {plate_of(d)}</i></div>' for d in ds) + "</div>"
    body = head("4.1", "Index des détails", "Trente-neuf détails, <em>douze familles</em>", w=380, y=M - 4)
    body += box(M, 50, 384, f'<div class="idx">{rows}</div>')
    page("401", "Index des détails décoratifs", "Détails", body)
    for num, title, n, ds in T.PLATES:
        base_h = 236
        img, w = framed(n, M, 34, base_h, ds)
        mmpx = w / size(n)[0]
        body = box(M, M - 4, 300, f'{kicker("Détails décoratifs · " + T.D[ds[0]][2])}<h2 class="ph">{esc(title)}</h2>')
        body += img + box(M, 34 + base_h + 2, w, f'<p class="src"><b>Rendu {n}</b> ({T.RENDERS[n][0]}) — rendu original '
                                                  f'entier ; les cadres numérotés repèrent les zones agrandies.</p>')
        cx, cw = M + w + 10, W - 2 * M - w - 10
        cell = 254 / 3 if len(ds) == 3 else 254 / 2
        for j, d in enumerate(ds):
            t, desc, cat, _, b = T.D[d]
            p = dcut(d)
            pw, ph = b[2] - b[0], b[3] - b[1]
            s = min(cw / pw, (cell - 24) / ph)
            iw, ih = pw * s, ph * s
            y = 30 + j * cell
            body += ext(p, cx, y, iw, ih, d, "fill", "ex zoom")
            body += box(cx, y + ih + 1.6, cw, f'<div class="zt">{d} · {esc(t)}</div><div class="zd">{esc(desc)}</div>'
                        f'<div class="zs">{esc(cat)} · extrait du rendu {n} · agrandissement ×{s / mmpx:.1f}</div>'
                        .replace("×" + f"{s / mmpx:.1f}", "×" + f"{s / mmpx:.1f}".replace(".", ",")))
        page(num, f"Détails — {title}", "Détails", body)


# ================================================================ 5 — TECHNICAL
def s5():
    opener("5", "Dossier technique", "Plans, élévations <em>et coupes</em>",
           "Le dossier technique reprend les cotes écrites du plan coté et relève les autres sur la maquette et les rendus. "
           "Chaque cote porte son statut : vérifiée, déduite (≈) ou à confirmer.", "03",
           ["Plan d'aménagement coté", "Plan de repérage et revêtement de sol", "Élévations A à F", "Coupes AA et BB",
            "Dimensions des équipements", "Mobilier sur mesure M1 et M2", "Revêtements", "Installations"])
    X.SHEETS.clear()
    X.series200()
    old = {s["num"]: s for s in X.SHEETS}
    remap = [("201", "501"), ("202", "502"), ("204", "503"), ("205", "504"), ("206", "505"), ("207", "506"), ("208", "507"),
             ("209", "508"), ("210", "509")]
    for a, b in remap:
        s = old[a]
        page(b, s["title"], "Dossier technique", s["body"], "tech", s["scale"])
    # 510 — equipment dimensions
    rows = "".join(f'<tr><td><b>{esc(e[0])}</b><br><span class="small">{esc(e[1])}</span></td><td>' + "<br>".join(
        f'{esc(l)} : <span class="st-{st}">{esc(v)}</span>' for l, v, st in e[4]) + f'</td><td>{esc(e[5])}</td>'
        f'<td class="ref">{esc(e[8])}</td></tr>' for e in PA.EQUIP)
    half = (len(PA.EQUIP) + 1) // 2
    rws = rows.split("</tr>")
    tbl = lambda rr: (f'<table class="tb2 full"><tr><th>Élément</th><th>Dimensions disponibles</th><th>Matériaux</th>'
                      f'<th>Planches</th></tr>{"</tr>".join(rr)}</tr></table>')
    body = (X.box(AX + 2, AY + 2, 160, '<div class="nh">Dimensions des équipements</div>' + tbl(rws[:half]))
            + X.box(AX + 168, AY + 7.3, 160, tbl(rws[half:-1])))
    page("510", "Dimensions des équipements", "Dossier technique", body, "tech")
    page("511", old["211"]["title"], "Dossier technique", old["211"]["body"], "tech", "1:10")
    page("512", old["212"]["title"], "Dossier technique", old["212"]["body"], "tech", "1:10")
    # 513 — finishes by wall
    rows = "".join(f'<tr><td class="ref">{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in [
        ("A — sud", "Effet travertin, toute hauteur ; coffrage WC en faïence bordeaux (116 × 40, H ≈ 145)",
         "Fenêtres F1 et F2 : encadrements blancs", "503"),
        ("B — est", "Effet travertin ; crédence effet terrazzo ≈ 16 de haut sous le miroir", "Miroir ≈ 175 × 100", "504"),
        ("C — nord", "Effet travertin, toute hauteur", "Porte P1 74 × ≈ 202", "505"),
        ("D — ouest", "Effet travertin ; dans la douche : effet travertin (mur latéral)", "Colonne de douche", "506"),
        ("E — fond de douche", "Faïence bordeaux brillante, pose verticale, toute hauteur et toute largeur (164,80)",
         "Rangement : niche ou étagère À CONF.", "507"),
        ("F — retour", "Effet travertin ; chant de faïence côté douche", "Patères", "505"),
        ("Sol", "Dalles « galets » blanches veinées et inserts noirs, pièce et douche", "Seuil de douche ≈ 8,5", "502"),
        ("Plafond", "Faux plafond peint blanc, gorge LED en périphérie", "H ≈ 289", "601 · 602"),
    ])
    t = (f'<div class="nh">Revêtements — localisation par paroi</div><table class="tb2 full"><tr><th>Paroi</th><th>Revêtement'
         f'</th><th>Éléments</th><th>Planche</th></tr>{rows}</table>'
         '<div class="nh" style="margin-top:4mm">Calepinage relevé</div><table class="tb2 full">'
         '<tr><td>Faïence bordeaux</td><td>Entraxe des joints ≈ 7,7 × 17,7 (relevé sur le coffrage, rendu 02 : 14 colonnes, '
         '6 rangs) — format et joint <span class="st-c">À CONF.</span></td></tr>'
         '<tr><td>Effet travertin</td><td>Joints non visibles sur les rendus — format des panneaux <span class="st-c">À CONF.</span></td></tr>'
         '<tr><td>Dalles « galets »</td><td>Motif à grande échelle ; format, sens de pose et départ du calepinage '
         '<span class="st-c">À CONF.</span></td></tr></table>')
    side = X.notes(["Toutes les parois sont relevées sur les rendus ; aucune référence ni format n'est inventé.",
                    "Pièce humide : classement des revêtements (glissance du sol de douche, étanchéité sous carrelage, "
                    "résistance à l'eau des panneaux) à vérifier avec les fournisseurs."])
    page("513", "Revêtements — localisation et calepinage", "Dossier technique",
         X.box(AX + 2, AY + 2, 236, t) + X.box(AX + 244, AY + 2, 82, side), "tech")
    # 514 — installations
    svg, w, h = V.plan(20, "install")
    side = X.notes([
        "<b>Eau</b> (cercles bleus) : alimentations eau froide / eau chaude ; <b>évacuations</b> (carrés) : eaux usées "
        "et eaux vannes. Positions en plan relevées sur les équipements ; hauteurs et diamètres <span class='st-c'>À CONF.</span>",
        "Lavabo : axe ≈ 137 depuis le mur sud. WC : axe ≈ 78, dans le coffrage. Douche : colonne sur le mur ouest, mitigeur "
        "≈ 100 ; évacuation non visible.",
        "<b>Électricité</b> (triangles) : miroir rétroéclairé, suspensions (plafond), gorge LED (voir 601). Alimentation, "
        "transformateurs, interrupteurs et prises : non visibles — <span class='st-c'>À CONF.</span>",
        "Ventilation et chauffage : non visibles sur les documents — <span class='st-c'>À CONF.</span>",
        "Volumes de sécurité de la zone humide et indices de protection : à vérifier par l'électricien.",
    ], "Installations")
    page("514", "Installations — points d'eau et électricité", "Dossier technique",
         X.place(svg, AX, AY) + X.vtitle(AX + 4, AY + h - 2, w - 8, "I", "Plan des installations", "1:20")
         + X.box(AX + w + 4, AY + 4, AW - w - 6, side), "tech", "1:20")


# ================================================================ 6 — LIGHTING
def s6():
    opener("6", "Éclairage", "Une lumière <em>indirecte et chaude</em>",
           "La lumière vient des bords : une gorge LED en périphérie du plafond, le halo du miroir et quatre suspensions "
           "à globe devant le plan vasque. Aucune source nue n'éclaire la pièce.", "01",
           ["Plan d'éclairage", "Gorge lumineuse et éclairage indirect", "Éclairage du miroir et éclairage décoratif",
            "Points lumineux"])
    X.SHEETS.clear()
    X.series200()
    s = next(s for s in X.SHEETS if s["num"] == "203")
    page("601", "Plan d'éclairage et de plafond", "Éclairage", s["body"], "tech", "1:25")
    svg, w, h = V.gorge_principle()
    k = 1.55
    svg = svg.replace(f'width="{w:.2f}mm" height="{h:.2f}mm"', f'width="{w * k:.2f}mm" height="{h * k:.2f}mm"')
    body = X.place(svg, AX + 4, AY + 8) + X.vtitle(AX + 4, AY + 8 + h * k + 6, w * k - 8, "G", "Gorge lumineuse — principe",
                                                   "sans échelle")
    side = X.notes([
        "Ligne LED continue en périphérie du faux plafond, visible sur les rendus 01, 02, 04 et 06.",
        "Retrait par rapport aux murs : ≈ 28 relevé sur le rendu 02, ≈ 9 sur le rendu 06 — <span class='st-c'>À CONF.</span>",
        "Profilé, diffuseur, puissance, température de couleur et indice de protection : <span class='st-c'>À CONF.</span>",
        "Hauteur sous faux plafond ≈ 289 (rendus 02, 06, 08). Épaisseur du faux plafond et de la retombée : "
        "<span class='st-c'>À CONF.</span>",
        "Le schéma montre le principe d'une gorge rasante ; ses proportions ne sont pas des cotes.",
    ], "Gorge lumineuse")
    sx = AX + w * k + 12
    body += X.box(sx, AY + 4, AW - (sx - AX) - 2, side)
    y = AY + 92
    for j, d in enumerate(("D09", "D27")):
        p = dcut(d)
        b = T.D[d][4]
        tw = AW - (sx - AX) - 2
        th = min(tw * (b[3] - b[1]) / (b[2] - b[0]), 62)
        tw = th * (b[2] - b[0]) / (b[3] - b[1])
        body += f'<div class="zoom-t" style="left:{sx:.1f}mm;top:{y:.1f}mm;width:{tw:.1f}mm;height:{th:.1f}mm"><img src="{p.as_uri()}"></div>'
        body += X.box(sx, y + th + 1, AW - (sx - AX) - 2, f'<p class="small"><b>{d}</b> — {esc(T.D[d][0])} (rendu {T.D[d][3]}, pl. {plate_of(d)})</p>')
        y += th + 14
    page("602", "Gorge lumineuse et éclairage indirect", "Éclairage", body, "tech", "—")
    # 603 mirror + decorative (editorial)
    body = head("6.3", "Éclairage du miroir et éclairage décoratif", "Le miroir, <em>les globes</em>", w=380, y=M - 4)
    items = [("D30", "Miroir rétroéclairé", "Le grand miroir (≈ 175 × 100) diffuse un halo sur son pourtour : une lumière "
              "douce pour le visage, sans ombre portée du plafond."),
             ("D31", "Le halo", "La lumière s'étale sur le mur effet travertin et révèle son veinage."),
             ("D32", "Suspensions à globe", "Quatre globes à hauteurs décalées (≈ 123 et ≈ 144) devant le bord du plan : "
              "l'éclairage décoratif de la pièce, à hauteur du regard.")]
    cw = (W - 2 * M - 2 * 12) / 3
    for i, (d, t, txt) in enumerate(items):
        x = M + i * (cw + 12)
        body += ext(dcut(d), x, 54, cw, 150, d)
        body += box(x, 210, cw, f'<h3>{t}</h3><p>{txt}</p><p class="src">Extrait {d} — rendu {T.D[d][3]} · '
                                f'pl. {plate_of(d)}</p>')
    body += box(M, 264, 384, '<p class="src">Modèles, puissances, température de couleur et commandes : '
                '<span class="st-c">À CONFIRMER</span>.</p>')
    page("603", "Éclairage du miroir et éclairage décoratif", "Éclairage", body)
    # 604 lighting points table
    rows = "".join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td><td class="st-c">À CONF.</td></tr>' for a, b, c, d in [
        ("Gorge LED périphérique", "Éclairage indirect général", "Tout le périmètre du faux plafond", "retrait ≈ 9 à ≈ 28 (À CONF.)"),
        ("Miroir rétroéclairé", "Éclairage du visage", "Mur est, au-dessus du plan vasque", "≈ 175 × 100 · bas ≈ 99"),
        ("Suspensions à globe (×4)", "Éclairage décoratif", "Devant le bord du plan vasque", "H ≈ 123 et ≈ 144"),
        ("Cabine de douche", "Éclairage de la douche", "Aucun luminaire visible sur les rendus", "—"),
    ])
    body = head("6.4", "Points lumineux", "Trois couches <em>de lumière</em>", w=380)
    body += box(M, 62, 250, f'<table class="tb3"><tr><th>Point lumineux</th><th>Rôle</th><th>Emplacement</th>'
                f'<th>Relevé</th><th>Modèle, puissance, K, IP</th></tr>{rows}</table>'
                '<p class="small" style="margin-top:4mm">Circuits, interrupteurs, variation et scénarios d\'allumage : '
                'non visibles sur les documents — <span class="st-c">À CONFIRMER</span>.</p>')
    img, r = whole("01", 280, 58, 122, 200)
    body += img + box(r[0], r[1] + r[3] + 2, r[2], '<p class="src">Rendu 01 — les trois couches de lumière.</p>')
    page("604", "Points lumineux", "Éclairage", body)


# ================================================================ 7 — FURNITURE AND EQUIPMENT
def s7():
    opener("7", "Mobilier et équipements", "Chaque élément, <em>présenté séparément</em>",
           "Dix-sept fiches : mobilier sur mesure, sanitaires, robinetterie, luminaires et accessoires, avec les dimensions "
           "disponibles, les matériaux, les finitions et les détails de conception.", "04")
    per = 3
    for pg in range(0, len(PA.EQUIP), per):
        items = PA.EQUIP[pg:pg + per]
        body = box(M, M - 4, 380, kicker(f"Mobilier et équipements · fiches {pg + 1} à {pg + len(items)}"))
        cw = (W - 2 * M - 2 * 12) / 3
        for j, e in enumerate(items):
            name, cat, n, b, dims, mats, fin, det, links = e
            x = M + j * (cw + 12)
            pw, ph = b[2] - b[0], b[3] - b[1]
            ih = min(118, cw * ph / pw)
            body += ext(cut(n, b, f"eq-{pg + j:02d}"), x, 30, cw, 118, f"{pg + j + 1:02d}", "contain", "ex eq")
            dl = "".join(f'<tr><th>{esc(l)}</th><td class="st-{st}">{esc(v)}</td></tr>' for l, v, st in dims)
            body += box(x, 152, cw, f"""<div class="kick">{esc(cat)}</div><div class="cname">{esc(name)}</div>
<table class="mt">{dl}<tr><th>Matériaux</th><td>{esc(mats)}</td></tr><tr><th>Finition</th><td>{esc(fin)}</td></tr>
<tr><th>Conception</th><td>{esc(det)}</td></tr><tr><th>Référence</th><td class="st-c">À CONFIRMER</td></tr>
<tr><th>Planches</th><td>{esc(links)}</td></tr></table><p class="src">Visuel : extrait du rendu {n}</p>""")
        page(f"7{pg // per + 1:02d}", f"Mobilier et équipements — fiches {pg + 1} à {pg + len(items)}", "Mobilier", body)


# ================================================================ 8 — RENDERS
RVIEW = {   # camera → target (cm, indicative), elevations, materials seen
    "01": ((70, 225, 330, 30), "504 · 503", ["M01", "M02", "M04", "M06", "M08", "M10", "M11", "M13", "M14", "M16", "M17"]),
    "06": ((110, 110, 374, 110), "504", ["M01", "M02", "M04", "M06", "M07", "M10", "M11", "M12", "M13", "M15", "M16", "M17"]),
    "02": ((187, 225, 187, 2), "503", ["M01", "M03", "M04", "M06", "M08", "M11", "M14", "M15", "M16", "M17"]),
    "04": ((330, 220, 30, 70), "503 · 506", ["M01", "M03", "M04", "M08", "M11", "M14", "M15", "M16", "M17"]),
    "08": ((95, 150, 75, 369), "507", ["M01", "M03", "M04", "M05", "M07", "M09", "M11", "M18"]),
    "07": ((160, 90, 40, 340), "507 · 505", ["M01", "M03", "M04", "M05", "M09", "M11", "M18"]),
    "03": (None, "501 · 502", ["M01", "M03", "M04", "M05", "M06", "M09", "M13", "M15"]),
}


def s8():
    opener("8", "Rendus 3D", "Les rendus, <em>en grand format</em>",
           "Les sept rendus du projet, présentés en entier et sans retouche. Chacun est associé à son point de vue sur le plan, "
           "à l'élévation correspondante, aux matériaux visibles et aux détails qui en sont extraits.", "02")
    for i, n in enumerate(T.RENDER_ORDER):
        name, cap, view = T.RENDERS[n]
        img, r = whole(n, M, 14, 250, 268, "left")
        v, elev, mats = RVIEW[n]
        svg, kw, kh = V.plan(70, "key", view=v)
        px = r[0] + r[2] + 12
        pw = W - M - px
        dets = [d for d in T.D if T.D[d][3] == n]
        th = "".join(f'<div class="th"><img src="{dcut(d).as_uri()}"><span>{d}</span></div>' for d in dets[:8])
        chips = "".join(f'<div class="mc2"><img src="{cut(PA.MATERIALS[k][4], PA.MATERIALS[k][5], "mat-" + k).as_uri()}">'
                        f'<span>{k}</span></div>' for k in mats)
        body = img + box(px, 16, pw, f"""<div class="kick">Rendu 3D · {i + 1} / 7</div><h2 class="ph">Rendu {n}</h2>
<p>{esc(cap)}</p><p class="src">{esc(view)} · fichier {name}.png ({size(n)[0]} × {size(n)[1]} px), inséré en entier.</p>""")
        body += f'<div class="v" style="left:{px:.1f}mm;top:70mm">{svg}</div>'
        body += box(px, 70 + kh + 1, pw, f"""<p class="src">{'Point de vue indicatif' if v else 'Vue de dessus de la pièce'}
 — plan coté : 501 · élévations : {elev}</p>
<div class="kick" style="margin-top:3mm">Matériaux visibles</div><div class="mcg">{chips}</div>
<div class="kick" style="margin-top:3mm">Détails extraits ({len(dets)})</div><div class="ths">{th}</div>""")
        page(f"8{i + 1:02d}", f"Rendu 3D {n} — {view}", "Rendus 3D", body)


# ================================================================ 9 — SYNTHESIS
def s9():
    body = head("9.1", "Planche de synthèse", "Couleurs, matériaux, <em>équipements et décor</em>", w=380, y=M - 6)
    cols = "".join(f'<div class="sy-c"><i style="background:{COL[k][0]}"></i><b>{k} {esc(v[0])}</b><span>{COL[k][0]}</span></div>'
                   for k, v in PA.COLOURS.items())
    mats = "".join(f'<div class="sy-m"><img src="{cut(v[4], v[5], "mat-" + k).as_uri()}"><b>{k}</b><span>{esc(v[0])}</span></div>'
                   for k, v in PA.MATERIALS.items())
    eqs = "".join(f'<div class="sy-e"><img src="{cut(e[2], e[3], f"eq-{i:02d}").as_uri()}"><span>{esc(e[0])}</span></div>'
                  for i, e in enumerate(PA.EQUIP))
    deco = "".join(f'<div class="sy-e"><img src="{dcut(d).as_uri()}"><span>{d} {esc(T.D[d][0])}</span></div>'
                   for d in ("D36", "D37", "D38", "D39", "D17", "D28"))
    body += box(M, 46, 62, f'<div class="kick">Couleurs</div>{cols}')
    body += box(M + 70, 46, 150, f'<div class="kick">Matériaux et finitions</div><div class="sy-mg">{mats}</div>')
    body += box(M + 228, 46, 156, f'<div class="kick">Mobilier et équipements</div><div class="sy-eg">{eqs}</div>'
                f'<div class="kick" style="margin-top:3mm">Éléments décoratifs</div><div class="sy-eg">{deco}</div>')
    page("901", "Planche de synthèse", "Synthèse", body)
    img, r = whole("06", W - 200, M, 182, 252)
    body = head("9.2", "Synthèse esthétique", "Une pièce d'eau <em>cohérente et singulière</em>", w=r[0] - M - 14)
    body += box(M, 70, r[0] - M - 16, """<p class="lead">Une enveloppe minérale unique, un sol graphique, trois accents : la
douche principale applique à une pièce d'eau la même exigence que les pièces à vivre de la villa.</p>
<p>Le travertin des murs et le blanc veiné du sol installent le calme ; le noyer apporte la chaleur à hauteur de main ;
le bordeaux signale les deux zones d'eau ; le noir mat dessine les équipements. La lumière, toujours indirecte, relie
l'ensemble.</p>
<p>Le dossier technique fixe ce qui est connu — cotes écrites du plan, relevés sur la maquette et les rendus — et
signale clairement ce qui reste à confirmer avant exécution (planche 990).</p>""") + img
    page("902", "Synthèse esthétique", "Synthèse", body)
    items = [
        ("Plan", "Sens d'ouverture de la porte P1 et de la porte de douche ; épaisseur réelle des murs (≈ 20 relevée)."),
        ("Plan", "Cote « 478 » du plan coté (partie chambre) : ≈ 386 à l'échelle — À VÉRIFIER, non corrigée."),
        ("Plan", "Rectangle de ≈ 196 × 192 tracé sur le plan coté contre les murs est et sud, sans cote ni équivalent sur les "
                 "rendus : non dessiné — À VÉRIFIER."),
        ("Douche", "Sol : receveur extra-plat ou douche à l'italienne ; pente ; position de l'évacuation ; hauteur du seuil (≈ 8,5)."),
        ("Douche", "Rangement des produits : niche encastrée ou étagère ; dimensions."),
        ("Éclairage", "Éclairage de la douche (aucun luminaire visible) ; indices de protection ; circuits et commandes."),
        ("Éclairage", "Retrait de la gorge LED (≈ 28 ou ≈ 9 selon le rendu) ; profilé ; température de couleur ; épaisseur du faux plafond."),
        ("Mobilier", "Épaisseur du plan effet terrazzo ; largeur de la vasque ; quincaillerie et fixations du meuble M1."),
        ("Mobilier", "Poignées et finition de la commode M2 ; dimensions de l'échelle porte-serviettes ; position de la seconde patère."),
        ("Matériaux", "Nature, références, formats et finitions : effet travertin, faïence bordeaux (entraxe ≈ 7,7 × 17,7), "
                      "dalles « galets » et inserts, effet terrazzo, bois teinte noyer, verre fumé, paroi, métal noir mat."),
        ("Équipements", "Marques et modèles : WC, plaque de commande, robinetterie, colonne, paroi, vasque, miroir, suspensions, LED."),
        ("Installations", "Hauteurs et diamètres des alimentations et évacuations ; ventilation ; chauffage ; prises."),
    ]
    rows = "".join(f'<tr><td class="ref">{esc(a)}</td><td>{esc(b)}</td></tr>' for a, b in items)
    body = head("9.3", "Points à confirmer", "Avant exécution, <em>à confirmer</em>", w=380, y=M - 4)
    body += box(M, 50, 384, f'<table class="tb3"><tr><th>Sujet</th><th>À confirmer</th></tr>{rows}</table>'
                '<p class="small" style="margin-top:4mm">Toutes les cotes « ≈ » sont des relevés sur les documents du projet : '
                'à vérifier sur site avant fabrication. Aucune cote, aucun matériau et aucune référence n\'ont été inventés.</p>')
    page("990", "Points à confirmer", "Synthèse", body)
    logo = LOGO.read_text()
    img, r = whole("07", 0, 0, 272, H, "left")
    page("999", "Dos", "Dos", img + f'<div class="back" style="left:{r[2]:.1f}mm"><div class="cv-logo">{logo}</div>'
         f'<div class="rule"></div><p>{PROJECT}<br>{DOC}<br>Indice {INDICE} — {DATE}</p></div>', cls="p-back")


# ================================================================ chrome, toc, css
def title_block(pg, i, total):
    logo = LOGO.read_text()
    return f"""<div class="tb">
 <div class="tb-logo">{logo}</div>
 <div class="tb-firm">KAÏRA INTERIOR DESIGN<span>Architecture intérieure</span></div>
 <div class="tb-sec"><label>Projet</label><div>{PROJECT}</div></div>
 <div class="tb-sec"><label>Document</label><div>{DOC}</div></div>
 <div class="tb-sec"><label>Section</label><div>{esc(pg['section'])}</div></div>
 <div class="tb-sec tb-title"><label>Titre de la planche</label><div>{esc(pg['title'])}</div></div>
 <div class="tb-grid"><div><label>Échelle</label>{pg['scale']}</div><div><label>Format</label>A3</div>
  <div><label>Date</label>{DATE}</div><div><label>Indice</label>{INDICE}</div></div>
 <div class="tb-legend"><div><span class="st-v">374,8</span> cote vérifiée (plan source)</div>
  <div><span class="st-d"><i>≈ 59</i></span> cote déduite (relevé)</div><div><span class="st-c">À CONF.</span> cote à confirmer</div></div>
 <div class="tb-status">{STATUS}</div>
 <div class="tb-note">Cotes en cm. Ne pas mesurer sur le dessin. Toutes les cotes sont à vérifier sur site avant exécution.</div>
 <div class="tb-num"><label>N° de dessin</label><div>KAI-DPE-{pg['num']}</div></div>
 <div class="tb-page">Planche {i} / {total}</div>
</div>"""


def folio(pg, i, total):
    first = "KAÏRA" if pg["cls"] == "p-open" else "KAÏRA Interior Design · Douche principale – Étage 1"
    return (f'<div class="fol"><span>{first}</span><span>{esc(pg["section"])}</span>'
            f'<span>KAI-DPE-{pg["num"]} · indice {INDICE} · <b>{i}</b> / {total}</span></div>')


def toc_html(total):
    index = {p["num"]: i for i, p in enumerate(PAGES, 1)}
    groups = [("Présentation", ["000", "001", "002"])] + [
        (f"{n} · {k}", [p["num"] for p in PAGES if p["num"][0] == n and p["num"] not in ("000", "001", "002", "999")])
        for n, k, t, _ in SECTIONS] + [("9 · Synthèse", ["901", "902", "990"])]
    out = ""
    for g, nums in groups:
        out += f'<div class="tg"><div class="kick">{esc(g)}</div>'
        for n in nums:
            if n in index:
                pg = PAGES[index[n] - 1]
                out += (f'<div class="tr"><b>KAI-DPE-{n}</b><span>{esc(pg["title"])}</span><i>{index[n]}</i></div>')
        out += "</div>"
    return box(M, M - 2, 384, f'{kicker("Sommaire")}<h2>Contenu <em>du dossier</em></h2><div class="toc2">{out}</div>')


ED_CSS = """
@font-face{font-family:Cormorant;font-weight:300;font-style:italic;src:url(FONTS/cormorant-garamond-latin-300-italic.woff2)}
@font-face{font-family:Cormorant;font-weight:400;font-style:italic;src:url(FONTS/cormorant-garamond-latin-400-italic.woff2)}
.sheet.ed{background:#F5F1EB;color:#2B2622}
.ed .ebox{position:absolute;font-size:3.5mm;line-height:1.55;font-weight:300}
.ed h1{font-family:Cormorant;font-weight:300;font-size:21mm;line-height:1.0;margin:4mm 0 0}
.ed h2{font-family:Cormorant;font-weight:300;font-size:12.5mm;line-height:1.06;margin:0 0 3mm}
.ed h2.xl{font-size:17mm}.ed h2.ph{font-size:9mm;margin:0}
.ed h3{font-family:Cormorant;font-weight:400;font-size:6.6mm;line-height:1.1;margin:0 0 2mm}
.ed em{font-style:italic;color:#8C7462}
.ed p{margin:0 0 3mm}.ed .lead{font-size:5mm;line-height:1.5;color:#2B2622}
.kick{font-weight:400;font-size:2.45mm;letter-spacing:.42em;text-transform:uppercase;color:#8C7462;margin-bottom:2.6mm}
.snum{font-family:Cormorant;font-size:7mm;color:#CDBFAE;margin-bottom:1mm}
.bignum{font-family:Cormorant;font-weight:300;font-size:40mm;line-height:.9;color:#CDBFAE;margin-bottom:4mm}
.rule{width:24mm;height:.35mm;background:#8C7462;margin:7mm 0}
.olist{list-style:none;padding:0;margin:4mm 0 0;columns:1}
.olist li{border-bottom:.2mm solid #CDBFAE;padding:1.8mm 0;font-size:3.2mm;letter-spacing:.04em}
.rw{position:absolute}.rw img{width:100%;height:100%;display:block}
.ov{position:absolute}
.ex{position:absolute;overflow:hidden;background:#E9E2D8}.ex img{width:100%;height:100%;display:block}
.ex.zoom{border:.3mm solid #3A2A22}.ex.eq{background:#EDE6DC}
.etag{position:absolute;left:0;top:0;background:#6E2234;color:#fff;font-weight:500;font-size:2.5mm;letter-spacing:.08em;padding:.7mm 1.8mm}
.src{font-size:2.55mm;color:#8C7462;letter-spacing:.03em}
.quote{font-family:Cormorant;font-style:italic;font-size:6.2mm;line-height:1.3;color:#3A2A22;border-left:.6mm solid #8C7462;padding-left:5mm}
.word{font-family:Cormorant;font-size:11mm;font-weight:300;color:#2B2622;margin-bottom:1mm}
.facts{margin-top:6mm;border-top:.3mm solid #8C7462}
.facts div{display:flex;gap:6mm;border-bottom:.2mm solid #CDBFAE;padding:2mm 0;font-size:3.2mm}
.facts span{width:42mm;flex:none;font-size:2.4mm;letter-spacing:.3em;text-transform:uppercase;color:#8C7462;padding-top:.6mm}
.prs .pr,.zn{display:flex;gap:5mm;border-bottom:.2mm solid #CDBFAE;padding:2.6mm 0}
.prs .pr span,.zn span{font-family:Cormorant;font-size:8mm;color:#8C7462;width:12mm;flex:none;line-height:1}
.zn span{display:inline-block;width:8mm;height:8mm;border-radius:4mm;background:#3A2A22;color:#fff;font-family:Jost;
 font-size:3.4mm;text-align:center;line-height:8mm;font-weight:500}
.prs b,.zn b{font-weight:500;font-size:3.4mm}.prs p,.zn p{margin:.6mm 0 0;font-size:3.1mm}
.bar{position:absolute;display:flex;flex-direction:column;justify-content:flex-end;padding:3mm 2.4mm;font-size:2.6mm;letter-spacing:.06em}
.bar span{font-weight:500}.bar b{font-weight:400}
.bn{font-size:2.9mm;line-height:1.3}
.sw{position:absolute;box-shadow:0 0 0 .2mm rgba(0,0,0,.08)}
.cname{font-family:Cormorant;font-size:7.6mm;line-height:1.1;margin-bottom:1.5mm}
.cname span{font-family:Jost;font-size:2.6mm;font-weight:500;color:#fff;background:#6E2234;padding:.5mm 1.6mm;margin-right:2.4mm;vertical-align:middle;letter-spacing:.06em}
.ccode{font-size:2.8mm;letter-spacing:.12em;color:#8C7462;margin-bottom:2mm}
.mn{font-size:2.8mm;font-weight:400;line-height:1.25}.mf{font-size:2.2mm;letter-spacing:.2em;text-transform:uppercase;color:#8C7462}
table.mt{border-collapse:collapse;width:100%;font-size:2.95mm;margin-top:1mm}
table.mt th{text-align:left;font-weight:400;font-size:2.25mm;letter-spacing:.18em;text-transform:uppercase;color:#8C7462;
 width:34%;padding:1.5mm 2mm 1.5mm 0;vertical-align:top;border-bottom:.2mm solid #CDBFAE}
table.mt td{padding:1.5mm 0;border-bottom:.2mm solid #CDBFAE;vertical-align:top}
.chip{display:inline-block;width:6mm;height:4mm;border:.15mm solid #999;vertical-align:-.6mm;margin-right:1.6mm}
.chip.none{border-style:dashed}
table.tb3{border-collapse:collapse;width:100%;font-size:2.9mm}
table.tb3 th{text-align:left;font-weight:400;font-size:2.2mm;letter-spacing:.18em;text-transform:uppercase;color:#8C7462;
 border-bottom:.35mm solid #3A2A22;padding:1.6mm 1.2mm}
table.tb3 td{border-bottom:.2mm solid #CDBFAE;padding:1.8mm 1.2mm;vertical-align:top}
td.ref{font-weight:500;color:#6E2234}
.ed .st-c{color:#8A1F35;font-weight:500}.ed .st-d{color:#55603C;font-style:italic}
.tag{display:inline-block;background:#6E2234;color:#fff;font-weight:500;font-size:2.3mm;padding:0 1.2mm}
.idx{columns:4;column-gap:8mm}.ic{break-inside:avoid;margin-bottom:4mm}
.ir{display:flex;gap:2.4mm;font-size:2.8mm;border-bottom:.15mm solid #CDBFAE;padding:1mm 0}
.ir b{color:#6E2234;font-weight:500;width:8mm;flex:none}.ir span{flex:1}.ir i{color:#8C7462;font-style:normal;font-size:2.4mm}
.zt{font-size:3mm;font-weight:500}.zd{font-size:2.7mm;line-height:1.4;color:#3A2A22;margin-top:.4mm}
.zs{font-size:2.1mm;letter-spacing:.14em;text-transform:uppercase;color:#8C7462;margin-top:.6mm}
.mcg{display:grid;grid-template-columns:repeat(6,1fr);gap:1.6mm}
.mc2 img,.th img{width:100%;height:13mm;object-fit:cover;display:block;border:.15mm solid #CDBFAE}
.mc2 span,.th span{font-size:2.2mm;color:#6E2234;font-weight:500}
.ths{display:grid;grid-template-columns:repeat(4,1fr);gap:1.8mm}.th img{height:17mm}
.toc2{columns:3;column-gap:10mm;margin-top:4mm}.tg{break-inside:avoid;margin-bottom:4mm}
.tr{display:flex;gap:2.6mm;border-bottom:.15mm solid #CDBFAE;padding:.9mm 0;font-size:2.75mm}
.tr b{font-weight:500;width:19mm;flex:none;font-size:2.5mm}.tr span{flex:1}.tr i{font-style:normal;color:#8C7462}
.fol{position:absolute;left:18mm;right:18mm;bottom:7mm;display:flex;justify-content:space-between;font-size:2.2mm;
 letter-spacing:.24em;text-transform:uppercase;color:#8C7462}
.fol b{font-family:Cormorant;font-size:4mm;letter-spacing:0;color:#2B2622;font-weight:400}
.p-open .fol{right:290mm}.p-open .fol span:nth-child(2){display:none}
.cv-panel{position:absolute;top:0;bottom:0;display:flex;flex-direction:column;justify-content:space-between;padding:20mm 0 16mm}
.cv-logo svg{width:62mm;height:auto}
.cv-proj{font-size:3.6mm;letter-spacing:.24em;text-transform:uppercase;color:#6E6258}
.cv-list{font-size:3.1mm;line-height:1.7;color:#3A2A22;border-top:.25mm solid #CDBFAE;padding-top:4mm;margin-top:6mm}
.cv-foot{font-size:2.6mm;letter-spacing:.2em;text-transform:uppercase;color:#6E6258;line-height:1.8}
.cv-foot span{color:#6E2234;font-weight:500}
.back{position:absolute;top:0;bottom:0;right:0;background:#2B2622;color:#EDE6DC;padding:120mm 18mm 0;font-size:3.2mm;line-height:1.7}
.back .cv-logo svg{width:60mm;filter:invert(1) brightness(1.6)}.back .rule{background:#CDBFAE}
.sy-c{display:flex;align-items:center;gap:2.4mm;font-size:2.8mm;border-bottom:.15mm solid #CDBFAE;padding:1.6mm 0}
.sy-c i{width:16mm;height:16mm;flex:none;box-shadow:0 0 0 .15mm rgba(0,0,0,.15)}.sy-c b{font-weight:400;flex:1}.sy-c span{color:#8C7462}
.sy-mg{display:grid;grid-template-columns:repeat(6,1fr);gap:2.2mm}
.sy-m img{width:100%;height:30mm;object-fit:cover;display:block}.sy-m b{display:block;font-size:2.3mm;color:#6E2234;font-weight:500;margin-top:.6mm}
.sy-m span{display:block;font-size:2.15mm;line-height:1.25}
.sy-eg{display:grid;grid-template-columns:repeat(6,1fr);gap:2mm}
.sy-e img{width:100%;height:24mm;object-fit:cover;display:block}.sy-e span{display:block;font-size:2.05mm;line-height:1.2;margin-top:.5mm}
.zoom-t{position:absolute;border:.25mm solid #3A2A22;overflow:hidden}.zoom-t img{width:100%;height:100%;display:block}
.ed .nl{padding-left:3.6mm;margin:0 0 3mm}.ed .nl li{margin:0 0 1mm;font-size:3.05mm}
.ed table.lg{border-collapse:collapse;width:100%;margin-bottom:4mm}.ed table.lg td{padding:1.8mm 1.4mm;border-bottom:.2mm solid #CDBFAE;vertical-align:top;font-size:3mm}
.ed td.big{font-size:5mm;white-space:nowrap;width:24mm}
.small{font-size:2.6mm;color:#6E6258}
"""


def main():
    BUILD.mkdir(exist_ok=True)
    import shutil
    shutil.rmtree(CROPS, ignore_errors=True)
    front()
    s1()
    s2()
    s3()
    s4()
    s5()
    s6()
    s7()
    s8()
    s9()
    total = len(PAGES)
    out = []
    for i, pg in enumerate(PAGES, 1):
        body = toc_html(total) if pg["body"] == "__TOC__" else pg["body"]
        if pg["kind"] == "tech":
            out.append(f'<section class="sheet"><div class="frame"></div>{body}{title_block(pg, i, total)}</section>')
        else:
            f = "" if pg["cls"] in ("p-cover", "p-back") else folio(pg, i, total)
            out.append(f'<section class="sheet ed {pg["cls"]}">{body}{f}</section>')
    css = (X.VB.CSS + X.EXTRA_CSS + ED_CSS).replace("FONTS/", FONTS.as_uri() + "/")
    doc = (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>KAÏRA — Douche principale – Étage 1</title>'
           f'<style>{css}</style></head><body>{V.PATTERNS}{"".join(out)}</body></html>')
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
    for f in BUILD.glob("prev-*.png"):
        f.unlink()
    args = ["node", "-e", js] + (["prev"] if "--previews" in sys.argv else [])
    subprocess.run(args, check=True, cwd=str(REPO / "projects/instagram-lancement/tools"))
    print(OUT_PDF)


if __name__ == "__main__":
    main()
