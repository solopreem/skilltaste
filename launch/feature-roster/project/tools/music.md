# Music

`assets/music_raw.mp3` was generated with ElevenLabs Music (through fal, `fal-ai/elevenlabs/music`, 26 000 ms) from this prompt:

```
Instrumental only. Bright, confident, modern minimal electronic product music, 120 BPM, continuous groove from the first second to the end with no silent gaps. Clean plucked synth, warm sub bass, crisp tight drums with a soft four-on-the-floor kick, light claps, airy pads. Starts tight and clean, gets fuller after 4 seconds, ends on one clean final hit at the very end. No vocals, no bells, no chimes, no long risers, no glitch effects.
```

Then it is cut to the film length and faded out:

```bash
ffmpeg -i assets/music_raw.mp3 -t 25.5 -af "afade=t=out:st=24.4:d=1.1" assets/music_mix.mp3
```

What matters, if you swap the track: 120 BPM with the first downbeat near the start (scenes cut on 0.06 + 0.5k s of film
time), no silent gaps, length = the film without the credit card (25.5 s for five members; each extra member adds 3 s).
