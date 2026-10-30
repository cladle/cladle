# ゲキムズのデータの作り方

ゲキムズの `data-hard-*.json` は、本家のデータに、魚・爬虫両生類・海や陸の無脊椎動物・陸の生き物を足して作ります。中心は `merge_hard.py` です。

## 自分で直せるファイル

| ファイル | 中身 |
| --- | --- |
| `hard_facts.tsv` | ゲキムズだけの種の一言説明。1行1種で、学名・和名・説明・出典をタブで区切る |
| `hard_only.json` | 本家に入れず、ゲキムズだけに入れる種。`place` に、入れる場所の節目（科・目など）を下から順に書く |
| `hard_tiers.tsv` | ゲキムズだけの種の知名度（1〜4）の上書き。学名・和名・tier をタブで区切る（一覧ページの案を表にしたもの） |
| `insect_taxa.json` | 昆虫の目・科の並び（Catalogue of Life）と和名（環境省1997、無ければ Wikidata・GBIF・iNaturalist の多数決）。`insect_taxa.py` が作る。目より上の置き場所は `insect_taxa.py` の `ORDER_UNDER` に書く |
| `bird_taxa.json` | 鳥の目・科・属の並びと和名（日本鳥類目録改訂第8版）。`osj_birds.py` が目録の掲載鳥類リスト（Excel）から作る。目より上の置き場所は `osj_birds.py` の `ORDER_UNDER` に書く |
| `fixes.tsv` | 和名・学名の直し（標準和名リストなどと照らした結果） |
| `insects_refs.tsv` | 照合できなかった昆虫の和名の出典論文 |
| `clade_desc.tsv` | ゲキムズ・番外編だけの節目（目より上）の説明。学名・階級・説明・出典をタブで区切る。説明には、その群の特徴と、隣の（姉妹の）群との違いを書く。見た目で分けられない群は「遺伝子の解析でまとまる」と書く。直したら `apply_clade_desc.py` で今の版と予約中の版の data-*.json に書き込む（文だけの直しなので版は上げない） |

説明や出典は、学術的に確かめられるものだけを書きます。

## リポジトリに置いていない材料

次のファイルは外部のデータベースやリストから取ってきたデータそのものなので、このリポジトリには置かず、Claude のプロジェクトのフォルダ（`metazoa-guess-ja/tools/hard/cache/`）に置いています。データを丸ごと同梱しない、という方針のためです。

- `hard_vert.json`：魚・爬虫両生類（`build_hard.py` が日本産魚類全種目録と爬虫両棲類学会の標準和名リストから作る）
- `col.tgz`：Catalogue of Life の日本語名
- `worms.tgz`：WoRMS の日本語名
- `land.json`：陸の生き物（`build_land.py` が環境省の対象種一覧と Japan Spider Catalog から作る）
- `clade_ids.json`：前回作ったときの節目の id（id が変わっていないかの確認用）

そのため、ゲキムズの作り直しは今のところ Claude が行います。上の表のファイルを直して main に入れたら、作り直しを頼んでください。

## 作り直し

```
python3 tools/hard/merge_hard.py <本家の最新 data-*.json> cache/hard_vert.json <col を展開したフォルダ> <出力.json> tools/hard/fixes.tsv <worms を展開したフォルダ> cache/land.json
```

出力に `datasetVersion`（`hard-0.3.6` など）を付けて `data-hard-<版>.json` として置き、`data-hard.json` の `meta.next` に開始日とファイル名を書きます。切り替わったあとは中身を `data-hard.json` に写し、`data-hard-<版>.json` は消します。本家の種を足したときも、本家の新しい版を渡して作り直します。
