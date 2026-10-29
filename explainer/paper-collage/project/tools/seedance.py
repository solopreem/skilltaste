#!/usr/bin/env python3
"""Generate a video with BytePlus ModelArk Seedance and download it.

usage: seedance.py out.mp4 "prompt" [--duration 5] [--resolution 720p] [--ratio 16:9]
                   [--image first_frame.png] [--audio] [--model dreamina-seedance-2-0-260128]

Reads BYTEPLUS_API_KEY from the environment or from project/.env. BytePlus ModelArk, Seedance 2.0.
"""
import argparse, base64, json, mimetypes, os, sys, time, urllib.request
from pathlib import Path

BASE = "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks"


def key():
    if os.environ.get("BYTEPLUS_API_KEY"):
        return os.environ["BYTEPLUS_API_KEY"]
    env = Path(__file__).resolve().parent.parent / ".env"
    for line in (env.read_text().splitlines() if env.exists() else []):
        if line.startswith("BYTEPLUS_API_KEY="):
            return line.split("=", 1)[1].strip()
    sys.exit("BYTEPLUS_API_KEY not found")


def call(method, url, body=None):
    req = urllib.request.Request(url, method=method,
                                 data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {key()}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{e.code}: {e.read().decode()[:800]}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("out")
    p.add_argument("prompt")
    p.add_argument("--model", default="dreamina-seedance-2-0-260128")
    p.add_argument("--duration", type=int, default=5)
    p.add_argument("--resolution", default="720p")
    p.add_argument("--ratio", default="16:9")
    p.add_argument("--image", help="first-frame image")
    p.add_argument("--audio", action="store_true")
    a = p.parse_args()

    content = [{"type": "text", "text": a.prompt}]
    if a.image:
        mime = mimetypes.guess_type(a.image)[0] or "image/png"
        data = base64.b64encode(Path(a.image).read_bytes()).decode()
        content.append({"type": "image_url", "image_url": {"url": f"data:{mime};base64,{data}"},
                        "role": "first_frame"})
    task = call("POST", BASE, {"model": a.model, "content": content, "resolution": a.resolution,
                               "ratio": a.ratio, "duration": a.duration,
                               "generate_audio": a.audio, "watermark": False})
    tid = task["id"]
    print("task", tid, flush=True)
    t0 = time.time()
    while True:
        time.sleep(10)
        r = call("GET", f"{BASE}/{tid}")
        st = r.get("status")
        if st == "succeeded":
            url = r["content"]["video_url"]
            urllib.request.urlretrieve(url, a.out)
            print(f"saved {a.out} in {time.time() - t0:.0f}s usage={json.dumps(r.get('usage'))}")
            return
        if st in ("failed", "cancelled", "expired"):
            sys.exit(f"{st}: {json.dumps(r.get('error'))}")
        print(st, f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
