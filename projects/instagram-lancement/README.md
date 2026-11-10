# KAÏRA — Instagram launch (9 posts, built from the studio's own renders)

| Path | Content |
|---|---|
| `sources/recus/` | Renders sent by the studio (`sources/INVENTAIRE.md`) |
| `tools/retouch.py` | Daylight retouch: partial white balance, uniform exposure, soft shoulder, fine sharpening |
| `tools/build_feed.py` | TV screens off → retouch → covers and carousels (1080 × 1350) → `livrables/grille-feed.jpg` |
| `livrables/feed/NN-*/` | Slides of each post (first = cover) + `caption.txt` |
| `livrables/captions.md` | English captions, hashtags, posting order |
| `livrables/KAIRA-instagram-feed.zip` | Everything above in one download |

Grid as shown on the profile once the nine are live (newest top left):

| | | |
|---|---|---|
| 09 The detail | 08 Dining room | 07 Selected projects |
| 06 Lounge | 05 Material palette | 04 Guest bedroom |
| 03 Master bedroom | 02 Living room | 01 Manifesto |

`prompts/` and `tools/generate.py` are the earlier Gemini attempt (not used: the feed uses only the studio's renders).
Nothing is published automatically.
