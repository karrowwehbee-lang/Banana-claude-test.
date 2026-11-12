"""Assemble index.html: inline the KAÏRA wordmark and emblem (currentColor, tight viewBox) into src/home.html."""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent
LOGO = ROOT.parent / "kaira-logo/logo/svg"


def inline(name):
    s = (LOGO / name).read_text()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    pad = float(re.search(r'translate\(([\d.]+),', s).group(1))
    w, h = vb[2] - 2 * pad, vb[3] - 2 * pad
    s = re.sub(r'<svg [^>]*>', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{pad} {pad} {w:.1f} {h:.1f}" width="100%" '
               f'role="img" aria-label="KAÏRA Interior Design" style="display:block;height:auto">', s, count=1)
    return s.replace('fill="#3A2A22"', 'fill="currentColor"').replace('color="#3A2A22"', 'color="currentColor"')


page = (ROOT / "src/home.html").read_text()
page = page.replace("__WORDMARK__", inline("kaira-5-wordmark-only-chocolate.svg")).replace("__EMBLEM__", inline("kaira-3b-monogram-arch-emblem-chocolate.svg"))
assert "`" not in inline("kaira-5-wordmark-only-chocolate.svg")
(ROOT / "index.html").write_text(page)
print(len(page), "bytes")
