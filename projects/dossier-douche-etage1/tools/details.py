"""Douche principale — Étage 1 : rendus et détails décoratifs (données).

Rendus : fichiers originaux de Karen dans ../sources (copies exactes). Plan coté 05 : seule sa partie gauche (douche principale)
est utilisée, dans tools/geom.py ; la partie chambre est exclue.
Détails : agrandissements signalés, extraits des rendus. Chaque zone est encadrée et numérotée sur le rendu entier, qui
reste présenté en grand format. Boîtes en pixels du fichier original : (x0, y0, x1, y1).
"""

RENDERS = {   # n° de fichier : (nom d'envoi, légende, vue)
    "01": ("IMG_7775", "Vue d'ensemble : meuble vasque, miroir rétroéclairé, étagères en verre fumé et commode en noyer",
           "Vue de 3/4"),
    "02": ("IMG_7774", "Mur des fenêtres : étagères en verre fumé, commode en noyer, coffrage du WC en faïence bordeaux",
           "Vue de face"),
    "03": ("IMG_7773", "Vue de dessus de la maquette 3D : douche, WC, commode, porte-serviettes et meuble vasque",
           "Vue de dessus"),
    "04": ("IMG_7772", "Coin WC : WC suspendu, coffrage bordeaux, échelle porte-serviettes", "Vue de 3/4"),
    "06": ("IMG_7767", "Mur du meuble vasque : plan en terrazzo, vasque à poser, robinetterie noire, miroir rétroéclairé",
           "Vue de face"),
    "07": ("IMG_7768", "Douche : paroi verrière à profilés noirs, fond en faïence bordeaux, patères", "Vue de 3/4"),
    "08": ("IMG_7769", "Douche : paroi verrière d'angle, colonne de douche noire", "Vue de face"),
}
RENDER_ORDER = ["01", "06", "02", "04", "08", "07", "03"]

CATEGORIES = ["Meuble vasque", "Miroirs", "Robinetterie", "Douche", "Niches murales", "Parois vitrées", "Éclairage LED",
              "Habillage mural", "Revêtements", "Rangements", "Accessoires et décoration", "Ouvertures et plafond"]
RECAT = {"D01": "Habillage mural", "D02": "Habillage mural", "D03": "Revêtements", "D05": "Revêtements",
         "D07": "Miroirs", "D08": "Éclairage LED", "D09": "Éclairage LED", "D10": "Parois vitrées", "D11": "Robinetterie",
         "D12": "Robinetterie", "D13": "Douche", "D14": "Niches murales", "D15": "Douche", "D16": "Rangements",
         "D17": "Rangements", "D18": "Rangements", "D19": "Accessoires et décoration", "D20": "Accessoires et décoration",
         "D21": "Robinetterie", "D22": "Accessoires et décoration", "D23": "Ouvertures et plafond",
         "D24": "Niches murales", "D25": "Ouvertures et plafond", "D26": "Ouvertures et plafond",
         "D27": "Ouvertures et plafond", "D28": "Accessoires et décoration", "D29": "Parois vitrées", "D30": "Miroirs",
         "D31": "Éclairage LED", "D32": "Éclairage LED", "D04": "Meuble vasque", "D06": "Robinetterie"}

