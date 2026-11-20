"""KAÏRA — Storyboard vertical 9:16 de la visite + guide de réalisation dans Blender (PDF A4 paysage).
Les plans et durées sont identiques à ceux de blender/kaira_visite_9x16.py."""
import html, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / "build"
IMG = B / "img"

def ref(rel):
    """Image de référence (version TV éteinte si elle existe), en JPEG dans build/img."""
    src = B / "tvoff" / pathlib.Path(rel).name
    src = src if src.exists() else ROOT / "sources" / rel
    out = IMG / (src.stem + ".jpg")
    if not out.exists():
        Image.open(src).convert("RGB").save(out, quality=90)
    return "img/" + out.name

R, A, P, E = "01-rdc-salon-principal/rdc-salon-%02d.png", "02-chambre-amis/chambre-amis-%02d.png", \
    "03-chambre-principale/chambre-principale-%02d.png", "04-etage1-sejour/etage1-sejour-%02d.png"

# n, espace, titre, image, position du cadrage 9:16 (%), secondes, focale, hauteur, mouvement, transition
SHOTS = [
 (1, "Salon principal", "Ouverture — le seuil", R % 10, 72, 4, 20, "1,60 m",
  "Avancée lente (dolly avant) vers la double porte en bois foncé, puis vers le salon.", "Fondu du noir → fondu enchaîné"),
 (2, "Salon principal", "Révélation du salon", R % 2, 62, 6, 20, "1,40 m",
  "Avancée douce avec panoramique lent vers la droite : les canapés, puis l'œuvre graphique entre les rideaux.", "Coupe dans le mouvement"),
 (3, "Salon principal", "Le mur TV", R % 3, 42, 5, 22, "1,30 m",
  "Arc d'environ 20° autour de la table basse, face au mur TV rétroéclairé et à la baie.", "Fondu enchaîné"),
 (4, "Salle à manger", "Sous la ligne de lumière", R % 5, 45, 5, 20, "1,50 → 1,65 m",
  "Avancée vers la table en pierre avec une légère montée : la suspension lumineuse entre en haut du cadre.", "Coupe dans le mouvement"),
 (5, "Salle à manger", "Détail — bibliothèque et marbre", R % 1, 34, 4, 35, "0,90 → 1,90 m",
  "Élévation verticale lente le long de la colonne en marbre veiné et de la bibliothèque. Faible profondeur de champ (f/2,8).", "Fondu enchaîné"),
 (6, "Chambre d'amis", "Entrée dans la chambre", A % 3, 50, 5, 18, "1,60 m",
  "Avancée à travers la porte, révélation du lit plateforme et des suspensions globe.", "Coupe dans le mouvement"),
 (7, "Chambre d'amis", "Le mur de marbre", A % 2, 58, 4, 22, "1,30 m",
  "Inclinaison lente vers le haut, du meuble suspendu au marbre blanc veiné.", "Fondu enchaîné"),
 (8, "Séjour — étage 1", "Arrivée à l'étage", E % 8, 45, 6, 20, "1,60 m",
  "Avancée depuis la double porte en bois vitrée, panoramique vers la bibliothèque éclairée et l'œuvre rouge.", "Coupe dans le mouvement"),
 (9, "Séjour — étage 1", "Bois et lumière", E % 5, 30, 4, 24, "1,20 → 1,50 m",
  "Court travelling latéral avec élévation devant l'étagère verticale éclairée et le mur TV.", "Fondu enchaîné"),
 (10, "Chambre principale", "Vers la suite", P % 4, 78, 6, 18, "1,60 m",
  "Avancée dans le couloir lumineux, virage doux vers la chambre et le dressing en bois.", "Fondu enchaîné"),
 (11, "Chambre principale", "Finale — l'écrin", P % 5, 50, 6, 22, "1,20 → 1,70 m",
  "Recul lent et montée face à la tête de lit et à la bande de marbre rétroéclairée ; la gorge lumineuse apparaît en haut du cadre.",
  "Fondu au noir → logo KAÏRA (3 s)"),
]
TOTAL = sum(s[5] for s in SHOTS) + 3

pages = []
def fol(sec):
    return (f'<div class="folio" style="left:14mm;right:14mm"><span>KAÏRA Interior Design · Visite vidéo 9:16</span>'
            f'<span>{sec}</span><span class="pn">{len(pages) + 1:02d}</span></div>')

