# -*- coding: utf-8 -*-
"""（1回だけ使った）本家とゲキムズのデータから台帳を作る。

  python3 tools/ledger/export.py data-0.3.18.json data-hard-0.3.12.json

ゲキムズの種・節目をそのまま台帳にし、本家にもあるものに "main" を付ける。本家の種・節目は、同じ id か、
無ければ学名（節目は学名と階級）で台帳のものに対応させる。本家とゲキムズで値が違う欄は "main" に本家の値を残す。
"""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ledger

M = json.load(open(sys.argv[1], encoding="utf-8")); H = json.load(open(sys.argv[2], encoding="utf-8"))
HC = {c["id"]: c for c in H["clades"]}; HS = {s["id"]: s for s in H["species"]}
bysci = collections.defaultdict(list)
for s in H["species"]: bysci[s["sci"]].append(s["id"])
bysr = {(c["sci"], c["rank"]): c["id"] for c in H["clades"]}
bys = collections.defaultdict(list)
for c in H["clades"]: bys[c["sci"]].append(c["id"])

def over(m, h):
    o = {}
    for k in m.keys() | h.keys():
        if k in ("id", "parent"): continue
        if m.get(k) != h.get(k): o[k] = m.get(k)
    return o

used = set()
for n, c in enumerate(M["clades"]):
    i = c["id"] if c["id"] in HC else bysr.get((c["sci"], c["rank"])) or (bys[c["sci"]][0] if len(bys[c["sci"]]) == 1 else None)
    assert i and i not in used, c; used.add(i)
    m = {"order": n}
    if i != c["id"]: m["id"] = c["id"]
    m.update(over(c, HC[i])); HC[i]["main"] = m
used = set()
for n, s in enumerate(M["species"]):
    i = s["id"] if s["id"] in HS else bysci[s["sci"]][0]
    assert i and i not in used, s; used.add(i)
    m = {"order": n}
    if i != s["id"]: m["id"] = s["id"]
    m.update(over(s, HS[i])); HS[i]["main"] = m
L = {"species": H["species"], "clades": H["clades"],
     "meta-main": {k: v for k, v in M["meta"].items() if k not in ("datasetVersion", "next")},
     "meta-hard": {k: v for k, v in H["meta"].items() if k not in ("datasetVersion", "next")}}
bad = ledger.check(L)
print("\n".join(bad) or "台帳の確認：問題なし")
ledger.save(L)
print("種", len(L["species"]), "節目", len(L["clades"]), "本家の種", sum("main" in s for s in L["species"]), "本家の節目", sum("main" in c for c in L["clades"]))
