# KAÏRA — website launch on Instagram

**Status: awaiting approval.** Nothing in this folder is published. It is outside the daily queue (`queue/`), so the
daily 17:37 GMT routine never picks it up. It goes out only after (1) the website is online at its final domain and
(2) Karen says so.

## Contents
| File | Format | Use |
|---|---|---|
| `carousel/1-5.jpg` | 1080 × 1350 | Launch post: the new website, room by room, on every screen, four pages, link in bio |
| `reel.mp4` + `reel-cover.jpg` | 1080 × 1920, ~25 s, silent | The real site running on a phone (opening, villa walk-through, founder, KA reel), end card |
| `story.jpg` | 1080 × 1920 | Story for launch day — add the **link sticker** in the app |
| `caption.txt` | text | Caption + hashtags for the carousel (also fits the Reel) |
| `screens/` | PNG | Screens of the finished website used in the visuals |

The renders seen in these visuals are the website's own display of the studio's unmodified files.

## 1. Link in bio (by hand: Instagram does not allow apps to edit a profile)
**Phone app:** Profile → *Edit profile* → *Links* → *Add external link* → URL: `https://your-domain.com` →
Title: `KAÏRA website` → *Done*.
**Computer:** instagram.com → Profile → *Edit profile* → *Website* → paste the address → *Submit*.

Suggested bio (150 characters max; pick one):

    KAÏRA Interior Design
    Interior architecture · custom furniture · 3D visualization
    Founded by Karen Wehbe
    Discover our new website ↓

    KAÏRA Interior Design — calm, measured interiors
    Residences · workspaces · hospitality · retail
    Founder: Karen Wehbe
    New website ↓

Also worth doing once: *Edit profile → Contact options* → add the studio e-mail so an **E-mail** button appears.

## 2. Launch plan (once the site is online)
1. Send Claude the final address → the site is rebuilt with it (link previews, Google sitemap) and the caption gets
   the address as plain text. Upload the final folder.
2. Add the link in bio (above).
3. **Launch day:** the carousel replaces that day's queued post (the queue simply moves one day); post the Story in the
   app with a link sticker to the site.
4. **The next day:** the Reel. Best posted from the app so you can add music; it can also be published by the
   routine (silent).
5. Pin the carousel to the top of the profile (by hand: *⋯ → Pin to your profile*).

## Rebuild
With the site served on port 8765: `node tools/launch_screens.js launch/screens`, then
`python3 tools/make_launch.py <phone-film.mp4>` (a phone recording of the site, 30 fps).
