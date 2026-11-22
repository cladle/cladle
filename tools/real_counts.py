# -*- coding: utf-8 -*-
"""出題の重みに使う「実際の種数」（現生の記載種数）を Catalogue of Life から数えて、real_counts.json に控える。

  python3 tools/real_counts.py            足りない分類群だけ問い合わせる（控えにあるものは問い合わせない）
  python3 tools/real_counts.py --refresh  控えを全部問い合わせ直す（Catalogue of Life の版を上げるとき）

なぜ要るか：収録している種は、使った名前のリストの都合で群ごとに多い・少ないがある（日本の鳥の目録はチドリ目が多い、
海の無脊椎のリストは軟体動物が多い、など）。収録数のまま出題すると、その都合がそのまま出題の偏りになる。
そこで群（ゲキムズは門と綱、鳥編・昆虫編は目）を選ぶ確率は実際の種数で決め、群の中の種は知名度の重みで選ぶ。

- 数える群は、下の MODES に書いた階級の節目すべて（データのファイルから拾う）。
- 種数は Catalogue of Life のチェックリスト（版は COL_KEY）の、その分類群の現生の種数（speciesExtantCount）。
- ゲームの節目と Catalogue of Life で名前や範囲が違う群は ALIAS に、足し合わせる Catalogue of Life の分類群を書く。
- 群を足したとき（新しい目の種を入れたときなど）は、これを動かしてから各モードのデータを作り直す。
  tools/check.py が、数の無い群があれば知らせる。
"""
import json, os, sys, time, urllib.parse, urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "tools", "real_counts.json")
API = "https://api.checklistbank.org"
COL_KEY = 316595  # Catalogue of Life Checklist 版 2026-10-14（COL26.10）
SOURCE = ("Bánki, O. et al. (2026) Catalogue of Life (Version 2026-10-14). Catalogue of Life Foundation, Amsterdam. "
          "https://doi.org/10.48580/dgzh4（CC BY 4.0）。分類群ごとの現生の記載種数（speciesExtantCount）")
# モードごとに、確率を割り振る群の階級。上から順に、外側の群・その中の群
MODES = {
    "hard": {"file": "data-hard.json", "ranks": ["門", "綱"]},
    "bird": {"file": "data-bird.json", "ranks": ["目"]},
    "insect": {"file": "data-insect.json", "ranks": ["目"]},
    # 魚編は日本産魚類全種目録の全種が入っているので、収録数がそのまま日本の種数。問い合わせずにデータから数える。
    # シーラカンス・ハイギョは肉鰭類（groups）で一つの群にする（シーラカンス目・ケラトドゥス目の下でも）
    "fish": {"file": "data-fish.json", "ranks": ["目"], "self": True, "groups": ["Sarcopterygii"]},
}
FISH_SOURCE = "本村浩之（2026）日本産魚類全種目録 Online ver. 42 に載る種（魚編は全種を収録しているので、収録数を種数とした）"
# ゲームの節目の学名 → Catalogue of Life で足し合わせる分類群（学名, 階級）。理由も書く
ALIAS = {
    # ゲームでは鉤頭動物を輪形動物の中に置く（Sielaff et al. 2016 ほか）。Catalogue of Life では別の門
    "Rotifera": [["Rotifera", "phylum"], ["Acanthocephala", "phylum"]],
    # ゲームでは単生類の2亜綱を綱として置く（ふつうモードに合わせた）。Catalogue of Life では単生綱 Monogenea の亜綱
    "Monopisthocotyla": [["Monopisthocotylea", "subclass"]],
    "Polyopisthocotyla": [["Polyopisthocotylea", "subclass"]],
}
# 鳥の目は、ゲームの目（日本鳥類目録改訂第8版＋世界の44目）に合わせて、Catalogue of Life ではなく
# 国立科学博物館 特別展「鳥」（2024）図録の図「鳥の目の種数」（文：西海功）の数を使う（tools/archive/hard/bird_extra.py の BOOK と同じ）
BOOK_SOURCE = "国立科学博物館（2024）特別展「鳥 〜ゲノム解析が解き明かす新しい鳥類の系統〜」図録、図「鳥の目の種数」（文：西海功）"

