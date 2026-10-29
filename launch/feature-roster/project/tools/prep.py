"""Cut the film's small assets out of the official screenshots in assets/src/ (see assets/THIRD_PARTY.md).

Writes assets/img/av-<id>.png (each member's avatar, background flood-filled to transparent, 2x lanczos) and
assets/img/logo-mark.png, assets/img/logo-lockup.png (the black logo turned white on transparent).
Avatar boxes come from film.json `members[].avatar` = [image, x, y, size] in source pixels.
Run: uv run --with pillow python tools/prep.py
"""
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
FILM = json.loads((ROOT / "film.json").read_text())
IMG = ROOT / "assets/img"
IMG.mkdir(parents=True, exist_ok=True)


def cutout(src, x, y, size, out):
    """Square crop centred on (x, y); background connected to the corners becomes transparent."""
    h = size // 2
    im = Image.open(ROOT / src).convert("RGB").crop((x - h, y - h, x + h, y + h))
    key = (255, 0, 255)
    for corner in [(0, 0), (size - 1, 0), (0, size - 1), (size - 1, size - 1)]:
        ImageDraw.floodfill(im, corner, key, thresh=60)
    rgba = im.convert("RGBA")
    rgba.putalpha(ImageChops.difference(im, Image.new("RGB", im.size, key)).convert("L").point(lambda v: 255 if v else 0)
                  .filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.6)))  # eat the light jpeg fringe
    rgba.resize((size * 2, size * 2), Image.LANCZOS).save(out)


def white(src, box, out, scale=2):
    """Dark logo on a light ground -> white logo, alpha from darkness."""
    im = Image.open(ROOT / src).convert("L").crop(box)
    a = im.point(lambda v: 255 - v)
    w = Image.new("RGBA", im.size, (255, 255, 255, 0))
    w.putalpha(a)
    w.resize((im.width * scale, im.height * scale), Image.LANCZOS).save(out)


for m in FILM["members"]:
    src, x, y, size = m["avatar"]
    cutout(src, x, y, size, IMG / f"av-{m['id']}.png")
L = FILM["brand"]["logo_src"]
white(L["file"], L["mark"], IMG / "logo-mark.png")
white(L["file"], L["lockup"], IMG / "logo-lockup.png")
print("prep:", len(FILM["members"]), "avatars, logo")
