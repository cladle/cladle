# -*- coding: utf-8 -*-
"""ゲキムズの昆虫の目・科の並びと和名を作る（tools/hard/insect_taxa.json）。

  python3 tools/hard/insect_taxa.py data-hard.json <環境省PDFのフォルダ> <取得結果を置くフォルダ> tools/hard/insect_taxa.json

- 科と目の並び：Catalogue of Life（ChecklistBank 3LR）。科の無い属・目の無い属と、昆虫の全ての科を一度ずつ引く。
- 目より上の置き場所（ORDER_UNDER）は Misof et al. 2014（Science 346: 763–767）の系統に沿い、ゲキムズに既にある
  まとまり（多新翅類・準新翅類・完全変態類など）の中だけに置く。
- 和名：環境省「種の多様性調査（動物分布調査）対象種一覧」（1997、昆虫5群、PDL1.0）の科の和名を最優先。
  無ければ Wikidata・GBIF・iNaturalist のうち 2 つ以上でそろう名前（データの取得元の決まりと同じ多数決）。
  そろわなければ学名のまま。階級の語尾（目・亜目・下目・上科・科）が合わない名前は数えない。
  語尾の無い名前（Wikidata の「ヤンマ」など）は、その階級の語尾を付けたものとして数える。
- 取得結果は取得結果フォルダに 1 件ずつためて、2 回目からはそれを使う（外部の API に何度も問い合わせない）。
- 亜科：同じ科に Catalogue of Life の亜科が 2 つ以上出てくる科だけ、属をその亜科の節目の下に入れる
  （ハンミョウ亜科とオサムシ亜科など）。亜科の和名も上と同じ決まり。
- 作り直したゲキムズにもう一度かけてよい。前の insect_taxa.json の属の対応は残し、新しく科の無い属が出たら足す。
"""
import json, os, re, sys, time, unicodedata, urllib.parse, urllib.request, collections

src, pdfdir, cache, out = sys.argv[1:5]
os.makedirs(cache, exist_ok=True)
H = json.load(open(src, encoding="utf-8"))
C = {c["id"]: c for c in H["clades"]}
def anc(p):
    while p: yield C[p]; p = C[p]["parent"]
def insect(i): return "Insecta" in {c["sci"] for c in anc(i)}

def get(u):
    for _ in range(3):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "cladle-name-check/0.1 (educational)"})
            return json.load(urllib.request.urlopen(req, timeout=30))
        except Exception: time.sleep(3)
def cached(name, keys, fn):
    """取得結果フォルダの name に、keys のうちまだ無いものだけ fn(key) で取ってためる"""
    p = os.path.join(cache, name)
    d = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    for k in keys:
        if k not in d: d[k] = fn(k); json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    return d
def col(q, rank=None):
    time.sleep(0.4)
    d = get("https://api.checklistbank.org/dataset/3LR/match/nameusage?" + urllib.parse.urlencode({"q": q, **({"rank": rank} if rank else {})})) or {}
    u = d.get("usage") or {}
    return {"status": u.get("status"), "cl": [(c["rank"], c["name"]) for c in u.get("classification", [])]}

# ---- 1. 科・目の無い属と、昆虫の科（Catalogue of Life） ----
need = {}
for s in H["species"]:
    a = list(anc(s["parent"]))
    if "Insecta" not in {c["sci"] for c in a}: continue
    r = {c["rank"] for c in a}
    if "科" not in r or "目" not in r: need[a[0]["sci"]] = s["sci"]
G = cached("col_genera.json", sorted(need), lambda g: col(need[g]))
GENUS_FIX = {"Graphosoma": "Pentatomidae", "Halyomorpha": "Pentatomidae", "Megacopta": "Plataspidae"}  # 種名が CoL で引けなかったもの（属の所属は CoL と同じ）
genera = json.load(open(out, encoding="utf-8")).get("genera", {}) if os.path.exists(out) else {}
for g in need:
    f = GENUS_FIX.get(g) or next((n for r, n in G.get(g, {}).get("cl", []) if r == "family"), None)
    if f: genera[g] = f
