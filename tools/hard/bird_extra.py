# -*- coding: utf-8 -*-
"""鳥編・ゲキムズに足す外国の鳥の候補（目ごと）を集めて照合する。

  python3 tools/hard/bird_extra.py data-hard.json <取得結果を置くフォルダ> <出力 json>

- 目は世界の鳥の 44 目（目ごとの世界の種数は下の BOOK）。目ごとに、iNaturalist の世界の研究用観察数の多い順に種を見て、
  世界の種数の 5%（少なくとも 2 種、その目の種数まで）に届くまで足す。今ある種も数に入れる。
- 北アメリカの観察が多い iNaturalist の偏りを和らげるため、日本語版ウィキペディアに記事のある種を先に選ぶ
  （記事のある種だけで 2 種に届かない目は、記事の無い種でも足す）。
- 学名：Catalogue of Life（ChecklistBank 3LR）で accepted な種だけ。
- 和名：iNaturalist・Wikidata・GBIF のうち 2 つ以上でそろい、ほかの名前と同数で並ばないものだけ。
- 取得結果は取得結果フォルダに 1 件ずつためて、2 回目からはそれを使う（外部の API に何度も問い合わせない）。
"""
import json, os, re, sys, time, urllib.parse, urllib.request

src, cache, out = sys.argv[1:4]
os.makedirs(cache, exist_ok=True)
RATE = 0.05
# 目（学名, 和名, 世界の種数, iNaturalist で引く分類群）。種数は図「鳥の目の種数」（文：西海功）による
BOOK = [("Struthioniformes", "ダチョウ目", 2, ["Struthionidae"]), ("Rheiformes", "レア目", 2, ["Rheidae"]),
        ("Apterygiformes", "キーウィ目", 5, ["Apterygidae"]), ("Casuariiformes", "ヒクイドリ目", 4, ["Casuariidae", "Dromaiidae"]),
        ("Tinamiformes", "シギダチョウ目", 46, ["Tinamidae"]), ("Anseriformes", "カモ目", 178, ["Anseriformes"]),
        ("Galliformes", "キジ目", 308, ["Galliformes"]), ("Caprimulgiformes", "ヨタカ目", 97, ["Caprimulgidae"]),
        ("Steatornithiformes", "アブラヨタカ目", 1, ["Steatornithidae"]), ("Nyctibiiformes", "タチヨタカ目", 7, ["Nyctibiidae"]),
        ("Podargiformes", "ガマグチヨタカ目", 16, ["Podargidae"]), ("Aegotheliformes", "ズクヨタカ目", 9, ["Aegothelidae"]),
        ("Apodiformes", "アマツバメ目", 483, ["Apodidae", "Hemiprocnidae", "Trochilidae"]), ("Musophagiformes", "エボシドリ目", 23, ["Musophagidae"]),
        ("Otidiformes", "ノガン目", 26, ["Otididae"]), ("Cuculiformes", "カッコウ目", 150, ["Cuculidae"]),
        ("Mesitornithiformes", "クイナモドキ目", 3, ["Mesitornithidae"]), ("Pterocliformes", "サケイ目", 16, ["Pteroclidae"]),
        ("Columbiformes", "ハト目", 352, ["Columbidae"]), ("Gruiformes", "ツル目", 189, ["Gruiformes"]),
        ("Podicipediformes", "カイツブリ目", 23, ["Podicipedidae"]), ("Phoenicopteriformes", "フラミンゴ目", 6, ["Phoenicopteridae"]),
        ("Charadriiformes", "チドリ目", 391, ["Charadriiformes"]), ("Eurypygiformes", "ジャノメドリ目", 2, ["Eurypygidae", "Rhynochetidae"]),
        ("Phaethontiformes", "ネッタイチョウ目", 3, ["Phaethontidae"]), ("Gaviiformes", "アビ目", 5, ["Gaviidae"]),
        ("Sphenisciformes", "ペンギン目", 18, ["Spheniscidae"]), ("Procellariiformes", "ミズナギドリ目", 149, ["Procellariiformes"]),
        ("Ciconiiformes", "コウノトリ目", 20, ["Ciconiidae"]), ("Suliformes", "カツオドリ目", 61, ["Suliformes"]),
        ("Pelecaniformes", "ペリカン目", 120, ["Pelecanidae", "Ardeidae", "Threskiornithidae", "Scopidae", "Balaenicipitidae"]),
        ("Opisthocomiformes", "ツメバケイ目", 1, ["Opisthocomidae"]), ("Accipitriformes", "タカ目", 265, ["Accipitriformes"]),
        ("Strigiformes", "フクロウ目", 254, ["Strigiformes"]), ("Coliiformes", "ネズミドリ目", 6, ["Coliidae"]),
        ("Leptosomiformes", "オオブッポウソウ目", 1, ["Leptosomidae"]), ("Trogoniformes", "キヌバネドリ目", 46, ["Trogonidae"]),
        ("Bucerotiformes", "サイチョウ目", 77, ["Bucerotiformes"]), ("Coraciiformes", "ブッポウソウ目", 186, ["Coraciiformes"]),
        ("Piciformes", "キツツキ目", 449, ["Piciformes"]), ("Cariamiformes", "ノガンモドキ目", 2, ["Cariamidae"]),
        ("Falconiformes", "ハヤブサ目", 65, ["Falconidae"]), ("Psittaciformes", "インコ目", 408, ["Psittaciformes"]),
        ("Passeriformes", "スズメ目", 6719, ["Passeriformes"])]

