"""KAÏRA — Instagram production engine (feed posts, carousels, Reels) in the visual language of feed v3.

- Renders come from the studio library (library.json): pasted whole at 100 % on 2160 × 2700 HD slides (never cropped,
  retouched, recoloured or upscaled; checked pixel by pixel), then the slide is exported at 1080 × 1350 JPEG for Instagram.
- Reels: 1080 × 1920 MP4 (H.264 + silent AAC), each render shown whole on an ivory field with a slow, uncropped scale.

Usage (normally called by make_post.py):  python3 tools/studio.py --library   (rebuilds library.json)
"""
import hashlib
import json
import pathlib
import shutil
import statistics
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent                                   # projects/instagram-planning
REPO = ROOT.parent.parent
IG_TOOLS = REPO / "projects/instagram-lancement/tools"
sys.path.insert(0, str(IG_TOOLS))
import compose_feed12 as base                        # noqa: E402
import compose_v3 as v3                              # noqa: E402

W, H, M = base.W, base.H, base.M                     # 2160 × 2700, margin 246
SRGB = base.SRGB
BUILD = ROOT / "build"
QUEUE = ROOT / "queue"
LIB_FILE = ROOT / "library.json"

# ------------------------------------------------------------------------------------------------ library
VILLA = REPO / "projects/dossier-client/sources"
FEED = REPO / "projects/instagram-lancement/sources/recus"
NEW = REPO / "projects/portfolio-studio/sources/recus"
KIDS = REPO / "projects/portfolio-enfants/sources/recus"

TV_ON = {"rdc-salon-03", "rdc-salon-04", "rdc-salon-07", "etage1-sejour-01", "etage1-sejour-05", "chambre-amis-02",
         "chambre-amis-04", "chambre-principale-04", "r15", "r16", "n07"}
META = {   # id: (project, space)
    "r13": ("Residential Interiors", "Living room & staircase"), "r14": ("Workspaces", "Executive office"),
    "r15": ("Residential Interiors", "Walnut TV wall"), "r16": ("Residential Interiors", "Living room, walnut TV wall"),
    "r19": ("Residential Interiors", "Open living space"), "r20": ("Residential Interiors", "Kitchen"),
    "r21": ("Residential Interiors", "Entrance"),
    "n01": ("Residential Interiors", "L-shaped kitchen"), "n02": ("Residential Interiors", "Gallery dining room"),
    "n03": ("Residential Interiors", "Sculptural living room"), "n04": ("Workspaces", "Private office"),
    "n05": ("Rooftop Bar & Lounge", "Bar"), "n06": ("Residential Interiors", "Dining room"),
    "n07": ("Residential Interiors", "Oak TV wall"), "n08": ("Rooftop Bar & Lounge", "Lounge"),
    "n09": ("Residential Interiors", "Living room, walnut wall"), "n10": ("Retail Showroom", "TV & AC islands"),
    "n11": ("Retail Showroom", "Brand zones"), "n12": ("Retail Showroom", "Audio islands"),
    "n13": ("Retail Showroom", "Air-conditioning wall"), "n14": ("Retail Showroom", "Appliance hall"),
    "n15": ("Retail Showroom", "TV wall"), "n16": ("Retail Showroom", "Display units"),
    "k01": ("Children's Rooms", "Douceur Lapin"), "k04": ("Children's Rooms", "Nuages"),
    "k05": ("Children's Rooms", "Ourson Caramel"), "k06": ("Children's Rooms", "Jungle Douce"),
    "k07": ("Children's Rooms", "Nuage Olive"),
}
VILLA_SPACE = {"01-rdc-salon-principal": "Living & dining room", "02-chambre-amis": "Guest bedroom",
               "03-chambre-principale": "Master bedroom", "04-etage1-sejour": "First-floor living room"}


