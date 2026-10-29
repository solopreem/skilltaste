# Reference

**What it reproduces:** the Vox-style paper-collage explainer: a narrated true story told with real photos cut out as
white-border stickers, torn paper, newspaper clippings, rubber stamps and typed labels over b-roll under a halftone
screen. The direct prompt was a frame from a short narrated biography made by an AI video agent and shared on LinkedIn
(a cut-out portrait with a white border over a halftone city skyline, one big keyword across it). We worked from that
frame and the post's description; the video itself was not available to us, so it is neither measured nor redistributed.

Related open work we looked at, not copied: `Alisa0808/vox-director` (MIT; generates whole collage posters with image
models, then animates them) and the `vox-collage` template in `alchaincyf/huashu-motion` (MIT). This entry takes the
opposite route to vox-director: every real thing on screen is a real photo or document, cut and placed in code, and only
atmosphere is generated.

**The example story** is an unofficial explainer about Sam Bankman-Fried's 2022 investment in Anthropic, told the week
Anthropic filed to go public. Every fact comes from reporting or the S-1 (`project/assets/THIRD_PARTY.md`); every photo is
from Wikimedia Commons under CC BY 3.0 or in the public domain, credited on the end card.

## What the style does (and this entry keeps)

- One narrator, one sentence per scene, and something lands on the word it belongs to.
- Real people as cut-out photo stickers with a white die-cut border; never drawn.
- Paper everywhere: torn edges, a cheque, a clipping, tape, a highlighter, a red marker ring.
- Big condensed sans for names and numbers, a typewriter for labels.
- B-roll as texture, not as the subject: desaturated, halftone, grain.

## What this entry decides

| Choice | Why |
|---|---|
| Paper scenes alternate with b-roll scenes | dense collages need a rest; b-roll carries the mood between them |
| Generated b-roll with no people | atmosphere is free to generate; real people and events are not (`references/sourcing.md`) |
| Captions always on | feeds play muted; the narration is the spine |
| End card names the sources and photo credits | a true story has to show where it comes from; CC BY requires the credit |
| Everything placed in code from `film.json` | swap the story without touching the generator; pixel-exact, so real faces are never altered |

## Measured (result.mp4)

| | This entry |
|---|---|
| Duration | 43.8 s (incl. 1.2 s credit card) |
| Scenes | 9 |
| Events per 10 s | 9.8 |
| Still share | 0.52 |
| Loudness | -14.3 LUFS |
| True peak | -2.1 dBTP |
