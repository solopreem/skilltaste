"""Writes index.html and compositions/*.html for the feature-roster film (about 26.7 s, 120 BPM), 16:9 or 9:16.

Product content (copy, members, screenshots, palette, fonts, music) comes from film.json; change that, not this file.
This file holds what makes the film look like the reference: scene order and lengths, layout per ratio, eases, the
roster-to-tab-bar handoff, the camera push into each member's screenshot, the SFX cue table.
Scenes cut on 0.06 + 0.5k s (film time); with copy.credit set, a 1.2 s credit card plays first and everything starts 1.2 s later.
Run: python3 tools/build.py [16:9|9:16]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILM = json.loads((ROOT / "film.json").read_text())
C, B, P, M = FILM["copy"], FILM["brand"], FILM["palette"], FILM["members"]
SHOTS = FILM["shots"]
RATIO = sys.argv[1] if len(sys.argv) > 1 else "16:9"
W, H = (1920, 1080) if RATIO == "16:9" else (1080, 1920)
V = H > W  # vertical
COMP = ROOT / "compositions"
COMP.mkdir(exist_ok=True)
for f in COMP.glob("*.html"):
    f.unlink()

# ---------- layout per ratio ----------
L = {
    "hl": 76 if V else 92,                       # headline size
    "sub": 40 if V else 42,
    "row_y": 1240 if V else 790,                 # roster row centre (meet scene)
    "row_gap": 180 if V else 200, "row_sz": 130,
    "tab_y": 150 if V else 96, "tab_gap": 104, "tab_sz": 64, "tab_on": 92,
    "name": 76 if V else 72,
    "text_x": 80 if V else 120,
    "label_y": 300 if V else 392, "name_y": 340 if V else 432, "line_y": 436 if V else 524,
    "line_w": 920 if V else 640,
    "panel": (60, 620, 960, 1140) if V else (860, 190, 940, 760),  # x, y, w, h
    "credit_y": 110 if V else 92,
}
PANEL_X, PANEL_Y, PANEL_W, PANEL_H = L["panel"]
MAX_ZOOM = 1.7  # never show a screenshot larger than this many screen pixels per source pixel

FONTS = f"""
    @font-face {{ font-family: 'Geist'; src: url('{FILM["fonts"]["sans"]}') format('woff2'); font-weight: 100 900; }}
    @font-face {{ font-family: 'Geist Mono'; src: url('{FILM["fonts"]["mono"]}') format('woff2'); font-weight: 100 900; }}"""

BASE = f"""
    #root {{ position: absolute; inset: 0; overflow: hidden; background: {P['ground']}; color: {P['ink']};
      font-family: 'Geist', sans-serif; font-weight: 500; }}
    #root .abs {{ position: absolute; }}
    .hl {{ left: 0; width: {W}px; text-align: center; font-weight: 600; font-size: {L['hl']}px; line-height: 1.1; letter-spacing: -0.035em; }}
    .hl .w {{ display: inline-block; margin: 0 0.11em; }}
    .hl em {{ font-style: normal; background: linear-gradient({P['ink']}, {P['ink']}) no-repeat 0 96% / 0% 0.07em; }}
    .mut {{ color: {P['muted']}; }}
    .sub {{ left: 0; width: {W}px; text-align: center; font-size: {L['sub']}px; line-height: 1.3; color: {P['muted']}; font-weight: 400; }}
    .lab {{ font-family: 'Geist Mono', monospace; font-weight: 500; font-size: 26px; letter-spacing: .06em; color: {P['muted']}; }}
    .av {{ width: {L['row_sz']}px; height: {L['row_sz']}px; }}
    .av img {{ width: 100%; height: 100%; object-fit: contain; }}"""

JS_HELPERS = """
      const wIn = (s, t, st) => tl.fromTo(s, { opacity: 0, y: 24, filter: 'blur(8px)' }, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 0.5, ease: 'expo.out', stagger: st === undefined ? 0.06 : st }, t);
      const wOut = (s, t) => tl.to(s, { opacity: 0, filter: 'blur(8px)', duration: 0.22, ease: 'power2.in', stagger: 0.012 }, t);"""


def words(text, cls=""):
    """'a *b c*' -> one span per word; words between asterisks are <em>."""
    out, em = [], False
    for tok in text.split():
        start, end = tok.startswith("*"), tok.endswith("*")
        if start:
            em = True
        w = tok.strip("*")
        out.append(f'<em class="w{cls}">{w}</em>' if em else f'<span class="w{cls}">{w}</span>')
        if end:
            em = False
    return "".join(out)


SCENES = []


def add(cid, start, dur, css, html, js, track=1, z=None):
    """One scene; track > 1 marks an overlay on top of the scenes, so it gets no ground of its own."""
    if track > 1:
        css = "\n    #root { background: transparent; }" + css
    src = f"""<template>
  <style>{FONTS}{BASE}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
{html}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});{JS_HELPERS}
{js}
      tl.set({{}}, {{}}, {dur});
      window.__timelines['{cid}'] = tl;
    }})();
  </script>
