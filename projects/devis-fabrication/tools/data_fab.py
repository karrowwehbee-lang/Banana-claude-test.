"""Villa KAÏRA — devis descriptif et quantitatif de fabrication du mobilier (données). AUCUN PRIX.

Sources : dossier technique de la villa (projects/dossier-technique/tools/data.py : élévations, mobilier M1–M13,
matériaux, cotes avec statut), dossier de la douche principale (projects/dossier-douche-etage1/tools : geom, palette),
rendus 3D du projet. Statuts des cotes : 'v' cote écrite sur un plan source, 'd' ≈ relevée, 'c' DIMENSION À CONFIRMER.
Aucune dimension, aucun matériau ni aucune référence commerciale n'est inventé.
"""
import pathlib

from surfaces import D, wall

REPO = pathlib.Path(__file__).resolve().parents[3]
VS = REPO / "projects/dossier-client/sources"
DS = REPO / "projects/dossier-douche-etage1/sources"
FOLD = {"rdc-salon": "01-rdc-salon-principal", "chambre-amis": "02-chambre-amis",
        "chambre-principale": "03-chambre-principale", "etage1-sejour": "04-etage1-sejour"}


def R(name):
    """Path of a render: villa name (e.g. 'rdc-salon-07') or shower file number ('DPE-06')."""
    if name.startswith("DPE-"):
        return DS / f"{name[4:]}.png"
    for k, f in FOLD.items():
        if name.startswith(k):
            return VS / f / f"{name}.png"
    raise KeyError(name)


SA = "SUPPORT À CONFIRMER (type de panneau, épaisseur, qualité hydrofuge le cas échéant)"
FA = "FINITION À CONFIRMER"
NC = "À CONFIRMER"


def it(ref, name, cat, qty, unit, dims, mat, finish, img, elev, refs, *, support=SA, revet="—", facades="—",
       handles="—", opening="—", light="Aucun éclairage intégré visible sur les rendus.", fab="—", pose="—", obs="—",
       short=None, qty_note=""):
    return dict(ref=ref, name=name, cat=cat, qty=qty, unit=unit, dims=dims, mat=mat, finish=finish, img=img, elev=elev,
                refs=refs, support=support, revet=revet, facades=facades, handles=handles, opening=opening, light=light,
                fab=fab, pose=pose, obs=obs, short=short or name, qty_note=qty_note)


def S(room, walls, key="panneau"):
    """Sum of a finish over walls (m², ≈) + notes on openings to deduct / walls without a frontal render."""
    tot, parts, notes = 0.0, [], []
    for w in walls:
        s, unknown, sparse, W, H = wall(room, w)
        v = s.get(key, 0.0)
        if v <= 0:
            continue
        tot += v
        parts.append(f"mur {w} ≈ {v:.2f}".replace(".", ","))
        if unknown:
            notes.append(f"mur {w} : {', '.join(n for n, _ in unknown)} à déduire (hauteurs à confirmer)")
        if sparse:
            notes.append(f"mur {w} : sans rendu de face — nature du revêtement et ouvertures à confirmer")
    return round(tot, 2), parts, notes


def m2(v):
    return f"≈ {v:.2f} m²".replace(".", ",")


ROOMS = [   # code, name, level, villa room key (plan) or 'dpe', opener render, elevation sheets
    ("SAL", "Salon principal", "Rez-de-chaussée", "sejour", "rdc-salon-07", "KAI-VIL-201 · 204 · 205 · 208 · 209 · 210"),
    ("SAM", "Espace salle à manger", "Rez-de-chaussée", "sejour", "rdc-salon-05", "KAI-VIL-202 · 203 · 208 · 210"),
    ("AMI", "Chambre d'amis", "Rez-de-chaussée", "amis", "chambre-amis-02", "KAI-VIL-301 à 307"),
    ("SEJ", "Séjour", "Étage 1", "etsejour", "etage1-sejour-01", "KAI-VIL-401 à 406"),
    ("CHP", "Chambre principale", "Étage 1", "princ", "chambre-principale-05", "KAI-VIL-501 à 506"),
    ("DPE", "Douche principale", "Étage 1", "dpe", "DPE-01", "KAI-DPE-501 à 514"),
]

ITEMS = {}

