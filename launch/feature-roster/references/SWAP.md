# Swap in another product

The shortest path to the same film for a different product. Everything you change is in `project/film.json` and
`project/assets/src/`. Nothing in `tools/build.py` changes.

## 1. Take the screenshots

One to three real screenshots of the product, at 2× if you can, signed-out or with demo data. Together they must show,
for every member, the place where that member's work is visible: a row in a list, a message, a card, a result. A product's
own marketing image of its UI counts. Never mock up a screen. Put them in `project/assets/src/` and list each in `shots`
with its pixel size.

## 2. Fill the slots

| Slot (`film.json`) | What it must be | Used in |
|---|---|---|
| `brand.name`, `brand.url` | product name; bare domain or path for the end pill | end |
| `brand.logo_src` | a logo image, dark on light; `mark` and `lockup` are crop boxes `[x0, y0, x1, y1]` (prep.py turns them white) | meet, end |
| `copy.credit` | optional maker's credit, held centred 1.2 s before the film, then top right; adds 1.2 s | credit card |
| `copy.hook_a`, `copy.hook_b` | the problem in two lines from the product's own site or launch post; `*stars*` mark the words that get the underline | hook |
| `copy.meet`, `copy.meet_sub` | "Meet <name>." and the product's one-line promise | meet |
| `copy.end` | the product's tagline, `*stars*` for the underline | end |
| `copy.disclaimer` | optional end line, e.g. for an unofficial or spec film | end |
| `shots.<key>` | `{ file, size: [w, h] }` per screenshot | members |
| `members[]` | 3-6 entries, in film order. Each: `id`, `name` (≤ 18 characters), `line` (the product's own status text for it, ≤ 40 characters), `color` (the member's own colour, taken from its icon), `avatar` `[file, cx, cy, size]` (a square around its icon in a screenshot), `shot` (a key of `shots`), `focus` `[x0, y0, x1, y1]` (where the camera ends), `ring` `[x0, y0, x1, y1]` (the proof it circles), optional `push` (how much wider the camera starts, default 1.36) | members, tab bar, end |
| `palette` | `ground`, `ink`, `muted`, `line`, `panel` | everywhere |
| `fonts.sans`, `fonts.mono` | woff2; the brand's own if it has open ones | everywhere |
| `music` | the film length without the credit card, 120 BPM | see `tools/music.md` |

Boxes are in the screenshot's own pixels. The camera grows each focus box to the panel's shape and keeps it inside the
image, so choose a focus that still reads when it is widened a little; for a tall object (a phone) in 16:9, give a focus
whose centre keeps neighbouring UI out of frame, and lower `push`.

## 3. Build and look

```bash
uv run --with pillow python tools/prep.py
python3 tools/build.py 16:9   # then 9:16
npx --yes hyperframes@0.8.191 snapshot --at 0.6,3.5,6.5,8.0,<each member start + 2.0>,<end + 3.0> --no-end -o snapshots .
```

Check in both ratios: the credit fits the frame; the hook lines do not overlap; every avatar is clean on the dark ground (no
light fringe, nothing clipped); each member's name stays clear of the panel; every ring sits exactly on its proof; no panel
shows past the edge of its screenshot; the end card's disclaimer is readable.

## What never changes

The scene order and lengths, the roster-to-tab-bar handoff, one push and one ring per member, the 1.7× zoom limit, member
colours only on their own dot, ring and tab, and the sound cues.
