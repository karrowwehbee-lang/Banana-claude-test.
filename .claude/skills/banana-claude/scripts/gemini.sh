#!/usr/bin/env bash
# Send a text prompt to Gemini and print the reply.
# Usage: gemini.sh "your prompt"        (or pipe the prompt on stdin)
# Default model: gemini-3.5-flash. Override with GEMINI_MODEL=<model>.
# The API key comes from GEMINI_API_KEY. In the cloud environment the network
# proxy adds the real key, so a placeholder value is used when it is unset.
set -euo pipefail

MODEL="${GEMINI_MODEL:-gemini-3.5-flash}"
KEY="${GEMINI_API_KEY:-proxy-injected}"
PROMPT="${1:-$(cat)}"

BODY=$(python3 -c 'import json,sys; print(json.dumps({"contents":[{"parts":[{"text":sys.argv[1]}]}]}))' "$PROMPT")

# Stream the reply: long answers can take over 30 s, and a non-streamed
# request is cut off by the network proxy at about that point.
RESPONSE=$(curl -sS -N --max-time 300 \
  "https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:streamGenerateContent?alt=sse" \
  -H "x-goog-api-key: ${KEY}" \
  -H "Content-Type: application/json" \
  -d "$BODY")

python3 -c '
import json, sys
raw = sys.argv[1]
text, errors = [], []
chunks = [l[6:] for l in raw.splitlines() if l.startswith("data: ")] or [raw]
for chunk in chunks:
    try:
        data = json.loads(chunk)
    except ValueError:
        sys.exit("Gemini error: " + raw[:500])
    if isinstance(data, list):
        data = data[0] if data else {}
    if "error" in data:
        errors.append(data["error"].get("message", str(data["error"])))
    for c in data.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            text.append(p.get("text", ""))
if errors and not text:
    sys.exit("Gemini error: " + errors[0])
print("".join(text))
' "$RESPONSE"
