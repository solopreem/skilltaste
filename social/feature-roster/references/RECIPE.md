# Recipe: feature-roster

25.5 s for five members · 1920×1080 or 1080×1920 · 30 fps · 120 BPM · scenes cut on 0.06 + 0.5k s of film time. With
`copy.credit` set, a 1.2 s credit card plays first and the whole film (scenes, music, SFX) starts 1.2 s later: 26.7 s total.
Source of truth: `project/tools/build.py`. This file is its readable form. Times are film seconds (after the credit card).

## Energy

```
0        4.06     7.06    10.06   13.06   16.06   19.06   22.06    25.5
hook     meet     m1      m2      m3      m4      m5      end
4        3        3       3       3       3       3       3.44
```

A question in the product's own words, the product's name and promise, then the same beat once per member, then the team
again. Each member beat is identical on purpose: the viewer learns the pattern on the first one and reads the rest faster.

## Beats

| # | Start | Len | Scene | What happens | Moves |
|---|---|---|---|---|---|
| 0 | -1.2 | 1.2 | credit | `copy.credit` fades in centred at 2.2× (1.6× vertical), holds, flies to the top right at 1.1 s (0.7 s expo.inOut), fades at 3.62 | credit-card |
| 1 | 0.06 | 4.0 | hook | `hook_a` in muted ink, word by word (0.06 stagger); `hook_b` in white at 1.0; the `*starred*` words get an underline sweep at 1.7; out at 3.72 | word-blur-in, underline-sweep |
| 2 | 4.06 | 3.0 | meet | Logo mark pops (back.out), `meet` word by word at 0.2, `meet_sub` at 0.6; the member avatars pop one per eighth note from 1.06; text clears at 2.4; at 2.5 the row flies up into the tab bar (0.5 s expo.inOut), member 1 already large | roster-pop, roster-to-tabbar |
| 3 | 7.06 + 3k | 3.0 | member k | Panel rises (0.55 s expo.out) with the screenshot already pushing from 1.36× the focus box to the focus box (2.9 s power2.inOut); `0k / 0N` label with the member's colour dot, name word by word at 0.1, the member line at 0.42; the colour ring lands on the proof at 1.3 with a soft click; all out at 2.74 | panel-rise, push-and-ring |
| — | 7.06 → 22.06 | 15 | nav (overlay) | The tab bar stays on top; on each member's cut the active tab grows to 1.44× and goes full opacity, the others drop to 0.4 | roster-to-tabbar |
| 4 | 22.06 | 3.44 | end | The avatars gather in a row (0.06 stagger), logo lockup blurs in at 0.2, `end` at 0.6 with its underline at 1.2, URL pill at 1.1, disclaimer at 1.4 | roster-gather, lockup |

## Sound

| Film time | Cue |
|---|---|
| 1.0, 1.16, 1.32 | key-press, light, as `hook_b` lands |
| 4.0 | whoosh-short into meet |
| 5.12 + 0.125k | key-press per avatar pop, alternating tracks |
| 6.51 | whoosh as the row flies to the tab bar |
| 8.34 + 3k | click-soft as each ring lands |
| 22.06 | impact-bass on the end |

Music: one 120 BPM track, the film length without the credit card, faded over the last 1.1 s (`tools/music.md`).

## Layout

| | 16:9 | 9:16 |
|---|---|---|
| tab bar | centre x, y 96, 104 px apart, 64 px (active 92) | y 150 |
| member text | left 120: label 392, name 432 (72 px), line 524 (≤ 640 wide) | left 80: label 300, name 340 (76 px), line 436 |
| screenshot panel | 940×760 at (860, 190), 28 px radius | 960×1140 at (60, 620) |
| roster row (meet) | y 790, 200 px apart, 130 px | y 1240, 180 px apart |