def build_library():
    lib, seen = {}, {}
    for f in sorted(VILLA.glob("0*/*.png")):
        lib[f.stem] = dict(path=str(f.relative_to(REPO)), project="Villa", space=VILLA_SPACE[f.parent.name])
    for f in sorted(FEED.glob("*.*")):
        if f.suffix == ".jpg":
            lib["r" + f.stem] = dict(path=str(f.relative_to(REPO)), project=META["r" + f.stem][0], space=META["r" + f.stem][1])
    for f in sorted(NEW.glob("*.jpg")):
        lib["n" + f.stem] = dict(path=str(f.relative_to(REPO)), project=META["n" + f.stem][0], space=META["n" + f.stem][1])
    for k in ("01", "04", "05", "06", "07"):          # 02 and 03 are inspirations: never published
        f = KIDS / f"{k}.png"
        lib["k" + k] = dict(path=str(f.relative_to(REPO)), project="Children's Rooms", space=META["k" + k][1])
    for k, d in lib.items():
        p = REPO / d["path"]
        im = Image.open(p)
        d["size"] = list(im.size)
        d["tv_on"] = k in TV_ON
        d["brands"] = d["project"] == "Retail Showroom"
        h = hashlib.md5(p.read_bytes()).hexdigest()
        d["dup_of"] = seen.get(h)
        seen.setdefault(h, k)
    LIB_FILE.write_text(json.dumps(lib, indent=1, ensure_ascii=False))
    return lib


def library():
    return json.loads(LIB_FILE.read_text()) if LIB_FILE.exists() else build_library()


def original(rid):
    return Image.open(REPO / library()[rid]["path"]).convert("RGB")


def size(rid):
    return tuple(library()[rid]["size"])


def sample(rid, box):
    im = original(rid).crop(box)
    px = np.asarray(im).reshape(-1, 3).astype(int)
    return "#%02X%02X%02X" % tuple(int(statistics.median(px[:, i])) for i in range(3))


# ------------------------------------------------------------------------------------------------ slide templates
THEMES, K, page, sl, mark = v3.THEMES, v3.K, v3.page, v3.sl, v3.mark


def cover(rid, theme, kick, title, num):
    """Whole render at 100 % with the title below (feed v3 cover)."""
    bg, ink, acc, sub = THEMES[theme]
    w, h = size(rid)
    x, y = (W - w) // 2, M
    t = (f'<div class="abs" style="left:{x}px;top:{y + h + 90}px;right:{x + 520}px"><div class="caps" style="font-size:30px;color:{acc}">{kick}</div>'
         f'<div class="serif" style="font-size:{136 if h < 1700 else 118}px;line-height:1;margin-top:26px">{title}</div></div>'
         + mark(theme, num, right=x, bottom=max(120, H - (y + h) - 560)))
    return sl(page(t, bg, ink), [(rid, x, y, w)])


