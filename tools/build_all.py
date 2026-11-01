# -*- coding: utf-8 -*-
"""本家・ゲキムズ・魚編・鳥編・昆虫編のデータを、1回でまとめて作り直す。

  python3 tools/build_all.py            確かめるだけ（どのファイルがどう変わるかを表示し、何も書かない）
  python3 tools/build_all.py --write    data-*.json に書き込む

本家（tools/data_more.py）か、ゲキムズの材料（tools/hard/ の表）を直したら、同じ PR の中でこれを動かす。
本家の直しがゲキムズと各編に、ゲキムズの直しが各編に、その場で届く。

流れ:
1. tools/build_data.py で本家を作る
2. tools/hard/merge_hard.py で、本家に外部データの種を足してゲキムズを作る
3. tools/fish/make_fish.py・tools/bird/make_bird.py・tools/insect/make_insect.py で各編を切り出す
4. モードごとに、出来たものを「今の版」と「予約中の版」に入れる
   - 文だけの違い（和名・説明・別名など。出題の選び方に関わらないもの）：今の版にも予約中の版にも入れる。版は上げない
   - 種・節目・知名度などの違い（今日の動物の並びが変わるもの）：まだ始まっていない予約版だけを差し替える。
     予約版が無いか、もう始まっているときは止まる。新しい版を作って予約する（--new）
5. 本家とゲキムズの木がずれていないかを確かめる（本家で作った節目の外に、ゲキムズの同じ群が残っていないか）

  python3 tools/build_all.py --write --new hard=hard-0.3.13@2026-11-05
      ゲキムズの新しい版 data-hard-0.3.13.json を作り、2026-11-05 から始まるように今の最後の版の meta.next に書く。
      魚編・鳥編・昆虫編の新しい版の名前は、それぞれの make_*.py の版番号（FISH_VERSION など）を上げて決める（日付は --new fish=@2026-11-05 のように渡す）。
      本家の新しい版は今まで通り data_more.py で決める（このコマンドは本家の版を作らない）。

外部データ（Catalogue of Life・WoRMS の日本語名、魚・爬虫両生類、陸の生き物）はリポジトリに置いていない。
置き場所は --cache か環境変数 CLADLE_CACHE で渡す（既定は Claude のプロジェクトのフォルダ）。
"""
import argparse, datetime, json, os, shutil, subprocess, sys, tarfile, tempfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
T = os.path.join(ROOT, "tools")
DEFAULT_CACHE = "/mnt/project-files/metazoa-guess-ja/tools/hard/cache"

# 出題の選び方に関わらない欄（違っていても今日の動物の並びは変わらない）
TEXT = {"species": ("ja", "sci", "aliases", "fact", "sciSynonyms", "verify", "jaStatus", "subspeciesAliases", "groups", "gbif", "jaReading"),
        "clades": ("ja", "desc", "polytomy", "verify", "jaReading")}
MODES = [  # 名前, 最初のファイル, 書き方（本家は1行ずつ字下げ、ほかは詰める）
    ("本家", "data.json", 1), ("ゲキムズ", "data-hard.json", None),
    ("魚編", "data-fish.json", None), ("鳥編", "data-bird.json", None), ("昆虫編", "data-insect.json", None)]
KEY = {"本家": "main", "ゲキムズ": "hard", "魚編": "fish", "鳥編": "bird", "昆虫編": "insect"}

def load(f): return json.load(open(os.path.join(ROOT, f), encoding="utf-8"))
def save(f, d, indent):
    with open(os.path.join(ROOT, f), "w", encoding="utf-8") as o:
        json.dump(d, o, ensure_ascii=False, indent=indent, separators=None if indent else (",", ":"))

def chain(first):
    """[(ファイル, 始まる日 or None)]。最初のファイルは今の版（始まっている）"""
    out, f, start = [], first, None
    while f:
        d = load(f); out.append((f, start))
        nx = d["meta"].get("next") or {}
        f, start = nx.get("file"), nx.get("from")
    return out

def shape(d):
    """今日の動物の並びを決めるもの：種の並び・親・知名度、節目の親・階級・学名、出題の設定"""
    return (d["meta"].get("selection"), [(s["id"], s["parent"], s.get("tier")) for s in d["species"]],
            [(c["id"], c["parent"], c["rank"], c["sci"]) for c in d["clades"]])

def text_into(dst, src, skipped):
    """src の文（TEXT の欄）を、dst の同じ id の種・節目に入れる。変えた数を返す。
    名前を変えると dst のほかの種の和名とぶつかるとき（亜種を種にまとめる前の版など）は、その種は変えない"""
    n = 0
    for k, fields in TEXT.items():
        S = {x["id"]: x for x in src[k]}
        owner = {}
        if k == "species":
            for x in dst[k]: owner.setdefault(x["ja"], x["id"])
        for x in dst[k]:
            y = S.get(x["id"])
            if not y: continue
            added = {y["ja"], *y.get("aliases", [])} - {x["ja"], *x.get("aliases", [])}
            clash = k == "species" and any(owner.get(nm, x["id"]) != x["id"] for nm in added)
            if clash: skipped.append(x["ja"]); continue
            for f in fields:
                if x.get(f) != y.get(f):
                    n += 1
                    if f in y: x[f] = y[f]
                    else: x.pop(f, None)
    return n

