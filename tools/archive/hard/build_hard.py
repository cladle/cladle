"""ゲキムズ用データ（魚類＋爬虫両生類、日本産・標準和名のある種）を作る。
使い方: python3 build_hard.py <JAFList.xlsx> <herp.json> <本番data.json> <出力.json>
魚：本村（2026）日本産魚類全種目録 ver.42 の目・科・亜科・属（属は学名の最初の語）。
爬虫両生類：日本爬虫両棲類学会 標準和名リスト（2026-07-02版）の目・科・亜科・属。
目より上は分子系統の主な節目だけ置き、順の決まらないところは多分岐にする。"""
import sys, json, re, collections, openpyxl

xlsx, herpj, mainj, out = sys.argv[1:5]
MAIN = {c["id"]: c for c in json.load(open(mainj))["clades"]}

C = {}       # id -> clade
order = []
def clade(id, parent, ja, sci, rank, desc="", poly=None):
    if id in C: return id
    m = MAIN.get(id)
    c = {"id": id, "parent": parent, "ja": ja or (m and m["ja"]) or sci, "sci": sci, "rank": rank,
         "desc": desc or (m["desc"] if m and m["parent"] is not None else "")}
    if poly: c["polytomy"] = poly
    C[id] = c; order.append(id); return id

P_GEN = "この中の分かれる順は研究によって結果が分かれるため、ここでは決めずに並べています。"
# ---- 目より上の骨格 ----
clade("vertebrata", None, "脊椎動物亜門", "Vertebrata", "亜門")
clade("cyclostomata", "vertebrata", "円口類", "Cyclostomata", "クレード")
clade("gnathostomata", "vertebrata", "顎口類", "Gnathostomata", "クレード")
clade("chondrichthyes", "gnathostomata", "軟骨魚綱", "Chondrichthyes", "綱")
clade("holocephali", "chondrichthyes", "全頭亜綱", "Holocephali", "亜綱")
clade("elasmobranchii", "chondrichthyes", "板鰓亜綱", "Elasmobranchii", "亜綱")
clade("selachii", "elasmobranchii", "サメ類", "Selachii", "クレード")
clade("galeomorphii", "selachii", "Galeomorphii", "Galeomorphii", "クレード")
clade("squalomorphii", "selachii", "Squalomorphii", "Squalomorphii", "クレード")
clade("batoidea", "elasmobranchii", "エイ類", "Batoidea", "クレード", poly=P_GEN)
clade("osteichthyes", "gnathostomata", "Osteichthyes", "Osteichthyes", "クレード")
clade("actinopterygii", "osteichthyes", "条鰭綱", "Actinopterygii", "綱")
clade("neopterygii", "actinopterygii", "Neopterygii", "Neopterygii", "クレード")
clade("teleostei", "neopterygii", "真骨類", "Teleostei", "クレード")
clade("elopomorpha", "teleostei", "Elopomorpha", "Elopomorpha", "クレード", poly=P_GEN)
clade("clupeocephala", "teleostei", "Clupeocephala", "Clupeocephala", "クレード")
clade("otomorpha", "clupeocephala", "Otomorpha", "Otomorpha", "クレード", poly=P_GEN)
clade("ostariophysi", "otomorpha", "骨鰾類", "Ostariophysi", "上目")
clade("otophysi", "ostariophysi", "Otophysi", "Otophysi", "クレード")
clade("euteleostei", "clupeocephala", "正真骨類", "Euteleostei", "クレード", poly=P_GEN)
clade("stomiatii", "euteleostei", "Stomiatii", "Stomiatii", "クレード")
clade("neoteleostei", "euteleostei", "Neoteleostei", "Neoteleostei", "クレード")
clade("eurypterygii", "neoteleostei", "Eurypterygii", "Eurypterygii", "クレード")
clade("ctenosquamata", "eurypterygii", "Ctenosquamata", "Ctenosquamata", "クレード")
clade("acanthomorpha", "ctenosquamata", "Acanthomorpha", "Acanthomorpha", "クレード", poly=P_GEN)
clade("acanthopterygii", "acanthomorpha", "Acanthopterygii", "Acanthopterygii", "クレード", poly=P_GEN)
clade("percomorpha", "acanthopterygii", "スズキ系", "Percomorpha", "クレード", poly="スズキ系の中の大きなまとまり（シリーズ）どうしの分かれる順は研究によって結果が分かれるため、ここでは決めずに並べています。")
clade("anabantaria", "percomorpha", "Anabantaria", "Anabantaria", "クレード")
clade("ovalentaria", "percomorpha", "Ovalentaria", "Ovalentaria", "クレード", poly=P_GEN)
clade("atherinomorpha", "ovalentaria", "Atherinomorpha", "Atherinomorpha", "クレード", poly=P_GEN)
clade("eupercaria", "percomorpha", "Eupercaria", "Eupercaria", "クレード", poly=P_GEN)
clade("tetrapoda", "osteichthyes", "四肢動物", "Tetrapoda", "クレード")
clade("amphibia", "tetrapoda", "両生綱", "Amphibia", "綱")
clade("sauropsida", "tetrapoda", "Sauropsida", "Sauropsida", "クレード")
clade("testudines", "sauropsida", "カメ目", "Testudines", "目")
clade("durocryptodira", "testudines", "Durocryptodira", "Durocryptodira", "クレード", poly=P_GEN)
clade("chelonioidea", "durocryptodira", "Chelonioidea", "Chelonioidea", "上科")
clade("testudinoidea", "durocryptodira", "Testudinoidea", "Testudinoidea", "上科")
clade("squamata", "sauropsida", "有鱗目", "Squamata", "目", poly="有鱗目の中の大きなまとまりどうしの分かれる順は、遺伝子による研究と形による研究で結果が食い違うため、ここでは決めずに並べています。トカゲ亜目はヘビを含まない側系統群なので節目にしていません。")
clade("gekkota", "squamata", "Gekkota", "Gekkota", "下目")
clade("iguania", "squamata", "Iguania", "Iguania", "下目")
clade("serpentes", "squamata", "ヘビ亜目", "Serpentes", "亜目")
clade("colubroidea", "serpentes", "Colubroidea", "Colubroidea", "上科", poly=P_GEN)

