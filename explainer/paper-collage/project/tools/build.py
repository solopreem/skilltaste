"""Writes index.html and compositions/*.html for a paper-collage explainer, 16:9 or 9:16.

The story (narration, scenes, every piece of paper and where it lands) comes from film.json; change that, not this file.
This file holds the look and the motion: paper ground, b-roll under a halftone screen and grain, white-border stickers,
torn paper, typewriter labels, slaps, stamps, tape, the SFX that goes with each piece, and word-timed captions.
All times in film.json are narration seconds (assets/audio/words.json). With copy.credit set, a 1.2 s credit card plays
first and everything starts 1.2 s later.
Run: python3 tools/build.py [16:9|9:16]
"""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILM = json.loads((ROOT / "film.json").read_text())
RATIO = sys.argv[1] if len(sys.argv) > 1 else "16:9"
W, H = (1920, 1080) if RATIO == "16:9" else (1080, 1920)
V = H > W
COMP = ROOT / "compositions"
COMP.mkdir(exist_ok=True)
for f in COMP.glob("*.html"):
    f.unlink()

A, P, C = FILM["audio"], FILM["palette"], FILM["copy"]
WORDS = json.loads((ROOT / A["words"]).read_text())
LENGTH = A["length"]
INK, PAPER, RED, YEL = P["ink"], P["paper"], P["red"], P["yellow"]
COLOR = {"red": RED, "ink": INK, "yellow": YEL, "paper": PAPER}
PRE = 1.2 if C.get("credit") else 0


def r(x):
    return round(x, 2)


def pick(v):
    """A value, or {"16:9": a, "9:16": b} -> the one for this ratio."""
    return v[RATIO] if isinstance(v, dict) and RATIO in v else v


def torn(seed, jag=0.012, n=26):
    """clip-path with torn top and bottom edges; left and right stay cut straight."""
    rnd = random.Random(seed)
    top = [(i / n * 100, rnd.uniform(0, jag * 220)) for i in range(n + 1)]
    bot = [(100 - i / n * 100, 100 - rnd.uniform(0, jag * 220)) for i in range(n + 1)]
    return "polygon(" + ",".join(f"{x:.1f}% {y:.1f}%" for x, y in top + bot) + ")"


def torn_half(seed, side, jag=3.0, n=18):
    rnd = random.Random(seed)
    edge = [(50 + rnd.uniform(-jag, jag), i / n * 100) for i in range(n + 1)]
    pts = ([(0, 0)] if side == "l" else [(100, 0)]) + edge + ([(0, 100)] if side == "l" else [(100, 100)])
    return "polygon(" + ",".join(f"{x:.1f}% {y:.1f}%" for x, y in pts) + ")"


FONTS = """
    @font-face { font-family: 'Anton'; src: url('assets/fonts/anton-latin-400-normal.woff2') format('woff2'); }
    @font-face { font-family: 'Elite'; src: url('assets/fonts/special-elite-latin-400-normal.woff2') format('woff2'); }
    @font-face { font-family: 'Inter'; src: url('assets/fonts/inter-latin-700-normal.woff2') format('woff2'); font-weight: 700; }"""

