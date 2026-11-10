"""KAÏRA — Storyboard de la visite vidéo (4 espaces), composé en HTML puis exporté en PDF A4 paysage.
Réutilise les images et typographies du dossier (build/img, build/fonts) et tools/book.css."""
import html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / "build"

from PIL import Image
for rel in ["04-etage1-sejour/etage1-sejour-05.png"]:
    src = B / "tvoff" / pathlib.Path(rel).name
    src = src if src.exists() else ROOT / "sources" / rel
    Image.open(src).convert("RGB").save(B / "img" / (src.stem + ".jpg"), quality=90)

# Parcours indicatifs sur les plans d'aménagement (coordonnées en pixels des images de plan).
# n = numéro du plan-séquence, pts = trajet de la caméra (début -> fin).
PATH_RDC = [
    (1, [(395, 470), (300, 480)]),                       # entrée salon, avance
    (2, [(300, 455), (190, 430), (130, 455)]),           # travelling le long des canapés
    (3, [(170, 540), (230, 500)]),                       # arc vers le mur TV
    (4, [(380, 515), (450, 530), (520, 545)]),           # vers la salle à manger
    (5, [(640, 470), (720, 500)]),                       # détail bibliothèque / colonne
    (6, [(520, 300), (590, 270), (640, 215)]),           # couloir -> chambre d'amis
    (7, [(700, 200), (705, 160)]),                       # chambre d'amis, mur marbre
]
PATH_ET1 = [
    (8, [(330, 300), (230, 330), (170, 380)]),           # entrée séjour
    (9, [(140, 440), (210, 420)]),                       # mur TV séjour
    (10, [(560, 300), (560, 420), (640, 470)]),          # couloir -> chambre principale
    (11, [(700, 480), (620, 470)]),                      # finale, recul face tête de lit
]

SHOTS = [
 # n, espace, titre, image, durée, mouvement, détail caméra, transition
 (1, "Salon principal", "Ouverture — le seuil", "rdc-salon-10", "4 s",
  "Avancée lente (dolly avant) depuis la circulation, entre la double porte en bois foncé et le salon.",
  "Hauteur 1,60 m · objectif 24 mm · vitesse 0,3 m/s · départ en fondu du noir", "Fondu du noir"),
 (2, "Salon principal", "Révélation du salon", "rdc-salon-02", "6 s",
  "Travelling latéral le long des canapés modulaires, la caméra glisse vers le mur à l'œuvre graphique.",
  "Hauteur 1,40 m · 24 mm · 0,35 m/s · cadrage centré sur le tableau en fin de plan", "Coupe dans le mouvement"),
 (3, "Salon principal", "Le mur TV", "rdc-salon-03", "5 s",
  "Arc de caméra d'environ 20° autour de la table basse, face au mur TV rétroéclairé et à la baie.",
  "Hauteur 1,30 m · 24 mm · rotation lente, horizon parfaitement droit", "Enchaîné"),
 (4, "Salle à manger", "Sous la ligne de lumière", "rdc-salon-05", "5 s",
  "Avancée vers la table en pierre ; la suspension lumineuse entre dans le haut du cadre.",
  "Hauteur 1,55 m · 24 mm · 0,3 m/s · légère montée de 10 cm", "Enchaîné"),
 (5, "Salle à manger", "Détail — bibliothèque et marbre", "rdc-salon-01", "4 s",
  "Glissé latéral serré le long de la bibliothèque asymétrique et de la colonne en marbre veiné.",
  "Hauteur 1,40 m · 35 mm · 0,2 m/s · faible profondeur de champ (f/2,8)", "Coupe franche"),
 (6, "Chambre d'amis", "Entrée dans la chambre", "chambre-amis-03", "5 s",
  "Steadicam depuis la circulation, passage de la porte puis révélation du lit plateforme.",
  "Hauteur 1,60 m · 20 mm · 0,35 m/s", "Passage de porte (masque naturel)"),
 (7, "Chambre d'amis", "Le mur de marbre", "chambre-amis-02", "4 s",
  "Panoramique lent du lit vers le mur en marbre veiné, le meuble TV et la coiffeuse.",
  "Hauteur 1,40 m · 24 mm · rotation 15°", "Fondu enchaîné vers l'étage"),
 (8, "Séjour — étage 1", "Arrivée à l'étage", "etage1-sejour-08", "6 s",
  "Ouverture face à la double porte en bois vitrée, puis avancée qui découvre le salon et la grande œuvre rouge.",
  "Hauteur 1,60 m · 24 mm · 0,3 m/s", "Enchaîné"),
 (9, "Séjour — étage 1", "Bois et lumière", "etage1-sejour-05", "4 s",
  "Travelling latéral devant le mur TV et l'étagère verticale éclairée.",
  "Hauteur 1,30 m · 24 mm · 0,25 m/s", "Coupe dans le mouvement"),
 (10, "Chambre principale", "Vers la suite", "chambre-principale-04", "6 s",
  "Avancée dans le couloir lumineux, entrée dans la chambre devant le dressing en bois.",
  "Hauteur 1,60 m · 20 mm · 0,35 m/s · virage doux en fin de plan", "Enchaîné"),
 (11, "Chambre principale", "Finale — l'écrin", "chambre-principale-05", "7 s",
  "Plan final symétrique : lent recul face à la tête de lit et à la bande de marbre rétroéclairée, "
  "les gorges lumineuses s'intensifient.", "Hauteur 1,20 m · 24 mm · 0,15 m/s · fin en fondu vers le logo KAÏRA",
  "Fondu au noir + logo"),
]


