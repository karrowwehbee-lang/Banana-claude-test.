# KAÏRA — Instagram

**Version finale : `livrables/instagram-final/`** (15 posts, 3 épinglés, 6 Highlights, photo de profil, bio,
`PLAN-DE-LANCEMENT.md`, `KAIRA-Instagram-lancement.zip`). Script : `tools/compose_final.py`.
Les autres dossiers de `livrables/` sont les versions précédentes.

# KAÏRA — Instagram launch (9 posts) — studio's original renders only

Rule: renders are never modified (no crop, resize, retouch, recolouring, generation). Each render is pasted
pixel for pixel at 100 % on a 2160 × 2700 (4:5) slide; only background and typography are drawn around it.

| Path | Content |
|---|---|
| `sources/recus/` | The 16 original renders (`sources/INVENTAIRE.md`) |
| `tools/compose_feed.py` | Builds the slides and checks every render area against the original |
| `livrables/feed/NN-*/` | Slides (PNG, first = cover) + `caption.txt` |
| `livrables/captions.md` | English captions, hashtags, posting order |
| `livrables/verification.txt` | Per-slide proof that the render is identical to the original |
| `livrables/apercu-grille.jpg` | Reduced preview of the profile grid (preview only) |

Not used yet: renders 03, 10, 15, 16 (TV screen showing Netflix), waiting for the studio's decision.
`rendus/originaux/` holds 9 original renders sent to another session (kept untouched, not used in the feeds).

## 12-post version (`livrables/feed-12/`, `tools/compose_feed12.py`)

Full art direction: manifesto, brand palette, belief, approach, detail, services and process, plus the
studio's renders. Ready to post: `instagram-1080x1350/`; HD masters with renders at 100 %: `hd-2160x2700/`.
Renders are always whole and never upscaled; two editorial slides show a render reduced (72 % and 82 %).

## Brand feed (`livrables/feed-marque/`, `tools/compose_feed_brand.py`) — current proposal

12 posts: 3 featured projects with the studio's untouched renders (living room, master bedroom, dining room)
and 9 brand posts (welcome, who we are, palette, signature, quote, design notes, services, promise, contact).
