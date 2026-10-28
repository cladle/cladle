"""ゲキムズ用の全動物データを作る：本家の data.json ＋ 魚・爬虫両生類（build_hard.py の出力）
＋ Catalogue of Life の日本語名（主に BISMaL 由来）のある無脊椎動物。
使い方: python3 merge_hard.py <本家data.json> <hard_vert.json> <colディレクトリ> <出力.json> [fixes.tsv|-] [wormsディレクトリ|-] [land.json]"""
import os, sys, json, glob, re, collections
mainj, hardj, coldir, out = sys.argv[1:5]
fixesf = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != "-" else None  # tools/hard/fixes.tsv
wormsdir = sys.argv[6] if len(sys.argv) > 6 and sys.argv[6] != "-" else None  # WoRMS（ChecklistBank 2011）の日本語名 v*.json と cls/
landf = sys.argv[7] if len(sys.argv) > 7 else None  # 陸の生き物の追加分（tools/hard/build_land.py の出力 land.json）
M = json.load(open(mainj)); H = json.load(open(hardj))
MC = {c["id"]: dict(c) for c in M["clades"]}
HC = {c["id"]: dict(c) for c in H["clades"]}
def anc(T, i):
    a = []
    while i: a.append(i); i = T[i]["parent"]
    return a
log = collections.defaultdict(list)

# ---- 1. 本家の魚・爬虫両生類を目録側の種に合わせる ----
def mspath(s): return anc(MC, s["parent"])
FH = [s for s in M["species"] if "vertebrata" in mspath(s) and not {"mammalia", "aves"} & set(mspath(s))]
HS = H["species"]
b2 = lambda x: " ".join(x.split()[:2])
bysci = collections.defaultdict(list)
for s in HS: bysci[s["sci"]].append(s); bysci[b2(s["sci"])].append(s) if b2(s["sci"]) != s["sci"] else None
# 種小名だけで引いたときは基亜種（masou masou など）を先にする
for k, v in bysci.items(): v.sort(key=lambda x: not (len(x["sci"].split()) == 3 and x["sci"].split()[1] == x["sci"].split()[2]))
# 本家に無い亜種フラグ（爬虫両生類の標準和名リストで亜種とされる名前）
SUBSP_EXTRA = {"シリケンイモリ": ["アマミシリケンイモリ", "オキナワシリケンイモリ"]}
byja = {s["ja"]: s for s in HS}
# 目録に無い（外国産の）種の置き場所： (親, 科の学名) 。科を作らないものは None
FOREIGN = {"zebrafish": ("o_cypriniformes", "Danionidae"), "axolotl": ("caudata", "Ambystomatidae"),
           "amimenishikihebi": ("serpentes", "Pythonidae"), "komodo": ("squamata", "Varanidae"),
           "kingcobra": ("sf_elapinae", None), "zougame": ("testudinoidea", "Testudinidae"),
           "iriewani": ("crocodylia", "Crocodylidae"), "alligator": ("crocodylia", "Alligatoridae")}
extra_species = []
for s in FH:
    h = (byja.get(s["ja"]) if byja.get(s["ja"]) else None) or next((x for x in bysci.get(s["sci"], []) if True), None)
    if h:
        for k in ("fact", "gbif", "sciSynonyms", "groups", "subspeciesAliases", "verify"):
            if s.get(k): h[k] = s[k]
        # 学名は本家（種で収録する方針）に合わせ、目録の表記は旧学名・別表記として残す
        if s["sci"] != h["sci"]: h["sciSynonyms"] = list(dict.fromkeys(h.get("sciSynonyms", []) + [h["sci"]])); h["sci"] = s["sci"]
        h["aliases"] = sorted(set(h["aliases"]) | set(s.get("aliases", [])) - {h["ja"]})
        if s["ja"] != h["ja"]: h["aliases"].append(s["ja"])
        h["tier"] = min(h.get("tier", 2), s.get("tier", 2)); h["main"] = s["id"]
        log["matched"].append((s["ja"], h["ja"]))
    else:
        x = dict(s); x["foreign"] = FOREIGN.get(s["id"]); extra_species.append(x)
        log["foreign"].append(s["ja"])

# ---- 2. 節目を合わせる ----
removed = {s["id"] for s in FH}
keep_main = [s for s in M["species"] if s["id"] not in removed]
C = {}
used = set()
for s in keep_main + extra_species: used.update(anc(MC, s["parent"]))
for x in extra_species:
    if x["foreign"] and x["foreign"][0] in MC: used.update(anc(MC, x["foreign"][0]))
for i in used: C[i] = dict(MC[i])
# 目録側の節目：本家にも同じ id があれば、より細かい方の親を使う
for i, c in HC.items():
    if i in C:
        hp, mp = c["parent"], C[i]["parent"]
        if hp and mp != hp:
            # 本家の親が目録の親の子孫なら本家、そうでなければ目録の親
            if not (mp in MC and hp in anc(MC, mp)): C[i]["parent"] = hp
        if c.get("polytomy") and not C[i].get("polytomy"): C[i]["polytomy"] = c["polytomy"]
    else:
        C[i] = dict(c)
# 目録の親が本家だけにある場合も含めて、親が全部あるか
for i, c in C.items():
    if c["parent"] and c["parent"] not in C: c["parent"] = MC[c["parent"]]["parent"] if c["parent"] in MC else c["parent"]

# ---- 3. 属の節目 ----
def gid(fam_or_parent, g): return "g_" + re.sub(r"[^a-z0-9]", "", g.lower()) + ("" if fam_or_parent is None else "_" + re.sub(r"[^a-z0-9]", "", fam_or_parent.lower())[:24])
def add(id, parent, ja, sci, rank, desc=""):
    if id not in C: C[id] = {"id": id, "parent": parent, "ja": ja or sci, "sci": sci, "rank": rank, "desc": desc}
    return id