def svg_path(pts, n):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    x0, y0 = pts[0]
    return (f'<path d="{d}" fill="none" stroke="#B5462F" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" '
            f'stroke-dasharray="9 6" marker-end="url(#a)"/>'
            f'<circle cx="{x0}" cy="{y0}" r="16" fill="#7A4A2A"/><text x="{x0}" y="{y0 + 5}" font-size="17" font-family="Jost" '
            f'font-weight="500" fill="#fff" text-anchor="middle">{n}</text>')


def plan_svg(img, w, h, paths):
    body = "".join(svg_path(p, n) for n, p in paths)
    return (f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet"><defs><marker id="a" viewBox="0 0 10 10" refX="7" refY="5" '
            f'markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10z" fill="#B5462F"/></marker></defs>'
            f'<image href="img/{img}" width="{w}" height="{h}"/>{body}</svg>')


pages = []
fol = lambda sec, n: (f'<div class="folio" style="left:14mm;right:14mm"><span>KAÏRA Interior Design · Storyboard visite vidéo</span>'
                      f'<span>{sec}</span><span class="pn">{n:02d}</span></div>')

pages.append(f"""<section class="page"><div class="cover">
<figure class="tile cover-img"><div class="ph" style="background-image:url(img/chambre-principale-05.jpg);background-position:50% 40%"></div></figure>
<div class="cover-panel"><div class="brand"><div class="wordmark">KAÏRA</div><div class="sub">INTERIOR DESIGN</div></div>
<div class="cover-title"><div class="kicker">Visite vidéo cinématique</div><h1>Storyboard<br><em>de la visite</em></h1><div class="rule"></div>
<p class="proj">Salon principal · Chambre d'amis<br>Séjour de l'étage · Chambre principale</p></div>
<div class="cover-foot">11 plans · environ 56 s + logo</div></div></div></section>""")

tot = "".join(f'<div class="toc-row"><span class="tn">{n}</span><span class="tt">{html.escape(t)}</span><span class="dur">{d}</span></div>'
              for n, _, t, _, d, *_ in SHOTS)
pages.append(f"""<section class="page"><div class="sb-intro">
<div><div class="kicker">Principe</div><h2>Une visite <em>comme si l'on y marchait</em></h2>
<p>La caméra suit le parcours d'un visiteur : elle entre dans le salon principal, passe dans la salle à manger, rejoint la chambre d'amis,
puis monte à l'étage pour le séjour et la chambre principale. Les plans s'enchaînent dans le mouvement, sans arrêt de la caméra,
pour un rendu fluide et continu.</p>
<div class="rules"><div><b>Hauteur</b>1,20 à 1,60 m, comme un regard humain</div><div><b>Objectif</b>20 à 24 mm, 35 mm pour les détails</div>
<div><b>Vitesse</b>0,15 à 0,35 m/s, accélération et freinage progressifs</div><div><b>Horizon</b>toujours droit, verticales verticales</div>
<div><b>Lumière</b>ambiance du soir des rendus, gorges LED allumées</div><div><b>Rythme</b>4 à 7 s par plan, environ 1 minute</div></div></div>
<div><div class="kicker">Séquencier</div><div class="toc-list">{tot}</div></div>
</div>{fol("Principe", 2)}</section>""")

for lab, im, w, h, pth in [("Rez-de-chaussée", "plan-rdc-amenagement.jpg", 879, 694, PATH_RDC),
                            ("Étage 1", "plan-etage1-amenagement.jpg", 927, 640, PATH_ET1)]:
    pages.append(f"""<section class="page"><div class="sb-plan1"><div class="sbp-head"><div class="kicker">Parcours caméra</div>
<h2>{lab}</h2><p class="sb-note">Trajets indicatifs, à caler dans le logiciel de rendu sur le modèle 3D.
Les numéros renvoient aux plans du séquencier.</p></div><div class="sbp">{plan_svg(im, w, h, pth)}</div></div>
{fol("Parcours", len(pages) + 1)}</section>""")

