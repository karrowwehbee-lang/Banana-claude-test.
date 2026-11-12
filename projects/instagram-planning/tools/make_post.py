"""Render queued post specs into queue/<id>_<slug>/ (JPEG slides 1080 × 1350 or reel.mp4 + cover.jpg, post.json).

Usage: python3 tools/make_post.py 001 002 …   |   python3 tools/make_post.py --all-missing
"""
import datetime
import importlib.util
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import studio as S

ROOT = HERE.parent
spec = importlib.util.spec_from_file_location("posts", ROOT / "content/posts.py")
posts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(posts)


def build(p):
    out = S.QUEUE / f"{p['id']}_{p['slug']}"
    meta_file = out / "post.json"
    old = json.loads(meta_file.read_text()) if meta_file.exists() else {}
    if old.get("status") == "published":
        print(p["id"], "already published — not rebuilt")
        return
    checks, files = [], []
    if p["kind"] == "reel":
        r = p["reel"]
        dur = S.reel(r["scenes"], r["title"], r["kick"], out)
        files = ["reel.mp4", "cover.jpg"]
        checks = [f"reel {dur:.1f} s — renders shown whole: {', '.join(x for x, _ in r['scenes'])}"]
        from PIL import Image
        Image.open(out / "cover.jpg").resize((360, 640)).save(out / "preview.jpg", quality=88)
    else:
        slides = p["build"](S)
        files, checks = S.render_slides(slides, out, p["id"])
        S.contact_sheet(out, files)
    meta = dict(id=p["id"], slug=p["slug"], pillar=p["pillar"], kind=p["kind"], renders=p["renders"], files=files,
                caption=p["caption"], hashtags=p["hashtags"], full_caption=p["caption"] + "\n\n" + p["hashtags"],
                status=old.get("status", "ready"), created=old.get("created", datetime.date.today().isoformat()),
                published_at=None, media_id=None, permalink=None, checks=checks)
    meta_file.write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    (out / "caption.txt").write_text(meta["full_caption"] + "\n")
    assert len(meta["full_caption"]) <= 2200
    print(p["id"], p["slug"], files)


if __name__ == "__main__":
    ids = sys.argv[1:]
    for p in posts.POSTS:
        missing = not (S.QUEUE / f"{p['id']}_{p['slug']}" / "post.json").exists()
        if p["id"] in ids or ("--all-missing" in ids and missing):
            build(p)
