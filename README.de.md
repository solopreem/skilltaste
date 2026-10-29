<div align="center">

# video-skills

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | **Deutsch** | [Français](README.fr.md) | [Português](README.pt.md)

Bau ein Video mit gutem Geschmack in Minuten nach.

</div>

```bash
npx skills add sonnyproto/video-skills                       # die ganze Bibliothek (der Agent wählt einen Eintrag)
npx skills add sonnyproto/video-skills/launch/broll-wheel   # nur dieser Film
```

Dann in Claude Code oder Codex:

```text
Mach mit broll-wheel einen Launch-Film für https://your-product.com.
```

Sonst ist nichts von Hand zu installieren: Der Agent führt das `scripts/setup.sh` des Eintrags aus, das Node 20+, ffmpeg und Python 3 prüft
und die HyperFrames-Skills installiert, falls sie fehlen. Den Renderer holt `npx` in einer festen Version.

## Warum es das gibt

Video-Skills gibt es heute in zwei Formen. Die einen sind geschlossene Pakete: ein Stil pro Kauf, schnell, aber man kann weder
hineinsehen noch sie kombinieren. Die anderen sind tiefe offene Toolkits, jedes mit eigenem Format, sodass nichts zueinander passt.

video-skills ist die flache Version der ersten Form, offen gemacht:

- **Ein Eintrag = ein Film.** Jeder bringt das `result.mp4` mit, das er erzeugt hat, also wählst du mit den Augen.
- **Reproduzierbar.** Jeder Eintrag enthält ein vollständiges Projekt, das seinen Film unverändert rendert, dazu die Quell-IDs des Stock-Materials und die Prompts aller generierten Medien. Keine API-Keys nötig.
- **Überall dasselbe Format.** Alle Einträge haben dieselben Dateien und dieselbe `taste.json`-Karte, sodass du sie vergleichen
  und Agents sie kombinieren können ([spec/ENTRY.md](spec/ENTRY.md)).
- **Das Produkt in einer Datei.** Für dein Produkt änderst du `film.json` und die Assets, nie den Generator.

## Bibliothek

<!-- CATALOG -->
| Preview | Entry | Category · method | Length | Events / 10 s |
|---|---|---|---|---|
| <img src="launch/broll-wheel/result/preview.gif" width="240"> | [**broll-wheel**](launch/broll-wheel/) B-roll wheel launch | launch · broll-under-type | 90 s 16:9 | 8.7 |
| <img src="launch/feature-roster/result/preview.gif" width="240"> | [**feature-roster**](launch/feature-roster/) Feature roster | launch · rebuilt-ui-roster | 26.7 s 16:9 + 9:16 | 3.0 |
<!-- /CATALOG -->

## Aufbau eines Eintrags

```
<category>/<id>/
├── SKILL.md       laden und den Film machen
├── taste.json     die Karte: Voraussetzungen, sieben Ebenen, Spezifikation, Messwerte, was er braucht, wofür er passt
├── references/    floor.md (gemeinsame Regeln), sourcing.md (launch: echtes Material), RECIPE.md (Shot für Shot), SWAP.md (dein Produkt rein), REFERENCE.md
├── scripts/       setup.sh (installiert, was fehlt) und die Mess-Skripte
├── result/        result.mp4, Poster, Kontaktbogen, Vorschau, metrics.json
└── project/       ein renderbares Projekt: film.json, tools/, assets/
```

Jeder Eintrag wird auf denselben sieben Ebenen eingeordnet:

| Ebene | Frage |
|---|---|
| floor | Was ist nie verhandelbar? (nur das echte Produkt, Beispiele gekennzeichnet, die Marke) |
| category | Welche Art Film? (Launch, Erklärfilm, Tutorial, Datengeschichte, Social-Cut, Sting) |
| method | Wie entsteht das Bild, und wie läuft das Rückgrat? (B-Roll unter Typo, eine nie geschnittene Form, Beat-Montage, 3D-UI ...) |
| moves | Welche konkreten Moves füllen ihn? (Rad als Kapiteltrenner, Textmarker-Strich, Anker-Montage, Pill-Morph ...) |
| craft | Was lässt ihn teuer aussehen? (Hook in 3 s, Höhepunkt bei etwa 35 %, Akzente auf den Landungen, -14 LUFS) |
| style | Wie sieht er aus? (Grading, Schrift, Farbrollen) |
| tool | Womit wird gerendert? (HyperFrames, Remotion ...) |

Verschiedene Ebenen kollidieren nie. Auf derselben Ebene gilt: floor > category > method > moves > craft > style.

Jeder Eintrag ist in sich geschlossen: Unsere gemeinsamen Dateien (die floor-Regeln, die Mess-Skripte) werden hineinkopiert, externe Tools
(HyperFrames, ffmpeg) werden in `requires` von `taste.json` deklariert, und Geschmack wird nie geteilt. Siehe [spec/ENTRY.md](spec/ENTRY.md).

## Werkzeuge

| | |
|---|---|
| `tools/floor.md` | die gemeinsamen floor-Regeln (in `references/` jedes Eintrags kopiert) |
| `launch/sourcing.md` | wie Launch-Filme echte Screens, Logo und Texte des Produkts sammeln (in `references/` jedes Launch-Eintrags kopiert) |
| `tools/validate.py` | prüft jeden Eintrag gegen das Format und ob seine Kopien der gemeinsamen Dateien mit `tools/` übereinstimmen |
| `tools/catalog.py` | baut `catalog.json` und die Tabelle oben neu |
| `tools/analyze.py <video> <out>` | Schnitte, Shots, Kontaktbogen, LUFS, True Peak, BPM, Schnitte auf dem Beat |
| `tools/events.py <video> <out>` | visuelle Änderungen pro 10 s und Anteil stehender Bilder |

## Voraussetzungen

Node 20+, ffmpeg, Python 3. Einträge sagen, was sie sonst noch brauchen (eine Renderer-Version, ein Videomodell für B-Roll, ein Musikmodell).

## Mitmachen

Neue Einträge sind willkommen; siehe [CONTRIBUTING.md](CONTRIBUTING.md). Die Messlatte: Das Projekt rendert sein Ergebnis unverändert,
das Produkt steht in `film.json`, das Ergebnis ist gemessen, und nichts aus der Referenz wird weiterverbreitet.

## Dank

Ideen und Regeln, dankbar übernommen von [HyperFrames](https://hyperframes.heygen.com),
[huashu-motion](https://github.com/alchaincyf/huashu-motion) (Rhythmus und Regienotizen),
[video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) (Rezeptkarten und Austauschanleitung) und
[product-launch-motion](https://github.com/AbubakrChan/product-launch-motion) (handwerkliche Details).

## Lizenz

Das broll-wheel-Beispiel ist ein inoffizieller Spec-Film für Muse, den persönlichen KI-Agenten von Meta. Er steht in keiner Verbindung
zu Meta und wird von Meta weder unterstützt noch gesponsert; Muse und seine Assets gehören Meta und sind nicht in diesem Repo.

Code: MIT. Ergebnisfilme und generierte Medien: CC BY 4.0. Assets der Beispielprodukte gehören ihren Eigentümern; die
`taste.json` jedes Eintrags sagt, was wiederverwendet werden darf.