# ================================================================ SALON PRINCIPAL
p_sal, parts_sal, notes_sal = S("sejour", ["A", "D2", "E"])
ITEMS["SAL"] = [
    it("SAL-01", "Meuble TV suspendu laqué crème", "Meuble TV", 1, "pce",
       [("Longueur", 259, "d"), ("Profondeur", 32, "d"), ("Hauteur", 34, "d"), ("Hauteur sous meuble (pose)", 20, "d")],
       "Laque crème (teinte relevée #A1988F)", "Laque crème — brillance : " + FA, ("rdc-salon-07", (320, 1060, 960, 1200)),
       ("sejour", "A", (110, 385, 0, 70)), "Rendus rdc-salon-03, -04, -07 · Élévation A (KAI-VIL-201) · KAI-VIL-208",
       facades="3 façades affleurantes de largeurs inégales : ≈ 69 / ≈ 128 / ≈ 62 (joints à ≈ 186,8 et ≈ 315,0 depuis l'angle ouest du mur A)",
       handles="Aucune poignée visible — système sans poignée : " + NC,
       opening="Type d'ouverture (portes, abattants ou tiroirs) : " + NC,
       light="Rétroéclairage sous le meuble : " + NC,
       fab="Caisson suspendu, façades en léger retrait du plateau ; aménagement intérieur : " + NC,
       pose="Suspendu, fixé au mur A (fixation à définir par l'atelier) ; dessous à ≈ 20 du sol fini ; passage de câbles vers le téléviseur",
       obs="Téléviseur exclu (fourni séparément). Le meuble et son passage de câbles sont inclus.",
       short="Meuble suspendu laqué, 3 façades"),
    it("SAL-02", "Colonne cannelée du mur TV", "Habillage mural", 1, "pce",
       [("Largeur", 55.2, "d"), ("Hauteur (sol → plafond)", 284, "d"), ("Profondeur / saillie", None, "c")],
       "Lames cannelées verticales (teinte relevée #766759) — matière : " + FA, FA,
       ("rdc-salon-07", (360, 540, 520, 1200)), ("sejour", "A", (95, 200, 0, 284)),
       "Rendus rdc-salon-03, -04, -07 · Élévation A (KAI-VIL-201) · KAI-VIL-208 (ensemble M2)",
       revet="Cannelures verticales — pas et profil des cannelures : " + NC,
       fab="Partie de l'ensemble mur TV (M2). Le panneau chêne arrondi SAL-04 vient en applique devant la colonne entre ≈ 60,7 et ≈ 225,2.",
       pose="Fixée au mur A, toute hauteur", short="Colonne cannelée toute hauteur"),
    it("SAL-03", "Bande miroir verticale du mur TV", "Habillage mural", 1, "pce",
       [("Largeur", 18.3, "d"), ("Hauteur (sol → plafond)", 284, "d"), ("Épaisseur", None, "c")],
       "Miroir — teinte (clair, bronze, fumé) : " + FA, FA, ("rdc-salon-07", (300, 540, 400, 1200)),
       ("sejour", "A", (95, 130, 0, 284)), "Rendu rdc-salon-07 · Élévation A (KAI-VIL-201) · ensemble M2",
       fab="Bande d'un seul tenant ou en plusieurs éléments : " + NC + " ; chants polis",
       pose="Collée ou fixée sur le mur A, entre la colonne chêne et la colonne cannelée", short="Miroir toute hauteur ≈ 18 de large"),
    it("SAL-04", "Panneaux chêne arrondis rétroéclairés du mur TV", "Habillage mural", 2, "pce",
       [("Panneau gauche — largeur", 55.2, "d"), ("Panneau droit — largeur", 155.3, "d"), ("Hauteur des deux panneaux", 164.5, "d"),
        ("Bas des panneaux (depuis le sol)", 60.7, "d"), ("Épaisseur / saillie", None, "c"), ("Rayon des angles", None, "c"),
        ("Réservation téléviseur", "≈ 167,2 × ≈ 92,8 (bas à ≈ 86,4)", "d")],
       "Chêne clair (teinte relevée #6A5442) — essence, massif ou placage : " + FA, FA,
       ("rdc-salon-07", (360, 680, 890, 1070)), ("sejour", "A", (115, 355, 50, 235)),
       "Rendus rdc-salon-03, -04, -07 · Élévation A (KAI-VIL-201) · KAI-VIL-208 (ensemble M2)",
       facades="Panneau gauche : angles arrondis côté droit ; panneau droit : angles arrondis côté gauche (les deux panneaux se font face)",
       light="Rétroéclairage LED périphérique des deux panneaux (≈ 10,8 ml si sur tout le périmètre : " + NC + ") + ligne LED verticale "
             "≈ 284 à ≈ 177,4 de l'angle du mur. Profilés, température de couleur, alimentation : " + NC,
       fab="Panneaux décollés du mur pour le halo lumineux ; support et fixation du téléviseur à intégrer dans le panneau droit (support TV : " + NC + ")",
       pose="En applique sur le mur A et sur la colonne cannelée SAL-02", obs="Téléviseur exclu ; son support et sa réservation sont inclus.",
       short="2 panneaux chêne arrondis, rétroéclairés"),
    it("SAL-05", "Colonne laquée à niches éclairées", "Rangement / niches", 1, "pce",
       [("Largeur", 34.9, "d"), ("Hauteur", 230.3, "d"), ("Départ (depuis le sol)", 53.7, "d"), ("Profondeur", None, "c"),
        ("Niches (×3) — largeur", 25.7, "d"), ("Niches — hauteurs", "≈ 31,2 / ≈ 34,5 / ≈ 37,7", "d")],
       "Laque crème (teinte relevée #A1988F)", "Laque — brillance : " + FA, ("rdc-salon-07", (850, 540, 960, 1100)),
       ("sejour", "A", (340, 390, 40, 284)), "Rendus rdc-salon-03, -07 · Élévation A (KAI-VIL-201) · ensemble M2",
       facades="Trois niches ouvertes superposées (bas à ≈ 117,2 / ≈ 151,6 / ≈ 188,4)",
       light="Éclairage LED dans chacune des 3 niches — position (haut ou côtés) et profilé : " + NC,
       fab="Colonne posée sur le meuble TV SAL-01 jusqu'au plafond", pose="Fixée au mur A", short="Colonne laquée, 3 niches éclairées"),
    it("SAL-06", "Colonnes chêne du mur A", "Habillage mural", 2, "pce",
       [("Colonne ouest — largeur", 58.8, "d"), ("Colonne est — largeur", 49.7, "d"), ("Hauteur", 284, "d"),
        ("Joint horizontal à", 224.2, "d"), ("Épaisseur", None, "c"), ("Surface totale", m2(3.07), "d")],
       "Chêne clair (teinte relevée #6A5442) — essence, massif ou placage : " + FA, FA, ("rdc-salon-07", (180, 520, 370, 1210)),
       ("sejour", "A", (35, 110, 0, 284)), "Rendus rdc-salon-03, -07 · Élévation A (KAI-VIL-201)",
       facades="Chaque colonne en 2 panneaux superposés (joint à ≈ 224,2)",
       pose="En applique sur le mur A : l'une à gauche du mur TV, l'autre à droite de la porte vitrée", short="2 colonnes chêne toute hauteur"),
    it("SAL-07", "Colonnes chêne et soubassement cannelé éclairé (mur d'entrée)", "Habillage mural", 3, "pce",
       [("Largeurs", "≈ 60,6 / ≈ 61,7 / ≈ 62,4", "d"), ("Hauteur totale", 284, "d"), ("Partie basse cannelée (hauteur)", 105, "d"),
        ("Partie haute chêne pleine (hauteur)", 179, "d"), ("Entraxe", 140, "d"), ("Profondeur", None, "c"),
        ("Surfaces", "chêne ≈ 3,60 m² · cannelures ≈ 1,94 m²", "d")],
       "Chêne clair + lames cannelées — essence : " + FA, FA, ("rdc-salon-08", (540, 420, 1560, 1260)),
       ("sejour", "D2", (175, 535, 0, 284)), "Rendus rdc-salon-02, -08, -10 · Élévation D2 (KAI-VIL-204) · KAI-VIL-209 (M5)",
       light="Ligne LED horizontale à ≈ 105, en haut de la partie cannelée (≈ 1,85 ml pour les 3 colonnes) — profilé : " + NC,
       fab="Partie basse : cannelures verticales ; partie haute : panneau chêne plein ; LED entre les deux",
       pose="En applique sur le mur D2, à droite de la porte d'entrée", short="3 colonnes chêne, bas cannelé éclairé"),
    it("SAL-08", "Panneaux muraux crème à joints creux — salon", "Habillage mural", p_sal, "m²",
       [("Surface", m2(p_sal), "d"), ("Détail", " · ".join(parts_sal), "d"), ("Hauteur", 284, "d"),
        ("Joints creux — largeur, profondeur", None, "c")],
       "Panneaux crème (teinte relevée #978B80) — matériau : " + FA, FA, ("rdc-salon-11", (140, 380, 1560, 1500)),
       ("sejour", "E", None), "Rendus rdc-salon-02, -10, -11 · Élévations A, D2, E (KAI-VIL-201, 204, 205)",
       revet="Calepinage suivant les joints relevés sur les élévations (verticaux et horizontaux)",
       fab="Panneaux à joints creux ; découpes autour des fenêtres F1, F2 et de la porte d'entrée", pose="Fixés sur les murs A, D2 et E",
       obs="Surface brute déduite des zones déjà comptées (chêne, cannelures, miroir, porte). " + " ; ".join(notes_sal),
       short="Panneaux muraux crème, joints creux"),
    it("SAL-09", "Porte d'entrée deux vantaux, bois foncé", "Menuiserie", 1, "pce",
       [("Largeur (2 vantaux)", 163, "v"), ("Hauteur", 235, "d"), ("Épaisseur", None, "c")],
       "Bois foncé (teinte relevée #251B13) — essence : " + FA, FA, ("rdc-salon-10", (760, 560, 1440, 1500)),
       ("sejour", "D2", (0, 183.3, 0, 284)), "Rendus rdc-salon-08, -10 · Élévation D2 (KAI-VIL-204)",
       facades="Vantaux à rainures horizontales", handles="Deux béquilles métal argenté et serrure — modèles : " + NC,
       opening="Deux vantaux battants — sens d'ouverture : " + NC,
       obs="Menuiserie d'entrée : fabrication par l'atelier ou fourniture séparée " + NC + ".", short="Porte d'entrée 2 vantaux"),
]