ORDER_PARENT = {
 "Myxiniformes": "cyclostomata", "Petromyzontiformes": "cyclostomata",
 "Chimaeriformes": "holocephali",
 "Heterodontiformes": "galeomorphii", "Orectolobiformes": "galeomorphii", "Lamniformes": "galeomorphii", "Carcharhiniformes": "galeomorphii",
 "Hexanchiformes": "squalomorphii", "Squaliformes": "squalomorphii", "Echinorhiniformes": "squalomorphii", "Pristiophoriformes": "squalomorphii", "Squatiniformes": "squalomorphii",
 "Torpediniformes": "batoidea", "Rhinopristiformes": "batoidea", "Rajiformes": "batoidea", "Myliobatiformes": "batoidea",
 "Acipenseriformes": "actinopterygii", "Lepisosteiformes": "neopterygii",
 "Elopiformes": "elopomorpha", "Albuliformes": "elopomorpha", "Notacanthiformes": "elopomorpha", "Anguilliformes": "elopomorpha",
 "Clupeiformes": "otomorpha", "Alepocephaliformes": "otomorpha", "Gonorynchiformes": "ostariophysi", "Cypriniformes": "otophysi", "Siluriformes": "otophysi",
 "Argentiniformes": "euteleostei", "Salmoniformes": "euteleostei", "Osmeriformes": "stomiatii", "Stomiiformes": "stomiatii",
 "Ateleopodiformes": "neoteleostei", "Aulopiformes": "eurypterygii", "Myctophiformes": "ctenosquamata",
 "Lampriformes": "acanthomorpha", "Polymixiiformes": "acanthomorpha", "Zeiformes": "acanthomorpha", "Gadiformes": "acanthomorpha",
 "Trachichthyiformes": "acanthopterygii", "Beryciformes": "acanthopterygii",
 "Ophidiiformes": "percomorpha", "Gobiiformes": "percomorpha", "Syngnathiformes": "percomorpha", "Scombriformes": "percomorpha", "Carangiformes": "percomorpha",
 "Synbranchiformes": "anabantaria", "Anabantiformes": "anabantaria",
 "Atheriniformes": "atherinomorpha", "Beloniformes": "atherinomorpha", "Cyprinodontiformes": "atherinomorpha",
 "Cichliformes": "ovalentaria", "Mugiliformes": "ovalentaria", "Blenniiformes": "ovalentaria",
 "Perciformes": "eupercaria", "Centrarchiformes": "eupercaria", "Labriformes": "eupercaria", "Acropomatiformes": "eupercaria",
 "Acanthuriformes": "eupercaria", "Lophiiformes": "eupercaria", "Tetraodontiformes": "eupercaria",
 "Caudata": "amphibia", "Anura": "amphibia",
}
FAMILY_PARENT = {  # 爬虫類の科（リストの亜目・トカゲ亜目は使わない）
 "Cheloniidae": "chelonioidea", "Dermochelyidae": "chelonioidea", "Geoemydidae": "testudinoidea", "Emydidae": "testudinoidea",
 "Chelydridae": "durocryptodira", "Trionychidae": "testudines",
 "Eublepharidae": "gekkota", "Gekkonidae": "gekkota", "Agamidae": "iguania", "Iguanidae": "iguania",
 "Scincidae": "squamata", "Lacertidae": "squamata",
 "Typhlopidae": "serpentes", "Pareidae": "colubroidea", "Xenodermidae": "colubroidea", "Colubridae": "colubroidea", "Elapidae": "colubroidea", "Viperidae": "colubroidea",
}
def cid(prefix, sci): return prefix + re.sub(r"[^a-z0-9]", "", sci.lower())