</template>
"""
    (COMP / f"{cid}.html").write_text(src)
    SCENES.append((cid, start, dur, track, z))


def r(x):
    return round(x, 2)


def row_x(i, n, gap):
    return W / 2 + (i - (n - 1) / 2) * gap


N = len(M)
T_HOOK, T_MEET, T_MEM, MEM_DUR = 0.06, 4.06, 7.06, 3.0
T_END = T_MEM + N * MEM_DUR
END_DUR = 3.44
FILM_LEN = r(T_END + END_DUR)

# ---------- hook: the problem in the product's own words ----------
add("hook", T_HOOK, 4.0, f"""
    #hk {{ left: 80px; top: 0; width: {W - 160}px; height: {H}px; display: flex; flex-direction: column; justify-content: center; gap: 0.15em; }}
    #hk .hl {{ position: static; width: auto; text-wrap: balance; }}""", f"""
    <div id="hk" class="abs"><div id="a" class="hl mut">{words(C['hook_a'])}</div><div id="b" class="hl">{words(C['hook_b'])}</div></div>""", """
      wIn('#a .w', 0.1, 0.06);
      wIn('#b .w', 1.0, 0.08);
      tl.to('#b em', { backgroundSize: '100% 0.07em', duration: 0.5, ease: 'power2.inOut', stagger: 0.1 }, 1.7);
      wOut(['#a .w', '#b .w'], 3.72);""")

# ---------- meet: logo, name, promise, then the roster pops and flies up into the tab bar ----------
av_html = "".join(f'\n    <div id="r{i}" class="abs av" style="left:{row_x(i, N, L["row_gap"]) - L["row_sz"] / 2}px;top:{L["row_y"] - L["row_sz"] / 2}px">'
                  f'<img src="assets/img/av-{m["id"]}.png" alt="{m["name"]}" /></div>' for i, m in enumerate(M))
fly = "".join(
    f"\n      tl.to('#r{i}', {{ x: {r(row_x(i, N, L['tab_gap']) - row_x(i, N, L['row_gap']))}, y: {L['tab_y'] - L['row_y']}, "
    f"scale: {r((L['tab_on'] if i == 0 else L['tab_sz']) / L['row_sz'])}, opacity: {1 if i == 0 else 0.4}, duration: 0.5, ease: 'expo.inOut' }}, 2.5);"
    for i in range(N))
MARK = 120 if V else 110
add("meet", T_MEET, 3.0, f"""
    #mk {{ left: {W / 2 - MARK / 2}px; top: {L['row_y'] - (620 if V else 560)}px; width: {MARK}px; height: {MARK}px; }}
    #mk img {{ width: 100%; height: 100%; }}
    #t {{ top: {L['row_y'] - (440 if V else 400)}px; }}
    #s {{ top: {L['row_y'] - (300 if V else 270)}px; }}""", f"""
    <div id="mk" class="abs"><img src="assets/img/logo-mark.png" alt="{B['logo_alt']}" /></div>
    <div id="t" class="abs hl">{words(C['meet'])}</div>
    <div id="s" class="abs sub">{C['meet_sub']}</div>{av_html}""", f"""
      tl.fromTo('#mk', {{ opacity: 0, scale: 0.4, rotation: -20 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.6, ease: 'back.out(2)' }}, 0.04);
      wIn('#t .w', 0.2, 0.08);
      tl.fromTo('#s', {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: 'expo.out' }}, 0.6);
      for (let i = 0; i < {N}; i++) tl.fromTo('#r' + i, {{ opacity: 0, scale: 0.3, y: 30 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.45, ease: 'back.out(2)' }}, 1.06 + i * 0.125);
      wOut(['#mk', '#t .w', '#s'], 2.4);{fly}""")

# ---------- nav: the roster as a tab bar; the active member grows and gets its colour ring ----------
tab_html = "".join(f'\n    <div id="n{i}" class="abs tb" style="left:{row_x(i, N, L["tab_gap"]) - L["tab_sz"] / 2}px;top:{L["tab_y"] - L["tab_sz"] / 2}px">'
                   f'<img src="assets/img/av-{m["id"]}.png" alt="{m["name"]}" /></div>' for i, m in enumerate(M))
tab_js = ""
for k in range(N):
    t = r(k * MEM_DUR)
    for i in range(N):
        on = i == k
        tab_js += (f"\n      tl.{'set' if k == 0 else 'to'}('#n{i}', {{ scale: {r(L['tab_on'] / L['tab_sz']) if on else 1}, opacity: {1 if on else 0.4}"
                   + ("" if k == 0 else ", duration: 0.35, ease: 'expo.out'") + f" }}, {t if k == 0 else r(t - 0.08)});")
add("nav", T_MEM, N * MEM_DUR, f"""
    .tb {{ width: {L['tab_sz']}px; height: {L['tab_sz']}px; }}
    .tb img {{ width: 100%; height: 100%; object-fit: contain; }}""", tab_html, tab_js + f"""
      tl.to('.tb', {{ opacity: 0, y: -20, duration: 0.25, ease: 'power2.in' }}, {r(N * MEM_DUR - 0.3)});""", track=9, z=50)


# ---------- members: name, the product's own status line, a push into the real screen with a ring on the proof ----------
def fit(box, iw, ih):
    """Grow a source box to the panel's aspect (and to the zoom limit), keep it inside the image where possible."""
    x0, y0, x1, y1 = box
    cx, cy, bw, bh = (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0
    a = PANEL_W / PANEL_H
    bw, bh = (bh * a, bh) if bw / bh < a else (bw, bw / a)
    if PANEL_W / bw > MAX_ZOOM:
        bw, bh = PANEL_W / MAX_ZOOM, PANEL_H / MAX_ZOOM
    if bh > ih:  # never show past the image's top and bottom: crop the sides instead
        bw, bh = ih * a, ih
    if bw > iw:
        bw, bh = iw, iw / a
    cx = min(max(cx, bw / 2), iw - bw / 2) if bw <= iw else iw / 2
    cy = min(max(cy, bh / 2), ih - bh / 2) if bh <= ih else ih / 2
    return cx - bw / 2, cy - bh / 2, bw


def cam(box, iw, ih):
    x, y, bw = fit(box, iw, ih)
    s = PANEL_W / bw
    return {"x": r(-x * s), "y": r(-y * s), "scale": round(s, 4)}


for k, m in enumerate(M):
    shot = SHOTS[m["shot"]]
    iw, ih = shot["size"]
    fx0, fy0, fx1, fy1 = m["focus"]
    cx, cy, fw, fh = (fx0 + fx1) / 2, (fy0 + fy1) / 2, fx1 - fx0, fy1 - fy0
    k0 = m.get("push", 1.36) / 2  # begin this much wider than the focus, push in to it
    start = [cx - fw * k0, cy - fh * k0, cx + fw * k0, cy + fh * k0]
    c0, c1 = cam(start, iw, ih), cam(m["focus"], iw, ih)
    rx0, ry0, rx1, ry1 = m["ring"]
    bw = r(5 / c1["scale"])
    add(f"m{k}", T_MEM + k * MEM_DUR, MEM_DUR, f"""
    #lb {{ left: {L['text_x']}px; top: {L['label_y']}px; }}
    #lb b {{ display: inline-block; width: 14px; height: 14px; border-radius: 7px; background: {m['color']}; margin-right: 14px; vertical-align: 1px; }}
    #nm {{ left: {L['text_x']}px; top: {L['name_y']}px; width: {W - 2 * L['text_x']}px; text-align: left; font-size: {L['name']}px; }}
    #nm .w {{ margin: 0 0.22em 0 0; }}
    #ln {{ left: {L['text_x']}px; top: {L['line_y']}px; width: {L['line_w']}px; font-size: {L['sub'] + 4}px; line-height: 1.3; color: {P['muted']}; font-weight: 400; }}
    #ln .w {{ display: inline-block; margin-right: 0.26em; }}
    #pn {{ left: {PANEL_X}px; top: {PANEL_Y}px; width: {PANEL_W}px; height: {PANEL_H}px; border-radius: 28px; overflow: hidden;
      background: {P['panel']}; box-shadow: 0 0 0 2px {P['line']}, 0 40px 90px -30px rgba(0,0,0,.8); }}
    #cam {{ left: 0; top: 0; width: {iw}px; height: {ih}px; transform-origin: 0 0; }}
    #cam > img {{ position: absolute; left: 0; top: 0; width: {iw}px; height: {ih}px; }}
    #rg {{ left: {rx0}px; top: {ry0}px; width: {rx1 - rx0}px; height: {ry1 - ry0}px; border: {bw}px solid {m['color']}; border-radius: {r(12 / c1['scale'])}px;
      box-shadow: 0 0 0 {r(bw * 1.6)}px {m['color']}33; }}""", f"""
    <div id="lb" class="abs lab"><b></b>{k + 1:02d} / {N:02d}</div>
    <div id="nm" class="abs hl">{words(m['name'])}</div>
    <div id="ln" class="abs">{words(m['line'])}</div>
    <div id="pn" class="abs"><div id="cam" class="abs"><img src="{shot['file']}" alt="{B['name']}: {m['name']}" /><div id="rg" class="abs"></div></div></div>""", f"""
      tl.fromTo('#pn', {{ opacity: 0, y: 60, scale: 0.96 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.55, ease: 'expo.out' }}, 0);
      tl.fromTo('#cam', {json.dumps(c0)}, {{ ...{json.dumps(c1)}, duration: 2.9, ease: 'power2.inOut' }}, 0);
      tl.fromTo('#lb', {{ opacity: 0, x: -16 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: 'expo.out' }}, 0.04);
      wIn('#nm .w', 0.1, 0.07);
      wIn('#ln .w', 0.42, 0.04);
      tl.fromTo('#rg', {{ opacity: 0, scale: 1.12 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: 'expo.out' }}, 1.3);
      wOut(['#lb', '#nm .w', '#ln .w'], 2.74);
      tl.to('#pn', {{ opacity: 0, y: -30, duration: 0.24, ease: 'power2.in' }}, 2.76);""")

# ---------- end: the team gathers, logo lockup, the promise, URL, disclaimer ----------
LOCK_W = 560 if V else 520
end_av = "".join(f'\n    <div id="e{i}" class="abs ea" style="left:{row_x(i, N, 100) - 36}px;top:{H / 2 - (330 if V else 270)}px">'
                  f'<img src="assets/img/av-{m["id"]}.png" alt="{m["name"]}" /></div>' for i, m in enumerate(M))
add("end", T_END, END_DUR, f"""
    .ea {{ width: 72px; height: 72px; }}
    .ea img {{ width: 100%; height: 100%; object-fit: contain; }}
    #lk {{ left: {(W - LOCK_W) / 2}px; top: {H / 2 - (180 if V else 140)}px; width: {LOCK_W}px; }}
    #lk img {{ width: 100%; }}
    #e {{ top: {H / 2 + (40 if V else 30)}px; font-size: {L['hl'] - 16}px; }}
    #url {{ left: {(W - 300) / 2}px; top: {H / 2 + (200 if V else 160)}px; width: 300px; height: 64px; border-radius: 32px; background: {P['ink']}; color: {P['ground']};
      text-align: center; font-size: 28px; line-height: 64px; font-weight: 600; }}
    #dc {{ left: 60px; width: {W - 120}px; top: {H - (140 if V else 70)}px; text-align: center; font-size: {18 if V else 18}px; line-height: 1.5; }}""", f"""{end_av}
    <div id="lk" class="abs"><img src="assets/img/logo-lockup.png" alt="{B['logo_alt']}" /></div>
    <div id="e" class="abs hl">{words(C['end'])}</div>
    <div id="url" class="abs">{B['url']}</div>
    <div id="dc" class="abs lab">{C['disclaimer']}</div>""", f"""
      for (let i = 0; i < {N}; i++) tl.fromTo('#e' + i, {{ opacity: 0, scale: 0.3, y: 20 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.4, ease: 'back.out(2)' }}, 0.04 + i * 0.06);
      tl.fromTo('#lk', {{ opacity: 0, scale: 0.9, filter: 'blur(10px)' }}, {{ opacity: 1, scale: 1, filter: 'blur(0px)', duration: 0.6, ease: 'expo.out' }}, 0.2);
      wIn('#e .w', 0.6, 0.06);
      tl.to('#e em', {{ backgroundSize: '100% 0.07em', duration: 0.5, ease: 'power2.inOut', stagger: 0.1 }}, 1.2);
      tl.fromTo('#url', {{ opacity: 0, y: 20, scale: 0.9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.5, ease: 'back.out(1.8)' }}, 1.1);
      tl.fromTo('#dc', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 1.4);""")

# ---------- credit card: the maker's credit holds centred before the film, then flies to the top right ----------
PRE = 1.2 if C.get("credit") else 0
if PRE:
    CR_W = len(C["credit"]) * 0.62 * 26
    add("credit", -PRE, r(PRE + 3.9), f"""
    #pc {{ left: 0; top: 0; width: {W}px; height: {H}px; background: {P['ground']}; }}
    #cr {{ left: 0; top: 0; width: {W}px; height: {H}px; display: flex; align-items: center; justify-content: center; }}
    #crt {{ display: inline-block; color: {P['ink']}; white-space: nowrap; }}""", f"""
    <div id="pc" class="abs"></div>
    <div id="cr" class="abs"><span id="crt" class="lab">{C['credit']}</span></div>""", f"""
      tl.fromTo('#crt', {{ opacity: 0, scale: {1.6 if V else 2.2}, filter: 'blur(10px)' }}, {{ opacity: 1, scale: {1.6 if V else 2.2}, filter: 'blur(0px)', duration: 0.35, ease: 'expo.out' }}, 0);
      tl.set('#pc', {{ opacity: 0 }}, {PRE});
      tl.to('#crt', {{ x: {r(W - 80 - CR_W / 2 - W / 2)}, y: {r(L['credit_y'] - H / 2)}, scale: 1, color: '{P['muted']}', duration: 0.7, ease: 'expo.inOut' }}, {r(PRE - 0.1)});
      tl.to('#crt', {{ opacity: 0, duration: 0.24, ease: 'power2.in' }}, {r(PRE + 3.62)});""", track=8, z=99)
TOTAL = r(FILM_LEN + PRE)

# ---------- index ----------
hosts = []
for z, (cid, start, dur, track, zz) in enumerate(SCENES, 1):
    hosts.append(f'      <div id="{cid}" class="clip" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html"\n'
                 f'        data-start="{r(start + PRE)}" data-duration="{dur}" data-track-index="{track}" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:{zz or z}"></div>')

SFX = [  # (id, file, film time, dur, track, volume)
    *[(f"sx-h{i}", "key-press.mp3", r(1.0 + i * 0.16), 0.3, 6 + i % 2, 0.3) for i in range(3)],
    ("sx-meet", "whoosh-short.mp3", 4.0, 0.57, 4, 0.35),
    *[(f"sx-r{i}", "key-press.mp3", r(T_MEET + 1.06 + i * 0.125), 0.3, 6 + i % 2, 0.35) for i in range(N)],
    ("sx-fly", "whoosh.mp3", T_MEET + 2.45, 0.57, 4, 0.3),
    *[(f"sx-m{k}", "click-soft.mp3", r(T_MEM + k * MEM_DUR + 1.28), 0.36, 5, 0.6) for k in range(N)],
    ("sx-end", "impact-bass-1.mp3", T_END, 2.0, 3, 0.4),
]
audio = [f'      <audio id="music" src="{FILM["music"]}" data-start="{PRE}" data-duration="{FILM_LEN}" data-track-index="2" data-volume="0.75"></audio>']
for sid, f, s, d, tr, v in SFX:
    audio.append(f'      <audio id="{sid}" src="assets/sfx/{f}" data-start="{r(s + PRE)}" data-duration="{d}" data-track-index="{tr}" data-volume="{v}"></audio>')

(ROOT / "index.html").write_text(f"""<!doctype html>
<html lang="en" data-resolution="{'portrait' if V else 'landscape'}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: {P['ground']}; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <!-- generated by tools/build.py ({RATIO}); 120 BPM, scenes cut on 0.06 + 0.5k s of film time -->
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
print(RATIO, len(SCENES), "scenes,", TOTAL, "s")
