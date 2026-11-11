"""KAÏRA — posting guide for the 12-post feed (instagram-v3), using exactly the 29 existing visuals.

- Builds `livrables/instagram-v3/UPLOAD/POST-NN_.../` with byte-for-byte copies renamed in posting order
  (designs unchanged), plus caption.txt and hashtags.txt for each post.
- Writes GUIDE.md and GUIDE.pdf (thumbnails of every file, carousel order, caption, hashtags, pin).
Usage: python3 tools/make_posting_guide.py
"""
import filecmp, html, json, pathlib, shutil, subprocess
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
V3 = ROOT / "livrables/instagram-v3"
POSTS, EXTRA = V3 / "posts-1080x1350", V3 / "epingles/slides-complementaires"
UP = V3 / "UPLOAD"
B = ROOT / "build/guide"

# posting order, title, source visuals in carousel order, pin position in the top row (None = not pinned)
PLAN = [
    ("01", "Meet KAÏRA", ["01-kaira-1", "01-kaira-2", "01-kaira-3"], 2),
    ("02", "Our Services", ["02-services-1", "02-services-2", "02-services-3"], 3),
    ("03", "The Project — Villa master bedroom", ["03-master-bedroom-1", "03-master-bedroom-2"], 1),
    ("04", "Villa — First-floor lounge", ["04-first-floor-lounge-1", "04-first-floor-lounge-2"], None),
    ("05", "Our process", ["05-our-process-1", "05-our-process-2"], None),
    ("06", "Open-plan living", ["06-open-plan-living-1", "06-open-plan-living-2"], None),
    ("07", "Villa — Dining room", ["07-dining-room-1", "07-dining-room-2"], None),
    ("08", "Villa — Living room", ["08-living-room-1", "08-living-room-2"], None),
    ("09", "Design notes — 5 keys to a calm interior", [f"09-design-notes-{k}" for k in range(1, 7)], None),
    ("10", "Entrance", ["10-entrance-1", "10-entrance-2"], None),
    ("11", "Quote", ["11-quote-1"], None),
    ("12", "Kitchen", ["12-kitchen-1", "12-kitchen-2"], None),
]
SLUG = {"01": "Meet-KAIRA", "02": "Our-Services", "03": "The-Project", "04": "Lounge", "05": "Process", "06": "Open-plan",
        "07": "Dining-room", "08": "Living-room", "09": "Design-notes", "10": "Entrance", "11": "Quote", "12": "Kitchen"}


def src(name):
    post = name.rsplit("-", 1)[0]
    p = POSTS / post / f"{name}.png"
    return p if p.exists() else EXTRA / f"{name}.png"


def caption(num):
    post = next(p for p in POSTS.iterdir() if p.name.startswith(num + "-"))
    text = (post / "caption.txt").read_text().strip()
    paras = text.split("\n\n")
    tags = paras[-1] if paras[-1].startswith("#") else ""
    body = "\n\n".join(paras[:-1] if tags else paras)
    return body, tags


def main():
    if UP.exists():
        shutil.rmtree(UP)
    B.mkdir(parents=True, exist_ok=True)
    rows, total = [], 0
    for num, title, files, pin in PLAN:
        folder = UP / (f"POST-{num}_{SLUG[num]}" + ("_PIN" if pin else ""))
        folder.mkdir(parents=True)
        out = []
        for k, name in enumerate(files, 1):
            s = src(name)
            dst = folder / f"POST-{num}_{k}-of-{len(files)}.png"
            shutil.copyfile(s, dst)
            assert filecmp.cmp(s, dst, shallow=False)
            out.append((dst, s))
            total += 1
        body, tags = caption(num)
        (folder / "caption.txt").write_text(body + "\n")
        (folder / "hashtags.txt").write_text(tags + "\n")
        (folder / "caption+hashtags.txt").write_text(body + "\n\n" + tags + "\n")
        rows.append((num, title, folder, out, body, tags, pin))
    assert total == 29, total
    write_md(rows)
    write_pdf(rows)
    print(total, "files")