CARD = f"background: #f7f2e6 url('assets/tex/paper.jpg') center / 1200px;"
BASE = f"""
    #root {{ position: absolute; inset: 0; overflow: hidden; background: {PAPER} url('assets/tex/paper.jpg') center / cover; color: {INK}; }}
    #root .abs {{ position: absolute; }}
    .stage {{ position: absolute; inset: 0; transform-origin: 50% 50%; }}
    .vid {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; filter: saturate(.35) contrast(1.18) brightness(.7); }}
    .dots {{ position: absolute; inset: 0; background: url('assets/tex/dot.png') repeat; background-size: 8px 8px; opacity: .28; mix-blend-mode: multiply; }}
    .grain {{ position: absolute; inset: 0; background: url('assets/tex/paper.jpg') center / cover; opacity: .32; mix-blend-mode: multiply; }}
    .vign {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 45%, transparent 55%, rgba(0,0,0,.45)); }}
    .stk {{ filter: drop-shadow(3px 8px 10px rgba(0,0,0,.35)); }}
    .stk img {{ display: block; width: 100%; }}
    .shadow {{ filter: drop-shadow(4px 10px 12px rgba(0,0,0,.4)); }}
    .strip {{ padding: .12em .45em .08em; background: {PAPER} url('assets/tex/paper.jpg') center / 900px; filter: drop-shadow(2px 5px 6px rgba(0,0,0,.3)); white-space: nowrap; }}
    .anton {{ font-family: 'Anton', sans-serif; text-transform: uppercase; letter-spacing: .01em; line-height: 1; }}
    .elite {{ font-family: 'Elite', monospace; }}
    .red {{ background: {RED}; color: {PAPER}; }}
    .yellow {{ background: {YEL}; color: {INK}; }}
    .ink {{ background: {INK}; color: {PAPER}; }}
    .tape {{ position: absolute; width: 150px; height: 42px; background: rgba(236,226,196,.82); box-shadow: 0 1px 3px rgba(0,0,0,.15); }}
    .row {{ position: absolute; left: 0; width: {W}px; text-align: center; }}
    .row > * {{ display: inline-block; position: relative; vertical-align: top; }}
    .hi {{ background: linear-gradient(transparent 52%, {YEL} 52%, {YEL} 92%, transparent 92%) no-repeat 0 0 / 0% 100%; }}"""

JS = """
      const slap = (s, t, rot, from) => tl.fromTo(s, { opacity: 0, scale: from || 1.3, rotation: (rot || 0) + 7 }, { opacity: 1, scale: 1, rotation: rot || 0, duration: 0.32, ease: 'back.out(2.2)' }, t);
      const rise = (s, t, rot, dy) => tl.fromTo(s, { opacity: 0, y: dy || 160, rotation: (rot || 0) - 6 }, { opacity: 1, y: 0, rotation: rot || 0, duration: 0.5, ease: 'expo.out' }, t);
      const type = (s, t, per) => tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: 0.01, stagger: per || 0.035 }, t);
      const push = (s, d, a) => tl.fromTo(s, { scale: 1 }, { scale: a || 1.05, duration: d, ease: 'none' }, 0);"""

SCENES, SFX = [], []


def cue(f, t, v=0.5):
    SFX.append((f + ".mp3", r(t + PRE), v))


def add(cid, start, dur, css, html, js, track=1, z=None):
    if track > 1:
        css = "\n    #root { background: transparent; }" + css
    (COMP / f"{cid}.html").write_text(f"""<template>
  <style>{FONTS}{BASE}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
{html}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});{JS}
{js}
      tl.set({{}}, {{}}, {dur});
      window.__timelines['{cid}'] = tl;
    }})();
  </script>
</template>
""")
    SCENES.append((cid, start, dur, track, z))


def letters(text):
    return "".join(f'<span class="c">{c}</span>' if c != " " else " " for c in text)


def place(el_id, it, inner, cls=""):
    """Position an element at it.x / it.y; x "c" centres it on a full-width row (no CSS transform, so GSAP owns transforms)."""
    x, y = pick(it.get("x", "c")), pick(it["y"])
    if x == "c":
        return (f"    #r_{el_id} {{ top: {y}px; }}\n", f'<div id="r_{el_id}" class="row"><div id="{el_id}" class="{cls}">{inner}</div></div>')
    return (f"    #{el_id} {{ left: {x}px; top: {y}px; }}\n", f'<div id="{el_id}" class="abs {cls}">{inner}</div>')