GENUS_BY_NAME = collections.defaultdict(list)
for c in C.values():
    if c["rank"] == "属": GENUS_BY_NAME[c["sci"]].append(c["id"])

SP = []
for s in HS: SP.append(s)
for x in extra_species:
    if x["foreign"]:
        par, fam = x["foreign"]
        if fam: par = add("f_" + fam.lower(), par, fam, fam, "科")
        x["parent"] = par
    x.pop("foreign")
    SP.append(x)

# ---- 4. Catalogue of Life（日本語名）の無脊椎動物 ----
V = [r for f in sorted(glob.glob(coldir + "/v*.json")) for r in json.load(open(f))["result"] if re.search("[ァ-ヶ]", r["name"])]
refs = json.load(open(coldir + "/refs.json"))
U = {x["usage"]["id"]: x for f in glob.glob(coldir + "/cls/*.json") for x in json.load(open(f)).get("result", [])}
bysci_main = {s["sci"]: s for s in keep_main}; byja_all = {s["ja"]: s for s in keep_main + SP}
# 本家の節目を学名で引く（門の中だけで探す）
def desc_of(root):
    kids = collections.defaultdict(list)
    for c in C.values():
        if c["parent"]: kids[c["parent"]].append(c["id"])
    out = {}; st = [root]
    while st:
        i = st.pop(); out.setdefault(C[i]["sci"], i); st += kids[i]
    return out
PHY = {c["sci"]: c["id"] for c in C.values() if c["rank"] == "門"}
PHY_ALIAS = {}
# 本家に無い大きな群の置き場所（Catalogue of Life の分類は側系統群の「甲殻亜門」などを通るため）
PLACE = {"Copepoda": "multicrustacea", "Tantulocarida": "multicrustacea", "Ostracoda": "oligostraca", "Ichthyostraca": "oligostraca",
         "Cephalocarida": "allotriocarida", "Pycnogonida": "chelicerata", "Merostomata": "euchelicerata",
         "Polyplacophora": "aculifera", "Caudofoveata": "aculifera", "Solenogastres": "aculifera",
         "Scaphopoda": "conchifera", "Monoplacophora": "conchifera", "Cephalochordata": "chordata", "Echiura": "sedentaria",
         "Diclidophoridae": "polyopisthocotyla"}
# 本家に無くなった綱で、ゲキムズの種を入れるのに要るもの（本家の種が無くなり節目ごと外れた）
if "staurozoa" not in C and "medusozoa" in C:
    C["staurozoa"] = {"id": "staurozoa", "parent": "medusozoa", "ja": "十文字クラゲ綱", "sci": "Staurozoa", "rank": "綱", "desc": "海藻などに柄で付着して暮らすクラゲ。"}
PLACE["Stauromedusae"] = "staurozoa"
# 本家で名前を改めた群（Brabec et al. 2023：単生綱は単系統でなく、2亜綱を綱に格上げ）
SYN = {"Monopisthocotylea": "Monopisthocotyla", "Polyopisthocotylea": "Polyopisthocotyla"}
# 側系統・多系統とされる群は節目にしない（子は一つ上に付ける）
BLACK = {"Crustacea", "Polychaeta", "Canalipalpata", "Scolecida", "Littorinimorpha", "Cymothoida", "Filifera", "Anthoathecata",
         "Ascidiacea", "Phlebobranchia", "Arachnida", "Heterotremata", "Archaeogastropoda", "Mesogastropoda", "Opisthobranchia",
         "Pulmonata", "Prosobranchia", "Turbellaria", "Valvatida", "Spinulosida", "Valvatacea", "Aspidochirotida", "Lithistida",
         "Trachymedusae", "Gammaridea", "Maxillopoda", "Entomostraca", "Heterodonta", "Eumalacostraca", "Rhabdocoela", "Monogenea"}
KEEP_RANK = {"subphylum", "superclass", "class", "subclass", "infraclass", "subterclass", "superorder", "order", "suborder", "infraorder", "superfamily", "family"}
RANKJA = {"subphylum": "亜門", "superclass": "上綱", "class": "綱", "subclass": "亜綱", "infraclass": "下綱", "subterclass": "小綱",
          "superorder": "上目", "order": "目", "suborder": "亜目", "infraorder": "下目", "superfamily": "上科", "family": "科"}
cache = {}
cand = collections.defaultdict(list)
for r in V:
    u = U.get(r["taxonID"])
    if not u: continue
    n = u["usage"]["name"]
    if n.get("rank") != "species": log["col_notspecies"].append(r["name"]); continue
    cl = u.get("classification", [])
    if len(cl) < 3 or cl[1]["name"] != "Animalia": continue
    d = {c["rank"]: c["name"] for c in cl}
    if d.get("subphylum") == "Vertebrata": continue
    ja = re.sub(r"[（(].*?[）)]", "", r["name"]).strip()
    alias = []
    if "/" in ja or "／" in ja: ja, *alias = re.split("[/／]", ja)
    if not re.fullmatch(r"[ァ-ヶー・]+", ja) or re.search(r"の一種|属の|未同定|類$", ja): log["col_badname"].append(r["name"]); continue
    cand[ja].append((r, u, d, alias))
