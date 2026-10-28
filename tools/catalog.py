"""Write catalog.json (one record per entry, from taste.json + metrics.json) and the table between the CATALOG markers in both READMEs."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rows = []
for e in sorted(p for p in (ROOT / "entries").iterdir() if (p / "taste.json").exists()):
    t = json.loads((e / "taste.json").read_text())
    m = json.loads((e / "result/metrics.json").read_text()) if (e / "result/metrics.json").exists() else {}
    rows.append({"id": t["id"], "title": t["title"], "summary": t["summary"], "category": t["layers"]["category"],
                 "method": t["layers"]["method"], "duration_s": t["spec"]["duration_s"], "ratio": t["spec"]["ratio"],
                 "events_per_10s": m.get("events_per_10s"), "still_share": m.get("still_share"), "shots": m.get("shots"),
                 "needs": t["needs"], "fits": t["fits"], "avoid": t["avoid"], "poster": f"entries/{t['id']}/result/poster.jpg",
                 "preview": f"entries/{t['id']}/result/preview.gif", "video": f"entries/{t['id']}/result/result.mp4"})
(ROOT / "catalog.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")

table = "| Preview | Entry | Category · method | Length | Events / 10 s |\n|---|---|---|---|---|\n" + "".join(
    f"| <img src=\"{r['preview']}\" width=\"240\"> | [**{r['id']}**](entries/{r['id']}/) {r['title']} | {r['category']} · {r['method']} | {r['duration_s']} s {r['ratio']} | {r['events_per_10s']} |\n"
    for r in rows)
for name in ["README.md", "README_CN.md"]:
    p = ROOT / name
    if p.exists():
        p.write_text(re.sub(r"(<!-- CATALOG -->\n).*?(<!-- /CATALOG -->)", lambda mm: mm.group(1) + table + mm.group(2), p.read_text(), flags=re.S))
print(len(rows), "entries")
