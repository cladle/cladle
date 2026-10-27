"""鳥・哺乳類の追加候補を学会の標準和名リストと照らす（リスト本体は同梱しない）。
出力 std_land.json: 元の学名 -> {stdJa, stdSci}"""
import json, re, sys, openpyxl
bio, match, bird_x, mam_x, out = sys.argv[1:6]
norm = lambda s: re.sub(r"\s+", " ", str(s).strip())
L = {}; J = {"73_cho": {}, "74_ho": {}}
for k, x in (("73_cho", bird_x), ("74_ho", mam_x)): L[k] = {}
wb = openpyxl.load_workbook(bird_x, read_only=True)
for (a, *_) in wb.worksheets[0].iter_rows(values_only=True):
    if not a: continue
    m = re.match(r"\s*\d+\.\s+([A-Z][a-z]+ [a-z]+(?: [a-z]+)?)\s+(\S+)", str(a))
    if m:
        L["73_cho"][m.group(1)] = m.group(2)
        if len(m.group(1).split()) == 2: J["73_cho"].setdefault(m.group(2), m.group(1))
wb = openpyxl.load_workbook(mam_x, read_only=True)
for i, r in enumerate(wb.worksheets[0].iter_rows(values_only=True)):
    if i < 2 or not r[12] or not r[14] or not r[15]: continue
    L["74_ho"][norm(f"{r[12]} {r[14]}")] = norm(r[15])
    for j in re.split(r"[（）()]", norm(r[15])):
        if j: J["74_ho"].setdefault(j, norm(f"{r[12]} {r[14]}"))
    if r[22]: L["74_ho"].setdefault(norm(r[22]), norm(r[15]))
B = json.load(open(bio)); M = json.load(open(match)); res = {}
for k in ("73_cho", "74_ho"):
    S = L[k]
    for r in B[k]:
        s = re.sub(r" \([A-Z][a-z]+\)", "", r["sci"]); w = s.split()
        cands = []
        d = (M.get(r["sci"]) or {}).get("match") or {}
        u = d.get("usage", {})
        acc = next((c["name"] for c in u.get("classification", []) if c["rank"] == "species"), None) if u.get("rank") != "species" or u.get("status") not in ("accepted", "provisionally accepted") else u.get("name")
        if acc: cands.append(" ".join(re.sub(r" \([A-Z][a-z]+\)", "", acc).split()[:2]))
        cands += ([f"{w[0]} {w[2]}"] if len(w) == 3 else []) + [s, " ".join(w[:2])]
        hit = next(((c, S[c]) for c in cands if c in S), (None, None))
        if not hit[0] and r["ja"] in J[k]: hit = (J[k][r["ja"]], S[J[k][r["ja"]]])
        if hit[0]: hit = (" ".join(hit[0].split()[:2]), S.get(" ".join(hit[0].split()[:2]), hit[1]))
        res[r["sci"]] = {"grp": k, "ja": r["ja"], "acc": acc, "stdSci": hit[0], "stdJa": hit[1]}
json.dump(res, open(out, "w"), ensure_ascii=False, indent=0)
json.dump({"std": [{"sci": v["stdSci"], "ja": v["stdJa"]} for v in res.values() if v["stdSci"]]}, open(out.replace(".json", "_q.json"), "w"), ensure_ascii=False)
import collections
print(collections.Counter((v["grp"], "none" if not v["stdJa"] else "same" if v["stdJa"] == v["ja"] else "diff") for v in res.values()))
for v in res.values():
    if v["stdJa"] != v["ja"]: print(v["grp"], v["ja"], "|", v["stdJa"], v["stdSci"], "| acc", v["acc"])
