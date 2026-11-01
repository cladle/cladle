"""陸の生き物の追加分（ゲキムズ用）を作る。
入力: 環境省「種の多様性調査 対象種一覧」の読み取り（biodic_use.json）と学名照合（match.json）、
      Japan Spider Catalog の種リスト（taxon-ja.csv）、クモの科の CoL 照合（jsc_fam_col.json）と下目（spider_infra.json）
出力: land.json（[{id, ja, sci, aliases, subspeciesAliases, tier, src, classification:[{rank,name}] 根から順}]）と land.log.json"""
import json, csv, re, sys, collections
bio, match, jsc, famcol, infra, out, stdf, stdm, inatf = sys.argv[1:10]
B = json.load(open(bio)); M = json.load(open(match)); log = collections.defaultdict(list)
# 鳥・哺乳類は学会の標準和名リスト（日本鳥類目録第8版、世界哺乳類標準和名リスト2021）で種と和名を決める。リストに無いものは入れない
STD = json.load(open(stdf)); MS = json.load(open(stdm))
# iNaturalist と和名が違うもの（照合のみ。名前は変えず要確認にする）
INAT = {sci: re.sub(r"\s*[（(].*?[)）]|旧名?|\(旧\)", "", ij).strip() for _, bj, ij, sci in json.load(open(inatf))}
b2 = lambda s: " ".join(re.sub(r" \([A-Z][a-z]+\)", "", s).split()[:2])
SRC = {"01_ka": "陸産及び淡水産貝類", "05_to": "昆虫(トンボ)類", "06_cho": "昆虫(チョウ)類", "07_se": "昆虫(セミ・水生半翅)類",
       "08_ga": "昆虫(ガ)類", "09_ko": "昆虫(甲虫)類", "73_cho": "鳥類", "74_ho": "哺乳類"}
def accepted(d):
    u = d["usage"]
    if u.get("status") in ("accepted", "provisionally accepted"):
        if u["rank"] == "species": return u["name"], u["classification"]
        sp = next((c for c in u["classification"] if c["rank"] == "species"), None)
        return (sp["name"], u["classification"][u["classification"].index(sp) + 1:]) if sp else (None, None)
    cl = u.get("classification", [])
    sp = next((c for c in cl if c["rank"] == "species"), None)
    if not sp or sp.get("status") not in ("accepted", "provisionally accepted"): return None, None
    return sp["name"], cl[cl.index(sp) + 1:]
G = collections.OrderedDict(); ALT = {}
for k, rows in B.items():
    for r in rows:
        if k in ("73_cho", "74_ho"):
            st = STD.get(r["sci"]) or {}
            sj = st.get("stdJa") or ""
            if not st.get("stdSci") or "検討中" in sj: log["std_none"].append((k, r["sci"], r["ja"])); continue
            parts = [x for x in re.split(r"[（）()]", sj) if x and "新称" not in x]
            d = (MS.get(st["stdSci"]) or {}).get("match") or (M.get(r["sci"]) or {}).get("match")
            if not d: log["std_nomatch"].append((k, st["stdSci"], sj)); continue
            sp, cl = accepted(d)
            if not sp: log["noaccepted"].append((k, st["stdSci"], sj)); continue
            sp = b2(sp)
            # 種の範囲は標準和名リストに従う（CoL がまとめていても分ける）。属が食い違うときは CoL の名前のまま
            if sp != st["stdSci"]:
                if sp.split()[0] == st["stdSci"].split()[0]: log["std_split"].append((sp, st["stdSci"], parts[0])); sp = st["stdSci"]
                else: log["std_genus_diff"].append((sp, st["stdSci"], parts[0]))
            g = G.setdefault(sp, {"rows": [], "cl": cl, "src": k})
            g["rows"].append((st["stdSci"], parts[0], True))
            ALT.setdefault(sp, set()).update(parts[1:])
            if r["ja"] != parts[0] and len(re.sub(r" \([A-Z][a-z]+\)", "", r["sci"]).split()) == 3: g["rows"].append((r["sci"], r["ja"], False))
            continue
        d = (M.get(r["sci"]) or {}).get("match")
        if not d: log["nomatch"].append((k, r["sci"], r["ja"])); continue
        sp, cl = accepted(d)
        if not sp: log["noaccepted"].append((k, r["sci"], r["ja"])); continue
        sp = b2(sp)
        g = G.setdefault(sp, {"rows": [], "cl": cl, "src": k})
        g["rows"].append((r["sci"], r["ja"], len(re.sub(r" \([A-Z][a-z]+\)", "", r["sci"]).split()) == 2))
        ALT.setdefault(sp, set()).update(r.get("alt", []))
        if INAT.get(r["sci"]) and INAT[r["sci"]] != r["ja"]: g.setdefault("inat", INAT[r["sci"]])
