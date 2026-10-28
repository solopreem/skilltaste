# The example product's assets

The example film is an **unofficial spec film** for Muse, Meta's personal AI agent. It is not made, endorsed or
sponsored by Meta. Muse, its logo, screenshots and mascot belong to Meta and are **not included** in this repo; the
film shows them under that notice, and they are not covered by the repo's CC BY licence.

To re-render the example you need them locally. All six come from Muse's public page:

```bash
npx --yes hyperframes@0.8.191 capture https://ai.meta.com/muse/ --json -o /tmp/muse
```

| film.json path | Made from (in the capture) |
|---|---|
| `assets/muse-logo.png` | `assets/muse-nrp-blog-thumbnail.webp`, as PNG |
| `assets/img/muse-mac.png` | `assets/muse-desktop-mac-app.webp`, crop (110, 162, 1290, 826), resized to 1500×844 |
| `assets/img/muse-features.png` | `screenshots/scroll-010.png` crop (220, 586, 956, 1033) above `scroll-019.png` crop (220, 278, 956, 373) |
| `assets/img/muse-approve.png` | `screenshots/scroll-019.png` crop (976, 655, 1680, 945) |
| `assets/img/muse-props.jpg` | `assets/image-19.webp`, edge-extended to 3:1 (2904×968) |
| `assets/img/muse-mascot.png` | `assets/image-19.webp` crop (230, 330, 560, 660), background keyed out, 512×512 |

Page layouts change; check the crops against the screenshots. For your own film you replace all of these with your
product's assets anyway (`references/SWAP.md`). `assets/img/muse-flow.svg` is drawn for this film and does ship.

Fonts: DM Sans (SIL Open Font License 1.1).