for i in range(0, len(SHOTS), 2):
    cells = ""
    for n, room, title, imgn, dur, move, cam, tr in SHOTS[i:i + 2]:
        cells += f"""<div class="shot"><figure class="tile sh-ref"><div class="ph" style="background-image:url(img/{imgn}.jpg)"></div>
<figcaption>Image de référence</figcaption></figure><div class="sh-txt"><div class="sh-n">{n:02d}</div><div class="kicker">{room} · {dur}</div>
<h3>{title}</h3><p>{move}</p><div class="cam">{cam}</div><div class="tr">Transition — {tr}</div></div></div>"""
    pages.append(f'<section class="page"><div class="shots">{cells}</div>{fol("Plans", len(pages) + 1)}</section>')

pages.append(f"""<section class="page"><div class="sb-intro">
<div><div class="kicker">Export</div><h2>Réglages <em>de rendu</em></h2>
<div class="rules one"><div><b>Format Reels / TikTok</b>vertical 9:16 · 2160 × 3840 px (ou 1080 × 1920)</div>
<div><b>Format site / YouTube</b>horizontal 16:9 · 3840 × 2160 px</div><div><b>Cadence</b>30 images/s · flou de mouvement activé</div>
<div><b>Vertical 9:16</b>garder le sujet au centre ; préférer avancées et montées aux travellings latéraux larges</div>
<div><b>Logiciel</b>mode vidéo de D5 Render, Lumion ou Enscape (images clés de caméra), ou Blender (caméra sur courbe)</div>
<div><b>Écrans TV</b>éteints ou image neutre dans la scène avant le rendu</div></div></div>
<div><div class="kicker">Montage</div><h2>Rythme <em>et habillage</em></h2>
<div class="rules one"><div><b>Intro</b>fondu du noir sur le plan 01, titre « KAÏRA Interior Design »</div>
<div><b>Titres de pièces</b>discrets, en bas du cadre, 1,5 s</div><div><b>Musique</b>piano ou ambient lent, libre de droits, coupes calées sur les temps</div>
<div><b>Étalonnage</b>tons chauds, noirs légèrement relevés, pas de saturation excessive</div>
<div><b>Fin</b>plan 11 puis logo KAÏRA sur fond sombre, 3 s</div></div></div>
</div>{fol("Export", len(pages) + 1)}</section>""")

css = (ROOT / "tools/book.css").read_text() + """
.dur { margin-left: auto; font-size: 8pt; color: var(--soft); letter-spacing: 1px; }
.sb-intro { padding: 16mm 14mm 18mm; display: grid; grid-template-columns: 1fr 1fr; gap: 14mm; height: 100%; }
.sb-intro h2 { font-size: 26pt; }
.rules { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm 6mm; margin-top: 5mm; }
.rules.one { grid-template-columns: 1fr; gap: 2.4mm; }
.rules div { font-size: 8.8pt; border-top: .2mm solid var(--line); padding-top: 1.6mm; }
.rules b { display: block; font-family: "Cormorant"; font-weight: 500; font-size: 12pt; }
.sb-plan1 { padding: 14mm 14mm 16mm; display: grid; grid-template-columns: 62mm 1fr; gap: 10mm; height: 100%; }
.sbp { background: var(--paper2); padding: 5mm; display: flex; align-items: center; justify-content: center; }
.sbp svg { width: 100%; height: 100%; }
.sb-note { font-size: 8pt; color: var(--soft); }
.shots { padding: 12mm 14mm 16mm; display: grid; grid-template-columns: 1fr 1fr; gap: 8mm; height: 100%; }
.shot { display: grid; grid-template-rows: 100mm 1fr; }
.sh-ref { height: 100mm; } .sh-txt { padding-top: 4mm; }
.sh-n { font-family: "Cormorant"; font-size: 26pt; color: var(--line); line-height: 1; float: right; }
.sh-txt h3 { font-size: 18pt; margin-bottom: 2mm; } .sh-txt p { font-size: 9pt; color: #4a413a; margin-bottom: 2mm; }
.cam { font-size: 8pt; color: var(--ink); border-top: .2mm solid var(--line); padding-top: 1.5mm; }
.tr { font-size: 7.4pt; letter-spacing: 1.4px; text-transform: uppercase; color: var(--accent); margin-top: 1.5mm; }
"""
(B / "storyboard.html").write_text(f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>KAÏRA — Storyboard</title>'
                                   f'<style>{css}</style></head><body>{"".join(pages)}</body></html>', encoding="utf-8")
print("pages:", len(pages))
