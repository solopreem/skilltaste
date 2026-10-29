# Recipe: paper-collage

42.6 s of narration + 1.2 s credit card = 43.8 s · 1920×1080 or 1080×1920 · 30 fps · cuts on the narration, not a beat grid.
Source of truth: `project/tools/build.py` (the look and the moves) and `project/film.json` (this story). Times below are
narration seconds (`assets/audio/words.json`); the credit card plays before them.

## Shape

```
0        6.7     11.3      17.4    21.4      26.7     31.7  34.1   37.1        42.6
open     lab     collapse  sentence sold     ipo      worth prison end
paper    b-roll  b-roll    b-roll  paper     b-roll   paper b-roll paper
```

A true story in seven to nine scenes, about one sentence of narration each. Paper scenes and b-roll scenes alternate, so
the eye gets a rest between dense collages. The hook is the first sentence (a year, a person, a number); the turn comes
at about a quarter (the collapse); the reveal at about three quarters (the number nobody expected); the last line is a
headline the narration says word for word.

## Beats

| # | Start | Len | Scene | What lands, on which word | Moves |
|---|---|---|---|---|---|
| 0 | -1.2 | 1.2 | credit | `copy.credit` on a paper strip, centred at 2.2× (1.6× vertical), flies to the top right, fades at 3.62 | credit-card |
| 1 | 0 | 6.7 | open | "2022" stamped on (0.15); his photo-sticker rises from below (0.9); typewriter label types itself (1.3); a torn-paper cheque slaps on (3.0) and its payee line gets a highlighter sweep (5.1) | stamp, sticker-rise, typewriter-label, card-slap, highlighter |
| 2 | 6.7 | 4.6 | lab | b-roll; the Anthropic logo on torn paper slaps on with the word "Anthropic" (7.4), shrinks up (8.55) to make room for a second sticker (8.7) and his name on a red strip (9.8) | logo-slap, make-room, name-strip |
| 3 | 11.3 | 6.1 | collapse | b-roll of a chart turning red; FTX logo card slaps on (11.55) and tears in half on "collapsed" (12.55); the real price chart is taped on (13.5) and a red marker circles the crash (14.0); "Customers' money" on yellow (14.6) | rip, clipping-tape, marker-ring, key-strip |
| 4 | 17.4 | 4.0 | sentence | b-roll; dateline typed (17.55); "25 YEARS" slams on in black (19.4) | typewriter-label, slam |
| 5 | 21.4 | 5.3 | sold | paper; a newspaper clipping rises (21.7); a red box stamp "$1.3 BILLION" hits on "1.3" (23.3); "to repay creditors" typed (25.15) | news-rise, box-stamp |
| 6 | 26.7 | 5.0 | ipo | b-roll; "This week" (26.82); a black ticker tape slides across and scrolls (27.5); the logo again (28.6) | key-strip, ticker-tape, logo-slap |
| 7 | 31.7 | 2.4 | worth | paper; label (31.7); the number ticks from 1.3 to 47 in 13 steps of 0.075 s from "47" (32.15) and lands with a stamp; highlighter bar under it (33.25); the sum typed under it (33.4) | counter, highlighter |
| 8 | 34.1 | 3.0 | prison | b-roll; a taped photo print drops in (34.25); the place on a black strip (35.45) | print-drop, key-strip |
| 9 | 37.1 | 5.5 | end | paper; the last line appears word by word as it is spoken (37.1-38.4); the sting on a red strip (38.9); sources and photo credits fade in (40.3) | spoken-headline, sting-strip, sources-note |
| — | 0 | 42.6 | captions (overlay) | the narration a phrase at a time, white on a dark box at the bottom (most feeds play muted) | captions |

Every scene also has a slow push on its paper layer (1.03-1.05× over the scene), and every b-roll scene gets the same
treatment: desaturated to 35 %, contrast 1.18, brightness 0.7, an 8 px halftone dot screen and paper grain multiplied
over it, and a soft vignette.

## Motion vocabulary (build.py)

| Move | How |
|---|---|
| slap | from 1.3-1.7× and +7° to 1× in 0.32 s, back.out(2.2) |
| rise | from below (the frame height) and -6° in 0.5 s, expo.out |
| drop (print, clipping) | from 120-180 px above and tilted, 0.5 s back.out(1.5) |
| box stamp | from 1.8× to 1× in 0.18 s, power4.in, multiplied at 0.92 opacity |
| typewriter | letters appear one by one, 0.025-0.04 s each |
| rip | two torn halves part: -90/+90 px, -9°/+11°, 0.45 s |
| counter | discrete values, one per 0.075 s, the last one lands with back.out |

Every piece sits at a small tilt (-4° to +3°). Nothing glides; things land.

## Sound

| On | Cue |
|---|---|
| stamp, strip, logo, counter landing | stamp |
| sticker, card, clipping-free paper (news, rip) | paper |
| clipping, print | tape |
| rip `tear` | rip |
| every cut to b-roll, ticker | whoosh (0.3) |
| counter start | tick |

Narration at 1.0, music at 0.32, SFX 0.3-0.8. Master: -14 LUFS, true peak under -1 dBTP (`tools/master.sh`).