def item(sc, k, it):
    """One piece of paper. Returns css, html, js; adds its SFX. `at` is narration seconds."""
    t0 = sc["start"]
    i = f"{sc['id']}{k}"
    at = r(it.get("at", t0) - t0)
    rot = it.get("rot", 0)
    kind = it["type"]
    size = pick(it.get("size", 40))
    w = pick(it.get("w", 600))
    css, html, js = "", "", ""
    if kind == "stamp":                       # a big word stamped on: a year, a number
        col = COLOR[it.get("color", "red")]
        if it.get("box"):
            c, h = place(i, it, it["text"], "anton")
            css = c + f"    #{i} {{ font-size: {size}px; color: {col}; border: 10px solid {col}; padding: .02em .25em; mix-blend-mode: multiply; }}\n"
            js = f"tl.fromTo('#{i}', {{ opacity: 0, scale: 1.8, rotation: {rot} }}, {{ opacity: 0.92, scale: 1, rotation: {rot}, duration: 0.18, ease: 'power4.in' }}, {at});"
            cue("stamp", it["at"] + 0.12, 0.8)
        else:
            c, h = place(i, it, it["text"], "anton")
            css = c + f"    #{i} {{ font-size: {size}px; color: {col}; }}\n"
            js = f"slap('#{i}', {at}, {rot}, {it.get('from', 1.6)});"
            cue("stamp", it["at"], 0.55)
        html = h
    elif kind == "sticker":                   # a real photo, cut out, white die-cut border
        c, h = place(i, it, f'<img src="{it["src"]}" alt="{it.get("alt", "")}" />', "stk")
        css = c + f"    #{i} {{ width: {w}px; }}\n"
        html = h
        js = f"rise('#{i}', {at}, {rot}, {pick(it.get('dy', H))});"
        cue("paper", it["at"] + 0.05, 0.5)
    elif kind == "label":                     # typewriter words on a paper strip
        c, h = place(i, it, letters(it["text"]), "strip elite")
        css = c + f"    #{i} {{ font-size: {size}px; transform-origin: 0 50%; }}\n"
        html = h
        intro = (f"tl.fromTo('#{i}', {{ opacity: 0, scaleX: 0.2, rotation: {rot} }}, {{ opacity: 1, scaleX: 1, rotation: {rot}, duration: 0.25, ease: 'power3.out' }}, {at});"
                 if it.get("bar") else f"tl.set('#{i}', {{ rotation: {rot} }}, 0); tl.fromTo('#{i}', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1 }}, {at});")
        js = intro + f" type('#{i} .c', {r(at + (0.05 if it.get('bar') else 0))}, {it.get('per', 0.03)});"
    elif kind == "strip":                     # a name or a key phrase on a coloured torn strip
        c, h = place(i, it, it["text"], f"strip anton {it.get('color', 'red')}")
        css = c + f"    #{i} {{ font-size: {size}px; {it.get('css', '')} }}\n"
        html = h
        js = f"slap('#{i}', {at}, {rot}, {it.get('from', 1.35)});"
        cue("stamp", it["at"], it.get("vol", 0.55))
    elif kind == "card":                      # a torn paper card with typed lines (a cheque, a note, a receipt)
        rows = []
        for n, ln in enumerate(it["lines"]):
            st = ln.get("style", "line")
            txt = f'<span id="{i}h{n}" class="hi">{ln["text"]}</span>' if "hi" in ln else ln["text"]
            rows.append(f'<div class="{st} {"anton" if st == "big" else "elite"}">{txt}</div>')
            if "hi" in ln:
                js += f"tl.to('#{i}h{n}', {{ backgroundSize: '100% 100%', duration: 0.5, ease: 'power2.inOut' }}, {r(ln['hi'] - t0)});"
        c, h = place(i, it, f'<div class="cd">{"".join(rows)}</div>', "shadow")
        css = c + (f"    #{i} .cd {{ width: {w}px; padding: 34px 44px 30px; {CARD} clip-path: {torn(it.get('seed', 3))}; position: relative; }}\n"
                   f"    #{i} .small {{ font-size: 26px; letter-spacing: .12em; color: #6b6255; }}\n"
                   f"    #{i} .line {{ font-size: 48px; margin: 6px 0 16px; }}\n"
                   f"    #{i} .big {{ font-size: {it.get('big', 124)}px; }}\n"
                   f"    #{i} .sign {{ position: absolute; right: 50px; bottom: 30px; font-size: 24px; color: #6b6255; }}\n")
        html = h
        js = f"slap('#{i}', {at}, {rot}, 1.25);" + js
        cue("paper", it["at"], 0.6)
    elif kind == "news":                      # a newspaper clipping: masthead, headline, dek
        inner = (f'<div class="np"><div class="mast anton">{it["mast"]}</div><div class="head anton">{it["head"]}</div>'
                 f'<div class="dek elite">{it.get("dek", "")}</div></div>')
        c, h = place(i, it, inner, "shadow")
        css = c + (f"    #{i} .np {{ width: {w}px; padding: 40px 54px 50px; background: #f4efe2 url('assets/tex/paper.jpg') center / 1400px; clip-path: {torn(it.get('seed', 21), 0.01)}; }}\n"
                   f"    #{i} .mast {{ font-size: 28px; letter-spacing: .3em; border-bottom: 3px solid {INK}; padding-bottom: 10px; margin-bottom: 18px; }}\n"
                   f"    #{i} .head {{ font-size: {size}px; line-height: 1.02; }}\n"
                   f"    #{i} .dek {{ font-size: 28px; margin-top: 18px; color: #4b443a; }}\n")
        html = h
        js = f"rise('#{i}', {at}, {rot}, 220);"
        cue("paper", it["at"], 0.55)
    elif kind == "logo":                      # a real logo on torn paper; can shrink away to make room (`then`)
        c, h = place(i, it, f'<div class="lp"><img src="{it["src"]}" alt="{it.get("alt", "")}" /></div>', "shadow")
        css = c + (f"    #{i} .lp {{ padding: {it.get('pad', '34px 56px')}; {CARD} clip-path: {torn(it.get('seed', 11))}; }}\n"
                   f"    #{i} img {{ display: block; width: {w}px; }}\n")
        html = h
        js = f"slap('#{i}', {at}, {rot}, {it.get('from', 1.4)});"
        if "then" in it:
            th = it["then"]
            js += f" tl.to('#{i}', {{ y: {pick(th['dy'])}, scale: {th['scale']}, duration: 0.45, ease: 'expo.inOut' }}, {r(th['at'] - t0)});"
        cue("stamp", it["at"], 0.6)
    elif kind == "rip":                       # a logo card that tears in half on `tear`, gone by `out`
        x0 = W / 2 - w / 2 if pick(it.get("x", "c")) == "c" else pick(it["x"])
        css = (f"    #{i} .half {{ left: {x0}px; top: {pick(it['y'])}px; width: {w}px; padding: 70px 0; {CARD} text-align: center; }}\n"
               f"    #{i} .half img {{ width: 72%; }}\n    #{i}l {{ clip-path: {torn_half(it.get('seed', 5), 'l')}; }} #{i}r {{ clip-path: {torn_half(it.get('seed', 5), 'r')}; }}\n")
        html = (f'<div id="{i}" class="abs shadow" style="inset:0"><div id="{i}l" class="abs half"><img src="{it["src"]}" alt="{it.get("alt", "")}" /></div>'
                f'<div id="{i}r" class="abs half"><img src="{it["src"]}" alt="" /></div></div>')
        js = (f"slap('#{i}', {at}, {rot}, 1.3);"
              f" tl.to('#{i}l', {{ x: -90, y: 40, rotation: -9, duration: 0.45, ease: 'power3.out' }}, {r(it['tear'] - t0)});"
              f" tl.to('#{i}r', {{ x: 90, y: 70, rotation: 11, duration: 0.45, ease: 'power3.out' }}, {r(it['tear'] - t0)});"
              f" tl.to('#{i}', {{ opacity: 0, duration: 0.25 }}, {r(it['out'] - t0)});")
        cue("paper", it["at"], 0.5); cue("rip", it["tear"] - 0.05, 0.7)
    elif kind in ("clipping", "print"):       # a real chart/document (clipping) or photo (print), taped on
        ring = ""
        if "ring" in it:
            cx, cy, rx, ry = it["ring"]
            ring = (f'<svg class="ring" viewBox="0 0 100 100" preserveAspectRatio="none"><ellipse id="{i}e" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{RED}"'
                    f' vector-effect="non-scaling-stroke" style="stroke-width:7px" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" /></svg>')
            js += f" tl.to('#{i}e', {{ strokeDashoffset: 0, duration: 0.6, ease: 'power2.inOut' }}, {r(it['ring_at'] - t0)});"
        tape = it.get("tape", [42, -4])
        inner = f'<div class="pp"><img src="{it["src"]}" alt="{it.get("alt", "")}" />{ring}<div class="tape" style="left:{tape[0]}%;top:-20px;transform:rotate({tape[1]}deg)"></div></div>'
        c, h = place(i, it, inner, "shadow")
        pad = "14px" if kind == "clipping" else "12px 12px 46px"
        css = c + (f"    #{i} .pp {{ position: relative; width: {w}px; padding: {pad}; background: #fbf8f1; }}\n"
                   f"    #{i} .pp img {{ display: block; width: 100%; {'filter: grayscale(.4) contrast(1.05);' if kind == 'print' else ''} }}\n"
                   f"    #{i} .ring {{ position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }}\n")
        html = h
        dy, r0 = (-120, -6) if kind == "clipping" else (-180, 8)
        js = f"tl.fromTo('#{i}', {{ opacity: 0, y: {dy}, rotation: {r0} }}, {{ opacity: 1, y: 0, rotation: {rot}, duration: 0.5, ease: 'back.out(1.5)' }}, {at});" + js
        cue("tape", it["at"], 0.5)
    elif kind == "ticker":                    # a black tape of scrolling text across the frame
        txt = it["text"] * 3
        css = (f"    #{i} {{ left: -40px; top: {pick(it['y'])}px; width: {W + 80}px; height: 110px; background: {INK}; color: {YEL}; overflow: hidden; box-shadow: 0 8px 18px rgba(0,0,0,.4); }}\n"
               f"    #{i} .ti {{ position: absolute; left: 0; top: 18px; font-size: {size}px; white-space: nowrap; }}\n")
        html = f'<div id="{i}" class="abs"><div class="ti anton">{txt}</div></div>'
        js = (f"tl.fromTo('#{i}', {{ x: {W}, rotation: {rot} }}, {{ x: 0, rotation: {rot}, duration: 0.45, ease: 'expo.out' }}, {at});"
              f" tl.fromTo('#{i} .ti', {{ x: 0 }}, {{ x: -1400, duration: {sc['dur']}, ease: 'none' }}, {at});")
        cue("whoosh", it["at"] - 0.05, 0.45)
    elif kind == "counter":                   # a number that ticks through `values`, then lands
        vals, step = it["values"], it.get("step", 0.075)
        fmt = it.get("format", "{v}")
        html = "".join(f'<div class="abs anton {i}n" id="{i}n{n}">{fmt.format(v=f"{v:g}")}</div>' for n, v in enumerate(vals))
        css = f"    .{i}n {{ left: 0; width: {W}px; top: {pick(it['y'])}px; text-align: center; font-size: {size}px; opacity: 0; }}\n"
        for n in range(len(vals)):
            tn = r(at + n * step)
            js += f"tl.set('#{i}n{n}', {{ opacity: 1 }}, {tn});" + (f"tl.set('#{i}n{n - 1}', {{ opacity: 0 }}, {tn});" if n else "")
        land = r(at + (len(vals) - 1) * step)
        js += f"tl.fromTo('#{i}n{len(vals) - 1}', {{ scale: 1.12 }}, {{ scale: 1, duration: 0.3, ease: 'back.out(2)' }}, {land});"
        cue("tick", it["at"], 0.45); cue("stamp", it["at"] + land - at, 0.55)
    elif kind == "bar":                       # a highlighter bar that sweeps in under something
        x = pick(it.get("x", "c"))
        x = W / 2 - w / 2 if x == "c" else x
        css = f"    #{i} {{ left: {x}px; top: {pick(it['y'])}px; width: {w}px; height: 34px; background: {YEL}; transform-origin: 0 50%; mix-blend-mode: multiply; }}\n"
        html = f'<div id="{i}" class="abs"></div>'
        js = f"tl.set('#{i}', {{ rotation: {rot}, scaleX: 0 }}, 0); tl.to('#{i}', {{ scaleX: 1, duration: 0.4, ease: 'power2.inOut' }}, {at});"
    elif kind == "headline":                  # the narration's own words, revealed as they are spoken
        ws = [x for x in WORDS if it["from"] <= x[1] < it["to"]]
        html = f'<div id="{i}" class="abs anton">' + "".join(f'<span class="w" id="{i}w{n}">{x[0].rstrip(".,").upper()}</span> ' for n, x in enumerate(ws)) + "</div>"
        css = (f"    #{i} {{ left: {(W - w) / 2}px; width: {w}px; top: {pick(it['y'])}px; text-align: center; font-size: {size}px; line-height: 1.02; text-wrap: balance; }}\n"
               f"    #{i} .w {{ display: inline-block; opacity: 0; }}\n")
        js = "".join(f"tl.fromTo('#{i}w{n}', {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.18, ease: 'power3.out' }}, {r(x[1] - t0)});" for n, x in enumerate(ws))
    elif kind == "note":                      # small print: sources, credits, disclaimers
        css = f"    #{i} {{ left: {60 if V else 120}px; width: {W - (120 if V else 240)}px; bottom: {pick(it.get('bottom', 46))}px; text-align: center; font-size: {size}px; line-height: 1.45; color: #5d5549; }}\n"
        html = f'<div id="{i}" class="abs elite">{it["text"]}</div>'
        js = f"tl.fromTo('#{i}', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, {at});"
    else:
        sys.exit(f"unknown item type: {kind}")
    return css, "      " + html, "      " + js


