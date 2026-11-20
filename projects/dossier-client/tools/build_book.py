"""KAÏRA Interior Design — composition du dossier de conception (HTML -> PDF A4 paysage).

Sources : rendus et plans fournis par le studio (sources/), écrans TV éteints (build/tvoff/),
nuanciers relevés dans les rendus (build/swatches/). Aucune dimension ni référence n'est ajoutée :
les matières sont nommées de façon descriptive, telles qu'elles apparaissent dans les rendus.
"""
import json, pathlib, html
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / "build"
IMG = B / "img"; IMG.mkdir(parents=True, exist_ok=True)

PROJECT = "Villa — Rez-de-chaussée & Étage 1"     # à remplacer par le nom officiel du projet
DATE = "Novembre 2026"


def img(rel):
    """Copie la source (version TV éteinte si elle existe) en JPEG haute qualité ; renvoie le chemin relatif."""
    src = ROOT / "sources" / rel
    off = B / "tvoff" / src.name
    if off.exists():
        src = off
    out = IMG / (src.stem + ".jpg")
    if not out.exists():
        im = Image.open(src).convert("RGB")
        im.save(out, quality=90, optimize=True, progressive=True)
    return "img/" + out.name


R = "01-rdc-salon-principal/rdc-salon-%02d.png"
A = "02-chambre-amis/chambre-amis-%02d.png"
P = "03-chambre-principale/chambre-principale-%02d.png"
E = "04-etage1-sejour/etage1-sejour-%02d.png"
SW = json.loads((B / "swatches/swatches.json").read_text())

pages = []
toc = []


def tile(src, cls="", pos="50% 50%", zoom=None, caption=None):
    size = f"background-size:{zoom}%;" if zoom else ""
    cap = f'<figcaption>{caption}</figcaption>' if caption else ""
    return f'<figure class="tile {cls}"><div class="ph" style="background-image:url({src});background-position:{pos};{size}"></div>{cap}</figure>'


FOL = {"split": (14, 132), "concept": (116, 14), "opener": (14, 164), "feature": (214, 11), "synth": (166, 18), "toc": (132, 20)}


def page(body, cls="", folio=True, section="", fol=(14, 14)):
    pages.append((body, cls, folio, section, fol))


def palette_block(room, title):
    items = [s for s in SW if s["room"] == room]
    cells = "".join(
        f'<div class="sw"><div class="chip" style="background-image:url({s["img"]})"></div>'
        f'<div class="flat" style="background:{s["hex"]}"></div>'
        f'<div class="swname">{html.escape(s["name"])}</div><div class="hex">{s["hex"]}</div></div>' for s in items)
    return f'<div class="palette"><div class="kicker">{title}</div><div class="swgrid n{len(items)}">{cells}</div></div>'


# ---------------------------------------------------------------- COUVERTURE
page(f"""
<div class="cover">
  {tile(img(R % 2), "cover-img", "45% 60%")}
  <div class="cover-panel">
    <div class="brand"><div class="wordmark">KAÏRA</div><div class="sub">INTERIOR DESIGN</div></div>
    <div class="cover-title">
      <div class="kicker">Dossier de conception<br>et d'aménagement intérieur</div>
      <h1>Interior Design<br><em>Project Book</em></h1>
      <div class="rule"></div>
      <p class="proj">{PROJECT}</p>
    </div>
    <div class="cover-foot">{DATE}</div>
  </div>
</div>""", "p-cover", folio=False)

# ---------------------------------------------------------------- SOMMAIRE (rempli à la fin)
page("__TOC__", "p-toc", section="Sommaire")

# ---------------------------------------------------------------- 01 PROJET & CONCEPT
toc.append(("01", "Le projet et son concept"))
page(f"""
<div class="split">
  <div class="col-text">
    <div class="num">01</div>
    <div class="kicker">Le projet</div>
    <h2>Une demeure pensée comme<br><em>un écrin de calme</em></h2>
    <p class="lead">Ce dossier présente l'aménagement intérieur de quatre espaces de la villa : au rez-de-chaussée,
    le salon principal ouvert sur la salle à manger et la chambre d'amis ; à l'étage, le séjour et la chambre principale.</p>
    <p>Chaque pièce est traitée comme une composition à part entière, tout en partageant un même vocabulaire :
    des parois rythmées par des panneaux à joints creux, la chaleur du bois, la présence ponctuelle de la pierre,
    une lumière indirecte qui dessine les volumes et des œuvres d'art qui donnent à chaque espace son caractère.</p>
    <div class="facts">
      <div><span>Niveaux</span>Rez-de-chaussée · Étage 1</div>
      <div><span>Espaces</span>Salon principal · Salle à manger · Chambre d'amis · Séjour · Chambre principale</div>
    </div>
  </div>
  {tile(img(R % 11), "col-img", "50% 55%")}
</div>""", section="Le projet", fol=FOL["split"])

