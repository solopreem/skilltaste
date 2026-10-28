<div align="center">

# video-skills

**English** | [中文](README_CN.md)

**A flat, open library of reference films for coding agents. Every entry is one finished film plus everything needed to make it again.**

Load one entry, and your agent can make the same film for your product.

</div>

```bash
npx skills add solopreem/video-skills                       # the whole library (the agent picks an entry)
npx skills add solopreem/video-skills/entries/broll-wheel-launch   # just one film
```

Then, in Claude Code or Codex:

```text
Make a launch film for https://your-product.com with broll-wheel-launch.
```

Nothing else to install by hand: the agent runs the entry's `scripts/setup.sh`, which checks Node 20+, ffmpeg and Python 3
and installs the HyperFrames skills if they are missing. The renderer is fetched by `npx` at a pinned version.

## Why this exists

Video skills today come in two shapes. Some are closed bundles: one style per purchase, fast, but you cannot see inside
or mix them. Others are deep open toolkits, each with its own format, so nothing lines up across them.

video-skills is the flat version of the first, done in the open:

- **One entry = one film.** Each comes with the `result.mp4` it produced, so you choose with your eyes.
- **Reproducible.** Every entry ships a complete project that renders its film unchanged, plus the source IDs for stock footage and the prompts for any generated media. No API keys needed.
- **Same format everywhere.** Every entry has the same files and the same `taste.json` card, so you can compare entries,
  and agents can combine them ([spec/ENTRY.md](spec/ENTRY.md)).
- **Product in one file.** Swapping in your product means editing `film.json` and the assets, never the generator.

## Library

<!-- CATALOG -->
| Preview | Entry | Category · method | Length | Events / 10 s |
|---|---|---|---|---|
| <img src="entries/broll-wheel-launch/result/preview.gif" width="240"> | [**broll-wheel-launch**](entries/broll-wheel-launch/) B-roll wheel launch | launch-film · broll-under-type | 90 s 16:9 | 8.8 |
<!-- /CATALOG -->

## How an entry is built

```
entries/<id>/
├── SKILL.md       load this and make the film
├── taste.json     the card: requirements, seven layers, specs, metrics, what it needs, what it fits
├── references/    floor.md (shared rules), RECIPE.md (shot by shot), SWAP.md (your product in), REFERENCE.md
├── scripts/       measuring and generation scripts
├── result/        result.mp4, poster, contact sheet, preview, metrics.json
└── project/       a renderable project: film.json, tools/, assets/
```

Every entry is placed on the same seven layers:

| Layer | Question |
|---|---|
| floor | What is never up for negotiation? (real product only, labelled samples, the brand) |
| category | What kind of film? (launch, explainer, tutorial, data story, social cut, sting) |
| method | How is the picture made, and how does the spine run? (b-roll under type, one shape never cut, beat montage, 3D UI...) |
| moves | Which concrete moves fill it? (wheel divider, marker sweep, anchor montage, pill morph...) |
| craft | What makes it look expensive? (hook in 3 s, burst near 35 %, hits on landings, -14 LUFS) |
| style | What does it look like? (grade, type, palette roles) |
| tool | What renders it? (HyperFrames, Remotion...) |

Different layers never conflict. On the same layer: floor > category > method > moves > craft > style.

Each entry is self-contained: our shared files (the floor rules, the measuring scripts) are copied into it, external tools
(HyperFrames, ffmpeg) are declared in `taste.json` `requires`, and taste is never shared. See [spec/ENTRY.md](spec/ENTRY.md).

## Tools

| | |
|---|---|
| `tools/floor.md` | the shared floor rules (copied into every entry's `references/`) |
| `tools/validate.py` | checks every entry against the format, and that its copies of the shared files match `tools/` |
| `tools/catalog.py` | rebuilds `catalog.json` and the table above |
| `tools/analyze.py <video> <out>` | cuts, shots, contact sheet, LUFS, true peak, BPM, cuts on the beat |
| `tools/events.py <video> <out>` | visual change events per 10 s and still share |

## Requirements

Node 20+, ffmpeg, Python 3. Entries say what else they need (a renderer version, a video model for b-roll, a music model).

## Contributing

New entries are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md). The bar: the project renders its result unchanged,
the product lives in `film.json`, the result is measured, and nothing from the reference is redistributed.

## Standing on

Ideas and rules borrowed, with thanks, from [HyperFrames](https://hyperframes.heygen.com),
[huashu-motion](https://github.com/alchaincyf/huashu-motion) (rhythm and director notes),
[video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) (recipe cards and the swap guide) and
[product-launch-motion](https://github.com/AbubakrChan/product-launch-motion) (craft details).

## Licence

The broll-wheel-launch example is an unofficial spec film for Muse, Meta's personal AI agent. It is not affiliated with,
endorsed or sponsored by Meta; Muse and its assets are Meta's and are not in this repo.

Code: MIT. Result films and generated media: CC BY 4.0. Example product assets belong to their owners; each entry's
`taste.json` says what may be reused.
