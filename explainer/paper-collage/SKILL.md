---
name: paper-collage
description: Make a 40-45 s narrated explainer (16:9 and 9:16 from one project) in the Vox-style paper-collage look - a true story about a person, a company or an event, one sentence per scene, real photos cut out as white-border stickers, torn paper, newspaper clippings, rubber stamps and typed labels landing on the words they belong to, over b-roll under a halftone screen, with captions and a sources end card. Use when the user asks for this entry by name, picks it from the video-skills gallery, wants a Vox-style or paper-collage explainer, or wants a film that looks like its result/result.mp4. Ships a complete HyperFrames project that renders the example film as is.
---

# paper-collage

This folder reproduces one film. `result/result.mp4` (16:9) and `result/result-9x16.mp4` are what you will get; `project/`
renders them unchanged. To tell another story you change `project/film.json` and `project/assets/`, and nothing else.

Read before you start, in this order:
- `taste.json`: what it needs, what it fits, what it requires
- `references/floor.md`: the rules every film keeps
- `references/sourcing.md`: how to get the facts and the pictures for a true story
- `references/RECIPE.md`: this film beat by beat
- `references/SWAP.md`: the item types and slots in `film.json`, and what never changes

## 0. Requirements and fit

- Run `bash scripts/setup.sh` first, yourself; do not hand it to the user. It checks Node 20+, ffmpeg and Python 3 (and says
  how to install any that are missing) and installs the HyperFrames agent skills (`npx skills add heygen-com/hyperframes`)
  if they are not there. Re-running it is safe.
- Freshly installed skills load in the next session. Do not stop for that: read `~/.claude/skills/hyperframes/SKILL.md`
  (or `~/.agents/skills/hyperframes/`) directly for the render contract. This entry's own generator already follows it.
- The renderer is pinned and fetched by npx: `hyperframes@0.8.191`.
- No keys needed to render the example. A new story needs a narration and music: `FAL_KEY` (ElevenLabs through fal,
  `tools/voice.py`, `tools/music.md`, also used by `tools/cutout.py`). B-roll can be generated with Seedance
  (`BYTEPLUS_API_KEY`, `tools/footage.md`) or taken from stock or the user.
- Read `taste.json` `fits` / `avoid` against the story. This film needs a true story that fits in eight sentences, at least
  two licensed photos of the people in it, and a number or a turn worth stamping. If the user has no story yet, offer two
  or three from this week's news and let them pick.

## 1. Run the example first

```bash
cd project
python3 tools/build.py 16:9                 # writes index.html and compositions/ (or 9:16)
npx --yes hyperframes@0.8.191 check
npx --yes hyperframes@0.8.191 render -o renders/film.mp4
tools/master.sh renders/film.mp4 film.mp4   # -14 LUFS, peaks under -1 dBTP
```

It should match `result/result.mp4`.

## 2. Research, then tell the new story

First follow `references/sourcing.md` yourself: find the facts and a source for each, then the pictures, working down its
list of sources when a site blocks you. Do not invent a fact, a quote or a photo.

- Must be real: the people (licensed photos, cut out, never generated), documents, logos, every claim and number.
  Only atmosphere (b-roll with no people, music) may be generated.
- Look in order: primary sources and Wikimedia Commons → official pages and accounts → open data → only then the user.
  Blocked (Cloudflare, 403)? Do not get around it; take the next source.
- Estimates are labelled and their sum shown; the end card lists sources and photo credits; the film says it is unofficial.

Then follow `references/SWAP.md`: write 90-110 words, show the user the script with its sources before spending on voice
and footage, narrate (`tools/voice.py`), cut out the photos (`tools/cutout.py`), get one b-roll shot per b-roll scene,
fill `film.json` with scenes timed to `assets/audio/words.json`, build both ratios.

## 3. Look, render, measure

Follow the Process in `references/floor.md`: snapshot each scene's last landing in both ratios, read every frame, fix,
render, master. Then measure and compare with this entry's numbers (`result/metrics.json`):

```bash
uv run --with librosa --with numpy --with pillow python -I scripts/analyze.py project/film.mp4 /tmp/m
uv run --with numpy python -I scripts/events.py project/film.mp4 /tmp/m
```

## 4. Deliver

Report both files, the script with its sources, which pictures are real (and their licences) and which media was
generated, the metrics, and what you could not judge from stills (the voice and the mix). Do not post it anywhere unless
the user asks.

## This film's style rules

These are this entry's taste, not universal rules; they hold for this film.
- Paper ground, ink, one red, one yellow. B-roll is always desaturated under the halftone and grain; never shown clean.
- Every piece lands on the word it belongs to, at a small tilt, with its sound. Nothing glides or fades in, except the
  sources line.
- Two to four pieces per scene; at most one picture of the subject per scene.
- Names and numbers in Anton capitals on strips or stamps; everything typed is Special Elite.
- The last line is spoken and shown word for word, then a short sting on a red strip.
