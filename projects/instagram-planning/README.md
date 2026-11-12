# KAÏRA — Instagram daily management

Strategy: `STRATEGY.md`. Render library: `library.json` (56 renders, built by `tools/studio.py --library`).

## How it works
1. **Content** — `content/posts.py` holds the queue of publications (one per day, in order). `tools/make_post.py <id>`
   renders an item into `queue/<id>_<slug>/`: slides `1.jpg…` (1080 × 1350) or `reel.mp4` + `cover.jpg`, `caption.txt`,
   `post.json` (status `ready` → `published`, media id, permalink), `preview.jpg`.
2. **Media hosting** — Instagram only downloads public files. `tools/stage_media.py <id>` pushes the item's files to the
   public repository named in `media.json` and checks each URL.
3. **Publishing** — the daily scheduled task (17:37 GMT) publishes the next `ready` item through Windsor.ai
   (`create_carousel_post`, `create_image_post`, `create_video_post`), records the media id in `post.json` and
   `history.json`, renders new items so that 5 stay ready, and sends Karen the result and the next preview.
4. **Weekly review** — Sunday 09:37 GMT: performance, strategy adjustments, next week's items.

## Still required before the first publication
- Instagram connected in Windsor.ai (account kaira.interior.design, Business or Creator).
- Public GitHub repository for the media (`media.json`).

Done by hand in the app (no API): pinning, Highlights, music on Reels, location and people tags, collabs.
