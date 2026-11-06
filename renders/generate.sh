#!/usr/bin/env bash
# Generate the four Série Minérale renders with Nano Banana 2
# (gemini-3.1-flash-image). Run from this folder: ./generate.sh
# Each prompt in view-XX-*.txt becomes an image (view-XX-*.png) next to it.
# The API key comes from GEMINI_API_KEY, or from the network proxy in the
# cloud environment (a placeholder is used when it is unset).
set -euo pipefail
cd "$(dirname "$0")"

MODEL="${GEMINI_IMAGE_MODEL:-gemini-3.1-flash-image}"
KEY="${GEMINI_API_KEY:-proxy-injected}"

declare -A RATIO=(
  [view-01-hero-wide]=3:2
  [view-02-fireplace-closeup]=4:5
  [view-03-seating-area]=3:2
  [view-04-evening-lighting]=16:9
)

for name in view-01-hero-wide view-02-fireplace-closeup view-03-seating-area view-04-evening-lighting; do
  echo "Generating $name (${RATIO[$name]})..."
  body=$(python3 -c '
import json, sys
print(json.dumps({
  "contents": [{"parts": [{"text": open(sys.argv[1]).read()}]}],
  "generationConfig": {
    "responseModalities": ["IMAGE"],
    "imageConfig": {"aspectRatio": sys.argv[2]}
  }
}))' "$name.txt" "${RATIO[$name]}")

  curl -sS -N --max-time 300 \
    "https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:streamGenerateContent?alt=sse" \
    -H "x-goog-api-key: ${KEY}" -H "Content-Type: application/json" \
    -d "$body" > "$name.response"

  python3 -c '
import base64, json, sys
name = sys.argv[1]
raw = open(name + ".response").read()
for line in raw.splitlines():
    if not line.startswith("data: "):
        continue
    data = json.loads(line[6:])
    if "error" in data:
        sys.exit("  Gemini error: " + data["error"].get("message", ""))
    for c in data.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            img = p.get("inlineData")
            if img:
                ext = {"image/jpeg": ".jpg", "image/webp": ".webp"}.get(img.get("mimeType"), ".png")
                open(name + ext, "wb").write(base64.b64decode(img["data"]))
                print("  saved " + name + ext)
                sys.exit(0)
sys.exit("  no image returned: " + raw[:300])
' "$name"
  rm -f "$name.response"
done
