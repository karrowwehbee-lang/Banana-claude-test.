"""Make a queued item's media publicly reachable and record the URLs Instagram will download.

Mode "this-repo" (current): the repository karrowwehbee-lang/Banana-claude-test. is public, so the queue files are
served by raw.githubusercontent.com once they are pushed on the working branch.
Usage: python3 tools/stage_media.py 002
"""
import json
import pathlib
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main(pid):
    cfg = json.loads((ROOT / "media.json").read_text())
    item = next(ROOT.glob(f"queue/{pid}_*"))
    meta = json.loads((item / "post.json").read_text())
    subprocess.run(["git", "-C", str(ROOT), "add", str(item)], check=True)
    subprocess.run(["git", "-C", str(ROOT), "commit", "-q", "-m", f"Instagram media for post {pid}"], check=False)
    subprocess.run(["git", "-C", str(ROOT), "push", "-q", "origin", cfg["branch"]], check=True)
    urls = {f: cfg["raw_base"] + f"queue/{item.name}/{f}" for f in meta["files"]}
    for f, u in urls.items():
        with urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=30) as r:
            assert r.status == 200, (u, r.status)
            print(f, r.headers.get("Content-Type"), u)
    meta["media_urls"] = urls
    (item / "post.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
