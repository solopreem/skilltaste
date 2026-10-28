# B-roll slots

The nine footage slots this film cuts from, what each must show, and a prompt you can give any text-to-video model if you
would rather generate than use stock. The example film uses Pexels stock (`tools/stock.sh`, credits in
`assets/broll/CREDITS.md`). Either way: 16:9, at least 1080p, landscape, no text, no logos, no readable screens, and
the clip at least as long as the slot needs.

Shared look (append to every prompt): muted olive green and warm cream palette, soft natural light, shallow depth of
field, clean sharp image, no film grain, no text, no logos, no readable screens.

| Slot | Needs | Used as | Prompt |
|---|---|---|---|
| open | ≥ 10 s | open, sell 0, wheel 6 | Night. A person sits at a wooden desk deep in thought, warm desk lamp, laptop seen from behind so its screen is not visible, notebooks and plants. Slow steady dolly in. |
| research | ≥ 7 s | sell 1, montage 0 | Close-up of a hand sweeping a highlighter across a line of a printed page on a wooden table, morning light. Slow push in. |
| whiteboard | ≥ 5 s | sell 2, montage 1 | Close-up of a marker drawing boxes and arrows on a whiteboard. Gentle handheld drift. |
| notebook | ≥ 6 s | wheel 1, montage 2 | A person sketching a diagram, pen moving quickly, daylight. Slow lateral dolly. |
| window | ≥ 11 s | wheel 2, montage 4 | Dusk. A person reading beside a large window, warm lamp. Slow push in. |
| greenhouse | ≥ 21 s | tools (behind a card), montage 5 | A calm, dark natural texture with no people: ferns, moss, leaves. Very slow drift. Keep it quiet; a card sits on top. |
| moss | ≥ 19 s | wheel 3, terms (behind a card), montage 6 | Macro of moss on stone, very slow push in, no people. |
| receipt | ≥ 5 s | wheel 4, montage 7 | Close-up of a paper receipt or a payment moment, hands only. |
| walk | ≥ 3.2 s (5 s better) | wheel 5, keep, montage 3 | Golden hour. A person walks along a tree-lined path, tracking shot from the side. |

In-points and lengths are in `tools/cuts.py`. Change them there when a new clip's best moment is elsewhere.
