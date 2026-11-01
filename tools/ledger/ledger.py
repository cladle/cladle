# -*- coding: utf-8 -*-
"""全種の台帳（tools/ledger/）を読み、本家とゲキムズのデータを作る。魚編・鳥編・昆虫編はゲキムズから切り出す（tools/build_all.py）。

台帳のファイル（1行に1つの種・節目。JSON の形）:
  species.jsonl   ゲキムズに入る全種。並びはゲキムズの出題の並び
  clades.jsonl    全部の節目。parent が親の節目の id
  meta-main.json  本家の meta（版番号と予約は data-*.json の側で決める）
  meta-hard.json  ゲキムズの meta

本家に出す種・節目には "main" が付く:
  "main": {"order": 本家での並び, "id": 本家での id（台帳の id と違うときだけ）, ほかの欄: 本家だけの値}
  本家の木は、台帳の木から "main" の付いた節目だけを残したもの（間の節目はたたむ）。
  "main" の中の欄（tier・polytomy など）は本家だけ違う値。null はその欄を本家では消す。
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
S_KEYS = ["id", "parent", "ja", "sci", "jaStatus", "aliases", "fact", "verify", "tier", "gbif"]
C_KEYS = ["id", "parent", "ja", "sci", "rank", "desc"]

def ordered(x, keys):
    out = {k: x[k] for k in keys if k in x}
    out.update({k: v for k, v in x.items() if k not in out})
    return out

def read_jsonl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]

def write_jsonl(p, rows):
    with open(p, "w", encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")

def load(d=HERE):
    L = {"species": read_jsonl(os.path.join(d, "species.jsonl")), "clades": read_jsonl(os.path.join(d, "clades.jsonl"))}
    for k in ("main", "hard"):
        L["meta-" + k] = json.load(open(os.path.join(d, f"meta-{k}.json"), encoding="utf-8"))
    return L

def save(L, d=HERE):
    write_jsonl(os.path.join(d, "species.jsonl"), [ordered(s, S_KEYS) for s in L["species"]])
    write_jsonl(os.path.join(d, "clades.jsonl"), [ordered(c, C_KEYS) for c in L["clades"]])
    for k in ("main", "hard"):
        with open(os.path.join(d, f"meta-{k}.json"), "w", encoding="utf-8") as f:
            json.dump(L["meta-" + k], f, ensure_ascii=False, indent=1); f.write("\n")

def check(L):
    """id の重なり・親の無い節目・種の無い節目などを確かめる。問題のリストを返す"""
    bad, C = [], {}
    for c in L["clades"]:
        if c["id"] in C: bad.append("節目の id が重なっている: " + c["id"])
        C[c["id"]] = c
    roots = [c["id"] for c in L["clades"] if not c["parent"]]
    if len(roots) != 1: bad.append("根が1つでない: " + ", ".join(roots))
    for c in L["clades"]:
        if c["parent"] and c["parent"] not in C: bad.append(f"節目 {c['id']} の親 {c['parent']} が無い")
    ids, has = set(), set()
    for s in L["species"]:
        if s["id"] in ids or s["id"] in C: bad.append("種の id が重なっている: " + s["id"])
        ids.add(s["id"])
        if s["parent"] not in C: bad.append(f"種 {s['id']} の親 {s['parent']} が無い"); continue
        p = s["parent"]
        while p and p not in has: has.add(p); p = C[p]["parent"]
    empty = [c["id"] for c in L["clades"] if c["id"] not in has]
    if empty: bad.append(f"種の無い節目が {len(empty)} 個: " + ", ".join(empty[:10]))
    # 本家の木：本家の種の親をたどると本家の節目に着くか、本家の id が重ならないか
    mids = {}
    for x in L["clades"] + L["species"]:
        m = x.get("main")
        if m is None: continue
        i = m.get("id", x["id"])
        if i in mids: bad.append("本家の id が重なっている: " + i)
        mids[i] = x
    mroot = [c["id"] for c in L["clades"] if "main" in c and not main_parent(C, c["parent"])]
    if len(mroot) != 1: bad.append("本家の根が1つでない: " + ", ".join(mroot))
    # グループ名（ウニ・カニなど）を種の別名にしない（group_aliases.txt）
    G = {l.strip() for l in open(os.path.join(HERE, "group_aliases.txt"), encoding="utf-8") if l.strip() and not l.startswith("#")}
    for s in L["species"]:
        for a in s.get("aliases", []) + (s.get("main") or {}).get("aliases", []):
            if a in G: bad.append(f"種 {s['id']}（{s['ja']}）の別名「{a}」はグループ名。aliases ではなく groups に入れる")
    return bad

def main_parent(C, p):
    """台帳の節目 p から上へたどって、最初の本家の節目（の台帳の id）"""
    while p and "main" not in C[p]: p = C[p]["parent"]
    return p

def _apply_main(x, keys):
    m = dict(x.pop("main"))
    m.pop("order", None)
    x["id"] = m.pop("id", x["id"])
    for k, v in m.items():
        if v is None: x.pop(k, None)
        else: x[k] = v
    return ordered(x, keys)

def build_main(L):
    """本家の data（meta・clades・species）。版番号と meta.next は入れない"""
    C = {c["id"]: c for c in L["clades"]}
    mid = lambda i: C[i]["main"].get("id", i) if i else None
    clades = []
    for c in sorted((c for c in L["clades"] if "main" in c), key=lambda c: c["main"]["order"]):
        x = json.loads(json.dumps(c)); x["parent"] = mid(main_parent(C, c["parent"]))
        clades.append(_apply_main(x, C_KEYS))
    species = []
    for s in sorted((s for s in L["species"] if "main" in s), key=lambda s: s["main"]["order"]):
        x = json.loads(json.dumps(s)); x["parent"] = mid(main_parent(C, s["parent"]))
        species.append(_apply_main(x, S_KEYS))
    return {"meta": json.loads(json.dumps(L["meta-main"])), "clades": clades, "species": species}

def build_hard(L):
    """ゲキムズの data。出題の重み（実際の種数）は tools/real_counts.json から付け直す"""
    import sys
    sys.path.insert(0, os.path.join(HERE, ".."))
    import real_counts
    d = {"meta": json.loads(json.dumps(L["meta-hard"])),
         "clades": [ordered({k: v for k, v in c.items() if k != "main"}, C_KEYS) for c in L["clades"]],
         "species": [ordered({k: v for k, v in s.items() if k != "main"}, S_KEYS) for s in L["species"]]}
    return real_counts.apply(d, "hard", "sqrt")
