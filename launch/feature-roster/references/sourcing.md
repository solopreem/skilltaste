# Collect the real material

Do this yourself, before you build. A film about a real subject (a product, a place, a dish, a person, an event) made from
invented pictures or invented words cannot ship, however good it looks. Ask the user only for what this page cannot get you.
The entry's own `SKILL.md` says which pieces this film needs; this page says how to get them for any subject.

## What must be real, and what may be borrowed

| Must be real (from the subject itself) | May be borrowed (stock, licensed or generated) |
|---|---|
| the subject: its product, screens, packaging, dishes, venue, people, work | atmosphere: b-roll of a generic world, textures, skies, backgrounds |
| its name, logo, colours and the names of its parts (features, menu items, plans, tracks) | music and sound effects |
| every claim, number, quote and line of its own copy | fonts (open ones, close to the brand's) |

If a borrowed shot could be mistaken for the subject (a stock dish standing in for the restaurant's dish), it is not
atmosphere: get the real one or cut the shot. Anything invented for the story (a sample task, demo numbers) is labelled on screen.

## Where to look, in this order

1. **The subject's own site and pages**: capture with `npx hyperframes capture <url>` or read with a fetch tool.
2. **Its press kit, brand page, docs, menus, changelog or launch post**: often on another host, with full-size logos and
   the exact wording.
3. **Its official channels**: posts on X, Instagram, TikTok, YouTube, LinkedIn, Xiaohongshu; launch posts carry hero images and video.
4. **Press and blog coverage**: articles embed official images and logos, often full size. Search the name with
   "launch", "press", "logo", "screenshot", "photos"; read the image URLs in each article and take the largest.
5. **Store and listing pages it controls**: App Store, Google Play, Steam, Product Hunt, Amazon or Shopify listings, its own
   Google Maps or Dianping business photos (only the owner's uploads, not customers').
6. **The user**: only now, and for something specific (the logo file, a signed-in screenshot, photos of the dish, consent
   to show a person).

If a site blocks automated access (Cloudflare, 403, a bot check), do not get around it: move to the next source.
Write down where every file came from and who owns it; it goes into `project/assets/THIRD_PARTY.md`.

## Prepare it

- Use the material itself: crop, cut out, grade, push in. Do not redraw or regenerate the subject.
- Measure on the image (a pixel grid) and put boxes in `film.json` in the image's own pixels.
- Small elements (icons, avatars, product cut-outs): transparent background, upscale at most 2x.
- A dark-on-light logo for a dark ground: turn it white rather than drawing a new one.
- Never enlarge an image past about 1.7 screen pixels per source pixel; find a larger source instead.

## Check before you build

- Every picture of the subject exists; every name, number and line can be pointed to on a page you found.
- People shown are the subject's own, from its own channels, or the user confirms consent.
- For a brand that is not the user's own: the film says it is unofficial, and the brand's material stays out of any public repo.
