# -*- coding: utf-8 -*-
"""全種の台帳（tools/ledger/）から、本家・ゲキムズ・魚編・鳥編・昆虫編のデータを1回でまとめて作り直す。

  python3 tools/build_all.py            確かめるだけ（どのファイルがどう変わるかを表示し、何も書かない）
  python3 tools/build_all.py --write    data-*.json に書き込む

台帳（tools/ledger/species.jsonl・clades.jsonl）を直したら、同じ PR の中でこれを動かす。
GitHub に送るたびに tools/check.py がこれを「確かめるだけ」で動かし、書き忘れを知らせる。

流れ:
1. 台帳から本家とゲキムズを作る（tools/ledger/ledger.py）
2. tools/fish/make_fish.py・tools/bird/make_bird.py・tools/insect/make_insect.py でゲキムズから各編を切り出す
3. モードごとに、出来たものを「今の版」と「予約中の版」に入れる
   - 文だけの違い（和名・説明・別名など。出題の選び方に関わらないもの）：今の版にも予約中の版にも入れる。版は上げない
   - 種・節目・知名度などの違い（今日の動物の並びが変わるもの）：まだ始まっていない予約版だけを差し替える。
     予約版が無いか、もう始まっているときは止まる。新しい版を作って予約する（--new）
4. 本家の木とゲキムズの木がずれていないかを確かめる（本家の節目の外に、同じ階級の群が残っていないか）

  python3 tools/build_all.py --write --new hard=hard-0.3.13@2026-11-05
      ゲキムズの新しい版 data-hard-0.3.13.json を作り、2026-11-05 から始まるように今の最後の版の meta.next に書く。
      本家は --new main=0.3.19@2026-11-05（data-0.3.19.json）、各編は --new fish=fish-0.1.4@2026-11-05 のように渡す。
"""
import argparse, datetime, json, os, subprocess, sys, tempfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
T = os.path.join(ROOT, "tools")
sys.path.insert(0, os.path.join(T, "ledger"))
import ledger

# 出題の選び方に関わらない欄（違っていても今日の動物の並びは変わらない）
TEXT = {"species": ("ja", "sci", "aliases", "fact", "sciSynonyms", "verify", "jaStatus", "subspeciesAliases", "groups", "gbif", "jaReading"),
        "clades": ("ja", "desc", "polytomy", "verify", "jaReading")}
MODES = [  # 名前, 最初のファイル, 書き方（本家は1行ずつ字下げ、ほかは詰める）
    ("本家", "data.json", 1), ("ゲキムズ", "data-hard.json", None),
    ("魚編", "data-fish.json", None), ("鳥編", "data-bird.json", None), ("昆虫編", "data-insect.json", None)]
KEY = {"本家": "main", "ゲキムズ": "hard", "魚編": "fish", "鳥編": "bird", "昆虫編": "insect"}

def load(f): return json.load(open(os.path.join(ROOT, f), encoding="utf-8"))
def save(f, d, indent):
    p = os.path.join(ROOT, f)
    nl = os.path.exists(p) and open(p, "rb").read()[-1:] == b"\n"  # 終わりの改行は今のファイルに合わせる
    with open(p, "w", encoding="utf-8") as o:
        json.dump(d, o, ensure_ascii=False, indent=indent, separators=None if indent else (",", ":"))
        if nl: o.write("\n")

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

# 確かめて、ずれではないと分かったもの（本家の節目か、親の直下に残っている群の学名: そう判断した理由）
DRIFT_OK = {
    "Serpentes": "ヘビ亜目はトカゲ類の中から出た群。トカゲの科が有鱗目の直下に並ぶのは正しい",
    "Pinnipedia": "アライグマ科は鰭脚類ではない",
    "Spongicolidae": "ドウケツエビ科はオトヒメエビ下目（Stenopodidea）の科。その下目の節目は置いていない",
    "Polychelidae": "センジュエビ科はセンジュエビ下目（Polychelida）の科。その下目の節目は置いていない",
    "Sternorrhyncha": "ウンカ科・アオバハゴロモ科は腹吻亜目ではなく頸吻亜目（本家はカメムシ目の亜目をすべては置いていない）",
}

def drift(L):
    """本家の節目 X が親 P の下にあるのに、P の直下に X の子と同じ階級の群（本家に出ない群）が残っているもの。
    例：クモ目の下に本家の Araneoidea を作り、本家の種の科だけを移して、ほかのクモの科をクモ目の直下に残した。"""
    C = {c["id"]: c for c in L["clades"]}
    kids = {}
    for c in L["clades"]:
        if c["parent"]: kids.setdefault(c["parent"], []).append(c)
    found = []
    for x in L["clades"]:
        if "main" not in x or not x["parent"]: continue
        if x["rank"] not in ("クレード", "上科", "下目", "亜目", "上目", "亜綱", "下綱"): continue
        # 親が多分岐（分かれる順を決めずに並べている）なら、親の直下に群が残るのは決めた通り
        # （ゲキムズで足した群の置き場所に付ける決まり文句は、多分岐の理由に数えない）
        poly = C[x["parent"]].get("polytomy", "").split("ゲキムズでは、Catalogue of Life・WoRMS から足した群のうち")[0].strip()
        if x["sci"] in DRIFT_OK or poly: continue
        mine = {c["rank"] for c in kids.get(x["id"], []) if c["rank"] in ("科", "上科")}
        left = [c for c in kids.get(x["parent"], []) if c["rank"] in mine and "main" not in c and c["sci"] not in DRIFT_OK]
        if left:
            found.append((C[x["parent"]]["ja"], x["ja"], len(left), "・".join(c["ja"] for c in left[:5])))
    return found

