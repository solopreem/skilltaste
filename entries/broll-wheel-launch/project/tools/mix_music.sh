#!/bin/bash
# raw 90 s track -> assets/music_mix.mp3: duck to 0.22 for One More Thing (63.7-66.2 s), fade out from 88.4 s.
cd "$(dirname "$0")/.."
ffmpeg -loglevel error -y -i "$1" -af "volume='if(between(t,63.7,66.2),0.22,1)':eval=frame,afade=t=out:st=88.4:d=1.6" -t 90 assets/music_mix.mp3
