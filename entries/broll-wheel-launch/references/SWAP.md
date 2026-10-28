# Swap in another product

The shortest path to the same film for a different product. Everything you change is in `project/film.json`,
`project/assets/` and the b-roll. Nothing in `tools/build.py` changes.

## 1. Fill the slots

| Slot (`film.json`) | What it must be | Size / shape | Used in |
|---|---|---|---|
| `brand.logo` | the real logo file | square, ≥ 512 px | open, refer, end |
| `palette` | the brand's own colours in nine roles: `paper` (light ground), `paper_light` (cards), `paper_edge` (ground edge), `ink` (text), `ground` (dark ground, end card, vault), `ground_light`, `accent` (one loud colour, used only behind ink), `muted` (secondary text), `line` (rules, borders) | hex | everywhere |
| `fonts.display` / `fonts.body` | the brand's fonts as woff2 (a bold display face, a readable body face) | | everywhere |
| `images.illustration` | a wide hero illustration or photo the brand owns | ≈ 3:1, ≥ 2000 px wide | problem (8 s), invite (72 s) |
| `images.mascot` | an object, mascot or product shot | square, transparent or on its own tile | burst landing, refer, trust |
| `images.app` | a real screenshot of the product, signed-out or with demo data | 1500×844 (it sits under a 44 px browser bar) | app (18 s) |
| `images.app.ring`, `cursor_tabs_x/y`, `push_focus` | where the ring lands, the four x positions the cursor visits, the point the camera pushes to | card px | app |
| `images.tools_card`, `images.terms_card` | two crops of real cards from the site or app, each holding 2-3 rows worth circling | ≈ 560-640 × 554 | tools (26 s), terms (46 s) |
| `…_card.rings` | `[x, y, w, h, time]` per row, in crop px, times on beats (1.94, 3.06, 4.06) | | |
| `images.flow` | a five-stage diagram (how it works, a pipeline, a journey) | SVG at 1600×620; `stages_x` = left edge of each stage | proof (54 s) |
| `copy.*` | about twenty lines from the product's own site. Keep each line to the length of the line it replaces (headlines ≤ 32 characters, chips ≤ 18) | | everywhere |
| `copy.refer_number` | the One More Thing payoff: a number from the site (counts up 0→N with `refer_unit`, default %) or a short word shown as it is | number or ≤ 8 characters | refer (66 s) |
| `copy.disclaimer` | optional end-card line, e.g. for an unofficial or spec film | ≤ 90 characters | end |
| `copy.wheel` | six chapter words that finish "Your …" (`wheel_lead`), in film order | one word each | the six wheels |
| `music` | 90 s, 120 BPM, first downbeat ≈ 0.056 s, continuous | see `tools/music.md` | |

Capture the screens from the real product at 2× and crop; never mock up a screen. Anything you had to invent for the story
(a sample session, a worked example) gets an on-screen label (`vault_label`, `terms_label`).

## 2. Replace the b-roll

Nine slots, listed in `project/tools/broll-prompts.md` with what each must show and how long it must be: one ≥ 10 s
establishing shot of a person at work (open, sell, wheel 6), four close or medium shots of the work itself (research,
whiteboard, notebook, window), two calm textures with no people (greenhouse, moss: behind the floating cards), one object
shot (receipt), one walking shot (walk: wheel 5 and keep). Pick the product's world: who uses it, where, with what.

Three ways to fill them, cheapest first:
1. **Keep the shipped footage.** It is generic enough for many products; only the copy and screens change.
2. **Free stock.** Pexels (free to use and modify, no attribution required). Put the new IDs in `project/tools/stock.sh`,
   landscape 1080p or larger, and list them in `assets/broll/CREDITS.md`.
3. **Any text-to-video model.** Use the prompts in `broll-prompts.md`, save each clip as `assets/broll/<slot>.mp4`.

```bash
cd project
./tools/stock.sh                   # or drop your own clips in assets/broll/<slot>.mp4
python3 tools/cuts.py              # cut + grade into assets/graded/, then all-intra into assets/cuts/
```

Move the in-points in `tools/cuts.py` to each clip's best moment. Set the grade in `film.json` `grade` (`all`: the look of
every clip; `under_type`: what is added under type, darker for bright footage), as ffmpeg filters. Segments under type get a slow 6 % push there, so locked-off stock still moves.

## 3. Build, look, render

```bash
python3 tools/build.py
npx --yes hyperframes@0.8.191 check
npx --yes hyperframes@0.8.191 snapshot --at 0,1.5,4.5,7,13,14.2,20,29,32.3,33.8,35.5,40,48,57,67,82,87
npx --yes hyperframes@0.8.191 render -o renders/film.mp4
tools/master.sh renders/film.mp4 film.mp4   # -14 LUFS, peaks under -1 dBTP
```

Look at every snapshot: text over a busy part of the footage, a chip whose text vanished, a caption that runs off the bar.

## Never change

- Scene starts and lengths, and the beat grid (0.06 + 2k s). The music, the SFX table and the cuts are all locked to it.
- The eases and holds in `RECIPE.md`. They are the feel.
- The burst: eight cuts, beat then half-beat, a locked caption, a hard cut to paper on the landing.
- Accent only behind ink. One accent per frame.
- No grain, glow, vignette or flare; the footage carries the texture.

## Shorter cuts

30 s: open (0-6) + wheel1 + sell + app + burst + end, re-timed to the same grid. 15 s vertical: open line, burst, end.
Keep the burst in every cut; it is the film's signature.
