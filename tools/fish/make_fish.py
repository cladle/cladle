# -*- coding: utf-8 -*-
"""魚編のデータ（data-fish.json）を、ゲキムズのデータから切り出して作る。

  python3 tools/fish/make_fish.py data-hard.json data-fish.json

- 脊椎動物のうち四肢動物を除いた種（円口類・軟骨魚類・条鰭類・シーラカンス・ハイギョ）を残す。
  「魚類」は側系統群なので節目にはせず、出題の範囲として使うだけにする。根は脊椎動物亜門。
- 全種を答えに出す。目は種数の平方根に比例した確率で選び（種数の多い目ばかり出ないように、作者の判断）、目の中は全種から同じ確率で選ぶ。
  日本の魚は全種が入っているので、種数は収録数（tools/real_counts.py の fish）。目の無いシーラカンス・ハイギョは肉鰭類で一つの群にする。
- ふだんは tools/build_all.py から動かす。そのときの版番号は data-*.json の予約で決まる（FISH_VERSION は単独で動かしたとき用）。
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import real_counts

FISH_VERSION = "fish-0.1.3"
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
        "tierWeights": {"1": 1, "2": 1, "3": 1, "4": 1}, "hintAfter": [7, 11],
    },
})
json.dump(real_counts.apply({"meta": meta, "clades": clades, "species": species}, "fish", "sqrt"), open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(f"{out}: 節目 {len(clades)}・種 {len(species)}")
