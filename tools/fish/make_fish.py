# -*- coding: utf-8 -*-
"""魚編のデータ（data-fish.json）を、ゲキムズのデータから切り出して作る。

  python3 tools/fish/make_fish.py data-hard.json data-fish.json

- 脊椎動物のうち四肢動物を除いた種（円口類・軟骨魚類・条鰭類・シーラカンス・ハイギョ）を残す。
  「魚類」は側系統群なので節目にはせず、出題の範囲として使うだけにする。根は脊椎動物亜門。
- 全種を答えに出し、知名度や目ごとの重みは付けずに全種から同じ確率で選ぶ（作者の判断）。
- 種・節目・知名度を変えたら版番号（FISH_VERSION）を上げる。今日の動物の選び方に入っている。
"""
import json, sys

FISH_VERSION = "fish-0.1.0"
src, out = sys.argv[1], sys.argv[2]
H = json.load(open(src, encoding="utf-8"))
C = {c["id"]: c for c in H["clades"]}

def anc(p):
    while p:
        yield C[p]; p = C[p]["parent"]

def is_fish(s):
    sc = {c["sci"] for c in anc(s["parent"])}
    return "Vertebrata" in sc and "Tetrapoda" not in sc

species, used = [], set()
for s in H["species"]:
    if not is_fish(s): continue
    s = dict(s)
    species.append(s)
    used |= {c["id"] for c in anc(s["parent"])}
root = next(c["id"] for c in H["clades"] if c["sci"] == "Vertebrata")
clades = []
for c in H["clades"]:
    if c["id"] not in used or c["id"] in {x["id"] for x in anc(C[root]["parent"])}: continue
    c = dict(c)
    if c["id"] == root: c["parent"] = None
    clades.append(c)

meta = {k: H["meta"][k] for k in ("schemaVersion", "referenceDate") if k in H["meta"]}
meta.update({
    "datasetVersion": FISH_VERSION,
    "title": "Cladle 魚編",
    "taxonomy": {
        "backbone": H["meta"]["taxonomy"]["backbone"],
        "nomenclature": "本村浩之（2026）日本産魚類全種目録 Online ver. 42（2026-08-27）",
        "phylogenyNotes": "「魚類」は側系統群なので節目にせず、脊椎動物から四肢動物を除いた種を出題の範囲にした。属は学名の属名（和名の属名は付けていない）。",
        "nonMonophyleticGroupsExcluded": ["魚類"],
    },
    "japaneseNameSources": ["本村浩之（2026）日本産魚類全種目録 Online ver. 42"],
    "status": "試作版。ゲキムズのデータ（" + H["meta"]["datasetVersion"] + "）から魚だけを切り出した。",
    "counts": {"species": len(species)},
    "selection": {
        "maxGuesses": 20, "dailyEpoch": "2026-10-28",
        # 枠を一つ（脊椎動物亜門）にして、重みを付けずに全種から一様に選ぶ
        "bucketRank": "亜門", "tierWeights": {"1": 1, "2": 1, "3": 1, "4": 1},
    },
})
json.dump({"meta": meta, "clades": clades, "species": species}, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(f"{out}: 節目 {len(clades)}・種 {len(species)}")
