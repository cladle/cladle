# -*- coding: utf-8 -*-
"""鳥編のデータ（data-bird.json）を、ゲキムズのデータから切り出して作る。

  python3 tools/bird/make_bird.py data-hard.json data-bird.json

- 鳥綱の種をすべて残す。根は鳥綱。目・科・属の並びと和名は日本鳥類目録改訂第8版に合わせてある
  （ゲキムズ側の tools/archive/hard/bird_taxa.json）。外国の鳥も和名があれば入れる（作者の判断）。
- 全種を答えに出す。目は実際の種数（tools/real_counts.json）の平方根に比例した確率で選び、目の中は全種から同じ確率で選ぶ
  （収録数に左右されず、種数の多い目ばかりにもならないように。目を足したら tools/real_counts.py を動かす）。
- ふだんは tools/build_all.py から動かす。そのときの版番号は data-*.json の予約で決まる（BIRD_VERSION は単独で動かしたとき用）。
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import real_counts

BIRD_VERSION = "bird-0.1.4"
src, out = sys.argv[1], sys.argv[2]
H = json.load(open(src, encoding="utf-8"))
C = {c["id"]: c for c in H["clades"]}

def anc(p):
    while p:
        yield C[p]; p = C[p]["parent"]

species, used = [], set()
for s in H["species"]:
    if "Aves" not in {c["sci"] for c in anc(s["parent"])}: continue
    species.append(dict(s))
    used |= {c["id"] for c in anc(s["parent"])}
root = next(c["id"] for c in H["clades"] if c["sci"] == "Aves")
above = {x["id"] for x in anc(C[root]["parent"])}
clades = []
for c in H["clades"]:
    if c["id"] not in used or c["id"] in above: continue
    c = dict(c)
    if c["id"] == root: c["parent"] = None
    clades.append(c)

meta = {k: H["meta"][k] for k in ("schemaVersion", "referenceDate") if k in H["meta"]}
meta.update({
    "datasetVersion": BIRD_VERSION,
    "title": "Cladle 鳥編",
    "taxonomy": {
        "backbone": H["meta"]["taxonomy"]["backbone"],
        "nomenclature": "日本鳥学会（2024）日本鳥類目録改訂第8版 掲載鳥類リスト ver.1（2024-10-08公開）",
        "phylogenyNotes": "目・科・属は日本鳥類目録改訂第8版に従い、目より上は Jarvis et al. 2014・Prum et al. 2015・Stiller et al. 2024 でそろって支持されるまとまりだけを節目にした。新鳥類の中の分岐の順は決めていない。",
    },
    "japaneseNameSources": ["日本鳥学会（2024）日本鳥類目録改訂第8版 掲載鳥類リスト ver.1（2024-10-08公開）",
                            "外国の鳥：ふつうモードと同じ照合（GBIF・Wikidata・iNaturalist）"],
    "status": "試作版。ゲキムズのデータ（" + H["meta"]["datasetVersion"] + "）から鳥だけを切り出した。",
    "counts": {"species": len(species)},
    "selection": {
        "maxGuesses": 20, "dailyEpoch": "2026-10-28",
        "tierWeights": {"1": 1, "2": 1, "3": 1, "4": 1}, "hintAfter": [7, 11],
    },
})
json.dump(real_counts.apply({"meta": meta, "clades": clades, "species": species}, "bird", "sqrt"), open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(f"{out}: 節目 {len(clades)}・種 {len(species)}")
