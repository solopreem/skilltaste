#!/bin/bash
# Gets a machine ready to render a video-skills entry. Safe to re-run: it only installs what is missing.
# Checks node 20+, ffmpeg and python3 (prints how to install them; it does not install system packages),
# then installs the HyperFrames agent skills for every detected agent if they are not there yet.
# Usage: bash scripts/setup.sh
ok=1
need() { command -v "$1" >/dev/null 2>&1 || { echo "missing: $1 ($2)"; ok=0; }; }
need node "https://nodejs.org or: brew install node"
need ffmpeg "brew install ffmpeg, or apt install ffmpeg"
need python3 "https://python.org or: brew install python"
if command -v node >/dev/null 2>&1 && [ "$(node -p 'process.versions.node.split(".")[0]')" -lt 20 ]; then
  echo "node $(node -v) is too old: need 20+"; ok=0
fi

have_skill() { for d in "$HOME/.claude/skills" "$HOME/.agents/skills" "$HOME/.codex/skills" ".claude/skills" ".agents/skills"; do
  [ -f "$d/$1/SKILL.md" ] && return 0; done; return 1; }
if have_skill hyperframes && have_skill hyperframes-cli; then
  echo "hyperframes skills: installed"
elif command -v npx >/dev/null 2>&1; then
  echo "hyperframes skills: installing (user level, all detected agents)"
  npx --yes skills add heygen-com/hyperframes -g -y -s '*' || { echo "skill install failed; run: npx skills add heygen-com/hyperframes -g"; ok=0; }
  echo "Installed skills load in the next session; until then read them from ~/.claude/skills/hyperframes/ (or ~/.agents/skills/)."
fi

[ $ok = 1 ] && echo "ready" || { echo "not ready: fix the lines above"; exit 1; }