fams = {c["sci"] for c in H["clades"] if c["rank"] == "科" and insect(c["id"])} | set(genera.values())
F = cached("col_families.json", sorted(fams), lambda f: col(f, "family"))
FAM_UNDER = {"Plataspidae": ["Pentatomoidea", "Pentatomomorpha", "Heteroptera", "Hemiptera"],
             # CoL のハエ目は科の上の階級が無い。ハエ下目（Muscomorpha）は Wiegmann et al. 2011（PNAS 108: 5690–5695）
             "Drosophilidae": ["Muscomorpha", "Diptera"], "Muscidae": ["Muscomorpha", "Diptera"], "Syrphidae": ["Muscomorpha", "Diptera"]}
ORDER_UNDER = {
    "Archaeognatha": "Insecta", "Zygentoma": "Insecta", "Ephemeroptera": "Pterygota",
    "Plecoptera": "Polyneoptera", "Dermaptera": "Polyneoptera", "Notoptera": "Polyneoptera", "Embioptera": "Polyneoptera",
    "Phasmida": "Polyneoptera", "Zoraptera": "Polyneoptera", "Mantodea": "Dictyoptera",
    "Thysanoptera": "Paraneoptera", "Psocodea": "Paraneoptera",
    "Neuroptera": "Neuropterida", "Megaloptera": "Neuropterida", "Raphidioptera": "Neuropterida",
    "Siphonaptera": "Mecopterida", "Mecoptera": "Mecopterida", "Trichoptera": "Mecopterida", "Strepsiptera": "Holometabola",
}
UP = ("superfamily", "infraorder", "suborder", "order")
families, orders, syn = {}, {}, {}
for f in sorted(fams):
    cl = F.get(f, {}).get("cl", [])
    path = FAM_UNDER.get(f) or [n for r, n in cl if r in UP or r in ("parvorder", "series")]
    o = next((n for r, n in cl if r == "order"), path[-1] if path else None)
    if F.get(f, {}).get("status") == "synonym":  # 今の名前（classification の一番下の科）に読み替える
        syn[f] = next(n for r, n in cl if r == "family"); continue
    if not o: continue
    families[f] = {"order": o, "under": path}
    if o in ORDER_UNDER: orders[o] = {"under": ORDER_UNDER[o]}

# ---- 1b. 亜科（Catalogue of Life）。同じ科に 2 つ以上の亜科が出てくる科だけ、亜科の節目を置く ----
gen_fam = {}
for c in H["clades"]:
    if c["rank"] == "属" and insect(c["id"]):
        f = next((a["sci"] for a in anc(c["parent"]) if a["rank"] == "科"), None)
        if f: gen_fam[c["sci"]] = f
GA = cached("col_genus_all.json", sorted(gen_fam), lambda g: col(g, "genus"))
genus_sub = {}
for g, f in gen_fam.items():
    cl = GA.get(g, {}).get("cl", [])
    if GA.get(g, {}).get("status") != "accepted": continue
    sub = next((n for r, n in cl if r == "subfamily"), None)
    cf = next((n for r, n in cl if r == "family"), None)
    if sub and cf == f: genus_sub[g] = sub
by_fam = collections.defaultdict(set)
for g, sub in genus_sub.items(): by_fam[gen_fam[g]].add(sub)
genus_sub = {g: sub for g, sub in genus_sub.items() if len(by_fam[gen_fam[g]]) >= 2}
subfamilies = {sub: {"family": gen_fam[g]} for g, sub in genus_sub.items()}

# ---- 2. 和名 ----
B = {}
for f in ("05_to", "06_cho", "07_se", "08_ga", "09_ko"):
    import pdfplumber
    for pg in pdfplumber.open(os.path.join(pdfdir, f + ".pdf")).pages:
        for ln in (pg.extract_text() or "").splitlines():
            ln = unicodedata.normalize("NFKC", ln).strip()
            m = re.match(r"^([A-Z]{4,})(?:\s*\(([A-Za-z]+)\))?\s+([ァ-ヶー]+(?:科|目))\s*$", ln)
            if m:
                for n in (m[1], m[2]):
                    if n: B.setdefault(n.title(), m[3])
