# Collect the real material (explainers)

An explainer tells a true story: a company, a person, an event, an idea with a history. Do this yourself, before you
write the film. A film about something real made from invented facts or invented pictures cannot ship, however good it
looks. Ask the user only for what this page cannot get you. The entry's own `SKILL.md` says which pieces this film needs.

## Facts first

- Write the script from sources, not memory. Every name, date, number and quote must be found on a page you can point to.
- Prefer the primary source: the filing, the court record, the company's own post, the official statistics. Use press
  coverage to find it and to check it; when outlets disagree, use the primary source or say "about".
- Mark what is estimated (a paper value, a projection) as estimated, in the narration or on screen, and show the sum.
- Check the date of everything. "This week", "now" and "latest" need a source from this week.
- Keep a list: claim → source URL. It goes into the end card's sources line and `project/assets/THIRD_PARTY.md`.

## What must be real, and what may be borrowed

| Must be real | May be borrowed (stock, licensed or generated) |
|---|---|
| the people: their photos, their names, their words | atmosphere: places, objects, screens, skies, textures |
| documents and data: charts, filings, headlines, logos | music and sound effects |
| every claim, number, date and quote | fonts (open ones) |

- Never generate a real person's face or body, and never generate a real event (an arrest, a trial, a deal) as if it
  were footage of it. Generated b-roll shows atmosphere with no people in it.
- If a borrowed shot could be mistaken for the real thing (a generated courtroom read as the actual trial), make it
  plainly generic or cut it.

## Where to look for pictures, in this order

1. **Wikimedia Commons** (`commons.wikimedia.org`): search the name; the API returns each file's licence and author
   (`action=query&generator=search&gsrnamespace=6&prop=imageinfo&iiprop=url|size|extmetadata`). Public domain, CC0,
   CC BY and CC BY-SA can be used with credit; note which.
2. **Official sources**: the person's or company's own press page, government and court releases (US federal works are
   public domain), official social accounts.
3. **Open data** for charts: draw them from the numbers, or use a chart already released under an open licence.
4. **The user**: only now, and for something specific (a photo they own, a licensed press image).

If a site blocks automated access (Cloudflare, 403, a bot check), do not get around it: move to the next source. Press
agency photos (Getty, AP, Reuters) are not free to use; do not take them from articles.

## Prepare it

- Cut people out of photos (`tools/cutout.py`); never redraw them. A photo too small or flat to cut cleanly goes in as a
  taped print instead. Keep other people out of the frame: crop them away.
- Logos and documents stay as they are; put them on paper, do not recolour or redraw them.
- Never enlarge an image past about 2 screen pixels per source pixel unless it is a deliberately small print.

## Check before you build

- Every fact on screen and in the narration has a source on your list, and the end card names the main ones.
- Every image has a licence that allows the use, and the end card credits the ones that require it.
- The film says what it is: an unofficial explainer, not made or endorsed by the people or companies in it.
- A living person shown in a bad light gets only what the record says: charges, verdicts and sentences as reported,
  never guesses.
