"""KAÏRA — Villa : devis descriptif et quantitatif de fabrication du mobilier (A3 paysage). AUCUN PRIX.

Mise en page : identité éditoriale des dossiers KAÏRA (papier crème, Cormorant et Jost, folio).
Rendus : fichiers originaux insérés entiers ; les vues rapprochées sont des extraits signalés (zone encadrée sur le rendu
entier présenté sur la même fiche). Dessins : élévations du dossier technique de la villa (KAI-VIL) et du dossier de la
douche principale (KAI-DPE), régénérés à partir des mêmes données.

Usage : python3 tools/build.py [--previews]  ->  build/devis-fabrication.html, build/…pdf, build/prev-NN.png
"""
import html
import importlib.util
import math
import pathlib
import re
import shutil
import subprocess
import sys

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parents[1]
sys.path.insert(0, str(HERE))
import data_fab as F  # noqa: E402

sys.path.insert(1, str(REPO / "projects/dossier-technique/tools"))
import views as VV  # noqa: E402  (villa elevations and plans)

DPE_TOOLS = REPO / "projects/dossier-douche-etage1/tools"
sys.path.insert(2, str(DPE_TOOLS))
import views_dpe as VD  # noqa: E402  (shower drawings)

_s = importlib.util.spec_from_file_location("dpe_build", DPE_TOOLS / "build.py")
SB = importlib.util.module_from_spec(_s)
_s.loader.exec_module(SB)          # editorial stylesheet, logo, fonts of the KAÏRA dossiers

BUILD = ROOT / "build"
OUT_PDF = BUILD / "KAIRA-Villa-Devis-fabrication-mobilier-A3.pdf"
LOGO, FONTS = SB.LOGO, SB.FONTS

PROJECT = "Villa KAÏRA"
DOC = "Devis descriptif et quantitatif de fabrication du mobilier"
DATE = "18.11.2026"
INDICE = "0"
W, H, M = 420, 297, 18
PAGES = []

ELEV_REF = {("sejour", "A"): "KAI-VIL-201", ("sejour", "B"): "KAI-VIL-202", ("sejour", "C"): "KAI-VIL-202",
            ("sejour", "D1"): "KAI-VIL-203", ("sejour", "D2"): "KAI-VIL-204", ("sejour", "E"): "KAI-VIL-205",
            ("amis", "A"): "KAI-VIL-301", ("amis", "B"): "KAI-VIL-302", ("amis", "C"): "KAI-VIL-303",
            ("amis", "D"): "KAI-VIL-304", ("etsejour", "A"): "KAI-VIL-401", ("etsejour", "B"): "KAI-VIL-402",
            ("etsejour", "C"): "KAI-VIL-403", ("etsejour", "D"): "KAI-VIL-403", ("princ", "A"): "KAI-VIL-501",
            ("princ", "B"): "KAI-VIL-502", ("princ", "C"): "KAI-VIL-503", ("princ", "D"): "KAI-VIL-503"}
DPE_DRAW = {"elev_A": ("Élévation A — mur sud", "KAI-DPE-503", 20), "elev_B": ("Élévation B — mur est", "KAI-DPE-504", 20),
            "elev_C": ("Élévation C — mur nord", "KAI-DPE-505", 20), "elev_D": ("Élévation D — mur ouest", "KAI-DPE-506", 20),
            "elev_E": ("Élévation E — douche", "KAI-DPE-507", 20),
            "furniture_M1": ("Meuble vasque — vues cotées", "KAI-DPE-511", 10),
            "furniture_M2": ("Commode — vues cotées", "KAI-DPE-512", 10)}
SCALES = (10, 15, 20, 25, 30, 40, 50, 75, 100)

# surfaces (m², ≈) by material family, for the quantitative synthesis — from the dimensions of each sheet
SURF = {
    "Panneaux muraux (crème, beige)": [("SAL-08", None), ("SAM-05", None), ("AMI-08", None), ("SEJ-05", None), ("CHP-06", None)],
    "Chêne en applique (colonnes, montants, panneaux, lames)": [
        ("SAL-04", 3.44), ("SAL-06", 3.07), ("SAL-07", 3.60), ("SAM-02", 0.85), ("AMI-04", 1.17), ("AMI-06", 1.00), ("CHP-01", 0.75)],
    "Lames cannelées": [("SAL-02", 1.57), ("SAL-07", 1.94), ("CHP-01", 1.27)],
    "Marbre (habillages muraux)": [("AMI-05", None), ("CHP-02", None)],
    "Miroirs muraux": [("SAL-03", 0.52), ("AMI-03", 1.26), ("AMI-07", 0.13), ("CHP-03", None), ("DPE-06", 1.75)],
    "Effet travertin (douche principale)": [("DPE-08", None)],
    "Faïence bordeaux (douche principale)": [("DPE-09", None)],
}
SURF_NOTE = {"SAL-02": "toute hauteur, dont ≈ 0,66 visibles (le reste derrière les panneaux SAL-04)"}
LED = [("SAL-04", "Rétroéclairage périphérique des 2 panneaux + ligne verticale", "≈ 10,8 + ≈ 2,8"),
       ("SAL-05", "Éclairage des 3 niches", "3 niches"), ("SAL-07", "Ligne horizontale à ≈ 105", "≈ 1,85"),
       ("SEJ-02", "Sous les 7 tablettes", "≈ 2,1"), ("SEJ-03", "Sous les 5 tablettes", "≈ 8,1"),
       ("CHP-01", "Ligne horizontale à ≈ 184", "≈ 0,68"), ("CHP-02", "2 lignes verticales de part et d'autre", "≈ 5,8"),
       ("DPE-06", "Halo périphérique du miroir (si intégré)", "≈ 5,5")]


# ================================================================ helpers
def esc(s):
    return html.escape(str(s))


def T(s):
    """Escape + highlight every « … À CONFIRMER » and colour chips for the sampled HEX values."""
    t = esc(s)
    t = re.sub(r"((?:DIMENSION|FINITION|SUPPORT) À CONFIRMER|À CONFIRMER|À CONF\.)", r'<span class="st-c">\1</span>', t)
    t = re.sub(r"#([0-9A-F]{6})", r'<i class="chip" style="background:#\1"></i>#\1', t)
    return t


def num(v):
    if isinstance(v, (int, float)):
        r = round(v, 2)
        s = f"{r:.2f}".rstrip("0").rstrip(".") if r != int(r) else str(int(r))
        return s.replace(".", ",")
    return str(v)


