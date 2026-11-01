# data.json スキーマ（v1）

ゲーム本体 `index.html` は同じフォルダの `data.json` だけを読みます。このファイルを差し替えれば、出題する種や系統樹を入れ替えられます。
`data.json` などは、全種の台帳 `tools/ledger/` から `tools/build_all.py` で生成します（正本は台帳。2026-11-02 までは `tools/archive/build_data.py`・`data_more.py`）。生成時に親の存在・ID重複・空のクレード・グループ名の別名を検査します。台帳の形は `tools/ledger/README.md`。

## 全体

```json
{ "meta": { ... }, "clades": [ Clade, ... ], "species": [ Species, ... ] }
```

## meta

| キー | 型 | 説明 |
|---|---|---|
| schemaVersion | 数値 | このスキーマの版。現在 1 |
| datasetVersion | 文字列 | データの版。今日の動物の乱数の種にも使う（変えると出題が変わる） |
| title | 文字列 | データセット名 |
| referenceDate | 文字列 (YYYY-MM-DD) | 分類体系・名前を確認した基準日 |
| taxonomy.backbone | 文字列 | 骨格に採用した分類体系 |
| taxonomy.nomenclature | 文字列 | 命名の確認元 |
| taxonomy.phylogenyNotes | 文字列 | 系統の扱いの説明（多分岐の方針など） |
| taxonomy.nonMonophyleticGroupsExcluded | 文字列[] | 節目に使わない非単系統群 |
| japaneseNameSources | 文字列[] | 和名の典拠リスト |
| status | 文字列 | 確認状況の説明 |
| licenseNotes | 文字列 | 同梱データのライセンス・利用規約の状況 |
| selection.buckets | 文字列[] | 出題の枠にする門の clade id。ここに無い門はまとめて「その他の門」1枠になる。枠は等確率で選ぶ |
| selection.otherBucketLabel | 文字列 | 「その他」枠の表示名 |
| selection.phylumWeight | `"sqrt"` \| `"equal"` | 枠の中での門の重み。sqrt＝収録種数の平方根、equal＝全門同じ |
| selection.realCounts | オブジェクト | （ゲキムズ・鳥編・昆虫編・魚編）群を実際の種数で選ぶ。`ranks`＝群の階級（例 `["門","綱"]`、`["目"]`）、`top`＝外側の群の重み（`"linear"`＝種数そのまま、`"sqrt"`＝平方根）、`n`＝学名→現生の記載種数、`source`＝出典、`groups`＝`ranks[0]` の節目が上に無い種のための群の学名（魚編の肉鰭類）。これがあると buckets・phylumWeight・bucketWeight は使わない。数は tools/real_counts.py が数えて tools/real_counts.json に控える |
| selection.maxGuesses | 数値 | 推測の上限（既定 20） |
| selection.dailyEpoch | 文字列 (YYYY-MM-DD) | 「今日の動物 #1」の日付（日本時間） |

## Clade（節目）

| キー | 型 | 必須 | 説明 |
|---|---|---|---|
| id | 文字列 | ○ | 一意な ID（英小文字・数字・_） |
| parent | 文字列 \| null | ○ | 親クレードの id。根（動物界）だけ null |
| ja | 文字列 | ○ | 和名。定着した和名がないものは音写・説明的表記にし verify.ja に書く |
| sci | 文字列 | ○ | 学名（クレード名） |
| rank | 文字列 | ○ | 階級。`界` `門` `亜門` `綱` `亜綱` `上目` `目` `亜目` `下目` `科` `属` または `クレード`（階級なし）。**`門` は出題の偏り調整に使うので、各種の祖先にちょうど1つ置く** |
| desc | 文字列 | ○ | 短い説明（1〜2文） |
| polytomy | 文字列 | | 子の分岐順を決めていない（多分岐）理由。ある場合はゲーム上で「多分岐」と表示 |
| verify | オブジェクト | | 要確認の内容。キーは `ja`（和名）`sci`（学名）`placement`（系統上の位置）、値は理由 |

## Species（種・出題候補）

| キー | 型 | 必須 | 説明 |
|---|---|---|---|
| id | 文字列 | ○ | 一意な ID（クレードとも重複不可） |
| parent | 文字列 | ○ | 直上のクレードの id |
| ja | 文字列 | ○ | 表示する和名 |
| sci | 文字列 | ○ | 学名（属名＋種小名） |
| jaStatus | `"standard"` \| `"common"` \| `"provisional"` | ○ | standard＝標準和名、common＝通称、provisional＝和名なし（学名の音写などの仮表記） |
| aliases | 文字列[] | ○ | その種だけを指す別名・漢字表記・通称など。補完の検索語になる（空配列可）。グループ名は入れない |
| sciSynonyms | 文字列[] | | 旧学名（同じ種で名前だけ変わったもの）。種の説明に「旧学名：…」と表示し、入力でも打てる。別種と取り違えていた学名は入れない（収録種の学名と重ならないことをビルド時に検査） |
| subspeciesAliases | 文字列[] | | aliases のうち亜種の和名（ミシシッピアカミミガメなど）。補完候補では「〜（アカミミガメの亜種）」と出し、選ぶとその種の推測になる。黙って種に置き換えると「同じもの」と教えてしまうため（2026-10-24 作者の決定） |
| groups | 文字列[] | | その種が属するグループの通称（ウニ・カニなど）。補完には使わない（分類の知識を答えとして渡さないため）。グループ名の一覧は tools/ledger/group_aliases.txt（別名に入れると build_all.py が止まる） |
| fact | 文字列 | ○ | 正解後に表示する豆知識 |
| gbif | 数値 | | GBIF の種の番号（受理名）。正解画面の「GBIF」リンクがその種のページに飛ぶ。無ければ学名で検索する |
| answerable | 真偽値 | | false なら推測には使えるが出題はされない（近縁種の追加用）。省略時は true |
| tier | 1〜4 | | 知名度の段階。1＝だれでも知っている、2＝よく知られている（省略時）、3＝図鑑レベル、4＝専門的（仮名の種を含む）。出題（今日の動物・フリー）で段階的に少しずつ出にくくする（重みは meta.selection.tierWeights、ゲーム側）。推測の入力・補完には全種使う |
| verify | オブジェクト | | Clade と同じ形式 |

## ゲーム側の挙動（データとの関係）

- 補完は `ja`・`sci`・`aliases` を対象に、NFKC 正規化・カタカナ→ひらがな変換・空白と中黒の除去をしてから部分一致で探す。前方一致と和名を優先。
- 共通祖先は `parent` をたどって求める。背骨には根から共通祖先までの全クレードを表示する。
- 出題：`answerable` が false でない種を対象に、まず `selection.buckets` の枠（＋その他の門）を等確率で選び、枠の中で `selection.phylumWeight` に従って門を選び、門内で一様に1種を選ぶ。`selection.realCounts` があるときは、`ranks[0]` の群を実際の種数（`top` が sqrt ならその平方根）に比例して選び、その中で `ranks[1]` の群を実際の種数に比例して選び（`ranks[1]` の無い種と数の無い群の種は「残り」にまとめ、外側の種数から中の群の種数を引いた数を重みにする）、最後に tierWeights の重みで1種を選ぶ。収録数の多い・少ないは出題の割合に効かない。
- 推測中は「残り何種」を表示しない（図鑑では収録数を表示）。今日の動物は「日本時間の日付＋datasetVersion」から決まる。