def write_md(rows):
    L = ["# KAÏRA Interior Design — Instagram posting guide (12 posts · 29 visuals)", "",
         "All files are in `UPLOAD/`, one folder per post, already named in posting order (exact copies of your designs).", "",
         "| Post | Folder to open | Files to upload, in this order | Type | Pin |", "|---|---|---|---|---|"]
    for num, title, folder, out, body, tags, pin in rows:
        files = "<br>".join(d.name for d, _ in out)
        typ = "Single image" if len(out) == 1 else f"Carousel · {len(out)} images"
        L.append(f"| **{num}** · {title} | `{folder.name}` | {files} | {typ} | {'**Yes** (position ' + str(pin) + ')' if pin else 'No'} |")
    L += ["", "## Posting order", "",
          "1. Publish POST-01, then POST-02, … up to POST-12, in this exact order (same day, a few minutes apart, is ideal).",
          "2. For each post: tap **+** ▸ **Post** ▸ select multiple ▸ tap the files **in the order 1, 2, 3…** ▸ choose the "
          "**4:5 (portrait)** crop icon so nothing is cut ▸ Next ▸ paste `caption+hashtags.txt` ▸ Share.",
          "3. When the 12 are live, pin in this order: **POST-02 Our Services**, then **POST-01 Meet KAÏRA**, then **POST-03 The Project** "
          "(open the post ▸ ••• ▸ Pin to your profile). Instagram shows the last pinned post first, so the top row reads: "
          "The Project · Meet KAÏRA · Our Services. If the order differs, unpin and pin again.",
          "", "Final profile: `apercu-profil.jpg`.", "", "## Captions and hashtags", ""]
    for num, title, folder, out, body, tags, pin in rows:
        L += [f"### POST-{num} · {title}", "", "**Caption**", "", body, "", "**Hashtags**", "", tags, ""]
    (V3 / "GUIDE.md").write_text("\n".join(L) + "\n")


def thumb(path, key):
    t = B / f"t-{key}.jpg"
    Image.open(path).convert("RGB").resize((216, 270), Image.LANCZOS).save(t, quality=88)
    return t.name