def graft(u, d, sci, skip=()):
    """Catalogue of Life の分類に沿って節目をつなぎ、属の節目の id を返す"""
    ph = PHY.get(d.get("phylum")) or PHY_ALIAS.get(d.get("phylum"))
    if not ph: return None
    if ph not in cache: cache[ph] = desc_of(ph)
    names = cache[ph]
    par = ph
    for c in u["classification"][3:]:
        if c["rank"] in ("species", "genus"): break
        nm = SYN.get(c["name"], c["name"])
        if nm in names: par = names[nm]; continue
        if nm in PLACE and PLACE[nm] in C: par = PLACE[nm]
        if nm in BLACK or nm in skip or '"' in nm or "incertae" in nm.lower() or c["rank"] not in KEEP_RANK: continue
        rid = RANKJA[c["rank"]]
        nid = ("f_" if rid == "科" else "t_") + re.sub(r"[^a-z0-9]", "", nm.lower())
        if nid in C and C[nid]["parent"] != par: nid += "_" + re.sub(r"[^a-z0-9]", "", C[par]["sci"].lower())[:16]
        if nid not in C: C[nid] = {"id": nid, "parent": par, "ja": nm, "sci": nm, "rank": rid, "desc": "", "_graft": True}
        names[nm] = nid; par = nid
    g = sci.split()[0]
    if skip and g in names and C[names[g]]["rank"] == "属":
        # WoRMS：同じ門に同名の属があればそれを使う。新しく作った科などがその属の今の親より細かければ、属をその下へ移す
        e = names[g]
        if par != C[e]["parent"]:
            if C[e]["parent"] in anc(C, par): C[e]["parent"] = par; log["worms_genus_moved"].append((g, C[par]["sci"]))
            elif par not in anc(C, e): log["worms_genus_conflict"].append((g, C[par]["sci"], C[C[e]["parent"]]["sci"]))
        return e
    gi = gid(C[par]["sci"], g)
    if gi not in C: C[gi] = {"id": gi, "parent": par, "ja": g, "sci": g, "rank": "属", "desc": ""}
    names.setdefault(g, gi)
    return gi
MAIN_GENUS = {}
for ja, lst in cand.items():
    if len({x[1]["usage"]["name"]["scientificName"] for x in lst}) > 1: log["col_dupname"].append(ja); continue
    r, u, d, alias = lst[0]
    sci = u["usage"]["name"]["scientificName"]
    sci = re.sub(r" \([A-Z][a-z]+\)", "", sci)
    if sci in bysci_main:
        m = bysci_main[sci]; gi = graft(u, d, sci)
        if gi and m["parent"] in anc(C, gi): MAIN_GENUS[m["id"]] = gi
        log["col_inmain"].append(ja); continue
    if ja in byja_all: log["col_inmain"].append(ja); continue
    gi = graft(u, d, sci)
    if not gi: log["col_nophylum"].append((d.get("phylum"), ja)); continue
    SP.append({"id": "c" + r["taxonID"].lower(), "parent": gi, "ja": ja, "sci": sci, "jaStatus": "standard", "aliases": alias,
               "fact": "", "tier": 4})
    byja_all[ja] = SP[-1]
    log["col_added"].append(ja)

# ---- 4a. WoRMS（ChecklistBank 2011）の日本語名（BISMaL 由来）で、まだ入っていない無脊椎動物 ----
# Catalogue of Life の日本語名は十脚目では短尾下目だけなので、エビ・ヤドカリ類などをここで足す
if wormsdir:
    WV = [r for f in sorted(glob.glob(wormsdir + "/v*.json")) for r in json.load(open(f))["result"] if re.search("[ァ-ヶ]", r["name"])]
    WU = {x["usage"]["id"]: x for f in glob.glob(wormsdir + "/cls/*.json") for x in json.load(open(f)).get("result", [])}
    # Catalogue of Life 側の和名（学名ごと）と、候補に挙がった和名。食い違うものは足さない
    col_ja = collections.defaultdict(set)
    for ja, lst in cand.items():
        for x in lst: col_ja[re.sub(r" \([A-Z][a-z]+\)", "", x[1]["usage"]["name"]["scientificName"])].add(ja)
    # WoRMS で既存の節目を中に含む新しい群（Pleocyemata の中の Brachyura など）は節目にしない。
    # 作ると既存の節目がその外に残り、見かけ上の側系統群になるため
    have = {c["sci"] for c in C.values() if c["rank"] != "属"}
    below = collections.defaultdict(set)
    for x in WU.values():
        nm = [c["name"] for c in x.get("classification", [])]
        for i, a in enumerate(nm): below[a].update(nm[i + 1:])
    WSKIP = {a for a, b in below.items() if a not in have and b & have}
    wcand = collections.defaultdict(list)
    for r in WV:
        u = WU.get(r["taxonID"])
        if not u or u["usage"].get("status") not in ("accepted", "provisionally accepted"): continue
        if u["usage"]["name"].get("rank") != "species": continue
        cl = u.get("classification", [])
        if len(cl) < 3 or cl[1]["name"] != "Animalia": continue
        d = {c["rank"]: c["name"] for c in cl}
        if d.get("subphylum") == "Vertebrata" or d.get("phylum") == "Chordata" and d.get("class") not in ("Ascidiacea", "Thaliacea", "Appendicularia", "Leptocardii"): continue
        ja = re.sub(r"[（(].*?[）)]", "", r["name"]).strip()
        if not re.fullmatch(r"[ァ-ヶー・]+", ja) or re.search(r"の一種|属の|未同定|類$", ja): log["worms_badname"].append(r["name"]); continue
        wcand[ja].append((r, u, d))
    sp_sci = {s["sci"] for s in SP} | {a for s in SP for a in s.get("sciSynonyms", [])}
    for ja, lst in wcand.items():
        scis = {re.sub(r" \([A-Z][a-z]+\)", "", x[1]["usage"]["name"]["scientificName"]) for x in lst}
        if len(scis) > 1: log["worms_dupname"].append(ja); continue
        r, u, d = lst[0]; sci = scis.pop()
        if ja in byja_all or sci in bysci_main or ja in cand: continue
        if col_ja.get(sci) and ja not in col_ja[sci]: log["worms_colconflict"].append((ja, sci, sorted(col_ja[sci]))); continue
        if sci in sp_sci: log["worms_dupsci"].append(ja); continue
        gi = graft(u, d, sci, WSKIP)
        if not gi: log["worms_nophylum"].append((d.get("phylum"), ja)); continue
        SP.append({"id": "w" + r["taxonID"].rsplit(":", 1)[-1], "parent": gi, "ja": ja, "sci": sci, "jaStatus": "standard", "aliases": [],
                   "fact": "", "tier": 4, "_w": True})
        byja_all[ja] = SP[-1]
        log["worms_added"].append(ja); sp_sci.add(sci)
    log["worms_skipnode"] = sorted(WSKIP & {c["name"] for l in wcand.values() for x in l for c in x[1]["classification"][3:]})

