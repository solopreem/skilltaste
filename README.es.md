<div align="center">

# video-skills

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | **Español** | [Deutsch](README.de.md) | [Français](README.fr.md) | [Português](README.pt.md)

Rehaz un vídeo con buen gusto en minutos.

</div>

```bash
npx skills add sonnyproto/video-skills                       # toda la biblioteca (el agente elige la entrada)
npx skills add sonnyproto/video-skills/launch/broll-wheel   # solo este vídeo
```

Luego, en Claude Code o Codex:

```text
Haz un vídeo de lanzamiento para https://your-product.com con broll-wheel.
```

No hay que instalar nada a mano: el agente ejecuta el `scripts/setup.sh` de la entrada, que comprueba Node 20+, ffmpeg y Python 3
e instala las skills de HyperFrames si faltan. `npx` descarga el renderizador en una versión fija.

## Por qué existe

Hoy las skills de vídeo vienen en dos formas. Unas son paquetes cerrados: un estilo por compra, rápidos, pero no puedes ver
por dentro ni combinarlos. Otras son kits abiertos y profundos, cada uno con su propio formato, así que nada encaja entre ellos.

video-skills es la versión plana de lo primero, hecha en abierto:

- **Una entrada = un vídeo.** Cada una incluye el `result.mp4` que produjo, así que eliges con los ojos.
- **Reproducible.** Cada entrada trae un proyecto completo que renderiza su vídeo sin cambios, además de los ID de origen del material de archivo y los prompts de cualquier medio generado. No hacen falta claves de API.
- **El mismo formato en todas partes.** Todas las entradas tienen los mismos archivos y la misma ficha `taste.json`, así que puedes compararlas
  y los agentes pueden combinarlas ([spec/ENTRY.md](spec/ENTRY.md)).
- **El producto en un solo archivo.** Para poner tu producto basta con editar `film.json` y los recursos, nunca el generador.

## Biblioteca

<!-- CATALOG -->
| Preview | Entry | Category · method | Length | Events / 10 s |
|---|---|---|---|---|
| <img src="launch/broll-wheel/result/preview.gif" width="240"> | [**broll-wheel**](launch/broll-wheel/) B-roll wheel launch | launch · broll-under-type | 90 s 16:9 | 8.7 |
| <img src="launch/feature-roster/result/preview.gif" width="240"> | [**feature-roster**](launch/feature-roster/) Feature roster | launch · rebuilt-ui-roster | 26.7 s 16:9 + 9:16 | 3.0 |
<!-- /CATALOG -->

## Cómo es una entrada

```
<category>/<id>/
├── SKILL.md       cárgalo y haz el vídeo
├── taste.json     la ficha: requisitos, siete capas, especificaciones, métricas, qué necesita, para qué sirve
├── references/    floor.md (reglas compartidas), sourcing.md (launch: material real), RECIPE.md (plano a plano), SWAP.md (tu producto), REFERENCE.md
├── scripts/       setup.sh (instala lo que falta) y los scripts de medición
├── result/        result.mp4, póster, hoja de contactos, vista previa, metrics.json
└── project/       un proyecto renderizable: film.json, tools/, assets/
```

Cada entrada se sitúa en las mismas siete capas:

| Capa | Pregunta |
|---|---|
| floor | ¿Qué nunca se negocia? (solo producto real, ejemplos etiquetados, la marca) |
| category | ¿Qué tipo de vídeo? (lanzamiento, explicativo, tutorial, historia con datos, corte para redes, cortinilla) |
| method | ¿Cómo se hace la imagen y cómo avanza la columna vertebral? (b-roll bajo texto, una forma sin cortes, montaje al ritmo, UI en 3D...) |
| moves | ¿Qué recursos concretos lo llenan? (rueda entre capítulos, subrayado con marcador, montaje de anclas, morph de píldora...) |
| craft | ¿Qué lo hace parecer caro? (gancho en 3 s, ráfaga cerca del 35 %, golpes en los aterrizajes, -14 LUFS) |
| style | ¿Cómo se ve? (etalonaje, tipografía, roles de la paleta) |
| tool | ¿Con qué se renderiza? (HyperFrames, Remotion...) |

Capas distintas nunca entran en conflicto. Dentro de la misma capa: floor > category > method > moves > craft > style.

Cada entrada es autónoma: nuestros archivos compartidos (las reglas del floor, los scripts de medición) se copian dentro, las herramientas externas
(HyperFrames, ffmpeg) se declaran en `requires` de `taste.json`, y el gusto nunca se comparte. Ver [spec/ENTRY.md](spec/ENTRY.md).

## Herramientas

| | |
|---|---|
| `tools/floor.md` | las reglas compartidas del floor (copiadas en `references/` de cada entrada) |
| `launch/sourcing.md` | cómo los films de launch reúnen las pantallas, el logo y los textos reales del producto (copiado en `references/` de cada entrada de launch) |
| `tools/validate.py` | comprueba cada entrada contra el formato y que sus copias de los archivos compartidos coincidan con `tools/` |
| `tools/catalog.py` | regenera `catalog.json` y la tabla de arriba |
| `tools/analyze.py <video> <out>` | cortes, planos, hoja de contactos, LUFS, pico real, BPM, cortes en el pulso |
| `tools/events.py <video> <out>` | eventos de cambio visual cada 10 s y proporción de imagen quieta |

## Requisitos

Node 20+, ffmpeg, Python 3. Cada entrada indica qué más necesita (una versión del renderizador, un modelo de vídeo para el b-roll, un modelo de música).

## Contribuir

Las entradas nuevas son bienvenidas; ver [CONTRIBUTING.md](CONTRIBUTING.md). El listón: el proyecto renderiza su resultado sin cambios,
el producto vive en `film.json`, el resultado está medido y no se redistribuye nada de la referencia.

## Agradecimientos

Ideas y reglas tomadas, con gratitud, de [HyperFrames](https://hyperframes.heygen.com),
[huashu-motion](https://github.com/alchaincyf/huashu-motion) (ritmo y notas de dirección),
[video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) (fichas de receta y la guía de sustitución) y
[product-launch-motion](https://github.com/AbubakrChan/product-launch-motion) (detalles de oficio).

## Licencia

El ejemplo de broll-wheel es un vídeo especulativo no oficial para Muse, el agente personal de IA de Meta. No está afiliado
a Meta ni cuenta con su respaldo o patrocinio; Muse y sus recursos son de Meta y no están en este repositorio.

Código: MIT. Vídeos resultantes y medios generados: CC BY 4.0. Los recursos de los productos de ejemplo pertenecen a sus dueños; el
`taste.json` de cada entrada indica qué se puede reutilizar.