def frame(src, x, cls="v916"):
    return f'<div class="{cls}" style="background-image:url({ref(src)});background-position:{x}% 50%"></div>'

# couverture
pages.append(f"""<section class="page"><div class="cv">
<div class="cv-frames">{frame(P % 5, 50)}{frame(R % 2, 62)}{frame(E % 8, 45)}</div>
<div class="cv-panel"><div class="wordmark">KAÏRA</div><div class="sub">INTERIOR DESIGN</div>
<div class="cover-title"><div class="kicker">Visite vidéo · TikTok & Instagram Reels</div><h1>Cinematic<br><em>walkthrough</em></h1>
<div class="rule"></div><p class="proj">Storyboard vertical 9:16 et guide de réalisation dans Blender</p></div>
<div class="cover-foot">11 plans · {TOTAL} s · 1080 × 1920 · 30 i/s</div></div></div></section>""")

# vue d'ensemble : frise des 11 plans
strip = "".join(f'<div class="fr"><div class="frn">{n:02d}</div>{frame(im, x, "v916 sm")}<div class="frt">{html.escape(t)}</div>'
                f'<div class="frd">{sec} s</div></div>' for n, _, t, im, x, sec, *_ in SHOTS)
pages.append(f"""<section class="page"><div class="ov"><div class="ov-head"><div class="kicker">Vue d'ensemble</div>
<h2>Le film <em>en 11 plans</em></h2><p class="note">Salon principal → salle à manger → chambre d'amis → séjour de l'étage → chambre principale.
Chaque vignette montre le cadrage vertical visé, d'après tes rendus.</p></div><div class="frise">{strip}</div>
<div class="tl">{''.join(f'<div style="flex:{s[5]}" class="tl{i % 2}">{s[0]:02d}</div>' for i, s in enumerate(SHOTS))}<div style="flex:3" class="tll">logo</div></div>
<div class="tlx"><span>0 s</span><span>{TOTAL} s</span></div></div>{fol("Vue d'ensemble")}</section>""")

# plans : 3 par page
for k in range(0, len(SHOTS), 2):
    cells = ""
    for n, room, t, im, x, sec, foc, h, mv, tr in SHOTS[k:k + 2]:
        cells += f"""<div class="sh9">{frame(im, x)}<div class="sh9t"><div class="sh-n">{n:02d}</div><div class="kicker">{room}</div>
<h3>{html.escape(t)}</h3><p>{mv}</p><dl><dt>Durée</dt><dd>{sec} s</dd><dt>Focale</dt><dd>{foc} mm</dd><dt>Hauteur</dt><dd>{h}</dd>
<dt>Transition</dt><dd>{tr}</dd></dl></div></div>"""
    pages.append(f'<section class="page"><div class="shots9">{cells}</div>{fol("Storyboard")}</section>')

# règles caméra
pages.append(f"""<section class="page"><div class="sb-intro">
<div><div class="kicker">Le langage caméra</div><h2>Fluide, lent, <em>réaliste</em></h2>
<div class="rules one"><div><b>Regard humain</b>caméra entre 1,20 et 1,70 m, comme un visiteur</div>
<div><b>Verticales droites</b>rotation X = 90°, Y = 0° : les murs restent parfaitement verticaux. Pour cadrer plus haut ou plus bas, utilise le décalage (Shift Y) plutôt que d'incliner.</div>
<div><b>Vitesse</b>0,15 à 0,35 m/s. Distance entre repères = vitesse × durée (ex. 0,3 m/s × 5 s = 1,5 m)</div>
<div><b>Accélération</b>chaque plan démarre et freine en douceur (géré par le script)</div>
<div><b>Pas de tremblement</b>aucun effet caméra à l'épaule : le luxe, c'est la stabilité</div></div></div>
<div><div class="kicker">Spécial vertical 9:16</div><h2>Penser <em>en hauteur</em></h2>
<div class="rules one"><div><b>Mouvements à privilégier</b>avancées, élévations, inclinaisons ; travellings latéraux courts</div>
<div><b>Focales</b>18 à 24 mm pour les vues d'ensemble, 35 mm pour les détails</div>
<div><b>Sujet au centre</b>l'élément fort (œuvre, marbre, lit) reste dans le tiers central</div>
<div><b>Zones réservées</b>rien d'important dans les 12 % du haut et les 25 % du bas : l'interface TikTok et Reels s'y affiche</div>
<div><b>Plafonds</b>les gorges lumineuses donnent la profondeur : garde un peu de plafond dans le cadre</div></div></div>
</div>{fol("Caméra")}</section>""")

