# Music and sound effects

All generated with ElevenLabs through fal (needs FAL_KEY). The shipped files render without any key.

## Music (`assets/audio/music.mp3`)

Generated 43 s, then cut to `audio.length` with a 2.2 s fade out:

```bash
python3 tools/fal.py fal-ai/elevenlabs/music '{"prompt":"Tense modern documentary underscore for a true-crime finance story. Ticking muted pulse, low synth drone, sparse felt piano motif, subtle risers, a hit at 11 seconds when the empire collapses, darker from 17 seconds, builds slightly at 27 seconds, resolves to a single sustained low note at 37 seconds and ends cleanly at 43 seconds. No vocals. Leaves space for a narrator.","music_length_ms":43000}' assets/audio/music-raw
ffmpeg -i assets/audio/music-raw.mp3 -t 42.6 -af "afade=t=in:d=0.3,afade=t=out:st=40.4:d=2.2" assets/audio/music.mp3
```

Write the prompt's hit times from your own narration (the turn of the story, the reveal, the last line). It sits at
`audio.music_volume` 0.32 under the voice.

## Sound effects (`assets/audio/sfx/`)

`fal-ai/elevenlabs/sound-effects/v2`, `duration_seconds` 1.2. `build.py` places them: every item type has its own sound.

| File | Prompt | Used by |
|---|---|---|
| stamp.mp3 | A heavy rubber stamp hitting paper on a desk, one thud, dry | stamp, strip, logo, counter landing |
| paper.mp3 | A single sheet of thick paper slapped down onto a wooden desk, short, close, dry | sticker, card, news, rip |
| tape.mp3 | A strip of masking tape quickly torn off a roll and pressed down, short | clipping, print |
| rip.mp3 | A sheet of paper torn in half quickly, short, dry | rip (on `tear`) |
| whoosh.mp3 | A quick soft paper whoosh swipe, short | every cut to b-roll, ticker |
| tick.mp3 | Fast mechanical counter digits ticking up, like an old flip counter, short | counter |

## Voice

`python3 tools/voice.py script.txt` (ElevenLabs multilingual v2, voice "Brian"). See `references/SWAP.md`.