# ================================================================ SALLE À MANGER
p_sam, parts_sam, notes_sam = S("sejour", ["B", "C", "D1"])
ITEMS["SAM"] = [
    it("SAM-01", "Bibliothèque chêne toute hauteur", "Rangement", 1, "pce",
       [("Longueur totale", 185, "d"), ("dont étagères ouvertes", 139.7, "d"), ("dont panneau plein (côté fenêtre)", 45, "d"),
        ("Profondeur", 23, "d"), ("Hauteur", 284, "d"), ("Épaisseur des montants et tablettes", None, "c")],
       "Chêne clair (teinte relevée #6A5442) — essence, massif ou placage : " + FA, FA, ("rdc-salon-09", (0, 200, 740, 1660)),
       ("sejour", "D1", (0, 190, 0, 284)), "Rendus rdc-salon-01, -05, -09 · Élévation D1 (KAI-VIL-203) · KAI-VIL-208 (M3)",
       facades="Étagères ouvertes asymétriques sur trois travées (rendu rdc-salon-09) ; panneau plein à joint horizontal côté fenêtre",
       opening="Sans porte (étagères ouvertes)", fab="Répartition et nombre des tablettes : selon le rendu rdc-salon-09 — cotes " + NC,
       pose="Posée au sol et fixée au mur D1, du sol au plafond", short="Bibliothèque chêne ouverte + panneau plein"),
    it("SAM-02", "Montants chêne toute hauteur", "Habillage mural", 3, "pce",
       [("Largeurs", "≈ 10,3 / ≈ 10,4 / ≈ 10,2", "d"), ("Hauteur", 284, "d"), ("Profondeur / saillie", None, "c"),
        ("Surface totale", m2(0.85), "d")],
       "Chêne clair — essence : " + FA, FA, ("rdc-salon-09", (1250, 240, 1390, 1420)),
       ("sejour", "D1", (290, 595, 0, 284)), "Rendus rdc-salon-05, -09, -10 · Élévation D1 (KAI-VIL-203)",
       pose="En applique sur le mur D1 : de part et d'autre de l'œuvre rouge et à droite de la fenêtre F3 (≈ 299,1 · ≈ 403,9 · ≈ 581,1 de l'angle)",
       short="3 montants chêne"),
    it("SAM-03", "Console murale et colonne marbre", "Console / meuble d'entrée", 1, "ens.",
       [("Console — longueur", 128, "d"), ("Console — profondeur", 30, "d"), ("Console — épaisseur et hauteur de pose", None, "c"),
        ("Colonne — section et hauteur", None, "c")],
       "Console : " + FA + " (aspect clair mat sur le rendu rdc-salon-01) · colonne : marbre blanc veiné (teinte relevée #97887A)",
       FA, ("rdc-salon-01", (40, 380, 720, 1580)), ("sejour", "C", None),
       "Rendus rdc-salon-01, -05 · Élévation C (KAI-VIL-202) · KAI-VIL-208 (M4)",
       fab="Console en porte-à-faux appuyée sur une colonne en marbre ; calepinage et sens du veinage : " + NC,
       pose="Console fixée au mur C ; colonne posée au sol", short="Console + colonne marbre"),
    it("SAM-04", "Table de salle à manger", "Mobilier de salle à manger", 1, "pce",
       [("Longueur", 243, "d"), ("Largeur", 95, "d"), ("Hauteur", None, "c"), ("Épaisseur du plateau", None, "c"),
        ("Piètement — dimensions", None, "c")],
       "Plateau effet travertin (teinte relevée #C2BAB2) — matériau : " + FA + " · piètement central cannelé bois foncé : " + FA, FA,
       ("rdc-salon-05", (300, 980, 1000, 1400)), None, "Rendus rdc-salon-05, -09 · Plan d'aménagement RDC (KAI-VIL-101)",
       fab="Plateau rectangulaire sur piètement central cannelé", pose="Posée au sol",
       obs="Dimensions en plan relevées sur la vue de dessus. Fabrication par l'atelier ou achat : " + NC + ". Les 8 chaises sont achetées séparément.",
       short="Table plateau effet travertin, pied cannelé"),
    it("SAM-05", "Panneaux muraux crème à joints creux — salle à manger", "Habillage mural", p_sam, "m²",
       [("Surface", m2(p_sam), "d"), ("Détail", " · ".join(parts_sam), "d"), ("Hauteur", 284, "d"),
        ("Joints creux — largeur, profondeur", None, "c")],
       "Panneaux crème (teinte relevée #978B80) — matériau : " + FA, FA, ("rdc-salon-05", (1050, 380, 1667, 1500)),
       ("sejour", "D1", None), "Rendus rdc-salon-05, -06, -10 · Élévations B, C, D1 (KAI-VIL-202, 203)",
       revet="Calepinage suivant les joints relevés", fab="Découpes autour des fenêtres F3 et F4",
       pose="Fixés sur les murs B, C et D1",
       obs="Surface brute, déduction faite de la bibliothèque SAM-01, des montants et des fenêtres F3 / F4. " + " ; ".join(notes_sam),
       short="Panneaux muraux crème, joints creux"),
]