page(f"""
<div class="concept">
  {tile(img(P % 5), "concept-img", "50% 40%")}
  <div class="concept-text">
    <div class="kicker">Concept architectural et intention esthétique</div>
    <h2>Lumière, matière,<br><em>sérénité</em></h2>
    <div class="pillars">
      <div><b>La lumière comme architecture</b><p>Des gorges lumineuses soulignent le périmètre des plafonds ; les niches, les lames
      de bois et les panneaux de pierre sont rétroéclairés. La lumière indirecte crée une atmosphère enveloppante, sans éblouissement.</p></div>
      <div><b>Des parois composées</b><p>Panneaux muraux à joints creux, colonnes de bois et bandes de lames verticales
      structurent les murs et donnent aux pièces leur rythme et leur hauteur.</p></div>
      <div><b>Une matière naturelle et chaleureuse</b><p>Le bois, la pierre aux veinages marqués, les textiles doux et
      les tapis clairs composent une palette tactile, dans des tons neutres et chauds.</p></div>
      <div><b>L'art comme point focal</b><p>Chaque espace s'articule autour d'une œuvre ou d'un mur signature
      qui apporte une note de couleur et de personnalité.</p></div>
    </div>
  </div>
</div>""", section="Concept", fol=FOL["concept"])

# ---------------------------------------------------------------- 02 MOODBOARD
toc.append(("02", "Moodboard et univers"))
page(f"""
<div class="mood">
  <div class="mood-head"><div class="num">02</div><div><div class="kicker">Moodboard</div><h2>L'univers <em>du projet</em></h2></div></div>
  <div class="mood-grid">
    {tile(img(R % 9), "m1", "20% 45%")}
    {tile(img(A % 2), "m2", "62% 6%", 300)}
    {tile(img(P % 5), "m3", "52% 30%", 300)}
    {tile(img(E % 8), "m4", "62% 45%", 220)}
    {tile(img(R % 8), "m5", "45% 62%", 230)}
    {tile(img(R % 1), "m6", "36% 52%", 230)}
    {tile(img(E % 3), "m7", "20% 82%", 260)}
    {tile(img(R % 5), "m8", "40% 30%", 190)}
  </div>
</div>""", section="Moodboard")

# ---------------------------------------------------------------- 03 PALETTE GÉNÉRALE
toc.append(("03", "Palette chromatique et matières"))
glob_sel = ["Panneaux muraux crème", "Chêne clair — panneaux et colonnes", "Parquet bois", "Bois foncé — double porte",
            "Travertin — table à manger", "Marbre blanc veiné caramel", "Marbre brun foncé veiné", "Cuir taupe foncé — canapé",
            "Rideaux taupe", "Kaki — linge de lit", "Cuir cognac — pouf", "Rouge — œuvre"]
gl = [next(s for s in SW if s["name"] == n) for n in glob_sel]
bars = "".join(f'<div class="bar" style="background:{s["hex"]}"><span>{s["hex"]}</span></div>' for s in gl)
names = "".join(f'<div class="bn"><span class="bhex">{s["hex"]}</span>{html.escape(s["name"])}</div>' for s in gl)
page(f"""
<div class="palette-page">
  <div class="pp-head"><div class="num">03</div><div><div class="kicker">Palette chromatique</div>
  <h2>Les couleurs <em>du projet</em></h2>
  <p class="note">Teintes relevées directement dans les rendus du projet (valeur médiane de chaque matière, codes HEX).
  Elles restent à confirmer sur échantillons physiques.</p></div></div>
  <div class="bars">{bars}</div>
  <div class="bnames">{names}</div>
</div>""", section="Palette")