# ---------- scenes ----------
SC = FILM["scenes"]
for n, sc in enumerate(SC):
    sc["dur"] = r((SC[n + 1]["start"] if n + 1 < len(SC) else LENGTH) - sc["start"])
for sc in SC:
    css, html, js = "", [], []
    bg = sc.get("bg", "paper")
    if bg != "paper":
        html.append(f'    <video id="v-{sc["id"]}" class="vid clip" src="{bg}" data-start="0" data-duration="{sc["dur"]}" data-track-index="0" muted playsinline></video>'
                    '<div class="dots"></div><div class="grain"></div><div class="vign"></div>')
        if sc["start"] > 0:
            cue("whoosh", sc["start"], 0.3)
    for k, it in enumerate(sc["items"]):
        c, h, j = item(sc, k, it)
        css += c; html.append(h); js.append(j)
    add(sc["id"], r(sc["start"] + PRE), sc["dur"], css,
        "\n".join(html[:1] if bg != "paper" else []) + '\n    <div class="stage" id="st">\n' + "\n".join(html[1:] if bg != "paper" else html) + "\n    </div>",
        f"      push('#st', {sc['dur']}, {sc.get('push', 1.04)});\n" + "\n".join(js))

# ---------- credit card: held on paper before the film, then flies to the top right ----------
if PRE:
    add("credit", 0, r(PRE + 3.9), f"""
    #pc {{ left: 0; top: 0; width: {W}px; height: {H}px; background: {PAPER} url('assets/tex/paper.jpg') center / cover; }}
    #cr {{ left: 0; top: 0; width: {W}px; height: {H}px; display: flex; align-items: center; justify-content: center; }}
    #crt {{ font-size: 26px; letter-spacing: .06em; white-space: nowrap; }}""", f"""
    <div id="pc" class="abs"></div>
    <div id="cr" class="abs"><span id="crt" class="strip elite">{C['credit']}</span></div>""", f"""
      tl.fromTo('#crt', {{ opacity: 0, scale: {1.6 if V else 2.2} }}, {{ opacity: 1, scale: {1.6 if V else 2.2}, duration: 0.3, ease: 'expo.out' }}, 0);
      tl.set('#pc', {{ opacity: 0 }}, {PRE});
      tl.to('#crt', {{ x: {r(W / 2 - 80 - len(C['credit']) * 0.62 * 26 / 2)}, y: {r((110 if V else 70) - H / 2)}, scale: 1, duration: 0.7, ease: 'expo.inOut' }}, {r(PRE - 0.1)});
      tl.to('#crt', {{ opacity: 0, duration: 0.24, ease: 'power2.in' }}, {r(PRE + 3.62)});""", track=8, z=98)

