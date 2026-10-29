"""Count visual change events (peaks of frame-to-frame change) and add them to metrics.json."""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np

src, out = Path(sys.argv[1]), Path(sys.argv[2])
log = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(src), "-vf", "scale=320:-2,fps=30,select='gte(scene,0)',metadata=print:key=lavfi.scene_score",
                      "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
t = [float(x) for x in re.findall(r"pts_time:([\d.]+)", log)]
s = np.array([float(x) for x in re.findall(r"scene_score=([\d.]+)", log)])
t = np.array(t[:len(s)])
# smooth over ~0.2s, peaks above an adaptive floor, at least 0.35s apart
k = np.ones(6) / 6
ss = np.convolve(s, k, mode="same")
floor = max(0.004, np.percentile(ss, 60) * 1.5)
ev = []
for i in range(1, len(ss) - 1):
    if ss[i] > floor and ss[i] >= ss[i - 1] and ss[i] >= ss[i + 1]:
        if not ev or t[i] - ev[-1] > 0.35:
            ev.append(round(float(t[i]), 2))
m = json.loads((out / "metrics.json").read_text())
dur = m["duration"]
m["change_events"] = ev
m["events_per_10s"] = round(len(ev) / dur * 10, 1)
m["avg_s_between_events"] = round(dur / max(1, len(ev)), 2)
# share of time that is nearly still (reading holds)
m["still_share"] = round(float((ss < floor * 0.5).mean()), 2)
(out / "metrics.json").write_text(json.dumps(m, indent=1))
print(f"{src.stem:<26} {dur:>6}s events/10s={m['events_per_10s']:>4}  avg_gap={m['avg_s_between_events']:>5}s  still={m['still_share']}")
