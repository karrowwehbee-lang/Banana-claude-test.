"""KAÏRA — website launch kit for Instagram (held for approval; NOT in the daily queue).

Builds launch/ from screens of the finished website (tools/launch_screens.js) and the phone preview film:
  carousel/1-5.jpg (1080 × 1350), story.jpg (1080 × 1920), reel.mp4 (1080 × 1920, silent AAC) + reel-cover.jpg,
  caption.txt, launch.json (status: awaiting-approval).
Website screens are captures of the approved site, shown whole inside a thin frame; the renders inside them are the
site's display of the studio's unmodified files.   Usage: python3 tools/make_launch.py <phone-film.mp4>
"""
import json
import pathlib
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import studio as S  # noqa: E402

ROOT = HERE.parent
L = ROOT / "launch"
SCR = L / "screens"
K, THEMES, page, sl, mark = S.K, S.THEMES, S.page, S.sl, S.mark
IVORY = "#F7F3EC"


def scr(name):
    return (SCR / name).as_uri()


def frame(name, w, radius=18, dark=True):
    """A website screen shown whole in a thin, quiet frame (no device mock-up)."""
    line = "rgba(247,243,236,.28)" if dark else "rgba(58,42,34,.22)"
    return (f'<div style="width:{w}px;border:2px solid {line};border-radius:{radius}px;overflow:hidden;'
            f'box-shadow:0 60px 120px rgba(0,0,0,.28)"><img src="{scr(name)}" style="display:block;width:100%"></div>')


def phone(name, w):
    return (f'<div style="width:{w}px;border-radius:{round(w * .11)}px;overflow:hidden;border:2px solid rgba(247,243,236,.3);'
            f'box-shadow:0 50px 110px rgba(0,0,0,.35)"><img src="{scr(name)}" style="display:block;width:100%"></div>')


def slides():
    out = []
    bg, ink, acc, sub = THEMES["choc"]
    out.append(sl(page(f"""<div class="abs" style="left:200px;right:200px;top:250px">
 <div class="caps" style="font-size:30px;color:{acc}">KAÏRA Interior Design</div>
 <div class="serif" style="font-size:168px;line-height:1.02;margin-top:56px">The new website</div></div>
<div class="abs" style="left:200px;top:820px">{frame('desktop-home.png', 1760)}</div>
<div class="caps abs" style="left:200px;bottom:250px;font-size:28px;color:{acc}">Now online · link in bio</div>
{mark('choc', '01 / 05', bottom=200)}""", bg, ink)))
    bg, ink, acc, sub = THEMES["white"]
    out.append(sl(page(f"""<div class="abs" style="left:200px;right:200px;top:250px">
 <div class="caps" style="font-size:30px;color:{acc}">A walk through our interiors</div>
 <div class="serif" style="font-size:150px;line-height:1.02;margin-top:56px">Room by room</div></div>
<div class="abs" style="left:200px;top:800px">{frame('desktop-walls.png', 1760, dark=False)}</div>
<div class="abs" style="left:200px;right:760px;bottom:250px;font-size:40px;line-height:1.55;color:{sub}">Each room of the villa opens like a door,
 with the words that guide our work.</div>
{mark('white', '02 / 05', bottom=200)}""", bg, ink)))
    bg, ink, acc, sub = THEMES["olive"]
    phones = "".join(f'<div>{phone(n, 520)}</div>' for n in ("phone-home.png", "phone-founder.png", "phone-reel.png"))
    out.append(sl(page(f"""<div class="abs" style="left:200px;right:200px;top:230px">
 <div class="caps" style="font-size:30px;color:{acc}">On your phone</div>
 <div class="serif" style="font-size:140px;line-height:1.02;margin-top:50px">Made for every screen</div></div>
<div class="abs" style="left:225px;top:900px;display:flex;gap:70px">{phones}</div>
{mark('olive', '03 / 05', bottom=190)}""", bg, ink)))
    out.append(S.numbered("white", "Inside the website", "Four pages", [
        ("Projects", "Six projects, every render shown in full."),
        ("Studio", "The founder, our approach and how we work."),
        ("Services", "Eight disciplines, from the plan to the last joint."),
        ("Contact", "Tell us about your space and start a project.")], size_t=88, pg="04 / 05"))
    out.append(S.solid("burgundy", "Now online", "Visit the<br>new website", "Link in bio<br>@kaira.interior.design", center=True))
    return out


def story():
    bg = "#15110E"
    body = f"""<div class="abs" style="left:0;right:0;top:150px;text-align:center">
 <div class="caps" style="font-size:22px;color:#B9A58E">KAÏRA Interior Design</div>
 <div class="serif" style="font-size:96px;line-height:1.02;margin-top:28px;color:{IVORY}">The new website</div></div>
<div class="abs" style="left:280px;top:430px">{phone('phone-home.png', 520)}</div>
<div class="abs" style="left:0;right:0;bottom:150px;text-align:center">
 <div class="caps" style="font-size:24px;color:{IVORY}">Now online · link in bio</div>
 <div class="word" style="font-size:40px;margin-top:26px;color:{IVORY};margin-right:-.42em">KAÏRA</div></div>"""
    return S._card_png(body, bg, IVORY, L / "story.png")


