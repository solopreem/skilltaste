# Adding an entry

1. Make the film first. An entry starts from a finished film someone would want to copy, not from a template.
2. Copy the shape of an existing entry: `entries/<new-id>/` with the files listed in [spec/ENTRY.md](spec/ENTRY.md).
   Name it by its method and look (`broll-wheel-launch`), never by another company's brand.
   Copy `tools/floor.md` to `references/floor.md` and `tools/{analyze,events}.py` and `tools/setup.sh` to `scripts/`; do not edit the copies.
   Declare external tools in `taste.json` `requires`. Put the film's own taste in its `SKILL.md` and `RECIPE.md`, not in floor.md.
3. Move everything that is the product into `project/film.json`. Someone swapping products should never open the generator.
4. Ship generated media (b-roll, music) in `project/assets/` and the prompts that made them in `project/tools/`.
5. Measure the result from the repo root:
   ```bash
   uv run --with librosa --with numpy --with pillow python -I entries/<id>/scripts/analyze.py entries/<id>/result/result.mp4 /tmp/m
   uv run --with numpy python -I entries/<id>/scripts/events.py entries/<id>/result/result.mp4 /tmp/m
   cp /tmp/m/metrics.json entries/<id>/result/
   ```
6. `python3 tools/validate.py <id>` must pass, then `python3 tools/catalog.py`.

## The bar

- `project/` renders `result/result.mp4` with no edits.
- Loudness about -14 LUFS, true peak under -1 dBTP.
- Every product claim in the example comes from the product's own material; anything invented is labelled on screen.
- No reference footage, logos or characters are redistributed. `REFERENCE.md` describes and measures; it does not copy.
- You have the right to publish the example product's assets, or you replace them with your own.
