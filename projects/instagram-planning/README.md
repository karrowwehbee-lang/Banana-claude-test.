# KAÏRA — Instagram content management

Operating manual for the weekly plan and the daily publishing run.
Account: **@kaira.interior.design** (Instagram id `17841415605783311`, via Windsor.ai). Time zone: **Abidjan (GMT)**.

## Rhythm

| When (GMT) | What | Publishes? |
|---|---|---|
| Sunday 09:37 | Plan for the next week (Mon–Sun): 3 feed posts, 7 Stories, optional Reel. Preview sent for approval. | No |
| Every day 17:37 | Publishes only today's items marked `approved`, checks new comments, sends a 3-line summary. | Only approved items |

Feed posts go out Monday, Wednesday and Friday at 17:37 GMT (18:37 Paris, 12:37 New York, 21:37 Dubai).
Stories go out every day at the same time.

## Rules (from Karen, always apply)

- Nothing is published without Karen's explicit approval.
- Renders are used whole and untouched: no crop, retouch, recolour, regeneration or zoom. Each one is checked pixel for pixel.
- Only renders Karen supplied (`instagram-lancement/sources/recus/`, plus any new ones she sends). No generated images, no Gemini, no paid API.
- If an image needs any processing, ask first.
- The existing 12-post feed is never modified.
- Comments are never deleted. Replies are posted only after approval.

## Approval

The Sunday preview gives every item an id: `W47-F1` (feed post 1), `W47-S3` (Story 3), `W47-R1` (Reel).
Karen answers in the chat:

- `Approved` → everything in the week is approved.
- `Approved except W47-F2` → the others are approved, F2 stays pending.
- `W47-F2: change the caption to …` → I revise and send the item again.
- `Cancel W47-S5` → the item is dropped.

Statuses in `plan.json`: `pending` → `approved` → `published` (or `cancelled`).

## Publishing (daily run)

1. Pick today's items with status `approved`.
2. Convert the PNG to JPEG quality 95 (same pixels, same size, sRGB) because Instagram only accepts JPEG.
3. Push the JPEG to the public media repository so Instagram can download it from a public link.
4. Publish with Windsor.ai: `create_image_post`, `create_carousel_post` (2–10 images), `create_story` or `create_video_post` (Reel).
5. Record the Instagram media id and set the status to `published`, then commit.
6. Draft replies to new comments and send them for approval.

Done by hand in the Instagram app (no API exists): pinning, Highlights, music on Stories/Reels, location and people tags, collabs.

## Folders

```
weeks/<YYYY-Www>/
  plan.json          items, dates, files, captions, hashtags, status
  preview.pdf        what Karen approves
  feed/  stories/  reels/   final 1080×1350 / 1080×1920 PNG
```

## plan.json item

```json
{
  "id": "W47-F1",
  "date": "2026-11-16",
  "time_gmt": "17:37",
  "type": "carousel",
  "files": ["feed/W47-F1_1.png", "feed/W47-F1_2.png"],
  "renders": ["sources/recus/05.png"],
  "caption": "…",
  "hashtags": "#…",
  "status": "pending",
  "media_id": null
}
```

`type` is one of `image`, `carousel`, `story`, `reel`.