# ================================================================ CHAMBRE D'AMIS
p_ami, parts_ami, notes_ami = S("amis", ["A", "B", "C", "D"])
ITEMS["AMI"] = [
    it("AMI-01", "Meuble TV suspendu chêne, plateau marbre", "Meuble TV", 1, "pce",
       [("Longueur", 173.6, "d"), ("Profondeur", 39, "d"), ("Hauteur", 23.6, "d"), ("Hauteur sous meuble (pose)", 48.8, "d"),
        ("Épaisseur du plateau marbre", None, "c")],
       "Caisson et façades chêne (teinte relevée #6C503C) — essence : " + FA + " · plateau marbre blanc veiné", FA,
       ("chambre-amis-02", (580, 1120, 1620, 1320)), ("amis", "C", (100, 285, 40, 90)),
       "Rendus chambre-amis-02, -04 · Élévation C (KAI-VIL-303) · KAI-VIL-306 (M6)",
       facades="3 tiroirs en façade", handles="Aucune poignée visible — système : " + NC, opening="3 tiroirs — coulisses : " + NC,
       pose="Suspendu, fixé au mur C devant l'habillage marbre AMI-05", obs="Téléviseur exclu ; le meuble est inclus.",
       short="Meuble TV suspendu chêne, 3 tiroirs, plateau marbre"),
    it("AMI-02", "Coiffeuse suspendue chêne, plateau marbre", "Coiffeuse", 1, "pce",
       [("Longueur", 92.9, "d"), ("Profondeur", None, "c"), ("Hauteur du caisson", 18.3, "d"), ("Dessus du plateau", 85.7, "d"),
        ("Épaisseur du plateau marbre", None, "c")],
       "Chêne (teinte relevée #6C503C) — essence : " + FA + " · plateau marbre blanc veiné", FA,
       ("chambre-amis-02", (40, 1060, 640, 1230)), ("amis", "C", (10, 120, 55, 100)),
       "Rendus chambre-amis-02, -04 · Élévation C (KAI-VIL-303) · KAI-VIL-306 (M7)",
       facades="Façade de tiroir(s) — nombre : " + NC, handles="Aucune poignée visible — " + NC, opening="Tiroir(s) — " + NC,
       pose="Suspendue, fixée au mur C sous le miroir AMI-03", obs="Pouf et lampes de la coiffeuse : achat séparé.",
       short="Coiffeuse suspendue chêne, plateau marbre"),
    it("AMI-03", "Miroir de la coiffeuse, toute hauteur", "Habillage mural", 1, "pce",
       [("Largeur", 60.3, "d"), ("Hauteur", 209, "d"), ("Bas du miroir", 76, "d"), ("Épaisseur", None, "c")],
       "Miroir — teinte : " + FA, FA, ("chambre-amis-02", (220, 80, 560, 1090)), ("amis", "C", (10, 110, 60, 285)),
       "Rendus chambre-amis-02, -04 · Élévation C (KAI-VIL-303)", fab="Chants polis", pose="Collé ou fixé au mur C, entre les deux colonnes chêne AMI-04",
       short="Miroir ≈ 60 × 209"),
    it("AMI-04", "Colonnes chêne du mur TV", "Habillage mural", 2, "pce",
       [("Largeurs", "≈ 19,8 / ≈ 21,0", "d"), ("Hauteur", 285, "d"), ("Profondeur / saillie", None, "c"), ("Surface totale", m2(1.17), "d")],
       "Chêne (teinte relevée #6C503C) — essence : " + FA, FA, ("chambre-amis-02", (140, 90, 640, 1430)), ("amis", "C", (0, 105, 0, 285)),
       "Rendus chambre-amis-02, -04 · Élévation C (KAI-VIL-303)", pose="En applique sur le mur C, de part et d'autre du miroir AMI-03",
       short="2 colonnes chêne toute hauteur"),
    it("AMI-05", "Habillage marbre blanc veiné caramel — mur TV", "Habillage mural", 3.42, "m²",
       [("Largeur", 120.5, "d"), ("Hauteur", 285, "d"), ("Surface", m2(3.42), "d"), ("Épaisseur", None, "c")],
       "Marbre blanc veiné caramel (teinte relevée #B6AFA9) — référence : " + FA, "Finition (poli, adouci) : " + FA,
       ("chambre-amis-02", (780, 80, 1370, 1430)), ("amis", "C", (130, 270, 0, 285)),
       "Rendus chambre-amis-02, -04 · Élévation C (KAI-VIL-303)",
       revet="Calepinage (nombre de dalles, joints, sens du veinage) : " + NC,
       fab="Découpes pour le passage des câbles du téléviseur et la fixation de son support (support TV : " + NC + ")",
       pose="Collé ou agrafé sur le mur C, toute hauteur, derrière le meuble TV AMI-01", obs="Téléviseur exclu.",
       short="Habillage marbre toute hauteur"),
    it("AMI-06", "Lames chêne verticales — mur tête de lit", "Habillage mural", 1, "pce",
       [("Largeur", 34.9, "d"), ("Hauteur", 285, "d"), ("Surface", m2(1.0), "d"), ("Pas et section des lames", None, "c")],
       "Lames chêne (teinte relevée #82624B) — essence : " + FA, FA, ("chambre-amis-01", (300, 80, 520, 1460)),
       ("amis", "A", (45, 95, 0, 285)), "Rendus chambre-amis-01, -03 · Élévation A (KAI-VIL-301)",
       pose="En applique sur le mur A, toute hauteur, à gauche de la tête de lit", short="Bande de lames chêne toute hauteur"),
    it("AMI-07", "Fente miroir verticale — mur tête de lit", "Habillage mural", 1, "pce",
       [("Largeur", 5.6, "d"), ("Hauteur", 229.6, "d"), ("Bas du miroir", 55.4, "d"), ("Épaisseur", None, "c")],
       "Miroir — teinte : " + FA, FA, ("chambre-amis-01", (1120, 400, 1260, 1200)), ("amis", "A", (220, 245, 40, 285)),
       "Rendu chambre-amis-01 · Élévation A (KAI-VIL-301)", fab="Encastrement dans les panneaux muraux (fente) : " + NC,
       pose="Mur A, à droite de la tête de lit", short="Fente miroir ≈ 6 × 230"),
    it("AMI-08", "Panneaux muraux beige — chambre d'amis", "Habillage mural", p_ami, "m²",
       [("Surface", m2(p_ami), "d"), ("Détail", " · ".join(parts_ami), "d"), ("Hauteur", 285, "d"),
        ("Joints — largeur, profondeur", None, "c")],
       "Panneaux beige (teinte relevée #A1968E) — matériau : " + FA, FA, ("chambre-amis-01", (0, 0, 1667, 1480)), ("amis", "A", None),
       "Rendus chambre-amis-01 à -04 · Élévations A à D (KAI-VIL-301 à 304)",
       revet="Joint horizontal à ≈ 40,6 sur le mur A ; autres joints suivant les élévations", fab="Découpes autour de la fenêtre F5 et de l'ouverture de l'alcôve",
       pose="Fixés sur les murs A, B, C et D",
       obs="Surface brute, déduction faite des zones chêne, marbre, miroir et lames. " + " ; ".join(notes_ami),
       short="Panneaux muraux beige"),
]

