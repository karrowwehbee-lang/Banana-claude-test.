"""KAÏRA — Dossier technique d'architecture intérieure (A3 paysage).

Usage: python3 tools/build.py   ->  build/dossier-technique.html  +  ../../livrables/KAIRA-Dossier-technique-Villa-A3.pdf
"""
import html
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import data as D
import views as V
from draw import PATTERNS, OLIVE, BURG, INK, fmt

ROOT = HERE.parent
REPO = ROOT.parent.parent
BUILD = ROOT / "build"
SRC = REPO / "projects/dossier-client/sources"
FONTS = REPO / "projects/dossier-client/build/fonts"
LOGO = REPO / "projects/kaira-logo/logo/svg/kaira-4-horizontal-chocolate.svg"
OUT_PDF = BUILD / "KAIRA-Dossier-technique-Villa-A3.pdf"   # full PDF (118 MB) — volumes go to livrables/

PROJECT = "Villa — Rez-de-chaussée & Étage 1"
DOC = "Dossier technique d'architecture intérieure"
DATE = "11.11.2026"
INDICE = "A"

# drawing area (mm)
AX, AY, AW, AH = 12, 12, 328, 272

RENDERS = {
    "sejour": [
        ("rdc-salon-02", "Salon — vue générale (vers l'ouest)", "E"),
        ("rdc-salon-07", "Mur A — mur TV et porte vitrée (vue de face)", "A"),
        ("rdc-salon-03", "Mur A — mur TV et porte vitrée (vue de 3/4)", "A"),
        ("rdc-salon-04", "Mur A — mur TV, tables basses (vue de 3/4)", "A"),
        ("rdc-salon-11", "Mur E — mur tableau (vue de face)", "E"),
        ("rdc-salon-08", "Mur D — colonnes chêne et porte d'entrée (vue de face)", "D"),
        ("rdc-salon-10", "Mur D — porte d'entrée, fenêtre F3, plafond à deux caissons", "D"),
        ("rdc-salon-05", "Salle à manger — vue générale (vers l'est)", "C"),
        ("rdc-salon-09", "Mur D — bibliothèque M3, fenêtre F4, œuvre rouge", "D"),
        ("rdc-salon-01", "Salle à manger — bibliothèque, colonne marbre et console (vers le sud-est)", "C"),
        ("rdc-salon-06", "Mur B — mur d'art et passage vers le dégagement", "B"),
    ],
    "amis": [
        ("chambre-amis-01", "Mur A — tête de lit (vue de face)", "A"),
        ("chambre-amis-02", "Mur C — TV, habillage marbre et coiffeuse (vue de face)", "C"),
        ("chambre-amis-03", "Lit plateforme et fenêtre F5 (vue de 3/4)", "B"),
        ("chambre-amis-04", "Mur C — TV et coiffeuse (vue de 3/4)", "C"),
    ],
    "etsejour": [
        ("etage1-sejour-02", "Salon — vers les baies du mur sud", "C"),
        ("etage1-sejour-01", "Mur A — mur TV (vue de face)", "A"),
        ("etage1-sejour-05", "Mur A — mur TV (vue de 3/4)", "A"),
        ("etage1-sejour-08", "Mur B — mur d'entrée (vue de face)", "B"),
        ("etage1-sejour-06", "Mur B — mur d'entrée (vue de 3/4)", "B"),
        ("etage1-sejour-09", "Mur B — depuis le canapé (vue de 3/4)", "B"),
        ("etage1-sejour-03", "Salon — vers le sud-ouest (vue de 3/4)", "D"),
        ("etage1-sejour-04", "Œuvre et bibliothèque M10 (vue de 3/4)", "B"),
    ],
    "princ": [
        ("chambre-principale-05", "Mur A — tête de lit (vue de face)", "A"),
        ("chambre-principale-01", "Mur A — tête de lit (vue de 3/4)", "A"),
        ("chambre-principale-02", "Mur A — variante de cadrage", "A"),
        ("chambre-principale-03", "Vue large avec la baie vitrée du mur C", "C"),
        ("chambre-principale-04", "Mur B — dressing M12 et meuble TV M13", "B"),
    ],
}
FOLDER = {"sejour": "01-rdc-salon-principal", "amis": "02-chambre-amis", "etsejour": "04-etage1-sejour",
          "princ": "03-chambre-principale"}

SHEETS = []


def sheet(num, title, level, room, scale, body, toc=True):
    SHEETS.append(dict(num=num, title=title, level=level, room=room, scale=scale, body=body, toc=toc))


# ---------------------------------------------------------------- html helpers
def place(svg, x, y):
    return f'<div class="v" style="left:{x:.1f}mm;top:{y:.1f}mm">{svg}</div>'


def vtitle(x, y, w, letter, title, scale):
    return (f'<div class="vt" style="left:{x:.1f}mm;top:{y:.1f}mm;width:{w:.1f}mm"><span class="vn">{letter}</span>'
            f'<span class="vtt">{html.escape(title)}</span><span class="vs">{scale}</span></div>')


def textbox(x, y, w, inner, cls="tx"):
    return f'<div class="{cls}" style="left:{x:.1f}mm;top:{y:.1f}mm;width:{w:.1f}mm">{inner}</div>'


def view_block(svg, w, h, x, y, letter, title, scale):
    return place(svg, x, y) + vtitle(x + 4, y + h - 3, max(70, w - 8), letter, title, scale)


def notes_html(items, title="Notes"):
    li = "".join(f"<li>{html.escape(n)}</li>" for n in items)
    return f'<div class="nh">{title}</div><ul class="nl">{li}</ul>'


