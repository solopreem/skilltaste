#!/bin/bash
# Fetches the stock clips this film uses from Pexels into assets/broll/ (1080p landscape), for regrading with
# tools/cuts.py. The graded cuts already ship in assets/graded/, so you only need this to change the grade or the in-points.
# To re-shoot for another product, swap the IDs (see tools/broll-prompts.md for what each slot needs).
cd "$(dirname "$0")/.."
mkdir -p assets/broll
get() { curl -sSL -o "assets/broll/$1.mp4" "https://www.pexels.com/download/video/$2/?h=1080&w=1920" && echo "$1"; }
get open 3325978
get research 32590005
get receipt 32590005
get whiteboard 5408798
get notebook 7570671
get window 3209550
get greenhouse 5487609
get moss 6772574
get walk 8928272