mat_sel = ["Chêne clair — panneaux et colonnes", "Lames chêne", "Parquet bois", "Bois foncé — double porte",
           "Marbre blanc veiné caramel", "Marbre blanc veiné — colonne", "Marbre brun foncé veiné", "Travertin — table à manger",
           "Bouclé — chaises", "Cuir taupe foncé — canapé", "Cuir cognac — pouf", "Tapis tissé"]
ms = [next(s for s in SW if s["name"] == n) for n in mat_sel]
cells = "".join(f'<div class="mat"><div class="mchip" style="background-image:url({s["img"]})"></div>'
                f'<div class="mname">{html.escape(s["name"])}</div><div class="hex">{s["hex"]}</div></div>' for s in ms)
page(f"""
<div class="mat-page">
  <div class="pp-head"><div class="num">03</div><div><div class="kicker">Palette de matériaux et de finitions</div>
  <h2>Bois, pierres <em>et textiles</em></h2>
  <p class="note">Échantillons extraits des rendus. Les références fournisseurs, essences, finitions et formats
  seront précisés dans le cahier des prescriptions.</p></div></div>
  <div class="matgrid">{cells}</div>
</div>""", section="Matériaux")

# ---------------------------------------------------------------- 04 PLANS
toc.append(("04", "Plans d'aménagement"))
page(f"""
<div class="plans">
  <div class="plans-head"><div class="num">04</div><div><div class="kicker">Plans d'aménagement</div><h2>Rez-de-chaussée</h2></div></div>
  <div class="plan-box"><img src="{img('plans/plan-rdc-amenagement.png')}"></div>
  <div class="legend"><b>Rez-de-chaussée</b><span>Salon principal</span><span>Salle à manger</span><span>Chambre d'amis</span></div>
</div>""", section="Plans")
page(f"""
<div class="plans">
  <div class="plans-head"><div class="num">04</div><div><div class="kicker">Plans d'aménagement</div><h2>Étage 1</h2></div></div>
  <div class="plan-box"><img src="{img('plans/plan-etage1-amenagement.png')}"></div>
  <div class="legend"><b>Étage 1</b><span>Séjour</span><span>Chambre principale</span></div>
</div>""", section="Plans")
page(f"""
<div class="plans tech">
  <div class="plans-head"><div class="num">04</div><div><div class="kicker">Plan technique</div><h2>Rez-de-chaussée <em>— plan coté</em></h2></div></div>
  <div class="plan-box white"><img src="{img('plans/plan-rdc-cote-2D.png')}"></div>
  <div class="legend"><b>Cotes en centimètres</b><span>Plan d'architecture existant</span></div>
</div>""", section="Plans")


# ---------------------------------------------------------------- ESPACES
def opener(num, level, title, em, text, hero, pos="50% 50%"):
    toc.append((num, f"{title} {em}".strip()))
    page(f"""
<div class="opener">
  <div class="op-text">
    <div class="num big">{num}</div>
    <div class="kicker">{level}</div>
    <h2 class="xl">{title}<br><em>{em}</em></h2>
    <div class="rule"></div>
    <p>{text}</p>
  </div>
  {tile(img(hero), "op-img", pos)}
</div>""", section=f"{title} {em}", fol=FOL["opener"])


def gallery3(section, kicker, title, srcs, caps, text=None, poss=None):
    poss = poss or ["50% 50%"] * 3
    t = "".join(tile(img(s), "g3", p, caption=c) for s, c, p in zip(srcs, caps, poss))
    intro = f'<p class="gintro">{text}</p>' if text else ""
    page(f"""<div class="gal"><div class="g-head"><div class="kicker">{kicker}</div><h3>{title}</h3>{intro}</div>
<div class="g3row">{t}</div></div>""", section=section)


def feature(section, kicker, title, big, small, caps, text, items, posb="50% 50%", poss="50% 50%"):
    li = "".join(f"<li>{i}</li>" for i in items)
    page(f"""
<div class="feature">
  {tile(img(big), "f-big", posb, caption=caps[0])}
  {tile(img(small), "f-small", poss, caption=caps[1])}
  <div class="f-text"><div class="kicker">{kicker}</div><h3>{title}</h3><p>{text}</p><ul>{li}</ul></div>
</div>""", section=section, fol=FOL["feature"])