def img_uri(room, name):
    return (SRC / FOLDER[room] / f"{name}.png").as_uri()


# ---------------------------------------------------------------- cover, contents, conventions
def build_front():
    logo = LOGO.read_text()
    body = f"""
<div class="cover-img"><img src="{img_uri('sejour', 'rdc-salon-07')}"></div>
<div class="cover-txt">
  <div class="cv-logo">{logo}</div>
  <div class="cv-k">{DOC}</div>
  <h1>{PROJECT}</h1>
  <div class="cv-list">Plans cotés · Élévations intérieures · Coupes · Mobilier sur mesure · Matériaux et finitions · Rendus 3D</div>
  <div class="cv-meta"><b>Indice {INDICE}</b> — {DATE}<br>Format A3 paysage · Cotes en centimètres</div>
  <div class="cv-warn">Document établi à partir des plans et des rendus 3D du projet. Chaque cote est classée :
  <span class="st-v">vérifiée</span>, <span class="st-d">≈ déduite</span> ou <span class="st-c">à confirmer</span>
  (planche 002). Aucune cote n'a été inventée.</div>
</div>"""
    sheet("000", "Page de garde", "—", "—", "—", body)
    sheet("001", "Sommaire", "—", "—", "—", "__TOC__")
    conv = f"""
<div class="conv">
 <div class="col">
  <h2>Statut des cotes</h2>
  <table class="lg">
   <tr><td class="st-v big">424</td><td><b>Cote vérifiée</b> — écrite sur le plan coté source du rez-de-chaussée
     (plan-rdc-cote-2D). Reportée telle quelle.</td></tr>
   <tr><td class="st-d big"><i>≈ 59</i></td><td><b>Cote déduite</b> — relevée à l'échelle sur un plan, ou mesurée sur un rendu
     3D de face calibré sur une cote connue. Arrondie au centimètre. Tolérance indicative ±3 cm (murs, ouvertures) et ±5 cm
     (mobilier, hauteurs à l'étage). À vérifier sur site.</td></tr>
   <tr><td class="st-c big">À CONF.</td><td><b>Cote à confirmer</b> — impossible à déterminer avec précision à partir des
     documents du projet. Dessinée en tiretés bordeaux, sans valeur.</td></tr>
  </table>
  <h2>Méthode de relevé</h2>
  <ul class="nl">
   <li><b>Rez-de-chaussée :</b> plan coté source au 1,080 cm/px, contrôlé sur ses 16 cotes écrites (écart ≤ 1 cm).
     Murs et ouvertures non cotés : relevés à l'échelle (≈).</li>
   <li><b>Mobilier en plan :</b> vues de dessus de la maquette 3D. La grille du logiciel mesure 100,0 cm
     une fois recalée sur le plan coté : elle sert d'échelle (RDC 1,507 cm/px, étage 1,805 cm/px).</li>
   <li><b>Étage 1 :</b> aucun plan coté disponible. Toutes les cotes viennent de la vue de dessus (grille 1 m) :
     elles sont toutes « déduites ». Contrôle : trémie d'escalier ≈ 374 × 244 contre 383 × 234 au RDC.</li>
   <li><b>Hauteurs et élévations :</b> rendus 3D de face (perspective à un point, horizon au centre de l'image).
     Le plan du mur est calibré sur une largeur connue. Contrôles : les téléviseurs 75" mesurent 167 × 93 dans
     les trois pièces (dimension réelle 166 × 93) ; hauteur du séjour RDC concordante sur 4 rendus (282 à 286).</li>
   <li><b>Rendus 3D :</b> fichiers originaux du projet, insérés sans recadrage, retouche ni recompression.</li>
  </ul>
 </div>
 <div class="col">
  <h2>Hauteurs déduites</h2>
  <table class="tb2">
   <tr><th>Pièce</th><th>Sol → sous faux-plafond</th><th>Rendus de calibrage</th></tr>
   <tr><td>Séjour RDC</td><td class="st-d">≈ 284</td><td>07, 08, 09, 10</td></tr>
   <tr><td>Chambre d'amis</td><td class="st-d">≈ 285</td><td>01, 02</td></tr>
   <tr><td>Séjour étage 1</td><td class="st-d">≈ 289</td><td>01, 08</td></tr>
   <tr><td>Chambre principale</td><td class="st-d">≈ 292 (±5)</td><td>05</td></tr>
   <tr><td colspan="3" class="st-c">Plafonds centraux (au-dessus des gorges lumineuses), épaisseurs de dalles et
     niveau du plancher de l'étage : à confirmer.</td></tr>
  </table>
  <h2>Graphisme</h2>
  <table class="lg2">
   <tr><td><span class="sw poche"></span></td><td>Mur coupé</td><td><span class="sw hors"></span></td><td>Hors périmètre</td></tr>
   <tr><td><span class="ln led"></span></td><td>Éclairage LED / rétroéclairage</td><td><span class="ln jt"></span></td><td>Joint, calepinage</td></tr>
   <tr><td><span class="ln cf"></span></td><td>Élément à confirmer</td><td><span class="bb">M1</span></td><td>Mobilier sur mesure</td></tr>
   <tr><td><span class="wm">A</span></td><td>Repère d'élévation (mur vu)</td><td><span class="sm">A</span></td><td>Trait de coupe</td></tr>
  </table>
  <h2>Documents sources</h2>
  <ul class="nl">
   <li>plan-rdc-cote-2D — plan d'architecture coté du rez-de-chaussée</li>
   <li>plan-rdc-amenagement, plan-etage1-amenagement — vues de dessus de la maquette 3D</li>
   <li>28 rendus 3D : séjour RDC (11), chambre d'amis (4), chambre principale (5), séjour étage 1 (8)</li>
  </ul>
  <p class="small">Plan source et maquette 3D diffèrent sur un point : le placard « 130 » de la chambre d'amis
  n'existe pas dans la maquette (chevet à cet endroit). Il est dessiné en tiretés et noté à confirmer.</p>
 </div>
</div>"""
    sheet("002", "Conventions, méthode et fiabilité des cotes", "—", "—", "—", conv)


