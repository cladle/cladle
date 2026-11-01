# -*- coding: utf-8 -*-
"""公開前の確認。GitHub に送るたびに自動で動く（.github/workflows/check.yml）。手元では  python3 tools/check.py

1. data.json と data-hard.json から meta.next をたどり、予約されている版のファイルが全部あるか
2. tools/build_data.py で作り直したデータが、いちばん新しい版のファイルと同じか
   （違うときは、data-*.json を手で直したか、data_more.py を直したのに作り直していない）
3. 出題の重みを実際の種数で決めるデータ（meta.selection.realCounts）に、種数の無い群（目・門・綱）が無いか
   （新しい目などの種を足したら  python3 tools/real_counts.py  を動かして数を足し、データを作り直す）
4. data-fish.json・data-bird.json・data-insect.json が data-hard.json から tools/fish/make_fish.py・tools/bird/make_bird.py・tools/insect/make_insect.py で作ったものと同じか（違っても止めずに知らせるだけ）
"""
import json, os, subprocess, sys, tempfile
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ok = True

def chain(first):
    files, f = [], first
    while f:
        assert f not in files, "予約がループしている: " + f
        p = os.path.join(ROOT, f)
        if not os.path.exists(p):
            print("× 予約されたファイルがない:", f); return files, False
        files.append(f)
        f = (json.load(open(p, encoding="utf-8"))["meta"].get("next") or {}).get("file")
    return files, True

main, good = chain("data.json"); ok &= good
hard, good = chain("data-hard.json"); ok &= good
print("今日の動物の予約:", " → ".join(main))
fish, good = chain("data-fish.json"); ok &= good
bird, good = chain("data-bird.json"); ok &= good
insect, good = chain("data-insect.json"); ok &= good
print("ゲキムズの予約:", " → ".join(hard))
print("魚編の予約:", " → ".join(fish))
print("鳥編の予約:", " → ".join(bird))
print("昆虫編の予約:", " → ".join(insect))

with tempfile.TemporaryDirectory() as d:
    out = os.path.join(d, "built.json")
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build_data.py"), out], check=True)
    built = json.load(open(out, encoding="utf-8"))
latest = json.load(open(os.path.join(ROOT, main[-1]), encoding="utf-8"))
for k in ("clades", "species"):
    if built[k] != latest[k]:
        ok = False
        A = {x["id"]: x for x in built[k]}; B = {x["id"]: x for x in latest[k]}
        diff = sorted(i for i in A.keys() | B.keys() if A.get(i) != B.get(i))
        print(f"× {main[-1]} の {k} が build_data.py の結果と {len(diff)} 件ちがう:", ", ".join(diff[:10]))
if built["meta"]["datasetVersion"] != latest["meta"]["datasetVersion"]:
    print(f"△ 版番号：build_data.py は {built['meta']['datasetVersion']}、{main[-1]} は {latest['meta']['datasetVersion']}（新しい版を作ったら予約を足す）")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import real_counts
for files in (hard, bird, insect):
    for f in files:
        d = json.load(open(os.path.join(ROOT, f), encoding="utf-8"))
        if "realCounts" not in d["meta"].get("selection", {}): continue
        P, missing = real_counts.probs(d)
        if missing:
            ok = False; print(f"× {f}：実際の種数が無い群がある（tools/real_counts.py を動かして作り直す）:", "、".join(sorted(missing)))
        if f == files[-1]:
            rk = d["meta"]["selection"]["realCounts"]["ranks"][0]
            C = {c["id"]: c for c in d["clades"]}; S = {s["id"]: s for s in d["species"]}; share = {}
            for i, p in P.items():
                x = S[i]["parent"]
                while x and C[x].get("rank") != rk: x = C[x]["parent"]
                share[C[x]["ja"]] = share.get(C[x]["ja"], 0) + p
            print(f"{f} の出題の割合（{rk}、上位5）:", "・".join(f"{k} {v:.0%}" for k, v in sorted(share.items(), key=lambda x: -x[1])[:5]))
for name, tool, files in (("魚編", "fish/make_fish.py", fish), ("鳥編", "bird/make_bird.py", bird), ("昆虫編", "insect/make_insect.py", insect)):
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "sub.json")
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", *tool.split("/")), os.path.join(ROOT, hard[-1]), out], check=True, stdout=subprocess.DEVNULL)
        built = json.load(open(out, encoding="utf-8"))
    latest = json.load(open(os.path.join(ROOT, files[-1]), encoding="utf-8"))
    if any(built[k] != latest[k] for k in ("clades", "species")):
        print(f"△ {files[-1]} が {hard[-1]} から作ったものと違う（ゲキムズを作り直したら、{name}も版を上げて作り直す）")
print("○ 問題なし" if ok else "× 直すところがあります")
sys.exit(0 if ok else 1)