# ---- 4a0. 陸の生き物（環境省「種の多様性調査 対象種一覧」の学名を CoL に合わせたもの＋Japan Spider Catalog のクモ） ----
LD = json.load(open(landf)) if landf else {"species": [], "cladeJa": {}}
# 足す昆虫（tools/hard/insect_extra.json、insect_extra.py が作る）も陸の生き物と同じ扱いで足す
_ie = os.path.join(os.path.dirname(os.path.abspath(__file__)), "insect_extra.json")
if landf and os.path.exists(_ie):
    LD["species"] = LD["species"] + [{k: v for k, v in x.items() if k != "jaVotes"} for x in json.load(open(_ie, encoding="utf-8"))["species"]]
if landf:
    have = {c["sci"] for c in C.values() if c["rank"] != "属"}
    below = collections.defaultdict(set)
    for x in LD["species"]:
        nm = [c["name"] for c in x["classification"]]
        for i, a in enumerate(nm): below[a].update(nm[i + 1:])
    LSKIP = {a for a, b in below.items() if a not in have and b & have} | {"\0"}
    sp_sci = {s["sci"] for s in SP} | {a for s in SP for a in s.get("sciSynonyms", [])}
    before = set(C); land_ids = set()
    alias_of = {a: s["ja"] for s in keep_main + SP for a in s.get("aliases", [])}
    for x in LD["species"]:
        old = byja_all.get(x["ja"])
        # 既にある種の別名（亜種名など）と同じ和名は、その種の扱いを優先して入れない（イリオモテヤマネコなど）
        if not old and x["ja"] in alias_of: log["land_is_alias"].append((x["ja"], x["sci"], alias_of[x["ja"]])); continue
        # 別名（亜種名など）が同じ属の既にある種の和名なら、同じ生き物を別の扱いで入れていることになるので入れない
        # （本家のニホンウサギコウモリ P. sacrimontis と、それを亜種に含めたウサギコウモリ P. auritus など）
        same = [a for a in x.get("aliases", []) if a in byja_all and byja_all[a]["sci"].split()[0] == x["sci"].split()[0]]
        if same: log["land_alias_is_species"].append((x["ja"], x["sci"], same)); continue
        if x["sci"] in sp_sci or x["sci"] in bysci_main: log["land_exists"].append(x["ja"]); continue
        if old:
            # 綱が違う同名（鳥のクロサギと魚のクロサギ、チョウのヤマトシジミと貝のヤマトシジミなど）は両方入れる
            ocls = next((C[i]["sci"] for i in anc(C, old["parent"]) if C[i]["rank"] == "綱"), None)
            ncls = next((c["name"] for c in x["classification"] if c["rank"] == "class"), None)
            if old["sci"] == x["sci"] or not ocls or not ncls or ocls == ncls:
                log["land_exists" if old["sci"] == x["sci"] else "land_ja_conflict"].append((x["ja"], x["sci"], old["sci"])); continue
            log["land_homonym"].append((x["ja"], x["sci"], ncls, old["sci"], ocls))
        cl = x["classification"]
        if len(cl) < 3 or cl[1]["name"] != "Animalia" or cl[2]["rank"] != "phylum": log["land_badcl"].append(x["ja"]); continue
        gi = graft({"classification": cl}, {c["rank"]: c["name"] for c in cl}, x["sci"], LSKIP)
        if not gi: log["land_nophylum"].append((cl[2]["name"], x["ja"])); continue
        y = {"id": x["id"], "parent": gi, "ja": x["ja"], "sci": x["sci"], "jaStatus": "standard", "aliases": x.get("aliases", []),
             "fact": "", "tier": x.get("tier", 4)}
        for k in ("subspeciesAliases", "sciSynonyms", "verify"):
            if x.get(k): y[k] = x[k]
        SP.append(y); byja_all[x["ja"]] = y; sp_sci.add(x["sci"])
        log["land_added"].append((x["src"], x["ja"])); land_ids.add(y["id"])
    # 別名が他の種の和名と同じなら外す
    allja = {s["ja"] for s in SP}
    for y in SP:
        if y["id"] in land_ids and set(y["aliases"]) & allja:
            log["land_alias_drop"].append((y["ja"], sorted(set(y["aliases"]) & allja)))
            for k in ("aliases", "subspeciesAliases"):
                if k in y: y[k] = [a for a in y[k] if a not in allja]
    # 文献にある科などの和名（クモの科は Japan Spider Catalog）
    for i in set(C) - before:
        if C[i]["ja"] == C[i]["sci"] and LD["cladeJa"].get(C[i]["sci"]): C[i]["ja"] = LD["cladeJa"][C[i]["sci"]]

# ---- 4a1. 足した群が本家の節目を中に含むとき（Pleocyemata と短尾下目・コエビ下目など）、本家の節目をその下へ移す ----
# そうしないと、足した群の外に本家の節目が残り、見かけ上の側系統群になる。一番深い群から順に処理する
below_all = collections.defaultdict(set)
for x in list(U.values()) + (list(WU.values()) if wormsdir else []) + LD["species"]:
    nm = [c["name"] for c in x.get("classification", [])]
    for i, a in enumerate(nm): below_all[a].update(nm[i + 1:])
