# -*- coding: utf-8 -*-
"""data.json を生成・検証するスクリプト。

使い方:  python3 tools/build_data.py data-<版>.json
データの正本はこのファイル。data.json は生成物。
スキーマは docs/SCHEMA.md を参照。
"""
import json, sys

META = {
    "schemaVersion": 1,
    "datasetVersion": "0.2.0",
    "title": "和名版・動物系統あて 代表種データ（初版）",
    "referenceDate": "2026-10-21",
    "taxonomy": {
        "backbone": "NCBI Taxonomy / Open Tree of Life の構成を参考に手作業で編集",
        "nomenclature": "学名は GBIF Backbone / Catalogue of Life (ChecklistBank 3LR) / WoRMS の多数決で照合（2026-10-22、tools/name_consensus.py）。魚類の基準である Eschmeyer's Catalog of Fishes とは未照合",
        "phylogenyNotes": "主要分岐は分子系統（系統ゲノム解析）に基づく。動物の根元、ParaHoxozoa内、左右相称動物の根元、毛顎動物、二胚動物・直泳動物などの位置は議論中のため多分岐で表現。",
        "nonMonophyleticGroupsExcluded": ["魚類", "爬虫類（鳥類を除く）", "甲殻類", "無脊椎動物", "原索動物"]
    },
    "japaneseNameSources": [
        "日本鳥類目録 改訂第8版（日本鳥学会）",
        "日本産哺乳類の標準和名（日本哺乳類学会）",
        "日本産爬虫両生類標準和名リスト（日本爬虫両棲類学会）",
        "日本産魚類全種の学名（中坊編）/ 魚類の標準和名",
        "日本昆虫目録",
        "BISMaL（海洋生物多様性情報システム）"
    ],
    "status": "学名と和名を GBIF・Catalogue of Life・WoRMS・Wikidata・iNaturalist と照合済み（2026-10-22）。標準和名リストとの手作業の突き合わせは未実施。verify が付いた項目は特に要確認。",
    "licenseNotes": "外部リストのデータは同梱していない（名前は事実情報として個別に記載）。外部リストを一括取り込みする際は各利用規約を確認すること。",
    "selection": {
        "maxGuesses": 15, "dailyEpoch": "2026-10-21",
        "buckets": ["chordata", "arthropoda", "mollusca", "annelida", "cnidaria",
                    "echinodermata", "platyhelminthes", "nematoda"],
        "otherBucketLabel": "その他の門",
        "phylumWeight": "sqrt"
    }
}

clades = []
species = []

def C(id, parent, ja, sci, rank, desc, poly=None, v=None, jaReading=None):
    d = {"id": id, "parent": parent, "ja": ja, "sci": sci, "rank": rank, "desc": desc}
    if poly: d["polytomy"] = poly
    if v: d["verify"] = v
    clades.append(d)

def S(id, parent, ja, sci, fact, aliases=(), v=None, jaStatus="standard"):
    d = {"id": id, "parent": parent, "ja": ja, "sci": sci, "jaStatus": jaStatus,
         "aliases": list(aliases), "fact": fact}
    if v: d["verify"] = v
    species.append(d)

# ---------------- 骨格 ----------------
C("metazoa", None, "動物界", "Metazoa", "界",
  "多細胞で、コラーゲンを含む細胞外基質をもち、多くは胚発生で原腸を作る生物のまとまり。",
  poly="海綿動物・有櫛動物・それ以外（ParaHoxozoa）のどれが最初に分かれたかは議論中（有櫛動物が先とする解析が近年は優勢）。ここでは三分岐で示す。")

# 海綿
C("porifera", "metazoa", "海綿動物門", "Porifera", "門",
  "襟細胞で水流を起こし、体内の水路で濾過食する。神経や筋肉をもたない。")
C("hexactinellida", "porifera", "六放海綿綱", "Hexactinellida", "綱", "ケイ酸質の六放射の骨片をもつ深海性の海綿。ガラス海綿とも呼ばれる。")
C("demospongiae", "porifera", "普通海綿綱", "Demospongiae", "綱", "現生海綿の大半を占めるグループ。")
S("kairodokets", "hexactinellida", "カイロウドウケツ", "Euplectella aspergillum",
  "網かごのような骨格の中に、ドウケツエビのつがいが閉じこめられて一生を過ごすことがある。", ["偕老同穴"])
S("kuroisokaimen", "demospongiae", "クロイソカイメン", "Halichondria okadai",
  "下痢性貝毒のオカダ酸は、この海綿から最初に見つかり学名にちなんで名づけられた。")

# 有櫛
C("ctenophora", "metazoa", "有櫛動物門", "Ctenophora", "門",
  "繊毛が板状に並んだ櫛板を打って泳ぐ。刺胞をもたず、多くは粘着細胞で獲物を捕まえる。")
S("kabutokurage", "ctenophora", "カブトクラゲ", "Bolinopsis mikado",
  "クラゲと呼ばれるが刺胞動物ではない。櫛板が光を散乱して虹色に光って見える。", ["クシクラゲ"])
S("urikurage", "ctenophora", "ウリクラゲ", "Beroe cucumis",
  "触手をもたず、大きな口でほかのクシクラゲを丸のみにする。",
  ["クシクラゲ"], v={"sci": "日本産個体群の種同定は再検討の余地あり"})

C("parahoxozoa", "metazoa", "ParaHoxozoa", "ParaHoxozoa", "クレード",
  "板形動物・刺胞動物・左右相称動物をまとめたクレード。Hox/ParaHox遺伝子をもつことにちなむ。",
  poly="板形動物・刺胞動物・左右相称動物の三者の分岐順は議論中のため多分岐で示す。",
  v={"ja": "定着した和名が確認できないため学名で表記"})

C("placozoa", "parahoxozoa", "板形動物門", "Placozoa", "門",
  "数種類の細胞だけからなる、平たく薄い体の動物。決まった形も口もない。")
S("senmohirahamushi", "placozoa", "センモウヒラムシ", "Trichoplax adhaerens",
  "体の構造が動物の中でも最も単純な部類で、ゲノムは小さいが多くの発生関連遺伝子をもつ。",
  ["トリコプラックス"], v={"sci": "日本産の個体が本種か別種かは要確認（遺伝的に多様）"})

# 刺胞
C("cnidaria", "parahoxozoa", "刺胞動物門", "Cnidaria", "門",
  "刺胞という毒針の細胞小器官をもつ。ポリプとクラゲの二つの体制がある。",
  poly="ミクソゾアが鉢・箱・ヒドロ虫と同じクラゲ類の側に入るとする解析があるが、ここでは三分岐で示す。")
C("anthozoa", "cnidaria", "花虫綱", "Anthozoa", "綱", "クラゲ世代をもたず、一生ポリプで過ごす。サンゴやイソギンチャク。")
C("hexacorallia", "anthozoa", "六放サンゴ亜綱", "Hexacorallia", "亜綱", "触手や隔膜が6の倍数で並ぶ。イシサンゴやイソギンチャク。")
C("medusozoa", "cnidaria", "クラゲ亜門", "Medusozoa", "亜門", "生活史にクラゲの時期をもつ（二次的に失ったものもいる）グループ。",
  poly="鉢虫綱・箱虫綱・ヒドロ虫綱の関係は多分岐で示す。")
C("myxozoa", "cnidaria", "ミクソゾア", "Myxozoa", "クレード",
  "魚などに寄生する顕微鏡サイズの刺胞動物。かつては原生生物とされていた。")
