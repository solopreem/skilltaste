# Third-party assets

The example film is an unofficial spec film for Grok Bot. It is not affiliated with, endorsed or sponsored by the makers
of Grok Bot. Grok and Grok Bot and their screenshots and logo belong to their owner and are not in this repo.

To render the example as is, download these three images into `assets/src/` under these names, then run
`uv run --with pillow python tools/prep.py` (it cuts the avatars and the white logo out of them):

| File | What | Where it was found |
|---|---|---|
| `grokbot-app.jpg` (2048×1152) | desktop app and phone: the Bot list, a Chief of Staff chat, routines | "Grok Bot UI" in vellum.ai/blog/official-grok-bot-breakdown |
| `grokbot-home.png` (3786×2118) | x.ai/bot hero and the dark app: Sales Outbound asking you to sign in to Salesforce | "Grok Bot Homepage" in the same post |
| `grokbot-logo.png` (811×456) | the Grok Bot logo, black on white | the header image of gigazine.net/gsc_news/en/20260812-spacexai-grok-bot/ |

Every line of copy in `film.json` is taken from the product: the hook and the end line from the launch post
(x.ai/news/introducing-grok-bot), "AI teammates you can give real work to." from x.ai/bot, and each member's line is the
status text shown under that Bot in the screenshots.

Shipped and free to reuse: `fonts/` (Geist and Geist Mono, SIL OFL 1.1), `sfx/`, and `music_mix.mp3` (generated with
ElevenLabs Music through fal; prompt in `tools/music.md`).