SPECIES = []
def species(gid, ja, sci, tier, src, aliases=()):
    # 目録で「サクラマス・ヤマメ」のように二つ並ぶ名前は、最初を和名、残りを別名にする
    ja, *more = ja.split("・"); aliases = list(aliases) + more
    SPECIES.append({"id": "s%d" % (len(SPECIES) + 1), "parent": gid, "ja": ja, "sci": sci, "jaStatus": "standard",
                    "aliases": list(aliases), "fact": "", "tier": tier, "src": src})

GENUS_HOME = {}
def genus(parent, sci, ja=""):
    gid = cid("g_", sci)
    if gid in C and C[gid]["parent"] != parent:
        raise SystemExit(f"属 {sci} が2つの場所にある: {C[gid]['parent']} / {parent}")
    return clade(gid, parent, ja or sci, sci, "属")

def sciname(raw):
    """目録の学名欄から著者名を除き、属名＋種小名（未記載種は sp. 以下）にする。亜属は省く"""
    t = raw.split("\n")[0].strip()
    t = re.sub(r"^(\S+) \([A-Z][a-z]+\) ", r"\1 ", t)
    w = t.split()
    if len(w) > 3 and w[2] == "subsp.":  # 未記載亜種（Carassius buergeri subsp. 1 など）
        return " ".join(w[:4])
    if w[1] not in ("sp.", "cf."):  # 亜種があれば三名
        return " ".join(w[:3] if len(w) > 2 and re.fullmatch(r"[a-z]+", w[2]) and w[2] not in ("de", "van", "von", "da", "du", "le", "la") else w[:2])
    t = re.sub(r"\s*\([^)]*\d{4}\)", "", t)
    t = re.sub(r"\s+[A-Z][^\s,&]*(?:[ ,&]+[A-Z][^\s,&]*)*\s+\d{4}$", "", t)
    return t

