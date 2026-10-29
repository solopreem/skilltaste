---
name: feature-roster
description: Make a 25-30 s launch film for social feeds (16:9 and 9:16 from one project, 120 BPM) in the "feature roster" style - a hook in the product's own words, the product's agents, features or modules introduced as a roster that flies up into a tab bar, then one 3 s beat per member with its name, its real status line and a camera push into the real screenshot with a colour ring on the proof, ending on the logo lockup. Use when the user asks for this entry by name, picks it from the video-skills gallery, or wants a film that looks like its result/result.mp4. Ships a complete HyperFrames project that renders the example film as is.
---

# feature-roster

This folder reproduces one film. `result/result.mp4` (16:9) and `result/result-9x16.mp4` are what you will get; `project/`
renders them unchanged. To make it for another product you change `project/film.json` and the screenshots, and nothing else.

Read before you start, in this order:
- `taste.json`: what it needs, what it fits, what it requires
- `references/floor.md`: the rules every film keeps
- `references/sourcing.md`: how to collect the real screens, logo and copy
- `references/RECIPE.md`: this film beat by beat
- `references/SWAP.md`: the slots to fill, and what never changes

## 0. Requirements and fit

- Run `bash scripts/setup.sh` first, yourself; do not hand it to the user. It checks Node 20+, ffmpeg and Python 3 (and says
  how to install any that are missing) and installs the HyperFrames agent skills (`npx skills add heygen-com/hyperframes`)
  if they are not there. Re-running it is safe.
- Freshly installed skills load in the next session. Do not stop for that: read `~/.claude/skills/hyperframes/SKILL.md`
  (or `~/.agents/skills/hyperframes/`) directly for the render contract. This entry's own generator already follows it.
- The renderer is pinned and fetched by npx: `hyperframes@0.8.191`. Pillow (through `uv run --with pillow`) cuts the avatars.
- No keys needed to render. To regenerate music: see `project/tools/music.md`.
- Read `taste.json` `fits` / `avoid` against the product. This film needs 3-6 members (agents, features, modules, plans),
  each with a small icon or avatar, one line of the product's own copy, and one real screenshot that proves it. If the
  product has no screens, say so and suggest another entry rather than inventing UI.

## 1. Run the example first

```bash
cd project
uv run --with pillow python tools/prep.py   # avatars and white logo, cut from assets/src/
python3 tools/build.py 16:9                 # writes index.html and compositions/ (or 9:16)
npx --yes hyperframes@0.8.191 check
npx --yes hyperframes@0.8.191 render -o renders/film.mp4
tools/master.sh renders/film.mp4 film.mp4   # -14 LUFS, peaks under -1 dBTP
```

It should match `result/result.mp4`. The example product's screenshots and logo (Grok Bot) are not shipped; to render the
example as is, download them first (`project/assets/THIRD_PARTY.md`), or skip straight to step 2 with your own product.

## 2. Collect the real material, then swap the product

First follow `references/sourcing.md` yourself: find the product's real screenshots, logo and copy, working down its list
of sources when a site blocks you, and write down where each came from. Do not mock up a screen or rename a feature.

- Must be real: the subject itself, its logo, names and every claim. Only atmosphere (generic b-roll, music) may be borrowed.
- Look in order: its site → press kit, docs, launch post → official social accounts → press coverage → store and listing
    pages it controls → only then the user. Blocked (Cloudflare, 403)? Do not get around it; take the next source.
- Never mock up the subject or rename its parts. Label anything invented for the story.

Then follow `references/SWAP.md`: fill every slot in `film.json`, run `prep.py`, build both ratios. The generator handles 3-6 members; each member adds 3 s, and the music must match the new length.

Ask the user only for what you cannot get yourself: a demo account for screenshots, the logo file if the site does not
expose one, permission to show customer data. Write your other choices down and list them at hand-over.

## 3. Look, render, measure

Follow the Process in `references/floor.md`: snapshot the moments in `SWAP.md` §3 in both ratios, read every frame, fix,
render, master. Then measure and compare with this entry's numbers (`result/metrics.json`):

```bash
uv run --with librosa --with numpy --with pillow python -I scripts/analyze.py project/film.mp4 /tmp/m
uv run --with numpy python -I scripts/events.py project/film.mp4 /tmp/m
```

## 4. Deliver

Report both files, what came from the product and what was generated, the metrics, and what you could not judge from
stills. Do not post it anywhere unless the user asks.

## This film's style rules

These are this entry's taste, not universal rules; they hold for this film.
- One dark ground, white type, the product's screenshots as the only bright thing on screen. No grain, glow or vignette.
- Every member keeps its own colour: its dot, its ring, its tab. Nothing else is coloured.
- The roster is one object: it pops in a row, flies up into the tab bar, the active tab grows, and it gathers again at the end.
- One camera move per member: a slow push into the screenshot, then the ring lands on the proof. Never zoom a screenshot
  past 1.7 screen pixels per source pixel.
- Copy is the product's own words. The member line is the status text the product itself shows for that member.