def diff_count(a, b):
    out = {}
    for k in ("species", "clades"):
        A = {x["id"]: x for x in a[k]}; B = {x["id"]: x for x in b[k]}
        out[k] = (len(A.keys() - B.keys()), len(B.keys() - A.keys()), sum(1 for i in A.keys() & B.keys() if A[i] != B[i]))
    return out

# 確かめて、ずれではないと分かったもの（本家の節目の学名: そう判断した理由）
DRIFT_OK = {
    "Serpentes": "ヘビ亜目はトカゲ類の中から出た群。トカゲの科が有鱗目の直下に並ぶのは正しい",
    "Pinnipedia": "アライグマ科は鰭脚類ではない",
    "Sternorrhyncha": "ウンカ科・アオバハゴロモ科は腹吻亜目ではなく頸吻亜目（本家はカメムシ目の亜目をすべては置いていない）",
}

def drift(main, hard):
    """本家で作った節目 X が親 P の下にあるのに、ゲキムズでは P の直下に X の子と同じ階級の群が残っているもの。
    例：本家でクモ目の下に Araneoidea を作ったのに、ゲキムズのクモの科がクモ目の直下に並んだまま。"""
    MC = {c["id"] for c in main["clades"]}
    C = {c["id"]: c for c in hard["clades"]}
    kids = {}
    for c in hard["clades"]:
        if c["parent"]: kids.setdefault(c["parent"], []).append(c)
    found = []
    for x in main["clades"]:
        if x["id"] not in C or x["rank"] in ("属", "科") or not x["parent"] or x["parent"] not in C: continue
        if x["rank"] not in ("クレード", "上科", "下目", "亜目", "上目", "亜綱", "下綱"): continue
        # 親が多分岐（分かれる順を決めずに並べている）なら、親の直下に群が残るのは決めた通り
        if x["sci"] in DRIFT_OK or C[x["parent"]].get("polytomy"): continue
        mine = {c["rank"] for c in kids.get(x["id"], []) if c["rank"] in ("科", "上科")}
        if not mine: continue
        left = [c for c in kids.get(x["parent"], []) if c["rank"] in mine and c["id"] not in MC]
        if left:
            found.append((C[x["parent"]]["ja"], x["ja"], len(left), "・".join(c["ja"] for c in left[:5])))
    return found