def dim_val(v, st):
    if v is None:
        return '<span class="st-c">DIMENSION À CONFIRMER</span>'
    if isinstance(v, str):
        s = T(v)
        return s + (' <span class="st-c">— À CONFIRMER</span>' if st == "c" else "")
    if st == "v":
        return f'<b class="st-v">{num(v)}</b>'
    if st == "c":
        return f'<span class="st-d"><i>≈ {num(v)}</i></span> <span class="st-c">— À CONFIRMER</span>'
    return f'<span class="st-d"><i>≈ {num(v)}</i></span>'


def page(num_, title, section, body, cls=""):
    PAGES.append(dict(num=num_, title=title, section=section, body=body, cls=cls))


def box(x, y, w, inner, cls="ebox", h=None):
    hh = f";height:{h:.1f}mm" if h else ""
    return f'<div class="{cls}" style="left:{x:.1f}mm;top:{y:.1f}mm;width:{w:.1f}mm{hh}">{inner}</div>'


def kicker(t):
    return f'<div class="kick">{esc(t)}</div>'


def whole(name, x, y, w, h, align="center", frames=()):
    """Original render shown whole (contain), with optional framed zones drawn over it (SVG; the image is untouched)."""
    p = F.R(name)
    iw, ih = Image.open(p).size
    s = min(w / iw, h / ih)
    dw, dh = iw * s, ih * s
    ox = x + (w - dw) / 2 if align == "center" else (x if align == "left" else x + w - dw)
    oy = y + (h - dh) / 2 if align != "top" else y
    if align == "top":
        ox = x + (w - dw) / 2
    out = (f'<div class="rw" style="left:{ox:.2f}mm;top:{oy:.2f}mm;width:{dw:.2f}mm;height:{dh:.2f}mm">'
           f'<img src="{p.as_uri()}"></div>')
    if frames:
        sv = ""
        for label, (a, b, c, d) in frames:
            sv += (f'<rect x="{a}" y="{b}" width="{c - a}" height="{d - b}" fill="none" stroke="#FFFFFF" stroke-width="12" '
                   f'stroke-opacity=".75"/><rect x="{a}" y="{b}" width="{c - a}" height="{d - b}" fill="none" '
                   f'stroke="#6E2234" stroke-width="6"/>')
            ty = b - 14 if b > 70 else d + 52
            sv += (f'<rect x="{a}" y="{ty - 44}" width="{len(label) * 25 + 28}" height="58" fill="#6E2234"/>'
                   f'<text x="{a + 14}" y="{ty}" font-family="Jost" font-weight="500" font-size="40" fill="#fff">{esc(label)}</text>')
        out += (f'<svg class="ov" style="left:{ox:.2f}mm;top:{oy:.2f}mm;width:{dw:.2f}mm;height:{dh:.2f}mm" '
                f'viewBox="0 0 {iw} {ih}" preserveAspectRatio="none">{sv}</svg>')
    return out, (ox, oy, dw, dh)


def scaled(svg, w, h, bw, bh):
    """Fit an SVG drawing (paper mm) into a box; returns html, factor, drawn size."""
    f = min(1.0, bw / w, bh / h)
    dw, dh = w * f, h * f
    svg = re.sub(r'width="[\d.]+mm" height="[\d.]+mm"', f'width="{dw:.2f}mm" height="{dh:.2f}mm"', svg, count=1)
    return svg, f, dw, dh


def drawing(elev, bw, bh):
    """Return (svg html, title, scale label, sheet ref) for an element's elevation / drawing."""
    if elev is None:
        return None
    room, key = elev[0], elev[1]
    if room == "dpe":
        title, ref, sc = DPE_DRAW[key]
        svg, w, h = getattr(VD, key)()
        svg, f, dw, dh = scaled(svg, w, h, bw, bh)
        lab = f"1/{sc}" if f >= 0.999 else f"réduite (dessin source au 1/{sc})"
        return svg, dw, dh, title, lab, ref
    crop = elev[2]
    rname = {"sejour": "Salon et salle à manger", "amis": "Chambre d'amis", "etsejour": "Séjour", "princ": "Chambre principale"}[room]
    title = f"Élévation {key} — {rname}" + (" — extrait" if crop else "")
    for sc in SCALES:
        svg, w, h = VV.elev_view(room, key, scale=sc, crop=crop)
        if w <= bw and h <= bh:
            return svg, w, h, title, f"1/{sc}", ELEV_REF[(room, key)]
    svg, f, dw, dh = scaled(svg, w, h, bw, bh)
    return svg, dw, dh, title, "réduite", ELEV_REF[(room, key)]


def plan_svg(code, bw, bh):
    key = {"SAL": "sejour", "SAM": "sejour", "AMI": "amis", "SEJ": "etsejour", "CHP": "princ"}.get(code)
    if key:
        svg, w, h = VV.plan_room(key)
        sc = VV.ROOM_VIEW[key]["scale"]
        ref = {"sejour": "KAI-VIL-200", "amis": "KAI-VIL-300", "etsejour": "KAI-VIL-400", "princ": "KAI-VIL-500"}[key]
    else:
        svg, w, h = VD.plan(scale=20, mode="cote")
        sc, ref = 20, "KAI-DPE-501"
    svg, f, dw, dh = scaled(svg, w, h, bw, bh)
    return svg, dw, dh, f"1/{sc}" if f >= .999 else f"réduite (source au 1/{sc})", ref


def room_of(code):
    return next(r for r in F.ROOMS if r[0] == code)


def qty_txt(it):
    q = it["qty"]
    return ("≈ " if it["unit"] == "m²" else "") + num(q)