# ================================================================ SÉJOUR ÉTAGE 1
p_sej, parts_sej, notes_sej = S("etsejour", ["A", "B", "C", "D"])
ITEMS["SEJ"] = [
    it("SEJ-01", "Meuble TV suspendu chêne", "Meuble TV", 1, "pce",
       [("Longueur", 281.6, "d"), ("Profondeur", 32, "d"), ("Hauteur", 32, "d"), ("Hauteur sous meuble (pose)", 17, "d")],
       "Chêne (teinte relevée #563C27) — essence : " + FA, FA, ("etage1-sejour-01", (260, 1180, 1350, 1350)),
       ("etsejour", "A", (55, 350, 0, 60)), "Rendus etage1-sejour-01, -05 · Élévation A (KAI-VIL-401) · KAI-VIL-405 (M9a)",
       facades="4 façades égales ≈ 70,4 (joints à ≈ 132,7 / ≈ 203,1 / ≈ 273,5)", handles="Aucune poignée visible — système : " + NC,
       opening="Type d'ouverture (portes ou abattants) : " + NC, pose="Suspendu, fixé au mur A",
       obs="Téléviseur exclu ; le meuble est inclus.", short="Meuble TV suspendu chêne, 4 façades"),
    it("SEJ-02", "Étagère verticale éclairée, montant marbre", "Rangement / niches", 1, "pce",
       [("Largeur", 71.2, "d"), ("Hauteur", 240, "d"), ("Départ (sur le meuble TV)", 49, "d"), ("Profondeur", None, "c"),
        ("Montant central marbre — largeur", 10.2, "d"), ("Tablettes", "7 : 4 à gauche (≈ 94 / 141 / 188 / 238), 3 à droite (≈ 117 / 164 / 212)", "d")],
       "Chêne (teinte relevée #563C27) + montant marbre blanc veiné (teinte relevée #877B6D)", FA,
       ("etage1-sejour-01", (280, 290, 560, 1220)), ("etsejour", "A", (45, 135, 40, 289)),
       "Rendus etage1-sejour-01, -05 · Élévation A (KAI-VIL-401) · KAI-VIL-405 (M9b)",
       light="LED sous les 7 tablettes (≈ 2,1 ml : 4 × ≈ 29,1 + 3 × ≈ 31,9) — profilé, température de couleur : " + NC,
       opening="Étagère ouverte", pose="Posée sur le meuble TV SEJ-01, fixée au mur A jusqu'au plafond",
       short="Étagère éclairée, 7 tablettes, montant marbre"),
    it("SEJ-03", "Bibliothèque chêne éclairée — mur d'entrée", "Rangement", 1, "pce",
       [("Longueur", 161.8, "d"), ("Profondeur", 27, "d"), ("Hauteur", 289, "d"), ("Soubassement fermé — hauteur", 70, "d"),
        ("Tablettes éclairées", "5 (≈ 77 / 102 / 158 / 209 / 231)", "d")],
       "Chêne (teinte relevée #563C27) — essence : " + FA, FA, ("etage1-sejour-08", (1150, 370, 1667, 1340)),
       ("etsejour", "B", (355, 524.4, 0, 289)), "Rendus etage1-sejour-04, -06, -08, -09 · Élévation B (KAI-VIL-402) · KAI-VIL-405 (M10)",
       facades="Soubassement fermé — nombre de façades : " + NC + " ; étagères ouvertes au-dessus",
       light="LED sous les 5 tablettes (≈ 8,1 ml) — profilé, température de couleur : " + NC,
       opening="Soubassement : type d'ouverture " + NC, pose="Posée au sol, fixée au mur B, du sol au plafond",
       short="Bibliothèque chêne éclairée, soubassement fermé"),
    it("SEJ-04", "Porte double chêne à oculus", "Menuiserie", 1, "pce",
       [("Largeur (2 vantaux)", 156.5, "d"), ("Hauteur", 208.3, "d"), ("Oculus vitrés (×2)", "≈ 18,2 × ≈ 172,8, bas à ≈ 16", "d"),
        ("Épaisseur", None, "c")],
       "Chêne (teinte relevée #563C27) + verre des oculus — type de verre : " + FA, FA, ("etage1-sejour-08", (200, 640, 740, 1350)),
       ("etsejour", "B", (60, 230, 0, 215)), "Rendus etage1-sejour-06, -08, -09 · Élévation B (KAI-VIL-402)",
       handles="Deux béquilles métal argenté — modèle : " + NC, opening="Deux vantaux battants — sens d'ouverture : " + NC,
       obs="Menuiserie intérieure : fabrication par l'atelier ou fourniture séparée " + NC + ".", short="Porte double chêne à oculus"),
    it("SEJ-05", "Panneaux muraux crème à joints creux — séjour", "Habillage mural", p_sej, "m²",
       [("Surface", m2(p_sej), "d"), ("Détail", " · ".join(parts_sej), "d"), ("Hauteur", 289, "d"),
        ("Joints creux — largeur, profondeur", None, "c")],
       "Panneaux crème (teinte relevée #756758) — matériau : " + FA, FA, ("etage1-sejour-01", (0, 280, 1667, 1370)),
       ("etsejour", "A", None), "Rendus etage1-sejour-01 à -09 · Élévations A à D (KAI-VIL-401 à 403)",
       revet="Calepinage suivant les joints relevés (verticaux et horizontaux)", fab="Découpes autour de la porte double et des baies",
       pose="Fixés sur les murs A, B, C et D",
       obs="Surface brute, déduction faite de la bibliothèque SEJ-03 et de la porte. " + " ; ".join(notes_sej),
       short="Panneaux muraux crème, joints creux"),
]