def render_slide(rid, theme, label, pg=""):
    """Inner slide: whole render, centred, a discreet caption."""
    bg, ink, acc, sub = THEMES[theme]
    w, h = size(rid)
    x = (W - w) // 2
    y = max(M, (H - h - 170) // 2)
    t = (f'<div class="abs" style="left:{x}px;right:{x}px;top:{y + h + 54}px;display:flex;justify-content:space-between">'
         f'<div class="caps" style="font-size:24px;color:{sub}">{label}</div>'
         f'<div class="caps" style="font-size:24px;color:{acc}">{pg}</div></div>')
    return sl(page(t, bg, ink), [(rid, x, y, w)])


def palette_slide(theme, kick, title, chips, text=""):
    bg, ink, acc, sub = THEMES[theme]
    line = K["line"] if theme == "white" else "rgba(247,243,236,.3)"
    ch = "".join(f'<div><div style="height:640px;background:{hx};border:2px solid {line}"></div>'
                 f'<div class="serif" style="font-size:46px;margin-top:26px;line-height:1.1">{nm}</div>'
                 f'<div class="caps" style="font-size:20px;color:{sub};margin-top:12px">{hx}</div></div>' for nm, hx in chips)
    n = len(chips)
    return sl(page(f"""<div class="abs" style="left:200px;right:200px;top:230px"><div class="caps" style="font-size:30px;color:{acc}">{kick}</div>
 <div class="serif" style="font-size:150px;line-height:1.02;margin-top:44px">{title}</div>
 {f'<div style="font-size:40px;line-height:1.6;color:{sub};margin-top:50px;max-width:1500px">{text}</div>' if text else ''}</div>
<div class="abs" style="left:200px;right:200px;bottom:330px;display:grid;grid-template-columns:repeat({n},1fr);gap:36px">{ch}</div>
<div class="word abs" style="right:200px;bottom:170px;font-size:44px;margin-right:-.42em">KAÏRA</div>""", bg, ink))


def drawing_slide(svg, kick, title, note):
    bg, ink, acc, sub = THEMES["white"]
    sys.path.insert(0, str(REPO / "projects/dossier-technique/tools"))
    from draw import PATTERNS
    return sl(page(f"""{PATTERNS}<div class="abs" style="left:200px;right:200px;top:220px"><div class="caps" style="font-size:30px;color:{acc}">{kick}</div>
 <div class="serif" style="font-size:120px;line-height:1.02;margin-top:36px">{title}</div></div>
<div class="abs dwg" style="left:200px;right:200px;top:640px;height:1500px;display:flex;align-items:center;justify-content:center">{svg}</div>
<div class="abs" style="left:200px;right:700px;bottom:200px;font-size:34px;line-height:1.55;color:{sub}">{note}</div>
<div class="word abs" style="right:200px;bottom:200px;font-size:44px;margin-right:-.42em">KAÏRA</div>
<style>.dwg svg{{width:1760px!important;height:auto!important;max-height:1500px}}</style>""", bg, ink))


solid, numbered = v3.solid, v3.numbered


# ------------------------------------------------------------------------------------------------ rendering
def render_slides(slides, outdir, stem="slide"):
    """HTML → PNG background → paste renders at 100 % (verified) → 1080 × 1350 JPEG (q95, sRGB)."""
    BUILD.mkdir(parents=True, exist_ok=True)
    shutil.copytree(base.FONTS, BUILD / "fonts", dirs_exist_ok=True)
    outdir.mkdir(parents=True, exist_ok=True)
    jobs, plan = [], []
    for i, s in enumerate(slides, 1):
        h = BUILD / f"{outdir.name}-{i}.html"
        h.write_text(s["html"], encoding="utf-8")
        jobs.append([str(h), str(BUILD / f"{outdir.name}-{i}.png")])
        plan.append((i, s["imgs"], BUILD / f"{outdir.name}-{i}.png"))
    (BUILD / "jobs.json").write_text(json.dumps({"w": W, "h": H, "jobs": jobs}))
    subprocess.run(["node", str(IG_TOOLS / "shoot.js"), str(BUILD / "jobs.json")], check=True, cwd=str(IG_TOOLS))
    files, checks = [], []
    for i, imgs, bgp in plan:
        canvas = Image.open(bgp).convert("RGB")
        for rid, x, y, w in imgs:
            src = original(rid)
            assert w == src.width, "renders are pasted at 100 % only"
            canvas.paste(src, (x, y))
            assert np.array_equal(np.asarray(canvas)[y:y + src.height, x:x + src.width], np.asarray(src))
            checks.append(f"{stem}-{i}: {rid} whole, 100 %, pixel-identical on the HD slide")
        out = outdir / f"{i}.jpg"
        canvas.resize((1080, 1350), Image.LANCZOS).save(out, quality=95, icc_profile=SRGB, optimize=True)
        files.append(out.name)
    return files, checks


def contact_sheet(outdir, files, cols=None):
    ims = [Image.open(outdir / f).convert("RGB") for f in files]
    tw = 360
    ims = [im.resize((tw, round(im.height * tw / im.width))) for im in ims]
    cols = cols or len(ims)
    rows = (len(ims) + cols - 1) // cols
    th = max(im.height for im in ims)
    sheet = Image.new("RGB", (cols * tw + (cols - 1) * 8, rows * th + (rows - 1) * 8), "#FFFFFF")
    for k, im in enumerate(ims):
        sheet.paste(im, ((k % cols) * (tw + 8), (k // cols) * (th + 8)))
    sheet.save(outdir / "preview.jpg", quality=88)


# ------------------------------------------------------------------------------------------------ reels
RW, RH, FPS = 1080, 1920, 30


def _card_png(html_body, bg, ink, out):
    css = base.FACES + """*{margin:0;padding:0;box-sizing:border-box} html,body{width:1080px;height:1920px;overflow:hidden}
body{font-family:Jost;font-weight:300;position:relative;-webkit-font-smoothing:antialiased}
.serif{font-family:Cormorant;font-weight:300} .caps{font-family:Jost;font-weight:400;text-transform:uppercase;letter-spacing:.34em}
.word{font-family:Cormorant;font-weight:400;letter-spacing:.42em} .abs{position:absolute}"""
    h = BUILD / (out.stem + ".html")
    h.write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>'
                 f'<body style="background:{bg};color:{ink}">{html_body}</body></html>', encoding="utf-8")
    return [str(h), str(out)]


def reel(scenes, title, kick, outdir, end_line="Interior architecture &amp; design"):
    """scenes: [(render id, label)]. Writes reel.mp4 and cover.jpg."""
    BUILD.mkdir(parents=True, exist_ok=True)
    shutil.copytree(base.FONTS, BUILD / "fonts", dirs_exist_ok=True)
    outdir.mkdir(parents=True, exist_ok=True)
    ivory, ink, burg, mute = K["white"], K["ink"], K["burgundy"], K["mute"]
    tag = outdir.name
    jobs = [_card_png(f"""<div class="abs" style="left:110px;right:110px;top:700px"><div class="caps" style="font-size:24px;color:{burg}">{kick}</div>
<div class="serif" style="font-size:118px;line-height:1.02;margin-top:40px">{title}</div>
<div style="width:110px;height:3px;background:{burg};margin-top:70px"></div></div>
<div class="word abs" style="left:0;right:0;text-align:center;bottom:200px;font-size:40px">KAÏRA</div>""", ivory, ink, BUILD / f"{tag}-title.png"),
            _card_png(f"""<div class="abs" style="left:0;right:0;top:780px;text-align:center"><div class="word" style="font-size:96px;margin-right:-.42em">KAÏRA</div>
<div class="caps" style="font-size:22px;color:{mute};margin-top:26px">Interior design</div>
<div class="caps" style="font-size:24px;color:{burg};margin-top:120px">{end_line}</div>
<div class="serif" style="font-size:52px;margin-top:40px">@kaira.interior.design</div></div>""", ivory, ink, BUILD / f"{tag}-end.png")]
    for k, (rid, label) in enumerate(scenes):
        jobs.append(_card_png(f"""<div class="word abs" style="left:0;right:0;text-align:center;top:170px;font-size:36px">KAÏRA</div>
<div class="caps abs" style="left:0;right:0;text-align:center;bottom:250px;font-size:24px;color:{mute}">{label}</div>""",
                              ivory, ink, BUILD / f"{tag}-s{k}.png"))
    (BUILD / "reeljobs.json").write_text(json.dumps({"w": RW, "h": RH, "jobs": jobs}))
    subprocess.run(["node", str(IG_TOOLS / "shoot.js"), str(BUILD / "reeljobs.json")], check=True, cwd=str(IG_TOOLS))
    title_bg = Image.open(BUILD / f"{tag}-title.png").convert("RGB")
    end_bg = Image.open(BUILD / f"{tag}-end.png").convert("RGB")
    shutil.copy(BUILD / f"{tag}-title.png", outdir / "cover.png")
    title_bg.save(outdir / "cover.jpg", quality=95)

    def scene_frames(k, rid, n):
        bg = Image.open(BUILD / f"{tag}-s{k}.png").convert("RGB")
        src = original(rid)
        out = []
        for f in range(n):            # whole render, scale 940 → 990 px wide: always entirely visible, never cropped
            w = int(round(940 + 50 * f / max(1, n - 1)))
            h = round(src.height * w / src.width)
            fr = bg.copy()
            fr.paste(src.resize((w, h), Image.LANCZOS), ((RW - w) // 2, (RH - h) // 2 - 20))
            out.append(fr)
        return out

    seq = [[title_bg] * int(2.2 * FPS)] + [scene_frames(k, rid, int(3.3 * FPS)) for k, (rid, _) in enumerate(scenes)] \
        + [[end_bg] * int(2.6 * FPS)]
    xf = int(0.5 * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{RW}x{RH}", "-r", str(FPS),
           "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest", "-c:v", "libx264", "-preset", "slow",
           "-crf", "19", "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
           str(outdir / "reel.mp4")]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    total = 0
    for si, frames in enumerate(seq):
        nxt = seq[si + 1] if si + 1 < len(seq) else None
        body = frames[:-xf] if nxt else frames
        for fr in body:
            p.stdin.write(fr.tobytes()); total += 1
        if nxt:
            for j in range(xf):
                a = frames[len(frames) - xf + j]
                b = nxt[j]
                p.stdin.write(Image.blend(a, b, (j + 1) / (xf + 1)).tobytes()); total += 1
            seq[si + 1] = nxt[xf:]
    p.stdin.close()
    p.wait()
    assert p.returncode == 0
    return total / FPS



def elevation_svg(room, wall, scale=25):
    """Technical elevation from the KAÏRA technical dossier (projects/dossier-technique)."""
    sys.path.insert(0, str(REPO / "projects/dossier-technique/tools"))
    import views
    svg, w, h = views.elev_view(room, wall, scale=scale, show_dims=True, show_levels=True)
    return svg


if __name__ == "__main__":
    if "--library" in sys.argv:
        lib = build_library()
        print(len(lib), "renders;", sum(1 for d in lib.values() if d["dup_of"]), "duplicates")