# ---------------------------------------------------------------- level plans
def build_levels():
    svg, w, h = V.plan_rdc_general(50, furniture=False)
    x, y = AX + (AW - w) / 2, AY + 2
    body = view_block(svg, w, h, x, y, "1", "Plan général coté — rez-de-chaussée", "1:50")
    body += textbox(AX + 2, AY + AH - 22, 150, notes_html([
        "Cotes noires : cotes écrites du plan source. Cotes ≈ olive : relevées à l'échelle.",
        "Épaisseur des murs ≈ 20 (relevé). Ouvertures F1 à F5 : largeurs relevées ; hauteurs en élévation.",
        "Niveau de référence ±0,00 = sol fini du rez-de-chaussée (convention de ce dossier)."]))
    sheet("100", "Plan général coté — rez-de-chaussée", "RDC", "Niveau", "1:50", body)

    svg, w, h = V.plan_rdc_general(50, furniture=True)
    body = view_block(svg, w, h, AX + (AW - w) / 2, AY + 2, "2", "Plan d'aménagement — rez-de-chaussée", "1:50")
    body += textbox(AX + 2, AY + AH - 22, 170, notes_html([
        "Mobilier positionné d'après la vue de dessus de la maquette 3D (positions ≈, ±5).",
        "M1 à M8 : mobilier sur mesure, voir planches de détail. Tapis en tiretés.",
        "Surfaces calculées sur les faces intérieures des murs (≈)."]))
    sheet("101", "Plan d'aménagement — rez-de-chaussée", "RDC", "Niveau", "1:50", body)

    for furn, num, t in ((False, "110", "Plan général — étage 1 (cotes déduites)"),
                         (True, "111", "Plan d'aménagement — étage 1")):
        svg, w, h = V.plan_et_general(75 if not furn else 75, furniture=furn)
        body = view_block(svg, w, h, AX + (AW - w) / 2, AY + 2, "3" if not furn else "4", t, "1:75")
        body += textbox(AX + 2, AY + AH - 26, 190, notes_html([
            "Aucun plan coté de l'étage n'a été fourni : toutes les cotes sont déduites de la vue de dessus (grille 1 m).",
            "Baies dessinées en tiretés bordeaux : positions déduites des rideaux de la maquette, dimensions à confirmer.",
            "Niveau du plancher de l'étage et hauteur d'étage : à confirmer.",
            "Le recalage vertical entre RDC et étage n'est pas établi : les deux plans ne sont pas superposés."]))
        sheet(num, t, "ÉTAGE 1", "Niveau", "1:75", body)


# ---------------------------------------------------------------- room chapters
ROOM_NUM = {"sejour": 200, "amis": 300, "etsejour": 400, "princ": 500}
CUSTOM_CROPS = {
    "sejour": [("A", (100, 400, 0, D.H_SEJ), ["M1", "M2"]), ("D1", (0, 190, 0, D.H_SEJ), ["M3"]),
               ("D2", (170, 541, 0, D.H_SEJ), ["M5"]), ("C", (60, 236.5, 0, D.H_SEJ), ["M4"])],
    "amis": [("C", (0, 293.8, 0, D.H_AMIS), ["M6", "M7"])],
    "etsejour": [("A", (40, 360, 0, D.H_ET_SEJ), ["M9a", "M9b"]), ("B", (350, 524.4, 0, D.H_ET_SEJ), ["M10"])],
    "princ": [("A", (0, 377.3, 0, D.H_PRINC), ["M11"]), ("B", (0, 254.6, 0, D.H_PRINC), ["M12"])],
}


def fit_scale(wall_w, H, max_w, max_h, prefs=(20, 25, 30, 40, 50), extra_w=48, extra_h=46):
    for sc in prefs:
        m = 10 / sc
        if wall_w * m + extra_w <= max_w and H * m + extra_h <= max_h:
            return sc
    return prefs[-1]


