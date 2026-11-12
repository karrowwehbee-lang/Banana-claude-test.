"""Put a queued item's media online (public GitHub repository) and print the public URLs for the Windsor publish call.

Usage: python3 tools/stage_media.py 001
Config: media.json {"owner": "...", "repo": "...", "branch": "main"} — the public repository Karen created.
Instagram downloads the files from https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<id>/<file>.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO_ROOT = ROOT.parent.parent


def main(pid):
    cfg = json.loads((ROOT / "media.json").read_text())
    if not cfg.get("repo"):
        sys.exit("MEDIA REPOSITORY NOT CONFIGURED — Karen must create the public repository (see README).")
    clone = REPO_ROOT.parent / cfg["repo"]
    url = f"https://github.com/{cfg['owner']}/{cfg['repo']}.git"
    if not clone.exists():
        subprocess.run(["git", "clone", url, str(clone)], check=True)
    subprocess.run(["git", "-C", str(clone), "pull", "-q", "origin", cfg.get("branch", "main")], check=False)
    item = next(ROOT.glob(f"queue/{pid}_*"))
    meta = json.loads((item / "post.json").read_text())
    dst = clone / pid
    dst.mkdir(exist_ok=True)
    for f in meta["files"]:
        shutil.copy2(item / f, dst / f)
    subprocess.run(["git", "-C", str(clone), "add", pid], check=True)
    subprocess.run(["git", "-C", str(clone), "commit", "-q", "-m", f"Media for post {pid}"], check=False)
    subprocess.run(["git", "-C", str(clone), "push", "-q", "origin", cfg.get("branch", "main")], check=True)
    base = f"https://raw.githubusercontent.com/{cfg['owner']}/{cfg['repo']}/{cfg.get('branch', 'main')}/{pid}/"
    urls = {f: base + f for f in meta["files"]}
    for f, u in urls.items():          # Instagram must be able to download each file
        with urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=30) as r:
            assert r.status == 200, (u, r.status)
            print(f, r.headers.get("Content-Type"), u)
    meta["media_urls"] = urls
    (item / "post.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
