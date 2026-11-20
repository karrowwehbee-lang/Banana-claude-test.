"""Split the dossier in two volumes (< 100 MB each, GitHub limit) and check that every render in the PDF
is pixel-identical to its source file."""
import io
import json
import pathlib
import sys

import numpy as np
import pymupdf
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = ROOT.parent.parent
PDF = ROOT / "build/KAIRA-Dossier-technique-Villa-A3.pdf"
OUT = REPO / "livrables"
SRC = REPO / "projects/dossier-client/sources"


def check_renders(doc):
    sources = {}
    for f in SRC.glob("0*/*.png"):
        im = Image.open(f)
        sources.setdefault(im.size, []).append(f)
    seen, ok = set(), 0
    for page in doc:
        for info in page.get_images(full=True):
            xref = info[0]
            if xref in seen:
                continue
            seen.add(xref)
            pix = pymupdf.Pixmap(doc, xref)
            if pix.alpha:
                pix = pymupdf.Pixmap(pix, 0)
            arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
            match = None
            for f in sources.get((pix.width, pix.height), []):
                ref = np.array(Image.open(f).convert("RGB"))
                if ref.shape == arr.shape and np.array_equal(ref, arr):
                    match = f
                    break
            if match is None:
                print("NOT IDENTICAL:", xref, pix.width, pix.height)
                sys.exit(1)
            ok += 1
    print(f"{ok} renders in the PDF, all pixel-identical to their source files")


def main():
    doc = pymupdf.open(PDF)
    check_renders(doc)
    sheets = json.loads((ROOT / "build/sheets.json").read_text())
    cut = next(i for i, s in enumerate(sheets) if s["num"] == "400")
    for name, a, b in (("vol1-RDC", 0, cut - 1), ("vol2-Etage", cut, len(sheets) - 1)):
        out = pymupdf.open()
        out.insert_pdf(doc, from_page=a, to_page=b)
        path = OUT / (PDF.stem + f"-{name}.pdf")
        out.save(path, garbage=4, deflate=True)
        print(path.name, f"pages {a + 1}-{b + 1}", f"{path.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