# guide Blender
STEPS = [
 ("0", "Préparer le fichier", [
   "Fais une copie de ton fichier .blend : le script n'altère pas ta scène, mais on travaille toujours sur une copie.",
   "Les 4 espaces doivent être dans le même fichier. S'ils sont dans des fichiers séparés, utilise Fichier › Append, ou lance le script dans chaque fichier avec le même DOSSIER de sortie.",
   "Éteins les écrans TV : mets le matériau de l'écran en noir brillant, sans émission.",
   "Garde l'éclairage du soir de tes rendus, avec les gorges LED allumées."]),
 ("1", "Créer les repères", [
   "Onglet Scripting › Ouvrir › kaira_visite_9x16.py.",
   "Laisse ETAPE = \"1_PREPARER\" et clique sur Exécuter (▶). 22 caméras apparaissent : S01_debut, S01_fin, S02_debut…",
   "Le format passe en 1080 × 1920 : en vue caméra, tu vois déjà le cadre vertical."]),
 ("2", "Placer chaque repère", [
   "Dans l'Outliner, sélectionne S01_debut, puis fais Ctrl + Pavé 0 pour en faire la caméra active et regarder à travers.",
   "Panneau N › Vue › coche « Verrouiller la caméra sur la vue ». Navigue avec la souris jusqu'au cadrage de la vignette 01, puis décoche.",
   "Panneau N › Élément : règle la hauteur (Position Z), et Rotation X = 90°, Y = 0° pour garder les verticales droites.",
   "Fais de même pour S01_fin à la position d'arrivée, puis pour chacun des 11 plans. La focale de chaque repère est déjà réglée."]),
 ("3", "Animer", [
   "Mets ETAPE = \"2_ANIMER\", puis Exécuter : les caméras CAM_01 à CAM_11 sont animées avec des départs et des arrêts doux.",
   "Prévisualise : Pavé 0, ombrage Aperçu matériau, Espace pour lire. Les marqueurs de la timeline changent de caméra à chaque plan.",
   "Un plan ne te plaît pas ? Déplace ses repères et relance 2_ANIMER : l'animation est recréée."]),
 ("4", "Rendre les plans", [
   "Fais d'abord un test : PLANS_A_RENDRE = [1] et ECHANTILLONS = 64, puis ETAPE = \"3_RENDRE\".",
   "Rendu final : PLANS_A_RENDRE = [] et ECHANTILLONS = 256. Le script règle Cycles sur ta carte graphique avec débruitage et flou de mouvement.",
   "Compte environ 1 900 images. À 20–60 s par image, cela fait 10 à 30 h : rends plan par plan, la nuit. Le rendu reprend là où il s'est arrêté.",
   "Astuce : lance le rendu en ligne de commande, sans interface : blender -b copie.blend --python kaira_visite_9x16.py"]),
 ("5", "Monter et exporter", [
   "Renseigne MUSIQUE (fichier libre de droits), et LOGO_IMAGE (ton logo PNG) et POLICE si tu les as.",
   "Mets ETAPE = \"4_MONTER\", puis Exécuter : la scène « KAIRA_Montage » contient les plans, les fondus, les titres des pièces et le logo de fin.",
   "Rendu › Rendre l'animation (Ctrl + F12) : la vidéo KAIRA_visite_9x16.mp4 (H.264, 1080 × 1920, 30 i/s) est créée dans KAIRA_visite/."]),
 ("6", "Publier", [
   "Importe le MP4 tel quel sur TikTok et Instagram, sans recadrer.",
   "Choisis la vignette de couverture dans le plan 11 ou le plan 2.",
   "Si tu préfères monter dans CapCut ou Premiere, importe directement les dossiers S01 à S11 : ce sont des séquences d'images PNG."]),
]
for k in range(0, len(STEPS), 4):
    cols = ""
    for n, t, items in STEPS[k:k + 4]:
        li = "".join(f"<li>{html.escape(i)}</li>" for i in items)
        cols += f'<div class="step"><div class="stn">{n}</div><h3>{t}</h3><ul>{li}</ul></div>'
    head = ('<div class="kicker">Réalisation dans Blender</div><h2>Étape <em>par étape</em></h2>' if k == 0 else
            '<div class="kicker">Réalisation dans Blender</div><h2>Rendu <em>et publication</em></h2>')
    pages.append(f'<section class="page"><div class="guide"><div class="g-h">{head}</div><div class="steps n{len(STEPS[k:k+4])}">{cols}</div></div>{fol("Guide Blender")}</section>')