L = []
for sp, g in G.items():
    spr = [ja for s, ja, isp in g["rows"] if isp]
    sub = [ja for s, ja, isp in g["rows"] if not isp]
    if spr: ja = spr[0]
    elif len(set(sub)) == 1: ja = sub[0]
    else: log["only_subspecies"].append((sp, sorted(set(sub)))); continue
    if len(set(spr)) > 1:
        # 別種どうしが一つにまとまったときは、学名がそのまま一致する行の和名だけを使う（他の名前は別名にもしない）
        ex = {ja for s_, ja, isp in g["rows"] if isp and b2(s_) == sp}
        if len(ex) != 1: log["multi_species_ja"].append((sp, sorted(set(spr)))); continue
        ja = ex.pop(); log["multi_species_pick"].append((sp, ja, sorted(set(spr) - {ja}))); sub = []
    subs = sorted(set(sub) - {ja})
    cl = [{"rank": c["rank"], "name": c["name"]} for c in reversed(g["cl"]) if c["rank"] not in ("species", "subspecies")]
    al = sorted(set(subs) | (ALT.get(sp, set()) - {ja}))
    ver = {"verify": {"ja": f"環境省の対象種一覧の表記。iNaturalist では「{g['inat']}」"}} if g.get("inat") and g["inat"] != ja and g["src"] not in ("73_cho", "74_ho") else {}
    L.append({"id": "l" + re.sub(r"[^a-z]", "", sp.lower()), "ja": ja, "sci": sp, "aliases": al, "subspeciesAliases": subs, **ver,
              "tier": 4, "src": "biodic:" + g["src"], "classification": cl,
              **({"sciSynonyms": sorted({b2(s) for s, _, _ in g["rows"]} - {sp})} if {b2(s) for s, _, _ in g["rows"]} - {sp} else {})})
# クモ
F = json.load(open(famcol)); IN = json.load(open(infra)); IN.update({"Heptathelidae": "Mesothelae", "Cheiracanthiidae": "Araneomorphae"})
base = [{"rank": "domain", "name": "Eukaryota"}, {"rank": "kingdom", "name": "Animalia"}, {"rank": "phylum", "name": "Arthropoda"},
        {"rank": "subphylum", "name": "Chelicerata"}, {"rank": "class", "name": "Arachnida"}, {"rank": "order", "name": "Araneae"}]
INFRA = {"Mesothelae": [{"rank": "suborder", "name": "Mesothelae"}],
         "Mygalomorphae": [{"rank": "suborder", "name": "Opisthothelae"}, {"rank": "infraorder", "name": "Mygalomorphae"}],
         "Araneomorphae": [{"rank": "suborder", "name": "Opisthothelae"}, {"rank": "infraorder", "name": "Araneomorphae"}]}
cladeJa = {"Araneae": "クモ目", "Mesothelae": "中疣亜目", "Opisthothelae": "後疣亜目", "Mygalomorphae": "トタテグモ下目", "Araneomorphae": "クモ下目"}
for r in csv.DictReader(open(jsc, encoding="utf-8-sig")):
    if r["階級"] != "species" or not r["和名"]: continue
    fam = r["Family"]
    cladeJa.setdefault(fam, r["Family_ja"].strip())
    L.append({"id": "l" + re.sub(r"[^a-z]", "", r["学名"].lower()), "ja": r["和名"].strip(), "sci": r["学名"].strip(), "aliases": [],
              "tier": 4, "src": "jsc", "classification": base + INFRA[IN[fam]] + [{"rank": "family", "name": fam}]})
# 同じ和名・学名の重なり
c = collections.Counter(x["ja"] for x in L); log["dup_ja"] = [k for k, v in c.items() if v > 1]
c = collections.Counter(x["sci"] for x in L); log["dup_sci"] = [k for k, v in c.items() if v > 1]
bad = set(log["dup_ja"]) ; L2 = [x for x in L if x["ja"] not in bad]
allja = {x["ja"] for x in L2}
for x in L2:
    for f in ("aliases", "subspeciesAliases"):
        if f in x:
            drop = [a for a in x[f] if a in allja]
            if drop: log["alias_is_other_ja"].append((x["ja"], drop)); x[f] = [a for a in x[f] if a not in allja]
seen = set(); L3 = []
for x in L2:
    if x["sci"] in seen: continue
    seen.add(x["sci"]); L3.append(x)
json.dump({"species": L3, "cladeJa": cladeJa, "sources": SRC}, open(out, "w"), ensure_ascii=False, indent=0)
json.dump(log, open(out + ".log.json", "w"), ensure_ascii=False, indent=0)
print(len(L3), {k: len(v) for k, v in log.items()}, collections.Counter(x["src"] for x in L3))
