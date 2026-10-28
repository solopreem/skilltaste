"""Break down one video: metadata, cuts, contact sheet, loudness, tempo and cut-on-beat ratio."""
import json, re, subprocess, sys
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

def run(*a):
    return subprocess.run(a, capture_output=True, text=True)

probe = json.loads(run("ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(src)).stdout)
v = next(s for s in probe["streams"] if s["codec_type"] == "video")
has_audio = any(s["codec_type"] == "audio" for s in probe["streams"])
dur = float(probe["format"]["duration"])
num, den = map(int, v["r_frame_rate"].split("/"))
fps = num / den

# cuts: big frame-to-frame changes
log = run("ffmpeg", "-hide_banner", "-i", str(src), "-vf", "select='gt(scene,0.22)',showinfo", "-an", "-f", "null", "-").stderr
cuts = [round(float(t), 2) for t in re.findall(r"pts_time:([\d.]+)", log)]
cuts = [c for i, c in enumerate(cuts) if i == 0 or c - cuts[i - 1] > 0.25]
shots = len(cuts) + 1

# contact sheet: 2 fps for short pieces, fewer for long ones, max ~60 tiles per page
rate = 2 if dur <= 45 else (1 if dur <= 70 else 60 / dur)
cols = 6
n = int(dur * rate) + 1
pages = (n + 59) // 60
for p in range(pages):
    start = p * 60 / rate
    run("ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{start}", "-t", f"{60 / rate}", "-i", str(src),
        "-vf", f"fps={rate},scale=320:-2,drawtext=text='%{{pts\\:hms}}':x=6:y=6:fontsize=16:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=3,setpts=PTS+{start}/TB,tile={cols}x10:padding=4:color=white",
        "-frames:v", "1", str(out / f"sheet-{p + 1}.jpg"))

res = {"duration": round(dur, 2), "size": f"{v['width']}x{v['height']}", "fps": round(fps, 2),
       "cuts": cuts, "shots": shots, "avg_shot_s": round(dur / shots, 2), "sheet_rate_fps": round(rate, 3), "has_audio": has_audio}

if has_audio:
    lu = run("ffmpeg", "-hide_banner", "-i", str(src), "-af", "ebur128=peak=true", "-f", "null", "-").stderr
    m = re.search(r"I:\s+(-?[\d.]+) LUFS", lu.split("Summary:")[-1])
    pk = re.search(r"Peak:\s+(-?[\d.]+) dBFS", lu.split("Summary:")[-1])
    res["lufs"] = float(m.group(1)) if m else None
    res["true_peak_dbfs"] = float(pk.group(1)) if pk else None
    wav = out / "_a.wav"
    run("ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", "22050", str(wav))
    import librosa, numpy as np
    y, sr = librosa.load(wav, sr=22050)
    wav.unlink()
    if np.abs(y).max() > 1e-3:
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        bt = librosa.frames_to_time(beats, sr=sr)
        res["bpm"] = round(float(np.atleast_1d(tempo)[0]), 1)
        if len(bt) and cuts:
            d = [float(np.min(np.abs(bt - c))) for c in cuts]
            res["cuts_within_0.1s_of_beat"] = round(sum(x <= 0.1 for x in d) / len(d), 2)
(out / "metrics.json").write_text(json.dumps(res, indent=1))
print(src.stem, json.dumps({k: res[k] for k in res if k != "cuts"}))