S("usuedamidoriishi", "hexacorallia", "ウスエダミドリイシ", "Acropora tenuis",
  "体内に褐虫藻を共生させ、光合成産物をもらって成長する造礁サンゴ。", ["サンゴ", "ミドリイシ"])
S("umeboshiisogin", "hexacorallia", "ウメボシイソギンチャク", "Actinia equina",
  "潮が引くと触手をしまい、赤い梅干しのような姿になる。", ["イソギンチャク"],
  v={"sci": "日本産の個体群を Actinia equina とすることには異論あり"})
S("mizukurage", "medusozoa", "ミズクラゲ", "Aurelia coerulea",
  "四つ葉のように見える模様は生殖腺。日本産はかつて A. aurita とされた。", ["クラゲ"])
S("echizenkurage", "medusozoa", "エチゼンクラゲ", "Nemopilema nomurai",
  "傘の直径が1 m以上になる大型種。大量発生すると漁業被害を出す。")
S("andonkurage", "medusozoa", "アンドンクラゲ", "Carybdea brevipedalia",
  "箱虫類は目をもち、レンズのある眼で障害物を避けて泳ぐ。")
S("katsuonoeboshi", "medusozoa", "カツオノエボシ", "Physalia physalis",
  "一匹に見えて、役割の異なる多数の個体が集まった群体。", ["電気クラゲ"],
  v={"sci": "近年の研究で複数種に分けられ、日本近海の個体の学名は要確認"})
S("nanahoshikudoa", "myxozoa", "ナナホシクドア", "Kudoa septempunctata",
  "ヒラメの筋肉に寄生し、生食による一過性の食中毒の原因になる。", ["クドア"])

# ---------------- 左右相称 ----------------
C("bilateria", "parahoxozoa", "左右相称動物", "Bilateria", "クレード",
  "体に前後・背腹・左右の軸をもち、三胚葉からなる動物。",
  poly="珍無腸動物が新口動物の中に入る（水腔動物と姉妹群、Xenambulacraria）か、ほかの左右相称動物全体の姉妹群かは議論中。新口動物の単系統性にも疑問が出ているため、ここでは三分岐で示す。")
C("xenacoelomorpha", "bilateria", "珍無腸動物門", "Xenacoelomorpha", "門",
  "肛門も体腔もない、単純な体の左右相称動物。珍渦虫と無腸動物などを含む。")
S("xenoturbella", "xenacoelomorpha", "ゼノターベラ・ジャポニカ", "Xenoturbella japonica",
  "2016年に日本近海から記載された珍渦虫の一種。口しかない袋のような体をもつ。",
  ["珍渦虫", "チンウズムシ", "ちんうずむし"], jaStatus="provisional", v={"ja": "標準和名は未確認（学名の音写）"})
S("praesagittifera", "xenacoelomorpha", "ナイカイムチョウウズムシ", "Praesagittifera naikaiensis",
  "瀬戸内海の砂浜にすむ無腸動物。体内に緑藻を共生させて緑色に見える。",
  ["無腸動物", "ムチョウドウブツ", "プラエサギッティフェラ・ナイカイエンシス"], v={"ja": "和名は Wikidata・iNaturalist で一致。標準和名リストでは未確認"})

C("deuterostomia", "bilateria", "新口動物", "Deuterostomia", "クレード",
  "棘皮動物・半索動物（水腔動物）と脊索動物をまとめたクレード。",
  v={"placement": "単系統性を疑う解析もある"})
C("ambulacraria", "deuterostomia", "水腔動物", "Ambulacraria", "クレード",
  "棘皮動物と半索動物をまとめたクレード。幼生の形がよく似る。")
C("echinodermata", "ambulacraria", "棘皮動物門", "Echinodermata", "門",
  "成体は五放射相称で、水管系と管足をもつ。海にだけすむ。")
