"""KAÏRA website — web copies of the studio's renders, with an integrity report.

Rules: the renders are never cropped, resized, retouched or recoloured.
  * JPEG originals are copied byte for byte (same MD5).
  * PNG originals (villa, children's rooms; 2–5 MB each) are saved once as JPEG q90 with full colour resolution (4:4:4),
    same width and height; the report gives the PSNR against the original pixels (> 40 dB = visually lossless).
  * Renders where a television is switched on are left out (studio preference: screens off).
Output: img/<id>.jpg, img/sizes.json, img/INTEGRITY.json.   Usage: python3 tools/images.py
"""
import hashlib, json, pathlib, shutil
import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
LIB = json.loads((REPO / "projects/instagram-planning/library.json").read_text())
OUT = ROOT / "img"


def md5(p):
    return hashlib.md5(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*.jpg"):
        f.unlink()
    sizes, report = {}, {}
    for rid, v in sorted(LIB.items()):
        if v["tv_on"] or v["dup_of"]:
            continue
        src = REPO / v["path"]
        dst = OUT / f"{rid}.jpg"
        im = Image.open(src)
        if src.suffix.lower() in (".jpg", ".jpeg"):
            shutil.copyfile(src, dst)
            assert md5(src) == md5(dst)
            report[rid] = {"source": v["path"], "method": "byte-identical copy", "md5": md5(dst), "size": list(im.size)}
        else:
            rgb = im.convert("RGB")
            rgb.save(dst, "JPEG", quality=90, subsampling=0, progressive=True, optimize=True)
            a = np.asarray(rgb).astype(np.float64)
            b = np.asarray(Image.open(dst).convert("RGB")).astype(np.float64)
            assert a.shape == b.shape
            psnr = 10 * np.log10(255 ** 2 / ((a - b) ** 2).mean())
            report[rid] = {"source": v["path"], "method": "JPEG q90 4:4:4, same size, no crop or retouch",
                           "psnr_db": round(float(psnr), 1), "size": list(im.size)}
        sizes[rid] = list(im.size)
    (OUT / "sizes.json").write_text(json.dumps(sizes))
    (OUT / "INTEGRITY.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))
    same = sum(1 for r in report.values() if "md5" in r)
    low = min((r["psnr_db"] for r in report.values() if "psnr_db" in r), default=None)
    print(f"{len(report)} renders: {same} byte-identical, {len(report) - same} PNG→JPEG (lowest PSNR {low} dB)")
    print("total", round(sum(f.stat().st_size for f in OUT.glob('*.jpg')) / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