def get(u):
    for i in range(4):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "cladle-name-check/0.1 (educational)"})
            return json.load(urllib.request.urlopen(req, timeout=60))
        except Exception: time.sleep(3 * (i + 1))
class Cache:
    def __init__(self, name): self.p = os.path.join(cache, name); self.d = json.load(open(self.p, encoding="utf-8")) if os.path.exists(self.p) else {}
    def __call__(self, key, fn, wait):
        if key not in self.d:
            self.d[key] = fn(); time.sleep(wait)
            json.dump(self.d, open(self.p, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        return self.d[key]
TX, TOP, COL, GB, GBV, WD, JW = (Cache(n) for n in ("inat_taxon.json", "inat_top.json", "col.json", "gbif.json", "gbif_vern.json", "wikidata.json", "jawiki.json"))

def inat_taxon(name):
    def f():
        for t in (get("https://api.inaturalist.org/v1/taxa?" + urllib.parse.urlencode({"q": name, "is_active": "true", "per_page": 10})) or {}).get("results", []):
            if t["name"] == name: return t["id"]
    return TX(name, f, 1)
def inat_top(tid, n):
    def f():
        d = get("https://api.inaturalist.org/v1/observations/species_counts?" + urllib.parse.urlencode(
            {"taxon_id": tid, "quality_grade": "research", "locale": "ja", "per_page": n})) or {"results": []}
        return [{"sci": r["taxon"]["name"], "ja": r["taxon"].get("preferred_common_name"), "n": r["count"]} for r in d["results"] if r["taxon"]["rank"] == "species"]
    return TOP(f"{tid}:{n}", f, 1.5)
def col(name):
    def f():
        u = (get("https://api.checklistbank.org/dataset/3LR/match/nameusage?" + urllib.parse.urlencode({"q": name})) or {}).get("usage") or {}
        return {"rank": u.get("rank"), "status": u.get("status"), "name": u.get("name"),
                "cl": {c["rank"]: c["name"] for c in u.get("classification", [])}}
    return COL(name, f, 0.4)
def gbif_ja(name):
    def f():
        m = get("https://api.gbif.org/v1/species/match?" + urllib.parse.urlencode({"name": name, "kingdom": "Animalia"})) or {}
        if m.get("rank") != "SPECIES" or m.get("synonym"): return []
        v = get(f"https://api.gbif.org/v1/species/{m['usageKey']}/vernacularNames?limit=200") or {}
        return sorted({y["vernacularName"] for y in v.get("results", []) if y.get("language") == "jpn"})
    return GBV(name, f, 0.6)
def wd(name):
    def f():
        q = 'SELECT ?l WHERE { ?i wdt:P225 "%s" ; rdfs:label ?l FILTER(lang(?l)="ja") }' % name
        d = get("https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": q, "format": "json"})) or {"results": {"bindings": []}}
        return sorted({b["l"]["value"] for b in d["results"]["bindings"]})
    return WD(name, f, 0.5)