# ---------- captions: the narration a phrase at a time (most feeds play muted) ----------
phr, cur = [], []
for x in WORDS:
    cur.append(x)
    if x[0][-1] in ".,?!" or (len(cur) >= 9 and not x[0][0].isdigit()):
        phr.append(cur); cur = []
if cur:
    phr.append(cur)
cap_html, cap_js = [], []
for n, p in enumerate(phr):
    txt = " ".join(x[0] for x in p)
    for a, b in FILM.get("caption_fixes", {}).items():
        txt = txt.replace(a, b)
    end = phr[n + 1][0][1] if n + 1 < len(phr) else p[-1][2] + 0.6
    cap_html.append(f'    <div class="cap abs" id="c{n}"><span>{txt}</span></div>')
    cap_js.append(f"      tl.set('#c{n}', {{ opacity: 1 }}, {r(p[0][1])}); tl.set('#c{n}', {{ opacity: 0 }}, {r(min(end, p[-1][2] + 0.5))});")
add("captions", PRE, LENGTH, f"""
    .cap {{ left: 0; width: {W}px; bottom: {200 if V else 34}px; text-align: center; opacity: 0; }}
    .cap span {{ display: inline-block; max-width: {W - 160}px; padding: 6px 16px 8px; background: rgba(20,19,17,.82); color: #fff;
      font-family: 'Inter', sans-serif; font-weight: 700; font-size: {40 if V else 30}px; line-height: 1.25; }}""",
    "\n".join(cap_html), "\n".join(cap_js), track=9, z=99)

