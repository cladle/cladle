"""merge_hard.py の MOVE_INTO（置き場所の直し）を、出来上がった data-*.json に当てる。

作り直しをせずに予約版などの木を直すときに使う。直したあと、同じ属が二つの節目に分かれたものは深い方にまとめ、
種のいなくなった節目は消す。

  python3 tools/hard/move_into.py data-hard-0.3.12.json data-insect-0.1.3.json
"""
import ast, collections, json, os, sys

src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "merge_hard.py"), encoding="utf-8").read()
node = next(n for n in ast.parse(src).body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "MOVE_INTO")
MOVE_INTO = ast.literal_eval(node.value)

def anc(C, i):
    out = []
    while i: out.append(i); i = C[i]["parent"]
    return out

for f in sys.argv[1:]:
    data = json.load(open(f, encoding="utf-8"))
    C = {c["id"]: c for c in data["clades"]}
    moved = []
    for to, items in MOVE_INTO.items():
        t = [i for i, c in C.items() if c["sci"] == to and c["rank"] != "属"]
        if len(t) != 1: continue
        for i, c in C.items():
            if c["sci"] in items and c["parent"] != t[0] and i not in anc(C, t[0]):
                moved.append(f"{c['sci']}: {C[c['parent']]['sci']} → {to}"); c["parent"] = t[0]
    # 同じ属が二つの節目になり、一方がもう一方の上の節目の直下にあるものは、深い方へまとめる
    gen = collections.defaultdict(list)
    for i, c in C.items():
        if c["rank"] == "属": gen[c["sci"]].append(i)
    for g, ids in gen.items():
        for a in ids:
            for b in ids:
                if a != b and a in C and b in C and C[a]["parent"] in anc(C, C[b]["parent"])[1:]:
                    for x in list(C.values()) + data["species"]:
                        if x["parent"] == a: x["parent"] = b
                    moved.append(f"{g}: 属を {C[C[a]['parent']]['sci']} から {C[C[b]['parent']]['sci']} の下へまとめた"); del C[a]
    has = set()
    for s in data["species"]:
        p = s["parent"]
        while p and p not in has: has.add(p); p = C[p]["parent"]
    gone = [c["sci"] for i, c in C.items() if i not in has]
    data["clades"] = [c for c in data["clades"] if c["id"] in C and c["id"] in has]
    json.dump(data, open(f, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"{f}: {len(moved)} 件")
    for m in moved: print("  " + m)
    if gone: print("  種がいなくなって消した節目:", ", ".join(gone))
