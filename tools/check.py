# -*- coding: utf-8 -*-
"""公開前の確認。GitHub に送るたびに自動で動く（.github/workflows/check.yml）。手元では  python3 tools/check.py

1. data.json・data-hard.json・data-fish.json・data-bird.json・data-insect.json から meta.next をたどり、予約されている版のファイルが全部あるか
2. 全種の台帳（tools/ledger/）から tools/build_all.py で作ったものが、今の版・予約中の版と同じか
   （違うときは、data-*.json を手で直したか、台帳を直したのに  python3 tools/build_all.py --write  を動かしていない）
3. 出題の重みを実際の種数で決めるデータ（meta.selection.realCounts）に、種数の無い群（目・門・綱）が無いか
   （新しい目などの種を足したら  python3 tools/real_counts.py  を動かして数を足し、データを作り直す）
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

r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build_all.py"), "--check"], capture_output=True, text=True)
print(r.stdout.strip()); print(r.stderr.strip()) if r.returncode and r.stderr else None
ok &= r.returncode == 0
sys.path.insert(0, os.path.join(ROOT, "tools"))
import real_counts
for files in (hard, bird, insect, fish):
    for f in files:
        d = json.load(open(os.path.join(ROOT, f), encoding="utf-8"))
        if "realCounts" not in d["meta"].get("selection", {}): continue
        P, missing = real_counts.probs(d)
        if missing:
            ok = False; print(f"× {f}：実際の種数が無い群がある（tools/real_counts.py を動かして作り直す）:", "、".join(sorted(missing)))
        if f == files[-1]:
            rc = d["meta"]["selection"]["realCounts"]; rk = rc["ranks"][0]
            C = {c["id"]: c for c in d["clades"]}; S = {s["id"]: s for s in d["species"]}; share = {}
            for i, p in P.items():
                g = real_counts.group(C, S[i]["parent"], rc)["ja"]
                share[g] = share.get(g, 0) + p
            print(f"{f} の出題の割合（{rk}、上位5）:", "・".join(f"{k} {v:.0%}" for k, v in sorted(share.items(), key=lambda x: -x[1])[:5]))
print("○ 問題なし" if ok else "× 直すところがあります")
sys.exit(0 if ok else 1)