byname_c = collections.defaultdict(list)
for c in C.values(): byname_c[c["sci"]].append(c["id"])
for g in sorted([i for i, c in C.items() if c.get("_graft")], key=lambda i: -len(anc(C, i))):
    A = set(anc(C, C[g]["parent"])); Ag = set(anc(C, g))
    for nm in below_all.get(C[g]["sci"], ()):
        for x in byname_c.get(nm, []):
            if x in Ag or C[x]["rank"] == "属" or C[x]["parent"] not in A: continue
            log["regraft"].append((C[x]["sci"], C[C[x]["parent"]]["sci"], C[g]["sci"])); C[x]["parent"] = g

# ---- 4a0. 鳥と昆虫の目・科を整える（鳥：tools/hard/bird_taxa.json＝日本鳥類目録改訂第8版、osj_birds.py が作る。
#      昆虫：tools/hard/insect_taxa.json＝Catalogue of Life の並びと環境省 1997 ほかの和名、insect_taxa.py が作る） ----
# 陸の生き物で足した科は Catalogue of Life の分類から作ったので、和名が無く、目の抜けた科もある
# {"orders": {学名: {ja, under}}, "families": {学名: {ja, order, under: [上の階級の学名、下から順]}}, "genera": {属: 科}, "names": {学名: 和名}}
TAXA_GENERA = []
def fix_taxa(path, root, tag):
    if not os.path.exists(path) or root not in C: return
    BT = json.load(open(path, encoding="utf-8"))
    log[tag] = []
    def inside(i): return root in anc(C, i)
    def find(sci, rank): return next((i for i, c in C.items() if c["sci"] == sci and c["rank"] == rank and inside(i)), None)
    for a, b in BT.get("familySynonyms", {}).items():  # Catalogue of Life で今は別の名前の科（Carcinophoridae → Anisolabididae）
        for i, c in C.items():
            if c["sci"] == a and c["rank"] == "科" and inside(i): c["sci"] = b; c["ja"] = b; log[tag].append(["family_renamed", a, b])
    up = {c["sci"]: i for i, c in C.items() if c["rank"] != "属" and inside(i)}
    oid = {}
    for o, v in BT["orders"].items():
        i = find(o, "目")
        if not i:
            if v.get("under") not in up: log[tag].append(["noplace", o]); continue
            i = add("o_" + o.lower(), up[v["under"]], v["ja"], o, "目"); log[tag].append(["order", o, v["under"]])
        if C[i]["ja"] == C[i]["sci"]: C[i]["ja"] = v["ja"]
        # Catalogue of Life から作った目は綱の直下にあるので、決めた位置（より細かいまとまり）へ移す
        if v.get("under") in up and C[i]["parent"] in anc(C, up[v["under"]])[1:]:
            log[tag].append(["order_moved", o, C[C[i]["parent"]]["sci"], v["under"]]); C[i]["parent"] = up[v["under"]]
        C[i].pop("_graft", None)  # 科が一つだけの目も、片付けで畳まずに残す
        oid[o] = i
    for i, c in C.items():
        if c["rank"] == "目" and inside(i): oid.setdefault(c["sci"], i)
    fid = {}
    for f, v in BT["families"].items():
        if v["order"] not in oid: continue
        o = oid[v["order"]]
        # 置き場所：上の階級のうち、その目の中に既にある一番細かいもの（無ければ目）
        par = next((x for n in v.get("under", []) for x in [find_in(n, o)] if x), o)
        ids = [i for i, c in C.items() if c["sci"] == f and c["rank"] == "科" and inside(i)] or [add("f_" + f.lower(), par, v["ja"], f, "科")]
        for i in ids:  # 同じ科が別の id で二つできていることがある（本家の節目と陸の生き物で作った節目）
            if C[i]["ja"] == C[i]["sci"]: C[i]["ja"] = v["ja"]
            # 目の外にある科は目の下へ。目の中でも、より細かい置き場所があればそこへ
            if o not in anc(C, C[i]["parent"]) or (par != C[i]["parent"] and C[i]["parent"] in anc(C, par)):
                log[tag].append(["family", f, C[C[i]["parent"]]["sci"], C[par]["sci"]]); C[i]["parent"] = par
        fid[f] = ids[0]
    for n, j in BT.get("names", {}).items():
        for i, c in C.items():
            if c["sci"] == n and c["ja"] == c["sci"] and c["rank"] != "属" and inside(i): c["ja"] = j
    # 科を通らずに目やクレードの直下にある属は、決めた科の下へ（本家の種の属は後で作るので、そのあとにもう一度）
    def genera():
        for i, c in list(C.items()):
            if c["rank"] == "属" and inside(i) and C[c["parent"]]["rank"] != "科" and BT["genera"].get(c["sci"]) in fid:
                log[tag].append(["genus", c["sci"], C[c["parent"]]["sci"], BT["genera"][c["sci"]]]); c["parent"] = fid[BT["genera"][c["sci"]]]
        # 亜科（insect_taxa.json の genusSubfamily）：科の直下の属を、その科の中の亜科の節目の下へ
        for i, c in list(C.items()):
            sub = BT.get("genusSubfamily", {}).get(c["sci"])
            if c["rank"] != "属" or not sub or not inside(i) or C[c["parent"]]["rank"] != "科": continue
            fam = c["parent"]
            if C[fam]["sci"] != BT["subfamilies"][sub]["family"]: continue
            sid = "sf_" + re.sub(r"[^a-z0-9]", "", sub.lower())
            if sid in C and C[sid]["parent"] != fam: sid += "_" + re.sub(r"[^a-z0-9]", "", C[fam]["sci"].lower())[:16]
            if sid not in C: add(sid, fam, BT["subfamilies"][sub]["ja"], sub, "亜科")
            log[tag].append(["subfamily", c["sci"], sub]); c["parent"] = sid
    genera(); TAXA_GENERA.append(genera)
