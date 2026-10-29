# B-roll

Five 5 s shots generated with Seedance 2.0 (BytePlus ModelArk) at 720p, 16:9, then cut to their scene and scaled to
1920×1080. The shipped files in `assets/footage/` are the cut versions; the film renders without any key.

Rules for this film's b-roll: atmosphere only. A place, an object, a screen. **No people**, no readable brand names, never
a generated stand-in for a real person or a real event. The real people and documents come from photos (`cutout.py`).
Any footage works instead (stock, your own); the look comes from the halftone and grain in `build.py`, not the source.

| File | Scene | Prompt | Cut |
|---|---|---|---|
| servers.mp4 | lab | Slow dolly forward through a dim data center aisle, rows of server racks with small blue and white status lights, haze, cinematic documentary b-roll, no people, no text | first 4.7 s |
| chart.mp4 | collapse | Macro close-up of a trading monitor at night showing a green price chart line that suddenly turns red and plunges, screen glow, shallow depth of field, cinematic documentary b-roll, no people, no readable text or logos | slowed 1.22×, 6.2 s |
| court.mp4 | sentence | Exterior of a neoclassical stone federal courthouse with tall columns at dawn, overcast sky, slow push in from the street, cinematic documentary b-roll, no people | from 0.8 s, 4.1 s |
| ticker.mp4 | ipo | Giant electronic stock ticker wall at night with scrolling green numbers, slow push in, city lights, cinematic documentary b-roll, no people, no readable brand names | first 5.1 s |
| prison.mp4 | prison | Empty prison corridor with steel cell doors, cold fluorescent light flickering slightly, slow dolly forward, cinematic documentary b-roll, no people | from 1.5 s, 3.1 s |

```bash
python3 tools/seedance.py assets/broll/servers.mp4 "<prompt>" --duration 5          # needs BYTEPLUS_API_KEY
ffmpeg -i assets/broll/servers.mp4 -t 4.7 -vf "scale=1920:1080:flags=lanczos" -an -c:v libx264 -crf 18 -pix_fmt yuv420p -r 30 assets/footage/servers.mp4
ffmpeg -i assets/broll/chart.mp4 -vf "setpts=1.22*PTS,scale=1920:1080:flags=lanczos" -t 6.2 -an -c:v libx264 -crf 18 -pix_fmt yuv420p -r 30 assets/footage/chart.mp4
```

A cut must be at least as long as its scene (the next scene's start minus this one's). Run four or five generations in
parallel; each takes about a minute.
