# KAÏRA — Instagram strategy (daily publishing)

Account: @kaira.interior.design (Instagram id 17841415605783311, via Windsor.ai). Time zone: Abidjan (GMT).
Standing instruction from Karen (12 Nov 2026): one new professional feed publication **every day**, without
per-post approval. Each item is shown to Karen at least 24 h before it goes out; any item she asks to hold or change is
not published until fixed. Nothing is ever reported as published unless Instagram returned a media id.

## Daily rhythm (one feed publication per day, 17:37 GMT = 18:37 Paris, 12:37 New York, 21:37 Dubai)
| Day | Pillar | Format |
|---|---|---|
| Mon | Project spotlight | Carousel: cover + whole renders + design notes |
| Tue | Detail / single render | Single image, cover layout |
| Wed | Reel | 15–25 s slideshow of whole renders, title and end cards |
| Thu | Design notes | Carousel: principle slides + renders (lighting, layout, storage, colour…) |
| Fri | Project spotlight | Carousel (another project or space) |
| Sat | Materials & palette | Carousel: palette sampled from renders + renders |
| Sun | Studio & process | Carousel: process, technical drawings, services, studio philosophy |

Projects rotate: Villa · Residential Interiors · Workspaces · Rooftop Bar & Lounge · Retail Showroom · Children's Rooms.
Never two consecutive posts on the same project. Retail at most once every two weeks (brand logos visible).

## Coverage — nothing left out (Karen, 16 Nov 2026)
Every image Karen sends is published in at least one post. `COVERAGE.md` (built by `tools/coverage.py`) lists each render
and the post that carries it. When writing new specs, take renders first from the ones not yet planned; run
`python3 tools/coverage.py` after each change (it fails while a render has no post). Renders with a screen on and
retail renders follow the rules above (inner slides; retail every two weeks). New images: see README, "New images".
`CALENDAR.md` (built by `tools/calendar.py`) shows the date of every ready post; rebuild it after each publication or new post.

## Visual rules (identical to feed v3)
- 1080 × 1350 (4:5) JPEG for the feed; 1080 × 1920 MP4 for Reels.
- Palette: luminous white, olive, burgundy, chocolate, beige touches. Cormorant + Jost. KAÏRA mark on covers.
- Renders: only Karen's renders (library.json), **whole and unmodified** — pasted at 100 % on the HD slide and verified
  pixel by pixel; never cropped, retouched, recoloured, upscaled or generated. Images 02/03 of the children's folder
  were confirmed as KAÏRA renders by Karen on 16 Nov 2026.
- Renders with a TV screen switched on (flag `tv_on`): never as a cover; at most as an inner slide when useful.

## No repetition
- A render is not used as a cover again within 60 days, nor in any slot within 21 days (history.json + queue).
- Renders already used by the launch feed (05, 07, 09, 13, 20, 21 and chambre-principale-02 / etage1-sejour-02 /
  rdc-salon-11 / rdc-salon-05) wait at least 30 days.
- Titles, opening lines and hashtag sets vary from post to post.

## Captions
English, 3 short paragraphs: a title line, a factual description of what the renders show, a soft call to action
(save, share, DM for enquiries). Credit line "Interior design & 3D visualization by KAÏRA Interior Design" at most
every other post. Never name a client, a location, a date or a price that Karen has not given.
Hashtags: 5 core (#kairainteriordesign #interiorarchitecture #interiordesign #luxuryinteriors #interiordesigner)
+ 8–11 topical from the banks in content/posts.py; 16 maximum. Every hashtag must match what the visuals
show (no #walnut on an oak post, no #marble without marble).

## Buffer
The queue always holds at least 5 ready items. The Sunday run reviews the week's performance (reach, saves, shares,
follows) and adjusts the mix: more of what is saved and shared, less of what is skipped.

## Privacy
The project repository (client plans, dossiers, PDFs, sources) is private. Only finished Instagram media go to the public
repository kaira-instagram-media — never plans, technical drawings of client projects as files, PDFs, captions files,
metadata, or personal information. On Instagram, technical drawings are only shown for
concepts (e.g. the children's rooms collection), never for client projects. If that repository is not reachable, nothing is published (no fallback).

## Review log
**15 Nov 2026 (first weekly review — 4 posts since the daily routine started, plus the 12-post launch feed of 11 Nov).**
Reach per post: Reel 003 *Quiet bedrooms* 94 accounts (134 views); carousels 001 / 004 37 and 26 (004 after < 1 day);
single image 002 34; launch-feed posts 14–60. Engagement is very low everywhere (0–2 likes, 1 save in total, no shares,
no follows attributed to a post) although the profile has 3,831 followers: reach, not content, is the bottleneck.
**Change (test, two weeks):** a second Reel each week — the Friday project spotlight is made as a Reel (first: 010,
20 Nov). Keep it if Reels keep reaching at least twice as many accounts as carousels; otherwise return to one Reel a
week. Hashtags unchanged (no per-hashtag data available through the API).

**16 Nov 2026 — Karen:** integrate all the images she sent into the schedule and publish them along the calendar. Posts 006–029 (16 Nov → 9 Dec) carry every publishable render (118/118), including inner slides that show screens switched on, flags and shop names. Still held until she answers: children's images 02/03 and the three white kitchens (authorship), the villa plans and the two salon top views (client plans).
**16 Nov 2026 — Karen's answers:** the children's images 02/03 and the three white kitchens are KAÏRA designs; the three villa plans and the two salon top views may be published (her decision, an exception to the client-plan rule). Renders wider than the slide are shown whole, scaled down for display only.
**16 Nov 2026 — full check of every file Karen sent (152):** 146 were already in posts; the hand-annotated villa plan
joins 030, and the two photos of her screens (Revit, Blender) make 034 — the Blender photo cut just below its title bar,
which showed her name and a client project name in the file path. Not published: the three Cloudflare dashboard
screenshots (website set-up, not design content; they show the account e-mail).