def find_in(sci, o):
    return next((i for i, c in C.items() if c["sci"] == sci and c["rank"] not in ("属", "科") and (i == o or o in anc(C, i))), None)
_here = os.path.dirname(os.path.abspath(__file__))
fix_taxa(os.path.join(_here, "bird_taxa.json"), "aves", "birds")
fix_taxa(os.path.join(_here, "insect_taxa.json"), "insecta", "insects")

# ---- 4a1. 本家に無い節目（tools/hard/hard_clades.json） ----
# [{"id","ja","sci","rank","under":親の学名,"take":[下へ入れる種・節目の学名]}]  追加種で多分岐にならないように使う
_hc = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hard_clades.json")
if os.path.exists(_hc):
    for h in json.load(open(_hc, encoding="utf-8")):
        up = [c["id"] for c in C.values() if c["sci"] == h["under"]]
        if not up: log["hard_clades"].append(["noplace", h["sci"]]); continue
        add(h["id"], up[0], h["ja"], h["sci"], h["rank"], h.get("desc", ""))
        for x in list(C.values()) + SP:
            if x["parent"] == up[0] and x["sci"] in h["take"]: x["parent"] = h["id"]
        log["hard_clades"].append(["added", h["sci"], h["under"]])

# ---- 4a2. 本家に無い個別の追加種（tools/hard/hard_only.json） ----
# [{"ja","sci","aliases","fact","tier","verify","source","place":[祖先の学名, 下から順]}]
# 同じ学名の属があればその下、無ければ place の中で最初に木にある節目の下に属を作る
_ho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hard_only.json")
if os.path.exists(_ho):
    for h in json.load(open(_ho, encoding="utf-8")):
        old = byja_all.get(h["ja"]) or next((s for s in SP if s["sci"] == h["sci"]), None)
        if old:
            if old["sci"] != h["sci"] or old["ja"] != h["ja"]: log["hard_only"].append(["conflict", h["ja"], h["sci"], old["ja"], old["sci"]]); continue
            if h.get("fact") and not old.get("fact"): old["fact"] = h["fact"]
            old["aliases"] = list(dict.fromkeys(old.get("aliases", []) + h.get("aliases", [])))
            if h.get("verify"): old["verify"] = dict(old.get("verify", {}), **h["verify"])
            old["tier"] = min(old.get("tier", 4), h.get("tier", 4))
            log["hard_only"].append(["exists", h["ja"]]); continue
        g = h["sci"].split()[0]
        byname = collections.defaultdict(list)
        for c in C.values(): byname[c["sci"]].append(c["id"])
        anc_ids = [i for nm in h["place"] for i in byname.get(nm, [])]
        gs = [i for i in byname.get(g, []) if C[i]["rank"] == "属" and (not anc_ids or set(anc(C, i)) & set(anc_ids))]
        if gs: par = gs[0]
        elif anc_ids:
            par = add(gid(C[anc_ids[0]]["sci"], g), anc_ids[0], "", g, "属")
            # 同じ属の既存の種が place の節目の直下にあれば、作った属の下へ入れる（例：シーラカンス）
            for s in SP:
                if s["parent"] == anc_ids[0] and s["sci"].split()[0] == g: s["parent"] = par
        else: log["hard_only"].append(["noplace", h["ja"], h["sci"]]); continue
        sid = "h" + re.sub(r"[^a-z0-9]", "", h["sci"].lower())
        SP.append({"id": sid, "parent": par, "ja": h["ja"], "sci": h["sci"], "jaStatus": "standard", "aliases": h.get("aliases", []),
                   "fact": h.get("fact", ""), "tier": h.get("tier", 4), **({"verify": h["verify"]} if h.get("verify") else {})})
        byja_all[h["ja"]] = SP[-1]
        log["hard_only"].append(["added", h["ja"], C[par]["sci"], C[C[par]["parent"]]["sci"]])

# 本家の種（脊椎の魚・爬虫両生以外）も属の節目の下へ
for s in keep_main:
    g = s["sci"].split()[0]
    sub = set()
    hit = MAIN_GENUS.get(s["id"])
    for gi in [] if hit else [c["id"] for c in C.values() if c["rank"] == "属" and c["sci"] == g]:
        if s["parent"] in anc(C, gi): hit = gi; break
    if not hit:
        if C[s["parent"]]["rank"] == "属": hit = s["parent"]
        else: hit = add(gid(C[s["parent"]]["sci"], g), s["parent"], "", g, "属")
    s = dict(s); s["parent"] = hit; SP.append(s)
for _g in TAXA_GENERA: _g()

for s in SP:
    if s["ja"] in SUBSP_EXTRA:
        s["subspeciesAliases"] = sorted(set(s.get("subspeciesAliases", [])) | set(SUBSP_EXTRA[s["ja"]]))
        s["aliases"] = list(dict.fromkeys(s["aliases"] + s["subspeciesAliases"]))

# ゲキムズだけの種の一言説明（tools/hard/hard_facts.tsv、学名で引く。本家の種は本家の説明が優先）
_hf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hard_facts.tsv")
if os.path.exists(_hf):
    import csv
    bysci_sp = {s["sci"]: s for s in SP}
    log["hard_facts"] = []
    for r in csv.DictReader(open(_hf, encoding="utf-8"), delimiter="\t"):
        s = bysci_sp.get(r["sci"])
        if not s or s["ja"] != r["ja"]: log["hard_facts"].append(["notfound", r["sci"], r["ja"]]); continue
        if not s.get("fact"): s["fact"] = r["fact"]; log["hard_facts"].append(["set", r["sci"]])

