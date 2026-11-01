# -*- coding: utf-8 -*-
"""ゲキムズ（と昆虫編）に足す昆虫の一覧（tools/hard/insect_extra.json）を作る。

  python3 tools/hard/insect_extra.py data-hard.json <land_build.log.json> <取得結果を置くフォルダ> tools/hard/insect_extra.json

候補は 2 種類：
- 環境省「種の多様性調査（動物分布調査）対象種一覧」（1997）の昆虫のうち、当時の学名が Catalogue of Life と
  合わずに落ちていたもの（陸の生き物の追加のログ land_build.log.json の nomatch）。
- iNaturalist の日本の研究用観察数（research grade）の上位 TOP 種の昆虫で、ゲキムズに無いもの（身近さの目安）。
学名：Catalogue of Life（ChecklistBank 3LR）で accepted な種。昔の学名は GBIF の異名から今の学名に読み替え、
      それでも引けないときは iNaturalist の和名から学名を引く。CoL に種が無いもの（日本のチョウ・カメムシなどに多い）は
      GBIF Backbone の accepted な種を使い、分類は CoL の属（無ければ GBIF）に従う。
和名：iNaturalist・Wikidata・GBIF（環境省の種は環境省の和名も1票）のうち 2 つ以上でそろう名前だけ。
取得結果は取得結果フォルダに 1 件ずつためて、2 回目からはそれを使う（外部の API に何度も問い合わせない）。
出力は陸の生き物（land.json）と同じ形で、merge_hard.py が陸の生き物と一緒に足す。
"""
import json, os, re, sys, time, urllib.parse, urllib.request

src, logf, cache, out = sys.argv[1:5]
TOP = 300
os.makedirs(cache, exist_ok=True)
H = json.load(open(src, encoding="utf-8"))
have_sci = {s["sci"] for s in H["species"]} | {a for s in H["species"] for a in s.get("sciSynonyms", [])}
have_ja = {s["ja"] for s in H["species"]} | {a for s in H["species"] for a in s.get("aliases", [])}

def get(u):
    for _ in range(3):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "cladle-name-check/0.1 (educational)"})
            return json.load(urllib.request.urlopen(req, timeout=60))
        except Exception: time.sleep(3)
class Cache:
    def __init__(self, name): self.p = os.path.join(cache, name); self.d = json.load(open(self.p, encoding="utf-8")) if os.path.exists(self.p) else {}
    def __call__(self, key, fn, wait):
        if key not in self.d:
            self.d[key] = fn(); time.sleep(wait)
            json.dump(self.d, open(self.p, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        return self.d[key]
COL, GB, INAT, INATJA, WD = (Cache(n) for n in ("col_species.json", "gbif_match2.json", "inat_sci.json", "inat_ja.json", "wikidata_sp.json"))
GBV = Cache("gbif_vern.json")

def col(name):
    def f():
        u = (get("https://api.checklistbank.org/dataset/3LR/match/nameusage?" + urllib.parse.urlencode({"q": name})) or {}).get("usage") or {}
        return {"rank": u.get("rank"), "status": u.get("status"), "name": re.sub(r" \([A-Z][a-z]+\)", "", u.get("name") or "") or None,
                "cl": [{"rank": c["rank"], "name": c["name"]} for c in reversed(u.get("classification", []))]}
    return COL(name, f, 0.4)
def gbif(name):
    def f():
        m = get("https://api.gbif.org/v1/species/match?" + urllib.parse.urlencode({"name": name, "kingdom": "Animalia"})) or {}
        acc = m.get("species") if m.get("rank") == "SPECIES" or m.get("synonym") else None
        return {"key": m.get("acceptedUsageKey") or m.get("usageKey"), "accepted": acc, "rank": m.get("rank"), "match": m.get("matchType"),
                "cl": [{"rank": k, "name": m[k]} for k in ("kingdom", "phylum", "class", "order", "family", "genus") if m.get(k)]}
    return GB(name, f, 0.3)
def gbif_ja(key):
    def f():
        v = get(f"https://api.gbif.org/v1/species/{key}/vernacularNames?limit=200") or {}
        return sorted({y["vernacularName"] for y in v.get("results", []) if y.get("language") == "jpn"})
    return GBV(str(key), f, 0.3)
def inat_sci(name):
    def f():
        for t in (get("https://api.inaturalist.org/v1/taxa?" + urllib.parse.urlencode({"q": name, "locale": "ja", "per_page": 10})) or {}).get("results", []):
            if t["name"] == name and t["rank"] == "species": return t.get("preferred_common_name")
    return INAT(name, f, 1)
def inat_by_ja(ja):
    def f():
        r = [t["name"] for t in (get("https://api.inaturalist.org/v1/taxa?" + urllib.parse.urlencode({"q": ja, "locale": "ja", "per_page": 10})) or {}).get("results", [])
             if t.get("preferred_common_name") == ja and t["rank"] == "species" and t.get("iconic_taxon_name") == "Insecta"]
        return r[0] if len(r) == 1 else None
    return INATJA(ja, f, 1)
def wd(name):
    def f():
        q = 'SELECT ?l WHERE { ?i wdt:P225 "%s" ; rdfs:label ?l FILTER(lang(?l)="ja") }' % name
        d = get("https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": q, "format": "json"})) or {"results": {"bindings": []}}
        return sorted({b["l"]["value"] for b in d["results"]["bindings"]})
    return WD(name, f, 0.5)

