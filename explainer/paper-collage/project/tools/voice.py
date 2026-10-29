"""Narrate the script with ElevenLabs (via fal) and write the word timings every scene is timed to.

    python3 tools/voice.py script.txt [--voice Brian]

Writes assets/audio/vo.mp3 and assets/audio/words.json ([word, start, end] in seconds) and prints each sentence with its
start time, so you can set scene starts and item `at` times in film.json. Needs FAL_KEY.
"""
import argparse
import json
import subprocess
from pathlib import Path

from fal import fetch

ROOT = Path(__file__).resolve().parent.parent
AUD = ROOT / "assets/audio"

p = argparse.ArgumentParser()
p.add_argument("script")
p.add_argument("--voice", default="Brian")
a = p.parse_args()
text = " ".join(Path(a.script).read_text().split())

result, paths = fetch("fal-ai/elevenlabs/tts/multilingual-v2",
                      {"text": text, "voice": a.voice, "stability": 0.45, "similarity_boost": 0.75, "style": 0.25, "timestamps": True},
                      AUD / "vo")
words = []
for c in result["timestamps"]:
    cur, s = "", None
    for i, ch in enumerate(c["characters"]):
        if ch.isspace():
            if cur:
                words.append([cur, round(s, 3), round(c["character_end_times_seconds"][i - 1], 3)])
                cur = ""
        else:
            if not cur:
                s = c["character_start_times_seconds"][i]
            cur += ch
    if cur:
        words.append([cur, round(s, 3), round(c["character_end_times_seconds"][-1], 3)])
(AUD / "words.json").write_text(json.dumps(words))
dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(paths[0])],
                     capture_output=True, text=True).stdout.strip()
print(f"vo: {paths[0]} ({dur} s; set audio.vo_length, and audio.length about 2.3 s longer)")
line, t0 = [], None
for w in words:
    t0 = w[1] if not line else t0
    line.append(w[0])
    if w[0][-1] in ".?!":
        print(f"{t0:6.2f}  {' '.join(line)}")
        line = []
if line:
    print(f"{t0:6.2f}  {' '.join(line)}")
