"""Prototype sheet: wordmark + monogram options."""
import pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import geometry as G

S = "/tmp/claude-0/-home-user-Banana-claude-test-/302973dd-febb-55dd-a60b-d3d4322e0af4/scratchpad/logo"
pathlib.Path(S).mkdir(parents=True, exist_ok=True)
INK = "#3A2A22"

wm, w, top, bot = G.wordmark()
mono, mw = G.mono_ligature()

# option B : K | A side by side sharing the shadow gap, in an arch
k, kw = G.K()
a, aw = G.A()

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1500" viewBox="0 0 1600 1500" style="background:#F7F3EC">
<g fill="{INK}" transform="translate(150,170)">{''.join(wm)}</g>
<g fill="{INK}" transform="translate(150,520) scale(1.3)">{G.paths_svg(mono)}</g>
<g transform="translate(620,440)" fill="none" stroke="{INK}">{G.arch(380, 480)}</g>
<g fill="{INK}" transform="translate(660,640) scale(1.15)">{G.paths_svg(mono)}</g>
<g transform="translate(1100,440)">
 <rect x="0" y="0" width="380" height="480" fill="#5F6A45"/>
 <g transform="translate(40,40)" fill="none" stroke="#F7F3EC">{G.arch(300, 400, 3)}</g>
 <g fill="#F7F3EC" transform="translate(85,190) scale(0.95)">{G.paths_svg(mono)}</g></g>
<g fill="{INK}" transform="translate(150,1080)">{G.paths_svg(k)}<g transform="translate({kw + 30},0)">{G.paths_svg(a)}</g></g>
</svg>"""
(pathlib.Path(S) / "proto.svg").write_text(svg)
subprocess.run(["node", "-e", f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage({{ viewport: {{ width: 1600, height: 1500 }} }});
await p.goto('file://{S}/proto.svg'); await p.screenshot({{ path: '{S}/proto.png' }}); await b.close(); }})();"""], check=True,
               cwd="/home/user/Banana-claude-test./projects/instagram-lancement/tools")
