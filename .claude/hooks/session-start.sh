#!/bin/bash
set -euo pipefail

# Claude Code on the web spins up a fresh container per session, so any
# repo-local git config from a previous session is gone. Without this,
# commits fall back to the default Claude Code identity and don't count
# toward the GitHub contribution graph.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

git config user.name "yskkkkkk"
git config user.email "fb1014@naver.com"