# ---- 魚 ----
ws = openpyxl.load_workbook(xlsx, read_only=True).worksheets[0]
skipped = collections.Counter()
for i, r in enumerate(ws.iter_rows(values_only=True)):
    if i == 0: continue
    o_ja, o_sci = r[2].split("\n")
    fam_ja = r[3].split("\n"); fam_sci = r[4].split("\n")
    ja, sci = r[5].strip(), r[6].strip()
    if ja == "和名なし": skipped["fish_noname"] += 1; continue
    oid = clade(cid("o_", o_sci), ORDER_PARENT[o_sci], o_ja.strip(), o_sci.strip(), "目")
    fid = clade(cid("f_", fam_sci[0]), oid, fam_ja[0].strip(), fam_sci[0].strip(), "科")
    p = fid
    if len(fam_sci) > 1 and fam_sci[1].strip():
        sj = fam_ja[1].strip() if len(fam_ja) > 1 else ""
        if not re.search(r"[ぁ-んァ-ヶ一-龠]", sj): sj = fam_sci[1].strip()
        p = clade(cid("sf_", fam_sci[1]), fid, sj, fam_sci[1].strip(), "亜科")
    if re.search(r"の一種|の1種|未同定|近似種", ja): skipped["fish_notname"] += 1; continue
    name = sciname(sci); gsci = name.split()[0]
    gid = genus(p, gsci)
    refs = len([x for x in (r[7] or "").split("；") if x.strip()])
    tier = 1 if refs >= 20 else 2 if refs >= 12 else 3 if refs >= 4 else 4
    species(gid, ja, name, tier, "fish")

# ---- 爬虫両生類 ----
H = json.load(open(herpj))
stack = {}
for x in H:
    rk = x["rank"]; stack[rk] = x
    for lower in ("order", "suborder", "family", "subfamily", "genus", "species"):
        if ["class", "order", "suborder", "family", "subfamily", "genus", "species", "subspecies"].index(lower) > \
           ["class", "order", "suborder", "family", "subfamily", "genus", "species", "subspecies"].index(rk):
            stack.pop(lower, None)
    if rk == "order" and x["sci"] in ORDER_PARENT:
        clade(cid("o_", x["sci"]) if x["sci"] not in ("Caudata", "Anura") else x["sci"].lower(), ORDER_PARENT[x["sci"]], x["ja"], x["sci"], "目")
    elif rk == "family":
        o = stack["order"]["sci"]
        par = FAMILY_PARENT.get(x["sci"]) or (o.lower() if o in ("Caudata", "Anura") else None)
        if par: clade(cid("f_", x["sci"]), par, x["ja"], x["sci"], "科")
    elif rk == "subfamily":
        clade(cid("sf_", x["sci"]), cid("f_", stack["family"]["sci"]), x["ja"], x["sci"], "亜科")
    elif rk == "genus":
        p = cid("sf_", stack["subfamily"]["sci"]) if "subfamily" in stack else cid("f_", stack["family"]["sci"])
        if p in C: genus(p, x["sci"], x["ja"])
    elif rk == "species":
        g = cid("g_", stack["genus"]["sci"])
        if g not in C: skipped["herp_nogenus"] += 1; continue
        if not x["ja"]: skipped["herp_noname"] += 1; continue
        if x.get("flag"): skipped["herp_" + x["flag"]] += 1; continue
        species(g, x["ja"], x["sci"], 2, "herp")
    elif rk == "subspecies" and x["ja"] and SPECIES and SPECIES[-1]["src"] == "herp" and x["sci"].startswith(SPECIES[-1]["sci"] + " "):
        if x["ja"] != SPECIES[-1]["ja"]: SPECIES[-1]["aliases"].append(x["ja"])

