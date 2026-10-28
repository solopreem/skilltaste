# Reference

**What it reproduces:** the structure of a 94 s keynote-style launch film for a consumer AI assistant (user-supplied file,
not redistributed here), rebuilt with our own footage, type, timing and sound and the user's art direction.

**The example product** is Muse, Meta's personal AI agent, as an **unofficial spec film**: not made, endorsed or sponsored by
Meta, and labelled so on the end card. Every claim and screen comes from Muse's public page (ai.meta.com/muse). Meta's
assets are not in this repo (`project/assets/THIRD_PARTY.md`).

## What the reference does (and this entry keeps)

- Opens on the product name, then kinetic type that blurs in word by word.
- A dark "Your [ ]" wheel between chapters, rolling one word per chapter.
- Real product UI pushed into and scrolled; a glass card listing safety points over landscape footage.
- B-roll of people living their day with a line of type over it.
- "One More Thing", a pill that morphs, a hand-drawn circle around a word, a dot that becomes the logo.

## What this entry changes

| Reference | This entry | Why |
|---|---|---|
| Opens on the name over an empty light frame | Opens on footage of a person at work, type over it | frame 0 is the poster; hook within 3 s |
| Wheels on a flat dark ground | Wheels over graded b-roll | no flat colour holds; the ground keeps moving |
| No burst; one cut every 4-5 s | An eight-shot montage at 32-35 s, beat then half-beat, caption locked | an energy peak near 35 % |
| 3D toy props | The brand's own illustration and mascot | real brand assets only |
| Footage only in a few scenes | Footage under 11 of 23 scenes, product cards floating over it | the reference's best-looking frames are the footage ones |

## Measured

| | Reference | This entry (result.mp4) |
|---|---|---|
| Length | 94 s | 90 s |
| Shots (cuts + 1) | 20 | 25 |
| Visual events per 10 s | 6.1 | 6.2 |
| Still share | 0.71 | 0.68 |
| Loudness | -15.4 LUFS | -14.4 LUFS |
| True peak | | -1.9 dBTP |
| Tempo | | 120 BPM grid (the detector reads 80.7 on this mix) |

Measured with `tools/analyze.py` and `tools/events.py` at the repo root.

## Lineage

The film was first built for thot market (thot.market). Its v1 used only paper and moss grounds and the brand's illustrations (3.2 events per 10 s, still share 0.86).
The note that produced v2: the reference's backgrounds look better. v2 added the b-roll and the burst. v2 was cut from
generated clips (9.0 events per 10 s, still share 0.55); this entry swaps them for locked-off Pexels stock, so the grounds
behind the two cards stay calm and the measured motion drops while every scene, cue and cut time stays the same. Rhythm rules
(poster frame, hook, burst position, locked anchor over a changing world) follow huashu-motion's director notes.