def build_room(key):
    R = D.ROOMS[key]
    base = ROOM_NUM[key]
    lvl = R["level"]
    name = R["short"]
    num = [base]

    def add(title, scale, body):
        sheet(f"{num[0]}", title, lvl, name, scale, body)
        num[0] += 1

    # --- plan
    svg, w, h = V.plan_room(key)
    sc = V.ROOM_VIEW[key]["scale"]
    x = AX + max(0, (AW - 68 - w) / 2) if w < AW - 70 else AX + max(0, (AW - w) / 2)
    body = view_block(svg, w, h, x, AY + 2, "1", f"Plan coté — {R['name']}", f"1:{sc}")
    area = V.poly_area(R["poly"])
    info = (f'<div class="nh">{html.escape(R["name"])}</div><table class="kv">'
            f'<tr><td>Niveau</td><td>{lvl}</td></tr>'
            f'<tr><td>Surface</td><td class="st-d">≈ {area:.1f} m²</td></tr>'.replace(".", ",", 1) +
            f'<tr><td>Hauteur sous faux-plafond</td><td class="st-d">≈ {R["height"]}</td></tr>'
            f'<tr><td>Plafond central</td><td class="st-c">à confirmer</td></tr>'
            f'<tr><td>Sol fini</td><td>{"±0,00 (réf.)" if lvl == "RDC" else "<span class=st-c>à confirmer</span>"}</td></tr>'
            f'</table><p class="small">Repères A, B, C… : murs dessinés en élévation. Traits mixtes : coupes. '
            f'M… : mobilier sur mesure.</p>')
    if w < AW - 70:
        body += textbox(AX + AW - 64, AY + 4, 62, info)
    else:
        body += textbox(AX + 2, AY + AH - 40, 96, info)
    add(f"Plan coté — {name}", f"1:{sc}", body)
    # --- elevations: frontal walls one per sheet at the largest scale, sparse walls paired
    E = D.ELEV[key]
    walls = list(E.keys())
    H = R["height"]
    i = 0
    while i < len(walls):
        k = walls[i]
        k2 = walls[i + 1] if i + 1 < len(walls) else None
        if E[k].get("sparse") and k2 and E[k2].get("sparse"):
            done = False
            for sc in (25, 30, 40, 50):
                svg, w, h = V.elev_view(key, k, scale=sc)
                svg2, w2, h2 = V.elev_view(key, k2, scale=sc)
                if w + w2 + 6 <= AW and max(h, h2) + 45 <= AH:
                    body = view_block(svg, w, h, AX, AY + 2, k, E[k]["title"], f"1:{sc}")
                    body += view_block(svg2, w2, h2, AX + w + 6, AY + 2, k2, E[k2]["title"], f"1:{sc}")
                    y0 = AY + max(h, h2) + 6
                    body += notes_block(key, [k, k2], AX + 2, y0, AW - 54)
                    body += kp_block(key, [k, k2], AX + AW - 50, y0 + 4)
                    done = True
                    break
                if max(w, w2) + 60 <= AW and h + h2 + 4 <= AH:
                    body = view_block(svg, w, h, AX, AY + 1, k, E[k]["title"], f"1:{sc}")
                    body += view_block(svg2, w2, h2, AX, AY + h + 3, k2, E[k2]["title"], f"1:{sc}")
                    xn = AX + max(w, w2) + 4
                    body += notes_block(key, [k, k2], xn, AY + 4, AW - max(w, w2) - 6, stack=True)
                    body += kp_block(key, [k, k2], AX + AW - 50, AY + AH - 34)
                    done = True
                    break
            if done:
                add(f"Élévations {k} et {k2} — {name}", f"1:{sc}", body)
                i += 2
                continue
        sc = fit_scale(E[k]["width"], H, AW, AH - 36)
        svg, w, h = V.elev_view(key, k, scale=sc)
        body = view_block(svg, w, h, AX + max(0, (AW - w) / 2), AY + 2, k, E[k]["title"], f"1:{sc}")
        y0 = AY + h + 6
        if y0 + 30 <= AY + AH:
            body += notes_block(key, [k], AX + 2, y0, AW - 54)
            body += kp_block(key, [k], AX + AW - 50, y0 + 4)
        else:
            body += notes_block(key, [k], AX + w + 4, AY + 4, AW - w - 6, stack=True)
        add(f"Élévation {k} — {name}", f"1:{sc}", body)
        i += 1
    # --- sections
    for sec in V.SECTIONS[key]:
        for sc in (25, 30, 40, 50):
            sec["scale"] = sc
            svg, w, h = V.section_view(key, sec)
            if w <= AW and h + 40 <= AH:
                break
        body = view_block(svg, w, h, AX + max(0, (AW - w) / 2), AY + 2, sec["name"][0], sec["title"],
                          f"1:{sec['scale']}")
        y0 = AY + h + 6
        notes = ["Coupe établie à partir des hauteurs déduites ; l'élévation vue au-delà est dessinée en gris.",
                 "Retombée périphérique de faux-plafond avec gorge lumineuse LED : "
                 + ("largeur ≈ 50 (géométrie du rendu 07)." if sec["soffit"][0] else "largeur à confirmer."),
                 "Plafond central, plancher haut et épaisseur de dalle : à confirmer.",
                 "Mobilier coupé : profils relevés (vue de dessus pour la profondeur, rendus pour les hauteurs)."]
        body += textbox(AX + 2, y0, AW - 4, notes_html(notes))
        add(sec["title"].split(" — ")[0] + f" — {name}", f"1:{sec['scale']}", body)
    # --- custom furniture (paginated)
    pages = furniture_pages(key)
    for j, (b, scl) in enumerate(pages):
        suffix = f" ({j + 1}/{len(pages)})" if len(pages) > 1 else ""
        add(f"Mobilier sur mesure — {name}{suffix}", scl, b)
    # --- materials
    add(f"Matériaux et finitions — {name}", "—", materials_body(key))
    # --- renders
    rs = RENDERS[key]
    add(f"Rendu 3D — {name}", "—", render_hero(key, rs[0]))
    rest = rs[1:]
    for j in range(0, len(rest), 2):
        add(f"Rendus 3D — {name} ({j // 2 + 1}/{(len(rest) + 1) // 2})", "—", render_pair(key, rest[j:j + 2]))