C("eleutherozoa", "echinodermata", "Eleutherozoa", "Eleutherozoa", "亜門", "固着しない棘皮動物。ウミユリ類以外のすべて。",
  v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
C("asterozoa", "eleutherozoa", "Asterozoa", "Asterozoa", "クレード", "ヒトデとクモヒトデ。系統ゲノム解析で姉妹群と支持された。",
  v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
C("echinozoa", "eleutherozoa", "Echinozoa", "Echinozoa", "クレード", "ウニとナマコ。", v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
S("nipponumishida", "echinodermata", "ニッポンウミシダ", "Anneissia japonica",
  "ウミユリ類の仲間で、腕を羽ばたかせて泳ぐこともできる。旧学名は Oxycomanthus japonicus。", ["ウミシダ", "ウミユリ"])
S("itomakihitode", "asterozoa", "イトマキヒトデ", "Patiria pectinifera",
  "糸巻きのような五角形のヒトデ。発生学の研究材料として古くから使われる。", ["ヒトデ"])
S("nihonkumohitode", "asterozoa", "ニホンクモヒトデ", "Ophioplocus japonicus",
  "クモヒトデは細い腕をくねらせて素早く動く。", ["クモヒトデ"], v={"ja": "標準和名と学名の対応を要確認"})
S("murasakiuni", "echinozoa", "ムラサキウニ", "Heliocidaris crassispina",
  "食用にされるウニ。口には「アリストテレスの提灯」と呼ばれる咀嚼器がある。", ["ウニ"])
S("manamako", "echinozoa", "マナマコ", "Apostichopus japonicus",
  "ナマコはウニの仲間で、骨片が皮膚の中に散らばっている。", ["ナマコ"])
C("hemichordata", "ambulacraria", "半索動物門", "Hemichordata", "門", "ギボシムシとフサカツギ。咽頭に鰓裂をもつ。")
S("misakigiboshi", "hemichordata", "ミサキギボシムシ", "Balanoglossus misakiensis",
  "砂泥にすむ。鰓裂をもつことで脊索動物との共通祖先の姿を考える手がかりになる。", ["ギボシムシ"])

# 脊索動物
C("chordata", "deuterostomia", "脊索動物門", "Chordata", "門",
  "発生のある時期に脊索・背側神経管・鰓裂・肛門より後ろの尾をもつ。")
S("namekujiuo", "chordata", "ナメクジウオ", "Branchiostoma japonicum",
  "頭索動物。一生脊索をもち続け、脊椎動物の祖先の姿を考える材料になる。旧学名は B. belcheri とされることもあった。", ["頭索動物"])
C("olfactores", "chordata", "Olfactores", "Olfactores", "クレード", "尾索動物と脊椎動物をまとめたクレード。ナメクジウオより互いに近い。",
  v={"ja": "定着した和名が確認できないため学名で表記"})
C("tunicata", "olfactores", "尾索動物亜門", "Tunicata", "亜門", "セルロースを含む被嚢で体を包む。幼生はオタマジャクシ形。")
S("maboya", "tunicata", "マボヤ", "Halocynthia roretzi",
  "動物なのにセルロースを作れる。幼生期には脊索をもつ。", ["ホヤ"])
S("wakareotamaboya", "tunicata", "ワカレオタマボヤ", "Oikopleura dioica",
  "一生オタマジャクシ形で、自分で作った「ハウス」で餌を濾し取る。", ["オタマボヤ"])
C("vertebrata", "olfactores", "脊椎動物亜門", "Vertebrata", "亜門", "脊椎骨や頭蓋をもつ。神経堤細胞が多くの構造を作る。")
C("cyclostomata", "vertebrata", "円口類", "Cyclostomata", "クレード", "顎をもたない現生の脊椎動物。ヌタウナギとヤツメウナギ。")
S("nutaunagi", "cyclostomata", "ヌタウナギ", "Eptatretus burgeri",
  "大量の粘液を出して身を守る。韓国料理などで食用にされる。")
S("kawayatsume", "cyclostomata", "カワヤツメ", "Lethenteron camtschaticum",
  "目の後ろに7対の鰓孔が並び、目が8つあるように見える。", ["ヤツメウナギ"])
C("gnathostomata", "vertebrata", "顎口類", "Gnathostomata", "クレード", "顎をもつ脊椎動物。")
C("chondrichthyes", "gnathostomata", "軟骨魚綱", "Chondrichthyes", "綱", "骨格が軟骨でできている。サメ・エイ・ギンザメ。")
C("elasmobranchii", "chondrichthyes", "板鰓亜綱", "Elasmobranchii", "亜綱", "サメとエイ。鰓孔が体表に直接開く。")
S("jinbeizame", "elasmobranchii", "ジンベエザメ", "Rhincodon typus", "現生最大の魚類。プランクトンを濾して食べる。", ["サメ"])
S("akaei", "elasmobranchii", "アカエイ", "Hemitrygon akajei", "尾に毒のある棘をもつ。エイ類はサメ類の姉妹群で、鰓孔が腹側に開く。", ["エイ"])
S("ginzame", "chondrichthyes", "ギンザメ", "Chimaera phantasma", "全頭類の一種。サメ・エイとは古生代に分かれた。")
C("osteichthyes", "gnathostomata", "Osteichthyes", "Osteichthyes", "クレード",
  "硬い骨をもつ脊椎動物。条鰭類と肉鰭類（陸上脊椎動物を含む）からなる。和名の「硬骨魚類」は四肢動物を除いた魚だけの意味で使われることが多いので、ここでは学名のまま表記する。",
  v={"ja": "四肢動物を含む意味での定着した和名はないため学名で表記。従来名は硬骨魚類"})
C("actinopterygii", "osteichthyes", "条鰭綱", "Actinopterygii", "綱", "鰭が放射状の鰭条で支えられる魚。脊椎動物の種数の約半分を占める。")
S("mikadochozame", "actinopterygii", "ミカドチョウザメ", "Acipenser mikadoi", "チョウザメは軟質類で、硬い鱗が体に並ぶ古いタイプの条鰭類。", ["チョウザメ"])
C("teleostei", "actinopterygii", "真骨類", "Teleostei", "クレード", "条鰭類の大部分を占めるグループ。祖先で全ゲノム重複が起きた。")
S("nihonunagi", "teleostei", "ニホンウナギ", "Anguilla japonica", "マリアナ諸島西方の海で産卵し、レプトケファルス幼生として日本へ来る。", ["ウナギ"])
C("clupeocephala", "teleostei", "Clupeocephala", "Clupeocephala", "クレード",
  "真骨類のうちカライワシ類・アロワナ類以外。", v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
S("maiwashi", "clupeocephala", "マイワシ", "Sardinops melanostictus", "数十年周期で漁獲量が大きく増減する。", ["イワシ", "Sardinops sagax"],
  v={"sci": "GBIF・WoRMS は世界のマイワシ属を Sardinops sagax 1種にまとめる。日本の文献では S. melanostictus を使うことが多く、ここでは後者を採用（要確認）"})
S("koi", "clupeocephala", "コイ", "Cyprinus carpio", "喉の奥にある咽頭歯で餌をすりつぶす。")
C("percomorpha", "clupeocephala", "スズキ系", "Percomorpha", "クレード", "棘鰭類の中心となる大きなグループ。ペルカ目（Perciformes）のほか、フグ目・ダツ目・ハゼ目・アジ目（ヒラメ・カレイ類を含む）など多くの目を含む。")
S("minamimedaka", "percomorpha", "ミナミメダカ", "Oryzias latipes", "日本のメダカは2種に分けられ、本種は本州の太平洋側以南に分布する。", ["メダカ"])
S("kuromaguro", "percomorpha", "クロマグロ", "Thunnus orientalis", "体温を水温より高く保つ仕組みをもつ。", ["マグロ", "ホンマグロ"])
S("tatsunootoshigo", "percomorpha", "タツノオトシゴ", "Hippocampus coronatus", "雄の育児嚢で卵を育てる。")
S("madai", "percomorpha", "マダイ", "Pagrus major", "鮮やかな赤色は餌のエビなどに含まれる色素による。", ["タイ"])
C("sarcopterygii", "osteichthyes", "肉鰭類", "Sarcopterygii", "クレード", "肉質の鰭をもつ魚と、その子孫である四肢動物。")
S("coelacanth", "sarcopterygii", "シーラカンス", "Latimeria chalumnae", "1938年に南アフリカ沖で生きた個体が見つかった。", ["ラティメリア"])
C("rhipidistia", "sarcopterygii", "Rhipidistia", "Rhipidistia", "クレード", "ハイギョと四肢動物をまとめたクレード。", v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
S("australiahaigyo", "rhipidistia", "オーストラリアハイギョ", "Neoceratodus forsteri", "鰓に加えて肺で呼吸できる。四肢動物に最も近い現生の魚類の一つ。", ["ハイギョ"])
C("tetrapoda", "rhipidistia", "四肢動物", "Tetrapoda", "クレード", "四肢をもつ（または祖先がもっていた）脊椎動物。")
C("amphibia", "tetrapoda", "両生綱", "Amphibia", "綱", "多くは水中で幼生期を過ごし、変態して陸に上がる。")
S("nihonamagaeru", "amphibia", "ニホンアマガエル", "Dryophytes japonicus", "指先の吸盤で垂直な壁も登れる。", ["アマガエル", "カエル"])
S("osanshouo", "amphibia", "オオサンショウウオ", "Andrias japonicus", "全長1 mを超える世界最大級の両生類。特別天然記念物。", ["サンショウウオ"])
S("akaharaimori", "amphibia", "アカハライモリ", "Cynops pyrrhogaster", "失った手足や目のレンズまで再生できる。", ["イモリ", "ニホンイモリ"])
C("amniota", "tetrapoda", "有羊膜類", "Amniota", "クレード", "羊膜に包まれた卵（胚）で、陸上で発生できる脊椎動物。")
C("mammalia", "amniota", "哺乳綱", "Mammalia", "綱", "乳で子を育て、体毛をもつ。")
S("kamonohashi", "mammalia", "カモノハシ", "Ornithorhynchus anatinus", "卵を産む哺乳類（単孔類）。くちばしで獲物の電気を感じ取る。")
C("theria", "mammalia", "獣亜綱", "Theria", "亜綱", "子を産む哺乳類。有袋類と有胎盤類。")
S("akakangaroo", "theria", "アカカンガルー", "Osphranter rufus", "未熟な子を産み、袋の中で育てる。旧学名は Macropus rufus。", ["カンガルー"])
C("placentalia", "theria", "有胎盤類", "Placentalia", "クレード", "胎盤で胎児を長く育てる哺乳類。",
  poly="アフリカ獣類・異節類・北方真獣類の分岐順は議論中のため、ここでは多分岐で示す（異節類は未収録）。")
S("africazou", "placentalia", "アフリカゾウ", "Loxodonta africana", "アフリカ獣類の一員で、ハイラックスやジュゴンと近縁。", ["ゾウ"])
C("boreoeutheria", "placentalia", "北方真獣類", "Boreoeutheria", "クレード", "真主齧類とローラシア獣類をまとめたクレード。")
C("euarchontoglires", "boreoeutheria", "真主齧類", "Euarchontoglires", "クレード", "霊長類・齧歯類・ウサギ類など。")
C("primates", "euarchontoglires", "霊長目", "Primates", "目", "ものをつかむ手と前を向いた目をもつ。")
S("hito", "primates", "ヒト", "Homo sapiens", "現生のヒト属はこの1種だけ。", ["人間", "人"])
S("nihonzaru", "primates", "ニホンザル", "Macaca fuscata", "ヒト以外の霊長類で最も北に分布する。", ["サル"])
S("hatsukanezumi", "euarchontoglires", "ハツカネズミ", "Mus musculus", "実験用マウスの元になった種。", ["マウス", "ネズミ"])
C("laurasiatheria", "boreoeutheria", "ローラシア獣類", "Laurasiatheria", "クレード",
  "分子系統で見つかったクレード。コウモリ・食肉類・鯨偶蹄類など。", poly="内部の分岐順は議論があるため多分岐で示す。")
S("kikugashira", "laurasiatheria", "キクガシラコウモリ", "Rhinolophus nippon", "鼻から超音波を出してエコーロケーションする。日本産は R. ferrumequinum から分けられた。", ["コウモリ"])
C("carnivora", "laurasiatheria", "食肉目", "Carnivora", "目", "肉を切り裂く裂肉歯をもつ。")
S("tanuki", "carnivora", "タヌキ", "Nyctereutes viverrinus", "イヌ科で冬眠に近い冬ごもりをする。", ["ホンドタヌキ"],
  v={"sci": "日本産を独立種 N. viverrinus とするか N. procyonoides の亜種とするかで扱いが分かれる"})
S("tsukinowaguma", "carnivora", "ツキノワグマ", "Ursus thibetanus", "胸の三日月形の白い模様が名前の由来。", ["クマ"])
C("artiodactyla", "laurasiatheria", "鯨偶蹄目", "Artiodactyla", "目", "偶蹄類とクジラ類。クジラはカバに最も近い。", v={"sci": "Cetartiodactyla と表記されることもある"})
S("inoshishi", "artiodactyla", "イノシシ", "Sus scrofa", "家畜のブタの祖先。", ["ブタ"])
C("cetruminantia", "artiodactyla", "Cetruminantia", "Cetruminantia", "クレード", "反芻類とクジラ・カバ類をまとめたクレード。", v={"ja": "定着した和名が確認できないため学名で表記。日本語版ウィキペディアに「鯨反芻亜目」とあるが学術文献での使用は未確認"})
S("nihonjika", "cetruminantia", "ニホンジカ", "Cervus nippon", "胃が4つあり反芻する。雄の角は毎年生え変わる。", ["シカ"])
S("shironagasu", "cetruminantia", "シロナガスクジラ", "Balaenoptera musculus", "地球史上最大級の動物。ヒゲ板でオキアミを濾して食べる。", ["クジラ"])
C("sauropsida", "amniota", "Sauropsida", "Sauropsida", "クレード", "鳥類を含む「爬虫類」の系統。鳥を除いた爬虫類は単系統ではない。", v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
C("lepidosauria", "sauropsida", "鱗竜類", "Lepidosauria", "クレード", "有鱗類（トカゲ・ヘビ）とムカシトカゲ。")
S("mukashitokage", "lepidosauria", "ムカシトカゲ", "Sphenodon punctatus", "トカゲに似るが別の目（喙頭目）の唯一の生き残り。", ["トゥアタラ"])
C("squamata", "lepidosauria", "有鱗目", "Squamata", "目", "トカゲとヘビ。ヘビはトカゲの中から生まれた。")
S("nihonyamori", "squamata", "ニホンヤモリ", "Gekko japonicus", "指の裏の微細な毛で壁や天井に張りつく。", ["ヤモリ"])
S("aodaisho", "squamata", "アオダイショウ", "Elaphe climacophora", "日本最大級のヘビ。毒はない。", ["ヘビ"])
C("archelosauria", "sauropsida", "Archelosauria", "Archelosauria", "クレード",
  "カメ類と主竜類をまとめたクレード。カメはワニ・鳥に近いことが分子系統で示された。", v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
S("akaumigame", "archelosauria", "アカウミガメ", "Caretta caretta", "日本の砂浜は北太平洋で主要な産卵地。", ["カメ", "ウミガメ"])
C("archosauria", "archelosauria", "主竜類", "Archosauria", "クレード", "ワニ類と鳥類（恐竜を含む）。")
S("iriewani", "archosauria", "イリエワニ", "Crocodylus porosus", "現生最大の爬虫類。ワニに最も近い現生動物は鳥。", ["ワニ"])
C("aves", "archosauria", "鳥綱", "Aves", "綱", "羽毛と翼をもつ恐竜の子孫。")
S("dachou", "aves", "ダチョウ", "Struthio camelus", "古顎類。現生最大の鳥。")
C("neognathae", "aves", "新顎類", "Neognathae", "クレード", "古顎類以外の鳥。")
C("galloanserae", "neognathae", "キジカモ類", "Galloanserae", "クレード", "キジ目とカモ目。")
S("sekishokuyakei", "galloanserae", "セキショクヤケイ", "Gallus gallus", "ニワトリの祖先。", ["ニワトリ"])
S("magamo", "galloanserae", "マガモ", "Anas platyrhynchos", "アヒルの祖先。", ["カモ", "アヒル"])
C("neoaves", "neognathae", "新鳥類", "Neoaves", "クレード", "現生の鳥のほとんどを含む。", poly="内部の分岐は急速放散のため解像が難しい。")
C("aequornithes", "neoaves", "Aequornithes", "Aequornithes", "クレード", "ペンギン・コウノトリ・ペリカン・トキなど。", v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
S("toki", "aequornithes", "トキ", "Nipponia nippon", "学名に日本の名を持つ。日本の野生個体は一度絶滅し、再導入された。")
S("kouteipenguin", "aequornithes", "コウテイペンギン", "Aptenodytes forsteri", "南極の冬に雄が足の上で卵を温める。", ["ペンギン"])
C("passeriformes", "neoaves", "スズメ目", "Passeriformes", "目", "鳥類の種の半数以上を占める。")
S("hashibutogarasu", "passeriformes", "ハシブトガラス", "Corvus macrorhynchos", "道具を使うなど高い知能で知られる。", ["カラス"])
S("suzume", "passeriformes", "スズメ", "Passer montanus", "人の暮らしのそばで繁殖する。ヨーロッパでは同じ役回りを近縁のイエスズメが担う。")

# ---------------- 前口動物 ----------------
C("protostomia", "bilateria", "前口動物", "Protostomia", "クレード", "脱皮動物とらせん卵割動物をまとめたクレード。",
  poly="毛顎動物は前口動物の中の位置が定まっていない（顎口動物などと近いとする解析もある）ため、ここでは三分岐で示す。")
C("chaetognatha", "protostomia", "毛顎動物門", "Chaetognatha", "門", "頭部の顎毛で獲物を捕らえる矢のような形の海洋動物。")
S("isoyamushi", "chaetognatha", "イソヤムシ", "Paraspadella gotoi", "海藻などに体をはりつけて待ち伏せする底生のヤムシ。", ["ヤムシ"], v={"ja": "標準和名と学名の対応を要確認"})

C("ecdysozoa", "protostomia", "脱皮動物", "Ecdysozoa", "クレード", "成長のためにクチクラを脱ぎ捨てる（脱皮する）動物。分子系統で見つかった。")
C("scalidophora", "ecdysozoa", "有棘動物", "Scalidophora", "クレード", "吻に棘をもつ小さな動物。エラヒキムシ・トゲカワ・コウラムシ。")
C("priapulida", "scalidophora", "鰓曳動物門", "Priapulida", "門", "海底の泥にすむ。カンブリア紀の化石によく似た仲間がいる。")
S("erahikimushi", "priapulida", "エラヒキムシ", "Priapulus caudatus", "尾の付属器で呼吸するとされる。", v={"ja": "日本での標準和名の対応を要確認"})
C("kinorhyncha", "scalidophora", "動吻動物門", "Kinorhyncha", "門", "体節状の1 mm以下の動物。トゲカワと呼ばれる。")
S("echinoderes", "kinorhyncha", "エキノデレス・オオツカイ", "Echinoderes ohtsukai", "日本の干潟から記載されたトゲカワの一種。", ["トゲカワ"], jaStatus="provisional", v={"ja": "和名なし（学名の音写）"})
C("loricifera", "scalidophora", "胴甲動物門", "Loricifera", "門", "1983年に記載された最も新しい門の一つ。体は0.5 mm以下。")
S("nanaloricus", "loricifera", "ナナロリクス・ミスティクス", "Nanaloricus mysticus", "胴甲動物で最初に記載された種。", ["コウラムシ"], jaStatus="provisional", v={"ja": "和名なし（学名の音写）、日本産ではない"})
C("nematoida", "ecdysozoa", "糸形動物", "Nematoida", "クレード", "線虫とハリガネムシ。")
C("nematoda", "nematoida", "線形動物門", "Nematoda", "門", "線虫。土や海、他の生物の体内などあらゆる環境にいる。")
S("celegans", "nematoda", "シー・エレガンス", "Caenorhabditis elegans", "全細胞の系譜が分かっているモデル生物。", ["線虫", "エレガンス"], jaStatus="common", v={"ja": "標準和名ではなく通称"})
S("kaichu", "nematoda", "ヒトカイチュウ", "Ascaris lumbricoides", "かつて日本人の多くが感染していた寄生虫。", ["カイチュウ", "回虫"])
S("matsunozaisenchu", "nematoda", "マツノザイセンチュウ", "Bursaphelenchus xylophilus", "マツ材線虫病（松枯れ）の原因。カミキリムシに運ばれる。")
C("nematomorpha", "nematoida", "類線形動物門", "Nematomorpha", "門", "幼生は昆虫などに寄生し、成体は水中で暮らす。")
S("chordodes", "nematomorpha", "コルドデス・ヤポネンシス", "Chordodes japonensis", "カマキリなどに寄生するハリガネムシの一種。宿主を水辺に向かわせる。", ["ハリガネムシ"], jaStatus="provisional", v={"ja": "標準和名は未確認（学名の音写）"})
C("panarthropoda", "ecdysozoa", "汎節足動物", "Panarthropoda", "クレード", "脚をもつ脱皮動物。",
  poly="クマムシ・カギムシ・節足動物の関係は議論中のため多分岐で示す。")
C("tardigrada", "panarthropoda", "緩歩動物門", "Tardigrada", "門", "クマムシ。乾燥すると樽状になり、極端な環境に耐える。")
S("yokozunakumamushi", "tardigrada", "ヨコヅナクマムシ", "Ramazzottius varieornatus", "日本で研究が進むクマムシ。放射線から DNA を守るタンパク質をもつ。", ["クマムシ"])
C("onychophora", "panarthropoda", "有爪動物門", "Onychophora", "門", "カギムシ。粘液を発射して獲物を捕らえる。南半球と熱帯に分布。")
S("euperipatoides", "onychophora", "ユーペリパトイデス・ロウェリ", "Euperipatoides rowelli", "オーストラリア産のカギムシ。研究によく使われる。", ["カギムシ"], jaStatus="provisional", v={"ja": "和名なし（学名の音写）、日本産ではない"})
C("arthropoda", "panarthropoda", "節足動物門", "Arthropoda", "門", "外骨格と関節のある脚をもつ。既知の動物種の大半を占める。")
C("chelicerata", "arthropoda", "鋏角亜門", "Chelicerata", "亜門", "口の前にはさみ状の鋏角をもつ。")
S("umigumo", "chelicerata", "フタツメイソウミグモ", "Ammothella biunguiculata", "ウミグモは体が細く、内臓が脚の中まで伸びている。", ["ウミグモ", "ウミグモの一種"],
  v={"ja": "和名は GBIF・iNaturalist で一致。標準和名リストでは未確認"})
C("euchelicerata", "chelicerata", "真鋏角類", "Euchelicerata", "クレード", "カブトガニとクモ形類。",
  poly="カブトガニがクモ形類の内側に入るとする解析が増えているため、多分岐で示す。")
S("kabutogani", "euchelicerata", "カブトガニ", "Tachypleus tridentatus", "名前にカニとつくがクモやサソリに近い。青い血液をもつ。")
S("jorougumo", "euchelicerata", "ジョロウグモ", "Trichonephila clavata", "黄色い糸で大きな網を張る。旧学名は Nephila clavata。", ["クモ"])
S("yaeyamasasori", "euchelicerata", "ヤエヤマサソリ", "Liocheles australasiae", "日本に分布するサソリの一種。毒は弱い。", ["サソリ"])
S("futatogechimadani", "euchelicerata", "フタトゲチマダニ", "Haemaphysalis longicornis", "SFTSなどの病原体を媒介することがある。", ["ダニ", "マダニ"])
C("mandibulata", "arthropoda", "大顎類", "Mandibulata", "クレード", "大顎をもつ節足動物。多足類と汎甲殻類。")
C("myriapoda", "mandibulata", "多足亜門", "Myriapoda", "亜門", "ムカデやヤスデなど、多数の脚をもつ。")
S("tobizumukade", "myriapoda", "トビズムカデ", "Scolopendra mutilans", "第1脚が変化した顎肢で毒を注入する。", ["ムカデ"], v={"sci": "S. subspinipes mutilans とする扱いもある"})
S("yakeyasude", "myriapoda", "ヤケヤスデ", "Oxidus gracilis", "ヤスデは体節ごとに2対の脚をもつ。", ["ヤスデ"])
C("pancrustacea", "mandibulata", "汎甲殻類", "Pancrustacea", "クレード",
  "甲殻類と六脚類（昆虫など）をまとめたクレード。昆虫は甲殻類の中から生まれたので、甲殻類は単系統ではない。",
  poly="貝虫類などを含む Oligostraca、Multicrustacea、Allotriocarida の関係は多分岐で示す。")
C("oligostraca", "pancrustacea", "Oligostraca", "Oligostraca", "クレード", "貝形虫やシタムシなどをまとめたクレード。", v={"ja": "定着した和名が確認できないため学名で表記。日本語版ウィキペディアに「貧甲殻上綱」とあるが学術文献での使用は未確認"})
S("umihotaru", "oligostraca", "ウミホタル", "Vargula hilgendorfii", "貝形虫の一種。発光物質を海中に吐き出して青く光る。")
C("multicrustacea", "pancrustacea", "Multicrustacea", "Multicrustacea", "クレード", "軟甲類・カイアシ類・鞘甲類をまとめたクレード。", v={"ja": "定着した和名が確認できないため学名で表記。日本語版ウィキペディアに「多甲殻上綱」とあるが学術文献での使用は未確認"})
S("kamenote", "multicrustacea", "カメノテ", "Capitulum mitella", "フジツボの仲間（鞘甲類）。岩に固着し、蔓脚で餌を集める。", ["フジツボ"])
C("malacostraca", "multicrustacea", "軟甲綱", "Malacostraca", "綱", "エビ・カニ・ダンゴムシ・オキアミなど。")
S("okadangomushi", "malacostraca", "オカダンゴムシ", "Armadillidium vulgare", "陸にすむ甲殻類（等脚類）。丸まって身を守る。", ["ダンゴムシ"])
S("nankyokuokiami", "malacostraca", "ナンキョクオキアミ", "Euphausia superba", "南極の生態系を支える。総重量は地球上の野生動物で最大級。", ["オキアミ"])
C("decapoda", "malacostraca", "十脚目", "Decapoda", "目", "エビ・カニ・ヤドカリなど。")
S("americazarigani", "decapoda", "アメリカザリガニ", "Procambarus clarkii", "1927年に食用ガエルの餌として日本に持ち込まれた。条件付特定外来生物。", ["ザリガニ"])
S("zuwaigani", "decapoda", "ズワイガニ", "Chionoecetes opilio", "地方によりマツバガニ・エチゼンガニと呼ばれる。", ["カニ", "マツバガニ", "エチゼンガニ"])
S("kurumaebi", "decapoda", "クルマエビ", "Penaeus japonicus", "丸まると縞模様が車輪のように見える。Marsupenaeus 属とする扱いもある。", ["エビ"])
C("allotriocarida", "pancrustacea", "Allotriocarida", "Allotriocarida", "クレード", "鰓脚類・ムカデエビ類・六脚類をまとめたクレード。", v={"ja": "定着した和名が確認できないため学名で表記"})
C("branchiopoda", "allotriocarida", "鰓脚綱", "Branchiopoda", "綱", "ミジンコやホウネンエビなど。脚に鰓がある。")
S("mijinko", "branchiopoda", "ミジンコ", "Daphnia pulex", "条件が良いと雌だけで単為生殖して増える。", v={"sci": "日本産個体群の種名は再検討中"})
S("hounenebi", "branchiopoda", "ホウネンエビ", "Branchinella kugenumaensis", "田んぼに現れ、背を下にして泳ぐ。多いと豊年になるといわれた。")
C("hexapoda", "allotriocarida", "六脚亜門", "Hexapoda", "亜門", "3対の脚をもつ。昆虫とトビムシなど。")
S("mizutobimushi", "hexapoda", "ミズトビムシ", "Podura aquatica", "トビムシは腹部の跳躍器で跳ねる。昆虫ではない六脚類。", ["トビムシ"], v={"ja": "標準和名の確認が必要"})
C("insecta", "hexapoda", "昆虫綱", "Insecta", "綱", "体が頭・胸・腹に分かれ、胸に3対の脚をもつ。")
C("pterygota", "insecta", "有翅昆虫亜綱", "Pterygota", "亜綱", "翅をもつ（または祖先がもっていた）昆虫。",
  poly="トンボ類・カゲロウ類・新翅類の分岐順は議論中。")
S("akiakane", "pterygota", "アキアカネ", "Sympetrum frequens", "夏は高地で過ごし、秋に平地へ降りてくる。", ["赤とんぼ", "トンボ"])
C("neoptera", "pterygota", "新翅類", "Neoptera", "クレード", "翅を背中に折りたためる昆虫。")
C("polyneoptera", "neoptera", "多新翅類", "Polyneoptera", "クレード", "バッタ・ゴキブリ・カマキリなど。")
S("tonosamabatta", "polyneoptera", "トノサマバッタ", "Locusta migratoria", "密度が高くなると体色や行動が変わる「相変異」を起こす。", ["バッタ"])
C("blattodea", "polyneoptera", "ゴキブリ目", "Blattodea", "目", "ゴキブリとシロアリ。シロアリは社会性のゴキブリといえる。")
S("kurogokiburi", "blattodea", "クロゴキブリ", "Periplaneta fuliginosa", "日本の家屋でよく見られる。", ["ゴキブリ"])
S("yamatoshiroari", "blattodea", "ヤマトシロアリ", "Reticulitermes speratus", "アリではなくゴキブリの仲間。腸内微生物の力で木を消化する。", ["シロアリ"])
S("aburazemi", "neoptera", "アブラゼミ", "Graptopsaltria nigrofuscata", "半翅目（カメムシ目）。口吻で木の汁を吸う。", ["セミ"])
C("holometabola", "neoptera", "完全変態類", "Holometabola", "クレード", "幼虫・蛹・成虫と完全変態する昆虫。")
C("hymenoptera", "holometabola", "ハチ目", "Hymenoptera", "目", "ハチとアリ。完全変態類で最初に分かれた。")
S("seiyomitsubachi", "hymenoptera", "セイヨウミツバチ", "Apis mellifera", "8の字ダンスで蜜源の方向と距離を伝える。", ["ミツバチ", "ハチ"])
S("kurooari", "hymenoptera", "クロオオアリ", "Camponotus japonicus", "アリはハチから生まれたグループ。", ["アリ"])
C("coleoptera", "holometabola", "コウチュウ目", "Coleoptera", "目", "前翅が硬い鞘翅になった甲虫。動物で最も種数の多い目。")
S("kabutomushi", "coleoptera", "カブトムシ", "Trypoxylus dichotomus", "雄の角は幼虫期に作られる。")
S("nanahoshitentou", "coleoptera", "ナナホシテントウ", "Coccinella septempunctata", "アブラムシを食べる。", ["テントウムシ"])
C("mecopterida", "holometabola", "Mecopterida", "Mecopterida", "クレード", "チョウ目・トビケラ目・ハエ目・シリアゲムシ目などを含む。", v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
S("monshirocho", "mecopterida", "モンシロチョウ", "Pieris rapae", "幼虫はキャベツなどアブラナ科を食べる。", ["チョウ"])
S("kaiko", "mecopterida", "カイコ", "Bombyx mori", "野生のクワコから家畜化され、人の世話なしには生きられない。", ["蚕"])
S("drosophila", "mecopterida", "キイロショウジョウバエ", "Drosophila melanogaster", "遺伝学の代表的なモデル生物。", ["ショウジョウバエ", "ハエ"])
S("hitosujishimaka", "mecopterida", "ヒトスジシマカ", "Aedes albopictus", "デング熱などのウイルスを媒介する。", ["カ", "蚊", "ヤブカ"])

# らせん卵割
C("spiralia", "protostomia", "らせん卵割動物", "Spiralia", "クレード",
  "らせん卵割を祖先形質とする前口動物。冠輪動物・扁形動物・顎口動物など。",
  poly="扁形動物・腹毛動物・顎口動物類・冠輪動物・二胚動物・直泳動物の関係は議論中のため多分岐で示す。")
C("gnathifera", "spiralia", "担顎動物", "Gnathifera", "クレード", "咽頭に複雑な顎をもつ微小な動物のまとまり。有顎動物とも呼ぶ。")
C("gnathostomulida", "gnathifera", "顎口動物門", "Gnathostomulida", "門", "海底の砂のすきまにすむ1 mm前後の動物。")
S("gnathostomula", "gnathostomulida", "グナトストムラ・パラドクサ", "Gnathostomula paradoxa", "顎口動物の代表種。", jaStatus="provisional", v={"ja": "和名なし（学名の音写）、日本産ではない"})
C("micrognathozoa", "gnathifera", "微顎動物門", "Micrognathozoa", "門", "2000年に記載。グリーンランドの泉で見つかった1種だけからなる。")
S("limnognathia", "micrognathozoa", "リムノグナシア・マエルスキ", "Limnognathia maerski", "最も複雑な顎をもつ微小動物の一つ。", jaStatus="provisional", v={"ja": "和名なし（学名の音写）、日本産ではない"})
# 鉤頭動物は輪形動物の内側から生じた群（Dunn ほか 2014; Sielaff ほか 2016）。輪形動物を単系統にするため、鉤頭動物を輪形動物門（広義）の中に置く
C("rotifera", "gnathifera", "輪形動物門", "Rotifera", "門",
  "ワムシの仲間と、寄生性の鉤頭動物を含む。頭部の繊毛冠を回転するように動かすワムシから、寄生生活に適応した鉤頭動物が生じた。",
  poly="ワムシのどの群（Seisonidea など）が鉤頭動物に最も近いかは議論中のため多分岐で示す。鉤頭動物を別の門として扱う分類体系もあるが、それでは輪形動物門が単系統にならないため、ここでは含める。")
S("shiomizutsubowamushi", "rotifera", "シオミズツボワムシ", "Brachionus plicatilis", "魚の稚魚の餌として大量培養される。", ["ワムシ"])
C("acanthocephala", "rotifera", "鉤頭動物", "Acanthocephala", "クレード", "鉤のある吻で宿主の腸にとりつく寄生虫。口も消化管もない。ワムシの仲間から生じた。")
S("corynosoma", "acanthocephala", "コリノソーマ・ヴィラヌ", "Corynosoma villosum", "海獣類に寄生する鉤頭虫。", ["鉤頭虫"], jaStatus="provisional", v={"ja": "和名なし（学名の音写）", "sci": "代表種の選定を要確認"})
C("platyhelminthes", "spiralia", "扁形動物門", "Platyhelminthes", "門", "平たい体で、肛門がない。プラナリアや寄生性の吸虫・条虫。")
S("namiuzumushi", "platyhelminthes", "ナミウズムシ", "Dugesia japonica", "体を切っても各断片から全身が再生する。", ["プラナリア", "ウズムシ"])
S("nihonkairettojouchu", "platyhelminthes", "日本海裂頭条虫", "Dibothriocephalus nihonkaiensis", "サクラマスなどの生食で感染する。数mに達するサナダムシ。",
  ["ニホンカイレットウジョウチュウ", "サナダムシ", "条虫"], v={"sci": "Diphyllobothrium 属とする扱いもある"})
C("gastrotricha", "spiralia", "腹毛動物門", "Gastrotricha", "門", "イタチムシ。腹面の繊毛で砂のすきまを滑るように動く。")
S("lepidodermella", "gastrotricha", "レピドデルメラ・スクアマタ", "Lepidodermella squamata", "淡水にすむイタチムシの一種。", ["イタチムシ"], jaStatus="provisional", v={"ja": "和名なし（学名の音写）"})
C("dicyemida", "spiralia", "二胚動物門", "Dicyemida", "門", "タコやイカの腎臓にすむ。体は数十個の細胞だけでできている。",
  v={"placement": "らせん卵割動物内での位置は議論中"})
S("dicyema", "dicyemida", "ディキエマ・ヤポニクム", "Dicyema japonicum", "マダコの腎臓にすむニハイチュウの一種。", ["ニハイチュウ"], jaStatus="provisional", v={"ja": "標準和名は未確認（学名の音写）"})
C("orthonectida", "spiralia", "直泳動物門", "Orthonectida", "門", "海産無脊椎動物の寄生虫。単純化した体をもつ。",
  v={"placement": "環形動物の内側に入るとする解析がある"})
S("intoshia", "orthonectida", "イントシア・リネイ", "Intoshia linei", "ヒモムシに寄生する。ゲノムが解読された直泳動物。", ["直泳動物"], jaStatus="provisional", v={"ja": "和名なし（学名の音写）、日本産ではない"})

C("lophotrochozoa", "spiralia", "冠輪動物", "Lophotrochozoa", "クレード",
  "触手冠をもつ動物と、トロコフォア幼生をもつ動物をまとめたクレード。",
  poly="軟体動物・環形動物・紐形動物・腕足動物などの間の関係は議論中のため多分岐で示す。")
C("mollusca", "lophotrochozoa", "軟体動物門", "Mollusca", "門", "外套膜をもち、多くは貝殻を作る。")
S("hizaragai", "mollusca", "ヒザラガイ", "Liolophura japonica", "8枚の殻板をもつ多板類。歯舌の先に磁鉄鉱を含む。", ["Acanthopleura japonica"])
C("conchifera", "mollusca", "Conchifera", "Conchifera", "クレード", "一枚の殻（または二枚の殻）をもつ軟体動物。", poly="綱の間の関係は多分岐で示す。", v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
C("cephalopoda", "conchifera", "頭足綱", "Cephalopoda", "綱", "タコ・イカ・オウムガイ。腕は頭から生えている。")
S("oumugai", "cephalopoda", "オウムガイ", "Nautilus pompilius", "殻の中の気体の量を変えて浮き沈みする。")
S("madako", "cephalopoda", "マダコ", "Octopus sinensis", "日本のマダコは O. vulgaris から分けられた。", ["タコ"])
S("surumeika", "cephalopoda", "スルメイカ", "Todarodes pacificus", "日本近海を回遊する。", ["イカ"])
C("gastropoda", "conchifera", "腹足綱", "Gastropoda", "綱", "巻貝やナメクジ。発生中に体がねじれる。")
S("sazae", "gastropoda", "サザエ", "Turbo sazae", "2017年に新種として学名がつけられた。", ["巻貝"])
S("amefurashi", "gastropoda", "アメフラシ", "Aplysia kurodai", "殻が退化した巻貝。紫色の汁を出す。")
S("misujimaimai", "gastropoda", "ミスジマイマイ", "Euhadra peliomphala", "関東地方に多いカタツムリ。", ["カタツムリ", "マイマイ"])
C("bivalvia", "conchifera", "二枚貝綱", "Bivalvia", "綱", "左右2枚の殻をもち、頭部が退化している。")
S("hamaguri", "bivalvia", "ハマグリ", "Meretrix lusoria", "干潟の減少で数が減った。")
S("magaki", "bivalvia", "マガキ", "Magallana gigas", "世界中で養殖される。Crassostrea gigas とする扱いもある。", ["カキ"])
C("annelida", "lophotrochozoa", "環形動物門", "Annelida", "門", "体節をもつ細長い動物。ユムシやハオリムシも含まれる。")
S("yamatokawagokai", "annelida", "ヤマトカワゴカイ", "Hediste diadroma", "釣り餌の「ゴカイ」の一つ。", ["ゴカイ"])
S("yumushi", "annelida", "ユムシ", "Urechis unicinctus", "体節がないが、分子系統で環形動物の一員とわかった。")
S("satsumahaorimushi", "annelida", "サツマハオリムシ", "Lamellibrachia satsuma", "口も消化管もなく、共生細菌から栄養を得る。", ["ハオリムシ", "チューブワーム"])
C("clitellata", "annelida", "環帯綱", "Clitellata", "綱", "ミミズとヒル。生殖時に環帯ができる。")
S("siebold_mimizu", "clitellata", "シーボルトミミズ", "Metaphire sieboldi", "日本最大級のミミズ。青紫色の光沢がある。", ["ミミズ"])
S("chisuibiru", "clitellata", "チスイビル", "Hirudo nipponia", "かつて瀉血に使われた。ヒルはミミズの中から生じた。", ["ヒル"])
C("nemertea", "lophotrochozoa", "紐形動物門", "Nemertea", "門", "ヒモムシ。体内の吻を素早く突き出して獲物を捕らえる。")
S("midorihimomushi", "nemertea", "ミドリヒモムシ", "Lineus fuscoviridis", "干潟の石の下などにいる。", ["ヒモムシ"], v={"ja": "標準和名と学名の対応を要確認"})
C("brachiozoa", "lophotrochozoa", "Brachiozoa", "Brachiozoa", "クレード", "触手冠をもつ腕足動物と箒虫動物をまとめたクレード。", v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
C("brachiopoda", "brachiozoa", "腕足動物門", "Brachiopoda", "門", "二枚貝に似た殻をもつが、殻は背と腹にある。")
S("midorishamisengai", "brachiopoda", "ミドリシャミセンガイ", "Lingula anatina", "古生代から姿の変わらない「生きた化石」とされる。", ["シャミセンガイ"])
C("phoronida", "brachiozoa", "箒虫動物門", "Phoronida", "門", "管の中にすみ、馬蹄形の触手冠で餌を集める。")
S("himehoukimushi", "phoronida", "ヒメホウキムシ", "Phoronis ijimai", "ホウキムシの代表種。", ["ホウキムシ"], v={"ja": "標準和名と学名の対応を要確認"})
C("bryozoa", "lophotrochozoa", "外肛動物門", "Bryozoa", "門", "コケムシ。小さな個虫が群体を作る。Ectoprocta とも。")
S("oomarikokemushi", "bryozoa", "オオマリコケムシ", "Pectinatella magnifica", "ため池などで直径数十cmのゼリー状の塊になる。外来種。", ["コケムシ"])
C("entoprocta", "lophotrochozoa", "内肛動物門", "Entoprocta", "門", "スズコケムシなど。肛門が触手冠の内側に開く。")
S("barentsia", "entoprocta", "スズコケムシ", "Barentsia discreta", "柄の先に萼をもつ小さな群体性の動物。", v={"ja": "標準和名と学名の対応を要確認", "sci": "要確認"})
C("cycliophora", "lophotrochozoa", "有輪動物門", "Cycliophora", "門", "1995年に記載。アカザエビ類の口器にすむ。")
S("symbion", "cycliophora", "シンビオン・パンドラ", "Symbion pandora", "ヨーロッパアカザエビの口器に付着してくらす。", jaStatus="provisional", v={"ja": "和名なし（学名の音写）、日本産ではない"})


# ---------------- 追加分（v0.3） ----------------
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_more.py"), encoding="utf-8").read())

# ---------------- 検証 ----------------
# 補完に使わないグループ名の別名（2026-10-22 作者の決定）。
# 例外（2026-10-24 作者）：通称でしか知られないことが多いサナダムシ・プラナリアと、魚介類の流通名は通称として aliases に残す（data_more.py 末尾）。
# 「ウニ」でガンガゼが出るように、分類の知識そのものを答えとして渡してしまうため、
# その種だけを指す別名（漢字表記・通称・旧名など）だけを aliases に残し、グループ名は groups に移す。
GROUP_ALIASES = set("""
クシクラゲ サンゴ ミドリイシ イソギンチャク クラゲ クドア 無腸動物 ムチョウドウブツ ウミシダ ウミユリ ヒトデ クモヒトデ
ウニ ナマコ ギボシムシ 頭索動物 ホヤ オタマボヤ ヤツメウナギ サメ エイ チョウザメ ウナギ イワシ マグロ タイ ハイギョ
カエル ガマガエル ヒキガエル サンショウウオ カンガルー ゾウ サル ネズミ コウモリ クマ シカ クジラ ヤモリ ヘビ カメ ウミガメ ワニ
カモ ペンギン カラス ヤムシ トゲカワ コウラムシ 線虫 ハリガネムシ クマムシ カギムシ ウミグモ ウミグモの一種 クモ サソリ
ダニ マダニ ハダニ ムカデ ヤスデ フジツボ ダンゴムシ オキアミ ザリガニ カニ エビ トビムシ トンボ ヤンマ バッタ ゴキブリ シロアリ
セミ ハチ ミツバチ スズメバチ アリ テントウムシ チョウ アゲハチョウ ショウジョウバエ ハエ カ 蚊 ヤブカ ワムシ ヒルガタワムシ 鉤頭虫
ウズムシ 条虫 イタチムシ ニハイチュウ 直泳動物 タコ イカ 巻貝 カタツムリ マイマイ カキ ゴカイ イソメ
ハオリムシ チューブワーム ミミズ ヒル ヒモムシ シャミセンガイ チョウチンガイ ホウキムシ コケムシ ガラス海綿 淡水海綿
ハナギンチャク 宝石サンゴ ウミエラ ジュウモンジクラゲ ベニクラゲ テヅルモヅル タラ フグ クマノミ ハゼ アルマジロ ノウサギ ウサギ
類人猿 モグラ キツネ アザラシ ヤマネコ カモシカ シマウマ ウマ トカゲ イシガメ ハクチョウ ハト ツル カモメ ワシ インコ
ハエトリグモ グソクムシ ヤドカリ カブトエビ シミ 紙魚 カゲロウ コオロギ カマキリ ナナフシ シラミ ホタル クワガタ アリジゴク
ノミ ツノガイ アワビ タニシ イモガイ ウミウシ イガイ シジミ シャコガイ ホシムシ 星口動物 ヒラムシ コウガイビル 住血吸虫
ネコブセンチュウ
""".split())
for _s in species:
    _s["groups"] = [a for a in _s["aliases"] if a in GROUP_ALIASES]
    _s["aliases"] = [a for a in _s["aliases"] if a not in GROUP_ALIASES]
    if not _s["groups"]: del _s["groups"]

# GBIF の種ページへ直接リンクするための番号（名前照合の結果から。学名が一致するものだけ）
# gbif_keys.json は名前照合の結果（check/guessonly/consensus.json）から番号の欄だけを抜き出したもの
_cp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gbif_keys.json")
if os.path.exists(_cp):
    _rows = json.load(open(_cp, encoding="utf-8"))
    for _s in species:
        _r = _rows.get(_s["id"])
        if _r and _r.get("gbifKey") and _s["sci"] in (_r["sci"], _r.get("sciConsensus")):
            _s["gbif"] = _r["gbifKey"]

def validate():
    ids = {}
    for c in clades:
        assert c["id"] not in ids, "dup " + c["id"]
        ids[c["id"]] = c
    roots = [c for c in clades if c["parent"] is None]
    assert len(roots) == 1
    for c in clades:
        if c["parent"]: assert c["parent"] in ids, c
    sids = set()
    for s in species:
        assert s["id"] not in sids and s["id"] not in ids, "dup " + s["id"]
        sids.add(s["id"])
        assert s["parent"] in ids, s
    # every clade must have at least one descendant species
    child = {}
    for c in clades:
        child.setdefault(c["parent"], []).append(c["id"])
    has = set()
    for s in species:
        p = s["parent"]
        while p:
            has.add(p); p = ids[p]["parent"]
    empty = [c["id"] for c in clades if c["id"] not in has]
    assert not empty, empty
    for b in META["selection"]["buckets"]:
        assert b in ids and ids[b]["rank"] == "門", b
    phyla = [c for c in clades if c["rank"] == "門"]
    return len(clades), len(species), len(phyla)

if __name__ == "__main__":
    n = validate()
    out = {"meta": META, "clades": clades, "species": species}
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("clades=%d species=%d phyla=%d" % n)