def accepted(name, ja):
    """今の学名・分類（根から順）・学名の出典。CoL に種が無いときは GBIF Backbone の accepted な種で、
    分類は CoL にその属があれば CoL の属の分類、無ければ GBIF の分類。どちらにも無ければ None"""
    b = " ".join(name.split()[:2])
    cands = [x for x in (b, gbif(b).get("accepted"), inat_by_ja(ja)) if x]
    for cand in cands:
        c = col(cand)
        if c["rank"] == "species" and c["status"] in ("accepted", "provisionally accepted") and c["name"] == cand: return cand, c["cl"], "CoL"
    for cand in cands:
        g = gbif(cand)
        if g.get("rank") == "SPECIES" and g.get("accepted") == cand:
            cg = col(cand.split()[0])
            if cg["rank"] == "genus" and cg["status"] == "accepted" and cg["name"] == cand.split()[0]:
                return cand, cg["cl"] + [{"rank": "genus", "name": cg["name"]}], "GBIF"
            return cand, [{"rank": "domain", "name": "Eukaryota"}] + g["cl"], "GBIF"
    return None, None, None

# ---- 候補 ----
cands = []
L = json.load(open(logf, encoding="utf-8"))
for k, sci, ja in L.get("nomatch", []):
    if k in ("05_to", "06_cho", "07_se", "08_ga", "09_ko"): cands.append({"ja": ja, "sci": sci, "src": "biodic:" + k})
top = json.load(open(os.path.join(cache, "inat_japan_top.json"), encoding="utf-8")) if os.path.exists(os.path.join(cache, "inat_japan_top.json")) else None
if top is None:
    top = []
    for page in range(1, TOP // 500 + 2):
        d = get("https://api.inaturalist.org/v1/observations/species_counts?" + urllib.parse.urlencode(
            {"place_id": 6737, "iconic_taxa": "Insecta", "quality_grade": "research", "locale": "ja", "per_page": 500, "page": page}))
        top += [{"sci": r["taxon"]["name"], "ja": r["taxon"].get("preferred_common_name"), "n": r["count"]} for r in d["results"] if r["taxon"]["rank"] == "species"]
        time.sleep(1.5)
    json.dump(top, open(os.path.join(cache, "inat_japan_top.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
for i, x in enumerate(top[:TOP]):
    if x["ja"]: cands.append({"ja": x["ja"], "sci": x["sci"], "src": f"inat-japan-top{TOP}:{i + 1}"})

# ---- 照合 ----
res, skip, seen = [], [], set()
for x in cands:
    if x["ja"] in have_ja or x["sci"] in have_sci: skip.append([x["ja"], x["sci"], "already"]); continue
    sci, cl, sci_src = accepted(x["sci"], x["ja"])
    if not sci: skip.append([x["ja"], x["sci"], "no_col_species"]); continue
    if sci in have_sci or sci in seen: skip.append([x["ja"], sci, "already"]); continue
    if not any(c["name"] == "Insecta" for c in cl): skip.append([x["ja"], sci, "not_insect"]); continue
    votes = {}
    for who, names in (("iNaturalist", [inat_sci(sci)]), ("Wikidata", wd(sci)), ("GBIF", gbif_ja(gbif(sci)["key"]) if gbif(sci).get("key") else []),
                       ("環境省1997", [x["ja"]] if x["src"].startswith("biodic") else [])):
        for n in names:
            if n and re.fullmatch(r"[ァ-ヶー]+", n): votes.setdefault(n, set()).add(who)
    best = sorted(votes.items(), key=lambda kv: -len(kv[1]))
    if not best or len(best[0][1]) < 2 or (len(best) > 1 and len(best[1][1]) == len(best[0][1])):
        skip.append([x["ja"], sci, "ja_not_agreed", {k: sorted(v) for k, v in votes.items()}]); continue
    ja = best[0][0]
    if ja in have_ja: skip.append([ja, sci, "ja_exists"]); continue
    seen.add(sci); have_ja.add(ja)
    res.append({"id": "i" + re.sub(r"[^a-z0-9]", "", sci.lower()), "ja": ja, "sci": sci, "aliases": [], "tier": 4, "src": x["src"], "sciSource": sci_src,
                "jaVotes": sorted(best[0][1]), "classification": cl})
json.dump({"species": res, "skipped": skip}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{out}: 足す {len(res)}（環境省 {sum(1 for r in res if r['src'].startswith('biodic'))}・iNaturalist {sum(1 for r in res if r['src'].startswith('inat'))}）・見送り {len(skip)}")