def notes_block(key, walls, x, y, w, stack=False):
    E = D.ELEV[key]
    parts = []
    for k in walls:
        e = E[k]
        items = [f"Source : {e['src']}. Calibrage : {e['calib']}."] + e["notes"]
        parts.append(notes_html(items, f"Mur {k} — notes"))
    cls = "stack" if stack else "cols"
    return textbox(x, y, w, f'<div class="{cls}">' + "".join(f"<div>{p}</div>" for p in parts) + "</div>")


def kp_block(key, walls, x, y):
    out = textbox(x, y - 4.5, 48, '<div class="kpt">Plan de repérage</div>')
    for j, k in enumerate(walls[:2]):
        svg, w, h = V.key_plan(key, k, size=(23, 23) if len(walls) > 1 else (46, 34))
        out += place(svg, x + j * 25, y)
    return out


def schedule_html(key):
    rows = ""
    for ref, label, dims, note in D.CUSTOM[key]:
        cells = []
        for k_, v, st in dims:
            if v is None or st == "c":
                cells.append(f'<span class="st-c">{k_} à conf.</span>')
            elif st == "d":
                cells.append(f'<span class="st-d">{k_} ≈ {int(round(v))}</span>')
            else:
                cells.append(f"{k_} {fmt(v)}")
        rows += (f'<tr><td class="ref">{ref}</td><td>{html.escape(label)}</td><td>{" · ".join(cells)}</td>'
                 f'<td>{html.escape(note)}</td></tr>')
    return (f'<div class="nh">Nomenclature du mobilier sur mesure</div><table class="tb2 full">'
            f'<tr><th>Réf.</th><th>Désignation</th><th>Dimensions (cm)</th><th>Observations</th></tr>{rows}</table>'
            f'<p class="small">L = longueur, P = profondeur, H = hauteur, pose = hauteur sous meuble. Dimensions ≈ relevées sur la '
            f'vue de dessus (L, P) et sur les rendus de face (H). Quincaillerie, épaisseurs de panneaux, structure et '
            f'détails d\'assemblage : à définir en plans d\'exécution.</p>')


def furniture_pages(key):
    """Shelf-pack the cropped elevations of the custom pieces; schedule table at the end."""
    crops = CUSTOM_CROPS.get(key, [])
    # one common scale if everything fits on a single sheet at 1:25 or 1:30
    common = None
    for sc in (25, 30):
        ws = [V.elev_view(key, wall, scale=sc, crop=crop, show_dims=True, show_levels=False)[1:] for wall, crop, _ in crops]
        if sum(w for w, _ in ws) + 5 * (len(ws) - 1) <= AW and max([h for _, h in ws] + [0]) + 30 + len(D.CUSTOM[key]) * 7 <= AH:
            common = sc
            break
    pages, body, scales = [], "", set()
    x, y, row_h = AX, AY + 2, 0
    for wall, crop, refs in crops:
        cw, chh = crop[1] - crop[0], crop[3] - crop[2]
        sc = common or fit_scale(cw, chh, AW, AH - 40, prefs=(25, 30), extra_w=40, extra_h=60)
        svg, w, h = V.elev_view(key, wall, scale=sc, crop=crop, show_dims=True, show_levels=False)
        if x + w > AX + AW + 0.5:
            x, y, row_h = AX, y + row_h + 4, 0
        if y + h > AY + AH:
            pages.append((body, " / ".join(f"1:{v}" for v in sorted(scales))))
            body, scales, x, y, row_h = "", set(), AX, AY + 2, 0
        body += view_block(svg, w, h, x, y, refs[0], f"{' + '.join(refs)} — vue de face (extrait mur {wall})", f"1:{sc}")
        scales.add(sc)
        x += w + 5
        row_h = max(row_h, h)
    ytab = y + row_h + 9
    n_rows = len(D.CUSTOM[key])
    need = 26 + n_rows * 7
    if body and ytab + need > AY + AH:
        pages.append((body, " / ".join(f"1:{v}" for v in sorted(scales))))
        body, scales, ytab = "", set(), AY + 2
    body += textbox(AX + 2, ytab, AW - 4, schedule_html(key))
    pages.append((body, " / ".join(f"1:{v}" for v in sorted(scales)) or "—"))
    return pages


def materials_body(key):
    rows = ""
    for mat, use, hexc in D.MATERIALS[key]:
        chip = f'<span class="chip" style="background:{hexc}"></span>' if hexc else '<span class="chip none">—</span>'
        rows += (f'<tr><td>{chip}</td><td><b>{html.escape(mat)}</b></td><td>{html.escape(use)}</td>'
                 f'<td>{hexc or "—"}</td><td class="st-c">à confirmer</td><td class="st-c">à confirmer</td></tr>')
    t = (f'<div class="nh">Matériaux et finitions — {html.escape(D.ROOMS[key]["name"])}</div>'
         f'<table class="tb2 full mat"><tr><th></th><th>Matériau</th><th>Localisation</th><th>Teinte relevée</th>'
         f'<th>Référence fabricant</th><th>Finition</th></tr>{rows}</table>')
    side = notes_html([
        "Matériaux identifiés sur les rendus 3D du projet ; aucune référence n'est inventée.",
        "Teinte relevée : médiane des pixels d'une zone du rendu. Indicative : elle dépend de l'éclairage de la scène.",
        "« — » : teinte non relevable sur le rendu (reflets, lumière, métal).",
        "À valider avant commande : échantillons physiques, références fabricants, finitions (mat, satiné, brossé, "
        "adouci…), sens du fil et calepinage des panneaux bois et marbre.",
        "Éclairage : température de couleur et intensité des LED à définir (non mesurables sur les rendus).",
    ], "Notes")
    return textbox(AX + 2, AY + 2, 226, t) + textbox(AX + 236, AY + 2, 90, side)