# ================================================================ CHAMBRE PRINCIPALE
p_chp, parts_chp, notes_chp = S("princ", ["A", "B", "C", "D"])
ITEMS["CHP"] = [
    it("CHP-01", "Colonnes chêne et soubassement cannelé éclairé — mur tête de lit", "Habillage mural", 2, "pce",
       [("Largeurs", "≈ 33,5 / ≈ 34,2", "d"), ("Hauteur totale", 292, "d"), ("Partie basse cannelée (hauteur)", 184.2, "d"),
        ("Partie haute chêne (hauteur)", 107.8, "d"), ("Profondeur", None, "c"), ("Surfaces", "chêne ≈ 0,75 m² · cannelures ≈ 1,27 m²", "d")],
       "Chêne (teinte relevée #694E39) + lames cannelées (teinte relevée #A4978A) — essence : " + FA, FA,
       ("chambre-principale-05", (250, 340, 410, 960)), ("princ", "A", (0, 40, 0, 292)),
       "Rendus chambre-principale-01, -02, -05 · Élévation A (KAI-VIL-501) · KAI-VIL-505 (M11)",
       light="Ligne LED horizontale à ≈ 184,2 sur chaque colonne (≈ 0,68 ml) — profilé : " + NC,
       pose="En applique aux deux extrémités du mur A", short="2 colonnes chêne, bas cannelé éclairé"),
    it("CHP-02", "Bande marbre brun foncé veiné rétroéclairée", "Habillage mural", 2.86, "m²",
       [("Largeur", 97.8, "d"), ("Hauteur", 292, "d"), ("Surface", m2(2.86), "d"), ("Épaisseur", None, "c")],
       "Marbre brun-vert foncé veiné (teinte relevée #312A1B) — référence : " + FA, "Finition (poli, adouci) : " + FA,
       ("chambre-principale-05", (680, 350, 1030, 960)), ("princ", "A", (125, 240, 0, 292)),
       "Rendus chambre-principale-01 à -05 · Élévation A (KAI-VIL-501) · ensemble M11",
       revet="Calepinage et sens du veinage : " + NC,
       light="Deux lignes LED verticales, de part et d'autre de la bande (≈ 5,8 ml) — profilé : " + NC,
       pose="Mur A, au centre, toute hauteur, derrière la tête de lit murale CHP-04", short="Bande marbre rétroéclairée"),
    it("CHP-03", "Panneaux miroirs — mur tête de lit", "Habillage mural", 2.89, "m²",
       [("Largeur", 99.4, "d"), ("Hauteur", 292, "d"), ("Surface", m2(2.89), "d"), ("Nombre de panneaux", None, "c"),
        ("Épaisseur", None, "c")],
       "Miroir — teinte : " + FA, FA, ("chambre-principale-05", (1000, 350, 1350, 960)), ("princ", "A", (225, 340, 0, 292)),
       "Rendus chambre-principale-01, -02, -05 · Élévation A (KAI-VIL-501) · ensemble M11", fab="Chants polis",
       pose="Mur A, entre la bande marbre et la colonne est", short="Miroirs toute hauteur ≈ 99 de large"),
    it("CHP-04", "Tête de lit murale tapissée", "Habillage mural", 1, "pce",
       [("Longueur", 364.3, "d"), ("Hauteur", 112.4, "d"), ("Épaisseur", None, "c")],
       "Tissu clair (teinte relevée #918376) — tissu et rembourrage : " + FA, FA,
       ("chambre-principale-05", (270, 930, 1460, 1180)), ("princ", "A", (0, 377.3, 0, 130)),
       "Rendus chambre-principale-01 à -05 · Élévation A (KAI-VIL-501) · ensemble M11",
       revet="Panneau tapissé, découpe supérieure courbe au centre (rendus)", fab="Structure et rembourrage : " + NC,
       pose="Fixée au mur A sur presque toute sa longueur, derrière le lit",
       obs="Habillage mural indépendant du lit. Le lit, sa propre tête de lit et les chevets sont exclus. Fourniture par l'atelier : " + NC + ".",
       short="Tête de lit murale ≈ 364 × 112"),
    it("CHP-05", "Meuble TV noir mat", "Meuble TV", 1, "pce",
       [("Longueur", 168, "d"), ("Profondeur", 29, "d"), ("Hauteur", None, "c")],
       "Noir mat (teinte relevée #19170D) — matériau : " + FA, FA, ("chambre-principale-04", (440, 1160, 1240, 1550)),
       None, "Rendu chambre-principale-04 · Plan d'aménagement étage (KAI-VIL-111) · KAI-VIL-505 (M13)",
       facades="3 portes en façade (rendu chambre-principale-04)", handles="Aucune poignée visible — système : " + NC,
       opening="3 portes battantes ou poussoirs : " + NC, pose="Posé au sol, face au lit",
       obs="Téléviseur exclu ; le meuble est inclus.", short="Meuble TV noir mat, 3 portes"),
    it("CHP-06", "Panneaux muraux — chambre principale", "Habillage mural", p_chp, "m²",
       [("Surface", m2(p_chp), "d"), ("Détail", " · ".join(parts_chp), "d"), ("Hauteur", 292, "d"),
        ("Joints — largeur, profondeur", None, "c")],
       "Panneaux muraux (teinte des rendus) — matériau : " + FA, FA, ("chambre-principale-05", (240, 330, 1460, 1200)),
       ("princ", "A", None), "Rendus chambre-principale-01 à -05 · Élévations A à D (KAI-VIL-501 à 503)",
       revet="Joints verticaux à ≈ 50,6 et ≈ 106,7 et joint horizontal à ≈ 184,2 sur le mur A", pose="Fixés sur les murs A, B, C et D",
       obs="Surface brute ; la zone derrière le dressing (exclu) n'est pas comptée. " + " ; ".join(notes_chp),
       short="Panneaux muraux"),
]