def main_():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true", help="書き直しの要るファイルがあれば失敗にする（tools/check.py から使う）")
    ap.add_argument("--new", action="append", default=[], help="main=0.3.19@2026-11-05 / hard=hard-0.3.13@2026-11-05")
    a = ap.parse_args()
    new = {}
    for x in a.new:
        k, v = x.split("=", 1); ver, _, day = v.partition("@"); new[k] = (ver, day)
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().isoformat()
    L = ledger.load()
    bad = ledger.check(L)
    if bad: sys.exit("× 台帳に直すところがある:\n  " + "\n  ".join(bad))
    built = {"main": ledger.build_main(L), "hard": ledger.build_hard(L)}
    # 各編のデータに書くゲキムズの版（meta.status）を、入れる先のゲキムズの版にしておく
    built["hard"]["meta"]["datasetVersion"] = new["hard"][0] if "hard" in new else load(chain("data-hard.json")[-1][0])["meta"]["datasetVersion"]
    with tempfile.TemporaryDirectory() as tmp:
        p = lambda n: os.path.join(tmp, n)
        json.dump(built["hard"], open(p("hard.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
        for k, tool in (("fish", "fish/make_fish.py"), ("bird", "bird/make_bird.py"), ("insect", "insect/make_insect.py")):
            subprocess.run([sys.executable, os.path.join(T, *tool.split("/")), p("hard.json"), p(k + ".json")], check=True, stdout=subprocess.DEVNULL)
            built[k] = json.load(open(p(k + ".json"), encoding="utf-8"))

    ok, writes = True, {}
    print()
    for name, first, indent in MODES:
        k = KEY[name]; b = built[k]; ch = chain(first)
        tail, start = ch[-1]; cur = writes.get(tail) or load(tail)
        started = start is None or start <= today
        same = shape(b) == shape(cur)
        if same:
            target = None
        elif k in new:
            ver = new[k][0]
            if not ver or (k != "main" and not ver.startswith(k + "-")):
                ok = False; print(f"× {name}：新しい版の名前を  --new {k}={'0.3.x' if k == 'main' else k + '-0.x.x'}@YYYY-MM-DD  の形で渡す"); continue
            if ver == cur["meta"]["datasetVersion"]:
                ok = False; print(f"× {name}：新しい版の名前が今の最後の版（{ver}）と同じ"); continue
            if not new[k][1] or new[k][1] <= (start or today):
                ok = False; print(f"× {name}：新しい版の始まる日（--new {k}=…@YYYY-MM-DD）は {start or today} より後にする"); continue
            f = "data-" + ver + ".json"
            b["meta"]["datasetVersion"] = ver
            cur["meta"]["next"] = {"from": new[k][1], "file": f}; writes[tail] = cur
            ch.append((f, new[k][1])); target = f
            print(f"＋ {name}：新しい版 {f} を作り、{new[k][1]} から始める（{tail} の meta.next）")
        elif started:
            ok = False
            print(f"× {name}：種・節目・知名度が変わるが、{tail} はもう始まっている（{start or '今の版'}）。新しい版を作って予約する："
                  f"  --new {k}={'0.3.x' if k == 'main' else k + '-0.x.x'}@YYYY-MM-DD")
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

    found = drift(L)
    if found:
        print("\n△ 本家の節目の外に、同じ階級の群が残っている（台帳でその群もその節目の下に入れるか確かめる。入れないなら build_all.py の DRIFT_OK に理由を書く）:")
        for p_, x, n, ex in found: print(f"   {p_} の下の {x}：{p_} の直下に {n} 群（{ex} …）")

    if a.write and ok and writes:
        indents = {f: i for name, first, i in MODES for f, _ in chain(first)}
        for f, d in writes.items():
            save(f, d, indents.get(f, 1 if f[5:6].isdigit() else None))
        print(f"\n{len(writes)} 個のファイルに書いた:", "、".join(sorted(writes)))
    elif a.write:
        print("\n× のところを直すまで書かない")
    elif writes:
        print("\n（確かめただけ。書き込むには --write）")
        if a.check:
            print("× 台帳と data-*.json が食い違っている。python3 tools/build_all.py --write で作り直す"); ok = False
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main_()