def write_pdf(rows):
    shutil.copy(V3 / "apercu-profil.jpg", B / "profil.jpg")
    cards = ""
    for num, title, folder, out, body, tags, pin in rows:
        th = "".join(f'<figure><img src="{thumb(d, d.stem)}"><figcaption>{k}. {d.name}</figcaption></figure>' for k, (d, _) in enumerate(out, 1))
        pin_html = f'<span class="pin">PIN · position {pin}</span>' if pin else '<span class="nopin">Not pinned</span>'
        typ = "Single image" if len(out) == 1 else f"Carousel · {len(out)} images · upload in this order"
        cards += f"""<section class="card"><div class="head"><div class="num">{num}</div><div><div class="t">{html.escape(title)}</div>
<div class="meta">Folder <b>{folder.name}</b> · {typ}</div></div>{pin_html}</div>
<div class="thumbs">{th}</div>
<div class="cap"><div class="lab">Caption</div><p>{html.escape(body).replace(chr(10), '<br>')}</p>
<div class="lab">Hashtags</div><p class="tags">{html.escape(tags)}</p></div></section>"""
    rows_tbl = "".join(f"<tr><td><b>{n}</b></td><td>{html.escape(t)}</td><td>{f.name}</td><td>{len(o)}</td><td>{'Yes · ' + str(p) if p else '—'}</td></tr>"
                       for n, t, f, o, b, tg, p in rows)
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Cormorant;src:url(fonts/cormorant-garamond-latin-400-normal.woff2)}}
@font-face{{font-family:Jost;font-weight:300;src:url(fonts/jost-latin-300-normal.woff2)}}
@font-face{{font-family:Jost;font-weight:400;src:url(fonts/jost-latin-400-normal.woff2)}}
@page{{size:A4;margin:14mm}} body{{font-family:Jost;font-weight:300;color:#2E231D;font-size:9.5pt}}
h1{{font-family:Cormorant;font-weight:400;font-size:28pt;margin:0}} h2{{font-family:Cormorant;font-weight:400;font-size:18pt;margin:18px 0 8px}}
.k{{letter-spacing:.3em;text-transform:uppercase;font-size:7pt;color:#6E2234}}
table{{width:100%;border-collapse:collapse;margin:10px 0}} td,th{{border-bottom:1px solid #E4DACB;padding:5px 4px;text-align:left;font-size:8.5pt}}
th{{font-weight:400;color:#8A7B6E;font-size:7pt;letter-spacing:.2em;text-transform:uppercase}}
ol li{{margin:4px 0}} .card{{page-break-inside:avoid;border-top:2px solid #E4DACB;padding:12px 0 10px}}
.head{{display:flex;gap:12px;align-items:center}} .num{{font-family:Cormorant;font-size:28pt;color:#6E2234;width:42px}}
.t{{font-family:Cormorant;font-size:15pt}} .meta{{color:#8A7B6E;font-size:8pt}} .pin{{margin-left:auto;background:#6E2234;color:#fff;padding:4px 10px;font-size:7.5pt;letter-spacing:.15em}}
.nopin{{margin-left:auto;color:#8A7B6E;font-size:7.5pt}} .thumbs{{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0}}
figure{{margin:0;width:84px}} figure img{{width:84px;height:105px;object-fit:cover;border:1px solid #E4DACB}} figcaption{{font-size:5.5pt;color:#8A7B6E;word-break:break-all}}
.lab{{font-size:6.5pt;letter-spacing:.25em;text-transform:uppercase;color:#5F6A45;margin-top:4px}} .cap p{{margin:3px 0 6px;line-height:1.45}} .tags{{color:#6E2234}}
.prof{{width:60%;display:block;margin:8px auto;border:1px solid #E4DACB}}
</style></head><body>
<div class="k">KAÏRA Interior Design</div><h1>Instagram posting guide</h1>
<p>12 posts · 29 visuals · every file to upload is in <b>instagram-v3/UPLOAD/</b>, one folder per post, already named in order.</p>
<h2>Overview</h2><table><tr><th>Post</th><th>Content</th><th>Folder</th><th>Images</th><th>Pin</th></tr>{rows_tbl}</table>
<h2>Posting order — step by step</h2><ol>
<li>Publish <b>POST-01</b>, then <b>POST-02</b>, … up to <b>POST-12</b>, in this exact order (ideally the same day, a few minutes apart).</li>
<li>For each post: <b>+</b> ▸ <b>Post</b> ▸ select multiple ▸ tap the files in the order <b>1, 2, 3…</b> ▸ choose the <b>4:5 portrait</b> crop so nothing is cut ▸ Next ▸ paste <b>caption+hashtags.txt</b> ▸ Share.</li>
<li>When all 12 are live, pin: <b>POST-02 Our Services</b>, then <b>POST-01 Meet KAÏRA</b>, then <b>POST-03 The Project</b> (open the post ▸ ••• ▸ Pin to your profile). Instagram shows the last pinned first, so the top row reads <b>The Project · Meet KAÏRA · Our Services</b>. If it differs, unpin and pin again.</li></ol>
<h2>Your profile once published</h2><img class="prof" src="profil.jpg">
<h2>Post by post</h2>{cards}</body></html>"""
    shutil.copytree(ROOT / "build/feed12/fonts", B / "fonts", dirs_exist_ok=True)
    (B / "guide.html").write_text(doc, encoding="utf-8")
    js = f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage();
 await p.goto('file://{B / "guide.html"}', {{ waitUntil: 'networkidle' }}); await p.evaluate(() => document.fonts.ready);
 await p.pdf({{ path: '{V3 / "GUIDE.pdf"}', format: 'A4', printBackground: true, margin: {{ top: '14mm', bottom: '14mm', left: '14mm', right: '14mm' }} }});
 await b.close(); }})();"""
    subprocess.run(["node", "-e", js], check=True, cwd=str(ROOT / "tools"))


if __name__ == "__main__":
    main()