# D-number: (title, description, category, render, box)
D = {
    "D01": ("Panneaux muraux effet travertin", "Grands panneaux clairs à veinage horizontal, sur toute la hauteur des murs.",
            "Revêtements muraux", "02", (380, 170, 860, 530)),
    "D02": ("Faïence bordeaux brillante", "Carreaux rectangulaires posés à la verticale, joints alignés ; coffrage du WC.",
            "Revêtements muraux", "02", (930, 840, 1290, 1110)),
    "D03": ("Sol « galets » blanc et noir", "Grandes dalles blanches veinées aux angles arrondis, inserts noirs en étoile.",
            "Carrelage et marbre", "02", (40, 1496, 520, 1816)),
    "D04": ("Meuble vasque suspendu en noyer", "Deux tiroirs sans poignée apparente, niches ouvertes à droite.",
            "Meuble vasque", "06", (560, 1200, 1560, 1530)),
    "D05": ("Plan et crédence en terrazzo, vasque à poser", "Terrazzo clair à éclats ; vasque rectangulaire blanche.",
            "Carrelage et marbre", "06", (580, 1030, 1040, 1250)),
    "D06": ("Robinetterie noire mate", "Mitigeur trois trous : bec haut et deux croisillons.",
            "Robinetterie", "06", (690, 990, 930, 1170)),
    "D07": ("Miroir rétroéclairé", "Grand miroir rectangulaire, halo lumineux sur le pourtour.",
            "Miroirs", "01", (200, 580, 560, 850)),
    "D08": ("Suspensions à globe", "Petits globes lumineux sur câbles fins, à hauteurs décalées.",
            "Éclairage", "01", (620, 700, 940, 940)),
    "D09": ("Gorge lumineuse LED", "Ligne de LED continue en périphérie du faux plafond.",
            "Éclairage", "01", (40, 120, 560, 500)),
    "D10": ("Paroi verrière à profilés noirs", "Verre clair, montants et traverses noirs, porte avec poignée verticale.",
            "Douche et parois vitrées", "08", (300, 820, 660, 1090)),
    "D11": ("Colonne de douche noire", "Pommeau de tête rond sur bras, barre murale.",
            "Robinetterie", "08", (150, 480, 510, 750)),
    "D12": ("Mitigeur et douchette", "Commandes murales noires et douchette sur la colonne.",
            "Robinetterie", "08", (110, 950, 430, 1190)),
    "D13": ("Fond de douche en faïence bordeaux", "Même faïence que le coffrage du WC, posée à la verticale jusqu'au plafond.",
            "Revêtements muraux", "07", (209, 209, 900, 450)),
    "D14": ("Rangement de douche", "Produits rangés sur le mur du fond. Type à confirmer : niche encastrée ou étagère.",
            "Niches murales", "07", (560, 600, 800, 1040)),
    "D15": ("Sol de douche", "Motif « galets » dans la douche, au même calepinage que la pièce.",
            "Carrelage et marbre", "07", (160, 1400, 800, 1650)),
    "D16": ("Étagères en verre fumé", "Trois tablettes de verre sur fixations métalliques ; sculptures de chevaux noir et blanc.",
            "Accessoires et décoration", "02", (373, 640, 833, 1040)),
    "D17": ("Étagères en noyer et miroir grossissant", "Deux tablettes en noyer d'angle, petit miroir rond.",
            "Miroirs", "02", (1200, 420, 1490, 720)),
    "D18": ("Commode en noyer", "Deux tiroirs à poignées encastrées, plateau aux angles arrondis.",
            "Accessoires et décoration", "02", (350, 1140, 830, 1590)),
    "D19": ("Échelle porte-serviettes", "Montants noirs, barres et panier de rangement noir.",
            "Accessoires et décoration", "04", (1220, 680, 1580, 1480)),
    "D20": ("WC suspendu et coffrage", "Cuvette blanche suspendue devant le coffrage en faïence bordeaux.",
            "Accessoires et décoration", "04", (640, 860, 1060, 1440)),
    "D21": ("Plaque de commande et dérouleur", "Plaque de commande et dérouleur noirs sur le coffrage.",
            "Robinetterie", "04", (780, 1000, 1020, 1180)),
    "D22": ("Porte-serviettes à barres", "Porte-serviettes mural noir à côté du meuble vasque.",
            "Accessoires et décoration", "06", (270, 1140, 590, 1380)),
    "D23": ("Porte d'entrée", "Porte sombre à inserts métalliques horizontaux, béquille métal.",
            "Plafond et finitions", "06", (0, 880, 320, 1120)),
    "D24": ("Niches ouvertes du meuble vasque", "Deux niches en noyer pour le linge roulé.",
            "Niches murales", "06", (1140, 1200, 1550, 1515)),
    "D25": ("Fenêtre haute", "Grande fenêtre étroite, verre dépoli, encadrement blanc.",
            "Plafond et finitions", "02", (40, 470, 320, 900)),
    "D26": ("Petite fenêtre", "Fenêtre à deux vantaux au-dessus du coffrage du WC.",
            "Plafond et finitions", "02", (930, 470, 1230, 830)),
    "D27": ("Plafond et gorge lumineuse", "Faux plafond blanc, joint creux et ligne LED le long du mur.",
            "Plafond et finitions", "02", (0, 0, 900, 330)),
    "D28": ("Patères et peignoirs", "Patères noires murales à côté de la douche.",
            "Accessoires et décoration", "07", (850, 440, 1210, 720)),
    "D29": ("Pied de paroi", "Profilé noir en pied de la paroi vitrée, sur le sol en motif « galets ».",
            "Douche et parois vitrées", "07", (560, 1360, 980, 1660)),
}