# ---- 4b. 照合の修正表（check/hard_inv/fixes.tsv） ----
if fixesf:
    import csv
    rows = list(csv.DictReader(open(fixesf, encoding="utf-8"), delimiter="\t"))
    log["fixes"] = []
    GENUS_FAMILY = {"Truncastoma": "Raphitomidae"}  # 移す先の属が元と別の科にあるもの（WoRMS 2026-10-24）
    for r in rows:
        hit = [s for s in SP if s["id"] == r["id"] and s["sci"] == r["sci"]]
        if not hit: log["fixes"].append(["notfound", r["id"], r["sci"]]); continue
        s, a = hit[0], r["action"]
        if a == "drop" or a == "dedup":
            for x in hit[1:] if a == "dedup" else hit: SP.remove(x)
        if a == "drop": log["fixes"].append(["drop", r["sci"]]); continue
        if a in ("ja", "dedup"):
            s["ja"] = r["new"]
            if r["keep_alias"] and r["keep_alias"] not in s["aliases"]: s["aliases"] = s["aliases"] + [r["keep_alias"]]
            s["aliases"] = [x for x in s["aliases"] if x != s["ja"]]
        r["verify_text"] = r["verify_text"].replace("。属が変わるので属の節目も付け替える", "")
        if a == "sci":
            s["sci"] = r["new"]
            s["sciSynonyms"] = s.get("sciSynonyms", []) + [r["keep_alias"] or r["sci"]]
            g = r["new"].split()[0]
            if g != C[s["parent"]]["sci"]:
                fam = C[s["parent"]]["parent"]
                if g in GENUS_FAMILY and C[fam]["sci"] != GENUS_FAMILY[g]:
                    fam = [c["id"] for c in C.values() if c["rank"] == "科" and c["sci"] == GENUS_FAMILY[g]][0]
                    r["verify_text"] += f"。属 {g} は WoRMS で {GENUS_FAMILY[g]} なので科も移した"
                gs = [c["id"] for c in C.values() if c["rank"] == "属" and c["sci"] == g and c["parent"] == fam]
                s["parent"] = gs[0] if gs else add(gid(C[fam]["sci"], g), fam, "", g, "属")
        if a == "family":
            fs = [c["id"] for c in C.values() if c["rank"] == "科" and c["sci"] == r["new"]]
            assert len(fs) == 1, r
            C[s["parent"]]["parent"] = fs[0]
        if r["verify_text"]:
            k = r["verify_key"] or {"ja": "ja", "sci": "sci", "family": "placement"}.get(a, "ja")
            s["verify"] = dict(s.get("verify", {}), **{k: r["verify_text"]})
        log["fixes"].append([a, r["sci"], r["new"]])

# ---- 4d. 知名度の上書き（tools/hard/hard_tiers.tsv：sci・ja・tier。一覧ページで作者が変えた案を表にしたもの）----
# 本家にもいる種は本家の data_more.py で変えるので、ここではゲキムズだけの種に使う。和名が違う行は使わない
_ht = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hard_tiers.tsv")
if os.path.exists(_ht):
    import csv
    bysci_sp = {s["sci"]: s for s in SP}
    log["hard_tiers"] = []
    for r in csv.DictReader(open(_ht, encoding="utf-8"), delimiter="\t"):
        s = bysci_sp.get(r["sci"])
        if not s or s["ja"] != r["ja"] or r["tier"] not in ("1", "2", "3", "4"): log["hard_tiers"].append(["skip", r["sci"], r["ja"], r["tier"]]); continue
        s["tier"] = int(r["tier"]); log["hard_tiers"].append(["set", r["sci"], r["tier"]])

# ---- 5. 片付け ----
has = set()
for s in SP:
    p = s["parent"]
    while p and p not in has: has.add(p); p = C[p]["parent"]
order = [c["id"] for c in M["clades"]] + [i for i in C if i not in MC]
clades = [C[i] for i in dict.fromkeys(order) if i in has]
ch = collections.Counter(c["parent"] for c in clades); ch.update(s["parent"] for s in SP)
alive = {c["id"]: c for c in clades}
for c in clades:
    if (c["rank"] in ("クレード", "上科", "下目") or c.get("_graft") and c["rank"] not in ("科", "属")) and ch[c["id"]] == 1 and c["parent"]:
        for d in list(alive.values()) + SP:
            if d["parent"] == c["id"]: d["parent"] = c["parent"]
        del alive[c["id"]]
clades = [c for c in clades if c["id"] in alive]
graft_par = {c["parent"] for c in clades if c.pop("_graft", False)}
NOTE = "ゲキムズでは、Catalogue of Life・WoRMS から足した群のうち、この下のどの節目に入るかを決めていないものをここに置いています。"
kids = collections.Counter(c["parent"] for c in clades if c["id"] in MC)
for c in clades:
    if c["id"] in graft_par and kids[c["id"]]:
        c["polytomy"] = (c.get("polytomy", "") + " " + NOTE).strip()
for s in SP:
    for k in ("main", "colsrc", "_w"): s.pop(k, None)
# ゲキムズだけの節目の説明（tools/hard/clade_desc.tsv：id, desc, 出典。本家と同じ節目は本家の説明のまま）
_desc = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clade_desc.tsv")
if os.path.exists(_desc):
    import csv
    alive_c = {c["id"]: c for c in clades}
    log["hard_desc"] = []
    for r in csv.DictReader(open(_desc, encoding="utf-8"), delimiter="\t"):
        c = alive_c.get(r["id"])
        if not c: log["hard_desc"].append(["notfound", r["id"]]); continue
        if r["id"] in MC: log["hard_desc"].append(["main", r["id"]]); continue
        c["desc"] = r["desc"]; log["hard_desc"].append(["set", r["id"]])
# 節目の id が前回の作り直しから変わったか（説明などを id で付けている人のため）
_ids = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache", "clade_ids.json")
_now = {c["id"]: c["sci"] for c in clades}
if os.path.exists(_ids):
    _old = json.load(open(_ids))
    log["clade_ids_removed"] = sorted((i, _old[i]) for i in set(_old) - set(_now))
    log["clade_ids_added"] = sorted((i, _now[i]) for i in set(_now) - set(_old))
    print("節目 id：消えた", len(log["clade_ids_removed"]), "増えた", len(log["clade_ids_added"]))