def main_():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--cache", default=os.environ.get("CLADLE_CACHE", DEFAULT_CACHE))
    ap.add_argument("--new", action="append", default=[], help="hard=hard-0.3.13@2026-11-05 / fish=@2026-11-05")
    a = ap.parse_args()
    new = {}
    for x in a.new:
        k, v = x.split("=", 1); ver, _, day = v.partition("@"); new[k] = (ver, day)
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().isoformat()
    need = ["hard_vert.json", "col.tgz", "worms.tgz", "land.json"]
    miss = [f for f in need if not os.path.exists(os.path.join(a.cache, f))]
    if miss: sys.exit(f"外部データが見つからない（{a.cache}）: {', '.join(miss)}")

    built = {}
    with tempfile.TemporaryDirectory() as tmp:
        p = lambda n: os.path.join(tmp, n)
        print("本家を作る …"); subprocess.run([sys.executable, os.path.join(T, "build_data.py"), p("main.json")], check=True, stdout=subprocess.DEVNULL)
        for n in ("col", "worms"):
            with tarfile.open(os.path.join(a.cache, n + ".tgz")) as t: t.extractall(p(n), filter="data")
        sub = lambda n: next(os.path.join(r, "") for r, ds, fs in os.walk(p(n)) if any(f.startswith("v") and f.endswith(".json") for f in fs))
        # merge_hard.py は節目の id の控え（tools/hard/cache/clade_ids.json）を書き換えるので、外部の控えを写して使い、終わったら戻す
        ids_dir = os.path.join(T, "hard", "cache"); os.makedirs(ids_dir, exist_ok=True)
        ids, ids_src = os.path.join(ids_dir, "clade_ids.json"), os.path.join(a.cache, "clade_ids.json")
        ids_bak = ids + ".bak" if os.path.exists(ids) else None
        if ids_bak: shutil.copy(ids, ids_bak)
        if os.path.exists(ids_src): shutil.copy(ids_src, ids)
        try:
            print("ゲキムズを作る …（数分かかる）")
            subprocess.run([sys.executable, os.path.join(T, "hard", "merge_hard.py"), p("main.json"), os.path.join(a.cache, "hard_vert.json"),
                            sub("col"), p("hard.json"), os.path.join(T, "hard", "fixes.tsv"), sub("worms"), os.path.join(a.cache, "land.json")],
                           check=True, stdout=subprocess.DEVNULL)
        finally:
            if ids_bak: shutil.move(ids_bak, ids)
            elif os.path.exists(ids): os.remove(ids)
        # 各編のデータに書くゲキムズの版（meta.status）を、入れる先のゲキムズの版にしておく
        h = json.load(open(p("hard.json"), encoding="utf-8"))
        h["meta"]["datasetVersion"] = new["hard"][0] if "hard" in new else load(chain("data-hard.json")[-1][0])["meta"]["datasetVersion"]
        json.dump(h, open(p("hard.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
        for k, tool in (("fish", "fish/make_fish.py"), ("bird", "bird/make_bird.py"), ("insect", "insect/make_insect.py")):
            subprocess.run([sys.executable, os.path.join(T, *tool.split("/")), p("hard.json"), p(k + ".json")], check=True, stdout=subprocess.DEVNULL)
        for k in ("main", "hard", "fish", "bird", "insect"):
            built[k] = json.load(open(p(k + ".json"), encoding="utf-8"))

    ok, writes = True, {}
    print()
    for name, first, indent in MODES:
        k = KEY[name]; b = built[k]; ch = chain(first)
        tail, start = ch[-1]; cur = writes.get(tail) or load(tail)
        started = start is None or start <= today
        same = shape(b) == shape(cur)
        if k == "main":
            # 本家の版は data_more.py で決める。作り直したものがいちばん新しい版と違えば、作り直しを忘れている
            if not same or b["clades"] != cur["clades"] or b["species"] != cur["species"]:
                ok = False; print(f"× 本家：{tail} が build_data.py の結果と違う。先に  python3 tools/build_data.py {tail}  で作り直す")
            target = None
        elif same:
            target = None
        elif k in new:
            ver = new[k][0] or b["meta"]["datasetVersion"]
            if ver == cur["meta"]["datasetVersion"]:
                ok = False; print(f"× {name}：新しい版の名前が今の最後の版（{ver}）と同じ"); continue
            if not new[k][1] or new[k][1] <= (start or today):
                ok = False; print(f"× {name}：新しい版の始まる日（--new {k}=…@YYYY-MM-DD）は {start or today} より後にする"); continue
            f = ("data-" + ver + ".json") if ver.startswith(k + "-") else f"data-{k}-{ver}.json"
            b["meta"]["datasetVersion"] = ver
            cur["meta"]["next"] = {"from": new[k][1], "file": f}; writes[tail] = cur
            ch.append((f, new[k][1])); target = f
            print(f"＋ {name}：新しい版 {f} を作り、{new[k][1]} から始める（{tail} の meta.next）")
        elif started:
            ok = False
            print(f"× {name}：種・節目・知名度が変わるが、{tail} はもう始まっている（{start or '今の版'}）。新しい版を作って予約する："
                  f"  --new {k}={'hard-0.3.x' if k == 'hard' else ''}@YYYY-MM-DD" + ("" if k == "hard" else f"（先に tools/{k}/make_{k}.py の版番号を上げる）"))
            target = None
        else:
            target = tail
        if target:
            if target == tail:
                b["meta"]["datasetVersion"] = cur["meta"]["datasetVersion"]
                if cur["meta"].get("next"): b["meta"]["next"] = cur["meta"]["next"]
                print(f"△ {name}：まだ始まっていない予約版 {tail}（{start}〜）を差し替える（今日の動物の並びが変わる）", diff_count(b, cur))
            writes[target] = b
        # 文の直しは、今の版にも予約中の版にも入れる
        for f, _ in ch:
            if f == target: continue
            d = writes.get(f) or load(f)
            sk = []; n = text_into(d, b, sk)
            if n:
                print(f"・{name}：{f} に文の直しを {n} か所入れる（版は上げない）"); writes[f] = d
            if sk:
                print(f"  （{f} では、ほかの種の和名とぶつかるので変えなかった：{'・'.join(sk)}）")
        if not target and not any(f in writes for f, _ in ch):
            print(f"○ {name}：変わりなし")

    found = drift(built["main"], built["hard"])
    if found:
        print("\n△ 本家で作った節目の外に、ゲキムズの同じ階級の群が残っている（本家の木に合わせてゲキムズでも振り分けるか確かめる。tools/hard/merge_hard.py の MOVE_INTO など）:")
        for p_, x, n, ex in found: print(f"   {p_} の下の {x}：{p_} の直下に {n} 群（{ex} …）")

    if a.write and ok:
        indents = {f: i for name, first, i in MODES for f, _ in chain(first)}
        for f, d in writes.items():
            save(f, d, indents.get(f, 1 if f.startswith("data-0") else None))
        print(f"\n{len(writes)} 個のファイルに書いた:", "、".join(sorted(writes)))
    elif a.write:
        print("\n× のところを直すまで書かない")
    else:
        print("\n（確かめただけ。書き込むには --write）" if writes else "")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main_()