def bird_book():
    import ast
    src = open(os.path.join(ROOT, "tools", "hard", "bird_extra.py"), encoding="utf-8").read()
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "BOOK":
            return {sci: n for sci, ja, n, _ in ast.literal_eval(node.value)}
    raise SystemExit("bird_extra.py に BOOK が無い")

def get(u):
    for i in range(4):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "cladle-real-counts/0.1 (educational)"})
            return json.load(urllib.request.urlopen(req, timeout=60))
        except Exception as e:
            err = e; time.sleep(3 * (i + 1))
    raise err

def col_id(name, rank):
    q = urllib.parse.urlencode({"scientificName": name, "rank": rank})
    m = get(f"{API}/dataset/{COL_KEY}/match/nameusage?{q}"); time.sleep(0.3)
    u = m.get("usage") or {}
    ok = (m.get("type") in ("exact", "variant") and u.get("name") == name and u.get("status") == "accepted"
          and any(c["name"] == "Animalia" for c in u.get("classification", [])))
    return u["id"] if ok else None

def count(cid):
    m = get(f"{API}/dataset/{COL_KEY}/taxon/{cid}/metrics"); time.sleep(0.3)
    return m.get("speciesExtantCount") or 0

def selection(mode, top="linear"):
    """データの meta.selection.realCounts に入れる中身（make_bird.py・make_insect.py・merge_hard.py が使う）。
    数は、そのモードの階級の群の分だけ入れる"""
    R = json.load(open(OUT, encoding="utf-8"))
    if MODES[mode].get("self"):
        return {"ranks": MODES[mode]["ranks"], "groups": MODES[mode]["groups"], "top": top, "n": {}, "source": [FISH_SOURCE]}
    return {"ranks": MODES[mode]["ranks"], "top": top, "n": {k: v["n"] for k, v in R["taxa"].items()},
            "source": [R["source"][x] for x in sorted({v["src"] for v in R["taxa"].values()})]}

def trim(data):
    """realCounts の数を、データにある群の分だけに減らす"""
    rc = data["meta"]["selection"]["realCounts"]
    have = {c["sci"] for c in data["clades"] if c.get("rank") in rc["ranks"] or c["sci"] in rc.get("groups", [])}
    rc["n"] = {k: v for k, v in rc["n"].items() if k in have}
    rc["source"] = [x for x in rc["source"] if x != BOOK_SOURCE or any(k.endswith("formes") for k in rc["n"])]
    return data

def apply(data, mode, top="linear"):
    """データの出題の重みを実際の種数に切り替える（収録数で枠や門を重みづける古い設定は消す）"""
    sel = data["meta"]["selection"]
    for k in ("buckets", "otherBucketLabel", "phylumWeight", "bucketWeight", "bucketRank"): sel.pop(k, None)
    sel["realCounts"] = rc = selection(mode, top)
    if MODES[mode].get("self"):
        C = {c["id"]: c for c in data["clades"]}
        for sp in data["species"]:
            if sp.get("answerable") is False: continue
            g = group(C, sp["parent"], rc)
            if g: rc["n"][g["sci"]] = rc["n"].get(g["sci"], 0) + 1
        rc["n"] = dict(sorted(rc["n"].items()))
        return data
    return trim(data)

def group(C, p, rc, r=None):
    """種の親 p から上へたどって、階級 r（省略時は外側の群の階級）の節目か、groups にある節目を返す"""
    r = r or rc["ranks"][0]; extra = rc.get("groups", []) if r == rc["ranks"][0] else []
    hit, q = None, p
    while q:  # groups にある節目の中なら、その下に目があっても groups の節目を群にする
        if C[q]["sci"] in extra: return C[q]
        if hit is None and C[q].get("rank") == r: hit = C[q]
        q = C[q]["parent"]
    return hit