# ================================================================ front matter
def front():
    logo = LOGO.read_text()
    img, r = whole("rdc-salon-07", 0, 0, 272, H, "left")
    rooms = "".join(f"<li><b>{c}</b> {esc(n)} <span>{esc(l)}</span></li>" for c, n, l, *_ in F.ROOMS)
    body = img + f"""
<div class="cv-panel" style="left:{r[2] + 14:.1f}mm;width:{W - r[2] - 30:.1f}mm">
  <div class="cv-logo">{logo}</div>
  <div class="cv-mid"><div class="kick">Consultation fabricant</div>
   <h1 class="cvt">Devis descriptif <em>et quantitatif</em></h1>
   <p class="cv-sub">de fabrication du mobilier</p><div class="rule"></div>
   <p class="cv-proj">{PROJECT}</p><ul class="cv-rooms">{rooms}</ul></div>
  <div class="cv-foot">Indice {INDICE} — {DATE}<br>Format A3 paysage · cotes en centimètres<br>
   <span>Document sans prix — à chiffrer référence par référence</span></div>
</div>"""
    page("0.00", "Couverture", "Couverture", body, "p-cover")
    page("0.01", "Sommaire", "Sommaire", "__TOC__")

    n_items = sum(len(v) for v in F.ITEMS.values())
    body = box(M, M, 384, f'{kicker("Objet du document")}<h2>Périmètre, <em>conventions et mode de chiffrage</em></h2>')
    body += box(M, 50, 120, f"""<h3>Objet</h3>
<p>Ce document décrit, élément par élément, tout le mobilier et tous les ouvrages de menuiserie et d'habillage à fabriquer
pour la villa : {n_items} références réparties sur six espaces. Il est destiné au fabricant, qui chiffre
<b>chaque référence séparément</b>, dans l'unité indiquée (pièce, ensemble, m², ml).</p>
<p class="nop">Ce document ne contient aucun prix, aucun montant et aucun total financier.</p>
<h3>Espaces concernés</h3><ul class="nl">
<li><b>Rez-de-chaussée</b> — Salon principal (SAL) · Espace salle à manger (SAM) · Chambre d'amis (AMI)</li>
<li><b>Étage 1</b> — Séjour (SEJ) · Chambre principale (CHP) · Douche principale (DPE)</li></ul>
<h3>Hors du présent devis</h3><ul class="nl">
<li>Le placard de la chambre principale et le placard d'angle de la chambre d'amis</li>
<li>Tous les lits et toutes les tables de chevet</li>
<li>Les téléviseurs — <b>les meubles TV, leurs structures, leurs habillages muraux et leurs rangements sont inclus</b></li>
<li>Le mobilier, les luminaires et les équipements achetés séparément : liste en annexe B</li></ul>""")
    body += box(M + 132, 50, 120, f"""<h3>Les cotes</h3>
<table class="lg"><tr><td class="st-v big">163</td><td><b>Cote écrite</b> sur un plan coté du projet, reprise telle quelle.</td></tr>
<tr><td class="st-d big"><i>≈ 259</i></td><td><b>Cote relevée</b> sur la maquette (rendus de face calibrés sur une cote écrite,
vues de dessus recalées sur les plans). Arrondie au centimètre — tolérance ±3 cm en plan, ±5 cm en hauteur.</td></tr>
<tr><td class="st-c big">À CONF.</td><td><b>DIMENSION À CONFIRMER</b> — aucune source dans les documents du projet. Jamais inventée.</td></tr></table>
<p><b>Toutes les cotes sont à vérifier sur site par le fabricant avant fabrication.</b> Les surfaces (m²) sont des surfaces
brutes calculées à partir des élévations, déduction faite des ouvertures dont la hauteur est connue ; les métrés de LED (ml)
sont indicatifs.</p>
<h3>Matériaux et finitions</h3>
<p>Les matières sont nommées comme elles apparaissent sur les rendus validés. La teinte indiquée (code HEX) est la médiane
des pixels du rendu : indicative, elle dépend de l'éclairage de la scène. Quand la nature exacte n'est pas connue :
<span class="st-c">FINITION À CONFIRMER</span> ; quand le panneau support n'est pas défini : <span class="st-c">SUPPORT À CONFIRMER</span>.
Aucune référence commerciale n'est indiquée.</p>""")
    body += box(M + 264, 50, 120, f"""<h3>Organisation</h3><ul class="nl">
<li><b>Une section par espace</b> : vue d'ensemble et plan, puis une fiche par référence — rendu entier avec la zone encadrée,
extrait agrandi, élévation ou dessin coté, et description en 17 rubriques.</li>
<li><b>Un bordereau par espace</b> : N° de référence, désignation, description technique, dimensions, matériaux et finitions,
quantité, unité, observations.</li>
<li><b>Une synthèse quantitative</b> générale, puis les annexes : A — éléments exclus ; B — hors fabrication ;
C — points à confirmer, référence par référence.</li></ul>
<h3>Rendus et dessins</h3>
<p>Les rendus 3D sont les fichiers originaux validés, insérés en entier, sans recadrage, retouche ni modification. Les vues
rapprochées sont des extraits signalés (cadre bordeaux sur le rendu entier de la même fiche). Les élévations proviennent
du dossier technique de la villa (KAI-VIL) et du dossier de la douche principale (KAI-DPE).</p>
<h3>Unités</h3><p><b>pce</b> pièce · <b>ens.</b> ensemble (plusieurs pièces chiffrées ensemble) · <b>m²</b> mètre carré ·
<b>ml</b> mètre linéaire.</p>""")
    page("0.02", "Périmètre, conventions et mode de chiffrage", "Présentation", body)

    # exclusions at a glance
    rows = "".join(f"<tr><td>{esc(r)}</td><td>{T(d)}</td><td class='src'>{esc(n)}</td></tr>" for r, d, n in F.EXCLUDED)
    shots = ""
    for i, n in enumerate(["chambre-principale-04", "chambre-principale-05", "chambre-amis-03", "chambre-amis-01"]):
        img, _ = whole(n, M + 214 + (i % 2) * 87, 50 + (i // 2) * 101, 84, 92)
        shots += img + box(M + 214 + (i % 2) * 87, 50 + (i // 2) * 101 + 92.5, 84, f'<span class="src">{n}</span>')
    body = box(M, M, 384, f'{kicker("Exclusions")}<h2>Éléments <em>exclus du devis</em></h2>')
    body += box(M, 52, 200, f"""<table class="tb3"><tr><th>Espace</th><th>Élément exclu</th><th>Rendu</th></tr>{rows}</table>
<p class="small" style="margin-top:5mm">Les meubles TV, leurs structures, leurs habillages muraux et leurs rangements sont
<b>inclus</b> : seul le téléviseur est exclu. Dans la chambre principale, la tête de lit murale tapissée (CHP-04), fixée au
mur et indépendante du lit, est incluse sous réserve de confirmation. Les rendus ci-contre sont présentés pour repérer
les éléments exclus : ils restent entiers et non modifiés.</p>""")
    body += shots
    page("0.03", "Éléments exclus du devis", "Présentation", body)


# ================================================================ room sections
def opener(si, code):
    c, name, level, key, render, sheets = room_of(code)
    items = F.ITEMS[code]
    img, r = whole(render, W - 250, 0, 250, H, "right")
    lw = r[0] - M - 14
    li = "".join(f'<div class="oi"><b>{i["ref"]}</b><span>{esc(i["short"])}</span><i>{qty_txt(i)} {i["unit"]}</i></div>'
                 for i in items)
    ex = [e for e in F.EXCLUDED if e[0].startswith(name.split(" (")[0])]
    exl = "".join(f"<li>{T(e[1])}</li>" for e in ex)
    svg, dw, dh, sc, ref = plan_svg(code, lw, 70)
    body = img + box(M, 22, lw, f"""<div class="bignum">0{si}</div>{kicker(level)}
<h2 class="xl">{esc(name)}</h2><div class="rule"></div>
<div class="kick">{len(items)} références à fabriquer</div><div class="olist2">{li}</div>
{f'<div class="exn"><b>Exclus dans cet espace</b><ul>{exl}</ul></div>' if exl else ''}""")
    body += (f'<div class="pl" style="left:{M}mm;top:{H - 30 - dh:.1f}mm;width:{dw:.1f}mm;height:{dh:.1f}mm">{svg}</div>'
             + box(M, H - 28, lw, f'<span class="src">Plan — {esc(name)} · échelle {sc} · {ref} · repères des murs A, B, C… '
                                  f'utilisés par les élévations</span>'))
    body += box(r[0] + 3, H - 12, r[2] - 6, f'<span class="src lt">Rendu {render} — original, non modifié</span>')
    page(f"{si}.00", name, name, body, "p-open")


def field_rows(it, room_name, level):
    dims = "".join(f"<div class='dl'><span class='lb'>{esc(l)}</span><div class='dv'>{dim_val(v, st)}</div></div>"
                   for l, v, st in it["dims"])
    rows = [("Dimensions (L · l · H · P)", dims),
            ("Matériaux", T(it["mat"])), ("Type de panneaux et supports", T(it["support"])),
            ("Finitions et couleurs", T(it["finish"])), ("Revêtements et textures", T(it["revet"])),
            ("Façades", T(it["facades"])), ("Poignées et accessoires", T(it["handles"])),
            ("Systèmes d'ouverture", T(it["opening"])), ("Éclairage intégré", T(it["light"])),
            ("Détails de fabrication", T(it["fab"])), ("Installation et pose", T(it["pose"])),
            ("Référence rendu / élévation", T(it["refs"])), ("Observations", T(it["obs"]))]
    head = (f'<div class="fh"><div><label>Espace</label>{esc(room_name)} · {esc(level)}</div>'
            f'<div><label>Référence</label><b class="rf">{it["ref"]}</b></div>'
            f'<div><label>Quantité</label><b>{qty_txt(it)}</b> {it["unit"]}</div>'
            f'<div><label>Nature</label>{esc(it["cat"])}</div></div>')
    return head + '<table class="mt ft">' + "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in rows) + "</table>"


def situation(room, key, crop, bw, bh):
    """Whole wall elevation (no dimensions) with the element's zone framed — to locate the element on its wall."""
    E = VV.D.ELEV[room][key]
    Hh = VV.D.ROOMS[room]["height"]
    for sc in SCALES[2:] + (150,):
        svg, w, h = VV.elev_view(room, key, scale=sc, show_dims=False, show_levels=False, labels=False)
        if w <= bw and h <= bh:
            m = 10.0 / sc
            x0, x1, z0, z1 = crop
            X, Z = 16 + x0 * m, 12 + (Hh - z1) * m
            rect = (f'<rect x="{X:.2f}" y="{Z:.2f}" width="{(x1 - x0) * m:.2f}" height="{(z1 - z0) * m:.2f}" fill="#6E2234" '
                    f'fill-opacity=".10" stroke="#6E2234" stroke-width=".45"/>')
            return svg.replace("</svg>", rect + "</svg>"), w, h, f"1/{sc}", E
    return None


def element(si, code, n, it):
    c, name, level, key, render, sheets = room_of(code)
    rname, b = it["img"]
    ew, eh = b[2] - b[0], b[3] - b[1]
    a = ew / eh
    LX, LW, TOP, BOT = M, 222, 44, H - 15
    TX, TW = M + LW + 8, W - M - (M + LW + 8)
    src_uri = F.R(rname).as_uri()
    if a >= 1.0:                        # extract on top, drawings below (full width)
        exh = min(LW / a, 116)
        exw = exh * a
        ex_x, ex_y = LX, TOP
        cx, cy, cw, ch = LX, TOP + exh + 9, LW, BOT - (TOP + exh + 9)
    else:                               # tall extract on the left, drawings on its right (full height)
        exw = min((BOT - TOP - 12) * a, 104)
        exh = exw / a
        ex_x, ex_y = LX, TOP
        cx, cy, cw, ch = LX + exw + 6, TOP, LW - exw - 6, BOT - TOP
    iw, ih = Image.open(F.R(rname)).size
    k = exw / ew            # mm per pixel: the original render, shown through a window (no pixel crop, no resampling file)
    ext = (f'<div class="ex zoom" style="left:{ex_x:.1f}mm;top:{ex_y:.1f}mm;width:{exw:.2f}mm;height:{exh:.2f}mm">'
           f'<img src="{src_uri}" style="position:absolute;left:{-b[0] * k:.3f}mm;top:{-b[1] * k:.3f}mm;width:{iw * k:.3f}mm;'
           f'height:{ih * k:.3f}mm;max-width:none"><span class="etag">{it["ref"]}</span></div>'
           + box(ex_x, ex_y + exh + 0.8, max(exw, 58), f'<span class="src">Extrait agrandi du rendu {rname} — voir le rendu '
                                                       f'entier ci-contre</span>'))
    # drawings card: the element drawing (+ its wall, whole, for situation)
    inner, cap = "", []
    d = drawing(it["elev"], cw - 8, ch - 20)
    if d is None:
        svg, dw, dh, sc, ref = plan_svg(code, cw - 8, ch - 20)
        d = (svg, dw, dh, f"Plan — {name} (élément sans élévation de face)", sc, ref)
    svg, dw, dh, title, sc, ref = d
    sit = None
    elev = it["elev"]
    if elev and elev[0] != "dpe" and elev[2]:
        if cw - dw - 14 >= 60:
            sit = situation(elev[0], elev[1], elev[2], cw - dw - 18, ch - 24)
            side = True
        elif ch - dh - 20 >= 40:
            sit = situation(elev[0], elev[1], elev[2], cw - 10, ch - dh - 28)
            side = False
    if sit:
        s2, w2, h2, sc2, _ = sit
        if side:
            gap = (cw - dw - w2) / 3
            p1 = (gap, 4 + (ch - 20 - dh) / 2)
            p2 = (gap * 2 + dw, 4 + (ch - 20 - h2) / 2)
        else:
            gap = (ch - 20 - dh - h2) / 3
            p1 = ((cw - dw) / 2, 4 + gap)
            p2 = ((cw - w2) / 2, 4 + gap * 2 + dh)
        inner = (f'<div class="cd" style="left:{p1[0]:.1f}mm;top:{p1[1]:.1f}mm">{svg}</div>'
                 f'<div class="cd" style="left:{p2[0]:.1f}mm;top:{p2[1]:.1f}mm">{s2}</div>')
        cap = (f'<b>{esc(title)}</b><span>échelle {sc} · {ref} — {"à droite" if side else "en dessous"} : mur {elev[1]} entier '
               f'au {sc2}, zone de l\'élément teintée</span>')
    else:
        inner = f'<div class="cd" style="left:{(cw - dw) / 2:.1f}mm;top:{4 + (ch - 20 - dh) / 2:.1f}mm">{svg}</div>'
        cap = f'<b>{esc(title)}</b><span>échelle {sc} · {ref}</span>'
    card = (f'<div class="card" style="left:{cx:.1f}mm;top:{cy:.1f}mm;width:{cw:.1f}mm;height:{ch:.1f}mm">{inner}'
            f'<div class="ct">{cap}</div></div>')
    # whole render (framed zone) bottom right, table above it
    rh = 84
    img, rr = whole(rname, TX, BOT - rh, 0.918 * rh, rh, "left", frames=[(it["ref"], b)])
    rcap = box(TX + rr[2] + 5, BOT - 30, TW - rr[2] - 5,
               f'<div class="kick">Rendu de référence</div><span class="src">Rendu <b>{rname}</b> entier — fichier original, '
               f'non recadré, non modifié. Cadre bordeaux : zone de l\'extrait agrandi.</span>')
    head = box(M, 13, 384, f'{kicker(f"{name} · {level} · {it["cat"]}")}<h2 class="ph"><span class="rtag">{it["ref"]}</span>'
                           f'{esc(it["name"])}</h2>')
    table = (f'<div class="ebox fbox" data-fit="{BOT - rh - 6 - TOP:.1f}" style="left:{TX:.1f}mm;top:{TOP}mm;width:{TW:.1f}mm">'
             f'{field_rows(it, name, level)}</div>')
    body = head + ext + card + table + img + rcap
    page(f"{si}.{n:02d}", f'{it["ref"]} — {it["name"]}', name, body)


def describe(it):
    parts = [it["facades"], it["opening"], it["light"] if not it["light"].startswith("Aucun") else "", it["fab"], it["pose"]]
    return " · ".join(p for p in parts if p and p != "—")


def dims_compact(it):
    return "<br>".join(f"{esc(l)} : {dim_val(v, st)}" for l, v, st in it["dims"] if l != "Détail")


def bordereau(si, code):
    c, name, level, *_ = room_of(code)
    items = F.ITEMS[code]
    cols = [(15, "N° de référence"), (36, "Désignation"), (104, "Description technique"), (62, "Dimensions"),
            (66, "Matériaux et finitions"), (17, "Quantité"), (12, "Unité"), (72, "Observations")]

    def row(it):
        mat = it["mat"] + (" · " + it["finish"] if it["finish"] != F.FA else " · Finition : À CONFIRMER")
        obs = it["obs"] if it["obs"] != "—" else ""
        if it["support"] == F.SA:
            obs = (obs + " · " if obs else "") + "Support : SUPPORT À CONFIRMER."
        cells = [f'<td class="ref">{it["ref"]}</td>', f'<td><b>{esc(it["name"])}</b></td>', f"<td>{T(describe(it))}</td>",
                 f"<td>{dims_compact(it)}</td>", f"<td>{T(mat)}</td>", f'<td class="q">{qty_txt(it)}</td>',
                 f'<td class="q">{it["unit"]}</td>', f"<td>{T(obs)}</td>"]
        texts = [it["ref"], it["name"], describe(it), " ".join(f"{l} : {v}xxxxxx" for l, v, _ in it["dims"]), mat, "", "", obs]
        lines = 1
        for (w, _), t in zip(cols, texts):
            cpl = max(1, (w - 2.4) / 1.28)
            lines = max(lines, math.ceil(len(t) / cpl) + (len(it["dims"]) if t.endswith("xxxxxx") else 0) * 0)
        lines = max(lines, len([d for d in it["dims"] if d[0] != "Détail"]))
        return "<tr>" + "".join(cells) + "</tr>", lines * 3.45 + 3.6

    rows = [row(i) for i in items]
    chunks, cur, hgt = [], [], 0
    for r_, h_ in rows:
        if cur and hgt + h_ > 214:
            chunks.append(cur)
            cur, hgt = [], 0
        cur.append(r_)
        hgt += h_
    chunks.append(cur)
    th = "".join(f'<th style="width:{w}mm">{t}</th>' for w, t in cols)
    for k, ch in enumerate(chunks):
        suf = f" ({k + 1}/{len(chunks)})" if len(chunks) > 1 else ""
        body = box(M, M - 3, 384, f'{kicker(f"{name} · {level} · bordereau quantitatif")}'
                                  f'<h2 class="ph">Bordereau — <em>{esc(name)}</em>{suf}</h2>')
        body += box(M, 44, 384, f'<table class="bd"><tr>{th}</tr>{"".join(ch)}</table>'
                                + ('<p class="small" style="margin-top:3mm">Quantités : pièces comptées sur les rendus ; '
                                   'surfaces brutes ≈ en m² calculées sur les élévations. Aucun prix : chaque ligne est à '
                                   'chiffrer séparément par le fabricant.</p>' if k == len(chunks) - 1 else ""))
        page(f"{si}.9{k}", f"Bordereau — {name}{suf}", name, body)


# ================================================================ synthesis and annexes
def synthesis():
    allit = [(c, i) for c, *_ in F.ROOMS for i in F.ITEMS[c]]
    byref = {i["ref"]: i for _, i in allit}
    half = math.ceil(len(allit) / 2)

    def tab(lst):
        r = ""
        last = None
        for c, i in lst:
            nm = room_of(c)[1]
            if nm != last:
                r += f'<tr class="grp"><td colspan="4">{esc(nm)} — {esc(room_of(c)[2])}</td></tr>'
                last = nm
            r += (f'<tr><td class="ref">{i["ref"]}</td><td>{esc(i["name"])}</td><td class="q">{qty_txt(i)}</td>'
                  f'<td class="q">{i["unit"]}</td></tr>')
        return f'<table class="tb3 sy"><tr><th>Réf.</th><th>Désignation</th><th>Qté</th><th>Unité</th></tr>{r}</table>'
    body = box(M, M - 3, 384, f'{kicker("Synthèse quantitative")}<h2 class="ph">Récapitulatif <em>de toutes les références</em></h2>')
    body += box(M, 42, 188, tab(allit[:half])) + box(M + 196, 42, 188, tab(allit[half:]))
    page("7.01", "Récapitulatif de toutes les références", "Synthèse", body)

    # per room and per category
    rr = ""
    for c, name, level, *_ in F.ROOMS:
        its = F.ITEMS[c]
        pce = sum(i["qty"] for i in its if i["unit"] == "pce")
        ens = sum(i["qty"] for i in its if i["unit"] == "ens.")
        m2 = sum(i["qty"] for i in its if i["unit"] == "m²")
        rr += (f"<tr><td><b>{esc(name)}</b><br><span class='src'>{esc(level)}</span></td><td class='q'>{len(its)}</td>"
               f"<td class='q'>{pce}</td><td class='q'>{ens or '—'}</td><td class='q'>≈ {num(round(m2, 2))}</td></tr>")
    tot = [len(allit), sum(i["qty"] for _, i in allit if i["unit"] == "pce"), sum(i["qty"] for _, i in allit if i["unit"] == "ens."),
           round(sum(i["qty"] for _, i in allit if i["unit"] == "m²"), 2)]
    rr += (f"<tr class='tot'><td>Total villa</td><td class='q'>{tot[0]}</td><td class='q'>{tot[1]}</td><td class='q'>{tot[2]}</td>"
           f"<td class='q'>≈ {num(tot[3])}</td></tr>")
    cats = {}
    for _, i in allit:
        cats.setdefault(i["cat"], []).append(i)
    cr = ""
    for k, its in cats.items():
        per = {}
        for i in its:
            per[i["unit"]] = per.get(i["unit"], 0) + i["qty"]
        q = " · ".join(("≈ " if u == "m²" else "") + f"{num(round(v, 2))} {u}" for u, v in per.items())
        cr += f"<tr><td><b>{esc(k)}</b></td><td>{', '.join(i['ref'] for i in its)}</td><td>{q}</td></tr>"
    body = box(M, M - 3, 384, f'{kicker("Synthèse quantitative")}<h2 class="ph">Totaux <em>par espace et par nature d\'ouvrage</em></h2>')
    body += box(M, 44, 150, f"""<h3>Par espace</h3><table class="tb3 sy2"><tr><th>Espace</th><th>Réf.</th><th>Pièces</th>
<th>Ensembles</th><th>Habillages m²</th></tr>{rr}</table>
<p class="small" style="margin-top:4mm">Pièces : somme des quantités en « pce » (une référence peut compter plusieurs pièces
identiques ou de même nature). Surfaces : brutes, ≈, ouvertures sans hauteur connue non déduites.</p>""")
    body += box(M + 162, 44, 222, f'<h3>Par nature d\'ouvrage</h3><table class="tb3 sy2"><tr><th>Nature</th><th>Références</th>'
                                  f'<th>Quantités</th></tr>{cr}</table>')
    page("7.02", "Totaux par espace et par nature d'ouvrage", "Synthèse", body)

    # surfaces and LED
    sr = ""
    for fam, lst in SURF.items():
        tot_ = 0
        det = []
        for ref, v in lst:
            v = byref[ref]["qty"] if v is None else v
            tot_ += v
            det.append(f"{ref} ≈ {num(v)}" + (f" ({SURF_NOTE[ref]})" if ref in SURF_NOTE else ""))
        sr += f"<tr><td><b>{esc(fam)}</b></td><td>{esc(' · '.join(det))}</td><td class='q'>≈ {num(round(tot_, 2))}</td></tr>"
    lr = "".join(f"<tr><td class='ref'>{r}</td><td>{esc(byref[r]['name'])}</td><td>{esc(d)}</td><td class='q'>{esc(v)}</td></tr>"
                 for r, d, v in LED)
    menu = [i for _, i in allit if i["cat"] == "Menuiserie"]
    mr = "".join(f"<tr><td class='ref'>{i['ref']}</td><td>{esc(i['name'])}</td><td>{dims_compact(i)}</td><td>{T(i['obs'])}</td></tr>"
                 for i in menu)
    body = box(M, M - 3, 384, f'{kicker("Synthèse quantitative")}<h2 class="ph">Surfaces d\'habillage, <em>éclairage intégré et menuiseries</em></h2>')
    body += box(M, 44, 228, f"""<h3>Surfaces d'habillage par famille de matériau (m², ≈)</h3>
<table class="tb3 sy2"><tr><th>Famille</th><th>Détail par référence</th><th>Total</th></tr>{sr}</table>
<p class="small" style="margin-top:3mm">Surfaces calculées d'après les dimensions des fiches (largeur × hauteur) ou sur les
élévations ; à vérifier sur site. Les miroirs DPE-06 et la paroi DPE-10 peuvent relever d'un miroitier.</p>
<h3 style="margin-top:6mm">Menuiseries et paroi — fourniture par l'atelier à confirmer</h3>
<table class="tb3 sy2"><tr><th>Réf.</th><th>Désignation</th><th>Dimensions</th><th>Observation</th></tr>{mr}</table>""")
    body += box(M + 238, 44, 146, f"""<h3>Éclairage intégré au mobilier (ml de LED, ≈)</h3>
<table class="tb3 sy2"><tr><th>Réf.</th><th>Élément</th><th>Position</th><th>ml</th></tr>{lr}</table>
<p class="small" style="margin-top:3mm">Métrés indicatifs, d'après les dimensions des éléments éclairés. Profilés, diffuseurs,
température de couleur, indice de protection (douche), alimentations et commandes : <span class="st-c">À CONFIRMER</span>.
Les gorges lumineuses des faux plafonds ne font pas partie de ce devis.</p>""")
    page("7.03", "Surfaces, éclairage intégré et menuiseries", "Synthèse", body)


def annexes():
    rows = "".join(f"<tr><td>{esc(r)}</td><td>{esc(d)}</td><td class='src'>{esc(n)}</td></tr>" for r, d, n in F.EXCLUDED)
    rows2 = "".join(f"<tr><td>{esc(r)}</td><td>{esc(d)}</td><td>{T(s.replace('à confirmer', 'À CONFIRMER'))}</td></tr>"
                    for r, d, s in F.OUTSIDE)
    body = box(M, M - 3, 384, f'{kicker("Annexes A et B")}<h2 class="ph">Éléments exclus <em>et éléments hors fabrication</em></h2>')
    body += box(M, 44, 150, f"""<h3>A — Éléments exclus du devis</h3><table class="tb3"><tr><th>Espace</th><th>Élément</th>
<th>Rendu</th></tr>{rows}</table><p class="small" style="margin-top:3mm">Exclusions demandées par KAÏRA. Les meubles TV et
leurs habillages restent inclus ; seul le téléviseur est exclu.</p>""")
    body += box(M + 162, 44, 222, f"""<h3>B — Hors fabrication : à approvisionner ou à confirmer</h3>
<table class="tb3"><tr><th>Espace</th><th>Élément</th><th>Statut</th></tr>{rows2}</table>
<p class="small" style="margin-top:3mm">Éléments visibles sur les rendus mais qui ne relèvent pas de la fabrication sur mesure
(mobilier, luminaires, sanitaires, textiles et accessoires du commerce, autres corps d'état). Les éléments marqués
« fabrication ou achat : À CONFIRMER » peuvent être ajoutés au devis sur décision de KAÏRA.</p>""")
    page("8.01", "Annexes A et B — exclus et hors fabrication", "Annexes", body)

    # C — points to confirm
    entries = []
    for c, *_ in F.ROOMS:
        for it in F.ITEMS[c]:
            pts = [f"{l.lower()}" for l, v, st in it["dims"] if v is None or st == "c"]
            for k, lab in (("mat", "matériau"), ("finish", "finition"), ("support", "support"), ("facades", "façades"),
                           ("handles", "poignées"), ("opening", "ouverture"), ("light", "éclairage"), ("fab", "fabrication"),
                           ("revet", "revêtement"), ("obs", "fourniture")):
                if "CONFIRMER" in it[k] and lab not in pts:
                    pts.append(lab)
            entries.append((it["ref"], it["name"], pts))
    half = math.ceil(len(entries) / 2)

    def tb(lst):
        r = "".join(f"<tr><td class='ref'>{a}</td><td><b>{esc(b)}</b> — <span class='st-c'>à confirmer :</span> "
                    f"{esc(' · '.join(p))}</td></tr>" for a, b, p in lst)
        return f'<table class="tb3 pc"><tr><th>Réf.</th><th>Points à confirmer avant chiffrage définitif</th></tr>{r}</table>'
    body = box(M, M - 3, 384, f'{kicker("Annexe C")}<h2 class="ph">Points à confirmer <em>référence par référence</em></h2>')
    body += box(M, 42, 188, tb(entries[:half])) + box(M + 196, 42, 188, tb(entries[half:]))
    body += box(M, 266, 384, '<p class="small">Le détail de chaque point figure sur la fiche de la référence (rubriques marquées '
                             '<span class="st-c">À CONFIRMER</span>). Toutes les cotes ≈ sont des relevés : à vérifier sur site '
                             'avant fabrication. Aucune cote, aucun matériau et aucune référence commerciale n\'a été inventé.</p>')
    page("8.02", "Annexe C — points à confirmer", "Annexes", body)

    logo = LOGO.read_text()
    img, r = whole("etage1-sejour-08", 0, 0, 272, H, "left")
    page("8.99", "Dos", "Dos", img + f'<div class="back" style="left:{r[2]:.1f}mm"><div class="cv-logo">{logo}</div>'
         f'<div class="rule"></div><p>{PROJECT}<br>{DOC}<br>Indice {INDICE} — {DATE}<br>Document sans prix</p></div>', "p-back")


# ================================================================ chrome, toc, css
def folio(pg, i, total):
    first = "KAÏRA" if pg["cls"] == "p-open" else "KAÏRA Interior Design · Villa — devis de fabrication du mobilier · sans prix"
    return (f'<div class="fol"><span>{first}</span><span>{esc(pg["section"])}</span>'
            f'<span>{pg["num"]} · indice {INDICE} · <b>{i}</b> / {total}</span></div>')


def toc_html(total):
    index = {p["num"]: i for i, p in enumerate(PAGES, 1)}
    groups = [("0 · Présentation", "0")] + [(f"{k} · {r[1]} — {r[2]}", str(k)) for k, r in enumerate(F.ROOMS, 1)] + \
        [("7 · Synthèse quantitative", "7"), ("8 · Annexes", "8")]
    out = ""
    for g, pre in groups:
        out += f'<div class="tg"><div class="kick">{esc(g)}</div>'
        for p in PAGES:
            if p["num"].split(".")[0] == pre and p["cls"] not in ("p-back",):
                out += f'<div class="tr"><b>{p["num"]}</b><span>{esc(p["title"])}</span><i>{index[p["num"]]}</i></div>'
        out += "</div>"
    return box(M, M - 4, 384, f'{kicker("Sommaire")}<h2 class="ph">Contenu <em>du devis</em></h2><div class="toc2">{out}</div>')


CSS = """
.cvt{font-size:17mm!important}.cv-sub{font-family:Cormorant;font-size:9mm;font-weight:300;margin:1mm 0 0;color:#2B2622}
.cv-rooms{list-style:none;padding:0;margin:3mm 0 0;font-size:3.1mm}
.cv-rooms li{border-bottom:.2mm solid #CDBFAE;padding:1.4mm 0}.cv-rooms b{color:#6E2234;font-weight:500;display:inline-block;width:11mm}
.cv-rooms span{float:right;color:#8C7462;font-size:2.5mm;letter-spacing:.12em;text-transform:uppercase}
.nop{border:.3mm solid #6E2234;color:#6E2234;padding:2.4mm 3mm;font-weight:400}
.rtag{display:inline-block;background:#6E2234;color:#fff;font-family:Jost;font-weight:500;font-size:4.2mm;letter-spacing:.08em;
 padding:1mm 2.6mm;margin-right:4mm;vertical-align:2mm}
.ed h2.ph{font-size:8.6mm;line-height:1.1}
.olist2{margin:1mm 0 4mm}.oi{display:flex;gap:2.6mm;border-bottom:.2mm solid #CDBFAE;padding:1.25mm 0;font-size:2.85mm}
.oi b{color:#6E2234;font-weight:500;width:13mm;flex:none}.oi span{flex:1}.oi i{font-style:normal;color:#8C7462;white-space:nowrap}
.exn{font-size:2.6mm;color:#6E6258;line-height:1.4}.exn b{font-weight:500;letter-spacing:.1em;text-transform:uppercase;font-size:2.2mm}
.exn ul{margin:1mm 0 0;padding-left:3.4mm}
.pl{position:absolute;background:#fff;box-shadow:0 0 0 .2mm #CDBFAE}.pl svg{display:block}
.src.lt{color:#fff;text-shadow:0 0 1mm rgba(0,0,0,.6)}
.ex.zoom{background:#fff}.ex.zoom img{object-fit:fill}
.card{position:absolute;background:#fff;box-shadow:0 0 0 .2mm #CDBFAE}.cd{position:absolute}.cd svg{display:block}
.ct{position:absolute;left:3mm;right:3mm;bottom:2.2mm;font-size:2.3mm;line-height:1.35;border-top:.3mm solid #3A2A22;padding-top:.9mm}
.ct b{display:block;font-weight:500;text-transform:uppercase;letter-spacing:.06em;font-size:2.15mm}.ct span{display:block;color:#6E6258}
.fbox{font-size:3.15mm!important;line-height:1.36!important;overflow:hidden}
.fh{display:grid;grid-template-columns:1.5fr .8fr .8fr 1.1fr;gap:2mm;border-top:.45mm solid #3A2A22;border-bottom:.2mm solid #CDBFAE;
 padding:.5em 0 .55em;margin-bottom:.2em;font-size:1em}
.fh label{display:block;font-size:.66em;letter-spacing:.2em;text-transform:uppercase;color:#8C7462;margin-bottom:.15em}
.fh .rf{color:#6E2234;font-weight:500}.fh b{font-weight:500}
table.ft{font-size:.94em}table.ft th{width:25%;font-size:.7em;padding:.42em 2mm .42em 0;line-height:1.3}table.ft td{padding:.42em 0}
.dl{display:flex;gap:2mm}.dl .lb{color:#6E6258;flex:none;width:44%}.dl .dv{flex:1}
.chip{display:inline-block;width:4.4mm;height:2.8mm;vertical-align:-.3mm;margin-right:1mm;border:.15mm solid rgba(0,0,0,.25)}
table.bd{border-collapse:collapse;width:100%;font-size:2.45mm;line-height:1.36;table-layout:fixed}
table.bd th{text-align:left;font-weight:400;font-size:1.95mm;letter-spacing:.14em;text-transform:uppercase;color:#8C7462;
 border-bottom:.4mm solid #3A2A22;padding:1.4mm 1.2mm;vertical-align:bottom}
table.bd td{border-bottom:.2mm solid #CDBFAE;padding:1.6mm 1.2mm;vertical-align:top}
table.bd td.ref{font-weight:500;color:#6E2234}table.bd b{font-weight:500}
td.q{white-space:nowrap;text-align:right}td.ref{white-space:nowrap}
table.sy td,table.sy th{padding:.95mm 1.2mm;font-size:2.55mm}table.sy tr.grp td{font-weight:500;font-size:2.1mm;letter-spacing:.16em;
 text-transform:uppercase;color:#8C7462;padding-top:2.2mm;border-bottom:.3mm solid #8C7462}
table.sy2 td{font-size:2.7mm}tr.tot td{font-weight:500;border-top:.4mm solid #3A2A22}
table.pc td{font-size:2.6mm;padding:1.15mm 1.2mm;line-height:1.35}
.ed .st-v{font-weight:500}
"""


def main():
    BUILD.mkdir(exist_ok=True)
    shutil.rmtree(BUILD / "crops", ignore_errors=True)   # extracts are windows on the original files (no pixel crops)
    front()
    for si, (code, *_) in enumerate(F.ROOMS, 1):
        opener(si, code)
        for n, it in enumerate(F.ITEMS[code], 1):
            element(si, code, n, it)
        bordereau(si, code)
    synthesis()
    annexes()
    total = len(PAGES)
    out = []
    for i, pg in enumerate(PAGES, 1):
        body = toc_html(total) if pg["body"] == "__TOC__" else pg["body"]
        f = "" if pg["cls"] in ("p-cover", "p-back") else folio(pg, i, total)
        out.append(f'<section class="sheet ed {pg["cls"]}">{body}{f}</section>')
    css = (SB.X.VB.CSS + SB.ED_CSS + CSS).replace("FONTS/", FONTS.as_uri() + "/")
    doc = (f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>KAÏRA — Devis de fabrication du mobilier</title>'
           f'<style>{css}</style></head><body>{VD.PATTERNS}{"".join(out)}</body></html>')
    assert not re.search(r"(€|\bEUR\b|prix unitaire|\bHT\b|\bTTC\b|\d\s?euros?\b)", re.sub(r"<[^>]+>", " ", doc)), "price-like text found"
    out_html = BUILD / "devis-fabrication.html"
    out_html.write_text(doc, encoding="utf-8")
    print(total, "pages")
    js = f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage();
 await p.goto('file://{out_html}', {{ waitUntil: 'networkidle' }});
 await p.evaluate(() => document.fonts.ready);
 const fit = await p.evaluate(() => {{ const out = [];
  document.querySelectorAll('[data-fit]').forEach(el => {{
   const max = parseFloat(el.dataset.fit) * 96 / 25.4; let fs = 3.15;
   while (el.scrollHeight > max + 1 && fs > 2.1) {{ fs -= 0.05; el.style.setProperty('font-size', fs + 'mm', 'important'); }}
   out.push(fs.toFixed(2) + (el.scrollHeight > max + 1 ? ' OVERFLOW' : ''));
  }}); return out; }});
 console.log('fit', fit.join(' '));
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
