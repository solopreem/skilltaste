# Music

The shipped `assets/music_mix.mp3` was generated with ElevenLabs Music (through fal, `fal-ai/elevenlabs/music`, 90 000 ms) from this prompt:

```
Instrumental only. Warm, witty, premium product launch music, 120 BPM, continuous groove from the first second to the end with no silent gaps. Marimba and pizzicato strings, upright bass, soft wooden percussion, hand claps, light felt piano. Starts gentle and gradually gets fuller, ends on a warm final chord at the very end. No vocals, no bells, no chimes, no long risers, no glitch effects.
```

Then `tools/mix_music.sh raw.mp3` ducks it for One More Thing and fades the end.

What matters, if you swap the track: 120 BPM with the first downbeat at about 0.056 s (every scene starts on 0.06 + 2k s),
no silent gaps (section-by-section prompts produced gaps and the wrong tempo; the simple prompt above did not),
and a duck at 63.7-66.2 s. Change the instruments to fit the brand; keep the tempo and the grid.
