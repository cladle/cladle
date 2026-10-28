# -*- coding: utf-8 -*-
"""昆虫編のデータ（data-insect.json）を、ゲキムズのデータから切り出して作る。

  python3 tools/insect/make_insect.py data-hard.json data-insect.json

- 昆虫綱の種をすべて残す。根は昆虫綱。目・科の並びは Catalogue of Life、和名は環境省（1997）種の多様性調査の
  対象種一覧ほか（ゲキムズ側の tools/hard/insect_taxa.json）。種はゲキムズに今ある昆虫のまま（作者の判断）。
- 全種を答えに出し、知名度や目ごとの重みは付けずに全種から同じ確率で選ぶ（魚編と同じ）。
- 種・節目・知名度を変えたら版番号（INSECT_VERSION）を上げる。今日の動物の選び方に入っている。
"""
import json, sys

INSECT_VERSION = "insect-0.1.0"
src, out = sys.argv[1], sys.argv[2]
H = json.load(open(src, encoding="utf-8"))
C = {c["id"]: c for c in H["clades"]}

def anc(p):
    while p:
        yield C[p]; p = C[p]["parent"]

species, used = [], set()
for s in H["species"]:
    if "Insecta" not in {c["sci"] for c in anc(s["parent"])}: continue
    species.append(dict(s))
    used |= {c["id"] for c in anc(s["parent"])}
root = next(c["id"] for c in H["clades"] if c["sci"] == "Insecta")
above = {x["id"] for x in anc(C[root]["parent"])}
clades = []
for c in H["clades"]:
    if c["id"] not in used or c["id"] in above: continue
    c = dict(c)
    if c["id"] == root: c["parent"] = None
    clades.append(c)

meta = {k: H["meta"][k] for k in ("schemaVersion", "referenceDate") if k in H["meta"]}
meta.update({
    "datasetVersion": INSECT_VERSION,
    "title": "Cladle 昆虫編",
    "taxonomy": {
        "backbone": "目より上は分子系統の論文に基づく主な節目だけを置き、分かれる順が定まらないところは多分岐にした。",
        "nomenclature": "Catalogue of Life Checklist（ChecklistBank 3LR）",
        "phylogenyNotes": "目・科の並びは Catalogue of Life に従い、目より上は Misof et al. 2014（Science 346: 763–767）の系統で、ふつうモード・ゲキムズにあるまとまり（有翅昆虫・新翅類・多新翅類・準新翅類・完全変態類など）だけを節目にした。",
    },
    "japaneseNameSources": [x for x in H["meta"]["japaneseNameSources"] if x.startswith(("環境省", "昆虫の目・科", "GBIF", "Catalogue of Life", "World Register", "コガネムシ上科"))],
    "status": "試作版。ゲキムズのデータ（" + H["meta"]["datasetVersion"] + "）から昆虫だけを切り出した。",
    "counts": {"species": len(species)},
    "selection": {
        "maxGuesses": 20, "dailyEpoch": "2026-10-28",
        # 枠を一つ（昆虫綱）にして、重みを付けずに全種から一様に選ぶ
        "bucketRank": "綱", "tierWeights": {"1": 1, "2": 1, "3": 1, "4": 1},
    },
})
json.dump({"meta": meta, "clades": clades, "species": species}, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(f"{out}: 節目 {len(clades)}・種 {len(species)}")
