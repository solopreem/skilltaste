"""Run a fal.ai model through its queue API and download the files it returns.

    python3 tools/fal.py <endpoint> '<json input>' <out path without extension>

Reads FAL_KEY from the environment or from project/.env. Writes <out>.<ext> (and <out>_N.<ext> for further files)
plus <out>.json with the raw result, and prints the written paths. Used by voice.py and cutout.py.
"""
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def key():
    if os.environ.get("FAL_KEY"):
        return os.environ["FAL_KEY"]
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("FAL_KEY="):
                return line.split("=", 1)[1].strip()
    sys.exit("FAL_KEY not set (export it, or add FAL_KEY=... to project/.env)")


def call(method, url, body=None):
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Key {key()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def run(endpoint, args, poll=3, timeout=1800):
    job = call("POST", f"https://queue.fal.run/{endpoint}", args)
    start = time.time()
    while True:
        if call("GET", job["status_url"])["status"] == "COMPLETED":
            return call("GET", job["response_url"])
        if time.time() - start > timeout:
            sys.exit(f"{endpoint}: timed out (request {job['request_id']})")
        time.sleep(poll)


def files(result):
    if isinstance(result, dict):
        if isinstance(result.get("url"), str) and result["url"].startswith("http"):
            yield result
        for v in result.values():
            yield from files(v)
    elif isinstance(result, list):
        for v in result:
            yield from files(v)


def fetch(endpoint, args, out):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    result = run(endpoint, args)
    out.with_suffix(".json").write_text(json.dumps(result, indent=1))
    paths = []
    for i, f in enumerate(files(result)):
        ext = Path(f.get("file_name") or f["url"].split("?")[0]).suffix or ".bin"
        path = out.parent / f"{out.name}{'' if i == 0 else f'_{i}'}{ext}"
        urllib.request.urlretrieve(f["url"], path)
        paths.append(path)
    return result, paths


if __name__ == "__main__":
    for p in fetch(sys.argv[1], json.loads(sys.argv[2]), sys.argv[3])[1]:
        print(p)
