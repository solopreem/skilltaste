"""Makes the footage segments build.py uses. Run before build.py.

Two stages. If the stock originals are in assets/broll/ (tools/stock.sh), each segment is cut and graded into
assets/graded/ (shipped, small). Then every graded segment is re-encoded all-intra into assets/cuts/ (not shipped) so
seeking is frame-exact. Without the originals only the second stage runs.

One grade for every clip (a little warmer, a little less saturated, toward the example's palette); 'dark' segments sit under type
and are pulled down further, and get a slow 6 % push so the footage keeps moving under type even when the stock shot is
locked off (the open is pushed in build.py instead). Edit the table, fetch the originals and re-run.
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, MID, OUT = ROOT / "assets/broll", ROOT / "assets/graded", ROOT / "assets/cuts"
MID.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

GRADE = "eq=contrast=1.04:saturation=0.86,colorbalance=rs=-0.03:gs=0.02:bs=-0.04:rh=0.02:bh=-0.03"
DARK = ",eq=brightness=-0.10:gamma=0.92"
PUSH = 0.06

CUTS = [  # name, source, start, length, speed (0.8 = slowed to 1.25x length), dark
    ("open", "open", 0.0, 6.2, 1, False),
    ("sell0", "open", 6.3, 1.6, 1, False),
    ("wheel6", "open", 7.9, 2.1, 1, False),
    ("wheel1", "notebook", 0.0, 2.1, 1, True),
    ("sell1", "research", 1.0, 0.6, 1, True),
    ("sell2", "whiteboard", 1.0, 1.2, 1, True),
    ("wheel2", "window", 0.0, 2.1, 1, True),
    ("tools", "greenhouse", 10.0, 5.0, 0.8, True),
    ("m0", "research", 6.0, 0.6, 1, False),
    ("m1", "whiteboard", 4.0, 0.6, 1, False),
    ("m2", "notebook", 5.0, 0.6, 1, False),
    ("m3", "walk", 2.5, 0.6, 1, False),
    ("m4", "window", 10.0, 0.4, 1, False),
    ("m5", "greenhouse", 20.0, 0.4, 1, False),
    ("m6", "moss", 18.0, 0.4, 1, False),
    ("m7", "receipt", 4.0, 0.4, 1, False),
    ("wheel3", "moss", 0.0, 2.1, 1, True),
    ("wheel4", "receipt", 0.8, 2.1, 1, True),
    ("terms", "moss", 8.0, 5.0, 0.8, True),
    ("wheel5", "walk", 0.0, 2.1, 1, True),
    ("keep", "walk", 0.0, 4.1, 0.75, True),
]

def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *args], check=True)


for name, src, ss, n, speed, dark in CUTS:
    if (SRC / f"{src}.mp4").exists():
        vf = f"setpts=PTS/{speed}," + GRADE + (DARK if dark else "") + ",scale=1920:1080:flags=lanczos,fps=30"
        if dark:
            z = f"(1+{PUSH}*t/{n})"
            vf += f",format=yuv444p,scale=w='2*trunc(960*{z})':h='2*trunc(540*{z})':eval=frame:flags=bicubic,crop=1920:1080"
        ffmpeg("-ss", str(ss), "-t", str(n), "-i", str(SRC / f"{src}.mp4"), "-an", "-vf", vf,
               "-c:v", "libx264", "-crf", "20", "-preset", "slow", "-pix_fmt", "yuv420p", str(MID / f"{name}.mp4"))
    ffmpeg("-i", str(MID / f"{name}.mp4"), "-c:v", "libx264", "-g", "1", "-crf", "18", "-pix_fmt", "yuv420p", str(OUT / f"{name}.mp4"))
    print(name)