def reel_bg():
    bg = "#15110E"
    body = f"""<div class="abs" style="left:0;right:0;top:92px;text-align:center">
 <div class="caps" style="font-size:22px;color:#B9A58E">KAÏRA Interior Design</div>
 <div class="serif" style="font-size:76px;line-height:1;margin-top:20px;color:{IVORY}">The new website</div></div>
<div class="abs" style="left:0;right:0;bottom:70px;text-align:center"><div class="caps" style="font-size:24px;color:{IVORY}">Link in bio</div></div>"""
    end = f"""<div class="abs" style="left:0;right:0;top:700px;text-align:center">
 <div class="caps" style="font-size:24px;color:#B9A58E">Now online</div>
 <div class="serif" style="font-size:110px;line-height:1.04;margin-top:44px;color:{IVORY}">Visit the<br>new website</div>
 <div class="caps" style="font-size:24px;color:{IVORY};margin-top:70px">Link in bio · @kaira.interior.design</div>
 <div class="word" style="font-size:44px;margin-top:120px;color:{IVORY};margin-right:-.42em">KAÏRA</div></div>"""
    return [S._card_png(body, bg, IVORY, L / "reel-bg.png"), S._card_png(end, K["burgundy"], IVORY, L / "reel-end.png")]


def shoot(jobs, w, h):
    S.BUILD.mkdir(parents=True, exist_ok=True)
    (S.BUILD / "jobs-launch.json").write_text(json.dumps({"w": w, "h": h, "jobs": jobs}))
    subprocess.run(["node", str(S.IG_TOOLS / "shoot.js"), str(S.BUILD / "jobs-launch.json")], check=True, cwd=str(S.IG_TOOLS))


def make_reel(film):
    """Phone film segments (the real site on a 390 px phone) inside the frame, then an end card. Silent AAC track."""
    vw, vh, x, y = 660, 1428, (1080 - 660) // 2, 262
    mask = Image.new("L", (vw, vh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, vw - 1, vh - 1), radius=64, fill=255)
    mask.save(L / "reel-mask.png")
    segs = [(0.0, 6.5, 1.0), (6.5, 16.0, 2.0), (24.0, 33.5, 1.6), (47.5, 58.5, 2.0)]   # start, end, speed
    parts = "".join(f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{sp},fps=30[s{i}];" for i, (a, b, sp) in enumerate(segs))
    cat = "".join(f"[s{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0[ph];"
    fc = (parts + cat + f"[ph]scale={vw}:{vh},format=rgba[phs];[2:v]format=gray,scale={vw}:{vh}[m];[phs][m]alphamerge[pha];"
          f"[1:v]format=rgba[bg];[bg][pha]overlay={x}:{y}:shortest=1,format=yuv420p[main];"
          f"[3:v]loop=loop=-1:size=1,fps=30,trim=duration=3.2,format=yuv420p,setsar=1[end];"
          f"[main]fps=30,settb=1/30,setsar=1[mn];[end]settb=1/30[en];[mn][en]xfade=transition=fade:duration=0.6:offset=OFFSET[v]")
    dur = sum((b - a) / sp for a, b, sp in segs)
    fc = fc.replace("OFFSET", f"{dur - 0.6:.2f}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(film), "-loop", "1", "-i", str(L / "reel-bg.png"), "-i", str(L / "reel-mask.png"),
                    "-i", str(L / "reel-end.png"), "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
                    "-filter_complex", fc, "-map", "[v]", "-map", "4:a", "-shortest", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(L / "reel.mp4")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "4.2", "-i", str(L / "reel.mp4"), "-frames:v", "1", "-q:v", "2", str(L / "reel-cover.jpg")], check=True)
    for f in ("reel-bg.png", "reel-end.png", "reel-mask.png"):
        (L / f).unlink()
    return dur + 2.6


CAPTION = ("Our new website is online.\n\n"
           "A walk through our interiors, room by room: a family villa, residential interiors, workspaces, a rooftop bar, "
           "a retail showroom and a collection of children's rooms, with every render shown in full. You will also find the "
           "studio's approach, our eight disciplines and the way we work, from the first visit to the finished space.\n\n"
           "Visit it through the link in our bio.\n\n"
           "Interior design & 3D visualization by KAÏRA Interior Design.")
TAGS = ("#kairainteriordesign #interiorarchitecture #interiordesign #luxuryinteriors #interiordesigner #newwebsite "
        "#interiordesignstudio #luxuryhomes #contemporaryinterior #quietluxury #timelessdesign #3dvisualization "
        "#interiorrender #archviz #bespokefurniture #designstudio")

if __name__ == "__main__":
    film = pathlib.Path(sys.argv[1])
    car = L / "carousel"
    files, _ = S.render_slides(slides(), car, "launch")
    S.contact_sheet(car, files)
    shoot([story(), *reel_bg()], 1080, 1920)
    Image.open(L / "story.png").convert("RGB").save(L / "story.jpg", quality=95, icc_profile=S.SRGB)
    (L / "story.png").unlink()
    reel_s = make_reel(film)
    full = CAPTION + "\n\n" + TAGS
    assert len(full) <= 2200
    (L / "caption.txt").write_text(full + "\n")
    meta = {"id": "launch", "slug": "website-launch", "status": "awaiting-approval",
            "rule": "Not part of the daily queue. Publish only after the website is online at its final domain and Karen approves.",
            "carousel": [f"carousel/{f}" for f in files], "reel": "reel.mp4", "reel_cover": "reel-cover.jpg", "story": "story.jpg",
            "reel_seconds": round(reel_s, 1), "caption": CAPTION, "hashtags": TAGS, "full_caption": full}
    (L / "launch.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    print("carousel", files, "| story.jpg | reel.mp4", round(reel_s, 1), "s | caption", len(full), "chars")
