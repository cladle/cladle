# -*- coding: utf-8 -*-
"""鳥編のデータ（data-bird.json）を、ゲキムズのデータから切り出して作る。

  python3 tools/bird/make_bird.py data-hard.json data-bird.json

- 鳥綱の種をすべて残す。根は鳥綱。目・科・属の並びと和名は日本鳥類目録改訂第8版に合わせてある
  （ゲキムズ側の tools/hard/bird_taxa.json）。外国の鳥も和名があれば入れる（作者の判断）。
- 全種を答えに出し、知名度や目ごとの重みは付けずに全種から同じ確率で選ぶ（魚編と同じ）。
- 種・節目・知名度を変えたら版番号（BIRD_VERSION）を上げる。今日の動物の選び方に入っている。
"""
import json, sys

BIRD_VERSION = "bird-0.1.1"
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
        # 枠を一つ（鳥綱）にして、重みを付けずに全種から一様に選ぶ
        "bucketRank": "綱", "tierWeights": {"1": 1, "2": 1, "3": 1, "4": 1},
    },
})
json.dump({"meta": meta, "clades": clades, "species": species}, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(f"{out}: 節目 {len(clades)}・種 {len(species)}")
