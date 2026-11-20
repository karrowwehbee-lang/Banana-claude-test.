"""Nuanciers et échantillons de matières relevés directement dans les rendus du projet.
Chaque entrée : (pièce, nom descriptif, fichier source, boîte de recadrage x0,y0,x1,y1).
La couleur HEX est la médiane des pixels de la zone ; l'échantillon de texture est la zone elle-même."""
import json, pathlib, statistics
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
S = "sources/"
SW = [
 ("rdc", "Chêne clair — panneaux et colonnes", "01-rdc-salon-principal/rdc-salon-08.png", (600, 460, 730, 880)),
 ("rdc", "Panneaux muraux crème", "01-rdc-salon-principal/rdc-salon-08.png", (790, 480, 960, 880)),
 ("rdc", "Bois foncé — double porte", "01-rdc-salon-principal/rdc-salon-08.png", (160, 640, 500, 1080)),
 ("rdc", "Cuir taupe foncé — canapé", "01-rdc-salon-principal/rdc-salon-08.png", (800, 1180, 1000, 1270)),
 ("rdc", "Tapis clair", "01-rdc-salon-principal/rdc-salon-08.png", (150, 1450, 600, 1650)),
 ("rdc", "Parquet bois", "01-rdc-salon-principal/rdc-salon-03.png", (900, 1450, 1500, 1800)),
 ("rdc", "Marbre blanc veiné — colonne", "01-rdc-salon-principal/rdc-salon-01.png", (578, 420, 650, 820)),
 ("rdc", "Travertin — table à manger", "01-rdc-salon-principal/rdc-salon-09.png", (760, 1360, 1150, 1480)),
 ("rdc", "Bouclé — chaises", "01-rdc-salon-principal/rdc-salon-09.png", (447, 1378, 512, 1440)),
 ("rdc", "Rouge — œuvre salle à manger", "01-rdc-salon-principal/rdc-salon-09.png", (1400, 650, 1600, 900)),
 ("rdc", "Rideaux taupe", "01-rdc-salon-principal/rdc-salon-11.png", (270, 520, 380, 1100)),
 ("amis", "Marbre blanc veiné caramel", "02-chambre-amis/chambre-amis-02.png", (800, 130, 1350, 600)),
 ("amis", "Lames chêne", "02-chambre-amis/chambre-amis-01.png", (328, 300, 388, 1100)),
 ("amis", "Panneaux muraux beige", "02-chambre-amis/chambre-amis-01.png", (600, 200, 1100, 500)),
 ("amis", "Lin clair — lit", "02-chambre-amis/chambre-amis-01.png", (480, 1240, 760, 1340)),
 ("amis", "Cuir brun — pouf", "02-chambre-amis/chambre-amis-02.png", (160, 1300, 420, 1450)),
 ("princ", "Marbre brun foncé veiné", "03-chambre-principale/chambre-principale-05.png", (720, 380, 1000, 700)),
 ("princ", "Tissu clair — tête de lit", "03-chambre-principale/chambre-principale-05.png", (330, 965, 520, 1060)),
 ("princ", "Kaki — linge de lit", "03-chambre-principale/chambre-principale-05.png", (500, 1250, 1200, 1400)),
 ("princ", "Tissu — banc", "03-chambre-principale/chambre-principale-05.png", (500, 1530, 1300, 1700)),
 ("princ", "Chêne — dressing", "03-chambre-principale/chambre-principale-04.png", (600, 480, 1100, 880)),
 ("princ", "Noir — meuble TV", "03-chambre-principale/chambre-principale-04.png", (500, 1260, 1000, 1400)),
 ("et1", "Gris taupe — canapé", "04-etage1-sejour/etage1-sejour-03.png", (330, 1170, 620, 1270)),
 ("et1", "Marbre blanc veiné — table basse", "04-etage1-sejour/etage1-sejour-03.png", (660, 1330, 900, 1420)),
 ("et1", "Cuir cognac — pouf", "04-etage1-sejour/etage1-sejour-03.png", (40, 1450, 300, 1650)),
 ("et1", "Rouge — œuvre", "04-etage1-sejour/etage1-sejour-08.png", (900, 720, 1200, 1100)),
 ("et1", "Chêne — portes et bibliothèque", "04-etage1-sejour/etage1-sejour-08.png", (260, 760, 370, 1300)),
 ("et1", "Tapis tissé", "04-etage1-sejour/etage1-sejour-02.png", (300, 1650, 900, 1790)),
]

def main():
    out = ROOT / "build/swatches"; out.mkdir(parents=True, exist_ok=True)
    data = []
    for i, (room, name, f, box) in enumerate(SW):
        im = Image.open(ROOT / S / f).convert("RGB").crop(box)
        px = list(im.get_flattened_data()) if hasattr(im, "get_flattened_data") else list(im.getdata())
        med = tuple(int(statistics.median(c[k] for c in px)) for k in range(3))
        hexc = "#%02X%02X%02X" % med
        p = f"{room}-{i:02d}.jpg"; im.save(out / p, quality=92)
        data.append({"room": room, "name": name, "hex": hexc, "img": f"swatches/{p}"})
    (out / "swatches.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
    for d in data: print(d["room"], d["hex"], d["name"])

if __name__ == "__main__":
    main()
