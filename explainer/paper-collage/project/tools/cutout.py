"""Cut a real photo out of its background (BiRefNet via fal) and give it a white die-cut sticker border.

    uv run --with pillow python tools/cutout.py <photo.jpg> <name>

Writes assets/img/<name>-sticker.png. The subject is only cut out, never redrawn. Needs FAL_KEY. A photo too small or too
flat to cut cleanly works better as a `print` item (a taped rectangular photo) than as a sticker.
"""
import base64
import mimetypes
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

from fal import fetch

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets/img"
src, name = Path(sys.argv[1]), sys.argv[2]
uri = f"data:{mimetypes.guess_type(src.name)[0] or 'image/jpeg'};base64," + base64.b64encode(src.read_bytes()).decode()
_, paths = fetch("fal-ai/birefnet/v2", {"image_url": uri, "model": "General Use (Heavy)", "output_format": "png"}, IMG / f"{name}-cut")

im = Image.open(paths[0]).convert("RGBA")
scale = 1400 / max(im.size)                      # a fixed working size, so every border has the same weight
im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
a = im.getchannel("A").point(lambda v: 255 if v > 110 else 0)
pad = 40
big = Image.new("L", (im.width + 2 * pad, im.height + 2 * pad), 0)
big.paste(a, (pad, pad))
border = big.filter(ImageFilter.MaxFilter(27)).filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 255 if v > 100 else 0)
rgb = ImageEnhance.Contrast(ImageEnhance.Color(im.convert("RGB")).enhance(0.75)).enhance(1.08)
subj = Image.new("RGBA", big.size, (0, 0, 0, 0))
subj.paste(rgb, (pad, pad), a.filter(ImageFilter.GaussianBlur(0.6)))
out = Image.new("RGBA", big.size, (0, 0, 0, 0))
out.paste(Image.new("RGBA", big.size, (250, 247, 240, 255)), (0, 0), border)
out.alpha_composite(subj)
out = out.crop(out.getbbox())
out.save(IMG / f"{name}-sticker.png")
paths[0].unlink()
(IMG / f"{name}-cut.json").unlink(missing_ok=True)
print(IMG / f"{name}-sticker.png", out.size)
