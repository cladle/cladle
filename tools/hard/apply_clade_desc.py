"""clade_desc.tsv の説明を、出来上がった data-*.json の節目に書き込む。

学名と階級が同じで、説明がまだ空の節目だけに入れる（本家と同じ節目の説明は上書きしない）。
文だけの直しなので版は上げない。ゲキムズ・魚編・鳥編・昆虫編の今の版と予約中の版に使う。

  python3 tools/hard/apply_clade_desc.py data-hard.json data-hard-0.3.9.json data-fish.json ...
"""
import csv, json, os, sys

TSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clade_desc.tsv")
D = {(r["sci"], r["rank"]): r["desc"] for r in csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t")}

for f in sys.argv[1:]:
    data = json.load(open(f, encoding="utf-8"))
    n = 0
    for c in data["clades"]:
        d = D.get((c["sci"], c["rank"]))
        if d and not c.get("desc"):
            c["desc"] = d; n += 1
        elif d and c["desc"] != d:
            print(f"{f}: {c['sci']} は説明が既にあるので変えない", file=sys.stderr)
    json.dump(data, open(f, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"{f}: {n} 個の節目に説明を入れた")
