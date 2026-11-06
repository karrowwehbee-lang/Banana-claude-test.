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

RESPONSE=$(curl -sS --max-time 120 \
  "https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent" \
  -H "x-goog-api-key: ${KEY}" \
  -H "Content-Type: application/json" \
  -d "$BODY")

python3 -c '
import json, sys
try:
    data = json.loads(sys.argv[1])
except ValueError:
    sys.exit("Gemini error: " + sys.argv[1][:500])
if "error" in data:
    sys.exit("Gemini error: " + data["error"].get("message", str(data["error"])))
parts = data["candidates"][0]["content"]["parts"]
print("".join(p.get("text", "") for p in parts))
' "$RESPONSE"
