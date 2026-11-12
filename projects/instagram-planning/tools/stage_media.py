"""Publish a queued item's media to the dedicated public repository (Instagram downloads them from there).

Privacy rules: the media repository receives ONLY the final Instagram files of the item (1080 × 1350 JPEG slides,
reel.mp4, cover.jpg) — no plans, PDFs, sources, captions, metadata files or personal information. JPEGs must carry no
EXIF data. Commits use a neutral identity.
Usage: python3 tools/stage_media.py 002
Config: media.json {"mode": "media-repo", "owner": "karrowwehbee-lang", "repo": "kaira-instagram-media", "branch": "main"}
"""
import json
import pathlib
import shutil
import subprocess
import sys
import urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALLOWED = {".jpg", ".mp4"}


def git(clone, *args, check=True):
    return subprocess.run(["git", "-C", str(clone), *args], check=check)


def main(pid):
    cfg = json.loads((ROOT / "media.json").read_text())
    assert cfg.get("mode") == "media-repo", "media.json must point to the dedicated media repository"
    clone = ROOT.parent.parent.parent / cfg["repo"]
    if not clone.exists():
        subprocess.run(["git", "clone", "-q", f"https://github.com/{cfg['owner']}/{cfg['repo']}.git", str(clone)], check=True)
    git(clone, "config", "user.name", "KAIRA media")
    git(clone, "config", "user.email", "noreply@anthropic.com")
    git(clone, "pull", "-q", "origin", cfg["branch"], check=False)
    item = next(ROOT.glob(f"queue/{pid}_*"))
    meta = json.loads((item / "post.json").read_text())
    dst = clone / pid
    dst.mkdir(exist_ok=True)
    for f in meta["files"]:
        src = item / f
        assert src.suffix in ALLOWED, f"not an Instagram media file: {f}"
        if src.suffix == ".jpg":
            assert not Image.open(src).getexif(), f"EXIF data in {f}"
        shutil.copy2(src, dst / f)
    extra = [p.name for p in dst.iterdir() if p.name not in meta["files"]]
    assert not extra, f"unexpected files in the media folder: {extra}"
    git(clone, "add", pid)
    git(clone, "commit", "-q", "-m", f"Instagram {pid}", check=False)
    git(clone, "push", "-q", "origin", cfg["branch"])
    base = f"https://raw.githubusercontent.com/{cfg['owner']}/{cfg['repo']}/refs/heads/{cfg['branch']}/{pid}/"
    urls = {f: base + f for f in meta["files"]}
    for f, u in urls.items():
        with urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=30) as r:
            assert r.status == 200, (u, r.status)
            print(f, r.headers.get("Content-Type"), u)
    meta["media_urls"] = urls
    (item / "post.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
