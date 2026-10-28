"""Writes index.html and compositions/*.html for the broll-wheel-launch film (90 s, 16:9, 30 fps, 120 BPM).

Product content (copy, images, card geometry, palette, fonts, music) comes from film.json; change that, not this file.
This file holds what makes the film look like the reference: scene order and lengths, eases, holds, the beat grid,
the SFX cue table. Scenes cut on 0.06 + 2k s; beats sit at 0.056 + 0.5k s.
The template palette (paper #f7f4e5, ink #192219, ground #324632, accent #d7ff00 ...) is rewritten to film.json's palette
by recolour() at write time. B-roll: tools/stock.sh -> assets/broll/ -> tools/cuts.py -> assets/graded/, assets/cuts/. Run: python3 tools/build.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILM = json.loads((ROOT / "film.json").read_text())
C, IMG, B = FILM["copy"], FILM["images"], FILM["brand"]
# the template was tuned in these colours; add() maps each to the film.json palette at write time
TEMPLATE_HEX = {"#f7f4e5": "paper", "#fffdf3": "paper_light", "#ece7d2": "paper_edge", "#192219": "ink", "#324632": "ground",
                "#778561": "ground_light", "#d7ff00": "accent", "#626854": "muted", "#cbcdb9": "line"}


def recolour(src):
    for hx, k in TEMPLATE_HEX.items():
        src = re.sub(re.escape(hx), FILM["palette"][k], src, flags=re.I)
    return src
COMP = ROOT / "compositions"
COMP.mkdir(exist_ok=True)

FONTS = """
    @font-face { font-family: 'Bricolage'; src: url('""" + FILM["fonts"]["display"] + """') format('woff2'); font-weight: 200 800; }
    @font-face { font-family: 'DM Sans'; src: url('""" + FILM["fonts"]["body"] + """') format('woff2'); font-weight: 100 1000; }"""

BASE = """
    #root { position: absolute; inset: 0; overflow: hidden; font-family: 'DM Sans', sans-serif; font-weight: 500; }
    #root .abs { position: absolute; }
    .st { left: 0; width: 1920px; text-align: center; font-family: 'Bricolage', sans-serif; font-weight: 700; font-size: 84px; line-height: 1.12;
      letter-spacing: -0.03em; white-space: nowrap; }
    .st .w, .hl .w { display: inline-block; margin: 0 0.1em; }
    .hl { font-family: 'Bricolage', sans-serif; font-weight: 700; font-size: 76px; line-height: 1.08; letter-spacing: -0.03em; }
    .hl .w { margin: 0 0.22em 0 0; }
    .mono { font-family: 'JetBrains Mono', monospace; font-weight: 500; }
    .lab { font-family: 'JetBrains Mono', monospace; font-weight: 500; font-size: 28px; letter-spacing: .02em; color: #626854; }
    .sub { font-size: 36px; line-height: 1.35; color: #626854; }
    .card { border-radius: 28px; overflow: hidden; background: #fffdf3; border: 2px solid #cbcdb9; box-shadow: 0 30px 70px -30px rgba(25,34,25,.35); }
    .card img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; object-position: left top; }
    .bar { left: 0; top: 0; width: 100%; height: 44px; background: #f2efdd; border-bottom: 2px solid #e2e0cc; z-index: 3; }
    .bar i { position: absolute; top: 15px; width: 12px; height: 12px; border-radius: 6px; background: #cbcdb9; }
    .chip { right: 16px; top: 8px; height: 28px; padding: 0 14px; border-radius: 14px; background: #e9ecd8; font-family: 'JetBrains Mono', monospace;
      font-size: 19px; line-height: 28px; color: #49513f; white-space: nowrap; }
    .scr { left: 0; top: 44px; width: 100%; overflow: hidden; }
    .ring { border: 6px solid #192219; border-radius: 14px; z-index: 4; box-shadow: 0 0 0 6px #d7ff00; }
    .tile { border-radius: 26%; overflow: hidden; background: #f5f0d9; }
    .tile img { width: 100%; height: 100%; object-fit: cover; }
    #root .bg { left: 0; top: 0; width: 1920px; height: 1080px; object-fit: cover; }"""

MODE = {
    # light: the accent is a marker swept behind ink
    "light": """
    #root { background: radial-gradient(ellipse 75% 70% at 50% 42%, #fffdf3 0%, #f7f4e5 55%, #ece7d2 100%); color: #192219; }
    #root em { font-style: normal; background: linear-gradient(#d7ff00, #d7ff00) no-repeat 0 88% / 100% 40%; }""",
    # dark: the accent is a block with ink type
    # footage: real-world b-roll under cream type, the accent is the block
    "film": """
    #root { background: #192219; color: #f7f4e5; }
    #root .st, #root .hl, #root .wi, #root .sub { text-shadow: 0 2px 30px rgba(10,16,10,.55); }
    #root em { font-style: normal; color: #192219; background: #d7ff00; padding: 0 0.12em; border-radius: 0.12em; text-shadow: none; }""",
    "dark": """
    #root { background: #324632; color: #f7f4e5; }
    #root em { font-style: normal; color: #192219; background: #d7ff00; padding: 0 0.12em; border-radius: 0.12em; }""",
}

JS_HELPERS = """
      const wIn = (s, t, st) => tl.fromTo(s, { opacity: 0, x: 26, filter: 'blur(10px)' }, { opacity: 1, x: 0, filter: 'blur(0px)', duration: 0.6, ease: 'expo.out', stagger: st === undefined ? 0.08 : st }, t);
      const wOut = (s, t) => tl.to(s, { opacity: 0, filter: 'blur(8px)', duration: 0.24, ease: 'power2.in', stagger: 0.015 }, t);
      const mark = (s, t) => tl.fromTo(s, { backgroundSize: '0% 40%' }, { backgroundSize: '100% 40%', duration: 0.5, ease: 'power2.inOut', stagger: 0.12 }, t);"""

HIDE = re.compile(r"^\s*tl\.set\((\[[^\]]*\]|'[^']*'), \{ opacity: 0 \}, 0\);\n", re.M)


def words(text):
    """'Don't get distilled *for free.*' -> spans; a *...* run becomes one accent unit so the marker is continuous."""
    out, acc = [], []
    for tok in text.split():
        if tok.startswith("*") or acc:
            acc.append(tok.lstrip("*"))
            if tok.endswith("*"):
                out.append(f'<em class="w">{" ".join(acc)[:-1]}</em>')
                acc = []
            continue
        out.append(f'<span class="w">{tok}</span>')
    return "".join(out)


SCENES = []


def add(cid, start, dur, mode, css, html, js, overflow=False, fill=None):
    ov = " data-layout-allow-overflow" if overflow else ""
    hidden = [x.strip().strip("'") for m in HIDE.findall(js) for x in m.strip("[]").split(",")]
    js = HIDE.sub("", js)
    if hidden:
        css += "\n    " + ", ".join(hidden) + " { opacity: 0; }"
    src = f"""<template>
  <style>{FONTS}{BASE}{MODE[mode]}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080"{ov}>
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
    for k, v in (fill or {}).items():
        src = src.replace(f"__{k}__", str(v))
    (COMP / f"{cid}.html").write_text(recolour(src.replace('REFER_N', str(C['refer_number'])).replace('REFER_U', C.get('refer_unit', '%'))))
    SCENES.append((cid, start, dur))


LOGO = B["logo"]


def video(cut, dur, start=0, vid="v", z=0):
    """A graded b-roll segment from assets/cuts/ as a full-frame clip inside a scene."""
    return (f'    <video id="{vid}" class="abs bg clip" src="assets/cuts/{cut}.mp4" data-start="{start}" data-duration="{dur}"'
            f' data-track-index="{z}" muted playsinline></video>')


# ---------- 0.00 open on a real desk at night: the person is in frame 0, type lands on the beats ----------
add("open", 0, 6.06, "film", """
    #mk { left: 120px; top: 110px; width: 92px; height: 92px; }
    #a { left: 120px; top: 640px; text-align: left; width: auto; font-size: 92px; }
    #b { left: 120px; top: 640px; text-align: left; width: auto; font-size: 92px; }""",
    video("open", 6.06) + f"""
    <div id="mk" class="abs tile"><img src="{LOGO}" alt="{B['logo_alt']}" /></div>
    <div id="a" class="abs st"><span class="w ast">✳</span>{words(C['open_a'])}</div>
    <div id="b" class="abs st">{words(C['open_b'])}</div>""",
    """      // footage is already moving at frame 0; the first words land on the first beat
      tl.fromTo('#v', { scale: 1.12 }, { scale: 1, duration: 6.06, ease: 'power1.out' }, 0);
      tl.fromTo('#mk', { opacity: 0, scale: 0.6, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.6, ease: 'back.out(2)' }, 0.06);
      tl.fromTo('#a .ast', { rotation: -90 }, { rotation: 0, duration: 0.8, ease: 'expo.out' }, 0.3);
      wIn('#a .w', 0.3, 0.09);
      wOut('#a .w', 2.82);
      wIn('#b .w', 3.06, 0.08);
      mark('#b em', 3.6);
      wOut(['#b .w', '#mk'], 5.82);""")

WHEEL = C["wheel"]


def wheel(cid, start, f0, f1):
    items = "".join(f'<div class="wi" id="wi{i}">{w}</div>' for i, w in enumerate(WHEEL))
    add(cid, start, 2.04, "film", """
    #yr { left: 0; top: 470px; width: 880px; text-align: right; }
    #yr span { display: inline-block; font-family: 'Bricolage', sans-serif; font-weight: 700; font-size: 110px; line-height: 136px; letter-spacing: -0.03em;
      color: #192219; background: #d7ff00; padding: 0 22px; border-radius: 14px; }
    #col { left: 930px; top: 470px; }
    .wi { height: 136px; font-family: 'Bricolage', sans-serif; font-weight: 700; font-size: 110px; line-height: 136px; letter-spacing: -0.03em; white-space: nowrap; }""",
        video(cid, 2.04) + f"""
    <div id="yr" class="abs"><span>{C['wheel_lead']}</span></div>
    <div id="col" class="abs">{items}</div>""",
        f"""      const N = {len(WHEEL)};
      tl.fromTo('#v', {{ scale: 1.1 }}, {{ scale: 1, duration: 2.04, ease: 'power1.out' }}, 0);
      const st = (i, f) => {{ const d = Math.abs(i - f); return {{ color: '#f7f4e5', opacity: d < 0.5 ? 1 : Math.max(0.06, 0.45 - d * 0.14) }}; }};
      for (let i = 0; i < N; i++) tl.set('#wi' + i, st(i, {f0}), 0);
      tl.set('#col', {{ y: {-f0 * 136} }}, 0);
      tl.fromTo(['#yr', '#col'], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, 0);
      // the wheel rolls one word on the next beat
      tl.to('#col', {{ y: {-f1 * 136}, duration: 0.7, ease: 'expo.inOut' }}, 0.32);
      for (let i = 0; i < N; i++) tl.to('#wi' + i, {{ ...st(i, {f1}), duration: 0.5, ease: 'power2.out' }}, 0.42);
      tl.to(['#yr', '#col'], {{ opacity: 0, filter: 'blur(8px)', duration: 0.22, ease: 'power2.in' }}, 1.8);""", overflow=True)


wheel("wheel1", 6.06, -0.8, 0)

# ---------- 8.06 the brand's wide illustration: the problem ----------
add("feast", 8.06, 4.04, "light", """
    #fv { left: 0; top: 120px; width: 1920px; height: 640px; overflow: hidden; }
    #fv img { position: absolute; left: -126px; top: 0; width: 2172px; height: 724px; transform-origin: 50% 70%; }
    #cap { top: 820px; }""",
    f"""    <div id="fv" class="abs"><img id="fi" src="{IMG['illustration']['src']}" alt="{IMG['illustration']['alt']}" /></div>
    <div id="cap" class="abs st">{words(C['problem'])}</div>""",
    """      tl.fromTo('#fi', { scale: 1 }, { scale: 1.14, duration: 4.0, ease: 'none' }, 0);
      tl.fromTo('#fv', { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0);
      wIn('#cap .w', 0.6, 0.09);
      mark('#cap em', 1.4);
      tl.to(['#fv', '#cap'], { opacity: 0, filter: 'blur(8px)', duration: 0.25, ease: 'power2.in' }, 3.78);""")

# ---------- 12.06 what you can sell (site copy) ----------
add("sell", 12.06, 3.04, "film", """
    #s1 { top: 330px; }
    #chips { left: 0; top: 500px; width: 1920px; display: flex; justify-content: center; gap: 28px; }
    .ch { height: 104px; padding: 0 44px; border-radius: 52px; border: 4px solid #192219; background: #fffdf3; color: #192219; text-shadow: none; font-family: 'Bricolage', sans-serif;
      font-weight: 700; font-size: 52px; line-height: 96px; letter-spacing: -0.02em; }
    #s2 { left: 0; top: 700px; width: 1920px; text-align: center; color: #f7f4e5; }""",
    # the chips stay locked while the world behind them cuts on each chip's beat
    video("sell0", 1.44) + video("sell1", 0.5, 1.44, "v1") + video("sell2", 1.1, 1.94, "v2") + f"""
    <div id="s1" class="abs st">{words(C['sell_head'])}</div>
    <div id="chips" class="abs">{''.join(f'<div class="ch" id="c{i}">{t}</div>' for i, t in enumerate(C['sell_chips']))}</div>
    <div id="s2" class="abs sub">{C['sell_sub']}</div>""",
    """      wIn('#s1 .w', 0.04, 0.08);
      ['#c0', '#c1', '#c2'].forEach((s, i) => tl.fromTo(s, { opacity: 0, y: 40, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: 'back.out(2)' }, 0.94 + i * 0.5));
      tl.to('#c0', { backgroundColor: '#d7ff00', duration: 0.2 }, 0.94);
      tl.to('#c0', { backgroundColor: '#fffdf3', duration: 0.2 }, 1.44);
      tl.to('#c1', { backgroundColor: '#d7ff00', duration: 0.2 }, 1.44);
      tl.to('#c1', { backgroundColor: '#fffdf3', duration: 0.2 }, 1.94);
      tl.to('#c2', { backgroundColor: '#d7ff00', duration: 0.2 }, 1.94);
      tl.fromTo('#s2', { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: 'expo.out' }, 1.0);
      tl.fromTo('#v2', { scale: 1.08 }, { scale: 1, duration: 1.1, ease: 'none' }, 1.94);
      tl.to(['#s1', '#chips', '#s2'], { opacity: 0, filter: 'blur(8px)', duration: 0.24, ease: 'power2.in' }, 2.8);""")

# ---------- 15.06 site headline ----------
add("same", 15.06, 3.04, "light", """
    #l1 { top: 400px; } #l2 { top: 500px; }""",
    f"""    <div id="l1" class="abs st">{words(C['same_1'])}</div>
    <div id="l2" class="abs st">{words(C['same_2'])}</div>""",
    """      wIn('#l1 .w', 0.04, 0.1);
      wIn('#l2 .w', 0.5, 0.08);
      mark('#l2 em', 1.2);
      wOut(['#l1 .w', '#l2 .w'], 2.8);""")

APP = IMG["app"]
# the push brings the focus point to frame centre; the card sits at (210, 96)
APP_FILL = {"RGX": APP["ring"][0], "RGY": APP["ring"][1], "RGW": APP["ring"][2], "RGH": APP["ring"][3], "TY": APP["cursor_tabs_y"],
            **{f"TX{i}": x for i, x in enumerate(APP["cursor_tabs_x"])}, "PZ": APP["push_zoom"], "PFX": APP["push_focus"][0],
            "PFY": APP["push_focus"][1], "PX": 960 - (210 + APP["push_focus"][0]), "PY": 540 - (96 + APP["push_focus"][1])}
# ---------- 18.06 the real app: card grows, cursor walks the tabs, push into the panel ----------
add("app", 18.06, 6.04, "light", """
    #cd { left: 210px; top: 96px; width: 1500px; height: 888px; }
    #cd .scr { height: 844px; }
    #rg { left: __RGX__px; top: __RGY__px; width: __RGW__px; height: __RGH__px; }
    #cur { left: 0; top: 0; width: 52px; height: 52px; z-index: 6; }""",
    f"""    <div id="cd" class="abs card">
      <div class="abs bar"><i style="left:18px"></i><i style="left:38px"></i><i style="left:58px"></i><div class="abs chip">{IMG['app']['chip']}</div></div>
      <div class="abs scr"><img src="{IMG['app']['src']}" alt="{IMG['app']['alt']}" /></div>
      <div id="rg" class="abs ring"></div>
    </div>
    <svg id="cur" class="abs" viewBox="0 0 24 24"><path d="M3 2 L3 19 L8 14.5 L11.5 22 L14.5 20.6 L11 13.4 L17.5 13.4 Z" fill="#192219" stroke="#fffdf3" stroke-width="1.4" stroke-linejoin="round"/></svg>""",
    """      tl.set(['#rg', '#cur'], { opacity: 0 }, 0);
      tl.fromTo('#cd', { scale: 0.38, y: 40, opacity: 0 }, { scale: 0.38, y: 40, opacity: 1, duration: 0.3 }, 0);
      tl.to('#cd', { scale: 1, y: 0, duration: 1.1, ease: 'expo.inOut' }, 0.3);
      // cursor walks the app's real tabs: My data, Marketplace, Earnings, Purchases & receipts
      tl.fromTo('#cur', { opacity: 0, x: 1100, y: 420 }, { opacity: 1, x: __TX0__, y: __TY__, duration: 0.6, ease: 'power2.out' }, 1.3);
      tl.to('#cur', { x: __TX1__, duration: 0.35, ease: 'power2.inOut' }, 1.94);
      tl.to('#cur', { x: __TX2__, duration: 0.35, ease: 'power2.inOut' }, 2.44);
      tl.to('#cur', { x: __TX3__, duration: 0.35, ease: 'power2.inOut' }, 2.94);
      tl.to('#cur', { opacity: 0, duration: 0.2 }, 3.4);
      // push into the app's own "you did the work -> an item sold" panel
      tl.to('#cd', { scale: __PZ__, x: __PX__, y: __PY__, transformOrigin: '__PFX__px __PFY__px', duration: 1.0, ease: 'expo.inOut' }, 3.5);
      tl.fromTo('#rg', { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.4, ease: 'expo.out' }, 4.5);
      tl.to('#cd', { opacity: 0, duration: 0.24, ease: 'power2.in' }, 5.78);""", fill=APP_FILL)

wheel("wheel2", 24.06, 0, 1)


def split_card(cid, start, dur, head, sub, img, alt, iw, ih, scale, left, top, rings, label, extra_js="", bg=None):
    """Headline on the left, a real site crop on the right that pushes in, rings land in order; bg = b-roll cut behind it."""
    rs = "".join(f'<div id="r{i}" class="abs ring" style="left:{x * scale - 10:.0f}px;top:{y * scale - 10:.0f}px;width:{w * scale + 20:.0f}px;height:{h * scale + 20:.0f}px"></div>'
                 for i, (x, y, w, h, _) in enumerate(rings))
    rjs = "".join(f"""
      tl.fromTo('#r{i}', {{ opacity: 0, scale: 1.25 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: 'expo.out' }}, {t});""" +
                  (f"\n      tl.to('#r{i}', {{ opacity: 0, duration: 0.15 }}, {rings[i + 1][4] - 0.1});" if i + 1 < len(rings) else "")
                  for i, (_, _, _, _, t) in enumerate(rings))
    add(cid, start, dur, "film" if bg else "light", f"""
    #hd {{ left: 120px; top: 300px; width: 700px; }}
    #root .lab {{ color: {'#f7f4e5' if bg else '#626854'}; }}
    #root .sub {{ color: {'#f7f4e5' if bg else '#626854'}; }}
    #cd {{ box-shadow: 0 50px 120px -30px rgba(10,16,10,.6); }}
    #sb {{ left: 120px; top: 640px; width: 640px; }}
    #cd {{ left: {left}px; top: {top}px; width: {iw * scale:.0f}px; height: {ih * scale:.0f}px; }}
    #lb {{ left: {left}px; top: {top + ih * scale + 26:.0f}px; }}""",
        (video(bg, dur) + "\n" if bg else "") + f"""    <div id="hd" class="abs hl">{words(head)}</div>
    <div id="sb" class="abs sub">{sub}</div>
    <div id="cd" class="abs card"><img src="assets/img/{img}" alt="{alt}" />{rs}</div>
    <div id="lb" class="abs lab">{label}</div>""",
        """      wIn('#hd .w', 0.04, 0.08);
      mark('#hd em', 0.8);
      tl.fromTo('#cd', { opacity: 0, scale: 0.7, x: 120 }, { opacity: 1, scale: 1, x: 0, duration: 0.9, ease: 'expo.out' }, 0.2);
      tl.fromTo('#sb', { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: 'expo.out' }, 1.2);
      tl.fromTo('#lb', { opacity: 0 }, { opacity: 1, duration: 0.3 }, 1.0);""" + rjs + extra_js + (f"""
      tl.fromTo('#v', {{ scale: 1.0, x: 0 }}, {{ scale: 1.1, x: -40, duration: {dur}, ease: 'none' }}, 0);""" if bg else "") + f"""
      tl.to(['#hd', '#sb', '#cd', '#lb'], {{ opacity: 0, filter: 'blur(8px)', duration: 0.24, ease: 'power2.in' }}, {round(dur - 0.26, 2)});""")


# ---------- 26.06 chapter: tools (real site card) ----------
split_card("tools", 26.06, 6.04, C["tools_head"],
           C["tools_sub"],
           IMG["tools_card"]["src"], IMG["tools_card"]["alt"],
           *IMG["tools_card"]["size"], IMG["tools_card"]["scale"], *IMG["tools_card"]["pos"],
           [tuple(r) for r in IMG["tools_card"]["rings"]],
           C["tools_label"], bg="tools")

# ---------- 32.06 the burst: the world cuts on every beat (then every half beat) behind one locked caption, ----------
# ---------- and lands on the brand's mascot ----------
MONTAGE = [0, 0.5, 1.0, 1.5, 2.0, 2.25, 2.5, 2.75, 3.0]  # cut times; m0..m7, then the mascot on paper
add("brain", 32.06, 4.04, "film", """
    #pp { left: 0; top: 0; width: 1920px; height: 1080px; background: radial-gradient(ellipse 75% 70% at 50% 42%, #fffdf3 0%, #f7f4e5 55%, #ece7d2 100%); z-index: 1; }
    #br { left: 230px; top: 250px; width: 520px; height: 520px; border-radius: 40px; box-shadow: 0 30px 70px -30px rgba(25,34,25,.35); z-index: 2; }
    #cp { left: 360px; top: 800px; width: 1200px; height: 150px; border-radius: 28px; background: #fffdf3; z-index: 3;
      box-shadow: 0 40px 90px -30px rgba(10,16,10,.55); }
    #bt { left: 0; top: 0; width: 1200px; height: 150px; text-align: center; line-height: 150px; color: #192219; font-size: 62px; white-space: nowrap; text-shadow: none; }
    #bt .pl { left: 0; top: 0; width: 1200px; text-align: center; }
    #bt em { color: #192219; background: linear-gradient(#d7ff00, #d7ff00) no-repeat 0 88% / 100% 40%; padding: 0; }""",
    "\n".join(video(f"m{i}", round(MONTAGE[i + 1] - MONTAGE[i], 2), MONTAGE[i], f"v{i}") for i in range(8)) + f"""
    <div id="pp" class="abs"></div>
    <img id="br" class="abs" src="{IMG['mascot']['src']}" alt="{IMG['mascot']['alt']}" />
    <div id="cp" class="abs"><div id="bt" class="abs hl"><div id="p0" class="abs pl">{words(C['montage_a'])}</div><div id="p1" class="abs pl">{words(C['montage_b'])}</div></div></div>""",
    """      tl.set(['#pp', '#br', '#p1'], { opacity: 0 }, 0);
      // every shot enters already moving
      [0, 1, 2, 3, 4, 5, 6, 7].forEach((i) => tl.fromTo('#v' + i, { scale: 1.14 }, { scale: 1.0, duration: 0.6, ease: 'expo.out' }, [0, 0.5, 1.0, 1.5, 2.0, 2.25, 2.5, 2.75][i]));
      tl.fromTo('#cp', { opacity: 0, y: 40, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: 'back.out(1.8)' }, 0.04);
      wIn('#p0 .w', 0.1, 0.08);
      tl.to('#p0', { opacity: 0, filter: 'blur(6px)', duration: 0.18 }, 1.38);
      tl.set('#p1', { opacity: 1 }, 1.5);
      wIn('#p1 .w', 1.5, 0.06);
      // 35.06: hard cut to paper, the mascot slams in, the caption rides up beside it
      tl.set('#pp', { opacity: 1 }, 3.0);
      tl.fromTo('#br', { opacity: 0, scale: 0.5, rotation: -14 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.55, ease: 'back.out(2)' }, 3.0);
      tl.to('#cp', { x: 420, y: -420, scale: 0.92, boxShadow: '0 0 0 0 rgba(0,0,0,0)', duration: 0.5, ease: 'expo.out' }, 3.0);
      mark('#bt em', 3.3);
      tl.to(['#br', '#cp'], { opacity: 0, filter: 'blur(8px)', duration: 0.22, ease: 'power2.in' }, 3.8);""")

wheel("wheel3", 36.06, 1, 2)

# ---------- 38.06 chapter: private (illustrative session card -> vault) ----------
add("vault", 38.06, 6.04, "light", """
    #hd { top: 110px; }
    #vt { left: 560px; top: 330px; width: 800px; height: 470px; border-radius: 30px; background: #324632; }
    #ss { left: 610px; top: 300px; width: 700px; height: 400px; z-index: 2; }
    #ss .h { left: 40px; top: 32px; font-family: 'Bricolage', sans-serif; font-weight: 700; font-size: 40px; letter-spacing: -0.02em; }
    .ln { left: 40px; width: 620px; font-size: 30px; line-height: 44px; color: #192219; white-space: nowrap; }
    .hx { left: 40px; width: 620px; font-size: 30px; line-height: 44px; color: #778561; white-space: nowrap; }
    #l1, #x1 { top: 120px; } #l2, #x2 { top: 180px; } #l3, #x3 { top: 240px; }
    #lk { left: 1210px; top: 270px; width: 120px; height: 120px; border-radius: 26px; background: #192219; z-index: 3; display: flex; align-items: center; justify-content: center; }
    #lk svg { width: 64px; height: 64px; }
    #pv { left: 640px; top: 728px; z-index: 3; font-family: 'JetBrains Mono', monospace; font-size: 28px; color: #f7f4e5; }
    #sb { left: 0; top: 860px; width: 1920px; text-align: center; }
    #il { right: 60px; bottom: 40px; font-size: 22px; }""",
    f"""    <div id="hd" class="abs st">{words(C['vault_head'])}</div>
    <div id="vt" class="abs"></div>
    <div id="ss" class="abs card" style="overflow:hidden">
      <div class="abs h">{C['vault_title']}</div>
      <div id="l1" class="abs ln mono">{C['vault_lines'][0]}</div>
      <div id="l2" class="abs ln mono">{C['vault_lines'][1]}</div>
      <div id="l3" class="abs ln mono">{C['vault_lines'][2]}</div>
      <div id="x1" class="abs hx mono">{C['vault_hashes'][0]}</div>
      <div id="x2" class="abs hx mono">{C['vault_hashes'][1]}</div>
      <div id="x3" class="abs hx mono">{C['vault_hashes'][2]}</div>
    </div>
    <div id="lk" class="abs"><svg viewBox="0 0 24 24"><rect x="5" y="10.5" width="14" height="10" rx="2.2" fill="#d7ff00"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5" fill="none" stroke="#d7ff00" stroke-width="2.4"/></svg></div>
    <div id="pv" class="abs">{C['vault_private']}</div>
    <div id="sb" class="abs sub">{C['vault_sub']}</div>
    <div id="il" class="abs lab" data-layout-ignore>{C['vault_label']}</div>""",
    """      tl.set(['#x1', '#x2', '#x3', '#lk', '#pv', '#vt'], { opacity: 0 }, 0);
      wIn('#hd .w', 0.04, 0.08);
      tl.fromTo('#ss', { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.6, ease: 'expo.out' }, 0.3);
      ['#l1', '#l2', '#l3'].forEach((s, i) => tl.fromTo(s, { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.35, ease: 'expo.out' }, 0.7 + i * 0.25));
      mark('#hd em', 1.2);
      // 40.06: the vault slides in behind, the lock lands, each line turns into its hash
      tl.fromTo('#vt', { opacity: 0, y: 300, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.7, ease: 'expo.out' }, 1.94);
      tl.fromTo('#lk', { opacity: 0, y: -140, scale: 0.6 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: 'back.out(2.2)' }, 2.44);
      [['#l1', '#x1'], ['#l2', '#x2'], ['#l3', '#x3']].forEach(([a, b], i) => {
        tl.to(a, { opacity: 0, filter: 'blur(6px)', duration: 0.2 }, 2.94 + i * 0.12);
        tl.fromTo(b, { opacity: 0, filter: 'blur(6px)' }, { opacity: 1, filter: 'blur(0px)', duration: 0.3 }, 3.04 + i * 0.12);
      });
      tl.to('#ss', { y: -40, duration: 0.6, ease: 'power3.inOut' }, 3.0);
      tl.fromTo('#pv', { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.4 }, 3.5);
      tl.fromTo('#sb', { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: 'expo.out' }, 3.9);
      tl.to('#root > *', { opacity: 0, filter: 'blur(8px)', duration: 0.24, ease: 'power2.in' }, 5.78);""")

wheel("wheel4", 44.06, 2, 3)

# ---------- 46.06 chapter: terms (real worked-example card) ----------
split_card("terms", 46.06, 6.04, C["terms_head"],
           C["terms_sub"],
           IMG["terms_card"]["src"], IMG["terms_card"]["alt"],
           *IMG["terms_card"]["size"], IMG["terms_card"]["scale"], *IMG["terms_card"]["pos"],
           [tuple(r) for r in IMG["terms_card"]["rings"]],
           C["terms_label"], bg="terms",
           extra_js="""
      tl.to('#cd', { scale: 1.06, duration: 1.4, ease: 'power2.inOut' }, 3.2);""")

wheel("wheel5", 52.06, 3, 4)

# ---------- 54.06 the site's trade-proof path, stage by stage ----------
STAGES = IMG["flow"]["stages_x"]
add("proof", 54.06, 4.04, "light", """
    #hd { top: 110px; }
    #fl { left: 160px; top: 290px; width: 1600px; height: 620px; }
    .sg { top: 380px; width: 330px; height: 520px; border: 6px solid #192219; border-radius: 22px; box-shadow: 0 0 0 6px #d7ff00; }
    #sb { left: 0; top: 950px; width: 1920px; text-align: center; }""",
    f"""    <div id="hd" class="abs st">{words(C['proof_head'])}</div>
    <img id="fl" class="abs" src="{IMG['flow']['src']}" alt="{IMG['flow']['alt']}" />
    {''.join(f'<div id="g{i}" class="abs sg" style="left:{160 + x - 16}px"></div>' for i, x in enumerate(STAGES))}
    <div id="sb" class="abs sub">{C['proof_sub']}</div>""",
    """      tl.set(['#g0', '#g1', '#g2', '#g3', '#g4'], { opacity: 0 }, 0);
      wIn('#hd .w', 0.04, 0.1);
      mark('#hd em', 0.7);
      tl.fromTo('#fl', { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.6, ease: 'expo.out' }, 0.15);
      // the focus ring walks the five stages, one per beat
      [0, 1, 2, 3, 4].forEach((i) => {
        tl.fromTo('#g' + i, { opacity: 0, scale: 1.08 }, { opacity: 1, scale: 1, duration: 0.25, ease: 'expo.out' }, 0.94 + i * 0.5);
        if (i < 4) tl.to('#g' + i, { opacity: 0, duration: 0.15 }, 1.38 + i * 0.5);
      });
      tl.fromTo('#sb', { opacity: 0 }, { opacity: 1, duration: 0.4 }, 1.6);
      tl.to('#root > *', { opacity: 0, filter: 'blur(8px)', duration: 0.24, ease: 'power2.in' }, 3.78);""")

# ---------- 58.06 the site's three steps ----------
add("steps", 58.06, 4.04, "light", """
    #hd { top: 230px; }
    .cl { top: 470px; width: 480px; }
    .cl .n { width: 76px; height: 76px; border-radius: 38px; background: #324632; color: #f7f4e5; font-family: 'Bricolage', sans-serif; font-weight: 700;
      font-size: 40px; line-height: 76px; text-align: center; }
    .cl .t { margin-top: 30px; font-family: 'Bricolage', sans-serif; font-weight: 700; font-size: 52px; line-height: 1.05; letter-spacing: -0.02em; }
    .cl .d { margin-top: 18px; font-size: 32px; line-height: 1.35; color: #626854; }
    #k0 { left: 180px; } #k1 { left: 720px; } #k2 { left: 1260px; }""",
    f"""    <div id="hd" class="abs st">{words(C['steps_head'])}</div>
    <div id="k0" class="abs cl"><div class="n">1</div><div class="t">{C['steps'][0][0]}</div><div class="d">{C['steps'][0][1]}</div></div>
    <div id="k1" class="abs cl"><div class="n">2</div><div class="t">{C['steps'][1][0]}</div><div class="d">{C['steps'][1][1]}</div></div>
    <div id="k2" class="abs cl"><div class="n">3</div><div class="t">{C['steps'][2][0]}</div><div class="d">{C['steps'][2][1]}</div></div>""",
    """      wIn('#hd .w', 0.04, 0.08);
      mark('#hd em', 0.6);
      ['#k0', '#k1', '#k2'].forEach((s, i) => {
        tl.fromTo(s + ' .n', { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.45, ease: 'back.out(2.2)' }, 0.44 + i * 0.5);
        tl.fromTo([s + ' .t', s + ' .d'], { opacity: 0, x: 24, filter: 'blur(8px)' }, { opacity: 1, x: 0, filter: 'blur(0px)', duration: 0.6, ease: 'expo.out', stagger: 0.1 }, 0.5 + i * 0.5);
      });
      tl.to('#k2 .n', { backgroundColor: '#d7ff00', color: '#192219', duration: 0.3 }, 2.44);
      tl.to('#root > *', { opacity: 0, filter: 'blur(8px)', duration: 0.24, ease: 'power2.in' }, 3.78);""")

wheel("wheel6", 62.06, 4, 5)

# ---------- 64.06 One More Thing (music ducked) ----------
add("one", 64.06, 2.04, "light", """
    #big { left: 0; top: 400px; width: 1920px; text-align: center; font-family: 'Bricolage', sans-serif; font-weight: 800; font-size: 240px; line-height: 280px; letter-spacing: -0.04em; }
    #fin { top: 480px; font-size: 110px; }
    #fin .g { color: #9aa08a; }""",
    """    <div id="big" class="abs">One</div>
    <div id="fin" class="abs st"><span class="w">One</span><span class="w">More</span><span class="w g">Thing</span></div>""",
    """      tl.fromTo('#big', { opacity: 0, x: -140, filter: 'blur(26px)' }, { opacity: 1, x: 0, filter: 'blur(0px)', duration: 0.55, ease: 'expo.out' }, 0.02);
      tl.to('#big', { scale: 0.45, opacity: 0, duration: 0.28, ease: 'power3.in' }, 0.74);
      wIn('#fin .w', 0.8, 0.12);
      wOut('#fin .w', 1.84);""")

# ---------- 66.06 one more thing: the pill floods the accent and becomes refer_to, a number or word lands, mascots float in ----------
# refer_number: a number counts up 0 -> N with refer_unit after it (default %); text is shown as it is
REFER_COUNT = isinstance(C["refer_number"], (int, float))
REFER_TXT = f"{C['refer_number']}{C.get('refer_unit', '%')}" if REFER_COUNT else C["refer_number"]
add("refer", 66.06, 6.04, "light", """
    #pl { left: 760px; top: 300px; width: 400px; height: 96px; border-radius: 48px; background: #fffdf3; border: 4px solid #192219; }
    #pt1, #pt2 { left: 0; top: 0; width: 392px; height: 88px; text-align: center; line-height: 88px; font-family: 'Bricolage', sans-serif; font-weight: 700; font-size: 44px; letter-spacing: -0.02em; }
    #dot { left: 948px; top: 440px; width: 24px; height: 24px; border-radius: 12px; background: #cbcdb9; }
    #pc { left: 0; top: 430px; width: 1920px; text-align: center; font-family: 'Bricolage', sans-serif; font-weight: 800; font-size: 220px; line-height: 240px; letter-spacing: -0.04em; }
    #pd { left: 0; top: 690px; width: 1920px; text-align: center; }
    #gm { top: 100px; font-size: 72px; }
    .fb { position: absolute; width: 230px; height: 230px; }
    .ft { position: absolute; width: 130px; height: 130px; }""",
    f"""    <div id="gm" class="abs st">{words(C['refer_line'])}</div>
    <img id="b1" class="fb" style="left:150px;top:300px" src="{IMG['mascot']['src']}" alt="{IMG['mascot']['alt']}" />
    <img id="b2" class="fb" style="left:1540px;top:250px" src="{IMG['mascot']['src']}" alt="{IMG['mascot']['alt']}" />
    <img id="b3" class="fb" style="left:260px;top:720px" src="{IMG['mascot']['src']}" alt="{IMG['mascot']['alt']}" />
    <img id="b4" class="fb" style="left:1450px;top:700px" src="{IMG['mascot']['src']}" alt="{IMG['mascot']['alt']}" />
    <div id="t1" class="ft tile" style="left:560px;top:820px"><img src="{LOGO}" alt="{B['logo_alt']}" /></div>
    <div id="t2" class="ft tile" style="left:1230px;top:840px"><img src="{LOGO}" alt="{B['logo_alt']}" /></div>
    <div id="pl" class="abs"><div id="pt1" class="abs">{C['refer_from']}</div><div id="pt2" class="abs">{C['refer_to']}</div></div>
    <div id="dot" class="abs"></div>
    <div id="pc" class="abs">{REFER_TXT}</div>
    <div id="pd" class="abs sub">{C['refer_sub']}</div>""",
    """      tl.set(['#pt2', '#pc', '#pd'], { opacity: 0 }, 0);
      tl.fromTo('#pl', { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.6, ease: 'back.out(1.8)' }, 0.05);
      tl.fromTo('#dot', { opacity: 0, scale: 0 }, { opacity: 1, scale: 1, duration: 0.4, ease: 'back.out(2)' }, 0.9);
      // 68.06: the pill turns accent, the dot becomes the number, mascots drift in
      tl.to('#dot', { scale: 0, opacity: 0, duration: 0.3, ease: 'power3.in' }, 1.7);
      tl.to('#pl', { backgroundColor: '#d7ff00', scale: 1.15, duration: 0.5, ease: 'expo.inOut' }, 1.9);
      tl.to('#pt1', { opacity: 0, filter: 'blur(6px)', duration: 0.2 }, 1.95);
      tl.fromTo('#pt2', { opacity: 0, filter: 'blur(6px)' }, { opacity: 1, filter: 'blur(0px)', duration: 0.35 }, 2.1);
      tl.fromTo('#pc', { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.6, ease: 'back.out(1.8)' }, 2.0);
""" + ("""      const n = { v: 0 };
      tl.to(n, { v: REFER_N, duration: 0.8, ease: 'power2.out', onUpdate: () => { document.querySelector('[data-composition-id="refer"] #pc').textContent = Math.round(n.v) + 'REFER_U'; } }, 2.0);
""" if REFER_COUNT else "") + """      tl.fromTo('#pd', { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: 'expo.out' }, 2.6);
      ['#b1', '#b2', '#b3', '#b4', '#t1', '#t2'].forEach((s, i) => {
        tl.fromTo(s, { opacity: 0, scale: 0.3, rotation: (i % 2 ? 16 : -16) }, { opacity: 1, scale: 1, rotation: (i % 2 ? 5 : -5), duration: 0.7, ease: 'back.out(1.6)' }, 2.1 + i * 0.08);
        tl.to(s, { y: (i % 2 ? -18 : 18), rotation: (i % 2 ? -3 : 3), duration: 3.2, ease: 'sine.inOut' }, 2.8);
      });
      wIn('#gm .w', 3.0, 0.08);
      mark('#gm em', 3.6);
      tl.to('#root > *', { opacity: 0, filter: 'blur(8px)', duration: 0.25, ease: 'power2.in' }, 5.78);""")

# ---------- 72.06 a detail panel over the illustration, panned ----------
add("invite", 72.06, 4.04, "light", """
    #fv { left: 0; top: 0; width: 1920px; height: 1080px; overflow: hidden; }
    #fv img { position: absolute; left: -2400px; top: -380px; width: 4344px; height: 1448px; }
    #pn { left: 80px; top: 70px; width: 1160px; height: 360px; border-radius: 28px; background: #fffdf3; border: 2px solid #cbcdb9; box-shadow: 0 30px 70px -30px rgba(25,34,25,.35); }
    #tx { left: 130px; top: 110px; }
    #sb { left: 130px; top: 320px; width: 1060px; }""",
    f"""    <div id="fv" class="abs"><img id="fi" src="{IMG['illustration']['src']}" alt="{IMG['illustration']['alt']}" /></div>
    <div id="pn" class="abs"></div>
    <div id="tx" class="abs hl"><div>{words(C['invite_1'])}</div><div>{words(C['invite_2'])}</div></div>
    <div id="sb" class="abs sub">{C['invite_sub']}</div>""",
    """      tl.fromTo('#fi', { x: 0, scale: 1 }, { x: 260, scale: 1.04, duration: 4.0, ease: 'none' }, 0);
      tl.fromTo('#fv', { opacity: 0 }, { opacity: 1, duration: 0.25 }, 0);
      tl.fromTo('#pn', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: 'expo.out' }, 0.1);
      wIn('#tx .w', 0.2, 0.07);
      mark('#tx em', 1.2);
      tl.fromTo('#sb', { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.5, ease: 'expo.out' }, 1.3);
      tl.to('#root > *', { opacity: 0, filter: 'blur(8px)', duration: 0.24, ease: 'power2.in' }, 3.78);""")

# ---------- 76.06 trust: the site's FAQ headings ----------
add("trust", 76.06, 4.04, "light", """
    #hd { left: 120px; top: 260px; width: 700px; }
    .rw { left: 900px; width: 900px; height: 130px; border-top: 3px solid #cbcdb9; display: flex; align-items: center; justify-content: space-between;
      font-family: 'Bricolage', sans-serif; font-weight: 700; font-size: 40px; letter-spacing: -0.02em; }
    .rw b { font-family: 'DM Sans', sans-serif; font-weight: 500; font-size: 44px; color: #626854; }
    #q0 { top: 300px; } #q1 { top: 430px; } #q2 { top: 560px; } #q3 { top: 690px; height: 0; }
    #br { left: 300px; top: 640px; width: 260px; height: 260px; }""",
    f"""    <div id="hd" class="abs hl"><div>{words(C['trust_1'])}</div><div>{words(C['trust_2'])}</div></div>
    <div id="q0" class="abs rw">{C['trust_rows'][0]}<b>+</b></div>
    <div id="q1" class="abs rw">{C['trust_rows'][1]}<b>+</b></div>
    <div id="q2" class="abs rw">{C['trust_rows'][2]}<b>+</b></div>
    <div id="q3" class="abs rw"></div>
    <img id="br" class="abs" src="{IMG['mascot']['src']}" alt="{IMG['mascot']['alt']}" />""",
    """      wIn('#hd .w', 0.04, 0.08);
      mark('#hd em', 0.8);
      ['#q0', '#q1', '#q2', '#q3'].forEach((s, i) => tl.fromTo(s, { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.55, ease: 'expo.out' }, 0.44 + i * 0.5));
      tl.fromTo('#br', { opacity: 0, scale: 0.6, rotation: 10 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.7, ease: 'back.out(1.7)' }, 1.0);
      tl.to('#root > *', { opacity: 0, filter: 'blur(8px)', duration: 0.24, ease: 'power2.in' }, 3.78);""")

# ---------- 80.06 the site's closing line, hand-drawn circle ----------
add("keep", 80.06, 4.04, "film", """
    #k1 { top: 400px; } #k2 { top: 510px; }
    .cw { position: relative; display: inline-block; }
    .cw svg { position: absolute; left: -40px; top: -22px; width: calc(100% + 80px); height: calc(100% + 44px); overflow: visible; }""",
    video("keep", 4.04) + f"""
    <div id="k1" class="abs st">{words(C['keep_1'])}</div>
    <div id="k2" class="abs st"><span class="w">{C['keep_2_lead']}</span><span class="w cw">{C['keep_2_circled']}<svg viewBox="0 0 100 40" preserveAspectRatio="none"><path id="cc" d="M50 3 C80 2 98 9 97 20 C96 32 75 38 49 37 C22 37 3 31 3 20 C3 9 22 3 54 4" fill="none" stroke="#d7ff00" stroke-width="4" stroke-linecap="round" vector-effect="non-scaling-stroke" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg></span></div>""",
    """      tl.fromTo('#v', { scale: 1.0 }, { scale: 1.08, duration: 4.04, ease: 'none' }, 0);
      wIn('#k1 .w', 0.04, 0.12);
      wIn('#k2 .w', 0.6, 0.12);
      tl.to('#cc', { strokeDashoffset: 0, duration: 0.6, ease: 'power2.inOut' }, 1.44);
      wOut(['#k1 .w', '#k2 .w'], 3.8);""")

# ---------- 84.06 end on the ground colour: dot -> logo -> lockup (+ optional disclaimer) ----------
URL_W = max(400, len(B['url']) * 27 + 90)  # the URL pill grows with the domain
add("end", 84.06, 5.94, "dark", """
    #dt { left: 948px; top: 418px; width: 24px; height: 24px; border-radius: 12px; background: #d7ff00; }
    #lk { left: 0; top: 360px; width: 1920px; height: 140px; display: flex; justify-content: center; align-items: center; gap: 30px; }
    #lk .tile { width: 132px; height: 132px; }
    #lk span { font-family: 'Bricolage', sans-serif; font-weight: 700; font-size: 100px; letter-spacing: -0.03em; }
    #tg { top: 560px; font-size: 60px; }
    #dc { top: 960px; left: 0; width: 1920px; text-align: center; color: #ece7d2; }
    #url { left: """ + str(960 - URL_W // 2) + """px; top: 720px; width: """ + str(URL_W) + """px; height: 96px; border-radius: 48px; background: #d7ff00; color: #192219; text-align: center;
      line-height: 96px; font-family: 'Bricolage', sans-serif; font-weight: 700; font-size: 48px; letter-spacing: -0.02em; }""",
    f"""    <div id="dt" class="abs"></div>
    <div id="lk" class="abs"><div id="cm" class="tile"><img src="{LOGO}" alt="{B['logo_alt']}" /></div><span id="nm">{B['name']}</span></div>
    <div id="tg" class="abs st">{words(C['end_tagline'])}</div>
    <div id="url" class="abs">{B['url']}</div>""" + (f"""
    <div id="dc" class="abs lab">{C['disclaimer']}</div>""" if C.get('disclaimer') else ""),
    """      tl.set(['#cm', '#nm'], { opacity: 0 }, 0);
      tl.fromTo('#dt', { scale: 0 }, { scale: 1, duration: 0.35, ease: 'back.out(2.5)' }, 0.05);
      tl.to('#dt', { scale: 6, opacity: 0, duration: 0.4, ease: 'power3.in' }, 0.55);
      tl.fromTo('#cm', { opacity: 0, scale: 0.4, rotation: -14 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.8, ease: 'back.out(1.6)' }, 0.75);
      tl.fromTo('#nm', { opacity: 0, x: -30, filter: 'blur(10px)' }, { opacity: 1, x: 0, filter: 'blur(0px)', duration: 0.7, ease: 'expo.out' }, 1.1);
      wIn('#tg .w', 1.6, 0.07);
      tl.fromTo('#url', { opacity: 0, y: 24, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: 'back.out(1.8)' }, 2.3);""" + ("""
      tl.fromTo('#dc', { opacity: 0 }, { opacity: 1, duration: 0.4 }, 2.6);""" if C.get('disclaimer') else ""))

# ---------- index ----------
hosts = []
for z, (cid, start, dur) in enumerate(SCENES, 1):
    hosts.append(f'      <div id="{cid}" class="clip" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html"\n'
                 f'        data-start="{start}" data-duration="{dur}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:{z}"></div>')

SFX = [  # (id, file, start, dur, track, volume)
    *[(f"sx-m{i}", "key-press.mp3", round(32.06 + t, 2), 0.3, 8, 0.35) for i, t in enumerate([0.5, 1.0, 1.5, 2.0, 2.25, 2.5, 2.75])],
    ("sx-slam", "click-soft.mp3", 35.06, 0.36, 5, 0.8),
    ("sx-cut1", "key-press.mp3", 13.5, 0.3, 8, 0.35),
    ("sx-cut2", "key-press.mp3", 14.0, 0.3, 8, 0.35),
    *[(f"sx-wh{i}", "key-press.mp3", t + 0.36, 0.3, 6, 0.45) for i, t in enumerate([6.06, 24.06, 36.06, 44.06, 52.06, 62.06])],
    ("sx-app", "whoosh-short.mp3", 18.3, 0.57, 4, 0.25),
    ("sx-print", "printer.mp3", 38.8, 0.8, 7, 0.3),
    ("sx-lock", "click-soft.mp3", 40.55, 0.36, 5, 0.8),
    ("sx-one", "whoosh-short.mp3", 64.02, 0.57, 4, 0.35),
    ("sx-morph", "whoosh.mp3", 67.95, 0.57, 4, 0.3),
    ("sx-end", "impact-bass-1.mp3", 84.06, 2.0, 3, 0.35),
]
audio = [f'      <audio id="music" src="{FILM["music"]}" data-start="0" data-duration="90" data-track-index="2" data-volume="0.8"></audio>']
for sid, f, s, d, tr, v in SFX:
    audio.append(f'      <audio id="{sid}" src="assets/sfx/{f}" data-start="{s}" data-duration="{d}" data-track-index="{tr}" data-volume="{v}"></audio>')

(ROOT / "index.html").write_text(recolour(f"""<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #f7f4e5; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <!-- generated by tools/build.py; 120 BPM, scenes cut on 0.06 + 2k s -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="90" data-width="1920" data-height="1080">
{chr(10).join(hosts)}

{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""))
print(len(SCENES), "scenes")
