# The entry format

Every entry in `entries/<id>/` has the same files, so you can load any one of them on its own and reproduce its film,
and so entries can be compared and combined. `python3 tools/validate.py` checks this.

Entries follow the Agent Skills layout (`SKILL.md` plus `references/`, `scripts/`, assets), so each one installs as a skill.

```
entries/<id>/
├── SKILL.md          # the agent's instructions: load this folder and make the film
├── taste.json        # machine-readable card: requirements, the seven layers, specs, metrics, what it needs (spec/taste.schema.json)
├── references/
│   ├── floor.md      # the rules every film keeps (a copy of tools/floor.md)
│   ├── RECIPE.md     # the film shot by shot: time, scene, move, sound. The part you do not change
│   ├── SWAP.md       # how to put another product in: the slots, what never changes
│   └── REFERENCE.md  # what it reproduces: the reference's moves and measured numbers (never the reference footage)
├── scripts/          # analyze.py, events.py (copies of tools/)
├── result/
│   ├── result.mp4    # the film this entry produced (released under the entry's licence)
│   ├── poster.jpg    # one frame, 1280 wide
│   ├── sheet.jpg     # one frame every 5 s
│   ├── preview.gif   # ~6 s, for the catalogue
│   └── metrics.json  # measured: cuts, shots, events per 10 s, still share, LUFS, true peak, BPM
└── project/          # a complete, renderable project. Run it as it is and you get result.mp4
    ├── film.json     # everything that is the product: copy, images, geometry, palette, fonts, music
    ├── tools/        # the generator and the asset scripts (b-roll prompts, grading, music)
    └── assets/       # the example product's assets, fonts, SFX, music, b-roll
```

## The seven layers

Each `taste.json` places the entry on the same seven layers. A layer answers one question.

| Layer | Question | Combines how |
|---|---|---|
| `floor` | What is never up for negotiation? | Not merged. The user's rules and the brand win over everything below |
| `category` | What kind of film is it? (launch, explainer, tutorial, data story, social cut, sting) | One per film |
| `method` | How does the picture get made, and how does the spine run? (b-roll under type, one shape never cut, beat montage, 3D UI space, hand-drawn, rebuilt UI) | One per stretch; different stretches can use different methods |
| `moves` | Which concrete moves fill it? (wheel divider, word blur-in, marker sweep, card push-in, anchor montage, pill morph...) | Mix freely, as long as each obeys the method |
| `craft` | What makes the moves look expensive? (hook in 3 s, burst at 30-60 %, holds land on something, hits on landings, -14 LUFS) | Stack all of them |
| `style` | What does it look like? (grade, type, palette roles, texture) | One coherent set per film |
| `tool` | What renders it? (HyperFrames, Remotion, Playwright) | Ideas port across tools; code does not |

When two rules collide, check the layers first: rules on different layers do not conflict. On the same layer,
the order is floor > category > method > moves > craft > style.

## Shared files: copied, not linked

Each entry must work when it is installed on its own, so nothing in it points outside its folder (no `../../`, no symlinks).
Our own shared files (`tools/floor.md`, `tools/analyze.py`, `tools/events.py`) are copied into every
entry; `tools/validate.py` fails when a copy drifts from `tools/`. Edit the file in `tools/`, then copy it again.
Anthropic's own skills repo does the same: docx, pptx and xlsx each carry an identical `scripts/office/`.

External tools are never copied, only declared in `taste.json` `requires`: the renderer at a pinned version
(`hyperframes@0.8.191`, fetched by npx), the skills it expects (`hyperframes`), binaries (node, ffmpeg) and optional keys.

Taste is never shared. Style, motion and pacing rules live in the entry (`SKILL.md` "This film's style rules",
`references/RECIPE.md`), and the entry wins on them. `floor.md` holds only rules no good film of any style would break.

## Rules for every entry

- **Reproducible.** `project/` renders `result.mp4` with no edits and no keys. Footage and music ship in the project (stock as
  graded segments only, with its source IDs and licence; generated media with its prompts), so the film can be remade.
- **Product in one file.** Copy, images, geometry, palette, fonts and music live in `film.json`. Timing, eases, holds and the
  SFX grid live in the generator. Swapping a product never means editing the generator.
- **No reference footage.** `REFERENCE.md` describes and measures the reference; it never redistributes it. Name the entry
  by its method, never by someone else's brand.
- **Truthful product.** Product claims in the example come from the product's own site; illustrative content is labelled on screen.
- **Measured.** `result/metrics.json` comes from `tools/analyze.py` and `tools/events.py`, run on `result.mp4`.