def render_hero(key, r):
    name, cap, wall = r
    kp, kw, kh = V.key_plan(key, wall, size=(56, 44))
    side = (f'<div class="nh">{html.escape(D.ROOMS[key]["name"])}</div><p class="cap">{html.escape(cap)}</p>'
            f'<p class="small">Fichier : {name}.png — rendu 3D original KAÏRA, inséré en entier, sans recadrage ni retouche.</p>'
            f'<div class="kpt">Repérage — mur {wall}</div>')
    return (f'<div class="rimg hero" style="left:{AX}mm;top:{AY}mm;height:{AH}mm;width:{AW - 72}mm">'
            f'<img src="{img_uri(key, name)}"></div>' + textbox(AX + AW - 68, AY + 4, 66, side) +
            place(kp, AX + AW - 66, AY + 62))


def render_pair(key, rs):
    out = ""
    wbox = (AW - 6) / 2
    hbox = wbox * 1816 / 1667
    top = AY + (AH - hbox - 14) / 2
    for j, (name, cap, wall) in enumerate(rs):
        x = AX + j * (wbox + 6)
        out += (f'<div class="rimg" style="left:{x:.1f}mm;top:{top:.1f}mm;height:{hbox:.1f}mm;width:{wbox:.1f}mm">'
                f'<img src="{img_uri(key, name)}"></div>'
                + textbox(x, top + hbox + 2.5, wbox, f'<p class="cap"><b>{name}</b> — {html.escape(cap)}</p>'))
    return out


def build_recap():
    rows = []
    gen = ["Niveau du plancher de l'étage 1, hauteur d'étage et épaisseurs de dalles.",
           "Hauteur des plafonds centraux au-dessus des gorges lumineuses (4 pièces).",
           "Largeur des retombées de faux-plafond (chambre d'amis, séjour et chambre de l'étage).",
           "Sens d'ouverture de toutes les portes.",
           "Étage 1 : vérification sur site de toutes les cotes déduites de la vue de dessus (aucun plan coté).",
           "Étage 1 : nombre, positions, largeurs, allèges et linteaux des baies.",
           "RDC : nature des segments 85,8 / 142 / 163 du mur d'escalier (plan source).",
           "Chambre d'amis : placard « 130 » du plan source absent de la maquette 3D."]
    for k, room in D.ELEV.items():
        for w, e in room.items():
            for n in e["notes"]:
                if "confirmer" in n:
                    rows.append((D.ROOMS[k]["short"], f"Mur {w}", n))
            for el in e["els"]:
                if el[0] == "note":
                    rows.append((D.ROOMS[k]["short"], f"Mur {w}", el[3]))
                if el[0] == "open" and el[3] is None:
                    rows.append((D.ROOMS[k]["short"], f"Mur {w}", f"{el[6]} : allège et linteau."))
    for k, items in D.CUSTOM.items():
        for ref, label, dims, note in items:
            miss = [d[0] for d in dims if d[1] is None or d[2] == "c"]
            if miss:
                rows.append((D.ROOMS[k]["short"], ref, f"{label} : {', '.join(miss)} à confirmer."))
    seen, uniq = set(), []
    for r in rows:
        if r not in seen:
            seen.add(r); uniq.append(r)
    half = (len(uniq) + 1) // 2
    def tbl(rs):
        return ('<table class="tb2 full"><tr><th>Pièce</th><th>Repère</th><th>Élément à confirmer</th></tr>' +
                "".join(f"<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td><td>{html.escape(c)}</td></tr>" for a, b, c in rs)
                + "</table>")
    body = textbox(AX + 2, AY + 2, AW - 4, notes_html(gen, "Points généraux à relever sur site"))
    body += textbox(AX + 2, AY + 62, AW / 2 - 4, tbl(uniq[:half]))
    body += textbox(AX + AW / 2 + 2, AY + 62, AW / 2 - 4, tbl(uniq[half:]))
    sheet("900", "Récapitulatif des cotes et éléments à confirmer", "—", "Synthèse", "—", body)


# ---------------------------------------------------------------- title block + document
def title_block(sh, page, total):
    logo = LOGO.read_text()
    lvl = sh["level"] if sh["level"] != "—" else "Général"
    room = sh["room"] if sh["room"] != "—" else "—"
    return f"""<div class="tb">
 <div class="tb-logo">{logo}</div>
 <div class="tb-firm">KAÏRA INTERIOR DESIGN<span>Architecture intérieure</span></div>
 <div class="tb-sec"><label>Projet</label><div>{PROJECT}</div></div>
 <div class="tb-sec"><label>Document</label><div>{DOC}</div></div>
 <div class="tb-sec"><label>Niveau · Pièce</label><div>{lvl} · {html.escape(room)}</div></div>
 <div class="tb-sec tb-title"><label>Titre de la planche</label><div>{html.escape(sh['title'])}</div></div>
 <div class="tb-grid">
  <div><label>Échelle</label>{sh['scale']}</div><div><label>Format</label>A3</div>
  <div><label>Date</label>{DATE}</div><div><label>Indice</label>{INDICE}</div>
 </div>
 <div class="tb-legend">
  <div><span class="st-v">424</span> cote vérifiée (plan source)</div>
  <div><span class="st-d"><i>≈ 59</i></span> cote déduite (relevé)</div>
  <div><span class="st-c">À CONF.</span> cote à confirmer</div>
 </div>
 <div class="tb-note">Cotes en cm. Ne pas mesurer sur le dessin. Toutes les cotes sont à vérifier sur site avant exécution.</div>
 <div class="tb-num"><label>N° de dessin</label><div>KAI-VIL-{sh['num']}</div></div>
 <div class="tb-page">Planche {page} / {total}</div>
</div>"""