RANK = {"目": "目", "亜目": "亜目", "下目": "下目", "上科": "上科", "科": "科", "亜科": "亜科"}
names = {}
for c in H["clades"]:
    if c["rank"] in RANK and c["ja"] == c["sci"] and insect(c["id"]): names[c["sci"]] = c["rank"]
for f in families: names.setdefault(f, "科")
for o in orders: names.setdefault(o, "目")
for sub in subfamilies: names.setdefault(sub, "亜科")
def wd(n):
    q = "SELECT ?l WHERE { ?i wdt:P225 \"%s\" ; rdfs:label ?l FILTER(lang(?l)='ja') }" % n
    d = get("https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": q, "format": "json"}))
    time.sleep(0.5)
    return [b["l"]["value"] for b in d["results"]["bindings"]]
def vern(n):
    x = {}
    m = get("https://api.gbif.org/v1/species/match?" + urllib.parse.urlencode({"name": n, "kingdom": "Animalia"})) or {}
    if m.get("usageKey") and m.get("canonicalName") == n:
        v = get(f"https://api.gbif.org/v1/species/{m['usageKey']}/vernacularNames?limit=200") or {}
        x["gbif"] = sorted({y["vernacularName"] for y in v.get("results", []) if y.get("language") == "jpn"})
    time.sleep(0.3)
    i = get("https://api.inaturalist.org/v1/taxa?" + urllib.parse.urlencode({"q": n, "locale": "ja", "per_page": 5})) or {}
    for t in i.get("results", []):
        if t["name"] == n: x["inat"] = t.get("preferred_common_name"); break
    time.sleep(1)
    return x
W, V = cached("wikidata.json", sorted(names), wd), cached("vernacular.json", sorted(names), vern)
def norm(nm, suf):
    nm = nm.strip()
    if nm.endswith(suf) and not (suf == "目" and nm.endswith(("亜目", "下目", "上目"))) and not (suf == "科" and nm.endswith(("亜科", "上科"))): return nm
    if re.fullmatch(r"[ァ-ヶー]+", nm): return nm + suf
ja, votes = {}, {}
for n, rk in sorted(names.items()):
    if n in B and rk == "科": ja[n] = {"ja": B[n], "source": "環境省1997"}; continue
    v = collections.defaultdict(set)
    for who, lst in (("Wikidata", W.get(n, [])), ("GBIF", [p for x in V.get(n, {}).get("gbif", []) for p in re.split("[／/]", x)]),
                     ("iNaturalist", [V.get(n, {}).get("inat")] if V.get(n, {}).get("inat") else [])):
        for x in lst:
            y = norm(x, RANK[rk])
            if y: v[y].add(who)
    votes[n] = {k: sorted(s) for k, s in v.items()}
    top = sorted(v.items(), key=lambda kv: -len(kv[1]))
    if top and len(top[0][1]) >= 2 and (len(top) == 1 or len(top[1][1]) < len(top[0][1])):
        ja[n] = {"ja": top[0][0], "source": "・".join(sorted(top[0][1]))}

for o in orders: orders[o]["ja"] = ja.get(o, {}).get("ja", o)
for f in families: families[f]["ja"] = ja.get(f, {}).get("ja", f)
for sub in subfamilies: subfamilies[sub]["ja"] = ja.get(sub, {}).get("ja", sub)
json.dump({"source": "目・科の並び：Catalogue of Life（ChecklistBank 3LR）。和名：環境省（1997）種の多様性調査（動物分布調査）対象種一覧、無ければ Wikidata・GBIF・iNaturalist の多数決",
           "orders": orders, "families": families, "familySynonyms": syn, "genera": genera,
           "subfamilies": subfamilies, "genusSubfamily": dict(sorted(genus_sub.items())),
           "names": {n: v["ja"] for n, v in ja.items()}, "nameSources": {n: v["source"] for n, v in ja.items()},
           "unnamed": {n: votes.get(n, {}) for n in sorted(names) if n not in ja}},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{out}: 目 {len(orders)}・科 {len(families)}・属 {len(genera)}・亜科 {len(subfamilies)}（{len(genus_sub)} 属）・和名 {len(ja)}/{len(names)}")
print("学名のまま:", ", ".join(n for n in sorted(names) if n not in ja))
