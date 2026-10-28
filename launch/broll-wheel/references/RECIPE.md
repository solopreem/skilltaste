# Recipe: broll-wheel

90 s · 1920×1080 · 30 fps · 120 BPM (beats at 0.056 + 0.5k s) · every scene starts on 0.06 + 2k s · 23 scenes. With `copy.credit` set, a 1.2 s credit card plays first and the whole film (scenes, music, SFX) starts 1.2 s later: 91.2 s total.
Source of truth: `project/tools/build.py`. This file is its readable form. Times are film seconds.

## Energy

```
0      6     12    18    24    30  32-35  38    46    54    62  64-66   72    80   84    90
open   wheel problem sell  app  tools BURST vault terms proof wheel ONE  refer keep  end
 6      4     5     6     5     6     9     5     6     5     4    2→8   6     6    3
```

Hook in the first second (a person already at the desk), climb through three product chapters, the densest five seconds at
32-35 s (36 %), a near-stop for One More Thing (music ducked), the brightest stretch after it, then down to the mark.

## Shots

| # | Start | Len | Scene | Ground | What happens | Moves |
|---|---|---|---|---|---|---|
| 1 | 0.00 | 6.06 | open | b-roll `open` | Footage already moving at frame 0, slow 1.12→1 push. Logo tile pops (0.06). `✳ open_a` blurs in word by word (0.3), out at 2.82; `open_b` in at 3.06, accent marker at 3.6 | word-blur-in, marker block |
| 2 | 6.06 | 2.04 | wheel1 | b-roll `wheel1` | `Your` accent block + six-word column; the column rolls one word on the next beat (0.32, 0.7 s expo.inOut) | wheel-divider |
| 3 | 8.06 | 4.04 | feast | paper | The wide illustration fades up and creeps 1→1.14; `problem` line under it, marker sweep at 1.4 | word-blur-in, marker-sweep |
| 4 | 12.06 | 3.04 | sell | b-roll cuts | `sell_head` over `sell0`; the three chips pop in one per beat (0.94, 1.44, 1.94) and each lights accent in turn; the footage hard-cuts to `sell1`, `sell2` on those beats while the chips stay put | anchor-chips-over-cuts |
| 5 | 15.06 | 3.04 | same | paper | Two lines, second one marked | word-blur-in, marker-sweep |
| 6 | 18.06 | 6.04 | app | paper | The real app card grows 0.38→1 (0.3-1.4), a cursor walks the four tabs one per beat (1.3-2.94), then the camera pushes 1.75× into one panel and a focus ring lands (4.5) | card-push-in, cursor-tab-walk |
| 7 | 24.06 | 2.04 | wheel2 | b-roll `wheel2` | wheel rolls to word 2 | wheel-divider |
| 8 | 26.06 | 6.04 | tools | b-roll `tools` (slowed 0.8×) | Headline left, real card floats in right (0.2), rings land on its key rows at 1.94 / 3.06 / 4.06; footage drifts 1→1.1 | floating-card-over-footage, focus-rings-in-order |
| 9 | 32.06 | 4.04 | brain | 8 b-roll shots → paper | THE BURST. Cuts at 0, .5, 1, 1.5, 2, 2.25, 2.5, 2.75 (beat, then half-beat), every shot enters at 1.14 scale. One cream caption bar locked low: `montage_a`, then `montage_b` at 1.5. At 3.0 hard cut to paper, the mascot slams in, the caption rides up beside it, marker at 3.3 | anchor-montage |
| 10 | 36.06 | 2.04 | wheel3 | b-roll `wheel3` | wheel → 3 | wheel-divider |
| 11 | 38.06 | 6.04 | vault | paper | Illustrative session card; at 1.94 a dark vault slides up behind, the lock drops (2.44), each line blurs into its hash (2.94+), `vault_private`, `vault_sub` | hash-reveal |
| 12 | 44.06 | 2.04 | wheel4 | b-roll `wheel4` | wheel → 4 | wheel-divider |
| 13 | 46.06 | 6.04 | terms | b-roll `terms` (slowed) | Like tools: real worked-example card, rings on the price and on the result, card breathes to 1.06 | floating-card-over-footage |
| 14 | 52.06 | 2.04 | wheel5 | b-roll `wheel5` | wheel → 5 | wheel-divider |
| 15 | 54.06 | 4.04 | proof | paper | Flow diagram rises; a ring walks its five stages one per beat (0.94+) | stage-walk-ring |
| 16 | 58.06 | 4.04 | steps | paper | Three numbered steps, one per beat; the last number turns accent | word-blur-in |
| 17 | 62.06 | 2.04 | wheel6 | b-roll `wheel6` | wheel → 6 | wheel-divider |
| 18 | 64.06 | 2.04 | one | paper | Giant "One" whips in blurred, collapses; "One More Thing" word by word. Music ducked to 0.22 | one-more-thing |
| 19 | 66.06 | 6.04 | refer | paper | Pill with the brand name, a dot; at 1.9 the pill floods the accent and becomes `refer_to`, the number counts up 0→N (or a word lands), mascots and logo tiles float in around it | pill-morph-counter, floating-mascots |
| 20 | 72.06 | 4.04 | invite | illustration | The illustration enlarged and panned, a paper panel with two lines and a sub | marker-sweep |
| 21 | 76.06 | 4.04 | trust | paper | Two-line headline left, three FAQ rows slide in right one per beat, mascot pops | word-blur-in |
| 22 | 80.06 | 4.04 | keep | b-roll `keep` | Two lines over footage; an accent circle draws around the last words (1.44) | circle-draw |
| 23 | 84.06 | 5.94 | end | ground colour | Accent dot pops and bursts, logo tile spins in, name, tagline, URL pill | dot-to-logo |

## Sound

Music `music_mix.mp3` at 0.8. SFX (file, time, volume): key-press on every wheel roll (scene start + 0.36, 0.45) ·
whoosh-short on the app push (18.3) · key-press on the two sell cuts (13.5, 14.0) and on each montage cut (32.56-34.81, 0.35) ·
click-soft on the montage slam (35.06) and the vault lock (40.55) · printer under the vault (38.8) · whoosh-short into One
More Thing (64.02) · whoosh on the pill morph (67.95) · impact-bass-1 on the end (84.06). Master: -14 LUFS, limiter at -1 dBTP.

## Holds and eases (keep them)

- Word reveals: 0.6 s expo.out, 0.08 s stagger, from x 26 and blur 10 px. Exits: 0.24 s power2.in with blur 8 px.
- Marker sweep: 0.5 s power2.inOut. Wheel roll: 0.7 s expo.inOut on the beat after the cut.
- Cards: 0.9 s expo.out from 0.7 scale. Rings: 0.4 s expo.out from 1.25, each on a beat, the previous one fades 0.1 s before.
- Every scene fades its content out 0.24-0.26 s before its end so the next scene's cut is clean.