def jawiki(name):
    def f():
        q = 'SELECT ?a WHERE { ?i wdt:P225 "%s" . ?a schema:about ?i ; schema:isPartOf <https://ja.wikipedia.org/> }' % name
        d = get("https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": q, "format": "json"})) or {"results": {"bindings": []}}
        return bool(d["results"]["bindings"])
    return JW(name, f, 1)

H = json.load(open(src, encoding="utf-8"))
HC = {c["id"]: c for c in H["clades"]}
def order_of(pid):
    while pid:
        if HC[pid]["rank"] == "目": return HC[pid]["sci"]
        pid = HC[pid]["parent"]
have, have_ja, n_have = set(), set(), {}
for s in H["species"]:
    have.add(s["sci"]); have_ja.add(s["ja"]); have_ja.update(s.get("aliases", [])); have.update(s.get("sciSynonyms", []))
    o = order_of(s["parent"])
    if o: n_have[o] = n_have.get(o, 0) + 1
# 目の節目が無い種（ダチョウ・エミューなど）は科で数える
fam2order = {}
res, skip = [], []
for osci, oja, world, taxa in BOOK:
    target = min(world, max(2, round(world * RATE)))
    cur = n_have.get(osci, 0)
    cands = []
    for t in taxa:
        tid = inat_taxon(t)
        if tid: cands += inat_top(tid, 200 if world > 100 else 50)
    cands.sort(key=lambda x: -x["n"])
    cands = [x for x in cands if x["sci"] not in have][:max(30, (target - cur) * 4)]
    for x in [x for x in cands if jawiki(x["sci"])] + [x for x in cands if not jawiki(x["sci"])]:
        if x["sci"] in have: continue
        if cur >= target or (cur >= min(world, 2) and not jawiki(x["sci"])): break
        c = col(x["sci"])
        if c["rank"] != "species" or c["status"] not in ("accepted", "provisionally accepted") or c["name"] != x["sci"]:
            skip.append([osci, x["sci"], x["ja"], "col_" + str(c["status"])]); continue
        votes = {}
        for who, names in (("iNaturalist", [x["ja"]]), ("Wikidata", wd(x["sci"])), ("GBIF", gbif_ja(x["sci"]))):
            for nm in names:
                if nm and re.fullmatch(r"[ァ-ヶー]+", nm): votes.setdefault(nm, set()).add(who)
        best = sorted(votes.items(), key=lambda kv: -len(kv[1]))
        if not best or len(best[0][1]) < 2 or (len(best) > 1 and len(best[1][1]) == len(best[0][1])):
            skip.append([osci, x["sci"], x["ja"], "ja_not_agreed", {k: sorted(v) for k, v in votes.items()}]); continue
        ja = best[0][0]
        if ja in have_ja: skip.append([osci, x["sci"], ja, "ja_exists"]); continue
        have.add(x["sci"]); have_ja.add(ja); cur += 1
        res.append({"order": osci, "orderJa": oja, "family": c["cl"].get("family"), "ja": ja, "sci": x["sci"], "inatObs": x["n"], "jaVotes": sorted(best[0][1])})
    print(osci, oja, "世界", world, "目標", target, "今", n_have.get(osci, 0), "→", cur, flush=True)
json.dump({"species": res, "skipped": skip}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{out}: 足す {len(res)}・見送り {len(skip)}")
