# Reference

**What it reproduces:** the structure of a 20.5 s team film we made earlier for an AI marketing product (four AI employees
introduced as one team; not redistributed here), generalised into a generator for any roster of 3-6 members and both ratios.

**The example product** is Grok Bot, as an **unofficial spec film**: not made, endorsed or sponsored by its makers, and
labelled so on the end card. Every line comes from the product: the hook and end line from its launch post, the promise from
its product page, each member's line from the status text in its screenshots. The screenshots and logo are not in this repo
(`project/assets/THIRD_PARTY.md`).

## What the reference does (and this entry keeps)

- A one-line problem in the product's own words.
- The team introduced together, then the portraits fly up into a tab bar that stays on screen; the active one grows.
- One beat per member: name, what it does, the real product screen proving it.
- The team gathers again on the end card with the call to action.

## What this entry changes

| Reference | This entry | Why |
|---|---|---|
| Paper ground, serif headlines | Dark ground, sans headlines | the example brand is dark and sans; ground and type are `palette` and `fonts` slots |
| 3-4 different images per member, swapped on beats | One screenshot per member with a push and a ring | one real screenshot is all most products have for each feature |
| Fixed four members, 16:9 only | 3-6 members, 16:9 and 9:16 from one project | social needs vertical; rosters vary |
| Hand-written scenes | `film.json` + `tools/build.py` | swap without touching the generator |

## Measured

| | Reference | This entry (result.mp4) |
|---|---|---|
| Duration | 20.5 s | 26.7 s (incl. 1.2 s credit card) |
| Events per 10 s | 7.8 | 3.0 |
| Still share | 0.60 | 0.83 |
| Loudness | -13.4 LUFS | -14.1 LUFS |
| True peak | -1.4 dBTP | -2.5 dBTP |

The reference is denser because each member swaps two or three images on the beat; this entry holds one screenshot and
pushes into it. It reads calmer and more premium, but it is less punchy. To raise the energy for a feed, shorten `MEM_DUR` in
`tools/build.py` to 2.0 s, or (not built yet) give each member a second focus box and cut to it on the beat at 1.5 s.