def room_sheet(section, room, title, colors_title, mobilier, details, src_detail, pos):
    li = "".join(f"<li>{i}</li>" for i in mobilier)
    dl = "".join(f"<li>{i}</li>" for i in details)
    page(f"""
<div class="sheet">
  <div class="sh-left">
    <div class="kicker">{section}</div><h3>{title}</h3>
    {palette_block(room, colors_title)}
  </div>
  <div class="sh-right">
    {tile(img(src_detail), "sh-img", pos, 240)}
    <div class="lists"><div><div class="kicker">Mobilier et aménagement</div><ul>{li}</ul></div>
    <div><div class="kicker">Détails architecturaux</div><ul>{dl}</ul></div></div>
  </div>
</div>""", section=section)


# --- 05 SALON PRINCIPAL RDC
S1 = "Salon principal"
opener("05", "Rez-de-chaussée", "Salon", "principal",
       "Un grand espace de réception ouvert, où le salon, la salle à manger et la bibliothèque se répondent. "
       "Les murs sont rythmés par des panneaux crème et des colonnes de bois rétroéclairées ; une gorge lumineuse "
       "court le long du plafond et unifie l'ensemble.", R % 2, "40% 60%")
gallery3(S1, "Salon", "Un salon composé autour de l'art",
         [R % 11, R % 8, R % 3],
         ["Mur signature : œuvre graphique entre deux rideaux", "Colonnes de bois et lames rétroéclairées", "Mur TV et baie vitrée"],
         "Deux canapés modulaires bas — l'un en cuir taupe foncé, l'autre crème — se font face autour d'une table basse "
         "en bois noir et pierre veinée, posés sur un grand tapis clair.")
feature(S1, "Mur TV", "Un mur sculpté par la lumière", R % 7, R % 4,
        ["Vue frontale", "Vue en perspective"],
        "Le mur TV associe des panneaux de bois aux angles arrondis, une bande de lames verticales et des niches lumineuses. "
        "Le meuble bas suspendu laqué blanc libère le sol et allège la composition.",
        ["Panneaux bois aux angles arrondis, rétroéclairés", "Bande de lames verticales", "Niches éclairées", "Meuble bas suspendu blanc"],
        "45% 55%", "40% 55%")
gallery3(S1, "Salle à manger", "Recevoir sous une ligne de lumière",
         [R % 5, R % 9, R % 6],
         ["Table en pierre et pied cannelé", "Bibliothèque en bois et œuvre rouge", "Mur d'art et olivier"],
         "Une grande table en pierre claire accueille huit chaises en bouclé à structure en bois foncé. "
         "Au-dessus, une suspension lumineuse aux courbes libres dessine un trait de lumière.")
feature(S1, "Transitions", "Seuils et circulations", R % 1, R % 10,
        ["Colonne en marbre veiné, console et sculpture", "Double porte en bois foncé"],
        "Les passages entre les espaces sont traités comme des scènes : une colonne de marbre veiné porte une console "
        "et une sculpture, la bibliothèque asymétrique en bois se prolonge jusqu'au plafond.",
        ["Bibliothèque asymétrique en bois", "Colonne et console en marbre veiné", "Double porte en bois foncé",
         "Plafond à caissons séparés par un profil noir"], "50% 50%", "60% 50%")
room_sheet(S1, "rdc", "Couleurs et matières", "Nuancier — salon principal",
           ["Canapés modulaires cuir taupe foncé et crème", "Table basse bois noir et pierre veinée", "Grand tapis clair",
            "Table à manger en pierre, pied cannelé", "Chaises bouclé, structure bois foncé", "Suspension lumineuse sculpturale",
            "Rideaux taupe et voilages"],
           ["Gorge lumineuse périphérique au plafond", "Panneaux muraux à joints creux", "Colonnes de bois avec lames rétroéclairées",
            "Mur TV en bois aux angles arrondis", "Bibliothèques intégrées"], R % 8, "55% 65%")

# --- 06 CHAMBRE D'AMIS
S2 = "Chambre d'amis"
opener("06", "Rez-de-chaussée", "Chambre", "d'amis",
       "Une chambre lumineuse et douce, entre tons clairs et touches de bois. Le mur de tête de lit joue la sobriété ; "
       "le mur opposé réunit un habillage de marbre blanc veiné, le meuble TV et une coiffeuse.", A % 3, "45% 50%")
gallery3(S2, "Chambre d'amis", "Douceur et clarté",
         [A % 1, A % 2, A % 4],
         ["Mur de tête de lit", "Marbre, meuble TV et coiffeuse", "Vue en perspective"],
         "Lit plateforme tapissé aux angles arrondis, suspensions globe, chevets ronds en métal noir ; face au lit, "
         "un meuble suspendu en bois à plateau de marbre se prolonge en coiffeuse.")