D.update({
    "D30": ("Miroir rétroéclairé, vue de face", "Grand miroir sans cadre apparent au-dessus du plan, reflet de la pièce.",
            "Miroirs", "06", (580, 540, 1480, 1080)),
    "D31": ("Halo du miroir", "Lumière diffusée sur le pourtour du miroir, contre le mur effet travertin.",
            "Éclairage LED", "06", (1330, 520, 1500, 760)),
    "D32": ("Suspensions devant le miroir", "Globes lumineux à hauteurs décalées, câbles fins depuis le plafond.",
            "Éclairage LED", "06", (1250, 720, 1500, 1000)),
    "D33": ("Angle de la paroi et fond bordeaux", "Montant noir de la paroi contre la faïence bordeaux ; patère à droite.",
            "Parois vitrées", "08", (700, 420, 1000, 820)),
    "D34": ("Poignée de la porte de douche", "Poignée verticale noire sur le montant central.",
            "Parois vitrées", "08", (380, 900, 560, 1120)),
    "D35": ("Seuil et pied de paroi", "Profilé noir en pied de paroi, sol « galets » de la douche.",
            "Parois vitrées", "08", (150, 1450, 800, 1640)),
    "D36": ("Sculptures de chevaux", "Deux chevaux cabrés, noir et blanc, sur l'étagère en verre fumé.",
            "Accessoires et décoration", "02", (600, 750, 860, 880)),
    "D37": ("Linge sur la commode", "Serviettes pliées et roulées sur un plateau, sur le dessus en noyer.",
            "Accessoires et décoration", "02", (430, 1100, 840, 1200)),
    "D38": ("Plante et objets", "Plante en pot blanc et objets posés sur la tablette basse.",
            "Accessoires et décoration", "02", (560, 930, 860, 1020)),
    "D39": ("Plateau et diffuseur", "Plateau noir, diffuseur de parfum et savons sur le plan en terrazzo.",
            "Accessoires et décoration", "06", (1150, 1060, 1360, 1200)),
})

# detail plates: (number, title, base render, [details]) — every detail on a plate comes from its base render
PLATES = [
    ("402", "Meuble vasque", "06", ["D04", "D05", "D24"]),
    ("403", "Miroir et éclairage du miroir", "06", ["D30", "D31", "D32"]),
    ("404", "Robinetterie du lavabo et plan", "06", ["D06", "D39"]),
    ("405", "Douche : colonne, mitigeur et paroi", "08", ["D11", "D12", "D10"]),
    ("406", "Douche : fond, niche murale et sol", "07", ["D13", "D14", "D15"]),
    ("407", "Parois vitrées", "08", ["D33", "D34", "D35"]),
    ("408", "Éclairage LED et suspensions", "01", ["D09", "D07", "D08"]),
    ("409", "Habillage mural et revêtements", "02", ["D01", "D02", "D03"]),
    ("410", "Rangements", "02", ["D16", "D17", "D18"]),
    ("411", "Accessoires et décoration", "02", ["D36", "D37", "D38"]),
    ("412", "Coin WC et échelle porte-serviettes", "04", ["D19", "D20", "D21"]),
    ("413", "Patères et pied de paroi", "07", ["D28", "D29"]),
    ("414", "Porte et porte-serviettes", "06", ["D23", "D22"]),
    ("415", "Ouvertures et plafond", "02", ["D25", "D26", "D27"]),
]

# where the number tag sits on the frame when frames are close (default: top-left)
LABEL_POS = {"D04": "bl", "D06": "tr", "D12": "bl", "D21": "br", "D31": "tr", "D32": "bl", "D22": "bl", "D39": "tr", "D36": "tr", "D38": "bl"}

for _k, _c in RECAT.items():
    D[_k] = D[_k][:2] + (_c,) + D[_k][3:]
