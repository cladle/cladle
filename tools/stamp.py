# -*- coding: utf-8 -*-
"""公開用に、index.html が読み込む css/・js/ のファイル名の後ろに中身の印（?v=…）を付ける。
公開のたびに GitHub が自動で動かす（.github/workflows/pages.yml）。手で動かす必要はない。

ブラウザは一度読んだファイルをしばらく取っておくので、名前が同じままだと古いものを使い続けることがある。
中身から作った印を付けておけば、ファイルを直したときだけ名前が変わり、再読み込み1回で新しいものが読まれる。
リポジトリの index.html は印なしのまま（手元でそのまま開ける）。  python3 tools/stamp.py [index.html]
"""
import hashlib, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
page = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "index.html")
base = os.path.dirname(os.path.abspath(page))
html = open(page, encoding="utf-8").read()

def stamp(m):
    attr, path = m.group(1), m.group(2)
    v = hashlib.sha256(open(os.path.join(base, path), "rb").read()).hexdigest()[:10]
    return f'{attr}="{path}?v={v}"'

html, n = re.subn(r'\b(href|src)="((?:css|js)/[^"?#]+\.(?:css|js))(?:\?v=[^"]*)?"', stamp, html)
open(page, "w", encoding="utf-8").write(html)
print(f"{n} 個のファイルに印を付けた")