room_sheet(S2, "amis", "Couleurs et matières", "Nuancier — chambre d'amis",
           ["Lit plateforme tapissé, tête de lit double", "Chevets ronds en métal noir", "Suspensions globe opalin",
            "Meuble TV suspendu bois et marbre", "Coiffeuse et pouf capitonné cuir", "Rideaux taupe et voilage"],
           ["Habillage mural en marbre blanc veiné", "Bande de lames de bois verticales", "Panneaux muraux à joints creux",
            "Gorge lumineuse au plafond", "Miroir toute hauteur"], A % 3, "50% 62%")

# --- 07 SÉJOUR ÉTAGE 1
S3 = "Séjour — étage 1"
opener("07", "Étage 1", "Séjour", "de l'étage",
       "Un salon plus intime, baigné de lumière par de hautes fenêtres. Une grande œuvre graphique rouge et blanche "
       "répond à la bibliothèque éclairée ; les assises gris taupe et les accents cognac installent une atmosphère chaleureuse.",
       E % 4, "40% 50%")
gallery3(S3, "Séjour", "Un salon intime et lumineux",
         [E % 2, E % 3, E % 9],
         ["Vue vers les fenêtres", "Canapé, fauteuil et pouf", "Œuvre et bibliothèque"],
         "Canapé d'angle gris taupe, coussins pied-de-poule et cuir cognac, table basse ovale en marbre veiné associée à une "
         "table d'appoint en bois foncé, fauteuil à structure métallique et pouf en cuir cognac.")
feature(S3, "Mur TV et entrée", "Bois, lumière et seuils", E % 1, E % 8,
        ["Mur TV et étagère lumineuse", "Double porte en bois et bibliothèque"],
        "Le mur TV s'inscrit dans des panneaux crème à joints creux ; une étagère verticale en bois éclairée, "
        "rythmée par un montant de marbre, l'accompagne. La double porte en bois à fentes vitrées marque l'entrée.",
        ["Meuble bas suspendu en bois", "Étagère verticale éclairée", "Double porte en bois à fentes vitrées",
         "Bibliothèque éclairée toute hauteur"], "45% 55%", "45% 50%")
room_sheet(S3, "et1", "Couleurs et matières", "Nuancier — séjour",
           ["Canapé d'angle gris taupe", "Table basse ovale en marbre veiné", "Table d'appoint bois foncé et métal noir",
            "Fauteuil tissu, structure métal noir", "Pouf en cuir cognac", "Tapis tissé", "Rideaux taupe et voilages"],
           ["Gorge lumineuse au plafond", "Panneaux muraux à joints creux", "Bibliothèque éclairée", "Étagère avec montant en marbre"],
           E % 3, "15% 85%")

# --- 08 CHAMBRE PRINCIPALE
S4 = "Chambre principale"
opener("08", "Étage 1", "Chambre", "principale",
       "Une suite enveloppante construite autour d'une bande de marbre brun foncé rétroéclairée. La tête de lit aux formes "
       "arrondies, le linge kaki et les touches dorées composent une ambiance feutrée et précieuse.", P % 1, "50% 50%")
gallery3(S4, "Chambre principale", "Un écrin feutré",
         [P % 5, P % 3, P % 4],
         ["Mur de tête de lit", "Vue d'ensemble et baie vitrée", "Dressing et meuble TV"],
         "Grande tête de lit enveloppante, chevets en bois, suspensions globe à anneau doré, banc capitonné à piètement doré ; "
         "face au lit, un dressing en bois toute hauteur.")
room_sheet(S4, "princ", "Couleurs et matières", "Nuancier — chambre principale",
           ["Tête de lit enveloppante aux formes arrondies", "Chevets en bois à deux tiroirs", "Suspensions globe, anneau doré",
            "Banc capitonné, piètement doré", "Meuble TV noir", "Rideaux taupe et voilage"],
           ["Bande de marbre brun foncé rétroéclairée", "Colonnes de bois avec lames éclairées", "Miroirs verticaux",
            "Dressing en bois toute hauteur", "Gorge lumineuse au plafond"], P % 5, "50% 30%")

