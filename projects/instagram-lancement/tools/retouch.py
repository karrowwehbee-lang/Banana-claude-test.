"""KAÏRA — retouche « lumière du jour » des rendus du studio, sans toucher au design.

Corrections globales uniquement (comme un développement photo) : balance des blancs vers un blanc crème,
exposition, ouverture des ombres, contraste doux, netteté fine. Aucun objet n'est ajouté, retiré ou déplacé,
et les matériaux gardent leurs couleurs relatives.

Usage : python3 tools/retouch.py <source> <sortie.jpg> [--force 0..1]
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

CREAM = np.array([244, 239, 231]) / 255.0   # blanc crème visé pour les plafonds et murs clairs


def lum(a):
    return a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722


def retouch(img, force=1.0):
    a = np.asarray(img.convert("RGB"), dtype=np.float64) / 255.0
    h = a.shape[0]
    # 1. balance des blancs : on prend les surfaces claires et peu saturées du haut de l'image (plafond, murs)
    top = a[: int(h * 0.35)]
    L = lum(top)
    sat = top.max(-1) - top.min(-1)
    mask = (L > np.percentile(L, 55)) & (L < np.percentile(L, 97)) & (sat < 0.12)
    ref = top[mask].mean(0) if mask.sum() > 500 else a.reshape(-1, 3).mean(0)
    gain = (CREAM / CREAM.mean()) / (ref / ref.mean())
    gain = 1 + (gain - 1) * 0.45 * force                             # correction partielle : les LED restent chaudes
    a = np.clip(a * gain, 0, 1)
    # 2. exposition photographique (gain uniforme) : les matériaux gardent leurs rapports de valeur,
    #    puis épaule douce pour ne pas brûler les plafonds et les LED
    L = lum(a)
    med = np.median(L)
    target = med + (0.58 - med) * force
    e = min(max(target / max(med, 1e-3), 1.0), 1.55)
    Ln = L * e
    knee = 0.80
    Ln = np.where(Ln > knee, knee + (1 - knee) * np.tanh((Ln - knee) / (1 - knee)), Ln)
    ratio = (Ln / np.clip(L, 1e-4, 1))[..., None]
    a = np.clip(a * ratio, 0, 1)
    # 3. ombres ouvertes légèrement + contraste doux en S
    a = a + (1 - a) * 0.04 * force * (1 - a) ** 3
    s = 0.10 * force
    a = a + s * (a - 0.5) * (1 - np.abs(2 * a - 1))
    a = np.clip(a, 0, 1)
    out = Image.fromarray((a * 255 + 0.5).astype(np.uint8))
    # 4. netteté fine
    return out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=45, threshold=2))


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    f = float(sys.argv[sys.argv.index("--force") + 1]) if "--force" in sys.argv else 1.0
    retouch(Image.open(src), f).save(dst, quality=95, subsampling=0)
