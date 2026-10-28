#!/bin/bash
# Masters a render to -14 LUFS with peaks held under -1 dBTP (measure, apply the gain, limit). The video stream is copied untouched.
# Usage: tools/master.sh renders/film.mp4 film.mp4
set -e
I=$(ffmpeg -nostats -i "$1" -af ebur128 -f null - 2>&1 | awk '/I:/{v=$2} END{print v}')
G=$(python3 -c "print(round(-14 - $I, 2))")
ffmpeg -loglevel error -y -i "$1" -c:v copy -movflags +faststart -af "volume=${G}dB,alimiter=limit=0.75:level=false:attack=1:release=60" -c:a aac -b:a 192k "$2"
ffmpeg -nostats -i "$2" -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