# ================================================================ DOUCHE PRINCIPALE
ITEMS["DPE"] = [
    it("DPE-01", "Meuble vasque suspendu en noyer", "Mobilier de salle d'eau", 1, "pce",
       [("Longueur", 156, "d"), ("Profondeur", 52, "d"), ("Hauteur du caisson", 46, "d"), ("Dessous du meuble", 34, "d"),
        ("Dessus du plan", 83, "d"), ("Tiroirs — largeur", 92, "d"), ("Niches ouvertes — largeur", 64, "d")],
       "Bois teinte noyer (teinte relevée #4E392C) — essence, massif ou placage : " + FA, FA, ("DPE-06", (560, 1030, 1560, 1530)),
       ("dpe", "furniture_M1"), "Rendus 06, 01 (douche) · Élévation B (KAI-DPE-504) · KAI-DPE-511 (M1)",
       facades="2 tiroirs superposés à gauche ; 2 niches ouvertes superposées à droite", handles="Sans poignée apparente (gorge) : " + NC,
       opening="2 tiroirs — coulisses et découpe pour le siphon : " + NC,
       fab="Pièce humide : panneaux et finitions résistants à l'eau. Plan effet terrazzo : voir DPE-02",
       pose="Suspendu, fixé au mur est ; alimentations et évacuation de la vasque à intégrer",
       obs="Vasque et robinetterie fournies séparément.", short="Meuble vasque suspendu, 2 tiroirs + 2 niches"),
    it("DPE-02", "Plan et crédence effet terrazzo", "Mobilier de salle d'eau", 1, "ens.",
       [("Plan", "≈ 156 × ≈ 52", "d"), ("Épaisseur du plan", 3, "c"), ("Crédence", "≈ 175 × ≈ 16 (de ≈ 83 à ≈ 99)", "d"),
        ("Épaisseur de la crédence", None, "c")],
       "Effet terrazzo clair (teinte relevée #B3AFA9) — matériau : " + FA, "Finition (poli, adouci) : " + FA,
       ("DPE-06", (580, 1030, 1560, 1250)), ("dpe", "elev_B"), "Rendus 06, 01 (douche) · Élévation B (KAI-DPE-504)",
       fab="Découpes : évacuation de la vasque à poser, 3 perçages de robinetterie", pose="Plan posé sur le meuble DPE-01 ; crédence collée au mur",
       short="Plan + crédence effet terrazzo"),
    it("DPE-03", "Commode en noyer", "Rangement de salle d'eau", 1, "pce",
       [("Longueur", 84, "d"), ("Profondeur", 50, "d"), ("Hauteur", 87, "d"), ("Socle en retrait — hauteur", 9, "d"),
        ("Poignées — longueur", 16, "c")],
       "Bois teinte noyer (teinte relevée #4E392C) — essence : " + FA, FA, ("DPE-02", (350, 1140, 830, 1590)), ("dpe", "furniture_M2"),
       "Rendus 02, 01, 04 (douche) · Élévation A (KAI-DPE-503) · KAI-DPE-512 (M2)",
       facades="2 tiroirs ; angles arrondis", handles="Poignées noires encastrées (modèle : " + NC + ")", opening="2 tiroirs — coulisses : " + NC,
       fab="Pièce humide : finitions résistantes à l'eau", pose="Posée au sol contre le mur sud", short="Commode noyer, 2 tiroirs"),
    it("DPE-04", "Étagères murales en verre fumé", "Rangement de salle d'eau", 3, "pce",
       [("Longueur", 100, "d"), ("Profondeur", 22, "d"), ("Hauteurs de pose", "≈ 110 / ≈ 144 / ≈ 179", "d"), ("Épaisseur du verre", None, "c")],
       "Verre fumé (teinte relevée #666460)", FA, ("DPE-02", (373, 640, 833, 1040)), ("dpe", "elev_A"),
       "Rendus 02, 01, 04 (douche) · Élévation A (KAI-DPE-503)", handles="Fixations métalliques visibles — type : " + NC,
       pose="Fixées au mur sud au-dessus de la commode", short="3 tablettes verre fumé"),
    it("DPE-05", "Étagères d'angle en noyer", "Rangement de salle d'eau", 2, "pce",
       [("Longueur", 51, "d"), ("Profondeur", 20, "d"), ("Hauteurs de pose", "≈ 179 / ≈ 216", "d"), ("Épaisseur", None, "c")],
       "Bois teinte noyer — essence : " + FA, FA, ("DPE-02", (1200, 420, 1490, 720)), ("dpe", "elev_A"),
       "Rendus 02, 04 (douche) · Élévation A (KAI-DPE-503)", handles="Fixation (invisible ou équerres) : " + NC,
       pose="Fixées dans l'angle sud-ouest, au-dessus du coffrage du WC", short="2 tablettes noyer"),
    it("DPE-06", "Miroir rétroéclairé", "Miroir", 1, "pce",
       [("Largeur", 175, "d"), ("Hauteur", 100, "d"), ("Bas du miroir", 99, "d")],
       "Miroir argenté, sans cadre apparent", FA, ("DPE-06", (580, 540, 1480, 1080)), ("dpe", "elev_B"),
       "Rendus 06, 01 (douche) · Élévation B (KAI-DPE-504) · KAI-DPE-603",
       light="Halo LED sur le pourtour (≈ 5,5 ml si intégré) — température de couleur, IP : " + NC,
       pose="Fixé au mur est, au-dessus de la crédence",
       obs="Fabrication sur mesure (miroitier) ou modèle du commerce : " + NC + ".", short="Miroir ≈ 175 × 100 rétroéclairé"),
    it("DPE-07", "Rangement de douche (niche ou étagère)", "Niche murale", 1, "pce",
       [("Hauteur", "≈ 105 à ≈ 175", "d"), ("Largeur", None, "c"), ("Profondeur", None, "c")],
       "FINITION À CONFIRMER (fond de douche en faïence bordeaux)", FA, ("DPE-07", (560, 600, 800, 1040)), ("dpe", "elev_E"),
       "Rendus 07, 08 (douche) · Élévation E (KAI-DPE-507)",
       obs="Type (niche encastrée dans la paroi ou étagère rapportée) : " + NC + ".", short="Rangement de douche — type à confirmer"),
    it("DPE-08", "Habillage mural effet travertin", "Habillage mural", 31.01, "m²",
       [("Surface", m2(31.01), "d"), ("Détail", "mur A ≈ 7,59 · mur B ≈ 4,74 · mur C ≈ 4,57 · mur D ≈ 10,14 · retour ≈ 3,96", "d"),
        ("Hauteur", 289, "d"), ("Format des panneaux", None, "c")],
       "Revêtement effet travertin (teinte relevée #B8B2AC) — nature (pierre, céramique ou panneau) : " + FA, "Mat — " + FA,
       ("DPE-02", (380, 170, 860, 530)), ("dpe", "elev_D"), "Rendus 01 à 08 (douche) · Élévations A à F · KAI-DPE-513",
       revet="Veinage horizontal ; joints non visibles sur les rendus", fab="Découpes : fenêtres F1, F2, porte P1, crédence, miroir, coffrage du WC",
       pose="Tous les murs de la pièce et le mur latéral de la douche, toute hauteur",
       obs="Surface brute calculée d'après les cotes écrites et les hauteurs relevées. Pièce humide : produit adapté à confirmer.",
       short="Revêtement mural effet travertin"),
    it("DPE-09", "Faïence bordeaux — fond de douche et coffrage du WC", "Revêtement", 7.49, "m²",
       [("Surface", m2(7.49), "d"), ("Fond de douche", "164,80 × ≈ 289 (≈ 4,76 m²)", "d"),
        ("Coffrage du WC", "116 × 40 × ≈ 145 : face, côté et dessus (≈ 2,72 m²)", "d"), ("Format", "entraxe des joints ≈ 7,7 × 17,7 (relevé)", "c")],
       "Faïence bordeaux brillante (teinte relevée #48211F) — référence : " + FA, "Brillante, pose verticale",
       ("DPE-02", (930, 840, 1290, 1110)), ("dpe", "elev_E"), "Rendus 02, 04, 07, 08 (douche) · Élévations A, D, E · KAI-DPE-513",
       fab="Teinte de joint : " + NC + " ; bâti du coffrage (structure) : " + NC,
       pose="Fond de douche toute hauteur ; coffrage du WC sur ses faces visibles",
       obs="Pose par le carreleur : inclusion dans le lot de l'atelier " + NC + ".", short="Faïence bordeaux"),
    it("DPE-10", "Paroi de douche style verrière", "Menuiserie", 1, "ens.",
       [("Face", 122, "d"), ("Retour", 90, "d"), ("Hauteur du verre", "≈ 200 (de ≈ 8,5 à ≈ 209)", "d"), ("Trame", "5 rangs de ≈ 40 ; montant à ≈ 70", "d"),
        ("Épaisseur du verre", None, "c")],
       "Verre clair, profilés métal noir mat", FA, ("DPE-08", (60, 400, 980, 1640)), ("dpe", "elev_E"),
       "Rendus 07, 08 (douche) · Élévation E (KAI-DPE-507) · KAI-DPE-407", handles="Poignée verticale noire — modèle : " + NC,
       opening="Porte battante dans la face — sens d'ouverture : " + NC,
       obs="Fabrication sur mesure (miroitier, serrurier) ou modèle du commerce : " + NC + ".", short="Paroi d'angle verrière"),
    it("DPE-11", "Porte P1", "Menuiserie", 1, "pce",
       [("Largeur", 74, "v"), ("Hauteur", 202, "d"), ("Épaisseur", None, "c")],
       "Bois sombre à inserts métalliques horizontaux — " + FA, FA, ("DPE-06", (0, 380, 330, 1500)), ("dpe", "elev_C"),
       "Rendus 06, 08 (douche) · Élévation C (KAI-DPE-505)", handles="Béquille métal — modèle : " + NC,
       opening="Porte battante — sens d'ouverture : " + NC,
       obs="Menuiserie intérieure : fabrication par l'atelier ou fourniture séparée " + NC + ".", short="Porte P1"),
]

