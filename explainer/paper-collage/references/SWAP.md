# Tell another story

The shortest path to the same film about a different subject. Everything you change is `project/film.json` and
`project/assets/` (photos, b-roll, narration, music). Nothing in `tools/build.py` changes.

## 1. Research and write (references/sourcing.md)

Find the facts and their sources first. Then write 90-110 words of narration (about 40 s), seven to nine sentences, one
scene per sentence:

1. the hook: a year, a person, a number, an action ("In 2022, a 30-year-old crypto billionaire wrote a $500 million check")
2. who and what (names)
3. the turn
4. the consequence
5. the follow-up
6. "now": the news that makes this worth telling today
7. the number nobody expected
8. where they are now
9. a short last line that can be a headline

Write numbers as words the voice reads well ("500 million dollar", "1.3 billion dollars").

## 2. Narrate

```bash
python3 tools/voice.py script.txt           # assets/audio/vo.mp3 + words.json, prints each sentence's start time
```

Set `audio.vo_length` to the printed length and `audio.length` about 2.3 s longer (the end card holds after the last word).

## 3. Collect the pictures

- People: `uv run --with pillow python tools/cutout.py photo.jpg name` → `assets/img/name-sticker.png`. Licensed photos only.
- Logos (SVG if you can), charts and documents go in `assets/img/` as they are.
- B-roll: one shot per b-roll scene, atmosphere only, no people (`tools/footage.md`; Seedance, stock or your own), cut
  into `assets/footage/` at least as long as the scene.
- Music: `tools/music.md`, cut to `audio.length`.

## 4. Fill film.json

| Slot | What it must be |
|---|---|
| `copy.credit` | optional maker's credit, held 1.2 s before the film, then top right |
| `audio.*` | `vo`, `words`, `vo_length`, `music`, `music_volume` (0.32), `length` |
| `caption_fixes` | `{ "wrong": "right" }` for words the timings split oddly |
| `palette` | `paper`, `ink`, `red`, `yellow` |
| `scenes[]` | `id`, `start` (narration seconds: just before the sentence's first word), `bg` (`"paper"` or a cut in `assets/footage/`), `push` (1.03-1.05), `items[]` |

Each item has `type`, `at` (the narration second of the word it belongs to), `x` (px, or `"c"` to centre; omit for
centre), `y`, a size (`size` for type, `w` for images) and `rot` (degrees, keep it within ±4). Any number can be
`{ "16:9": a, "9:16": b }`.

| Type | Use it for | Extra fields |
|---|---|---|
| `stamp` | a year, a big number | `text`, `color` (red, ink), `box: true` for a bordered rubber stamp |
| `sticker` | a cut-out person | `src`, `alt`, `dy` (how far below it starts) |
| `label` | a typed caption, a dateline, a sum | `text`, `bar` (stretches in first), `per` (seconds per letter) |
| `strip` | a name, a key phrase | `text`, `color` (red, yellow, ink, paper), `from`, `vol`, `css` |
| `card` | a cheque, a note, a receipt | `w`, `lines[]` of `{ style: small/line/big/sign, text, hi }` (`hi`: when the highlighter sweeps it) |
| `news` | a newspaper clipping | `mast`, `head`, `dek`, `size` (headline), `w` |
| `logo` | a real logo on torn paper | `src`, `w`, `pad`, `then: { at, dy, scale }` to shrink it away |
| `rip` | a logo card that tears in half | `src`, `w`, `tear`, `out` |
| `clipping` | a real chart or document, taped | `src`, `w`, `ring: [cx, cy, rx, ry]` in % with `ring_at`, `tape: [x %, deg]` |
| `print` | a photo print, taped | `src`, `w`, `tape` |
| `ticker` | a scrolling tape of text | `text`, `size` |
| `counter` | a number ticking up | `values[]`, `format` (`"${v}B"`), `step` |
| `bar` | a highlighter bar | `w` |
| `headline` | the last line, spoken word by word | `from`, `to` (narration seconds), `w`, `size` |
| `note` | sources and credits | `text` (HTML allowed), `bottom` |

Two to four items per scene. One picture of the subject per scene at most; type does the rest.

## 5. Build and look

```bash
python3 tools/build.py 16:9          # then 9:16
npx --yes hyperframes@0.8.191 check
npx --yes hyperframes@0.8.191 snapshot --at <each scene start + 1.5>,<last item of each scene + 0.4> --no-end -o snapshots .
```

Check in both ratios: no piece leaves the frame; no strip sits in the caption band (bottom 110 px in 16:9, 200-260 px from
the bottom in 9:16); stickers' faces are not covered; every word on screen matches the narration; the end card's
sources line is readable.

## What never changes

The paper and b-roll treatment, the motion vocabulary and its sounds, captions on, the end card with sources, real
photos only for real people, and no generated people in the b-roll.
