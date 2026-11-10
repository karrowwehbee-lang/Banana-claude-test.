"""KAÏRA — retouche photographique des rendus (réglages globaux uniquement).

Usage : python3 tools/retouche_rendus.py
Lit rendus/originaux/, écrit rendus/retouches/ (JPEG pleine résolution) et rendus/avant-apres.jpg.

Seuls des réglages globaux sont appliqués : balance des blancs vers un blanc crème, exposition,
éclaircissement des tons moyens, protection des hautes lumières (lignes LED), légère vibrance et netteté.
Aucun élément n'est ajouté, retiré, déplacé ou repeint : le design et les matériaux restent intacts.
"""
import pathlib
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "rendus/originaux", ROOT / "rendus/retouches"

CREAM = np.array([1.0, 0.972, 0.93])   # blanc chaud visé pour les murs clairs (rapport R:G:B)

# expo : luminance visée pour le 96e centile · gamma < 1 éclaircit les tons moyens
# wb : force de la correction de balance des blancs (0 = aucune, 1 = totale)
SETTINGS = {
    "01-salon-tableau-bordeaux":  dict(expo=0.90, gamma=0.80, wb=0.55, vib=0.10),
    "02-salon-mur-tv":            dict(expo=0.90, gamma=0.80, wb=0.55, vib=0.08),
    "03-chambre-marbre":          dict(expo=0.90, gamma=0.80, wb=0.55, vib=0.10),
    "04-chambre-claire":          dict(expo=0.93, gamma=0.90, wb=0.50, vib=0.06),
    "05-salle-a-manger-detail":   dict(expo=0.92, gamma=0.86, wb=0.50, vib=0.08),
    "06-salle-a-manger":          dict(expo=0.92, gamma=0.84, wb=0.50, vib=0.08),
    "07-sejour-ouvert":           dict(expo=0.94, gamma=0.94, wb=0.40, vib=0.05, jpeg=True),
    "08-cuisine":                 dict(expo=0.94, gamma=0.94, wb=0.40, vib=0.05, jpeg=True),
    "09-entree":                  dict(expo=0.93, gamma=0.88, wb=0.40, vib=0.04, jpeg=True),
}


def luma(a):
    return a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722


def shoulder(x, knee=0.86):
    """Compression douce au-dessus du genou : les LED restent lumineuses sans brûler."""
    over = np.maximum(x - knee, 0)
    return np.where(x > knee, knee + (1 - knee) * (1 - np.exp(-over / (1 - knee))), x)


def retouch(img, expo, gamma, wb, vib, jpeg=False):
    a = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
    y = luma(a)
    sat = a.max(-1) - a.min(-1)

    # 1. balance des blancs : pixels clairs et peu saturés (murs, plafonds) -> blanc crème
    lo, hi = np.percentile(y, [55, 97])
    m = (y > lo) & (y < hi) & (sat < 0.12)
    if m.sum() > 500:
        ref = a[m].mean(0)
        gains = (CREAM * ref.mean() / CREAM.mean()) / ref
        gains = 1 + wb * (gains - 1)
        a = a * gains.clip(0.85, 1.2)

    # 2. exposition : le 96e centile de luminance vers la valeur visée
    y = luma(a)
    a = a * (expo / max(np.percentile(y, 96), 1e-3))

    # 3. tons moyens : courbe gamma sur la luminance, appliquée en rapport (teintes conservées)
    y = luma(a).clip(1e-4, None)
    y_new = np.power(y.clip(0, 1), gamma) * np.where(y > 1, y, 1)
    a = a * (y_new / y)[..., None]

    # 4. vibrance légère : compense la désaturation perçue après éclaircissement
    y = luma(a)[..., None]
    s = (a.max(-1) - a.min(-1))[..., None]
    a = y + (a - y) * (1 + vib * (1 - s.clip(0, 1)))

    # 5. hautes lumières protégées
    a = shoulder(a.clip(0, None)).clip(0, 1)
    out = Image.fromarray((a * 255 + 0.5).astype(np.uint8))

    # 6. micro-contraste discret + netteté fine (plus douce sur les JPEG compressés)
    out = out.filter(ImageFilter.UnsharpMask(radius=30, percent=10, threshold=0))
    out = out.filter(ImageFilter.UnsharpMask(radius=1.0, percent=35 if jpeg else 60, threshold=3))
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pairs = []
    for name, cfg in SETTINGS.items():
        src = next(SRC.glob(name + ".*"))
        img = Image.open(src)
        res = retouch(img, **cfg)
        res.save(OUT / f"{name}.jpg", quality=95, subsampling=0)
        pairs.append((name, img.convert("RGB"), res))
        print(f"{name}: {img.size} -> {OUT / (name + '.jpg')}")

    # planche avant / après (contrôle)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 13)
    except OSError:
        font = ImageFont.load_default()
    tw = 300
    rows = []
    for name, before, after in pairs:
        th = round(before.height * tw / before.width)
        row = Image.new("RGB", (2 * tw + 30, th + 34), "#FAF7F2")
        row.paste(before.resize((tw, th), Image.LANCZOS), (10, 28))
        row.paste(after.resize((tw, th), Image.LANCZOS), (tw + 20, 28))
        ImageDraw.Draw(row).text((10, 7), f"{name}   avant  |  après", fill="#3B2A22", font=font)
        rows.append(row)
    cols = 3
    w = max(r.width for r in rows)
    hs = [max(r.height for r in rows[i:i + cols]) for i in range(0, len(rows), cols)]
    sheet = Image.new("RGB", (w * cols, sum(hs)), "#FAF7F2")
    yy = 0
    for k, i in enumerate(range(0, len(rows), cols)):
        for j, r in enumerate(rows[i:i + cols]):
            sheet.paste(r, (j * w, yy))
        yy += hs[k]
    sheet.save(ROOT / "rendus/avant-apres.jpg", quality=90)
    print("planche :", ROOT / "rendus/avant-apres.jpg")


if __name__ == "__main__":
    main()
