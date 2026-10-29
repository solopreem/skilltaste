"""Check that every entry follows spec/ENTRY.md. Exit 1 on any problem. Entries live in <category>/<id>/. Usage: python3 tools/validate.py [entry-id ...]"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = ["SKILL.md", "taste.json", "references/floor.md", "references/RECIPE.md", "references/SWAP.md", "references/REFERENCE.md",
         "scripts/analyze.py", "scripts/events.py", "result/result.mp4", "result/poster.jpg",
         "result/sheet.jpg", "result/preview.gif", "result/metrics.json", "project/film.json", "project/tools/build.py", "project/index.html"]
LAYERS = ["floor", "category", "method", "moves", "craft", "style", "tool"]
KEYS = ["id", "title", "summary", "version", "requires", "layers", "spec", "reference", "result", "needs", "fits", "avoid", "licence"]
METRICS = ["duration", "shots", "events_per_10s", "still_share", "lufs", "true_peak_dbfs"]

problems = []
ENTRIES = {p.parent.name: p.parent for p in sorted(ROOT.glob("*/*/taste.json"))}  # <category>/<id>/
ids = sys.argv[1:] or list(ENTRIES)
for eid in ids:
    e = ENTRIES.get(eid, ROOT / eid)
    bad = lambda m: problems.append(f"{eid}: {m}")
    for f in FILES:
        if not (e / f).exists():
            bad(f"missing {f}")
    try:
        t = json.loads((e / "taste.json").read_text())
    except Exception as x:
        bad(f"taste.json unreadable ({x})"); continue
    for k in KEYS:
        if k not in t:
            bad(f"taste.json has no '{k}'")
    # shared files are copied into every entry (each entry must install on its own); the copies must match tools/
    for shared, copy in [("tools/floor.md", "references/floor.md"), ("tools/analyze.py", "scripts/analyze.py"),
                         ("tools/events.py", "scripts/events.py"), ("tools/setup.sh", "scripts/setup.sh")]:
        if (e / copy).exists() and (e / copy).read_bytes() != (ROOT / shared).read_bytes():
            bad(f"{copy} differs from {shared}: copy it again")
    # category files (<category>/*.md, e.g. launch/sourcing.md) hold rules for that category only; every entry in it carries a copy
    for shared in sorted(e.parent.glob("*.md")):
        copy = e / "references" / shared.name
        if not copy.exists():
            bad(f"missing references/{shared.name} (copy of {shared.relative_to(ROOT)})")
        elif copy.read_bytes() != shared.read_bytes():
            bad(f"references/{shared.name} differs from {shared.relative_to(ROOT)}: copy it again")
    if t.get("layers", {}).get("category") != e.parent.name:
        bad(f"taste.json layers.category '{t.get('layers', {}).get('category')}' != category folder '{e.parent.name}'")
    if t.get("id") != eid:
        bad(f"taste.json id '{t.get('id')}' != folder name")
    for k in LAYERS:
        if k not in t.get("layers", {}):
            bad(f"taste.json layers has no '{k}'")
    skill = (e / "SKILL.md").read_text() if (e / "SKILL.md").exists() else ""
    if not skill.startswith("---\nname: " + eid + "\n"):
        bad("SKILL.md frontmatter must start with 'name: <id>'")
    if (e / "result/metrics.json").exists():
        m = json.loads((e / "result/metrics.json").read_text())
        for k in METRICS:
            if k not in m:
                bad(f"metrics.json has no '{k}'")
        if m.get("true_peak_dbfs", 0) > -1:
            bad(f"true peak {m.get('true_peak_dbfs')} dBTP is above -1")
    if (e / "project/film.json").exists():
        film = (e / "project/film.json").read_text()
        for ref in json.loads(film).get("images", {}).values():
            src = ref.get("src", "") if isinstance(ref, dict) else ""
            if src and not ((e / "project" / src).exists() or (e / "project/assets/img" / src).exists()):
                bad(f"film.json image not found: {src}")

print("\n".join(problems) or f"ok: {len(ids)} entr{'y' if len(ids) == 1 else 'ies'}")
sys.exit(1 if problems else 0)