# ---------- index ----------
TOTAL = r(LENGTH + PRE)
hosts = [f'      <div id="h-{cid}" class="clip" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html"\n'
         f'        data-start="{st}" data-duration="{d}" data-track-index="{tr}" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:{zz or n + 1}"></div>'
         for n, (cid, st, d, tr, zz) in enumerate(SCENES)]
audio = [f'      <audio id="vo" src="{A["vo"]}" data-start="{PRE}" data-duration="{A["vo_length"]}" data-track-index="2" data-volume="1"></audio>',
         f'      <audio id="music" src="{A["music"]}" data-start="{PRE}" data-duration="{LENGTH}" data-track-index="3" data-volume="{A.get("music_volume", 0.32)}"></audio>']
for n, (f, t, v) in enumerate(SFX):
    audio.append(f'      <audio id="sx{n}" src="assets/audio/sfx/{f}" data-start="{t}" data-duration="1.2" data-track-index="{4 + n % 3}" data-volume="{v}"></audio>')

(ROOT / "index.html").write_text(f"""<!doctype html>
<html lang="en" data-resolution="{'portrait' if V else 'landscape'}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: {PAPER}; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <!-- generated by tools/build.py ({RATIO}) from film.json -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
{chr(10).join(hosts)}

{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print(RATIO, len(SCENES), "compositions,", TOTAL, "s,", len(SFX), "sfx")
