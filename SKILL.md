---
name: video-skills
description: Pick and reproduce a reference film from the video-skills library. Every entry (<category>/<id>/, e.g. launch/broll-wheel) is a self-contained skill with a finished result.mp4 and a project that renders it; load one entry and you can remake that exact film for another product. Use when the user asks for a video "like" a video-skills entry, names an entry, or wants a launch/promo film and is happy to choose a style from the gallery.
---

# video-skills

A library of films, one folder per category (`launch/`, later `explainer/`, `social/`...). Each entry under `<category>/<id>/` is one film you can reproduce almost exactly. Entries share one
format (`spec/ENTRY.md`) and one card (`taste.json`), so they can be compared and combined.

## Choosing an entry

1. Read `catalog.json` (one line per entry: id, category, method, length, ratio, what it needs, fits, avoid).
2. Match on **category** first (launch, explainer, social cut...), then on **method** (how the picture is made) against what
   the product actually has: a method that needs real screens is wrong for a product with none.
3. Offer the user one or two entries with their `result/poster.jpg` and one line each on why. If they named one, skip this.

## Using an entry

Open `<category>/<id>/SKILL.md` and follow it. Its first step is `bash scripts/setup.sh`, which you run yourself: it checks
the tools and installs the HyperFrames skills if they are missing. The entry is complete on its own: it runs its example, swaps the product through
`film.json`, regenerates any media and renders.

## Combining entries

Read `spec/ENTRY.md` "The seven layers". One method per stretch of film; moves and craft from other entries can be added
when they obey that method. When rules collide, floor > category > method > moves > craft > style.