# 和名の重複（同じ和名が2種）を検査
dup = [k for k, v in collections.Counter(s["ja"] for s in SPECIES).items() if v > 1]
# 空のクレードを落とし、種のいない枝を除く
kids = collections.defaultdict(list)
for c in C.values():
    if c["parent"]: kids[c["parent"]].append(c["id"])
has = set()
for s in SPECIES:
    p = s["parent"]
    while p and p not in has: has.add(p); p = C[p]["parent"]
clades = [C[i] for i in order if i in has]
# 子が1つしかない階級なしのクレードは省く（共通祖先として出てこないため）
ch = collections.Counter(c["parent"] for c in clades)
for s in SPECIES: ch[s["parent"]] += 1
alive = {c["id"]: c for c in clades}
for c in list(clades):
    if c["rank"] in ("クレード", "上科", "下目") and ch[c["id"]] == 1 and c["parent"]:
        for d in list(alive.values()) + SPECIES:
            if d["parent"] == c["id"]: d["parent"] = c["parent"]
        del alive[c["id"]]
clades = [c for c in clades if c["id"] in alive]
for c in clades:
    if c.get("polytomy"):
        n = sum(1 for d in clades if d["parent"] == c["id"]) + sum(1 for s in SPECIES if s["parent"] == c["id"])
        if n < 3: del c["polytomy"]
for s in SPECIES: s.pop("src")
meta = {
 "schemaVersion": 1, "datasetVersion": "hard-0.1.0", "title": "Cladle ゲキムズ 日本の魚類・爬虫類・両生類",
 "referenceDate": "2026-10-24",
 "taxonomy": {
  "backbone": "目より上は分子系統の論文に基づく主な節目だけを置き、分かれる順が定まらないところは多分岐にした。魚類の目・科は日本産魚類全種目録（Catalog of Fishes の体系）、爬虫両生類の目・科・属は日本産爬虫両生類標準和名リストに従う。",
  "nomenclature": "魚類：本村浩之（2026）日本産魚類全種目録 Online ver. 42（2026-08-27）。爬虫両生類：日本爬虫両棲類学会（2026）日本産爬虫両生類標準和名リスト（2026年7月2日版）",
  "phylogenyNotes": "属は魚類では学名の属名（和名の属名は付けていない）。トカゲ亜目（ヘビを含まない側系統群）は節目にしていない。",
  "nonMonophyleticGroupsExcluded": ["魚類", "爬虫類（鳥類を除く）", "トカゲ亜目"]},
 "japaneseNameSources": ["本村浩之（2026）日本産魚類全種目録 Online ver. 42", "日本爬虫両棲類学会（2026）日本産爬虫両生類標準和名リスト（2026年7月2日版）"],
 "status": "試作版。標準和名のある日本産の種だけを収録（和名のない種、未確定の和名案は除く）。",
 "licenseNotes": "魚類目録は「利用は自由ですが，できればご一報ください」、爬虫両生類リストは「典拠等を示すことなく自由に使用することができます」とある。",
 "selection": {"maxGuesses": 20, "dailyEpoch": "2026-10-25", "bucketRank": "目",
   "buckets": ["chondrichthyes", "actinopterygii", "amphibia", "sauropsida"], "otherBucketLabel": "円口類",
   "phylumWeight": "sqrt", "bucketWeight": "sqrt", "tierWeights": {"1": 1, "2": 0.6, "3": 0.3, "4": 0.1},
   "clearRank": "属"},
}
json.dump({"meta": meta, "clades": clades, "species": SPECIES}, open(out, "w"), ensure_ascii=False, separators=(",", ":"))
print("clades", len(clades), "species", len(SPECIES), "skipped", dict(skipped), "dup", dup[:20], len(dup))
print(collections.Counter(c["rank"] for c in clades))
print(collections.Counter(s["tier"] for s in SPECIES))
