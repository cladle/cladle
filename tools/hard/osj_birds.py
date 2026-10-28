# -*- coding: utf-8 -*-
"""日本鳥類目録改訂第8版の掲載鳥類リスト（Excel）から、ゲキムズの鳥の目・科・属の並びと和名を作る。

  python3 tools/hard/osj_birds.py jpbirdlist8ed_ver1.xlsx tools/hard/bird_taxa.json

- 元のリスト：日本鳥学会（2024）日本鳥類目録改訂第8版 掲載鳥類リスト ver.1（2024-10-08公開）
  https://ornithology.jp/checklist.html 。リストの注意書きに「利用者の責任において二次的に加工して使用することが
  できます」とある。種のリストそのものは置かず、目・科・属の対応と和名だけを bird_taxa.json に残す。
- 目より上の置き場所（ORDER_UNDER）は、Jarvis et al. 2014・Prum et al. 2015・Stiller et al. 2024 の
  系統ゲノム解析でそろって支持されるまとまりにだけ入れる。解析で位置が割れる目（ノガン目・ネッタイチョウ目）は
  新鳥類の直下に置き、多分岐のままにする。
"""
import json, sys, openpyxl

src, out = sys.argv[1:3]
ORDER_UNDER = {
    "Caprimulgiformes": "Strisores", "Apodiformes": "Strisores",
    "Columbiformes": "Columbimorphae", "Pterocliformes": "Columbimorphae",
    "Podicipediformes": "Mirandornithes",
    "Gaviiformes": "Aequornithes", "Ciconiiformes": "Aequornithes",
    "Accipitriformes": "Afroaves", "Bucerotiformes": "Afroaves",
    "Otidiformes": "Neoaves", "Phaethontiformes": "Neoaves",
}
rows = [r for r in list(openpyxl.load_workbook(src, read_only=True)["リスト"].iter_rows(values_only=True))[1:] if r[0]]
orders, families, genera = {}, {}, {}
cur = {}
for no, part, cat, sp, ssp, sci, auth, ja in rows:
    if cat not in ("目", "科", "属"): continue
    nm = sci.strip().title()
    if cat == "目":
        orders.setdefault(nm, {"ja": ja, **({"under": ORDER_UNDER[nm]} if nm in ORDER_UNDER else {})})
    elif cat == "科":
        families.setdefault(nm, {"ja": ja, "order": cur["目"]})
    else:
        genera.setdefault(nm, cur["科"])
    cur[cat] = nm
json.dump({"source": "日本鳥学会（2024）日本鳥類目録改訂第8版 掲載鳥類リスト ver.1（2024-10-08公開）",
           "orders": orders, "families": families, "genera": genera},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{out}: 目 {len(orders)}・科 {len(families)}・属 {len(genera)}")