CSS = """
@font-face{font-family:Jost;font-weight:300;src:url(FONTS/jost-latin-300-normal.woff2)}
@font-face{font-family:Jost;font-weight:400;src:url(FONTS/jost-latin-400-normal.woff2)}
@font-face{font-family:Jost;font-weight:500;src:url(FONTS/jost-latin-500-normal.woff2)}
@font-face{font-family:Cormorant;font-weight:400;src:url(FONTS/cormorant-garamond-latin-400-normal.woff2)}
@font-face{font-family:Cormorant;font-weight:300;src:url(FONTS/cormorant-garamond-latin-300-normal.woff2)}
@page{size:420mm 297mm;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff;color:#1E1E1E;font-family:Jost;font-weight:300}
.sheet{position:relative;width:420mm;height:297mm;page-break-after:always;overflow:hidden;background:#fff}
.frame{position:absolute;left:7mm;top:7mm;width:406mm;height:283mm;border:0.35mm solid #1E1E1E}
.v{position:absolute}
.vt{position:absolute;display:flex;align-items:baseline;gap:2mm;border-top:0.45mm solid #1E1E1E;padding-top:0.8mm;
 font-size:2.5mm;letter-spacing:.02em}
.vn{display:inline-block;min-width:5mm;height:5mm;line-height:5mm;border-radius:2.5mm;background:#1E1E1E;color:#fff;
 text-align:center;font-size:2.4mm;font-weight:500;padding:0 1mm}
.vtt{font-weight:500;text-transform:uppercase;letter-spacing:.06em;font-size:2.3mm}
.vs{margin-left:auto;font-size:2.3mm;color:#555}
.tx{position:absolute;font-size:2.35mm;line-height:1.38}
.nh{font-weight:500;text-transform:uppercase;letter-spacing:.12em;font-size:2.3mm;margin:0 0 1.4mm;color:#3A2A22}
.nl{margin:0 0 2mm;padding-left:3.6mm}
.nl li{margin:0 0 .7mm}
.cols{display:flex;gap:6mm}.cols>div{flex:1}.stack>div{margin-bottom:3mm}
.kpt{font-size:2mm;text-transform:uppercase;letter-spacing:.12em;color:#777}
.st-v{color:#1E1E1E}.st-d{color:#55603C;font-style:italic}.st-c{color:#8A1F35;font-weight:500}
.small{font-size:2.1mm;color:#555;line-height:1.4}
table.kv{border-collapse:collapse;width:100%;font-size:2.3mm}table.kv td{border-bottom:.15mm solid #E4DACB;padding:1mm .6mm}
table.tb2{border-collapse:collapse;font-size:2.25mm}table.tb2.full{width:100%}
table.tb2 th{font-weight:500;text-align:left;font-size:1.95mm;letter-spacing:.1em;text-transform:uppercase;color:#6E6259;
 border-bottom:.3mm solid #3A2A22;padding:1mm .8mm}
table.tb2 td{border-bottom:.15mm solid #E4DACB;padding:1.05mm .8mm;vertical-align:top}
table.tb2 td.ref{font-weight:500;color:#55603C}
.chip{display:inline-block;width:9mm;height:6mm;border:.15mm solid #999;vertical-align:middle}
.chip.none{text-align:center;line-height:6mm;color:#999;border-style:dashed}
.thumbs{display:grid;grid-template-columns:1fr 1fr;gap:2.5mm}
.thumbs figure{margin:0}.thumbs img{width:100%;display:block;border:.15mm solid #ddd}
.thumbs figcaption{font-size:1.8mm;color:#777;margin-top:.5mm}
.rimg{position:absolute;display:flex;align-items:center;justify-content:center}
.rimg img{max-width:100%;max-height:100%;display:block}
.rimg.hero{justify-content:flex-start}
.cap{font-size:2.45mm;margin:0 0 1.5mm;line-height:1.4}
/* title block */
.tb{position:absolute;left:345mm;top:7mm;width:68mm;height:283mm;border-left:.35mm solid #1E1E1E;padding:5mm 4.5mm;
 display:flex;flex-direction:column;gap:2.2mm;font-size:2.3mm}
.tb-logo svg{width:52mm;height:auto;display:block}
.tb-firm{font-weight:500;letter-spacing:.16em;font-size:2.2mm;border-bottom:.2mm solid #3A2A22;padding-bottom:2mm}
.tb-firm span{display:block;font-weight:300;letter-spacing:.08em;color:#6E6259;margin-top:.6mm}
.tb label{display:block;font-size:1.75mm;letter-spacing:.14em;text-transform:uppercase;color:#8A7B6E;margin-bottom:.4mm}
.tb-sec{border-bottom:.15mm solid #E4DACB;padding-bottom:1.6mm}
.tb-title div{font-family:Cormorant;font-size:5mm;line-height:1.08;color:#1E1E1E}
.tb-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.6mm 3mm;border-bottom:.15mm solid #E4DACB;padding-bottom:1.8mm}
.tb-legend{font-size:2.05mm;line-height:1.55;border-bottom:.15mm solid #E4DACB;padding-bottom:1.6mm}
.tb-legend span{display:inline-block;min-width:13mm}
.tb-note{font-size:1.9mm;color:#6E6259;line-height:1.4}
.tb-num{margin-top:auto;border-top:.45mm solid #1E1E1E;padding-top:1.6mm}
.tb-num div{font-size:5.4mm;font-weight:500;letter-spacing:.04em}
.tb-page{font-size:2.3mm;color:#555}
/* cover */
.cover-img{position:absolute;left:12mm;top:12mm;width:200mm;height:272mm;display:flex;align-items:center;justify-content:center}
.cover-img img{max-width:100%;max-height:100%}
.cover-txt{position:absolute;left:222mm;top:20mm;width:116mm}
.cv-logo svg{width:80mm;height:auto}
.cv-k{margin-top:18mm;font-size:2.8mm;letter-spacing:.24em;text-transform:uppercase;color:#6E2234}
.cover-txt h1{font-family:Cormorant;font-weight:300;font-size:13mm;line-height:1.02;margin:4mm 0 6mm}
.cv-list{font-size:3.1mm;line-height:1.6;color:#3A2A22;border-top:.25mm solid #3A2A22;padding-top:4mm}
.cv-meta{margin-top:10mm;font-size:3mm;line-height:1.6}
.cv-warn{margin-top:14mm;font-size:2.6mm;line-height:1.55;color:#555;border-left:.6mm solid #5F6A45;padding-left:3mm}
/* conventions */
.conv{position:absolute;left:14mm;top:14mm;width:324mm;display:flex;gap:10mm}
.conv .col{flex:1;font-size:2.45mm;line-height:1.45}
.conv h2{font-family:Cormorant;font-weight:400;font-size:6mm;margin:0 0 2.5mm}
table.lg{border-collapse:collapse;width:100%;margin-bottom:5mm}table.lg td{padding:1.6mm 1.5mm;border-bottom:.15mm solid #E4DACB;vertical-align:top}
td.big{font-size:4mm;white-space:nowrap;width:22mm}
table.lg2{border-collapse:collapse;margin-bottom:5mm;font-size:2.3mm}table.lg2 td{padding:1.3mm 1.4mm}
.sw{display:inline-block;width:9mm;height:4mm}.sw.poche{background:#2B2B2B}
.sw.hors{background:repeating-linear-gradient(45deg,#fff 0 .8mm,#ccc .8mm 1mm);border:.1mm solid #ccc}
.ln{display:inline-block;width:10mm;border-top:.5mm dashed #C8962E;vertical-align:middle}
.ln.jt{border-top:.2mm solid #8C8C8C}.ln.cf{border-top:.4mm dashed #8A1F35}
.bb{display:inline-block;border:.25mm solid #55603C;color:#55603C;border-radius:3mm;padding:0 1.4mm;font-size:2mm}
.wm,.sm{display:inline-block;width:5mm;height:5mm;border:.3mm solid #1E1E1E;border-radius:2.5mm;text-align:center;line-height:4.6mm;font-size:2.2mm}
.sm{border-radius:0;border-width:0 0 .4mm 0}
/* toc */
.toc{position:absolute;left:14mm;top:14mm;width:324mm;columns:2;column-gap:10mm;font-size:2.4mm}
.toc .lv{font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:#6E2234;margin:2.4mm 0 1mm;break-after:avoid}
.toc .r{display:flex;gap:2mm;border-bottom:.12mm solid #EEE6DA;padding:.65mm 0;break-inside:avoid}
.toc .r b{font-weight:500;width:21mm}.toc .r span.t{flex:1}.toc .r span.s{width:18mm;color:#777}.toc .r span.p{width:8mm;text-align:right}
"""