css = (ROOT / "tools/book.css").read_text() + """
.v916 { aspect-ratio: 9 / 16; background-size: cover; background-repeat: no-repeat; }
.cv { display: grid; grid-template-columns: 170mm 1fr; height: 100%; }
.cv-frames { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; padding: 14mm 0 14mm 14mm; align-items: center; }
.cv-frames .v916 { width: 100%; }
.cv-panel { padding: 18mm 15mm 14mm; display: flex; flex-direction: column; justify-content: space-between; }
.ov { padding: 13mm 14mm 16mm; height: 100%; display: flex; flex-direction: column; }
.ov-head h2 { margin-bottom: 2mm; }
.frise { display: grid; grid-template-columns: repeat(11, 1fr); gap: 2.2mm; margin-top: 6mm; }
.fr .v916 { width: 100%; } .frn { font-family: "Cormorant"; font-size: 13pt; color: var(--accent); }
.frt { font-family: "Cormorant"; font-size: 9.5pt; line-height: 1.1; margin-top: 1.5mm; } .frd { font-size: 6.8pt; color: var(--soft); letter-spacing: 1px; }
.tl { display: flex; height: 7mm; margin-top: auto; font-size: 6.6pt; color: #fff; }
.tl > div { display: flex; align-items: center; justify-content: center; border-right: .4mm solid var(--paper); }
.tl0 { background: #8C7462; } .tl1 { background: #6E5A4C; } .tll { background: #2B2622; }
.tlx { display: flex; justify-content: space-between; font-size: 6.6pt; color: var(--soft); margin: 1mm 0 5mm; }
.shots9 { padding: 13mm 14mm 16mm; display: grid; grid-template-columns: repeat(2, 1fr); gap: 10mm; height: 100%; }
.sh9 { display: grid; grid-template-columns: 88mm 1fr; gap: 6mm; align-items: start; }
.sh9 .v916 { width: 88mm; } .sh9t { padding-top: 4mm; } .sh9t h3 { font-size: 18pt; } .sh9t p { font-size: 9pt; color: #4a413a; }
.sh-n { font-family: "Cormorant"; font-size: 24pt; color: var(--line); line-height: 1; }
dl { display: grid; grid-template-columns: 17mm 1fr; gap: 1mm 2mm; font-size: 7.6pt; border-top: .2mm solid var(--line); padding-top: 2mm; }
dt { letter-spacing: 1.4px; text-transform: uppercase; color: var(--accent); font-size: 6.4pt; padding-top: .4mm; }
.sb-intro { padding: 16mm 14mm 18mm; display: grid; grid-template-columns: 1fr 1fr; gap: 14mm; height: 100%; }
.sb-intro h2 { font-size: 26pt; }
.rules.one { display: grid; gap: 2.4mm; margin-top: 5mm; }
.rules div { font-size: 8.8pt; border-top: .2mm solid var(--line); padding-top: 1.6mm; }
.rules b { display: block; font-family: "Cormorant"; font-weight: 500; font-size: 12pt; }
.guide { padding: 13mm 14mm 16mm; height: 100%; display: flex; flex-direction: column; }
.guide h2 { font-size: 26pt; margin-bottom: 5mm; }
.steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7mm; } .steps.n3 { grid-template-columns: repeat(3, 1fr); }
.stn { font-family: "Cormorant"; font-size: 40pt; color: var(--line); line-height: 1; }
.step h3 { font-size: 16pt; } .step li { font-size: 8.2pt; line-height: 1.45; padding: 1.6mm 0; }
"""
(B / "storyboard_9x16.html").write_text(f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>KAÏRA — Visite 9:16</title>'
                                        f'<style>{css}</style></head><body>{"".join(pages)}</body></html>', encoding="utf-8")
print("pages:", len(pages), "durée:", TOTAL)