# ================================================================ EXCLUSIONS (bought separately)
EXCLUDED = [
    ("Chambre principale", "Placard (dressing chêne toute hauteur, ≈ 231 × ≈ 70 × ≈ 292, M12)", "chambre-principale-04"),
    ("Chambre principale", "Lit et sa tête de lit", "chambre-principale-05"),
    ("Chambre principale", "Tables de chevet (×2)", "chambre-principale-05"),
    ("Chambre principale", "Téléviseur", "chambre-principale-04"),
    ("Chambre d'amis", "Placard d'angle (armoire de l'alcôve, ≈ 140 × ≈ 50, M8)", "—"),
    ("Chambre d'amis", "Lit plateforme tapissé et sa tête de lit", "chambre-amis-03"),
    ("Chambre d'amis", "Tables de chevet rondes (×2)", "chambre-amis-01"),
    ("Chambre d'amis", "Téléviseur", "chambre-amis-02"),
    ("Salon principal", "Téléviseur 75\"", "rdc-salon-07"),
    ("Séjour (étage 1)", "Téléviseur 75\"", "etage1-sejour-01"),
]

# ================================================================ OUTSIDE FABRICATION (to supply separately or to confirm)
OUTSIDE = [
    ("Salon principal", "Canapés modulaires (cuir taupe foncé, crème)", "achat séparé"),
    ("Salon principal", "Tables basses gigognes bois noir et pierre veinée (≈ 148 × ≈ 116 en plan)", "fabrication ou achat : à confirmer"),
    ("Salon principal", "Tapis, rideaux et voilages, jarre, plantes, œuvre d'art", "achat séparé"),
    ("Salle à manger", "8 chaises en bouclé, structure bois foncé", "achat séparé"),
    ("Salle à manger", "Suspension lumineuse sculpturale", "achat séparé (luminaire)"),
    ("Chambre d'amis", "Pouf capitonné cuir, suspensions à globe, lampes de la coiffeuse, rideaux", "achat séparé"),
    ("Séjour (étage 1)", "Canapé d'angle, fauteuil, pouf à côtes, tapis, rideaux, plantes, œuvre", "achat séparé"),
    ("Séjour (étage 1)", "Tables basses (ovale marbre ; rectangulaire bois et métal)", "fabrication ou achat : à confirmer"),
    ("Chambre principale", "Banc capitonné à piètement laiton", "fabrication ou achat : à confirmer"),
    ("Chambre principale", "Suspensions, rideaux, tapis, linge de lit", "achat séparé"),
    ("Douche principale", "Vasque, robinetterie, colonne de douche, WC suspendu et bâti-support, plaque de commande", "achat séparé (sanitaires)"),
    ("Douche principale", "Échelle porte-serviettes, porte-serviettes à barres, patères, suspensions, accessoires", "achat séparé"),
    ("Toute la villa", "Faux plafonds et gorges lumineuses périphériques", "lots plâtrerie et électricité"),
    ("Toute la villa", "Parquet, menuiseries extérieures (porte vitrée du salon, fenêtres, baies)", "autres lots"),
]
