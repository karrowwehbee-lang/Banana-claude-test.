"""Remplace l'image affichée sur les écrans TV des rendus par un écran éteint (noir satiné + léger reflet).
Les rendus d'origine restent intacts dans sources/ ; les versions modifiées vont dans build/tvoff/."""
import pathlib
from PIL import Image, ImageDraw, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCREENS = {  # coins écran (haut-gauche, haut-droit, bas-droit, bas-gauche), en pixels
    "01-rdc-salon-principal/rdc-salon-03.png": [(272, 782), (588, 766), (588, 1002), (272, 992)],
    "01-rdc-salon-principal/rdc-salon-04.png": [(510, 760), (945, 780), (945, 1002), (510, 1038)],
    "01-rdc-salon-principal/rdc-salon-07.png": [(432, 798), (798, 798), (798, 998), (432, 998)],
    "02-chambre-amis/chambre-amis-02.png": [(688, 605), (1452, 605), (1452, 1032), (688, 1032)],
    "02-chambre-amis/chambre-amis-04.png": [(692, 658), (1498, 580), (1498, 1092), (692, 1055)],
    "03-chambre-principale/chambre-principale-04.png": [(585, 922), (1050, 924), (1050, 1228), (585, 1205)],
    "04-etage1-sejour/etage1-sejour-01.png": [(638, 712), (1216, 712), (1216, 1034), (638, 1034)],
    "04-etage1-sejour/etage1-sejour-05.png": [(727, 710), (1250, 682), (1250, 995), (727, 1020)],
}

def inset(q, k):
    cx = sum(p[0] for p in q) / 4; cy = sum(p[1] for p in q) / 4
    return [(x + (cx - x) * k / abs(cx - x) if x != cx else x, y + (cy - y) * k / abs(cy - y) if y != cy else y) for x, y in q]

def main():
    out = ROOT / "build/tvoff"; out.mkdir(parents=True, exist_ok=True)
    for rel, quad in SCREENS.items():
        im = Image.open(ROOT / "sources" / rel).convert("RGB")
        q = inset(quad, 4)
        xs = [p[0] for p in q]; ys = [p[1] for p in q]
        w, h = int(max(xs) - min(xs)) + 1, int(max(ys) - min(ys)) + 1
        # écran éteint : noir satiné, dégradé vertical léger + reflet diagonal très doux
        scr = Image.new("RGB", (w, h))
        px = scr.load()
        for y in range(h):
            for x in range(w):
                t = y / h; r = max(0.0, 1 - abs((x / w) - 0.35 - (y / h) * 0.3) * 4)
                v = 14 + 8 * (1 - t) + 10 * r
                px[x, y] = (int(v), int(v), int(v * 1.08))
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).polygon(q, fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(0.8))
        layer = Image.new("RGB", im.size); layer.paste(scr, (int(min(xs)), int(min(ys))))
        im = Image.composite(layer, im, mask)
        im.save(out / pathlib.Path(rel).name)
        print("ok", rel)

if __name__ == "__main__":
    main()