def toc_html(total):
    out, cur = "", None
    for i, sh in enumerate(SHEETS, 1):
        grp = sh["level"] + (" — " + sh["room"] if sh["room"] not in ("—", "Niveau", "Synthèse") else "")
        if sh["num"] in ("000", "001", "002"):
            grp = "Généralités"
        elif sh["room"] == "Niveau":
            grp = "Plans de niveaux"
        elif sh["room"] == "Synthèse":
            grp = "Synthèse"
        if grp != cur:
            out += f'<div class="lv">{html.escape(grp)}</div>'
            cur = grp
        out += (f'<div class="r"><b>KAI-VIL-{sh["num"]}</b><span class="t">{html.escape(sh["title"])}</span>'
                f'<span class="s">{sh["scale"]}</span><span class="p">{i}</span></div>')
    return f'<div class="toc">{out}</div>'


def main():
    BUILD.mkdir(exist_ok=True)
    build_front()
    build_levels()
    for k in ("sejour", "amis", "etsejour", "princ"):
        build_room(k)
    build_recap()
    total = len(SHEETS)
    pages = []
    for i, sh in enumerate(SHEETS, 1):
        body = sh["body"] if sh["body"] != "__TOC__" else toc_html(total)
        pages.append(f'<section class="sheet"><div class="frame"></div>{body}{title_block(sh, i, total)}</section>')
    css = CSS.replace("FONTS/", FONTS.as_uri() + "/")
    doc = (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>KAÏRA — {DOC}</title>'
           f'<style>{css}</style></head><body>{PATTERNS}{"".join(pages)}</body></html>')
    (BUILD / "dossier-technique.html").write_text(doc, encoding="utf-8")
    (BUILD / "sheets.json").write_text(json.dumps([{k: v for k, v in s.items() if k != "body"} for s in SHEETS],
                                                  ensure_ascii=False, indent=1))
    print(total, "planches")
    if "--no-pdf" not in sys.argv:
        js = f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage();
 await p.goto('file://{BUILD / "dossier-technique.html"}', {{ waitUntil: 'networkidle' }});
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