# ---------------------------------------------------------------- 09 AGENCEMENTS SUR MESURE
toc.append(("09", "Agencements et menuiseries"))
cust = [(R % 7, "45% 50%", 170, "Mur TV — salon principal", "Panneaux bois aux angles arrondis, lames et niches lumineuses"),
        (R % 1, "70% 40%", 160, "Bibliothèque — salle à manger", "Composition asymétrique en bois, toute hauteur"),
        (A % 2, "45% 70%", 170, "Meuble TV et coiffeuse — chambre d'amis", "Bois et plateau de marbre, suspendus"),
        (P % 4, "50% 40%", 150, "Dressing — chambre principale", "Façades bois toute hauteur, poignées intégrées"),
        (E % 8, "85% 45%", 170, "Bibliothèque — séjour", "Étagères éclairées en bois"),
        (P % 5, "50% 62%", 170, "Tête de lit — chambre principale", "Volume enveloppant aux formes arrondies")]
cc = "".join(tile(img(s), "c6", p, z, f"<b>{t}</b><br>{d}") for s, p, z, t, d in cust)
page(f"""
<div class="custom"><div class="g-head"><div class="num">09</div><div class="kicker">Agencements et menuiseries</div>
<h3>Le sur-mesure <em>au cœur du projet</em></h3>
<p class="gintro">Les menuiseries intégrées dessinent l'architecture intérieure de chaque pièce. Les plans de fabrication,
dimensions et finitions seront détaillés dans les dossiers d'exécution.</p></div>
<div class="c6grid">{cc}</div></div>""", section="Agencements")

# ---------------------------------------------------------------- 10 SYNTHÈSE
toc.append(("10", "Synthèse"))
page(f"""
<div class="synth">
  {tile(img(R % 5), "sy-img", "35% 50%")}
  <div class="sy-text">
    <div class="num">10</div><div class="kicker">Synthèse esthétique</div>
    <h2>Une écriture <em>cohérente</em>,<br>des pièces singulières</h2>
    <p>Du salon de réception à la chambre principale, le projet décline un même langage : des parois composées,
    la chaleur du bois, la profondeur de la pierre et une lumière indirecte omniprésente.</p>
    <p>Chaque espace affirme ensuite sa propre identité — l'art au salon, le marbre clair dans la chambre d'amis,
    la couleur au séjour de l'étage, la pierre sombre et le kaki dans la chambre principale — pour une demeure à la fois
    unifiée et vivante.</p>
  </div>
</div>""", section="Synthèse", fol=FOL["synth"])

# ---------------------------------------------------------------- DOS
page(f"""
<div class="back">
  {tile(img(P % 5), "back-img", "50% 35%")}
  <div class="back-panel"><div class="wordmark">KAÏRA</div><div class="sub">INTERIOR DESIGN</div>
  <div class="rule"></div><p>{PROJECT}<br>{DATE}</p></div>
</div>""", "p-back", folio=False)

# ---------------------------------------------------------------- SOMMAIRE
toc_html = "".join(f'<div class="toc-row"><span class="tn">{n}</span><span class="tt">{html.escape(t)}</span></div>' for n, t in toc)
pages[1] = (f"""
<div class="toc">
  {tile(img(E % 4), "toc-img", "30% 50%")}
  <div class="toc-text"><div class="kicker">Sommaire</div><h2>Contenu <em>du dossier</em></h2><div class="toc-list">{toc_html}</div></div>
</div>""", "p-toc", True, "Sommaire", FOL["toc"])

# ---------------------------------------------------------------- HTML
CSS = (ROOT / "tools/book.css").read_text()
body = []
for i, (b, cls, folio, section, fol) in enumerate(pages, 1):
    narrow = " narrow" if 297 - fol[0] - fol[1] < 150 else ""
    brand = "KAÏRA" if narrow else "KAÏRA Interior Design · Dossier de conception"
    f = (f'<div class="folio{narrow}" style="left:{fol[0]}mm;right:{fol[1]}mm"><span>{brand}</span>'
         f'<span>{html.escape(section)}</span><span class="pn">{i:02d}</span></div>') if folio else ""
    body.append(f'<section class="page {cls}">{b}{f}</section>')
doc = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>KAÏRA — Dossier de conception</title>
<style>{CSS}</style></head><body>{''.join(body)}</body></html>"""
(B / "dossier.html").write_text(doc, encoding="utf-8")
print("pages:", len(pages))
