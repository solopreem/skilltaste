---
name: broll-wheel-launch
description: Make a 90 s keynote-style product launch film (16:9, 120 BPM) in the "b-roll wheel" style - real-world b-roll under kinetic type, a "Your [ ]" wheel between chapters, the product's real screens floating over footage, an eight-shot beat montage at 35 %, One More Thing, dot-to-logo end. Use when the user asks for this entry by name, picks it from the video-skills gallery, or wants a film that looks like its result/result.mp4. Ships a complete HyperFrames project that renders the example film as is.
---

# broll-wheel-launch

This folder reproduces one film. `result/result.mp4` is what you will get; `project/` renders it unchanged. To make it for
another product you change `project/film.json`, the assets and the b-roll subjects, and nothing else.

Read before you start, in this order:
- `taste.json`: what it needs, what it fits, what it requires
- `references/floor.md`: the rules every film keeps
- `references/RECIPE.md`: this film shot by shot
- `references/SWAP.md`: the slots to fill, and what never changes

## 0. Requirements and fit

- Node 20+, ffmpeg, Python 3. The renderer is pinned and fetched by npx: `hyperframes@0.8.191`.
- The HyperFrames skills (`hyperframes`, `hyperframes-cli`) should be installed for the render contract. If they are missing,
  tell the user to run `npx hyperframes skills update` and restart the agent.
- No keys needed to render: the graded footage ships in `project/assets/graded/`. To regrade it, `project/tools/stock.sh`
  fetches the Pexels originals. To regenerate music: see `project/tools/music.md`.
- Read `taste.json` `fits` / `avoid` against the product. This film needs a real product screen, two real cards worth
  circling, an illustration or mascot, a five-stage diagram and about twenty lines of the product's own copy. If the product
  has no screens, say so and suggest another entry rather than inventing UI.

## 1. Run the example first

```bash
cd project
python3 tools/cuts.py          # assets/graded/ -> assets/cuts/ (all-intra, for exact seeking)
python3 tools/build.py         # writes index.html and compositions/
npx --yes hyperframes@0.8.191 check
npx --yes hyperframes@0.8.191 render -o renders/film.mp4
tools/master.sh renders/film.mp4 film.mp4   # -14 LUFS, peaks under -1 dBTP
```

It should match `result/result.mp4`. The example product's assets (Muse, © Meta) are not shipped; to render the example as is,
recreate them first (`project/assets/THIRD_PARTY.md`), or skip straight to step 2 with your own product.
If the example does not match, fix the environment before swapping anything.

## 2. Swap the product

Follow `references/SWAP.md` §1-3: fill every slot in `film.json` from the real product, replace the nine b-roll clips with the
product's people and places (stock or any video model; the slots are in `project/tools/broll-prompts.md`), regrade, build.

Ask the user only for what you cannot get yourself: the logo file if the site does not expose one, a demo account for
screenshots, permission to show customer data. Write your other choices down and list them at hand-over.

## 3. Look, render, measure

Follow the Process in `references/floor.md`: snapshot the moments in `SWAP.md` §3, read every frame, fix, render, master.
Then measure and compare with this entry's numbers (`result/metrics.json`):

```bash
uv run --with librosa --with numpy --with pillow python -I scripts/analyze.py project/film.mp4 /tmp/m
uv run --with numpy python -I scripts/events.py project/film.mp4 /tmp/m
```

## 4. Deliver

Report the file, what came from the product and what was generated, anything labelled illustrative, the metrics, and what
you could not judge from stills. Do not post it anywhere unless the user asks.

## This film's style rules

These are this entry's taste, not universal rules; they hold for this film.
- No grain, glow, vignette or lens flare; the footage carries the texture. No chime or ding SFX.
- Footage keeps moving under type (slow push or drift); the type itself holds still once it lands.
- One accent colour, only ever behind ink.
- Keep every scene time, ease, hold and SFX cue in `RECIPE.md`.