json.dump(_now, open(_ids, "w"), ensure_ascii=False, indent=0)
meta = json.loads(json.dumps(H["meta"]))
meta.update({"datasetVersion": "hard-0.3.0", "title": "Cladle ゲキムズ（全動物）"})
meta["selection"] = dict(M["meta"]["selection"], **{"maxGuesses": 20, "tierWeights": {"1": 1, "2": 0.6, "3": 0.3, "4": 0.1}, "clearRank": "属", "dailyEpoch": H["meta"]["selection"]["dailyEpoch"]})
meta["selection"].pop("bucketRank", None)
meta["counts"] = {"main": len(keep_main) + len(log["matched"]) + len(log["foreign"]), "fishherp": len(HS), "col": len(log["col_added"]),
                  "worms": len(log.get("worms_added", [])), "land": len(log.get("land_added", [])), "extra": len([x for x in log.get("hard_only", []) if x[0] == "added"])}
meta["status"] = "試作版。本家の収録種に、標準和名のある日本産の魚類・爬虫類・両生類と、Catalogue of Life に日本語名（主に BISMaL 由来）がある無脊椎動物を加えた。Catalogue of Life 由来の種は、和名を日本産ワラジムシ亜目種リスト・日本近海産タナイス目リストと、学名と科を WoRMS と照合した（2026-10-24、check/hard_inv/）。ほかの和名は BISMaL のみが出典で、iNaturalist・Wikidata と食い違うものに要確認の印を付けた。"
if wormsdir:
    meta["status"] += "エビ・ヤドカリ類など Catalogue of Life に日本語名の無い無脊椎動物は、WoRMS の日本語名（BISMaL 由来）から足した。Catalogue of Life と和名が食い違うものと、一つの和名に学名が複数あるものは入れていない（2026-10-25）。"
meta["japaneseNameSources"] = M["meta"]["japaneseNameSources"] + ["Catalogue of Life Checklist（ChecklistBank 3LR, 2026-10-14版）の日本語名（主に BISMaL 由来）"]
if landf:
    meta["japaneseNameSources"] += ["環境省自然環境局生物多様性センター「種の多様性調査（動物分布調査）対象種一覧」（1997、公共データ利用規約 PDL1.0）を使用し、学名を Catalogue of Life に合わせて Cladle が加工",
                                    "Japan Spider Catalog. (2026). Japan Spider Catalog（種リスト 2026-10-24 生成分）. https://japan-spider-catalog.pages.dev/ (accessed 2026-10-25). Cladle が加工"]
    meta["status"] += "陸の昆虫・クモ・鳥・哺乳類・陸と淡水の貝は、環境省の種の多様性調査の対象種一覧（学名は Catalogue of Life に合わせた）と Japan Spider Catalog から足した（2026-10-25）。鳥と哺乳類はそのうち日本鳥類目録第8版・世界哺乳類標準和名リストにある種だけを、そのリストの和名で入れた。"
if os.path.exists(os.path.join(_here, "bird_taxa.json")):
    meta["japaneseNameSources"].append("日本鳥学会（2024）日本鳥類目録改訂第8版 掲載鳥類リスト ver.1（2024-10-08公開）。鳥の目・科・属の並びと和名、ゲキムズだけの鳥の和名・学名（Cladle が加工）")
if os.path.exists(os.path.join(_here, "insect_taxa.json")):
    meta["japaneseNameSources"].append("昆虫の目・科・亜科の和名：環境省（1997）種の多様性調査（動物分布調査）対象種一覧（PDL1.0）、無ければ Wikidata・GBIF・iNaturalist のうち 2 つ以上でそろう名前（Cladle が照合、そろわないものは学名のまま）。並びと亜科は Catalogue of Life、目より上は Misof et al. 2014")
if os.path.exists(_ie):
    meta["japaneseNameSources"].append("足した昆虫（環境省の一覧で学名が合わなかった種と、iNaturalist の日本の研究用観察数の上位 300 種）の和名：iNaturalist・Wikidata・GBIF（環境省の種は環境省の和名も）のうち 2 つ以上でそろう名前。学名は Catalogue of Life、無ければ GBIF Backbone（Cladle が照合）")
    meta["status"] += "身近な昆虫（iNaturalist の日本の観察数の上位）と、環境省の一覧で学名が合わずに落ちていた昆虫を足した（2026-10-28）。"
if wormsdir: meta["japaneseNameSources"].append("World Register of Marine Species（ChecklistBank 2011, CC BY 4.0）の日本語名（BISMaL 由来）")
# 照合できなかった昆虫（コガネムシ上科）の和名の出典論文（fixes.tsv と同じフォルダの insects_refs.tsv）
refsf = fixesf and os.path.join(os.path.dirname(fixesf), "insects_refs.tsv")
if refsf and os.path.exists(refsf):
    import csv
    ids = {x["id"] for x in SP}
    refs = [r["source"] for r in csv.DictReader(open(refsf, encoding="utf-8"), delimiter="\t") if r["id"] in ids]
    meta["japaneseNameSources"] += ["コガネムシ上科の和名（日本産昆虫目録とは未照合）：" + "／".join(dict.fromkeys(refs))]
json.dump({"meta": meta, "clades": clades, "species": SP}, open(out, "w"), ensure_ascii=False, separators=(",", ":"))
print({k: len(v) for k, v in log.items()})
print("clades", len(clades), "species", len(SP), "ja dup", [k for k, v in collections.Counter(s["ja"] for s in SP).items() if v > 1][:20])
json.dump({k: v for k, v in log.items()}, open(out + ".log.json", "w"), ensure_ascii=False, indent=0)