def probs(data):
    """js/core.js の byRealCounts と同じ計算で、種ごとの出題確率を返す（確認用）。数の無い群は missing に入れる"""
    sel = data["meta"]["selection"]; rc = sel["realCounts"]; r0, r1 = (rc["ranks"] + [None])[:2]
    TW = sel.get("tierWeights") or {"2": .9, "3": .8, "4": .7}
    C = {c["id"]: c for c in data["clades"]}
    up = lambda p, r: group(C, p, rc, r)
    n = rc["n"]; sub, top, missing = {}, {}, set()
    for c in data["clades"]:
        if r1 and c.get("rank") == r1 and c["sci"] in n:
            t = up(c["parent"], r0)
            if t: sub[t["id"]] = sub.get(t["id"], 0) + n[c["sci"]]
    for s in data["species"]:
        if s.get("answerable") is False: continue
        t = up(s["parent"], r0); u = up(s["parent"], r1) if r1 else None
        if not t or t["sci"] not in n: missing.add(t["sci"] if t else "（" + r0 + "なし）"); continue
        if u and u["sci"] not in n: missing.add(u["sci"])
        key = u["id"] if u and u["sci"] in n else "_rest"
        top.setdefault(t["id"], {}).setdefault(key, []).append(s)
    BW = {t: (n[C[t]["sci"]] ** .5 if rc.get("top") == "sqrt" else n[C[t]["sci"]]) for t in top}
    P, tot = {}, sum(BW.values())
    for t, g in top.items():
        w = {u: 1 if not r1 else max(0, n[C[t]["sci"]] - sub.get(t, 0)) if u == "_rest" else n[C[u]["sci"]] for u in g}
        if not any(w.values()): w = {u: 1 for u in g}
        wt = sum(w.values())
        for u, ss in g.items():
            sw = [TW.get(str(s.get("tier")), 1) for s in ss]; st = sum(sw)
            for s, x in zip(ss, sw): P[s["id"]] = BW[t] / tot * w[u] / wt * x / st
    return P, missing

RANK_EN = {"門": "phylum", "綱": "class", "目": "order"}

def wanted():
    """各モードのデータ（今の版と予約中の版）から、数える群の学名と階級を拾う"""
    need = {}
    for mode in MODES.values():
        if mode.get("self"): continue
        f = mode["file"]
        while f:
            d = json.load(open(os.path.join(ROOT, f), encoding="utf-8"))
            for c in d["clades"]:
                if c.get("rank") in mode["ranks"]: need[c["sci"]] = RANK_EN[c["rank"]]
            f = (d["meta"].get("next") or {}).get("file")
    return need

def main():
    old = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    refresh = "--refresh" in sys.argv or old.get("colKey") != COL_KEY
    taxa = {} if refresh else old.get("taxa", {})
    book = bird_book()
    for sci, rank in sorted(wanted().items()):
        if rank == "order" and sci in book:
            taxa[sci] = {"n": book[sci], "src": "book"}; continue
        if sci in taxa and taxa[sci].get("src") == "col" and taxa[sci].get("alias") == ALIAS.get(sci): continue
        parts = ALIAS.get(sci, [[sci, rank]])
        n, ids, miss = 0, [], []
        for name, r in parts:
            cid = col_id(name, r)
            if cid is None: miss.append(name); continue
            ids.append(cid); n += count(cid)
        if miss:
            print("× Catalogue of Life で一つに決まらない:", sci, miss); continue
        taxa[sci] = {"n": n, "src": "col", "col": ids, **({"alias": ALIAS[sci]} if sci in ALIAS else {})}
        print(f"{sci}: {n}", flush=True)
    json.dump({"source": {"col": SOURCE, "book": BOOK_SOURCE}, "colKey": COL_KEY, "taxa": dict(sorted(taxa.items()))},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(OUT, len(taxa), "群")

if __name__ == "__main__":
    if "--attach" in sys.argv:
        # 例：python3 tools/real_counts.py --attach data-hard-0.3.11.json hard sqrt（作り直さずに出題の重みだけ入れ替える）
        i = sys.argv.index("--attach"); f, mode, top = sys.argv[i + 1:i + 4]
        d = json.load(open(f, encoding="utf-8"))
        json.dump(apply(d, mode, top), open(f, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    else:
        main()
