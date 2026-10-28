#!/bin/bash
# Fetches the nine stock clips this film uses from Pexels into assets/broll/ (1080p landscape), for regrading with
# tools/cuts.py. The graded cuts already ship in assets/cuts/, so you only need this to change the grade or the in-points.
# To re-shoot for another product, swap the IDs (see tools/broll-prompts.md for what each slot needs).
cd "$(dirname "$0")/.."
mkdir -p assets/broll
get() { curl -sSL -o "assets/broll/$1.mp4" "https://www.pexels.com/download/video/$2/?h=1080&w=1920" && echo "$1"; }
get open 32788087
get research 8136080
get whiteboard 5569199
get notebook 6248636
get window 16820075
get greenhouse 38053795
get moss 3224617
get receipt 28827282
get walk 15289229
