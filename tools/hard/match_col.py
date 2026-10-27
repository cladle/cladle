"""環境省の対象種（biodic.json）の学名を今の Catalogue of Life (3LR) に合わせる。
CoL で種として当たらなければ GBIF で受理名を引き、その名前で CoL を引き直す。
1件ずつ、同じサイトへは1.2秒以上あけ、結果はキャッシュする。"""
import json, os, sys, time, hashlib, urllib.parse, urllib.request
UA = {"User-Agent": "Cladle-education-game (github.com/cladle/cladle; low-volume, sequential, cached)"}
CD = os.path.join(os.path.dirname(os.path.abspath(sys.argv[2])), "cache"); os.makedirs(CD, exist_ok=True)
last = {}
def get(url):
    cp = os.path.join(CD, hashlib.sha1(url.encode()).hexdigest() + ".json")
    if os.path.exists(cp): return json.load(open(cp))
    h = urllib.parse.urlparse(url).netloc
    for i in range(4):
        w = last.get(h, 0) + 1.2 - time.time()
        if w > 0: time.sleep(w)
        last[h] = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r: d = json.load(r)
            json.dump(d, open(cp, "w")); return d
        except urllib.error.HTTPError as e:
            if e.code == 404: json.dump(None, open(cp, "w")); return None
            time.sleep(10 * (i + 1))
        except Exception: time.sleep(10 * (i + 1))
    return None
def col(name):
    d = get("https://api.checklistbank.org/dataset/3LR/match/nameusage?" + urllib.parse.urlencode({"scientificName": name, "verbose": "true"}))
    if not d or d.get("type") in (None, "none", "higherrank") or "usage" not in d: return None
    u = d["usage"]
    if u.get("rank") not in ("species", "subspecies"): return None
    return d
B = json.load(open(sys.argv[1])); out = {}
todo = [(k, r) for k, v in B.items() for r in v]
for n, (k, r) in enumerate(todo):
    key = r["sci"]
    if key in out: continue
    d = col(key); via = "col"
    if not d:
        g = get("https://api.gbif.org/v1/species/match?" + urllib.parse.urlencode({"name": key, "kingdom": "Animalia"}))
        acc = g and g.get("matchType") in ("EXACT", "FUZZY") and (g.get("species") or g.get("canonicalName"))
        if acc and acc != key: d = col(acc); via = "gbif->col"
    out[key] = {"via": via if d else None, "match": d}
    if n % 200 == 0: print(n, len(todo), flush=True); json.dump(out, open(sys.argv[2], "w"))
json.dump(out, open(sys.argv[2], "w")); print("done", len(out))
