# -*- coding: utf-8 -*-
"""収録種の追加分（v0.3、2026-10-22）。build_data.py の末尾から読み込まれる。

既存の種・節目の id は変えない（ゲームの編集データと例題が id を参照するため）。
既存の種を新しい科・目などの節目の下へ移すときは move() を使う。
"""

def _find(id):
    for x in clades + species:
        if x["id"] == id: return x
    raise KeyError(id)

def move(parent, *ids):
    for id in ids: _find(id)["parent"] = parent

def edit(id, **kw):
    _find(id).update(kw)

FISH_V = "Eschmeyer's Catalog of Fishes とは未照合"

# ---------------- 海綿・有櫛 ----------------
S("hossugai", "hexactinellida", "ホッスガイ", "Hyalonema sieboldi",
  "長いガラス質の繊維の束で深海の泥に体を立てる。束が仏具の払子（ほっす）に似る。", ["ガラス海綿"])
S("kawakaimen", "demospongiae", "カワカイメン", "Ephydatia fluviatilis",
  "淡水にすむ海綿。冬や乾燥に耐える芽球という小さな休眠体を作る。", ["淡水海綿"])
S("fusenkurage", "ctenophora", "フウセンクラゲ", "Hormiphora palmata",
  "丸い体から2本の長い触手を伸ばし、粘着細胞で小さな獲物をとらえる。", ["クシクラゲ"])
S("obikurage", "ctenophora", "オビクラゲ", "Cestum veneris",
  "体が帯のように左右に長く伸び、1 m近くになることもある。体をくねらせて泳ぐ。", ["クシクラゲ"])

# ---------------- 刺胞 ----------------
C("actiniaria", "hexacorallia", "イソギンチャク目", "Actiniaria", "目", "骨格をもたない単体のポリプ。")
C("scleractinia", "hexacorallia", "イシサンゴ目", "Scleractinia", "目", "炭酸カルシウムの骨格を作るサンゴ。サンゴ礁を作るものが多い。")
move("actiniaria", "umeboshiisogin")
move("scleractinia", "usuedamidoriishi")
S("sangoisoginchaku", "actiniaria", "サンゴイソギンチャク", "Entacmaea quadricolor",
  "触手の先がふくらむ。クマノミ類がすみかにする。", ["イソギンチャク"])
S("kikumeishi", "scleractinia", "キクメイシ", "Dipsastraea speciosa",
  "菊の花のような個体が並ぶ塊状のサンゴ。かつては Favia 属に置かれた。", ["サンゴ"])
S("murasakihanaginchaku", "hexacorallia", "ムラサキハナギンチャク", "Cerianthus filiformis",
  "砂の中に粘液と刺胞で作った管を埋め、長い触手を広げる。イソギンチャクとは別の目（ハナギンチャク目）。",
  ["ハナギンチャク"], v={"placement": "ハナギンチャク類を六放サンゴ亜綱の外に置く解析もある"})
C("octocorallia", "anthozoa", "八放サンゴ亜綱", "Octocorallia", "亜綱", "触手が8本で、羽のように枝分かれする。宝石サンゴ・ソフトコーラル・ウミエラなど。")
S("akasango", "octocorallia", "アカサンゴ", "Corallium japonicum",
  "宝石サンゴの代表。深い海で年に数ミリしか太らない。", ["宝石サンゴ", "サンゴ"])
S("umisaboten", "octocorallia", "ウミサボテン", "Cavernularia obesa",
  "砂地に柄をさして立つウミエラの仲間。夜にふくらみ、刺激すると青白く光る。", ["ウミエラ"])
C("scyphozoa", "medusozoa", "鉢虫綱", "Scyphozoa", "綱", "いわゆる大型のクラゲ。ポリプが横に分裂してクラゲを生む。")
C("cubozoa", "medusozoa", "箱虫綱", "Cubozoa", "綱", "箱形の傘をもつクラゲ。眼をもち、毒が強いものが多い。")
C("staurozoa", "medusozoa", "十文字クラゲ綱", "Staurozoa", "綱", "海藻などに柄で付着して暮らすクラゲ。")
C("hydrozoa", "medusozoa", "ヒドロ虫綱", "Hydrozoa", "綱", "小さなクラゲや群体性のポリプ。淡水のヒドラも含む。")
edit("medusozoa", polytomy="鉢虫綱・箱虫綱・十文字クラゲ綱・ヒドロ虫綱の関係は多分岐で示す（鉢・箱・十文字クラゲをまとめる Acraspeda を支持する解析が多い）。")
move("scyphozoa", "mizukurage", "echizenkurage")
move("cubozoa", "andonkurage")
move("hydrozoa", "katsuonoeboshi")
S("akakurage", "scyphozoa", "アカクラゲ", "Chrysaora pacifica",
  "傘に赤褐色の放射状の縞がある。乾いた触手の粉でくしゃみが出るので「ハクションクラゲ」とも。", ["クラゲ"])
S("habukurage", "cubozoa", "ハブクラゲ", "Chironex yamaguchii",
  "沖縄などにすむ猛毒の箱虫類。2009年に新種として記載された。", ["クラゲ"])
S("asagaokurage", "staurozoa", "シラスジアサガオクラゲ", "Haliclystus borealis",
  "漏斗形の体を柄で海藻に付け、縁の8つの腕の先に小さな触手の房をもつ。",
  ["ジュウモンジクラゲ"], v={"ja": "和名は GBIF のみ。標準和名と学名の対応を要確認"})
S("katsuononkanmuri", "hydrozoa", "カツオノカンムリ", "Velella velella",
  "帆のある浮き袋で風を受けて海面を漂う。カツオノエボシと同じヒドロ虫類。")
S("benikurage", "hydrozoa", "チチュウカイベニクラゲ", "Turritopsis dohrnii",
  "成熟したクラゲが若いポリプに戻ることがあり「不老不死のクラゲ」と呼ばれる。日本近海のベニクラゲ類は別種とされる。",
  ["ベニクラゲ"])

# ---------------- 棘皮 ----------------
C("crinoidea", "echinodermata", "ウミユリ綱", "Crinoidea", "綱", "口を上に向け、羽のような腕で餌をとる。柄のあるウミユリと柄のないウミシダ。")
move("crinoidea", "nipponumishida")
S("torinoashi", "crinoidea", "トリノアシ", "Metacrinus rotundus",
  "柄で海底に立つウミユリ。日本近海では比較的浅い海でも見られる。", ["ウミユリ"])
C("asteroidea", "asterozoa", "ヒトデ綱", "Asteroidea", "綱", "腕と中央の盤の境目がはっきりしない。胃を外に出して獲物を消化する。")
C("ophiuroidea", "asterozoa", "クモヒトデ綱", "Ophiuroidea", "綱", "円い盤から細い腕が伸びる。棘皮動物で最も種数が多い。")
move("asteroidea", "itomakihitode")
move("ophiuroidea", "nihonkumohitode")
S("mahitode", "asteroidea", "キヒトデ", "Asterias amurensis",
  "貝類を食べる。オーストラリアなどに侵入して問題になっている。", ["マヒトデ", "ヒトデ"])
S("onihitode", "asteroidea", "オニヒトデ", "Acanthaster planci",
  "毒のある棘をもち、サンゴを食べる。大発生するとサンゴ礁に大きな被害が出る。", ["ヒトデ"],
  v={"sci": "太平洋の個体群を A. solaris として分ける提案がある"})
S("okinotezurumozuru", "ophiuroidea", "オキノテヅルモヅル", "Gorgonocephalus eucnemis",
  "腕が何度も枝分かれして網のように広がるクモヒトデの仲間。", ["テヅルモヅル", "クモヒトデ"])
C("echinoidea", "echinozoa", "ウニ綱", "Echinoidea", "綱", "骨片が組み合わさった殻と、動かせる棘をもつ。")
C("holothuroidea", "echinozoa", "ナマコ綱", "Holothuroidea", "綱", "骨片が小さく皮膚に散らばり、体が柔らかい。")
move("echinoidea", "murasakiuni")
move("holothuroidea", "manamako")
S("bafununi", "echinoidea", "バフンウニ", "Hemicentrotus pulcherrimus",
  "短い棘が密に生えた小型のウニ。発生学の実験材料としてよく使われる。", ["ウニ"])
S("takonomakura", "echinoidea", "タコノマクラ", "Clypeaster japonicus",
  "平たい殻に花びら形の模様がある。砂にすむウニの仲間。", ["ウニ"])
S("gangaze", "echinoidea", "ガンガゼ", "Diadema setosum",
  "長く折れやすい毒棘をもつ。", ["ウニ"])
S("kuronamako", "holothuroidea", "クロナマコ", "Holothuria atra",
  "サンゴ礁の砂地にすむ黒いナマコ。砂ごと有機物を食べて海底をきれいにする。", ["ナマコ"])

# ---------------- 半索・脊索（無脊椎） ----------------
S("himegiboshimushi", "hemichordata", "ヒメギボシムシ", "Ptychodera flava",
  "サンゴ礁の砂地にすむギボシムシ。再生能力が高く研究に使われる。", ["ギボシムシ"],
  v={"ja": "標準和名と学名の対応を要確認"})
S("katayureiboya", "tunicata", "カタユウレイボヤ", "Ciona robusta",
  "発生学のモデル生物。かつて Ciona intestinalis とされていたが、2015年に別種として分けられた。", ["ホヤ"])

# ---------------- 魚類（軟骨魚） ----------------
C("selachii", "elasmobranchii", "サメ類", "Selachii", "クレード", "サメの仲間。分子系統でエイ類と姉妹群になる。",
  v={"ja": "階級なしのクレードとして使用"})
C("batoidea", "elasmobranchii", "エイ類", "Batoidea", "クレード", "エイの仲間。体が平たく、鰓孔が腹側に開く。",
  v={"ja": "階級なしのクレードとして使用"})
move("selachii", "jinbeizame")
move("batoidea", "akaei")
S("hohojirozame", "selachii", "ホホジロザメ", "Carcharodon carcharias",
  "大型の肉食ザメ。体温を水温より高く保てる。", ["サメ"], v={"sci": FISH_V})
S("nanyoumanta", "batoidea", "ナンヨウマンタ", "Mobula alfredi",
  "大きな胸鰭で羽ばたくように泳ぐ。2018年にマンタ属はイトマキエイ属（Mobula）にまとめられた。",
  ["マンタ", "エイ"], v={"sci": FISH_V})

# ---------------- 魚類（条鰭類） ----------------
C("otomorpha", "clupeocephala", "Otomorpha", "Otomorpha", "クレード", "ニシン類と、コイ・ナマズなどの骨鰾類をまとめたクレード。",
  v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
C("clupeiformes", "otomorpha", "ニシン目", "Clupeiformes", "目", "イワシやニシン。群れで泳ぎ、プランクトンを食べる。")
C("ostariophysi", "otomorpha", "骨鰾類", "Ostariophysi", "上目", "うきぶくろと内耳を小骨（ウェーバー器官）でつなぎ、音をよく聞く。淡水魚の多くを占める。")
move("clupeiformes", "maiwashi")
move("ostariophysi", "koi")
S("katakuchiiwashi", "clupeiformes", "カタクチイワシ", "Engraulis japonicus",
  "下あごが短く、口が片側だけにあるように見えることが名の由来。しらすや煮干しになる。", ["イワシ", "シラス"], v={"sci": FISH_V})
S("namazu", "ostariophysi", "ナマズ", "Silurus asotus",
  "口ひげで餌を探す。コイと同じ骨鰾類。", ["マナマズ"], v={"sci": FISH_V})
C("euteleostei", "clupeocephala", "正真骨類", "Euteleostei", "クレード", "サケ・タラ・スズキの仲間など、真骨類の大部分を含むクレード。",
  poly="サケ目・キュウリウオ目・タラ目とスズキ系の関係は、ここでは多分岐で示す。")
move("euteleostei", "percomorpha")
S("sake", "euteleostei", "サケ", "Oncorhynchus keta",
  "川で生まれて海で育ち、生まれた川に戻って産卵する。", ["シロザケ", "鮭"], v={"sci": FISH_V})
S("ayu", "euteleostei", "アユ", "Plecoglossus altivelis",
  "川の石についた藻を櫛のような歯で削り取って食べる。寿命はふつう1年。", ["鮎"], v={"sci": FISH_V})
S("madara", "euteleostei", "マダラ", "Gadus macrocephalus",
  "北の海にすむ大型のタラ。白子や鱈子も食用にされる。", ["タラ", "鱈"], v={"sci": FISH_V})
edit("percomorpha", polytomy="スズキ系の中は、ここでは目・科の節目だけを置いて多分岐で示す。")
C("beloniformes", "percomorpha", "ダツ目", "Beloniformes", "目", "サンマ・トビウオ・ダツと、メダカ科をまとめた目。")
C("scombridae", "percomorpha", "サバ科", "Scombridae", "科", "マグロ・カツオ・サバなど、速く泳ぐ外洋性の魚。")
C("tetraodontiformes", "percomorpha", "フグ目", "Tetraodontiformes", "目", "フグ・カワハギ・マンボウなど。腹鰭や骨の一部を失ったものが多い。")
move("beloniformes", "minamimedaka")
move("scombridae", "kuromaguro")
S("sanma", "beloniformes", "サンマ", "Cololabis saira",
  "メダカと同じダツ目。胃をもたない。", ["秋刀魚"], v={"sci": FISH_V})
S("katsuo", "scombridae", "カツオ", "Katsuwonus pelamis",
  "黒潮に乗って北上し、秋に南へ戻る。かつお節の原料。", ["鰹"], v={"sci": FISH_V})
S("torafugu", "tetraodontiformes", "トラフグ", "Takifugu rubripes",
  "肝臓や卵巣にテトロドトキシンをもつ。脊椎動物で最も小さい部類のゲノムをもつ。", ["フグ"], v={"sci": FISH_V})
S("manbou", "tetraodontiformes", "マンボウ", "Mola mola",
  "フグの仲間で、尾鰭がなく舵鰭で泳ぐ。日本近海には別種のウシマンボウもいる。", v={"sci": FISH_V + "。マンボウ属の種の区別は近年見直された"})
S("hirame", "percomorpha", "ヒラメ", "Paralichthys olivaceus",
  "稚魚のうちは左右対称で、成長すると右目が体の左側へ移る。", v={"sci": FISH_V})
S("kakurekumanomi", "percomorpha", "カクレクマノミ", "Amphiprion ocellaris",
  "イソギンチャクの刺胞に刺されずにすむ。群れの最大個体が雄から雌に性転換する。", ["クマノミ"], v={"sci": FISH_V})
S("mahaze", "percomorpha", "マハゼ", "Acanthogobius flavimanus",
  "内湾や河口にすむ。左右の腹鰭がくっついて吸盤のようになっている。", ["ハゼ"], v={"sci": FISH_V})

# ---------------- 両生類 ----------------
C("anura", "amphibia", "無尾目", "Anura", "目", "カエル。成体は尾がなく、後ろ脚が長い。")
C("caudata", "amphibia", "有尾目", "Caudata", "目", "サンショウウオとイモリ。成体にも尾がある。")
move("anura", "nihonamagaeru")
move("caudata", "osanshouo", "akaharaimori")
S("nihonhikigaeru", "anura", "ニホンヒキガエル", "Bufo japonicus",
  "耳腺から毒を出す。春先に池に集まって紐状の卵を産む。", ["ヒキガエル", "ガマガエル", "カエル"])
S("tonosamagaeru", "anura", "トノサマガエル", "Pelophylax nigromaculatus",
  "水田でよく見られた。関東平野の多くでは近縁のトウキョウダルマガエルに置き換わる。", ["カエル"])

# ---------------- 哺乳類 ----------------
edit("placentalia", polytomy="アフリカ獣類・異節類・北方真獣類の分岐順は議論中のため、ここでは多分岐で示す。")
C("xenarthra", "placentalia", "異節類", "Xenarthra", "クレード", "アルマジロ・ナマケモノ・アリクイ。南米で多様化した。")
C("afrotheria", "placentalia", "アフリカ獣類", "Afrotheria", "クレード", "ゾウ・ジュゴン・ハイラックスなど。分子系統で見つかったクレード。")
move("afrotheria", "africazou")
S("kokonoobiarumajiro", "xenarthra", "ココノオビアルマジロ", "Dasypus novemcinctus",
  "1回の出産で、1つの受精卵から分かれた遺伝的に同じ四つ子を産む。", ["アルマジロ"], jaStatus="common")
S("jugon", "afrotheria", "ジュゴン", "Dugong dugon",
  "海草を食べる海の哺乳類。ゾウに近い。", ["人魚"])
C("glires", "euarchontoglires", "Glires", "Glires", "クレード", "齧歯類とウサギ類をまとめたクレード。伸び続ける門歯をもつ。",
  v={"ja": "定着した和名が確認できないため学名で表記"})
C("rodentia", "glires", "齧歯目", "Rodentia", "目", "ネズミやリス。哺乳類で最も種数が多い目。")
C("muridae", "rodentia", "ネズミ科", "Muridae", "科", "ハツカネズミやドブネズミなど。")
C("lagomorpha", "glires", "兎形目", "Lagomorpha", "目", "ウサギとナキウサギ。上の門歯が前後2対ある。")
move("muridae", "hatsukanezumi")
S("dobunezumi", "muridae", "ドブネズミ", "Rattus norvegicus",
  "実験用ラットの元になった種。", ["ラット", "ネズミ"])
S("nihonnousagi", "lagomorpha", "ニホンノウサギ", "Lepus brachyurus",
  "日本固有のノウサギ。雪の多い地方の個体は冬に白い毛に生え変わる。", ["ノウサギ", "ウサギ"])
C("hominidae", "primates", "ヒト科", "Hominidae", "科", "大型類人猿とヒト。オランウータン・ゴリラ・チンパンジー・ヒト。")
move("hominidae", "hito")
S("chimpanzee", "hominidae", "チンパンジー", "Pan troglodytes",
  "ヒトに最も近い現生動物の一つ（もう一つはボノボ）。道具を使う。", ["類人猿"])
C("eulipotyphla", "laurasiatheria", "真無盲腸目", "Eulipotyphla", "目", "モグラ・トガリネズミ・ハリネズミ。")
C("chiroptera", "laurasiatheria", "翼手目", "Chiroptera", "目", "コウモリ。飛ぶことのできる唯一の哺乳類。")
move("chiroptera", "kikugashira")
S("azumamogura", "eulipotyphla", "アズマモグラ", "Mogera imaizumii",
  "東日本に多いモグラ。シャベルのような前足で土を掘る。", ["モグラ"])
S("aburakoumori", "chiroptera", "アブラコウモリ", "Pipistrellus abramus",
  "家屋にすむ小型のコウモリ。夕方に町の上を飛んで虫を食べる。", ["イエコウモリ", "コウモリ"])
C("caniformia", "carnivora", "イヌ型亜目", "Caniformia", "亜目", "イヌ・クマ・イタチ・アザラシなど。")
C("canidae", "caniformia", "イヌ科", "Canidae", "科", "イヌ・オオカミ・キツネ・タヌキ。")
C("feliformia", "carnivora", "ネコ型亜目", "Feliformia", "亜目", "ネコ・ハイエナ・マングースなど。")
move("canidae", "tanuki")
move("caniformia", "tsukinowaguma")
S("akagitsune", "canidae", "アカギツネ", "Vulpes vulpes",
  "北半球に広く分布する。日本のホンドギツネ・キタキツネはその亜種。", ["キツネ", "ホンドギツネ", "キタキツネ"])
S("gomafuazarashi", "caniformia", "ゴマフアザラシ", "Phoca largha",
  "アザラシは食肉目のイヌ型亜目で、クマやイタチに近い。冬に流氷の上で子を産む。", ["アザラシ"])
S("bengaruyamaneko", "feliformia", "ベンガルヤマネコ", "Prionailurus bengalensis",
  "ツシマヤマネコはその亜種。イリオモテヤマネコも亜種とする見解が多い。", ["ヤマネコ", "ツシマヤマネコ", "イリオモテヤマネコ"],
  v={"sci": "イリオモテヤマネコの位置づけ（亜種か別種か）は議論がある"})
C("ruminantia", "cetruminantia", "反芻亜目", "Ruminantia", "亜目", "シカ・ウシ・キリンなど。複数の部屋に分かれた胃で反芻する。")
C("whippomorpha", "cetruminantia", "Whippomorpha", "Whippomorpha", "クレード", "カバとクジラ類をまとめたクレード。分子系統で見つかった。",
  v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
C("cetacea", "whippomorpha", "クジラ類", "Cetacea", "クレード", "海で暮らすようになった鯨偶蹄類。ヒゲクジラとハクジラ。",
  v={"ja": "鯨目・クジラ下目など階級の扱いが分かれるため、階級なしで表示"})
move("ruminantia", "nihonjika")
move("cetacea", "shironagasu")
S("nihonkamoshika", "ruminantia", "ニホンカモシカ", "Capricornis crispus",
  "名前にシカとつくがウシ科。日本固有種で特別天然記念物。", ["カモシカ"])
S("kaba", "whippomorpha", "カバ", "Hippopotamus amphibius",
  "クジラに最も近い現生の陸上動物。皮膚から赤い色素を含む液を出す。")
S("makkoukujira", "cetacea", "マッコウクジラ", "Physeter macrocephalus",
  "最大のハクジラ。深海に潜ってダイオウイカなどを食べる。", ["クジラ"])
C("perissodactyla", "laurasiatheria", "奇蹄目", "Perissodactyla", "目", "ウマ・サイ・バク。体重を主に中指で支える。")
S("savannashimauma", "perissodactyla", "サバンナシマウマ", "Equus quagga",
  "縞模様は個体ごとに違う。吸血するハエを寄せつけにくくする効果があるとされる。", ["シマウマ", "ウマ"], jaStatus="common")

# ---------------- 爬虫類 ----------------
C("serpentes", "squamata", "ヘビ亜目", "Serpentes", "亜目", "ヘビ。トカゲの仲間の中から、脚を失って生まれた。")
C("viperidae", "serpentes", "クサリヘビ科", "Viperidae", "科", "長い毒牙を折りたたんでもつヘビ。マムシ類は目と鼻の間に赤外線を感じるピット器官をもつ。")
move("serpentes", "aodaisho")
S("habu", "viperidae", "ハブ", "Protobothrops flavoviridis",
  "南西諸島にすむ毒ヘビ。夜に活動する。", ["ヘビ"])
S("nihonmamushi", "viperidae", "ニホンマムシ", "Gloydius blomhoffii",
  "卵ではなく子ヘビを産む。", ["マムシ", "ヘビ"])
S("nihontokage", "squamata", "ニホントカゲ", "Plestiodon japonicus",
  "幼体の尾は鮮やかな青色。襲われると尾を自分で切って逃げる。", ["トカゲ"])
C("testudines", "archelosauria", "カメ目", "Testudines", "目", "背甲と腹甲からなる甲羅をもつ。")
move("testudines", "akaumigame")
S("nihonishigame", "testudines", "ニホンイシガメ", "Mauremys japonica",
  "日本固有のカメ。川や池にすむ。", ["イシガメ", "カメ"])

# ---------------- 鳥類 ----------------
C("galliformes", "galloanserae", "キジ目", "Galliformes", "目", "キジ・ウズラ・ニワトリなど。地上で暮らすものが多い。")
C("anseriformes", "galloanserae", "カモ目", "Anseriformes", "目", "カモ・ガン・ハクチョウ。くちばしの縁に濾し取るための板がある。")
move("galliformes", "sekishokuyakei")
move("anseriformes", "magamo")
S("uzura", "galliformes", "ウズラ", "Coturnix japonica",
  "日本で家禽化された鳥。うずら卵の殻の模様は個体ごとに違う。")
S("oohakuchou", "anseriformes", "オオハクチョウ", "Cygnus cygnus",
  "シベリアから冬に日本へ渡ってくる。", ["ハクチョウ"])
S("kijibato", "neoaves", "キジバト", "Streptopelia orientalis",
  "ハトは素嚢から「ピジョンミルク」を出してひなに与える。", ["ヤマバト", "ハト"])
S("tancho", "neoaves", "タンチョウ", "Grus japonensis",
  "頭頂の赤い部分は羽毛ではなく皮膚。北海道東部で繁殖する。", ["ツル", "タンチョウヅル"])
S("umineko", "neoaves", "ウミネコ", "Larus crassirostris",
  "鳴き声が猫に似ているカモメの仲間。", ["カモメ"])
C("telluraves", "neoaves", "Telluraves", "Telluraves", "クレード", "タカ・フクロウ・キツツキ・ハヤブサ・オウム・スズメなどをまとめたクレード。",
  v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
C("afroaves", "telluraves", "Afroaves", "Afroaves", "クレード", "タカ類・フクロウ類・キツツキ類などをまとめたクレード。",
  v={"ja": "定着した和名が確認できないため学名で表記"})
C("australaves", "telluraves", "Australaves", "Australaves", "クレード",
  "ハヤブサ類・オウム類・スズメ類をまとめたクレード。ハヤブサはタカよりもオウムやスズメに近い。",
  v={"ja": "定着した和名が確認できないため学名で表記"})
move("australaves", "passeriformes")
S("inuwashi", "afroaves", "イヌワシ", "Aquila chrysaetos",
  "翼を広げると2 mほどになる大型のタカ科の鳥。", ["ワシ"])
S("fukurou", "afroaves", "フクロウ", "Strix uralensis",
  "左右の耳の位置が上下にずれていて、音のする方向を正確に知る。")
S("hayabusa", "australaves", "ハヤブサ", "Falco peregrinus",
  "急降下では時速300 km近くに達する。タカに似るが、オウムやスズメに近い。")
S("sekiseiinko", "australaves", "セキセイインコ", "Melopsittacus undulatus",
  "オーストラリア原産。人の言葉をまねることができる。", ["インコ"])
C("corvus", "passeriformes", "カラス属", "Corvus", "属", "ハシブトガラス・ハシボソガラスなど。")
move("corvus", "hashibutogarasu")
S("hashibosogarasu", "corvus", "ハシボソガラス", "Corvus corone",
  "ハシブトガラスよりくちばしが細い。クルミを車にひかせて割ることがある。", ["カラス"])
S("uguisu", "passeriformes", "ウグイス", "Horornis diphone",
  "「ホーホケキョ」とさえずるのは雄。姿は地味で茂みの中にいる。")
S("shijuukara", "passeriformes", "シジュウカラ", "Parus minor",
  "鳴き声を組み合わせて「文」のように使うことが研究で示された。")

# ---------------- 鋏角・多足 ----------------
C("araneae", "euchelicerata", "クモ目", "Araneae", "目", "腹部の出糸突起から糸を出す。")
move("araneae", "jorougumo")
S("ashidakagumo", "araneae", "アシダカグモ", "Heteropoda venatoria",
  "網を張らずに歩き回って獲物を捕らえる大型のクモ。家の中でゴキブリを食べる。", ["クモ"])
S("adansonhaetori", "araneae", "アダンソンハエトリ", "Hasarius adansoni",
  "大きな前の目で距離を測り、跳びかかって虫を捕らえる。", ["ハエトリグモ", "クモ"])
S("namihadani", "euchelicerata", "ナミハダニ", "Tetranychus urticae",
  "植物の汁を吸う小さなダニ。農作物の害虫。", ["ハダニ", "ダニ"])
C("chilopoda", "myriapoda", "唇脚綱", "Chilopoda", "綱", "ムカデ類。体節ごとに1対の脚と、毒をもつ顎肢をもつ。")
C("diplopoda", "myriapoda", "倍脚綱", "Diplopoda", "綱", "ヤスデ類。体節ごとに2対の脚をもち、落ち葉などを食べる。")
move("chilopoda", "tobizumukade")
move("diplopoda", "yakeyasude")
S("geji", "chilopoda", "ゲジ", "Thereuonema tuberculata",
  "長い15対の脚で素早く走るムカデの仲間。", ["ゲジゲジ"])
S("kishayasude", "diplopoda", "キシャヤスデ", "Parafontaria laminata",
  "8年周期で大発生し、線路に集まって列車を止めたことから名づけられた。", ["オビババヤスデ", "ヤスデ"],
  v={"ja": "MilliBase は亜種を分けず、キシャヤスデ（armigera）は P. laminata の異名とする。種の和名をオビババヤスデとする資料（GBIF・Wikidata・iNaturalist）もあるが、学術的な典拠は未確認"})

# ---------------- 甲殻類 ----------------
C("isopoda", "malacostraca", "等脚目", "Isopoda", "目", "ダンゴムシ・ワラジムシ・フナムシ・グソクムシなど。")
move("isopoda", "okadangomushi")
S("daiougusokumushi", "isopoda", "ダイオウグソクムシ", "Bathynomus giganteus",
  "深海にすむ最大級の等脚類。長期間食べずに生きられる。", ["グソクムシ"])
S("shako", "malacostraca", "シャコ", "Oratosquilla oratoria",
  "口脚目。鎌のような脚で獲物を一撃する。", v={"sci": "日本産を別属（Oratosquilla 以外）に置く見解がある"})
C("anomura", "decapoda", "異尾下目", "Anomura", "下目", "ヤドカリ・タラバガニ・コシオリエビなど。")
C("brachyura", "decapoda", "短尾下目", "Brachyura", "下目", "いわゆるカニ。腹部が小さく胸の下に折りたたまれる。")
move("brachyura", "zuwaigani")
S("tarabagani", "anomura", "タラバガニ", "Paralithodes camtschaticus",
  "カニと呼ばれるが、ヤドカリに近い。歩く脚が3対に見える。", ["カニ"])
S("honyadokari", "anomura", "ホンヤドカリ", "Pagurus filholi",
  "磯で巻貝の殻を借りて暮らす。成長すると大きな殻に引っ越す。", ["ヤドカリ"])
S("sawagani", "brachyura", "サワガニ", "Geothelphusa dehaani",
  "一生を淡水で過ごし、卵から小さなカニの姿で生まれる。", ["カニ"])
S("iseebi", "decapoda", "イセエビ", "Panulirus japonicus",
  "長いフィロソーマ幼生期を海で過ごしてから沿岸に戻る。", ["エビ"])
S("ajiakabutoebi", "branchiopoda", "アジアカブトエビ", "Triops granarius",
  "田んぼに現れる。卵は乾燥に耐え、何年も休眠できる。", ["カブトエビ"])

# ---------------- 昆虫 ----------------
S("seiyoushimi", "insecta", "セイヨウシミ", "Lepisma saccharinum",
  "翅をもたない原始的な昆虫。紙や糊を食べ、成虫になっても脱皮を続ける。", ["シミ", "紙魚"])
C("odonata", "pterygota", "トンボ目", "Odonata", "目", "トンボとイトトンボ。幼虫（ヤゴ）は水中で暮らす。")
move("odonata", "akiakane")
S("oniyanma", "odonata", "オニヤンマ", "Anotogaster sieboldii",
  "日本最大のトンボ。", ["ヤンマ", "トンボ"])
S("monkagerou", "pterygota", "モンカゲロウ", "Ephemera strigata",
  "カゲロウは亜成虫という翅のある段階を経て、もう一度脱皮して成虫になる。", ["カゲロウ"])
C("orthoptera", "polyneoptera", "バッタ目", "Orthoptera", "目", "バッタ・コオロギ・キリギリス。後ろ脚が跳ぶのに適している。")
C("dictyoptera", "polyneoptera", "網翅類", "Dictyoptera", "クレード", "ゴキブリ・シロアリ・カマキリ。卵を卵鞘にまとめて産む。")
move("orthoptera", "tonosamabatta")
move("dictyoptera", "blattodea")
S("enmakorogi", "orthoptera", "エンマコオロギ", "Teleogryllus emma",
  "雄が前翅をこすり合わせて鳴く。耳は前脚にある。", ["コオロギ"])
S("ookamakiri", "dictyoptera", "オオカマキリ", "Tenodera sinensis",
  "カマキリはゴキブリに近い。泡で包んだ卵鞘を枝に産む。", ["カマキリ"],
  v={"sci": "T. aridifolia の亜種とする扱いもある"})
S("nanafushimodoki", "polyneoptera", "ナナフシモドキ", "Ramulus mikado",
  "枝に擬態する。日本では雄がほとんど見つからず、雌だけで単為生殖する。", ["ナナフシ"])
C("paraneoptera", "neoptera", "準新翅類", "Paraneoptera", "クレード", "カメムシ・セミ・アザミウマ・シラミなど。")
C("hemiptera", "paraneoptera", "カメムシ目", "Hemiptera", "目", "針のような口吻で汁を吸う。半翅目とも。")
move("paraneoptera", "aburazemi")
move("hemiptera", "aburazemi")
S("amenbo", "hemiptera", "アメンボ", "Aquarius paludum",
  "脚の細かい毛が水をはじき、水面に浮いて歩く。カメムシの仲間で、あめのような匂いを出す。")
S("hitojirami", "paraneoptera", "ヒトジラミ", "Pediculus humanus",
  "アタマジラミとコロモジラミを含む。コロモジラミは衣服を着る習慣とともに生まれたと考えられている。", ["シラミ", "アタマジラミ"])
S("oosuzumebachi", "hymenoptera", "オオスズメバチ", "Vespa mandarinia",
  "世界最大のスズメバチ。ニホンミツバチは集団で取り囲んで熱で殺す。", ["スズメバチ", "ハチ"])
S("genjibotaru", "coleoptera", "ゲンジボタル", "Nipponoluciola cruciata",
  "幼虫は川でカワニナを食べる。2022年に Luciola 属から新属 Nipponoluciola に移された。", ["ホタル", "Luciola cruciata"],
  v={"sci": "COL は Nipponoluciola、GBIF は旧属名 Luciola"})
S("nokogirikuwagata", "coleoptera", "ノコギリクワガタ", "Prosopocoilus inclinatus",
  "大あごの形が体の大きさで変わる。", ["クワガタ"])
C("coccinellidae", "coleoptera", "テントウムシ科", "Coccinellidae", "科", "丸い体の甲虫。アブラムシなどを食べるものが多い。")
move("coccinellidae", "nanahoshitentou")
S("namitentou", "coccinellidae", "ナミテントウ", "Harmonia axyridis",
  "斑紋が個体によって大きく違い、遺伝子の組み合わせで決まる。", ["テントウムシ"])
S("usubakagerou", "holometabola", "ウスバカゲロウ", "Hagenomyia micans",
  "幼虫はアリジゴクで、砂にすり鉢状の巣を作る。カゲロウとは別の目（アミメカゲロウ目）。", ["アリジゴク"])
C("lepidoptera", "mecopterida", "チョウ目", "Lepidoptera", "目", "チョウとガ。翅が鱗粉におおわれる。")
C("diptera", "mecopterida", "ハエ目", "Diptera", "目", "ハエ・カ・アブ。後翅が平均棍に変わり、翅は2枚。")
move("lepidoptera", "monshirocho", "kaiko")
move("diptera", "drosophila", "hitosujishimaka")
S("ageha", "lepidoptera", "ナミアゲハ", "Papilio xuthus",
  "幼虫はミカン類の葉を食べ、刺激すると臭い角（臭角）を出す。", ["アゲハ", "アゲハチョウ", "チョウ"])
S("oomurasaki", "lepidoptera", "オオムラサキ", "Sasakia charonda",
  "日本の国蝶。幼虫はエノキの葉を食べる。", ["チョウ"])
S("iebae", "diptera", "イエバエ", "Musca domestica",
  "人の暮らしのそばで世界中に分布する。", ["ハエ"])
S("nekonomi", "mecopterida", "ネコノミ", "Ctenocephalides felis",
  "ノミは翅を失ったシリアゲムシの仲間。体長の100倍近くも跳ぶ。", ["ノミ"])

# ---------------- 軟体 ----------------
C("aculifera", "mollusca", "Aculifera", "Aculifera", "クレード", "多板類と無板類（溝腹類・尾腔類）をまとめたクレード。",
  v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
move("aculifera", "hizaragai")
S("kasemimizu", "aculifera", "カセミミズ", "Epimenia babai",
  "殻のない細長い軟体動物（無板類）。ヒドロ虫などを食べる。", v={"ja": "標準和名と学名の対応を要確認"})
S("yakadotsunogai", "conchifera", "ヤカドツノガイ", "Dentalium octangulatum",
  "角のような筒形の殻をもつ掘足類。砂に潜って細い触手で餌を集める。", ["ツノガイ"])
C("coleoidea", "cephalopoda", "鞘形亜綱", "Coleoidea", "亜綱", "殻が体内に退化するか失われたタコ・イカの仲間。")
C("octopodiformes", "coleoidea", "八腕形上目", "Octopodiformes", "上目", "タコとコウモリダコ。")
C("decapodiformes", "coleoidea", "十腕形上目", "Decapodiformes", "上目", "イカ類。8本の腕と2本の触腕をもつ。")
move("octopodiformes", "madako")
move("decapodiformes", "surumeika")
S("mizudako", "octopodiformes", "ミズダコ", "Enteroctopus dofleini",
  "世界最大級のタコ。腕を広げると3 mを超えることがある。", ["タコ"])
S("takobune", "octopodiformes", "タコブネ", "Argonauta hians",
  "雌が腕から分泌した薄い殻をもつタコ。殻の中で卵を守る。", ["タコ"])
S("daiouika", "decapodiformes", "ダイオウイカ", "Architeuthis dux",
  "全長10 mを超える深海のイカ。2012年に小笠原沖で初めて生きた姿が撮影された。", ["イカ"])
S("kouika", "decapodiformes", "コウイカ", "Acanthosepion esculentum",
  "体内に石灰質の甲（イカの甲）をもつ。近年 Sepia 属から Acanthosepion 属に移された。", ["イカ", "スミイカ", "Sepia esculenta"],
  v={"sci": "GBIF・WoRMS は Acanthosepion。COL は Sepia esculenta のまま"})
S("hotaruika", "decapodiformes", "ホタルイカ", "Watasenia scintillans",
  "腕の先などの発光器で青く光る。富山湾の群れは特別天然記念物。", ["イカ"])
C("vetigastropoda", "gastropoda", "古腹足類", "Vetigastropoda", "クレード", "サザエ・アワビ・ニシキウズなど。")
C("caenogastropoda", "gastropoda", "新生腹足類", "Caenogastropoda", "クレード", "タニシ・タカラガイ・イモガイなど巻貝の多く。")
C("heterobranchia", "gastropoda", "異鰓類", "Heterobranchia", "クレード", "ウミウシ・アメフラシ・カタツムリ・ナメクジなど。")
move("vetigastropoda", "sazae")
move("heterobranchia", "amefurashi", "misujimaimai")
S("kuroawabi", "vetigastropoda", "クロアワビ", "Haliotis discus",
  "殻に並ぶ穴から水を出す。巻貝の仲間。", ["アワビ"], v={"sci": "H. discus discus（亜種）とする扱いが多い"})
S("ootanishi", "caenogastropoda", "オオタニシ", "Cipangopaludina japonica",
  "田んぼや池にすむ巻貝。卵ではなく子貝を産む。", ["タニシ"])
S("anboina", "caenogastropoda", "アンボイナ", "Conus geographus",
  "イモガイの一種。毒のある銛のような歯舌で魚を刺す。人が死亡した例もある。", ["アンボイナガイ", "イモガイ"])
S("aoumiushi", "heterobranchia", "アオウミウシ", "Hypselodoris festiva",
  "殻を失った巻貝の仲間。鮮やかな色は毒をもつ警告とされる。", ["ウミウシ"])
S("namekuji", "heterobranchia", "ナメクジ", "Meghimatium bilineatum",
  "殻を失った陸の巻貝。", ["フタスジナメクジ"])
C("veneridae", "bivalvia", "マルスダレガイ科", "Veneridae", "科", "ハマグリ・アサリなど。")
move("veneridae", "hamaguri")
S("asari", "veneridae", "アサリ", "Ruditapes philippinarum",
  "殻の模様は1個ずつ違う。2本の水管を砂の上に出して呼吸と食事をする。")
S("hotategai", "bivalvia", "ホタテガイ", "Mizuhopecten yessoensis",
  "殻をすばやく開閉して水を噴き出し、泳いで逃げる。外套膜の縁に多数の目がある。", ["ホタテ"],
  v={"sci": "Patinopecten yessoensis とする扱いもある"})
S("murasakiigai", "bivalvia", "ムラサキイガイ", "Mytilus galloprovincialis",
  "足糸で岩などに付着する。地中海原産の外来種。", ["ムール貝", "イガイ"])
S("yamatoshijimi", "bivalvia", "ヤマトシジミ", "Corbicula japonica",
  "河口の汽水域にすむ。食用のシジミの多くは本種。", ["シジミ"])
S("hirejako", "bivalvia", "ヒレシャコガイ", "Tridacna squamosa",
  "外套膜に褐虫藻を共生させ、光合成の産物を利用する。", ["ヒレジャコ", "シャコガイ"])

# ---------------- 環形 ----------------
edit("annelida", polytomy="ホシムシ類・ウミケムシ類などの基部の分岐順は議論中のため、多分岐で示す。")
S("sujihoshimushi", "annelida", "スジホシムシ", "Sipunculus nudus",
  "体節のない筒形の動物。かつては独立の星口動物門とされたが、分子系統で環形動物に含まれた。", ["ホシムシ", "星口動物"])
S("umikemushi", "annelida", "ウミケムシ", "Chloeia flava",
  "体側の毛は刺さると痛み、毒がある。", v={"ja": "日本産の種名は要確認"})
C("pleistoannelida", "annelida", "Pleistoannelida", "Pleistoannelida", "クレード", "よく動き回る Errantia と、定住性の多毛類やミミズ・ヒルを含む Sedentaria をまとめた、環形動物の大部分を含むクレード。",
  v={"ja": "定着した和名が確認できないため学名で表記"})
C("errantia", "pleistoannelida", "Errantia", "Errantia", "クレード", "よく動き回る多毛類。ゴカイやイソメなど。",
  v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
C("sedentaria", "pleistoannelida", "Sedentaria", "Sedentaria", "クレード", "管や巣穴にとどまる多毛類と、ミミズ・ヒルの仲間。",
  v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
move("errantia", "yamatokawagokai")
move("sedentaria", "yumushi", "satsumahaorimushi", "clitellata")
S("iwamushi", "errantia", "イワムシ", "Marphysa sanguinea",
  "釣り餌にされる大型のイソメ類。", ["イソメ"], v={"sci": "日本産を別種とする研究がある"})
S("keyarimushi", "sedentaria", "ケヤリムシ", "Sabellastarte japonica",
  "管から羽のようなえら（鰓冠）を広げ、触れるとすばやく引っ込める。", v={"ja": "標準和名と学名の対応を要確認"})
C("hirudinea", "clitellata", "ヒル亜綱", "Hirudinea", "亜綱", "前後に吸盤をもつ。ミミズの仲間の中から生じた。")
move("hirudinea", "chisuibiru")
S("yamabiru", "hirudinea", "ヤマビル", "Haemadipsa japonica",
  "陸にすむヒル。動物の吐く二酸化炭素や体温を感じて近寄る。", ["ヒル"])
S("shimamimizu", "clitellata", "シマミミズ", "Eisenia fetida",
  "堆肥の中に多い。生ごみ処理にも使われる。", ["ミミズ"])

# ---------------- 扁形 ----------------
C("tricladida", "platyhelminthes", "三岐腸目", "Tricladida", "目", "腸が三つに分かれる。プラナリアやコウガイビル。")
C("neodermata", "platyhelminthes", "Neodermata", "Neodermata", "クレード", "吸虫・条虫・単生類をまとめた寄生性のクレード。幼生の表皮を脱ぎ捨てる。",
  v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
C("trematoda", "neodermata", "吸虫綱", "Trematoda", "綱", "吸盤で宿主にとりつく寄生虫。貝を中間宿主にするものが多い。")
C("cestoda", "neodermata", "条虫綱", "Cestoda", "綱", "サナダムシの仲間。口も腸もなく、体表から栄養を吸収する。")
move("tricladida", "namiuzumushi")
move("cestoda", "nihonkairettojouchu")
S("tsunohiramushi", "platyhelminthes", "ツノヒラムシ", "Planocera reticulata",
  "磯の石の下にいる多岐腸類。薄い体で滑るように動く。", ["ヒラムシ"], v={"ja": "標準和名と学名の対応を要確認"})
S("oomisujikougaibiru", "tricladida", "オオミスジコウガイビル", "Bipalium nobile",
  "頭が半月形の陸生のプラナリア。1 mに達することもある。", ["コウガイビル"])
S("nihonjuketsukyuchu", "trematoda", "日本住血吸虫", "Schistosoma japonicum",
  "1904年に日本で発見された。中間宿主のミヤイリガイの駆除などで、国内では流行が終わった。",
  ["ニホンジュウケツキュウチュウ", "住血吸虫"])
S("kankyuchu", "trematoda", "肝吸虫", "Clonorchis sinensis",
  "コイ科の淡水魚の生食で感染し、胆管にすむ。", ["カンキュウチュウ"], v={"sci": "Opisthorchis 属に含める見解がある"})
S("takoujouchu", "cestoda", "多包条虫", "Echinococcus multilocularis",
  "キツネなどの腸にすみ、人に感染すると肝臓に病巣を作る（エキノコックス症）。北海道に多い。",
  ["タホウジョウチュウ", "エキノコックス"])

# ---------------- 線形 ----------------
C("rhabditida", "nematoda", "Rhabditida", "Rhabditida", "目", "線虫の多くを含む大きな目。自由生活の線虫と多くの寄生虫。",
  v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
C("spirurina", "rhabditida", "Spirurina", "Spirurina", "亜目", "動物に寄生する線虫の多くを含む。回虫・蟯虫・糸状虫など。",
  v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
C("tylenchina", "rhabditida", "Tylenchina", "Tylenchina", "亜目", "口針で植物の細胞を吸う植物寄生線虫などを含む。",
  v={"ja": "定着した和名が確認できないため学名で表記"})
move("rhabditida", "celegans")
move("spirurina", "kaichu")
move("tylenchina", "matsunozaisenchu")
S("anisakis", "spirurina", "イルカウミカイチュウ", "Anisakis simplex",
  "幼虫がサバやイカなどにいて、生食すると胃に激痛を起こすことがある。", ["アニサキス", "アニサキス・シンプレックス"],
  v={"ja": "和名は GBIF・iNaturalist で一致。一般には属名のアニサキスで呼ばれる。標準和名リストでは未確認"})
S("gyochu", "spirurina", "ヒトギョウチュウ", "Enterobius vermicularis",
  "夜に肛門の周りに出てきて卵を産む。", ["ギョウチュウ", "蟯虫"])
S("inushijouchu", "spirurina", "イヌ糸状虫", "Dirofilaria immitis",
  "蚊が媒介し、イヌの心臓や肺動脈にすむ（フィラリア症）。", ["フィラリア", "イヌシジョウチュウ"])
S("nekobusenchu", "tylenchina", "サツマイモネコブセンチュウ", "Meloidogyne incognita",
  "根に入りこんでこぶを作る。世界的な農業害虫。", ["ネコブセンチュウ"])
S("senmouchu", "nematoda", "旋毛虫", "Trichinella spiralis",
  "幼虫が筋肉の中にすむ。クマ肉などの生食で感染する。ほかの多くの線虫と早い時期に分かれた系統。",
  ["センモウチュウ", "トリヒナ"])

# ---------------- その他の門 ----------------
S("onikumamushi", "tardigrada", "オニクマムシ", "Milnesium tardigradum",
  "肉食のクマムシ。ほかのクマムシやワムシを食べる。", ["クマムシ"],
  v={"sci": "日本産を本種とするかは要確認（近縁の別種が記載されている）"})
S("adineta", "rotifera", "アディネタ・ウァガ", "Adineta vaga",
  "ヒルガタワムシの一種。雌だけで数千万年続いてきたとされ、ほかの生物の遺伝子を取り込んでいる。",
  ["ヒルガタワムシ", "ワムシ"], jaStatus="provisional", v={"ja": "和名なし（学名の音写）"})
S("kubinagakoutouchu", "acanthocephala", "クビナガコウトウチュウ", "Longicollum pagrosomi",
  "マダイなどの腸に寄生する鉤頭虫。", ["鉤頭虫"], v={"ja": "標準和名と学名の対応を要確認"})
S("misakihimomushi", "nemertea", "ミサキヒモムシ", "Notospermus geniculatus",
  "黒地に白い横帯がある。ちぎれやすく、断片から再生することがある。", ["ヒモムシ"], v={"ja": "標準和名と学名の対応を要確認"})
S("kamehoozukichouchin", "brachiopoda", "ホウズキチョウチン", "Laqueus rubellus",
  "ほおずき提灯のような殻をもつ腕足動物。柄で岩に付着する。", ["ホオズキチョウチン", "チョウチンガイ"], v={"ja": "和名は GBIF・iNaturalist で一致。標準和名リストでは未確認"})
S("fusakokemushi", "bryozoa", "フサコケムシ", "Bugula neritina",
  "赤褐色の房状の群体を作る。共生細菌が作るブリオスタチンが薬として研究された。", ["コケムシ"])

# ---------------- メタ情報 ----------------
META["referenceDate"] = "2026-10-22"
META["status"] = ("学名と和名を GBIF・Catalogue of Life・WoRMS・Wikidata・iNaturalist と照合済み（初版134種・v0.3追加138種とも 2026-10-22）。"
                  "標準和名リストとの手作業の突き合わせは未実施。魚類は Eschmeyer's Catalog of Fishes と未照合。verify が付いた項目は特に要確認。")

# ---------------- 少ない群への追加（2026-10-22） ----------------
# 綱・目などの節目で収録が4種以下だと、そこまで絞れた後に総当たりで当たってしまうので候補を増やす。
# 作者の判断で、これらも出題対象にする（推測専用にすると「正解にならない」と覚えられるため）。
# 図鑑や水族館で見かける程度の種を選ぶ。グループ名は aliases に入れない。
R = S

# 海綿
R("mokuyokukaimen", "demospongiae", "モクヨクカイメン", "Spongia officinalis", "地中海産。骨格が柔らかい繊維だけでできていて、昔から入浴用の海綿にされた。")
# 刺胞
R("tatejimaisoginchaku", "actiniaria", "タテジマイソギンチャク", "Diadumene lineata", "体に縦じまがある小型種。分裂して増え、世界中の港に広がった。")
R("hatagoisoginchaku", "actiniaria", "ハタゴイソギンチャク", "Stichodactyla gigantea", "サンゴ礁の大型のイソギンチャク。クマノミ類がすむ。")
R("kusabiraishi", "scleractinia", "シタザラクサビライシ", "Fungia fungites", "1つの大きなポリプからなる、きのこの傘のような円盤形のサンゴ。固着せず海底に転がっている。")
R("hiranousango", "scleractinia", "ヒラノウサンゴ", "Platygyra daedalea", "表面に脳のような溝が走る塊状のサンゴ。")
R("aosango", "octocorallia", "アオサンゴ", "Heliopora coerulea", "骨格が青い八放サンゴ。石垣島の白保には大きな群落がある。")
R("momoirosango", "octocorallia", "モモイロサンゴ", "Pleurocorallium elatius", "桃色の宝石サンゴ。かつては Corallium 属に置かれた。")
R("bizenkurage", "scyphozoa", "ビゼンクラゲ", "Rhopilema esculentum", "中華料理の食用クラゲの原料になる。")
R("ginkakurage", "hydrozoa", "ギンカクラゲ", "Porpita porpita", "銀色の円盤の浮きで海面を漂う。カツオノカンムリに近い。")
R("owankurage", "hydrozoa", "オワンクラゲ", "Aequorea coerulescens", "近縁種から見つかった緑色蛍光タンパク質（GFP）は2008年のノーベル化学賞につながった。",
  v={"sci": "GFP が見つかったのは北米の A. victoria。日本産の種名は要確認"})
R("hanagasakurage", "hydrozoa", "ハナガサクラゲ", "Olindias formosus", "傘の縁に色とりどりの触手が並ぶ美しいクラゲ。")
# 棘皮
R("aohitode", "asteroidea", "アオヒトデ", "Linckia laevigata", "サンゴ礁にすむ鮮やかな青色のヒトデ。")
R("momijigai", "asteroidea", "モミジガイ", "Astropecten scoparius", "砂に潜り、貝などを丸のみにする。管足に吸盤がない。")
R("yatsudehitode", "asteroidea", "ヤツデヒトデ", "Coscinasterias acutispina", "腕が7〜8本あり、体を分裂させて増える。")
R("akauni", "echinoidea", "アカウニ", "Pseudocentrotus depressus", "食用にされる。棘は短く赤みがある。")
R("kitamurasakiuni", "echinoidea", "キタムラサキウニ", "Mesocentrotus nudus", "北日本の食用ウニ。かつては Strongylocentrotus 属に置かれた。")
R("rappauni", "echinoidea", "ラッパウニ", "Toxopneustes pileolus", "棘の間のラッパ形の叉棘に強い毒がある。")
R("paipuuni", "echinoidea", "パイプウニ", "Heterocentrotus mamillatus", "鉛筆ほどの太い棘をもつ。棘は風鈴などに使われる。")
R("nisekuronamako", "holothuroidea", "ニセクロナマコ", "Holothuria leucospilota", "刺激すると白い糸状の器官（キュビエ器官）を吹き出す。")
R("shikakunamako", "holothuroidea", "シカクナマコ", "Stichopus chloronotus", "断面が四角い。体を自分で切って増えることがある。")
# 軟骨魚
R("akashumokuzame", "selachii", "アカシュモクザメ", "Sphyrna lewini", "左右に張り出した頭の両端に目がある。群れをつくることがある。", v={"sci": FISH_V})
R("nekozame", "selachii", "ネコザメ", "Heterodontus japonicus", "臼のような歯でサザエなどの貝を割って食べる。卵はらせん状の殻に包まれる。", v={"sci": FISH_V})
R("rabuka", "selachii", "ラブカ", "Chlamydoselachus anguineus", "深海にすむ古いタイプのサメ。ひだ状の鰓孔が6対ある。", v={"sci": FISH_V})
R("shibireei", "batoidea", "シビレエイ", "Narke japonica", "発電器官で電気を起こす。", v={"sci": FISH_V})
R("narutobiei", "batoidea", "ナルトビエイ", "Aetobatus narutobiei", "有明海などで二枚貝を食べる。2013年に新種として記載された。", v={"sci": FISH_V})
# 条鰭類
R("nishin", "clupeiformes", "ニシン", "Clupea pallasii", "春に北海道の沿岸に押し寄せて産卵した。卵は数の子になる。", v={"sci": FISH_V})
R("urumeiwashi", "clupeiformes", "ウルメイワシ", "Etrumeus micropus", "目が脂瞼に覆われて潤んだように見える。北西太平洋の個体群は E. teres から分けられた。", v={"sci": FISH_V})
R("konoshiro", "clupeiformes", "コノシロ", "Konosirus punctatus", "出世魚で、小さいものはコハダとして寿司種にされる。", v={"sci": FISH_V})
R("oikawa", "ostariophysi", "オイカワ", "Opsariichthys platypus", "繁殖期の雄は青や赤の婚姻色になる。", v={"sci": FISH_V})
R("ugui", "ostariophysi", "ウグイ", "Pseudaspius hakonensis", "海に下る個体もいる。かつては Tribolodon 属に置かれた。", v={"sci": FISH_V})
R("zebrafish", "ostariophysi", "ゼブラフィッシュ", "Danio rerio", "胚が透明で発生を観察しやすいモデル生物。", jaStatus="common", v={"sci": FISH_V})
R("kitanomedaka", "beloniformes", "キタノメダカ", "Oryzias sakaizumii", "日本海側に分布するメダカ。2012年にミナミメダカと別種とされた。", v={"sci": FISH_V})
R("sayori", "beloniformes", "サヨリ", "Hyporhamphus sajori", "下あごが長く突き出る。", v={"sci": FISH_V})
R("datsu", "beloniformes", "ダツ", "Strongylura anastomella", "光に向かって突進する性質があり、夜の海で人に刺さる事故がある。", v={"sci": FISH_V})
R("masaba", "scombridae", "マサバ", "Scomber japonicus", "背に波のような模様がある。", v={"sci": FISH_V})
R("sawara", "scombridae", "サワラ", "Scomberomorus niphonius", "細長い体の大型のサバ科魚類。", v={"sci": FISH_V})
R("kihada", "scombridae", "キハダ", "Thunnus albacares", "第2背鰭と尻鰭が黄色く長く伸びるマグロ。", v={"sci": FISH_V})
R("kawahagi", "tetraodontiformes", "カワハギ", "Stephanolepis cirrhifer", "硬い皮をはいで料理することが名の由来。", v={"sci": FISH_V})
R("harisenbon", "tetraodontiformes", "ハリセンボン", "Diodon holocanthus", "水を飲んでふくらみ、鱗が変化した棘を立てる。", v={"sci": FISH_V})
R("hakofugu", "tetraodontiformes", "ハコフグ", "Ostracion immaculatum", "骨板が組み合わさった箱のような体をもつ。", v={"sci": FISH_V})
R("ushimanbou", "tetraodontiformes", "ウシマンボウ", "Mola alexandrini", "マンボウより大きくなり、硬骨魚類で最も重い記録をもつ。", v={"sci": FISH_V})
# 両生類
R("ushigaeru", "anura", "ウシガエル", "Aquarana catesbeiana", "北米原産の特定外来生物。牛のような声で鳴く。", v={"sci": "Lithobates catesbeianus とする扱いもある"})
R("schlegelaogaeru", "anura", "シュレーゲルアオガエル", "Zhangixalus schlegelii", "日本固有種。田の畔に泡の卵塊を産む。かつては Rhacophorus 属に置かれた。")
R("moriaogaeru", "anura", "モリアオガエル", "Zhangixalus arboreus", "水辺の木の枝に泡の卵塊を産み、孵ったオタマジャクシが水に落ちる。")
R("hakonesanshouo", "caudata", "ハコネサンショウウオ", "Onychodactylus japonicus", "成体は肺をもたず、皮膚で呼吸する。", v={"sci": "近年複数種に分けられた"})
R("shirikenimori", "caudata", "シリケンイモリ", "Cynops ensicauda", "奄美・沖縄のイモリ。尾が剣のように平たい。")
R("axolotl", "caudata", "メキシコサンショウウオ", "Ambystoma mexicanum", "幼生の姿のまま成熟する。ウーパールーパーの名で知られる。", ["ウーパールーパー", "アホロートル"])
# 哺乳類
R("gorilla", "hominidae", "ニシゴリラ", "Gorilla gorilla", "最大の霊長類。", jaStatus="common")
R("orangutan", "hominidae", "ボルネオオランウータン", "Pongo pygmaeus", "樹上で暮らす大型類人猿。", jaStatus="common")
R("waokitsunezaru", "primates", "ワオキツネザル", "Lemur catta", "マダガスカルにすむ原猿類。尾に白黒の輪の模様がある。", jaStatus="common")
R("akagezaru", "primates", "アカゲザル", "Macaca mulatta", "ニホンザルと同じマカク属。医学研究に多く使われ、Rh因子の名の由来になった。")
R("nihonrisu", "rodentia", "ニホンリス", "Sciurus lis", "日本固有のリス。冬眠しない。")
R("akanezumi", "muridae", "アカネズミ", "Apodemus speciosus", "日本固有の野ネズミ。ドングリを土に埋めて蓄える。")
R("capybara", "rodentia", "カピバラ", "Hydrochoerus hydrochaeris", "現生最大の齧歯類。", jaStatus="common")
R("nutria", "rodentia", "ヌートリア", "Myocastor coypus", "南米原産の特定外来生物。毛皮用に持ち込まれた。")
R("amaminokurousagi", "lagomorpha", "アマミノクロウサギ", "Pentalagus furnessi", "奄美大島と徳之島だけにすむ。耳が短い原始的なウサギ。特別天然記念物。")
R("anausagi", "lagomorpha", "アナウサギ", "Oryctolagus cuniculus", "飼いウサギの祖先。地下に巣穴を掘る。", ["カイウサギ"])
R("kitanakiusagi", "lagomorpha", "キタナキウサギ", "Ochotona hyperborea", "北海道の岩場にすむ。高い声で鳴く。エゾナキウサギはその亜種。", ["エゾナキウサギ"])
R("koubemogura", "eulipotyphla", "コウベモグラ", "Mogera wogura", "西日本に多い大型のモグラ。")
R("amurharinezumi", "eulipotyphla", "アムールハリネズミ", "Erinaceus amurensis", "背中の毛が針になっている。日本では外来種。")
R("kubiwaookoumori", "chiroptera", "クビワオオコウモリ", "Pteropus dasymallus", "果実を食べる大型のコウモリ。エコーロケーションをしない。")
R("yubinagakoumori", "chiroptera", "ユビナガコウモリ", "Miniopterus fuliginosus", "洞窟で大きな集団をつくる。")
R("nihonanaguma", "caniformia", "ニホンアナグマ", "Meles anakuma", "日本固有のアナグマ。イタチ科。")
R("rakko", "caniformia", "ラッコ", "Enhydra lutris", "腹の上で石を使って貝を割る。")
R("todo", "caniformia", "トド", "Eumetopias jubatus", "最大のアシカ科の動物。")
R("panda", "caniformia", "ジャイアントパンダ", "Ailuropoda melanoleuca", "クマ科だが、ほとんど竹だけを食べる。", ["パンダ"])
R("ookami", "canidae", "タイリクオオカミ", "Canis lupus", "イエイヌの祖先。", ["オオカミ"])
R("lion", "feliformia", "ライオン", "Panthera leo", "群れで暮らす唯一のネコ科動物。", jaStatus="common")
R("tora", "feliformia", "トラ", "Panthera tigris", "最大のネコ科動物。")
R("buchihyena", "feliformia", "ブチハイエナ", "Crocuta crocuta", "イヌに似るが、ネコ型亜目でマングースなどに近い。")
R("hakubishin", "feliformia", "ハクビシン", "Paguma larvata", "額から鼻に白い線がある。ジャコウネコ科。")
R("kirin", "ruminantia", "キリン", "Giraffa camelopardalis", "首の骨の数はヒトと同じ7個。", v={"sci": "複数種に分ける提案がある"})
R("herajika", "ruminantia", "ヘラジカ", "Alces alces", "最大のシカ。雄はへら状の大きな角をもつ。")
R("africasuigyu", "ruminantia", "アフリカスイギュウ", "Syncerus caffer", "大きな群れで暮らすウシ科の動物。", jaStatus="common")
R("shirosai", "perissodactyla", "シロサイ", "Ceratotherium simum", "幅の広い口で草を食べる。", jaStatus="common")
R("mareebaku", "perissodactyla", "マレーバク", "Tapirus indicus", "白黒の体色。サイやウマと同じ奇蹄目。", jaStatus="common",
  v={"sci": "Acrocodia 属に分ける扱いもある"})
# 爬虫類
R("shimahebi", "serpentes", "シマヘビ", "Elaphe quadrivirgata", "体に4本の縦じまがある。黒化型はカラスヘビと呼ばれる。")
R("yamakagashi", "serpentes", "ヤマカガシ", "Rhabdophis tigrinus", "奥歯に毒牙をもつ。首の腺にはヒキガエルから取り込んだ毒をためる。")
R("erabuumihebi", "serpentes", "エラブウミヘビ", "Laticauda semifasciata", "海で暮らすが、産卵は陸の岩の隙間で行う。")
R("amimenishikihebi", "serpentes", "アミメニシキヘビ", "Malayopython reticulatus", "世界最長のヘビ。かつては Python 属に置かれた。")
R("kusagame", "testudines", "クサガメ", "Mauremys reevesii", "危険を感じると臭いにおいを出す。日本のものは古い時代の移入とされる。")
R("akamimigame", "testudines", "アカミミガメ", "Trachemys scripta", "ミドリガメとして売られた北米原産のカメ。日本で野生化したものの多くは亜種ミシシッピアカミミガメ。条件付特定外来生物。", ["ミシシッピアカミミガメ", "ミドリガメ"])
R("suppon", "testudines", "スッポン", "Pelodiscus sinensis", "甲羅が柔らかい皮膚におおわれる。", ["チュウゴクスッポン"], v={"sci": "日本産を P. japonicus とする見解がある", "ja": "P. sinensis の和名は GBIF・iNat ではチュウゴクスッポン"})
R("aoumigame", "testudines", "アオウミガメ", "Chelonia mydas", "成体は海藻や海草を食べる。脂肪が緑色を帯びることが名の由来。")
# 鳥類
R("raichou", "galliformes", "ライチョウ", "Lagopus muta", "日本アルプスなどの高山にすむ。冬は白い羽に生え変わる。")
R("yamadori", "galliformes", "ヤマドリ", "Syrmaticus soemmerringii", "日本固有種。雄は長い尾をもつ。")
R("kujaku", "galliformes", "インドクジャク", "Pavo cristatus", "雄の飾り羽は尾ではなく背中の羽。", ["クジャク"])
R("oshidori", "anseriformes", "オシドリ", "Aix galericulata", "雄は銀杏羽と呼ばれる飾り羽をもつ。")
R("karugamo", "anseriformes", "カルガモ", "Anas zonorhyncha", "雌雄が似た色のカモ。日本で一年中見られる。")
R("magan", "anseriformes", "マガン", "Anser albifrons", "冬に宮城県の伊豆沼などに大群で渡ってくる。")
R("kohakuchou", "anseriformes", "コハクチョウ", "Cygnus columbianus", "オオハクチョウより小さく、くちばしの黄色い部分が少ない。")
# 節足（鋏角・多足・甲殻）
R("nagakoganegumo", "araneae", "ナガコガネグモ", "Argiope bruennichi", "網にジグザグの白い帯（隠れ帯）をつける。")
R("oohimegumo", "araneae", "オオヒメグモ", "Parasteatoda tepidariorum", "家の隅に不規則な網を張る。発生研究のモデル生物。")
R("seakagokegumo", "araneae", "セアカゴケグモ", "Latrodectus hasselti", "オーストラリア原産の毒グモ。特定外来生物。")
R("aozumukade", "chilopoda", "アオズムカデ", "Scolopendra japonica", "頭が青黒いムカデ。")
R("yanbarutosakayasude", "diplopoda", "ヤンバルトサカヤスデ", "Chamberlinius hualienensis", "台湾原産。沖縄などで大発生する。")
R("warajimushi", "isopoda", "ワラジムシ", "Porcellio scaber", "ダンゴムシに似るが丸まれない。")
R("hamadangomushi", "isopoda", "ハマダンゴムシ", "Tylos granuliferus", "砂浜にすみ、夜に活動する。")
R("yashigani", "anomura", "ヤシガニ", "Birgus latro", "最大の陸生甲殻類。ヤドカリの仲間で、幼い時は貝殻を背負う。")
R("murasakiokayadokari", "anomura", "ムラサキオカヤドカリ", "Coenobita purpureus", "陸で暮らすヤドカリ。天然記念物。")
R("hanasakigani", "anomura", "ハナサキガニ", "Paralithodes brevipes", "タラバガニに近い。根室半島の名物。")
R("gazami", "brachyura", "ガザミ", "Portunus trituberculatus", "最後の脚がひれ状で、泳ぐことができる。", ["ワタリガニ"])
R("kegani", "brachyura", "ケガニ", "Erimacrus isenbeckii", "全身が短い毛におおわれる。")
R("takaashigani", "brachyura", "タカアシガニ", "Macrocheira kaempferi", "脚を広げると3 m以上になる世界最大のカニ。")
R("mokuzugani", "brachyura", "モクズガニ", "Eriocheir japonica", "はさみに毛の房がある。海で生まれ川で育つ。")
# 昆虫
R("shiokaratombo", "odonata", "シオカラトンボ", "Orthetrum albistylum", "雄は成熟すると白い粉をふいて塩辛色になる。")
R("ginyanma", "odonata", "ギンヤンマ", "Anax parthenope", "池の上をパトロールするように飛ぶ。", v={"sci": "日本産は亜種 A. p. julius とされる"})
R("hagurotombo", "odonata", "ハグロトンボ", "Atrocalopteryx atrata", "黒い翅をもつカワトンボの仲間。")
R("mukashitombo", "odonata", "ムカシトンボ", "Epiophlebia superstes", "日本固有種。トンボとイトトンボの中間的な特徴をもつ。")
R("shouryoubatta", "orthoptera", "ショウリョウバッタ", "Acrida cinerea", "頭がとがった細長いバッタ。雄は飛ぶときキチキチと音を出す。")
R("higashikirigirisu", "orthoptera", "ヒガシキリギリス", "Gampsocleis mikado", "かつてキリギリス1種とされたものが東西2種に分けられた。", ["キリギリス"],
  v={"sci": "GBIF は G. buergeri にまとめている"})
R("kera", "orthoptera", "ケラ", "Gryllotalpa orientalis", "モグラのような前脚で土を掘る。")
R("suzumushi", "orthoptera", "スズムシ", "Meloimorpha japonica", "江戸時代から鳴き声を楽しむために飼われてきた。")
R("haraburokamakiri", "dictyoptera", "ハラビロカマキリ", "Hierodula patellifera", "腹部の幅が広いカマキリ。")
R("chabanegokiburi", "blattodea", "チャバネゴキブリ", "Blattella germanica", "飲食店などに多い小型のゴキブリ。")
R("wamongokiburi", "blattodea", "ワモンゴキブリ", "Periplaneta americana", "胸に輪の模様がある大型種。")
R("ieshiroari", "blattodea", "イエシロアリ", "Coptotermes formosanus", "大きな巣を作り、建物に大きな被害を与える。")
R("minminzemi", "hemiptera", "ミンミンゼミ", "Hyalessa maculaticollis", "ミーンミンミンと鳴く。")
R("tsukutsukuboushi", "hemiptera", "ツクツクボウシ", "Meimuna opalifera", "夏の終わりに鳴く小型のセミ。")
R("tagame", "hemiptera", "タガメ", "Kirkaldyia deyrollei", "日本最大の水生カメムシ。雄が卵を守る。")
R("kusagikamemushi", "hemiptera", "クサギカメムシ", "Halyomorpha halys", "秋に家屋に入り込んで越冬する。")
R("nihonmitsubachi", "hymenoptera", "トウヨウミツバチ", "Apis cerana", "日本の在来亜種がニホンミツバチ。オオスズメバチを集団で包んで熱殺する。", ["ニホンミツバチ"])
R("kiirosuzumebachi", "hymenoptera", "キイロスズメバチ", "Vespa simillima", "都市部の軒下にも大きな巣を作る。")
R("seguroashinagabachi", "hymenoptera", "セグロアシナガバチ", "Polistes jokahamae", "傘のような形の巣を作る。")
R("argentinaari", "hymenoptera", "アルゼンチンアリ", "Linepithema humile", "南米原産の特定外来生物。巨大な巣のネットワークを作る。")
R("aosujiageha", "lepidoptera", "アオスジアゲハ", "Graphium sarpedon", "翅に青緑色の帯がある。幼虫はクスノキの葉を食べる。")
R("yamamayu", "lepidoptera", "ヤママユ", "Antheraea yamamai", "緑色の繭から天蚕糸がとれる。")
R("asagimadara", "lepidoptera", "アサギマダラ", "Parantica sita", "日本から台湾まで1000 km以上を渡ることがある。")
R("akaieka", "diptera", "アカイエカ", "Culex pipiens", "夜に家の中で人を刺す。", v={"sci": "日本産は亜種 C. p. pallens とされる"})
# 軟体
R("iidako", "octopodiformes", "イイダコ", "Amphioctopus fangsiao", "冬から春に飯粒のような卵をもつことが名の由来。")
R("hyoumondako", "octopodiformes", "ヒョウモンダコ", "Hapalochlaena fasciata", "唾液にテトロドトキシンをもつ。興奮すると青い輪が浮かぶ。", v={"sci": "日本産の種名は要確認"})
R("koumoridako", "octopodiformes", "コウモリダコ", "Vampyroteuthis infernalis", "深海にすむ。タコとイカの中間的な特徴をもつ独自の目。")
R("aoriika", "decapodiformes", "アオリイカ", "Sepioteuthis lessoniana", "大きな鰭が胴の全体にある。", v={"sci": "複数の隠蔽種を含むとされる"})
R("yariika", "decapodiformes", "ヤリイカ", "Heterololigo bleekeri", "槍の穂先のような細長い胴をもつ。かつては Loligo 属に置かれた。")
R("kensakiika", "decapodiformes", "ケンサキイカ", "Uroteuthis edulis", "剣のような胴をもつ。")
# 環形・扁形・線形
R("itomimizu", "clitellata", "イトミミズ", "Tubifex tubifex", "泥の中に頭を入れ、尾を揺らして呼吸する。", v={"sci": "日本産の種同定は要確認"})
R("umabiru", "hirudinea", "ウマビル", "Whitmania pigra", "血を吸わず、貝などを丸のみにする。")
R("haikyuchu", "trematoda", "ウェステルマン肺吸虫", "Paragonimus westermani", "サワガニなどの生食で感染し、肺に寄生する。", ["ハイキュウチュウ"])
R("mukoujouchu", "cestoda", "無鉤条虫", "Taenia saginata", "牛肉の生食で感染するサナダムシ。", ["ムコウジョウチュウ"])
R("yuukoujouchu", "cestoda", "有鉤条虫", "Taenia solium", "豚肉の生食で感染する。頭部に鉤をもつ。", ["ユウコウジョウチュウ"])
R("inukaichu", "spirurina", "イヌ回虫", "Toxocara canis", "イヌの腸に寄生する回虫。", ["イヌカイチュウ"])

# ---------------- 魚類の学名・和名を日本産魚類全種目録で照合（2026-10-23） ----------------
# 基準：本村浩之．2026．日本産魚類全種目録．これまでに記録された日本産魚類全種の現在の標準和名と学名．
#       Online ver. 42（2026-08-27）．https://www.museum.kagoshima-u.ac.jp/staff/motomura/jaf.html
# 照合に使っただけで、一覧そのものは同梱していない。結果は check/fish_jaf/summary.md。
edit("katakuchiiwashi", sci="Engraulis japonica", aliases=["イワシ", "シラス", "Engraulis japonicus"])
edit("hohojirozame", ja="ホオジロザメ")
edit("mikadochozame", ja="チョウザメ", sci="Sinosturio medirostris",
     fact="チョウザメは軟質類で、硬い鱗が体に並ぶ古いタイプの条鰭類。2025年に Acipenser 属から Sinosturio 属に移された。",
     aliases=["Acipenser medirostris"])
JAF_OK = ['nutaunagi', 'kawayatsume', 'jinbeizame', 'akaei', 'ginzame', 'nihonunagi', 'maiwashi', 'koi', 'minamimedaka', 'kuromaguro', 'tatsunootoshigo', 'madai', 'nanyoumanta', 'namazu', 'sake', 'ayu', 'madara', 'sanma', 'katsuo', 'torafugu', 'manbou', 'hirame', 'kakurekumanomi', 'mahaze', 'akashumokuzame', 'nekozame', 'rabuka', 'shibireei', 'narutobiei', 'nishin', 'urumeiwashi', 'konoshiro', 'oikawa', 'ugui', 'kitanomedaka', 'sayori', 'datsu', 'masaba', 'sawara', 'kihada', 'kawahagi', 'harisenbon', 'hakofugu', 'ushimanbou', 'katakuchiiwashi', 'hohojirozame', 'mikadochozame']
for _id in JAF_OK:
    _x = _find(_id)
    if _x.get("verify", {}).get("sci"):
        del _x["verify"]["sci"]
        if not _x["verify"]: del _x["verify"]
edit("zebrafish", verify={"sci": "日本産ではないため日本産魚類全種目録の対象外。Catalog of Fishes とは未照合"})
META["taxonomy"]["nomenclature"] = ("学名は GBIF Backbone / Catalogue of Life (ChecklistBank 3LR) / WoRMS の多数決で照合（2026-10-22、tools/name_consensus.py）。"
    "日本産の魚類は本村浩之（2026）日本産魚類全種目録 Online ver. 42（2026-08-27）の標準和名・学名に合わせた（2026-10-23）")
# 公開ページ向けの meta（2026-10-23、GitHub Pages 公開にあわせて内部メモを除いた）
META["taxonomy"]["nomenclature"] = ("学名は GBIF Backbone Taxonomy・Catalogue of Life・WoRMS で照合（2026-10-22）。"
    "日本産の魚類は本村浩之（2026）日本産魚類全種目録 Online ver. 42 に合わせた（2026-10-23）")
META["japaneseNameSources"] = ["本村浩之（2026）日本産魚類全種目録 Online ver. 42（魚類）",
    "GBIF・Wikidata・iNaturalist の日本語名（2つ以上の一致で採用）"]
META["status"] = "試作版。鳥類・哺乳類・爬虫両生類・昆虫などの標準和名リストとの突き合わせは未実施。verify が付いた項目は要確認。"
META["licenseNotes"] = "外部の情報源のデータは丸ごと同梱していない（名前は照合結果を個別に記載）。"

# ---------------- メジャーな動物の追加（2026-10-23） ----------------
# 作者「もっとメジャーな生物を」「節足動物・魚類は綱（目）が多い分増やす」。候補は check/major/candidates.md。
# 魚の和名・学名と目は本村（2026）日本産魚類全種目録 ver. 42 に合わせた（スズキはペルカ目ではなくホタルジャコ目、など）。
M = S

# 哺乳類
C("marsupialia", "theria", "有袋類", "Marsupialia", "クレード", "未熟な子を産み、多くは袋で育てる哺乳類。")
move("marsupialia", "akakangaroo")
M("koala", "marsupialia", "コアラ", "Phascolarctos cinereus", "ユーカリの葉だけを食べ、腸内細菌の助けで毒を分解する。")
M("ooarikui", "xenarthra", "オオアリクイ", "Myrmecophaga tridactyla", "歯がなく、60 cmにもなる舌でアリやシロアリをなめとる。", ["アリクイ"])
M("futayubinamakemono", "xenarthra", "フタユビナマケモノ", "Choloepus didactylus", "木にぶら下がって暮らし、代謝がとても遅い。", ["ナマケモノ"], jaStatus="common")
M("goldenhamster", "rodentia", "ゴールデンハムスター", "Mesocricetus auratus", "頬袋に餌をためる。シリアの野生個体は少ない。", ["ハムスター"])
M("guineapig", "rodentia", "モルモット", "Cavia porcellus", "南米で家畜化されたテンジクネズミの仲間。", ["テンジクネズミ"])
C("felidae", "feliformia", "ネコ科", "Felidae", "科", "ネコ・ライオン・トラなど。爪を出し入れできるものが多い。")
move("felidae", "bengaruyamaneko", "lion", "tora")
M("ieneko", "felidae", "イエネコ", "Felis catus", "中東のリビアヤマネコから家畜化された。", ["ネコ", "猫"], v={"sci": "Felis silvestris catus（亜種）とする扱いもある"})
M("cheetah", "felidae", "チーター", "Acinonyx jubatus", "陸上で最も速い動物。爪を完全には引っ込められない。")
M("inu", "canidae", "イヌ", "Canis familiaris", "オオカミから家畜化された最初の家畜。", ["犬"], v={"sci": "タイリクオオカミの亜種 Canis lupus familiaris とする扱いもある"})
C("ursidae", "caniformia", "クマ科", "Ursidae", "科", "クマ・パンダ。かかとをつけて歩く。")
move("ursidae", "tsukinowaguma", "panda")
M("higuma", "ursidae", "ヒグマ", "Ursus arctos", "日本最大の陸上動物。北海道にすむ。")
M("hokkyokuguma", "ursidae", "ホッキョクグマ", "Ursus maritimus", "毛は透明で中空、皮膚は黒い。ヒグマと交雑できるほど近い。", ["シロクマ"])
C("mustelidae", "caniformia", "イタチ科", "Mustelidae", "科", "イタチ・テン・アナグマ・カワウソ・ラッコなど。")
move("mustelidae", "nihonanaguma", "rakko")
M("nihonitachi", "mustelidae", "ニホンイタチ", "Mustela itatsi", "日本固有のイタチ。細長い体でネズミの巣穴にも入る。")
C("pinnipedia", "caniformia", "鰭脚類", "Pinnipedia", "クレード", "アザラシ・アシカ・セイウチ。海にもどった食肉類。")
move("pinnipedia", "gomafuazarashi", "todo")
M("lesserpanda", "caniformia", "レッサーパンダ", "Ailurus fulgens", "ジャイアントパンダとは別の科（レッサーパンダ科）。先に「パンダ」と呼ばれたのはこちら。")
C("bovidae", "ruminantia", "ウシ科", "Bovidae", "科", "ウシ・ヤギ・ヒツジ・カモシカなど。角は生え変わらない。")
move("bovidae", "nihonkamoshika", "africasuigyu")
M("ushi", "bovidae", "ウシ", "Bos taurus", "絶滅したオーロックスから家畜化された。", ["牛"])
M("hitsuji", "bovidae", "ヒツジ", "Ovis aries", "野生のムフロンなどから家畜化された。毛は生え変わらず伸び続ける。", ["羊"])
M("yagi", "bovidae", "ヤギ", "Capra hircus", "野生のパサンから家畜化された。", ["山羊"])
M("hitokobu", "artiodactyla", "ヒトコブラクダ", "Camelus dromedarius", "こぶの中身は脂肪。ラクダ類は鯨偶蹄目の中で最初に分かれた系統。", ["ラクダ"])
C("odontoceti", "cetacea", "ハクジラ類", "Odontoceti", "クレード", "歯をもつクジラ。イルカやシャチ、マッコウクジラ。エコーロケーションをする。")
C("mysticeti", "cetacea", "ヒゲクジラ類", "Mysticeti", "クレード", "歯のかわりにヒゲ板でオキアミなどを濾しとるクジラ。")
move("odontoceti", "makkoukujira")
move("mysticeti", "shironagasu")
M("shachi", "odontoceti", "シャチ", "Orcinus orca", "最大のマイルカ科動物。群れで狩りをする。")
M("handouiruka", "odontoceti", "ハンドウイルカ", "Tursiops truncatus", "水族館でよく見られるイルカ。", ["バンドウイルカ"])
M("zatoukujira", "mysticeti", "ザトウクジラ", "Megaptera novaeangliae", "雄は長く複雑な「歌」をうたう。胸びれがとても長い。")
C("equus", "perissodactyla", "ウマ属", "Equus", "属", "ウマ・シマウマ・ロバ。指が1本だけになった。")
move("equus", "savannashimauma")
M("uma", "equus", "ウマ", "Equus caballus", "中央アジアの草原で家畜化された。", ["馬"], v={"sci": "Equus ferus caballus（亜種）とする扱いもある"})

# 鳥類
C("palaeognathae", "aves", "古顎類", "Palaeognathae", "クレード", "ダチョウ・エミュー・キーウィなど。多くは飛べない。")
move("palaeognathae", "dachou")
M("emu", "palaeognathae", "エミュー", "Dromaius novaehollandiae", "オーストラリアにすむ飛べない鳥。卵は雄が温める。")
C("columbidae", "neoaves", "ハト科", "Columbidae", "科", "ハトの仲間。")
move("columbidae", "kijibato")
M("kawarabato", "columbidae", "カワラバト", "Columba livia", "伝書鳩や町のドバトの原種。", ["ドバト", "伝書鳩"])
M("kakkou", "neoaves", "カッコウ", "Cuculus canorus", "ほかの鳥の巣に卵を産み、ひなを育てさせる（托卵）。")
M("benifuramingo", "neoaves", "ベニイロフラミンゴ", "Phoenicopterus ruber", "赤い色は餌の藻類やエビの色素。カイツブリに近い。", ["フラミンゴ"], jaStatus="common")
M("aosagi", "aequornithes", "アオサギ", "Ardea cinerea", "日本最大のサギ。")
M("kounotori", "aequornithes", "コウノトリ", "Ciconia boyciana", "日本の野生個体は一度絶滅し、兵庫県豊岡市で再導入された。")
M("ahoudori", "aequornithes", "アホウドリ", "Phoebastria albatrus", "翼を広げると2 mを超える。伊豆諸島の鳥島などで繁殖する。")
C("accipitridae", "afroaves", "タカ科", "Accipitridae", "科", "ワシ・タカ・トビなど。")
move("accipitridae", "inuwashi")
M("ootaka", "accipitridae", "オオタカ", "Astur gentilis", "森林で鳥を狩るタカ。近年 Accipiter 属から Astur 属に移された。", ["Accipiter gentilis"], v={"sci": "属の扱いは文献により異なる"})
M("tobi", "accipitridae", "トビ", "Milvus migrans", "ピーヒョロロと鳴きながら輪を描いて飛ぶ。", ["トンビ"])
M("kawasemi", "afroaves", "カワセミ", "Alcedo atthis", "水に飛び込んで魚をとる。くちばしの形は新幹線の先頭の設計に参考にされた。")
M("tsubame", "passeriformes", "ツバメ", "Hirundo rustica", "春に東南アジアから渡ってきて、人家の軒下に巣を作る。")
M("mejiro", "passeriformes", "メジロ", "Zosterops japonicus", "目の周りが白い。花の蜜を吸う。", v={"sci": "Zosterops simplex とする扱いもある"})
M("hiyodori", "passeriformes", "ヒヨドリ", "Hypsipetes amaurotis", "日本ではどこにでもいるが、分布の中心は日本周辺に限られる。")
M("mukudori", "passeriformes", "ムクドリ", "Spodiopsar cineraceus", "夕方に大群で街路樹にねぐらをとる。")

# 爬虫類
M("nihonkanahebi", "squamata", "ニホンカナヘビ", "Takydromus tachydromoides", "日本固有種。尾が体の2倍以上長い。")
M("komodo", "squamata", "コモドオオトカゲ", "Varanus komodoensis", "最大のトカゲ。下あごに毒腺をもつ。", jaStatus="common")
M("iguana", "squamata", "グリーンイグアナ", "Iguana iguana", "中南米の樹上にすむ草食のトカゲ。", jaStatus="common")
M("kingcobra", "serpentes", "キングコブラ", "Ophiophagus hannah", "世界最長の毒ヘビ。おもにほかのヘビを食べる。", v={"sci": "近年4種に分ける提案がある"}, jaStatus="common")
M("zougame", "testudines", "ガラパゴスゾウガメ", "Chelonoidis niger", "100年以上生きる個体もいる。島ごとに甲羅の形が違う。", v={"sci": "島ごとに別種とする扱いがある"}, jaStatus="common")
C("crocodylia", "archosauria", "ワニ目", "Crocodylia", "目", "ワニ・アリゲーター・ガビアル。")
move("crocodylia", "iriewani")
M("alligator", "crocodylia", "アメリカアリゲーター", "Alligator mississippiensis", "卵の温度で性別が決まる。", ["ミシシッピワニ"], jaStatus="common")

# 魚類（軟骨魚）
M("yoshikirizame", "selachii", "ヨシキリザメ", "Prionace glauca", "外洋を回遊する細長いサメ。ふかひれの主な原料。")
M("megamouth", "selachii", "メガマウスザメ", "Megachasma pelagios", "1976年に初めて見つかった深海の大型ザメ。プランクトンを食べる。")
M("nokogirizame", "selachii", "ノコギリザメ", "Pristiophorus japonicus", "のこぎり状の吻をもつサメ。エイの仲間のノコギリエイとは別。")
M("hoshizame", "selachii", "ホシザメ", "Mustelus manazo", "体に白い点が並ぶ。かまぼこの原料にされる。")
# 魚類（条鰭類）
C("anguilliformes", "teleostei", "ウナギ目", "Anguilliformes", "目", "ウナギ・アナゴ・ウツボ・ハモ。幼生はレプトケファルス。")
move("anguilliformes", "nihonunagi")
M("utsubo", "anguilliformes", "ウツボ", "Gymnothorax kidako", "喉の奥にもう一つのあご（咽頭顎）があり、獲物を引き込む。")
M("maanago", "anguilliformes", "マアナゴ", "Conger myriaster", "体側に白い点が並ぶ。天ぷらや寿司にされる。", ["アナゴ"])
M("hamo", "anguilliformes", "ハモ", "Muraenesox cinereus", "小骨が多く、「骨切り」してから料理する。")
C("cypriniformes", "ostariophysi", "コイ目", "Cypriniformes", "目", "コイ・フナ・ドジョウなど。あごに歯がなく、喉の奥の咽頭歯で噛む。")
move("cypriniformes", "koi", "oikawa", "ugui", "zebrafish")
M("dojou", "cypriniformes", "ドジョウ", "Misgurnus anguillicaudatus", "腸で空気呼吸ができる。", v={"sci": "日本の在来ドジョウは複数の系統を含み、学名は見直し中"})
C("salmoniformes", "euteleostei", "サケ目", "Salmoniformes", "目", "サケ・マス・イトウ。背びれの後ろに脂びれがある。")
C("osmeriformes", "euteleostei", "キュウリウオ目", "Osmeriformes", "目", "アユ・ワカサギ・シシャモなど。")
move("salmoniformes", "sake")
move("osmeriformes", "ayu")
M("nijimasu", "salmoniformes", "ニジマス", "Oncorhynchus mykiss", "北米原産。海に下るものはスチールヘッドと呼ばれる。")
M("sakuramasu", "salmoniformes", "サクラマス", "Oncorhynchus masou", "川に残って一生を過ごすものがヤマメ。", ["ヤマメ"])
M("itou", "salmoniformes", "イトウ", "Parahucho perryi", "日本最大の淡水魚。北海道にすむ。")
M("wakasagi", "osmeriformes", "ワカサギ", "Hypomesus nipponensis", "冬に凍った湖での穴釣りで知られる。")
M("shishamo", "osmeriformes", "シシャモ", "Spirinchus lanceolatus", "北海道の太平洋岸だけにすむ。店で売られる多くは別種のカラフトシシャモ。")
M("kinmedai", "euteleostei", "キンメダイ", "Beryx splendens", "深海にすむ赤い魚。目が大きく金色に光る。")
M("matoudai", "euteleostei", "マトウダイ", "Zeus faber", "体の中央に的のような黒い斑点がある。")
M("ryuuguunotsukai", "euteleostei", "リュウグウノツカイ", "Regalecus russellii", "全長数mになる細長い深海魚。人魚伝説のもとになったともいわれる。")
C("scombriformes", "percomorpha", "サバ目", "Scombriformes", "目", "サバ・マグロ・タチウオなど。")
move("scombriformes", "scombridae")
M("tachiuo", "scombriformes", "タチウオ", "Trichiurus japonicus", "銀色の帯のような体で、頭を上にして立ち泳ぎする。")
M("tobiuo", "beloniformes", "トビウオ", "Cheilopogon agoo", "大きな胸びれを広げて海面上を滑空する。", ["アゴ"])
C("carangiformes", "percomorpha", "アジ目", "Carangiformes", "目", "アジ・ブリと、ヒラメ・カレイ。カレイ類はアジの仲間から生まれた。")
move("carangiformes", "hirame")
M("maaji", "carangiformes", "マアジ", "Trachurus japonicus", "体の側面に「ぜいご」と呼ばれる硬い鱗が並ぶ。", ["アジ"])
M("buri", "carangiformes", "ブリ", "Seriola quinqueradiata", "成長につれて呼び名が変わる出世魚。", ["ハマチ", "イナダ", "ワラサ"])
M("makogarei", "carangiformes", "マコガレイ", "Pseudopleuronectes yokohamae", "カレイは目が体の右側に寄る（ヒラメは左）。", ["カレイ"])
C("perciformes", "percomorpha", "ペルカ目", "Perciformes", "目", "カサゴ・オコゼ・ホッケ・トゲウオなど。スズキはこの目ではない。",
  v={"ja": "日本産魚類全種目録の表記。従来のスズキ目とは範囲が違う"})
M("kasago", "perciformes", "カサゴ", "Sebastiscus marmoratus", "岩礁にすみ、卵ではなく仔魚を産む。")
M("niokoze", "perciformes", "オニオコゼ", "Inimicus japonicus", "背びれの棘に毒がある。高級な食用魚。", ["オコゼ"])
M("minokasago", "perciformes", "ミノカサゴ", "Pterois lunulata", "長いひれを広げて泳ぐ。ひれの棘に毒がある。")
M("hokke", "perciformes", "ホッケ", "Pleurogrammus azonus", "干物でよく食べられる。アイナメの仲間。")
M("hatahata", "perciformes", "ハタハタ", "Arctoscopus japonicus", "冬の雷の頃に秋田の浜へ産卵に押し寄せる。秋田県の県魚。")
M("houbou", "perciformes", "ホウボウ", "Chelidonichthys spinosus", "胸びれの一部が脚のようになり、海底を歩く。")
M("nihonitoyo", "perciformes", "ニホンイトヨ", "Gasterosteus nipponicus", "雄が水草で巣を作り卵を守る。2014年に別種として記載された。", ["イトヨ"])
M("suzuki", "percomorpha", "スズキ", "Lateolabrax japonicus", "成長につれて呼び名が変わる出世魚。日本産魚類全種目録ではホタルジャコ目に置かれる。", ["セイゴ", "フッコ"])
C("acanthuriformes", "percomorpha", "ニザダイ目", "Acanthuriformes", "目", "ニザダイ・チョウチョウウオ・タイなどを含む。",
  v={"placement": "目の範囲は分類体系によって大きく異なる（日本産魚類全種目録に従う）"})
move("acanthuriformes", "madai")
M("kurodai", "acanthuriformes", "クロダイ", "Acanthopagrus schlegelii", "雄から雌に性転換する。", ["チヌ"])
M("nanyouhagi", "acanthuriformes", "ナンヨウハギ", "Paracanthurus hepatus", "鮮やかな青い体。尾の付け根に鋭い骨質板がある。")
C("centrarchiformes", "percomorpha", "サンフィッシュ目", "Centrarchiformes", "目", "メジナ・イシダイ・ブラックバスなど。")
M("ishidai", "centrarchiformes", "イシダイ", "Oplegnathus fasciatus", "くちばし状の歯でウニや貝をかみ砕く。若魚は黒い横縞が目立つ。")
M("mejina", "centrarchiformes", "メジナ", "Girella punctata", "磯釣りで人気の魚。", ["グレ"])
C("gobiiformes", "percomorpha", "ハゼ目", "Gobiiformes", "目", "ハゼの仲間。腹びれが吸盤状になるものが多い。")
move("gobiiformes", "mahaze")
M("mutsugorou", "gobiiformes", "ムツゴロウ", "Boleophthalmus pectinirostris", "干潟の泥の上を胸びれで這い、皮膚でも呼吸する。")
M("kiankou", "percomorpha", "キアンコウ", "Lophius litulon", "頭の上の竿のような棘の先で獲物をおびき寄せる。", ["アンコウ"])

# 鋏角・多足
M("onigumo", "araneae", "オニグモ", "Araneus ventricosus", "夕方に大きな円網を張り、朝にたたむ。")
M("koganegumo", "araneae", "コガネグモ", "Argiope amoena", "腹部に黄色と黒の縞がある。網にX字の白い帯をつける。")
M("kabakikomachigumo", "araneae", "カバキコマチグモ", "Cheiracanthium japonicum", "ススキの葉を巻いた巣にすむ。日本の在来のクモで毒が強い部類。")
C("scorpiones", "euchelicerata", "サソリ目", "Scorpiones", "目", "尾の先に毒針をもつ。紫外線を当てると体が光る。")
move("scorpiones", "yaeyamasasori")
M("daiousasori", "scorpiones", "ダイオウサソリ", "Pandinus imperator", "西アフリカの大型サソリ。毒は弱い。", jaStatus="common")
M("hizendani", "euchelicerata", "ヒゼンダニ", "Sarcoptes scabiei", "人の皮膚にトンネルを掘ってすみ、疥癬を起こす。")
M("konahyouhidani", "euchelicerata", "コナヒョウヒダニ", "Dermatophagoides farinae", "家のほこりにすむチリダニ。アレルギーの原因になる。")
M("gohontogezatoumushi", "euchelicerata", "ゴホントゲザトウムシ", "Himalphalangium spinulatum", "ザトウムシは体の前後がくびれず、とても長い脚をもつ。クモとは別の目。", v={"ja": "和名と学名の対応を要確認"})
M("oogeji", "chilopoda", "オオゲジ", "Thereuopoda clunifera", "日本最大のゲジ。洞窟や崖にすむ。")

# 甲殻類
C("dendrobranchiata", "decapoda", "根鰓亜目", "Dendrobranchiata", "亜目", "クルマエビ・サクラエビなど。卵を抱かずに水中に放つ。")
C("caridea", "decapoda", "コエビ下目", "Caridea", "下目", "テナガエビ・ヌマエビ・タラバエビなど。雌が卵を腹に抱く。")
C("astacidea", "decapoda", "ザリガニ下目", "Astacidea", "下目", "ザリガニとロブスター。大きなはさみをもつ。")
C("achelata", "decapoda", "イセエビ下目", "Achelata", "下目", "イセエビとセミエビ。はさみがない。")
move("dendrobranchiata", "kurumaebi")
move("astacidea", "americazarigani")
move("achelata", "iseebi")
M("ushiebi", "dendrobranchiata", "ウシエビ", "Penaeus monodon", "ブラックタイガーの名で輸入される養殖エビ。", ["ブラックタイガー"])
M("sakuraebi", "dendrobranchiata", "サクラエビ", "Lucensosergia lucens", "体に多数の発光器がある。漁は駿河湾などに限られる。", ["Sergia lucens"])
M("tenagaebi", "caridea", "テナガエビ", "Macrobrachium nipponense", "雄の第2脚が体より長くなる。")
M("yamatonumaebi", "caridea", "ヤマトヌマエビ", "Caridina multidentata", "水槽のコケとりに使われる。幼生は海で育つ。")
M("hokkokuakaebi", "caridea", "ホッコクアカエビ", "Pandalus eous", "甘エビの名で売られる。雄として成熟したあと雌に性転換する。", ["アマエビ"])
M("nihonzarigani", "astacidea", "ニホンザリガニ", "Cambaroides japonicus", "北海道と北東北の冷たい水にすむ在来のザリガニ。")
M("lobster", "astacidea", "アメリカンロブスター", "Homarus americanus", "北米大西洋岸の大型のエビ。", ["ロブスター"], jaStatus="common")
M("semiebi", "achelata", "セミエビ", "Scyllarides squammosus", "平たい触角をもち、セミのような姿をしている。")
M("hakusenshiomaneki", "brachyura", "ハクセンシオマネキ", "Austruca lactea", "雄は片方の大きなはさみを振って雌を呼ぶ。かつては Uca 属に置かれた。", ["シオマネキ"])
M("sunagani", "brachyura", "スナガニ", "Ocypode stimpsoni", "砂浜に穴を掘ってすみ、素早く走る。")
M("himehamatobimushi", "malacostraca", "タイヘイヨウヒメハマトビムシ", "Platorchestia pacifica", "砂浜の打ち上げ海藻の下にいて、よく跳ねる。ヨコエビの仲間。", ["ヒメハマトビムシ"])
M("isazaami", "malacostraca", "イサザアミ", "Neomysis awatschensis", "汽水域で群れる小さなアミ。佃煮にされる。")
C("thecostraca", "multicrustacea", "鞘甲類", "Thecostraca", "クレード", "フジツボやカメノテ。幼生は泳ぐが、成体は岩などに固着する。")
move("thecostraca", "kamenote")
M("akafujitsubo", "thecostraca", "アカフジツボ", "Megabalanus rosa", "赤い殻の大型のフジツボ。食用にもされる。")
M("kurofujitsubo", "thecostraca", "クロフジツボ", "Tetraclita japonica", "岩礁の潮間帯の上の方にすむ。")
M("sakejirami", "multicrustacea", "サケジラミ", "Lepeophtheirus salmonis", "サケ類の体表に寄生するカイアシ類。養殖で被害を出す。")
M("chou", "oligostraca", "チョウ", "Argulus japonicus", "コイや金魚の体表に寄生する鰓尾類。昆虫のチョウとは無関係。")

# 昆虫
M("yamatoishinomi", "insecta", "ヤマトイシノミ", "Pedetontus nipponicus", "翅をもたない原始的な昆虫。腹を使って跳ねる。")
M("ooyamakawagera", "polyneoptera", "オオヤマカワゲラ", "Oyamia lugubris", "幼虫は川の石の下で暮らす。きれいな水の指標になる。")
M("oohasamimushi", "polyneoptera", "オオハサミムシ", "Labidura riparia", "尾のはさみで獲物をとらえる。雌は卵と幼虫を守る。", ["ハサミムシ"])
M("garoamushi", "polyneoptera", "ガロアムシ", "Galloisiana nipponensis", "翅のない原始的な昆虫。1915年に日本で発見され、ガロアムシ目のもとになった。")
M("kamadouma", "orthoptera", "カマドウマ", "Diestrammena apicalis", "翅がなく、長い後ろ脚で大きく跳ねる。", v={"sci": "GBIF は Atachycines apicalis"})
M("minamikiiroazamiuma", "paraneoptera", "ミナミキイロアザミウマ", "Thrips palmi", "体長1 mmほどの細長い昆虫。翅は房のような毛でできている。野菜の害虫。")
C("cicadidae", "hemiptera", "セミ科", "Cicadidae", "科", "雄が腹の発音器で鳴く。幼虫は地中で何年も過ごす。")
move("cicadidae", "aburazemi", "minminzemi", "tsukutsukuboushi")
M("kumazemi", "cicadidae", "クマゼミ", "Cryptotympana facialis", "西日本に多い大型のセミ。シャシャシャと鳴く。")
M("higurashi", "cicadidae", "ヒグラシ", "Tanna japonensis", "夕方や明け方にカナカナと鳴く。")
M("tokojirami", "hemiptera", "トコジラミ", "Cimex lectularius", "夜に人の血を吸うカメムシの仲間。シラミとは別の目。", ["ナンキンムシ"])
M("hebitombo", "holometabola", "ヘビトンボ", "Protohermes grandis", "幼虫は川にすむ「孫太郎虫」。完全変態をする。")
M("yamatoshiriage", "mecopterida", "ヤマトシリアゲ", "Panorpa japonica", "雄は腹の先がサソリのように反り上がる。")
M("higenagakawatobikera", "mecopterida", "ヒゲナガカワトビケラ", "Stenopsyche marmorata", "幼虫は川の石の間に網を張って餌を集める。トビケラはチョウ目に最も近い。")
C("lucanidae", "coleoptera", "クワガタムシ科", "Lucanidae", "科", "雄の大あごが大きく発達する甲虫。")
C("scarabaeidae", "coleoptera", "コガネムシ科", "Scarabaeidae", "科", "カブトムシ・カナブン・コガネムシなど。")
move("lucanidae", "nokogirikuwagata")
move("scarabaeidae", "kabutomushi")
M("miyamakuwagata", "lucanidae", "ミヤマクワガタ", "Lucanus maculifemoratus", "雄の頭に耳のような張り出しがある。涼しい山地に多い。")
M("ookuwagata", "lucanidae", "オオクワガタ", "Dorcus hopei", "成虫で何年も生きる。")
M("herakuresu", "scarabaeidae", "ヘラクレスオオカブト", "Dynastes hercules", "中南米にすむ世界最長のカブトムシ。", jaStatus="common")
M("kanabun", "scarabaeidae", "カナブン", "Pseudotorynorrhina japonica", "樹液に集まる。翅を閉じたまま飛ぶ。")
M("namigengorou", "coleoptera", "ゲンゴロウ", "Cybister chinensis", "後ろ脚で泳ぐ水生の甲虫。数が減り絶滅危惧種。", ["ナミゲンゴロウ"])
M("gomadarakamikiri", "coleoptera", "ゴマダラカミキリ", "Anoplophora malasiaca", "幼虫はミカンなどの幹を食べる。触角が体より長い。", ["カミキリムシ"])
C("papilionidae", "lepidoptera", "アゲハチョウ科", "Papilionidae", "科", "大型のチョウ。幼虫は臭角をもつ。")
move("papilionidae", "ageha", "aosujiageha")
M("kiageha", "papilionidae", "キアゲハ", "Papilio machaon", "幼虫はニンジンやパセリなどセリ科を食べる。")
M("monkichou", "lepidoptera", "モンキチョウ", "Colias erate", "黄色い翅のチョウ。雌には白いものもいる。")
M("oominoga", "lepidoptera", "オオミノガ", "Eumeta variegatus", "幼虫は枝や葉で蓑を作る（ミノムシ）。雌は翅も脚もない。", ["ミノムシ"])
C("culicidae", "diptera", "カ科", "Culicidae", "科", "蚊。雌だけが血を吸う。")
move("culicidae", "hitosujishimaka", "akaieka")
M("shinahamadaraka", "culicidae", "シナハマダラカ", "Anopheles sinensis", "ハマダラカの仲間はマラリアを媒介する。止まるとき体を斜めに立てる。", ["ハマダラカ"])
M("ushiabu", "diptera", "ウシアブ", "Tabanus trigonus", "雌は牛や人の血を吸う。")
C("formicidae", "hymenoptera", "アリ科", "Formicidae", "科", "アリ。ハチの中から生まれた社会性昆虫。")
move("formicidae", "kurooari", "argentinaari")
M("kuroyamaari", "formicidae", "クロヤマアリ", "Formica japonica", "日本で最もよく見られるアリの一つ。")

# 軟体
M("akoyagai", "bivalvia", "アコヤガイ", "Pinctada fucata", "真珠の養殖に使われる。")
M("ooshakogai", "bivalvia", "オオシャコガイ", "Tridacna gigas", "最大の二枚貝。殻の長さは1 mを超える。")
M("hadakakamegai", "heterobranchia", "ハダカカメガイ", "Clione limacina", "殻のない浮遊性の巻貝。クリオネの名で知られる。", ["クリオネ"], v={"sci": "北太平洋のものを別種・別亜種とする見解がある", "ja": "C. limacina の和名は GBIF・Wikidata・iNat ではダイオウハダカカメガイ。日本のハダカカメガイを C. okhotensis とする見解がある"})
M("africamaimai", "heterobranchia", "アフリカマイマイ", "Lissachatina fulica", "世界最大級の陸貝。南西諸島などで外来種。広東住血線虫を運ぶ。", ["Achatina fulica"])

# ---------------- 知名度の段階（tier、2026-10-23 作者了承） ----------------
# tier 1 = よく知られている（省略時）、tier 2 = 図鑑レベル。今日の動物は tier 2 を少しだけ出にくくする。
# 推測・補完は全種で使う。判断は手作業（学名の音写しかない種は tier 2）。
TIER2 = set("""
kuroisokaimen urikurage senmohirahamushi usuedamidoriishi umeboshiisogin nanahoshikudoa xenoturbella praesagittifera
nipponumishida nihonkumohitode misakigiboshi wakareotamaboya isoyamushi erahikimushi echinoderes nanaloricus
matsunozaisenchu chordodes euperipatoides umigumo futatogechimadani yakeyasude mizutobimushi gnathostomula limnognathia
shiomizutsubowamushi corynosoma nihonkairettojouchu lepidodermella dicyema intoshia yamatokawagokai satsumahaorimushi
siebold_mimizu midorihimomushi midorishamisengai himehoukimushi oomarikokemushi barentsia symbion hossugai kawakaimen
fusenkurage obikurage sangoisoginchaku kikumeishi murasakihanaginchaku umisaboten asagaokurage katsuononkanmuri torinoashi
mahitode okinotezurumozuru takonomakura gangaze kuronamako himegiboshimushi katayureiboya azumamogura aburakoumori
namihadani kishayasude ajiakabutoebi seiyoushimi monkagerou nanafushimodoki hitojirami nekonomi kasemimizu yakadotsunogai
takobune ootanishi anboina aoumiushi hirejako sujihoshimushi umikemushi iwamushi keyarimushi shimamimizu tsunohiramushi
oomisujikougaibiru nihonjuketsukyuchu kankyuchu takoujouchu inushijouchu nekobusenchu senmouchu onikumamushi adineta
kubinagakoutouchu misakihimomushi kamehoozukichouchin fusakokemushi mokuyokukaimen tatejimaisoginchaku hatagoisoginchaku
kusabiraishi hiranousango aosango momoirosango bizenkurage ginkakurage hanagasakurage aohitode momijigai yatsudehitode
akauni kitamurasakiuni rappauni paipuuni nisekuronamako shikakunamako shibireei narutobiei konoshiro oikawa ugui zebrafish
kitanomedaka datsu ushimanbou schlegelaogaeru hakonesanshouo shirikenimori akagezaru akanezumi kitanakiusagi koubemogura
kubiwaookoumori yubinagakoumori nihonanaguma africasuigyu erabuumihebi amimenishikihebi yamadori magan kohakuchou
nagakoganegumo oohimegumo aozumukade yanbarutosakayasude hamadangomushi murasakiokayadokari hanasakigani hagurotombo
mukashitombo haraburokamakiri ieshiroari kusagikamemushi seguroashinagabachi argentinaari yamamayu umabiru haikyuchu
mukoujouchu yuukoujouchu inukaichu hoshizame nokogirizame matoudai houbou nihonitoyo kabakikomachigumo hizendani
konahyouhidani gohontogezatoumushi oogeji ushiebi yamatonumaebi semiebi hakusenshiomaneki sunagani himehamatobimushi
isazaami akafujitsubo kurofujitsubo sakejirami chou yamatoishinomi ooyamakawagera oohasamimushi garoamushi
minamikiiroazamiuma hebitombo yamatoshiriage higenagakawatobikera shinahamadaraka ushiabu kuroyamaari africamaimai
""".split())
for _s in species:
    if _s["id"] in TIER2 or _s.get("jaStatus") == "provisional":
        _s["tier"] = 2
assert TIER2 <= {_s["id"] for _s in species}, TIER2 - {_s["id"] for _s in species}

# ---------------- 知名度を4段階に（2026-10-23 作者「もうちょっと細かく」） ----------------
# 1 = だれでも知っている／2 = よく知られている（水族館・動物園・食卓の定番など）
# 3 = 図鑑レベル／4 = 専門的（和名が学名表記・微小動物・寄生虫の多くなど）
# 既定は上の TIER2 に入っていれば 3、それ以外は 2。下の2つのリストで 1 と 4 に上書きする。
TIER1 = set("""
hito inu ieneko ushi uma hitsuji yagi inoshishi nihonzaru chimpanzee gorilla orangutan africazou kirin lion tora cheetah
panda lesserpanda higuma hokkyokuguma tsukinowaguma tanuki akagitsune ookami koala akakangaroo kamonohashi kaba shirosai
savannashimauma hitokobu shironagasu makkoukujira shachi handouiruka zatoukujira rakko gomafuazarashi nihonjika dobunezumi
hatsukanezumi nihonrisu goldenhamster guineapig anausagi capybara
suzume hashibutogarasu hashibosogarasu kawarabato tsubame dachou kouteipenguin sekishokuyakei magamo uguisu mejiro fukurou
tancho toki hayabusa sekiseiinko kujaku benifuramingo kawasemi oohakuchou
iriewani alligator akaumigame aoumigame aodaisho habu nihonmamushi komodo zougame kingcobra akamimigame kusagame nihonyamori
nihontokage iguana nihonamagaeru tonosamagaeru ushigaeru osanshouo akaharaimori axolotl
jinbeizame hohojirozame kuromaguro katsuo sake maiwashi sanma madai koi minamimedaka nihonunagi tatsunootoshigo manbou
torafugu hirame kakurekumanomi ayu masaba maaji buri katakuchiiwashi nanyoumanta utsubo harisenbon mikadochozame namazu
dojou nijimasu shishamo kiankou coelacanth
kabutomushi nokogirikuwagata miyamakuwagata ookuwagata herakuresu nanahoshitentou genjibotaru monshirocho ageha kaiko
akiakane oniyanma shiokaratombo tonosamabatta enmakorogi suzumushi ookamakiri aburazemi minminzemi kumazemi higurashi
tsukutsukuboushi seiyomitsubachi oosuzumebachi kurooari kurogokiburi iebae hitosujishimaka amenbo
madako surumeika hotaruika daiouika oumugai sazae hamaguri asari magaki hotategai mizukurage katsuonoeboshi echizenkurage
murasakiuni bafununi manamako onihitode jorougumo americazarigani zuwaigani tarabagani iseebi kurumaebi okadangomushi
kegani takaashigani namekuji misujimaimai kabutogani mijinko sawagani
""".split())
TIER4 = set("""
nanahoshikudoa praesagittifera isoyamushi erahikimushi shiomizutsubowamushi umigumo mizutobimushi midorihimomushi
himehoukimushi barentsia kuroisokaimen senmohirahamushi wakareotamaboya misakigiboshi himegiboshimushi nihonkumohitode
kankyuchu kubinagakoutouchu misakihimomushi kamehoozukichouchin keyarimushi tsunohiramushi kasemimizu sakejirami chou
isazaami himehamatobimushi gohontogezatoumushi minamikiiroazamiuma ooyamakawagera higenagakawatobikera yamatoshiriage
yamatoishinomi asagaokurage haikyuchu umabiru yanbarutosakayasude onikumamushi
""".split())
_ids = {_s["id"] for _s in species}
assert TIER1 <= _ids and TIER4 <= _ids, (TIER1 - _ids, TIER4 - _ids)
assert not (TIER1 & TIER4)
for _s in species:
    _t = 3 if _s.get("tier") == 2 else 2
    if _s["id"] in TIER1: _t = 1
    if _s["id"] in TIER4 or _s.get("jaStatus") == "provisional": _t = 4
    _s["tier"] = _t

# 出題の重み（ページ側が読む）。作者の A/B/C 回答が出たら bucketWeight と tierWeights をここで変える。
META["selection"]["tierWeights"] = {"1": 1, "2": 0.9, "3": 0.8, "4": 0.7}
META["selection"]["bucketWeight"] = "sqrt"  # 2026-10-23 作者案B

# 和名の無い種は入れない（2026-10-23 作者）。種の和名が無い仮名13種を外し、種が無くなった節目も外す。
# 動吻・腹毛・二胚は和名のある種で戻した（CoL 経由の BISMaL と原記載論文、check/bismal_col/summary.md）。
# 作者「コガネトゲカワでいいかも」（2026-10-23）。和名は BISMaL（CoL 3LR 経由）。原記載 Adrianov, Murakami & Shirayama (2002) Species Diversity 7: 47–66
edit("echinoderes", ja="コガネトゲカワ", sci="Echinoderes aureus", jaStatus="standard", aliases=["トゲカワ"],
     fact="和歌山県の田辺湾から2002年に新種として記載されたトゲカワ。動吻動物は英語で mud dragon（マッドドラゴン）と呼ばれる。")
_find("echinoderes").pop("verify", None)
_find("echinoderes")["gbif"] = 2501480
edit("dicyema", ja="ヤマトニハイチュウ", jaStatus="standard",
     verify={"ja": "原記載（Furuya, Tsuneki & Koshida 1992, Zool. Sci. 9）のローマ字表記 Yamato-nihaityu から"})
S("ikaritogeobimushi", "gastrotricha", "イカリトゲオビムシ", "Tetranchyroderma dendricum",
  "海岸の砂粒のすき間にすむ腹毛動物。1937年に日本から記載された。", ["イタチムシ"])
_find("ikaritogeobimushi")["tier"] = 4
NO_JA = set("""xenoturbella nanaloricus chordodes euperipatoides gnathostomula limnognathia
corynosoma lepidodermella intoshia symbion adineta""".split())
species[:] = [s for s in species if s["id"] not in NO_JA]
while True:
    _used = {s["parent"] for s in species} | {c["parent"] for c in clades}
    _empty = [c for c in clades if c["id"] not in _used]
    if not _empty: break
    _gone = {c["id"] for c in _empty}
    clades[:] = [c for c in clades if c["id"] not in _gone]

# 標準和名リストとの照合（2026-10-23、tools/std_check.py、結果 check/std/）。
# 表示する和名を学会の標準和名に合わせ、よく使われる呼び名は別名に残す。
edit("nihonanaguma", ja="アナグマ", aliases=["ニホンアナグマ"])           # 世界哺乳類標準和名リスト2021: Meles anakuma = アナグマ
edit("ookami", ja="オオカミ", aliases=["タイリクオオカミ"])               # 同: Canis lupus = オオカミ
edit("guineapig", ja="テンジクネズミ", aliases=["モルモット"],            # 同: Cavia porcellus = テンジクネズミ
     fact="南米で家畜化されたネズミの仲間。ペットや実験動物のモルモットはこの種。")
edit("suppon", ja="チュウゴクスッポン", aliases=[],                       # 日本産爬虫両生類標準和名リスト: P. sinensis = チュウゴクスッポン
     verify={"sci": "日本在来の個体群は別種ニホンスッポン P. japonicus とされる（標準和名リスト）。GBIF 未収録のため P. sinensis で掲載"})
edit("africazou", aliases=["サバンナゾウ"])                               # 同リストの括弧書きの別名

META["japaneseNameSources"] = ["本村浩之（2026）日本産魚類全種目録 Online ver. 42（魚類）",
    "日本鳥学会 日本鳥類目録改訂第8版 和名・学名リスト（2023-09-30公開版）（鳥類）",
    "川田ほか（2021）世界哺乳類標準和名リスト2021年度版. https://www.mammalogy.jp/list/index.html（哺乳類）",
    "日本爬虫両棲類学会（2026）日本産爬虫両生類標準和名リスト（2026年7月2日版）. https://herpetology.jp/wamei/ (2026年10月23日アクセス)（爬虫両生類）",
    "GBIF・Wikidata・iNaturalist の日本語名（2つ以上の一致で採用、上のリストに無い種）"]
META["status"] = ("試作版。魚類・鳥類・哺乳類・爬虫両生類の和名は各学会等の標準和名リストと照合済み（2026-10-23）。"
    "昆虫や海の無脊椎動物は標準和名リストとの突き合わせが未実施。種の和名が無い動物は収録しない。verify が付いた項目は要確認。")

edit("namekujiuo", ja="ヒガシナメクジウオ", aliases=["ナメクジウオ"])   # BISMaL(CoL)・Wikidata・iNat。ナメクジウオは日本での旧称
edit("hadakakamegai", sci="Clione elegantissima", verify=None)          # 北太平洋のハダカカメガイは C. limacina（ダイオウハダカカメガイ）と別種（Yamazaki & Kuwahara 2017）
_find("hadakakamegai").pop("verify", None)

# 和名の別名を併記（2026-10-23 作者「キヒトデとマヒトデみたいに併記」）。BISMaL(CoL)・CoL にある同じ種の別の和名。check/bismal_col/summary.md
_find("akoyagai")["aliases"] += ["ベニコチョウガイ"]   # BISMaL・CoL・GBIF は P. fucata をベニコチョウガイ、日本のアコヤガイは亜種 P. f. martensii とする扱い
_find("isazaami")["aliases"] += ["クロイサザアミ"]
_find("manamako")["aliases"] += ["アカナマコ"]           # 体色の型の名前としても使われる
_find("sangoisoginchaku")["aliases"] += ["ウスカワイソギンチャク", "タマイタダキイソギンチャク"]

# 旧学名（2026-10-23 作者「主な旧名だけ」）。同じ種で名前だけ変わったものに限る。別種と取り違えていた名前は入れない。
# 候補と除外の理由は check/synonyms/candidates.md。表示と入力はゲーム側。
SCI_SYN = {
    "mikadochozame": ["Acipenser medirostris", "Acipenser mikadoi"],
    "kouika": ["Sepia esculenta"],
    "katakuchiiwashi": ["Engraulis japonicus"],
    "genjibotaru": ["Luciola cruciata"],
    "jorougumo": ["Nephila clavata"],
    "akakangaroo": ["Macropus rufus"],
    "nipponumishida": ["Oxycomanthus japonicus"],
    "ushigaeru": ["Lithobates catesbeianus", "Rana catesbeiana"],
    "ootaka": ["Accipiter gentilis"],
    "oikawa": ["Zacco platypus"],
    "ootanishi": ["Heterogen japonica"],
    "hizaragai": ["Acanthopleura japonica"],
    "kamadouma": ["Atachycines apicalis"],
    "siebold_mimizu": ["Perichaeta sieboldi"],
    "midorihimomushi": ["Notospermus fuscoviridis"],
    "kubinagakoutouchu": ["Pomphorhynchus pagrosomi"],
    "mareebaku": ["Acrocodia indica"],
}
for _id, _ns in SCI_SYN.items():
    _find(_id)["sciSynonyms"] = _ns
_scis = {s["sci"] for s in species}
_names = {}
for s in species:
    for n in [s["ja"]] + s["aliases"]:
        _names.setdefault(n, set()).add(s["id"])
    for n in s.get("sciSynonyms", []):
        assert n not in _scis, ("旧学名がほかの種の学名と同じ", s["id"], n)
# 足した別名がほかの種の和名・別名と重ならないか
for _n in ["ベニコチョウガイ", "クロイサザアミ", "アカナマコ", "ウスカワイソギンチャク", "タマイタダキイソギンチャク", "マヒトデ"]:
    assert len(_names[_n]) == 1, ("別名の重複", _n, _names[_n])

# 2026-10-23 作者了承：出題の並びを入れ替えるため版を上げる（ページ担当の依頼）
META["datasetVersion"] = "0.3.2.1"  # 0.3.2.1（633種）=10/25〜（ネタバレ回避で版名を変更、0.3.1 は不使用）。文（fact/desc）だけの修正は版を上げずページ担当が各data*.jsonに直接差し替える。種・節目・tier・重みを変えるときだけ 0.3.3 以降に上げる

# ---------------- 作者が入れたい種（2026-10-23〜） ----------------
# 照合は check/picks/（学名 GBIF・CoL・WoRMS、和名 BISMaL(CoL)・GBIF・Wikidata・iNat）。
C("polycladida", "platyhelminthes", "多岐腸目", "Polycladida", "目",
  "海にすむ大型の渦虫類（ヒラムシ）。腸が体の中央から多数に枝分かれする。")
move("polycladida", "tsunohiramushi")
S("kaiyadorihiramushi", "polycladida", "カイヤドリヒラムシ", "Comoplana pusilla",
  "巻貝のイシダタミの殻の中にすむ小さなヒラムシ。")
S("usuhiramushi", "polycladida", "ウスヒラムシ", "Notocomplana humilis",
  "日本の磯で石の下によく見つかる、薄く平たいヒラムシ。")
S("isoawamochi", "heterobranchia", "イソアワモチ", "Peronia verruculata",
  "殻のない巻貝で、潮が引いた岩の上をはい回る。肺で空気を呼吸する。")
C("loliginidae", "decapodiformes", "ヤリイカ科", "Loliginidae", "科",
  "目が透明な膜（角膜）でおおわれた、沿岸にすむイカの仲間。")
move("loliginidae", "aoriika", "yariika", "kensakiika")
S("jindouika", "loliginidae", "ジンドウイカ", "Loliolus japonica",
  "内湾にすむ小型のヤリイカの仲間。胴の長さは10cmほど。")
for _id, _t in {"kaiyadorihiramushi": 4, "usuhiramushi": 4, "isoawamochi": 3, "jindouika": 3}.items():
    _find(_id)["tier"] = _t
# 作者「アワモチとジンドウイカ系は和名わかるやつ全部」。和名が2つ以上の情報源で確かめられた種だけ（check/picks2/）。
# センベイアワモチ・ゴマセンベイアワモチ・チゴイソアワモチは iNat だけで、学名との対応を確かめられず見送り。
# ボウズジンドウイカ・アジアボウズジンドウイカは iNat と全国いか加工業協同組合のイカ図鑑で確認。
C("onchidiidae", "heterobranchia", "アワモチ科", "Onchidiidae", "科",
  "殻のない巻貝の仲間。潮間帯の岩や干潟の泥の上で暮らし、肺で空気を呼吸する。")
move("onchidiidae", "isoawamochi")
S("doroawamochi", "onchidiidae", "ドロアワモチ", "Paromoionchis tumidus", "干潟の泥の上にすむアワモチの仲間。")
S("yabegawamochi", "onchidiidae", "ヤベガワモチ", "Onchidium reevesii", "有明海などの干潟にすむ大型のアワモチの仲間。")
S("himeawamochi", "onchidiidae", "ヒメアワモチ", "Onchidella kurodai", "磯にすむ小型のアワモチの仲間。")
C("loliolus", "loliginidae", "ジンドウイカ属", "Loliolus", "属", "内湾や沿岸にすむ小型のヤリイカ科のイカ。")
move("loliolus", "jindouika")
S("beika", "loliolus", "ベイカ", "Loliolus beka", "有明海などの内湾にすむ小型のイカ。")
S("himejindouika", "loliolus", "ヒメジンドウイカ", "Loliolus sumatrensis", "ジンドウイカに似た小型のイカ。")
S("bouzujindouika", "loliolus", "ボウズジンドウイカ", "Loliolus affinis", "腕が短い小型のイカ。")
S("asiabouzujindouika", "loliolus", "アジアボウズジンドウイカ", "Loliolus hardwickei", "ボウズジンドウイカによく似た小型のイカ。")
S("uijindouika", "loliolus", "ウイジンドウイカ", "Loliolus uyii", "小型のジンドウイカ属のイカ。")
for _id in ["doroawamochi", "yabegawamochi", "himeawamochi", "beika", "himejindouika", "bouzujindouika", "asiabouzujindouika", "uijindouika"]:
    _find(_id)["tier"] = 4
META["status"] += "説明文（一言説明）は出典を個別に確かめたものではなく、誤りを含む可能性がある。"

# ---------------- 鳥・昆虫・魚の目を埋める（2026-10-23 作者「一目に最低1〜2種」） ----------------
# 鳥は日本鳥類目録改訂第8版の目、魚は本村（2026）日本産魚類全種目録 ver. 42 の目、昆虫は日本産の目を基準に、欠けていた目へ1〜2種を足した。
# 名前は鳥=鳥類目録、魚=本村目録、それ以外=check/orders/ の照合。目の節目は2種以上になるときだけ作る（1種だけの目は上の節目に直接つける）。
# 見送り：ガー目（本村目録で和名が括弧付きの外来種のみ）、カカトアルキ目（種の和名が無い）。
O = S
# 鳥
C("strisores", "neoaves", "Strisores", "Strisores", "クレード", "ヨタカ類とアマツバメ・ハチドリ類のまとまり。")
O("yotaka", "strisores", "ヨタカ", "Caprimulgus jotaka", "夜に飛びながら虫を捕らえる。昼は枝の上で木の皮のような姿でじっとしている。")
O("amatsubame", "strisores", "アマツバメ", "Apus pacificus", "ほとんど地上に降りず、飛びながら暮らす。ツバメとは別の目。")
O("nogan", "neoaves", "ノガン", "Otis tarda", "草原にすむ大型の鳥。飛べる鳥の中では最も重い部類。")
C("cuculiformes", "neoaves", "カッコウ目", "Cuculiformes", "目", "カッコウ・ホトトギスなど。托卵をする種が多い。")
move("cuculiformes", "kakkou")
O("hototogisu", "cuculiformes", "ホトトギス", "Cuculus poliocephalus", "ウグイスの巣に托卵する。「特許許可局」と聞きなされる声で鳴く。")
C("columbimorphae", "neoaves", "Columbimorphae", "Columbimorphae", "クレード", "ハト類とサケイ類などのまとまり。")
move("columbimorphae", "columbidae")
O("sakei", "columbimorphae", "サケイ", "Syrrhaptes paradoxus", "中央アジアの乾燥地にすむ。日本にはまれに渡来する。")
C("gruiformes", "neoaves", "ツル目", "Gruiformes", "目", "ツル類とクイナ類など。")
move("gruiformes", "tancho")
O("ban", "gruiformes", "バン", "Gallinula chloropus", "赤い額をもつクイナの仲間。水辺の草むらで暮らす。")
C("mirandornithes", "neoaves", "Mirandornithes", "Mirandornithes", "クレード", "カイツブリ類とフラミンゴ類のまとまり。見た目は違うが分子系統で近縁とされる。")
move("mirandornithes", "benifuramingo")
O("kaitsuburi", "mirandornithes", "カイツブリ", "Tachybaptus ruficollis", "池や湖で潜って魚を捕らえる小型の水鳥。")
C("charadriiformes", "neoaves", "チドリ目", "Charadriiformes", "目", "チドリ・シギ・カモメ・ウミスズメなど。")
move("charadriiformes", "umineko")
O("kochidori", "charadriiformes", "コチドリ", "Charadrius dubius", "河原や埋め立て地の地面に卵を産む。目のまわりが黄色い。")
O("akaonettaichou", "neoaves", "アカオネッタイチョウ", "Phaethon rubricauda", "赤くて長い中央の尾羽をもつ海鳥。")
O("abi", "aequornithes", "アビ", "Gavia stellata", "冬に日本の沿岸に来る潜水の得意な水鳥。")
C("procellariiformes", "aequornithes", "ミズナギドリ目", "Procellariiformes", "目", "管状の鼻孔をもつ外洋性の海鳥。")
move("procellariiformes", "ahoudori")
O("oomizunagidori", "procellariiformes", "オオミズナギドリ", "Calonectris leucomelas", "日本近海の島で繁殖し、外洋で魚を捕らえる。")
C("suliformes", "aequornithes", "カツオドリ目", "Suliformes", "目", "カツオドリ・ウ・グンカンドリなど。")
O("kawau", "suliformes", "カワウ", "Phalacrocorax carbo", "潜って魚を捕らえる黒い水鳥。鵜飼いにはウミウが使われる。")
O("katsuodori", "suliformes", "カツオドリ", "Sula leucogaster", "空から海に飛び込んで魚を捕らえる。")
C("pelecaniformes", "aequornithes", "ペリカン目", "Pelecaniformes", "目", "ペリカン・サギ・トキなど。")
move("pelecaniformes", "toki", "aosagi")
O("yatsugashira", "afroaves", "ヤツガシラ", "Upupa epops", "扇のような冠羽をもつ。サイチョウに近い仲間。")
C("coraciiformes", "afroaves", "ブッポウソウ目", "Coraciiformes", "目", "カワセミ・ブッポウソウ・ハチクイなど。")
move("coraciiformes", "kawasemi")
O("buppousou", "coraciiformes", "ブッポウソウ", "Eurystomus orientalis", "青緑色の夏鳥。名前は別の鳥（コノハズク）の鳴き声から誤って付けられた。")
O("akagera", "afroaves", "アカゲラ", "Dendrocopos major", "木の幹をつついて穴をあけ、中の虫を食べるキツツキ。")
# 昆虫
C("neuropterida", "holometabola", "Neuropterida", "Neuropterida", "クレード", "アミメカゲロウ目・ヘビトンボ目・ラクダムシ目のまとまり。")
move("neuropterida", "usubakagerou", "hebitombo")
O("rakudamushi", "neuropterida", "ラクダムシ", "Inocellia japonica", "首のように長い前胸をもつ。幼虫は樹皮の下で他の虫を食べる。")
O("suzumebachinejirebane", "holometabola", "スズメバチネジレバネ", "Xenos moutoni", "スズメバチの腹部に寄生する。雌は一生ハチの体から出ない。")
O("iga", "lepidoptera", "イガ", "Tinea translucens", "幼虫が毛織物などを食べる小さなガ。")
O("shiroarimodoki", "polyneoptera", "シロアリモドキ", "Oligotoma saundersii", "前脚の先から糸を出し、絹のトンネルを作ってその中で暮らす。")
O("caudelljuzuhige", "polyneoptera", "コーデルジュズヒゲムシ", "Spiralizoros caudelli", "数珠のような触角をもつ小さな昆虫。朽ち木の中で集団で暮らす。",
  v={"ja": "和名は日本の研究発表（筑波大学）での使用例のみで確認"})
_find("caudelljuzuhige")["sciSynonyms"] = ["Zorotypus caudelli"]
# 棘皮（作者の指定）
O("bunbukuchagama", "echinoidea", "ブンブクチャガマ", "Schizaster lacunosus", "砂の中にもぐってすむ、心臓のような形のウニ。")
# 魚（名前・目は本村目録 ver. 42）
C("elopomorpha", "teleostei", "カライワシ上目", "Elopomorpha", "上目", "カライワシ・ソトイワシ・ソコギス・ウナギなど。幼生が平たく透明なレプトセファルスになる。")
move("elopomorpha", "anguilliformes")
O("karaiwashi", "elopomorpha", "カライワシ", "Elops hawaiensis", "沿岸や河口にすむ細長い魚。")
O("sotoiwashi", "elopomorpha", "ソトイワシ", "Albula argentea", "浅い砂底の海にすむ銀色の魚。")
O("sokogisu", "elopomorpha", "ソコギス", "Polyacanthonotus challengeri", "深海にすむ細長い魚。")
O("sekitoriiwashi", "otomorpha", "セキトリイワシ", "Rouleina squamilatera", "深海にすむ黒っぽい魚。")
O("nezumigisu", "ostariophysi", "ネズミギス", "Gonorynchus abbreviatus", "砂底にすむ細長い魚。コイやナマズと同じ骨鰾類。")
C("siluriformes", "ostariophysi", "ナマズ目", "Siluriformes", "目", "口のまわりにひげをもつ魚。")
move("siluriformes", "namazu")
O("gigi", "siluriformes", "ギギ", "Tachysurus nudiceps", "西日本の川にすむ。胸びれの棘をこすって「ギーギー」と音を出す。")
O("nigisu", "euteleostei", "ニギス", "Glossanodon semifasciatus", "やや深い海にすむ。干物などで食べられる。")
O("houraieso", "euteleostei", "ホウライエソ", "Chauliodus sloani", "長い牙をもつ深海魚。")
O("shachiburi", "euteleostei", "シャチブリ", "Ateleopus japonicus", "やわらかい体をもつ深海魚。")
C("aulopiformes", "euteleostei", "ヒメ目", "Aulopiformes", "目", "エソ類やミズウオなど。")
O("maeso", "aulopiformes", "マエソ", "Saurida macrolepis", "砂底にすむ。かまぼこの原料になる。")
O("mizuuo", "aulopiformes", "ミズウオ", "Alepisaurus ferox", "大きな背びれと鋭い歯をもつ深海魚。")
O("hadakaiwashi", "euteleostei", "ハダカイワシ", "Diaphus watasei", "体に発光器をもつ深海魚。")
C("lampriformes", "euteleostei", "アカマンボウ目", "Lampriformes", "目", "アカマンボウやリュウグウノツカイなど。")
move("lampriformes", "ryuuguunotsukai")
O("akamanbou", "lampriformes", "アカマンボウ", "Lampris megalopsis", "体の一部を温かく保つことができる魚。マンボウとは別の目。")
O("ginmedai", "euteleostei", "ギンメダイ", "Polymixia japonica", "あごの下に2本のひげをもつ。")
C("gadiformes", "euteleostei", "タラ目", "Gadiformes", "目", "タラ類やソコダラ類。冷たい海に多い。")
move("gadiformes", "madara")
O("suketoudara", "gadiformes", "スケトウダラ", "Gadus chalcogrammus", "卵巣がたらこや明太子になる。")
O("matsukasauo", "euteleostei", "マツカサウオ", "Monocentris japonica", "硬いうろこでおおわれ、あごの下に発光器をもつ。")
C("beryciformes", "euteleostei", "キンメダイ目", "Beryciformes", "目", "キンメダイ類やイットウダイ類。")
move("beryciformes", "kinmedai")
O("ittoudai", "beryciformes", "イットウダイ", "Sargocentron spinosissimum", "赤い体と大きな目をもつ。")
C("ophidiiformes", "percomorpha", "アシロ目", "Ophidiiformes", "目", "アシロ類やカクレウオ類。")
O("ashiro", "ophidiiformes", "アシロ", "Ophidion asiro", "砂底にすむ細長い魚。")
O("kakureuo", "ophidiiformes", "カクレウオ", "Encheliophis sagamianus", "ナマコの体の中に隠れてすむ。")
C("syngnathiformes", "percomorpha", "ヨウジウオ目", "Syngnathiformes", "目", "ヨウジウオ・タツノオトシゴ・ヘラヤガラなど。雄が卵を守る種が多い。")
move("syngnathiformes", "tatsunootoshigo")
O("youjiuo", "syngnathiformes", "ヨウジウオ", "Syngnathus schlegeli", "楊枝のように細長い。雄の腹に卵を抱く。")
O("taunagi", "percomorpha", "タウナギ", "Monopterus albus", "ウナギに似た細長い淡水魚。空気呼吸ができる。")
O("kamuruchi", "percomorpha", "カムルチー", "Channa argus", "空気呼吸ができる外来の淡水魚。ライギョとも呼ばれる。")
O("tougorouiwashi", "percomorpha", "トウゴロウイワシ", "Doboatherina bleekeri", "沿岸を群れで泳ぐ小魚。イワシとは別の目。")
O("kadayashi", "percomorpha", "カダヤシ", "Gambusia affinis", "子を産む外来の小魚。蚊の幼虫を食べる。")
O("nairutirapia", "percomorpha", "ナイルティラピア", "Oreochromis niloticus", "アフリカ原産の外来魚。口の中で卵や稚魚を守る。")
O("bora", "percomorpha", "ボラ", "Mugil cephalus", "成長につれて名前が変わる出世魚。卵巣がからすみになる。")
C("blenniiformes", "percomorpha", "ギンポ目", "Blenniiformes", "目", "イソギンポ類やスズメダイ類など。")
move("blenniiformes", "kakurekumanomi")
O("isoginpo", "blenniiformes", "イソギンポ", "Parablennius yatabei", "磯の岩の穴にすむ小魚。")
C("labriformes", "percomorpha", "ベラ目", "Labriformes", "目", "ベラ類やブダイ類。")
O("kyuusen", "labriformes", "キュウセン", "Leptojulis poecilepterus", "夜は砂にもぐって眠るベラ。")
O("kobudai", "labriformes", "コブダイ", "Bodianus reticulatus", "雄の額が大きくこぶ状にふくらむ。雌から雄に性転換する。")
C("acropomatiformes", "percomorpha", "ホタルジャコ目", "Acropomatiformes", "目", "スズキ・アカムツ・ムツなど。")
move("acropomatiformes", "suzuki")
O("akamutsu", "acropomatiformes", "アカムツ", "Doederleinia berycoides", "口の中が黒いことから「のどぐろ」とも呼ばれる。")
_find("akamutsu")["aliases"] = ["ノドグロ"]
C("lophiiformes", "percomorpha", "アンコウ目", "Lophiiformes", "目", "背びれの棘が釣り竿のように変化した魚。")
move("lophiiformes", "kiankou")
O("kaeruankou", "lophiiformes", "カエルアンコウ", "Antennarius striatus", "胸びれで海底を歩くように動く。")
C("carcharhiniformes", "selachii", "メジロザメ目", "Carcharhiniformes", "目", "メジロザメ・シュモクザメ・ドチザメなど。")
move("carcharhiniformes", "akashumokuzame", "yoshikirizame", "hoshizame")
C("lamniformes", "selachii", "ネズミザメ目", "Lamniformes", "目", "ホオジロザメ・メガマウスザメなど。")
move("lamniformes", "hohojirozame", "megamouth")
O("aburatsunozame", "selachii", "アブラツノザメ", "Squalus suckleyi", "背びれの前に棘をもつ。")
O("kikuzame", "selachii", "キクザメ", "Echinorhinus brucus", "体に菊の花のような大きな突起が散らばる深海のサメ。")
O("kasuzame", "selachii", "カスザメ", "Squatina japonica", "エイのように平たい体をもつサメ。")
C("myliobatiformes", "batoidea", "トビエイ目", "Myliobatiformes", "目", "アカエイ・トビエイ・イトマキエイなど。")
move("myliobatiformes", "akaei", "nanyoumanta", "narutobiei")
O("gangiei", "batoidea", "ガンギエイ", "Dipturus chinensis", "ひし形の体をもつエイ。卵を殻に包んで産む。")
O("sakatazame", "batoidea", "サカタザメ", "Rhinobatos schlegelii", "サメのような体の後半をもつエイ。")
_T = {4: "sokogisu sekitoriiwashi nezumigisu houraieso shachiburi hadakaiwashi ginmedai ashiro kakureuo karaiwashi sotoiwashi isoginpo kyuusen kikuzame gangiei sakatazame aburatsunozame kasuzame ittoudai mizuuo maeso nigisu gigi taunagi tougorouiwashi kaeruankou youjiuo akamanbou matsukasauo caudelljuzuhige shiroarimodoki suzumebachinejirebane rakudamushi sakei akaonettaichou abi nogan amatsubame yotaka kochidori oomizunagidori katsuodori buppousou yatsugashira bunbukuchagama",
      3: "kamuruchi kadayashi nairutirapia bora suketoudara akamutsu kobudai iga hototogisu ban kaitsuburi kawau akagera"}
for _t, _ids in _T.items():
    for _id in _ids.split():
        _find(_id)["tier"] = _t

# ---------------- 環形動物（特に多毛類）を増やす（2026-10-23 作者「環形動物少なすぎ、特に多毛類」） ----------------
# 照合は check/annelida/・check/annelida2/（和名は BISMaL(CoL) 優先）。
C("phyllodocida", "errantia", "サシバゴカイ目", "Phyllodocida", "目", "ゴカイ・チロリ・ウロコムシなど。よく動き回る多毛類。")
C("nereididae", "phyllodocida", "ゴカイ科", "Nereididae", "科", "釣り餌でおなじみのゴカイ類。")
move("nereididae", "yamatokawagokai")
O("isogokai", "nereididae", "イソゴカイ", "Perinereis nuntia", "岩の多い海岸にすむゴカイ。")
O("aogokai", "nereididae", "アオゴカイ", "Perinereis aibuhitensis", "「アオイソメ」の名で釣り餌として売られる。")
_find("aogokai")["aliases"] = ["アオイソメ"]
O("chirori", "phyllodocida", "チロリ", "Glycera chirori", "口を勢いよく突き出して獲物を捕らえる。釣り餌にもされる。")
O("yachiurokomushi", "phyllodocida", "ヤチウロコムシ", "Lepidonotus elongatus", "背中がうろこのような板でおおわれた多毛類。")
O("oyogigokai", "phyllodocida", "オヨギゴカイ", "Tomopteris pacifica", "透明な体で一生を海中で泳いで暮らす。")
C("eunicida", "errantia", "イソメ目", "Eunicida", "目", "イソメ類。じょうぶなあごをもつ。")
move("eunicida", "iwamushi")
O("oniisome", "eunicida", "オニイソメ", "Eunice aphroditois", "砂に体を埋め、大きなあごで通りかかった魚を捕らえる。長さ1m以上になることもある。")
O("sugokaiisome", "eunicida", "スゴカイイソメ", "Diopatra sugokai", "貝殻のかけらなどを貼りつけた管の中にすむ。")
C("sabellida", "sedentaria", "ケヤリムシ目", "Sabellida", "目", "管の中にすみ、頭の触手を花のように広げて餌をとる。ハオリムシ類もここに含まれる。")
move("sabellida", "keyarimushi", "satsumahaorimushi")
O("ibarakanzashi", "sabellida", "イバラカンザシ", "Spirobranchus giganteus", "サンゴに埋まった石灰の管から、色とりどりのらせん状の触手を出す。")
O("kasanekanzashigokai", "sabellida", "カサネカンザシゴカイ", "Hydroides elegans", "船底などに石灰の管を作って付着する。")
O("tamashikigokai", "sedentaria", "タマシキゴカイ", "Arenicola brasiliensis", "干潟の砂にすみ、砂の上にとぐろを巻いたような糞を残す。")
O("mizuhikigokai", "sedentaria", "ミズヒキゴカイ", "Cirriformia tentaculata", "泥の中にすみ、糸のような触手を泥の上に広げる。")
O("itogokai", "sedentaria", "イトゴカイ", "Capitella capitata", "有機物の多い泥に多く、環境の汚れの目安にされる。")
_find("itogokai")["aliases"] = ["ナミイトゴカイ"]
O("umiisagomushi", "sedentaria", "ウミイサゴムシ", "Lagis bocki", "砂粒を貼りつけた円すい形の管の中にすむ。")
O("tsutsuoofelia", "sedentaria", "ツツオオフェリア", "Armandia lanceolata", "砂の中にすむ小型の多毛類。")
O("tsubasagokai", "annelida", "ツバサゴカイ", "Chaetopterus cautus", "U字形の管の中にすみ、翼のような突起で水流を起こす。")
O("eramimizu", "clitellata", "エラミミズ", "Branchiura sowerbyi", "体の後ろにえらをもつ水中のミミズ。")
for _t, _ids in {3: "isogokai aogokai chirori oniisome ibarakanzashi",
                 4: "yachiurokomushi oyogigokai sugokaiisome kasanekanzashigokai tamashikigokai mizuhikigokai itogokai umiisagomushi tsutsuoofelia tsubasagokai eramimizu"}.items():
    for _id in _ids.split():
        _find(_id)["tier"] = _t

# 作者の指定（2026-10-24）
C("psittaciformes", "australaves", "インコ目", "Psittaciformes", "目", "インコ・オウム類。足の指が前後2本ずつに分かれる。")
move("psittaciformes", "sekiseiinko")
O("kakapo", "psittaciformes", "カカポ", "Strigops habroptilus", "ニュージーランドにすむ飛べないインコ。夜行性で、世界で最も重いインコ。",
  ["フクロウオウム"])
_find("kakapo")["sciSynonyms"] = ["Strigops habroptila"]
_find("kakapo")["tier"] = 3
O("youmu", "psittaciformes", "ヨウム", "Psittacus erithacus", "アフリカにすむ灰色のインコ。人の言葉をよくまねる。")
O("greenbasilisk", "squamata", "グリーンバシリスク", "Basiliscus plumifrons", "後ろ脚で水面を走ることができるトカゲ。")
C("boidae", "serpentes", "ボア科", "Boidae", "科", "獲物に巻きついて締めつけるヘビ。子を産む種が多い。")
O("nijiboa", "boidae", "ニジボア", "Epicrates cenchria", "うろこが光を受けて虹色に輝くボア。", ["ブラジルレインボーボア"])
O("colombianijiboa", "boidae", "コロンビアニジボア", "Epicrates maurus", "以前はニジボアの亜種とされていたボア。", ["コロンビアレインボーボア"],
  v={"ja": "和名は Catalogue of Life のみで確認。ペットの通称はコロンビアレインボーボア"})
for _id, _t in {"youmu": 2, "greenbasilisk": 3, "nijiboa": 3, "colombianijiboa": 4}.items():
    _find(_id)["tier"] = _t
O("etopirika", "charadriiformes", "エトピリカ", "Fratercula cirrhata", "大きなオレンジ色のくちばしと黄色い飾り羽をもつ海鳥。北海道東部でわずかに繁殖する。")
_find("etopirika")["tier"] = 3
C("calappidae", "brachyura", "カラッパ科", "Calappidae", "科", "はさみで顔を隠すような姿勢をとるカニ。")
O("torafukarappa", "calappidae", "トラフカラッパ", "Calappa lophos", "砂にもぐるカニ。はさみの突起で巻貝の殻を割って食べる。")
O("meganekarappa", "calappidae", "メガネカラッパ", "Calappa philargius", "甲羅に眼鏡のような模様があるカラッパ。")
# タナゴ類（名前と科は本村目録 ver. 42）。種の和名がある種だけ。亜種にだけ和名がある種（バラタナゴ類・タビラ類・カゼトゲタナゴ類）は保留。
C("acheilognathidae", "cypriniformes", "タナゴ科", "Acheilognathidae", "科", "生きた二枚貝の中に卵を産みつける小型のコイ類。")
O("tanago", "acheilognathidae", "タナゴ", "Acheilognathus melanogaster", "関東・東北の平野部にすむ。")
O("ichimonjitanago", "acheilognathidae", "イチモンジタナゴ", "Acheilognathus cyanostigma", "体の側面に一本の青い線がある。")
O("itasenpara", "acheilognathidae", "イタセンパラ", "Acheilognathus longipinnis", "国の天然記念物。秋に産卵する。")
O("ootanago", "acheilognathidae", "オオタナゴ", "Acheilognathus macropterus", "大陸から入った外来のタナゴ。")
O("kanehira", "acheilognathidae", "カネヒラ", "Acheilognathus rhombeus", "日本のタナゴでは大型。秋に産卵する。")
O("zenitanago", "acheilognathidae", "ゼニタナゴ", "Acheilognathus typus", "うろこが細かい。数が大きく減っている。")
O("miyakotanago", "acheilognathidae", "ミヤコタナゴ", "Pseudorhodeus tanago", "関東地方の固有種で国の天然記念物。")
O("yaritanago", "acheilognathidae", "ヤリタナゴ", "Tanakia lanceolata", "日本で最も広く分布するタナゴの一つ。")
O("aburabote", "acheilognathidae", "アブラボテ", "Tanakia limbata", "体が油を塗ったような褐色をしている。")
for _id, _t in {"torafukarappa": 3, "meganekarappa": 4, "tanago": 3, "itasenpara": 3, "miyakotanago": 3,
                "ichimonjitanago": 4, "ootanago": 4, "kanehira": 4, "zenitanago": 4, "yaritanago": 4, "aburabote": 4}.items():
    _find(_id)["tier"] = _t
# 作者「ニッポンバラタナゴとタイリクバラタナゴを同種と扱うのはまずい」（2026-10-24）→ 亜種を別々の項目として入れる（例外）。
O("nipponbaratanago", "acheilognathidae", "ニッポンバラタナゴ", "Rhodeus ocellatus kurumeus",
  "西日本の在来の亜種。外来のタイリクバラタナゴとの交雑で純粋な集団が減っている。")
O("tairikubaratanago", "acheilognathidae", "タイリクバラタナゴ", "Rhodeus ocellatus ocellatus",
  "大陸から入った外来の亜種。在来のニッポンバラタナゴと交雑する。")
_find("nipponbaratanago")["tier"] = 3
_find("tairikubaratanago")["tier"] = 3
# 亜種の扱いは保留（2026-10-24 作者「もっと深掘って議論するべき、別名で拾うのも危うい。一旦保留」）。バラタナゴの2亜種はいったん外す。
species[:] = [s for s in species if s["id"] not in ("nipponbaratanago", "tairikubaratanago")]
_find("inu")["verify"] = {"sci": "オオカミの亜種 Canis lupus familiaris とする扱いもある"}
# 亜種名の別名（2026-10-24 作者の決定「亜種と明示して種で推測」）。aliases のうち亜種の和名を subspeciesAliases にも書き、
# 補完候補で「〜（…の亜種）」と表示する。aliases には残すので、古いページでも今までどおり打てる。
# キシャヤスデ／オビババヤスデはどちらが種かの扱いを議論中のため入れない。
SUBSP_ALIASES = {
    "akamimigame": ["ミシシッピアカミミガメ"],
    "bengaruyamaneko": ["ツシマヤマネコ", "イリオモテヤマネコ"],
    "akagitsune": ["ホンドギツネ", "キタキツネ"],
    "kitanakiusagi": ["エゾナキウサギ"],
    "nihonmitsubachi": ["ニホンミツバチ"],
    "tanuki": ["ホンドタヌキ"],
}
for _id, _ns in SUBSP_ALIASES.items():
    _s = _find(_id)
    assert all(n in _s["aliases"] for n in _ns), _id
    _s["subspeciesAliases"] = _ns

# ---------------- 一言説明の言い切りの見直し（2026-10-24、check/facts/fixes.md） ----------------
edit("garoamushi", fact="翅のない原始的な昆虫。寒い山地の石の下などにすむ。1924年に日光の中禅寺湖付近の標本から記載された。")
edit("daiouika", fact="全長10 mを超える深海のイカ。2004年に小笠原沖で初めて野生の生きた姿が撮影され、2012年には深海を泳ぐ姿が動画に収められた。")
edit("akasango", fact="宝石サンゴの代表。深い海にすみ、成長が非常に遅い。")
edit("gorilla", fact="最大級の霊長類。")
edit("lion", fact="ネコ科では珍しく、群れで暮らす。")
edit("itou", fact="日本最大級の淡水魚。北海道にすむ。")
edit("ikaritogeobimushi", fact="海岸の砂粒のすき間にすむ腹毛動物。1937年に広島付近から記載された。")
edit("minamimedaka", fact="日本のメダカは2種に分けられ、本種は本州の日本海側北部（キタノメダカの分布域）を除く本州から琉球列島にかけて分布する。")
edit("kitanomedaka", fact="本州の日本海側（青森県から兵庫県）に分布するメダカ。ミナミメダカとは別種として記載された。")
edit("hayabusa", fact="急降下では時速300 kmを超えるともいわれる。タカに似るが、オウムやスズメに近い。")
# 種の範囲（種か亜種か）は分類群ごとに更新されている世界の種リストに従う（2026-10-24 作者「最新の学説を参照したい」）。
# 哺乳類 MDD 2.1、鳥 IOC World Bird List 15.2、爬虫類 Reptile Database 2026-06（いずれも ChecklistBank 経由）、魚は本村目録、海産は WoRMS。
# 2026-10-24 照合（check/latest/summary.md）：四肢動物171種のうち食い違いはシジュウカラだけ。
_s = _find("shijuukara")
_s["sci"] = "Parus cinereus"
_s["gbif"] = 6101070
_s["sciSynonyms"] = ["Parus minor"]   # 日本のシジュウカラに使われていた学名。説明文で今の扱い（P. cinereus の亜種）を書いている
_s["fact"] += "日本のものを別種 Parus minor とする扱いもあったが、IOC世界鳥類リスト（15.2版）と日本鳥類目録改訂第8版は P. cinereus の亜種とする。"
META["taxonomy"]["nomenclature"] += ("。種の範囲（種か亜種か）は分類群ごとの世界の種リストに合わせた（2026-10-24）："
    "哺乳類 Mammal Diversity Database 2.1、鳥類 IOC World Bird List 15.2、爬虫類 The Reptile Database 2026-06。")

# ---------------- 一言説明の出典確認による修正（2026-10-24、check/facts/sources.md） ----------------
edit("kakurekumanomi", fact="イソギンチャクの刺胞に刺されずにすむ。群れでいちばん大きな個体が雌で、雌がいなくなると次に大きな雄が雌に性転換する。")
edit("dicyemida", desc="タコやコウイカなど、海底近くで暮らす頭足類の腎臓にすむ。体は40個ほどまでの細胞だけでできている。")
edit("yatsudehitode", fact="腕は7〜10本ほどあり、体を分裂させて増える。")
edit("obikurage", fact="体が帯のように左右に長く伸び、1 mを超えることもある。体をくねらせて泳ぐ。")
edit("ookami", fact="イエイヌはオオカミから家畜化された。")
edit("koala", fact="ほぼユーカリの葉だけを食べる。ユーカリの毒の分解に関わるとみられる酵素の遺伝子が多い。")
edit("minamikiiroazamiuma", fact="体長1 mmほどの細長い昆虫。細い翅の縁に長い毛が房のように並ぶ。野菜の害虫。")
edit("eleutherozoa", desc="ウミユリ綱（ウミユリ・ウミシダ）を除く現生の棘皮動物。ヒトデ・クモヒトデの仲間と、ウニ・ナマコの仲間からなる。")
edit("nankyokuokiami", fact="南極の生態系を支える。1種あたりの総重量は野生動物で最大級とされる。")
edit("sazae", fact="それまで使われていた学名が使えないと分かり、2017年に新しい学名 Turbo sazae がつけられた。")
edit("katakuchiiwashi", fact="下あごが上あごよりずっと短く、上あごしかないように見えることが名の由来とされる。しらすや煮干しになる。")
edit("umabiru", fact="血を吸わず、おもに巻貝を食べる。")
edit("culicidae", desc="蚊。血を吸うのは雌だけで、雌も血を吸わない種がある。")
edit("chiroptera", desc="コウモリ。羽ばたいて飛ぶことのできる唯一の哺乳類。")
edit("hexacorallia", desc="触手や隔膜の数が6の倍数になるものが多い。イシサンゴやイソギンチャク。")
edit("coleoptera", desc="前翅が硬い鞘翅になった甲虫。記載された種の数が動物で最も多い目。")
edit("spiralia", desc="らせん卵割を祖先形質とする前口動物。冠輪動物・扁形動物・有顎動物など。")
edit("takaashigani", fact="脚を広げると3 m以上になり、脚を広げた幅では世界最大のカニ。")
edit("higashikirigirisu", fact="日本のキリギリスを東西2種に分ける扱いでの、東日本の種。同じ種とする見方もある。")

# ---------------- ハゼ目を増やす（2026-10-24 作者了承、0.3.3 として 10/26〜） ----------------
# 和名・学名・科は本村浩之（2026）日本産魚類全種目録 ver.42 で照合（8種とも一致）。
# 目録ではマハゼ・ムツゴロウなどはオクスデルクス科、ダテハゼはハゼ科。ハゼ科はダテハゼ1種なので節目を作らない。
C("oxudercidae", "gobiiformes", "オクスデルクス科", "Oxudercidae", "科",
  "マハゼ・ムツゴロウ・ヨシノボリ類など。日本産魚類全種目録では、従来のハゼ科からこの科が分けられている。",
  v={"placement": "ハゼ科に含める分類体系もある（日本産魚類全種目録に従う）"})
move("oxudercidae", "mahaze", "mutsugorou")
O("tobihaze", "oxudercidae", "トビハゼ", "Periophthalmus modestus", "干潟の泥の上で暮らし、胸びれで這ったり、尾で跳ねたりする。")
O("warasubo", "oxudercidae", "ワラスボ", "Odontamblyopus lacepedii", "日本では有明海などの泥干潟にすむ。目は小さく皮膚に埋もれ、口には鋭い歯が並ぶ。")
O("chichibu", "oxudercidae", "チチブ", "Tridentiger obscurus", "河口や内湾の汽水域に多いハゼ。雄が石のすき間などに産みつけられた卵を守る。")
O("shirouo", "oxudercidae", "シロウオ", "Leucopsarion petersii", "春に川をさかのぼって産卵する透明な小魚。シラウオ（シラウオ科）とは別の魚。")
O("ukigori", "oxudercidae", "ウキゴリ", "Gymnogobius urotaenia", "川や湖にすむハゼ。第1背びれの後ろの端に黒い斑点がある。")
O("kawayoshinobori", "oxudercidae", "カワヨシノボリ", "Rhinogobius flumineus", "海に下らず、一生を川で過ごすヨシノボリ。")
O("mimizuhaze", "oxudercidae", "ミミズハゼ", "Luciogobius guttatus", "体が細長い小さなハゼ。海岸や河口の石のすき間にすむ。")
O("datehaze", "gobiiformes", "ダテハゼ", "Amblyeleotris japonica", "テッポウエビの仲間が掘った巣穴に同居し、ハゼが見張り役をする。")
for _id, _t in {"tobihaze": 2, "warasubo": 3, "chichibu": 3, "shirouo": 3, "ukigori": 3,
                "kawayoshinobori": 3, "mimizuhaze": 4, "datehaze": 3}.items():
    _find(_id)["tier"] = _t
META["datasetVersion"] = "0.3.3"  # 10/26〜（ハゼ8種）

# C. elegans の表示名（2026-10-24 作者の決定）：標準和名がないので、日本語の文献で使われる表記にする
edit("celegans", ja="C. エレガンス", aliases=["シー・エレガンス", "エレガンス", "線虫"],
     verify={"ja": "標準和名はない。日本語の文献で使われる表記「C. エレガンス」で示す"})

# アメリカンロブスター → 標準和名アメリカウミザリガニ（2026-10-24 作者了承。徳島県水産研究所の報告に「標準和名；アメリカウミザリガニ」）
edit("lobster", ja="アメリカウミザリガニ", jaStatus="standard", aliases=["アメリカンロブスター", "オマールエビ", "ロブスター"],
     fact="北米大西洋岸の大型のエビ。アメリカンロブスターとも呼ばれ、オマールエビの名で売られる。")

# ---------------- 通称（2026-10-24 作者「許可できるのはサナダムシとプラナリアと魚介類だけ」） ----------------
# 打っても今の名前に含まれず候補に出ないものだけ足す。プラナリア（ナミウズムシ）は build_data.py の GROUP_ALIASES から外して aliases に残した。
for _id in ("mukoujouchu", "yuukoujouchu"):
    _find(_id)["aliases"].append("サナダムシ")
# 通称で当てる種は、一言説明でも通称との関係を書く（2026-10-24 作者）
edit("namiuzumushi", fact="体を切っても各断片から全身が再生する。「プラナリア」の名で実験に使われる代表的な種。プラナリアはもともとウズムシの仲間を広く指す呼び名。")
edit("nihonkairettojouchu", fact="サクラマスなどの生食で感染し、数mに達する。「サナダムシ」は条虫の仲間をまとめて呼ぶ俗称。")
edit("mukoujouchu", fact="牛肉の生食で感染する。「サナダムシ」と呼ばれる条虫の一種。")
edit("yuukoujouchu", fact="豚肉の生食で感染する。頭部に鉤をもつ。「サナダムシ」と呼ばれる条虫の一種。")

# 学術的に大事な種の一言説明（2026-10-24 作者了承、出典は check/facts/notable_species.md）
edit("senmohirahamushi", fact="体の構造が動物の中でも最も単純な部類。2008年に板状動物で初めてゲノムが読まれ、多くの発生関連遺伝子をもつことが分かった。")
edit("celegans", fact="全細胞の系譜が分かっているモデル生物。1998年に、多細胞生物で初めてゲノムのほぼ全体が読まれた。この線虫を使った研究に2002年のノーベル生理学・医学賞が贈られた。")
edit("drosophila", fact="遺伝学の代表的なモデル生物。このハエで遺伝子が染色体にのっていることを示したモーガンは1933年にノーベル賞を受けた。2000年に昆虫で初めてゲノムの大部分が読まれた。")
edit("sekishokuyakei", fact="ニワトリの祖先。2004年に鳥類で初めてゲノムが読まれた。")
edit("katayureiboya", fact="発生学のモデル生物。2002年に脊椎動物以外の脊索動物で初めてゲノムが読まれた。その時は Ciona intestinalis とされていたが、2015年に本種として分けられた。")
edit("mijinko", fact="条件が良いと雌だけで単為生殖して増える。2011年に甲殻類で初めてゲノムが読まれ、遺伝子が3万以上あることが分かった。")
edit("namihadani", fact="植物の汁を吸う小さなダニ。農作物の害虫。2011年に鋏角類（クモ・ダニの仲間）で初めてゲノムが読まれた。")
edit("kaiko", fact="野生のクワコから家畜化され、人の世話なしには生きられない。2004年にチョウ目で初めてゲノムが読まれた。")
edit("himegiboshimushi", fact="サンゴ礁の砂地にすむギボシムシ。2015年に、別のギボシムシ1種とともに半索動物で初めてゲノムが読まれた。")
edit("kamonohashi", fact="卵を産む哺乳類（単孔類）。くちばしで獲物の電気を感じ取る。2008年に単孔類で初めてゲノムが読まれた。")
edit("akoyagai", fact="真珠の養殖に使われる。2012年に、軟体動物で初めてゲノムを読んだ論文が出た。")
edit("torafugu", fact="肝臓や卵巣にテトロドトキシンをもつ。ゲノムが小さいため、2002年にヒトに次いで脊椎動物で2番目にゲノムが読まれた。")
edit("hatsukanezumi", fact="実験用マウスの元になった種。2002年に、ヒトに次いで哺乳類で2番目にゲノムが読まれた。")
edit("dobunezumi", fact="実験用ラットの元になった種。2004年に、ヒト・マウスに次いで哺乳類で3番目にゲノムが読まれた。")
edit("chimpanzee", fact="ヒトに最も近い現生動物の一つ（もう一つはボノボ）。2005年にゲノムが読まれ、ヒトとの塩基配列の違いは約1.2％だった。")
edit("coelacanth", fact="1938年に南アフリカ沖で生きた個体が見つかった。2013年にゲノムが読まれ、遺伝子の変化がほかの脊椎動物より遅いことが分かった。")
edit("zebrafish", fact="胚が透明で発生を観察しやすいモデル生物。2013年にゲノムが読まれ、ヒトの遺伝子の約7割に対応する遺伝子をもつことが分かった。")
edit("yokozunakumamushi", fact="日本で研究が進むクマムシ。2016年にゲノムが読まれ、放射線から DNA を守るタンパク質（Dsup）が見つかった。")
edit("wakareotamaboya", fact="一生オタマジャクシ形で、自分で作った「ハウス」で餌を濾し取る。ゲノムは約7000万塩基対と動物でとても小さい部類。")
edit("midorishamisengai", fact="古生代から姿の変わらない「生きた化石」とされる。2015年にゲノムが読まれ、姿は変わらなくても遺伝子は変化してきたことが分かった。")
edit("australiahaigyo", fact="鰓に加えて肺で呼吸できる。四肢動物に最も近い現生の魚類の一つ。2021年に読まれたゲノムは約430億塩基対で、ヒトの約14倍ある。")
edit("axolotl", fact="幼生の姿のまま成熟する。ウーパールーパーの名で知られる。再生研究に使われ、2018年に読まれたゲノムは約320億塩基対とヒトの10倍以上ある。")
edit("nankyokuokiami", fact="南極の生態系を支える。1種あたりの総重量は野生動物で最大級とされる。2023年に読まれたゲノムは約480億塩基対で、ヒトの約16倍ある。")
edit("umihotaru", fact="貝形虫の一種。発光物質を海中に吐き出して青く光る。この発光物質（ルシフェリン）は1956年に下村脩が結晶化し、のちのGFPの発見（2008年ノーベル化学賞）につながった。")
edit("seiyomitsubachi", fact="8の字ダンスで蜜源の方向と距離を伝える。このダンスを解き明かしたフリッシュは1973年にノーベル生理学・医学賞を受けた。")

# ---------------- カメムシ目と水生昆虫を増やす（2026-10-25 作者「カメムシ増やす、ミズカマキリとかの有名水生昆虫増やす」） ----------------
# 照合は check/hemiptera_aquatic/（和名は15種とも CoL・GBIF・Wikidata・iNat で一致。学名は3種が GBIF のみ応答）。
C("heteroptera", "hemiptera", "カメムシ亜目", "Heteroptera", "亜目", "前翅の付け根側が硬くなったカメムシ類。異翅亜目とも。アメンボ・タガメ・サシガメなど。")
move("heteroptera", "amenbo", "tagame", "kusagikamemushi", "tokojirami")
C("nepomorpha", "heteroptera", "タイコウチ下目", "Nepomorpha", "下目", "水中で暮らすカメムシ類。前脚で獲物を捕らえるものが多い。")
C("nepidae", "nepomorpha", "タイコウチ科", "Nepidae", "科", "腹の先の長い呼吸管を水面に出して空気を取り入れる。")
C("belostomatidae", "nepomorpha", "コオイムシ科", "Belostomatidae", "科", "タガメ・コオイムシなど。雄が卵を守る。")
move("belostomatidae", "tagame")
O("mizukamakiri", "nepidae", "ミズカマキリ", "Ranatra chinensis", "細長い体と鎌のような前脚をもつ水生のカメムシ。前脚で小魚や昆虫を捕らえて体液を吸う。")
O("taikouchi", "nepidae", "タイコウチ", "Laccotrephes japonensis", "池や田んぼの浅い水にすむ。腹の先の呼吸管を水面に出して呼吸する。")
O("kooimushi", "belostomatidae", "コオイムシ", "Appasus japonicus", "雌が雄の背中に卵を産みつけ、雄が卵を背負って守る。")
O("matsumomushi", "nepomorpha", "マツモムシ", "Notonecta triguttata", "背中を下にして泳ぐ水生のカメムシ。刺されると痛い。")
O("esakimonkitsunokamemushi", "heteroptera", "エサキモンキツノカメムシ", "Sastragala esakii", "背中に黄色いハート形の紋がある。雌が卵や幼虫に覆いかぶさって守る。")
O("akasujikamemushi", "heteroptera", "アカスジカメムシ", "Graphosoma rubrolineatum", "赤と黒の縦縞が目立つ。セリ科の植物によくとまる。",
  v={"sci": "Catalogue of Life では未確認（GBIF のみ）"})
O("marukamemushi", "heteroptera", "マルカメムシ", "Megacopta punctatissima", "丸くて小さなカメムシ。クズなどマメ科の植物に群がる。",
  v={"sci": "近縁の M. cribraria と同種とする見解もある"})
O("yokozunasashigame", "heteroptera", "ヨコヅナサシガメ", "Agriosphodrus dohrni", "中国から入ってきたとされるサシガメ。サクラなどの幹で集団で越冬し、ほかの昆虫の体液を吸う。")
C("sternorrhyncha", "hemiptera", "腹吻亜目", "Sternorrhyncha", "亜目", "アブラムシ・カイガラムシ・コナジラミ・キジラミなど。植物の汁を吸う小さな虫。")
O("momoakaaburamushi", "sternorrhyncha", "モモアカアブラムシ", "Myzus persicae", "さまざまな作物につく害虫。植物のウイルス病を広める。")
O("iseriakaigaramushi", "sternorrhyncha", "イセリアカイガラムシ", "Icerya purchasi", "柑橘類の害虫。天敵のベダリアテントウを導入して抑えた、生物的防除の代表例。", ["ワタフキカイガラムシ"])
O("tobiirounka", "hemiptera", "トビイロウンカ", "Nilaparvata lugens", "稲の害虫。梅雨のころ、大陸から気流に乗って日本に飛んでくる。")
O("aobahagoromo", "hemiptera", "アオバハゴロモ", "Geisha distinctissima", "薄緑色の三角形の翅をもつ。幼虫は白い綿のような蝋をまとう。")
C("lampyridae", "coleoptera", "ホタル科", "Lampyridae", "科", "腹の発光器で光るものが多い甲虫。")
move("lampyridae", "genjibotaru")
O("heikebotaru", "lampyridae", "ヘイケボタル", "Aquatica lateralis", "田んぼや湿地にすむホタル。幼虫は水中で巻貝を食べる。")
O("gamushi", "coleoptera", "ガムシ", "Hydrophilus acuminatus", "池や田んぼにすむ大型の水生甲虫。成虫はおもに水草を食べ、幼虫は巻貝などを捕らえる。")
O("mizusumashi", "coleoptera", "ミズスマシ", "Gyrinus japonicus", "水面をくるくる回るように泳ぐ甲虫。複眼が水面の上と下を見る2つに分かれている。",
  v={"sci": "Catalogue of Life では未確認（GBIF のみ）"})
for _id, _t in {"mizukamakiri": 2, "taikouchi": 3, "kooimushi": 3, "matsumomushi": 3, "esakimonkitsunokamemushi": 3,
                "akasujikamemushi": 3, "marukamemushi": 3, "yokozunasashigame": 3, "momoakaaburamushi": 3,
                "iseriakaigaramushi": 4, "tobiirounka": 3, "aobahagoromo": 3, "heikebotaru": 2, "gamushi": 3, "mizusumashi": 3}.items():
    _find(_id)["tier"] = _t
META["datasetVersion"] = "0.3.4.1"  # (上書きあり) カメムシ目・水生昆虫15種。10/26〜（ネタバレ回避で版名変更、0.3.3 は不使用）

# ---------------- 作者の指定（2026-10-25）：鳥 ----------------
# 照合は check/picks7/・check/picks8/（学名・和名とも一致）。
C("muscicapidae", "passeriformes", "ヒタキ科", "Muscicapidae", "科", "ヒタキ・ツグミの仲間に近い小鳥。ジョウビタキ・キビタキ・オオルリなど。")
O("joubitaki", "muscicapidae", "ジョウビタキ", "Phoenicurus auroreus", "冬に大陸から渡ってくる。雄は胸がオレンジ色で、翼に白い斑がある。日本で繁殖する例も見つかっている。")
O("kibitaki", "muscicapidae", "キビタキ", "Ficedula narcissina", "夏に林で繁殖する。雄は眉と腰が黄色く、のどが橙色。")
O("mozu", "passeriformes", "モズ", "Lanius bucephalus", "捕らえた虫やカエルなどを枝に刺しておく「はやにえ」で知られる。秋に鋭い声で高鳴きする。")
for _id, _t in {"joubitaki": 2, "kibitaki": 3, "mozu": 2}.items():
    _find(_id)["tier"] = _t
O("yairochou", "passeriformes", "ヤイロチョウ", "Pitta nympha", "夏に渡ってきて、西日本などの暗い森で繁殖する。名のとおり羽が多くの色で彩られる。数が少なく絶滅危惧種。")
_find("yairochou")["tier"] = 3   # check/picks9/
O("ogamaguchiyotaka", "strisores", "オーストラリアガマグチヨタカ", "Podargus strigoides",
  "オーストラリアにすむ夜行性の鳥。幅の広い口をもち、昼は枝の上で折れた枝のような姿でじっとしている。ヨタカとは別の目（ガマグチヨタカ目）に分けられる。")
_find("ogamaguchiyotaka")["tier"] = 3   # check/picks10/
# 作者が指定した鳥（2026-10-25 第2弾）。照合は check/picks11/（和名12種一致、ヤマガラは GBIF のみ Poecile varius）。
# コハクチョウ・カワセミ・シジュウカラは収録済み。「ミミズク」は1種の名前ではないので 作者に確認。
C("strigiformes", "afroaves", "フクロウ目", "Strigiformes", "目", "夜行性の猛禽。顔が平たく、音で獲物の位置を知る。")
move("strigiformes", "fukurou")
O("konohazuku", "strigiformes", "コノハズク", "Otus sunia", "夏に渡ってくる小型のフクロウ。「ブッ・ポウ・ソウ」と鳴き、「声のブッポウソウ」と呼ばれた。")
C("piciformes", "afroaves", "キツツキ目", "Piciformes", "目", "キツツキ・オオハシなど。足の指が前後2本ずつに分かれる。")
move("piciformes", "akagera")
O("kogera", "piciformes", "コゲラ", "Yungipicus kizuki", "スズメほどの大きさの小さなキツツキ。都市の公園でも見られる。")
_find("kogera")["sciSynonyms"] = ["Dendrocopos kizuki"]
C("falconiformes", "australaves", "ハヤブサ目", "Falconiformes", "目", "ハヤブサ・チョウゲンボウなど。タカに似るが、タカ目とは別の系統。")
move("falconiformes", "hayabusa")
O("chougenbou", "falconiformes", "チョウゲンボウ", "Falco tinnunculus", "小型のハヤブサの仲間。空中で羽ばたいて止まり（停空飛翔）、地上のネズミなどを探す。")
O("okameinko", "psittaciformes", "オカメインコ", "Nymphicus hollandicus", "オーストラリア原産。冠羽と頬の橙色の斑が目立つ。オウム科の仲間で、ペットとして飼われる。")
O("aoashikatsuodori", "suliformes", "アオアシカツオドリ", "Sula nebouxii", "鮮やかな青い足をもつ海鳥。雄は求愛のとき足を交互に持ち上げて見せる。ガラパゴス諸島などにすむ。")
C("paridae", "passeriformes", "シジュウカラ科", "Paridae", "科", "シジュウカラ・ヤマガラ・コガラなど。")
move("paridae", "shijuukara")
O("yamagara", "paridae", "ヤマガラ", "Sittiparus varius", "木の実を蓄える習性がある。人によく慣れ、昔はおみくじを引く芸に使われた。")
_find("yamagara")["sciSynonyms"] = ["Poecile varius"]
O("enaga", "passeriformes", "エナガ", "Aegithalos caudatus", "長い尾をもつ小さな鳥。冬は群れで動く。北海道の亜種シマエナガは顔が真っ白。", ["シマエナガ"])
_find("enaga")["subspeciesAliases"] = ["シマエナガ"]
O("misosazai", "passeriformes", "ミソサザイ", "Troglodytes troglodytes", "尾をぴんと立てる小さな茶色の鳥。体の割に大きな声で複雑にさえずる。")
O("rurikakesu", "passeriformes", "ルリカケス", "Garrulus lidthi", "奄美群島の一部にだけすむカラス科の鳥。瑠璃色と赤茶色の羽をもつ。鹿児島県の県鳥。")
O("ooruri", "muscicapidae", "オオルリ", "Cyanoptila cyanomelana", "夏に渡ってきて渓流沿いの林で繁殖する。雄は背中が深い青色で、美しい声でさえずる。")
O("isohiyodori", "muscicapidae", "イソヒヨドリ", "Monticola solitarius", "海岸の岩場にすむが、市街地でも見られるようになった。名前に反してヒヨドリではなくヒタキ科の鳥。")
O("rurihitaki", "muscicapidae", "ルリビタキ", "Tarsiger cyanurus", "雄は成長すると背中が瑠璃色になる。夏は山地の森、冬は低地で過ごす。")
for _id, _t in {"konohazuku": 3, "kogera": 2, "chougenbou": 3, "okameinko": 2, "aoashikatsuodori": 3, "yamagara": 2,
                "enaga": 2, "misosazai": 3, "rurikakesu": 3, "ooruri": 2, "isohiyodori": 3, "rurihitaki": 3}.items():
    _find(_id)["tier"] = _t
# 「ミミズク」→ 作者「トラフズク以外」（2026-10-25）。照合は check/picks12/。ワシミミズクの和名は日本鳥類目録改訂第8版に掲載。
O("washimimizuku", "strigiformes", "ワシミミズク", "Bubo bubo", "ユーラシアに広く分布する大型のフクロウ。日本では北海道でまれに記録される。")
O("komimizuku", "strigiformes", "コミミズク", "Asio flammeus", "冬に渡ってきて、草原や河原を低く飛んでネズミを探す。昼間も活動する。")
O("ookonohazuku", "strigiformes", "オオコノハズク", "Otus semitorques", "一年中日本の森にすむ小型のフクロウ。目が橙色。")
for _id, _t in {"washimimizuku": 2, "komimizuku": 3, "ookonohazuku": 3}.items():
    _find(_id)["tier"] = _t
# 作者の指定（2026-10-25）。照合は check/picks13/。
O("kantetsu", "trematoda", "肝蛭", "Fasciola hepatica", "ウシやヒツジなどの肝臓の胆管に寄生する大型の吸虫。巻貝を中間宿主とし、水草についた幼虫を食べて感染する。", ["カンテツ"],
  v={"sci": "日本の肝蛭は F. hepatica と巨大肝蛭 F. gigantica の雑種に由来するとされる系統が多い"})
_find("kantetsu")["tier"] = 4
META["datasetVersion"] = "0.3.5"  # 作者が指定した鳥など（10/27〜の予定）
# 作者の指定（2026-10-25）。照合はゲキムズ用の check/hard_inv/（result.json で ok）。
R("nunomeitomakihitode", "asteroidea", "ヌノメイトマキヒトデ", "Aquilonastra batheri", "磯の石の下などにいる小さなヒトデ。イトマキヒトデと同じイトマキヒトデ科。")
R("togemomijigai", "asteroidea", "トゲモミジガイ", "Astropecten polyacanthus", "モミジガイの仲間で、腕の縁に長い棘が並ぶ。砂底にすみ、フグ毒（テトロドトキシン）をもつ例が報告されている。")
R("sukashikashipan", "echinoidea", "スカシカシパン", "Astriclypeus mannii", "平たい円盤形のウニで、殻に細長い穴が5つ開いている。浅い砂底に潜ってすむ。タコノマクラと同じタコノマクラ目。")  # 照合 check/picks14/
for _id in ("nunomeitomakihitode", "togemomijigai"):
    _find(_id)["tier"] = 4
_find("sukashikashipan")["tier"] = 3
# ゲキムズと揃える（2026-10-25）：シリケンイモリの2亜種名（ゲキムズ側の別名に合わせた）。別名だけなので版は上げない。
_find("shirikenimori")["aliases"] = ["アマミシリケンイモリ", "オキナワシリケンイモリ"]
_find("shirikenimori")["subspeciesAliases"] = ["アマミシリケンイモリ", "オキナワシリケンイモリ"]
META["datasetVersion"] = "0.3.6"  # 作者が指定したヒトデ・カシパン（10/28〜の予定）
# 十脚目の追加（作者「十脚目をもっと、ゴシキエビとか」、振り分けは任せる 2026-10-25）。候補と入れる先は check/decapoda/candidates.md。
# エビ類などは check/decapoda/consensus.tsv、カニはゲキムズの照合結果（check/hard_inv/result.json で ok）。知名度4の5種はゲキムズだけに置く。
R("goshikiebi", "achelata", "ゴシキエビ", "Panulirus versicolor", "イセエビの仲間。体に青・白・黒などの模様があり、サンゴ礁にすむ。")
R("nishikiebi", "achelata", "ニシキエビ", "Panulirus ornatus", "イセエビの仲間で大型になる。脚に黄色と黒の縞模様がある。")
R("uchiwaebi", "achelata", "ウチワエビ", "Ibacus ciliatus", "セミエビの仲間。体が平たく、うちわのような形をしている。砂泥底にすみ、食用にされる。")
R("zouriebi", "achelata", "ゾウリエビ", "Parribacus japonicus", "セミエビの仲間。平たい体が草履に似る。岩礁にすむ。")
R("akazaebi", "astacidea", "アカザエビ", "Metanephrops japonicus", "細長いはさみをもつ赤いエビ。やや深い海の泥底に穴を掘ってすむ。食用にされる。")
R("uchidazarigani", "astacidea", "ウチダザリガニ", "Pacifastacus leniusculus", "北米原産のザリガニ。食用として持ち込まれ、北海道などで野生化した。特定外来生物。")
R("botanebi", "caridea", "ボタンエビ", "Pandalus nipponensis", "やや深い海にすむタラバエビ科のエビ。市場で「ボタンエビ」として売られるものの多くは近縁のトヤマエビ。")
R("toyamaebi", "caridea", "トヤマエビ", "Pandalus hypsinotus", "北の海にすむタラバエビ科のエビ。北海道などでボタンエビの名で売られる。")
R("teppouebi", "caridea", "テッポウエビ", "Alpheus brevicristatus", "片方の大きなはさみを勢いよく閉じて、パチンと大きな音を出す。干潟などに穴を掘ってすむ。")
R("sujiebi", "caridea", "スジエビ", "Palaemon paucidens", "川や池にすむ透明なエビ。体に黒い縞がある。")
R("minaminumaebi", "caridea", "ミナミヌマエビ", "Neocaridina denticulata", "川や池にすむ小さなヌマエビの仲間。卵からいきなり小さなエビの姿で生まれる。")
R("furisodeebi", "caridea", "フリソデエビ", "Hymenocera picta", "振袖のように広がったはさみをもつ。ヒトデを食べる。")
R("otohimeebi", "decapoda", "オトヒメエビ", "Stenopus hispidus", "赤と白の縞模様のエビ。魚の体についた寄生虫などを食べる掃除エビとして知られる。")
R("shibaebi", "dendrobranchiata", "シバエビ", "Metapenaeus joyneri", "クルマエビの仲間。内湾の砂泥底にすみ、食用にされる。")
R("aburagani", "anomura", "アブラガニ", "Paralithodes platypus", "タラバガニと同じ属のヤドカリの仲間。タラバガニより甲羅の色が青みがかる。")
R("somenyadokari", "anomura", "ソメンヤドカリ", "Dardanus pedunculatus", "貝殻にイソギンチャクをつけて背負うヤドカリ。イソギンチャクは身を守るのに役立つ。")
R("okayadokari", "anomura", "オカヤドカリ", "Coenobita cavipes", "陸で暮らすヤドカリ。オカヤドカリの仲間は天然記念物に指定されている。")
R("benizuwaigani", "brachyura", "ベニズワイガニ", "Chionoecetes japonicus", "ズワイガニより深い海にすむ。ゆでる前から甲羅が赤い。")
R("chuugokumokuzugani", "brachyura", "チュウゴクモクズガニ", "Eriocheir sinensis", "モクズガニに近い種で、中国では「上海蟹（シャンハイガニ）」として食べられる。日本では特定外来生物。", ["上海蟹", "シャンハイガニ"])
R("amiminokogirigazami", "brachyura", "アミメノコギリガザミ", "Scylla serrata", "マングローブの泥地などにすむ大型のカニ。はさみが大きく、食用にされる。")
R("ishigani", "brachyura", "イシガニ", "Charybdis japonica", "ガザミに近いワタリガニの仲間。岩の多い浅い海にすむ。")
R("asahigani", "brachyura", "アサヒガニ", "Ranina ranina", "甲羅が縦に長く、朱色をしたカニ。砂に潜ってすむ。食用にされる。")
R("heikegani", "brachyura", "ヘイケガニ", "Heikeopsis japonica", "甲羅の凹凸が怒った人の顔に見える。平家の武者の怨念という言い伝えから名がついた。")
R("isogani", "brachyura", "イソガニ", "Hemigrapsus sanguineus", "磯の石の下などにふつうにいる小さなカニ。")
R("akategani", "brachyura", "アカテガニ", "Chiromantes haematocheir", "はさみが赤いカニ。海辺近くの陸で暮らし、夏の夜に海へ下りて幼生を放つ。")
R("benkeigani", "brachyura", "ベンケイガニ", "Orisarma intermedium", "河口近くの陸で暮らすカニ。甲羅が赤みを帯びる。")
R("shiomaneki", "brachyura", "シオマネキ", "Tubuca arcuata", "雄の片方のはさみがとても大きい。干潟ではさみを振る様子が潮を招くように見える。")
R("ashiharagani", "brachyura", "アシハラガニ", "Helice tridens", "河口のヨシ原などにすむカニ。")
R("kometsukigani", "brachyura", "コメツキガニ", "Scopimera globosa", "砂浜の干潟にすむ小さなカニ。砂を食べて残りを団子にして並べる。")
R("chigogani", "brachyura", "チゴガニ", "Ilyoplax pusilla", "泥の干潟にすむ小さなカニ。雄ははさみを上げ下げして求愛する。")
R("minamikometsukigani", "brachyura", "ミナミコメツキガニ", "Mictyris guinotae", "南の島の干潟に群れでいる青いカニ。前向きに歩く。")
R("mamekobushigani", "brachyura", "マメコブシガニ", "Pyrhila pisum", "丸く小さな甲羅をもつカニ。内湾の干潟にすむ。")
for _id, _t in {"goshikiebi": 3, "nishikiebi": 3, "uchiwaebi": 3, "zouriebi": 3, "akazaebi": 2, "uchidazarigani": 2,
                "botanebi": 2, "toyamaebi": 3, "teppouebi": 2, "sujiebi": 2, "minaminumaebi": 2, "furisodeebi": 3,
                "otohimeebi": 3, "shibaebi": 3, "aburagani": 3, "somenyadokari": 3, "okayadokari": 2, "benizuwaigani": 2,
                "chuugokumokuzugani": 2, "amiminokogirigazami": 3, "ishigani": 3, "asahigani": 3, "heikegani": 2,
                "isogani": 2, "akategani": 2, "benkeigani": 3, "shiomaneki": 2, "ashiharagani": 3, "kometsukigani": 3,
                "chigogani": 3, "minamikometsukigani": 3, "mamekobushigani": 3}.items():
    _find(_id)["tier"] = _t
META["datasetVersion"] = "0.3.7.1"  # 十脚目32種（10/29〜、ネタバレ回避で .1）
# 作者の指定（2026-10-25）。照合はゲキムズ用 check/hard_inv/result.json で ok。
R("subesubemanjuugani", "brachyura", "スベスベマンジュウガニ", "Atergatis floridus", "磯にすむ、つるりとした丸い甲羅のカニ。麻痺性貝毒やフグ毒をもつことがあり、食べると危険。")
_find("subesubemanjuugani")["tier"] = 2
META["datasetVersion"] = "0.3.8"  # スベスベマンジュウガニ（10/27〜に前倒し）
# 単生類（作者 2026-10-26「Neodermata に単生類がいない」）。Brabec et al. 2023（Curr. Biol. 33: 4269）の系統ゲノム解析で
# 単生綱 Monogenea は単系統でないとされ、2亜綱を綱に格上げ（Monopisthocotyla・Polyopisthocotyla）。Polyopisthocotyla が吸虫の姉妹、
# Monopisthocotyla は条虫の姉妹か最初に分かれる系統で解析法により揺れるため、Neodermata の下は4つの多分岐にする。
# 和名「単後吸盤類」「多後吸盤類」は学術文献での定着を確かめていないので学名表記。照合は check/monogenea/ と check/hard_inv/。
_find("neodermata")["desc"] = "吸虫・条虫と、魚などの体表やえらにつく単生類をまとめた寄生性のクレード。幼生の表皮を脱ぎ捨てる。"
_find("neodermata")["polytomy"] = ("吸虫・条虫と、かつて単生綱にまとめられた2群の分かれる順は議論中。系統ゲノム解析（Brabec et al. 2023）では"
                                   "Polyopisthocotyla が吸虫の姉妹群になり、単生綱は単系統でないとされたため、ここでは四分岐で示す。")
C("monopisthocotyla", "neodermata", "Monopisthocotyla", "Monopisthocotyla", "綱",
  "かつての単生綱の一部。体の後ろの固着器は1つの円盤状で、鉤をもつ。魚の体表やえらにつく。",
  v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
C("polyopisthocotyla", "neodermata", "Polyopisthocotyla", "Polyopisthocotyla", "綱",
  "かつての単生綱の一部。体の後ろに小さなはさみ状の固着器が多数並び、主に魚のえらにつく。",
  v={"ja": "日本語の学術文献で定着した和名を確認できないため学名で表記"})
R("burihadamushi", "monopisthocotyla", "ブリハダムシ", "Benedenia seriolae", "ブリなどの体表につく単生類。養殖のブリ類で増えて問題になる。")
R("hiramesinsakatemushi", "polyopisthocotyla", "ヒラメシンサカテムシ", "Neoheterobothrium hirame", "ヒラメのえらや口の中に寄生し、貧血を起こさせる。")
R("futagomushi", "polyopisthocotyla", "フタゴムシ", "Eudiplozoon nipponicum", "コイなどのえらにつく。2匹の幼虫が出会って体が合わさり、一生X字形につながったまま暮らす。")
for _id, _t in {"burihadamushi": 4, "hiramesinsakatemushi": 4, "futagomushi": 3}.items():
    _find(_id)["tier"] = _t
META["datasetVersion"] = "0.3.9"  # 単生類（10/27〜、0.3.8 の予約を差し替え）
# 一覧ページで作者が出した案（2026-10-27）：知名度の変更27件、本家に入れる11種、ゲキムズだけにする13種。
# 本家に入れる種の照合はゲキムズ用の結果（check/hard_inv/result.json、魚は日本産魚類全種目録）。ゲキムズだけにする種は tools/hard/hard_only.json へ。
for _id, _t in {"akaei": 1, "akashumokuzame": 1, "amaminokurousagi": 4, "benikurage": 3, "gangaze": 2, "gigi": 3,
                "hatagoisoginchaku": 4, "hiranousango": 4, "hossugai": 4, "itomakihitode": 1, "kanehira": 3,
                "katayureiboya": 2, "kikumeishi": 2, "kuronamako": 2, "kusabiraishi": 4, "maboya": 1, "matsukasauo": 3,
                "mokuyokukaimen": 4, "momijigai": 4, "nihonkumohitode": 2, "oikawa": 2, "onihitode": 2, "tanago": 1,
                "tatejimaisoginchaku": 2, "togemomijigai": 3, "urikurage": 2, "zebrafish": 1}.items():
    _find(_id)["tier"] = _t
HARD_ONLY = ("ootanago", "zenitanago", "datehaze", "kikuzame", "nezumigisu", "asagaokurage", "bouzujindouika",
             "asiabouzujindouika", "uijindouika", "hoshizame", "kitanakiusagi", "ashiro", "sekitoriiwashi")
species[:] = [s for s in species if s["id"] not in HARD_ONLY]
clades[:] = [c for c in clades if c["id"] != "staurozoa"]  # 十文字クラゲ綱はシラスジアサガオクラゲだけだった
R("kumanoashitsuki", "sedentaria", "クマノアシツキ", "Acrocirrus validus", "磯の石の下などにすむゴカイの仲間（多毛類）。")
R("samidorisashiba", "phyllodocida", "サミドリサシバ", "Eulalia viridis", "鮮やかな緑色をしたサシバゴカイの仲間。磯の岩の間にすむ。")
R("sanhachiurokomushi", "phyllodocida", "サンハチウロコムシ", "Hermilepidonotus helotypus", "背中がうろこのような板でおおわれるウロコムシの仲間。")
R("kuroshitanashiumiushi", "heterobranchia", "クロシタナシウミウシ", "Dendrodoris arborescens", "黒っぽいウミウシ。名のとおり、多くの巻貝がもつ歯舌（やすり状の歯）がない。")
R("akaeraminoumiushi", "heterobranchia", "アカエラミノウミウシ", "Sakuraeolis enosimensis", "背中にミノのような突起が並ぶウミウシ。内湾の岸壁などでよく見られる。")
R("dainanginpo", "perciformes", "ダイナンギンポ", "Dictyosoma temminckii", "磯の岩の間にすむ細長い魚。ギンポと呼ばれるが、ギンポ目ではない。")
R("nabeka", "blenniiformes", "ナベカ", "Omobranchus elegans", "磯や岸壁の穴にすむ小さなギンポ目の魚。体の前半が黄色っぽい。")
R("umiichigo", "octocorallia", "ウミイチゴ", "Eleutherobia rubra", "赤いイチゴのような形をした八放サンゴの仲間。")
R("kaginotekurage", "hydrozoa", "カギノテクラゲ", "Gonionemus vertens", "触手の途中が鉤のように曲がる小さなクラゲ。アマモ場などにすみ、刺されると強く痛む。")
R("kikumeishimodoki", "scleractinia", "キクメイシモドキ", "Oulastrea crispata", "小さな群体をつくるイシサンゴ。温帯の浅い海や内湾でも見られる。")
R("sanshouuni", "echinoidea", "サンショウウニ", "Temnopleurus toreumaticus", "内湾の砂泥底にすむ小型のウニ。")
for _id, _t in {"kumanoashitsuki": 4, "samidorisashiba": 4, "sanhachiurokomushi": 4, "kuroshitanashiumiushi": 3,
                "akaeraminoumiushi": 3, "dainanginpo": 3, "nabeka": 3, "umiichigo": 3, "kaginotekurage": 3,
                "kikumeishimodoki": 4, "sanshouuni": 3}.items():
    _find(_id)["tier"] = _t
# 作者の指定（2026-10-27）。照合はゲキムズ用の結果（check/hard_inv/result.json）と check/picks18/。
edit("asahigani", fact="甲羅が縦に長く、朱色をしたカニ。ふつうのカニのような横歩きはできず前後に歩くが、前にはほとんど進まない。砂に潜ってすむ。食用にされる。")
R("kaiyadoriumigumo", "chelicerata", "カイヤドリウミグモ", "Nymphonella tapetis", "アサリなどの二枚貝の中に寄生するウミグモ。各地で増えてアサリ漁に被害を出した。")
R("ryuujinoomukade", "chilopoda", "リュウジンオオムカデ", "Scolopendra alcyona", "2021年に新種として記載された、琉球列島と台湾の大型のムカデ。水に入って泳ぎ、水辺の生き物も食べる。")
R("sashihariari", "formicidae", "サシハリアリ", "Paraponera clavata", "中南米の熱帯林にすむ大型のアリ。刺されると非常に強い痛みが続く。", ["パラポネラ"],
  v={"ja": "和名の出典は Wikidata のみ"})
R("ootsunohiramushi", "polycladida", "オオツノヒラムシ", "Planocera multitentaculata", "日本の磯の石の下でよく見られる大型のヒラムシ。")
R("minohiramushi", "polycladida", "ミノヒラムシ", "Thysanozoon brocchii", "背中一面に小さな突起が生えたヒラムシ。体を波打たせて泳ぐこともできる。")
R("chigokemushi", "bryozoa", "チゴケムシ", "Watersipora subatra", "港の岸壁や船底に付着し、赤黒い板状の群体をつくるコケムシ。")
R("tagayasanminashi", "caenogastropoda", "タガヤサンミナシ", "Conus textile", "イモガイの一種。網目模様の殻をもつ。毒のある銛のような歯舌で獲物を刺し、人も刺されると危険。")
R("ashihidanamekuji", "heterobranchia", "アシヒダナメクジ", "Laevicaulis alte", "殻のない陸の貝で、足の両側にひだがある。外来種で、南西諸島などに定着している。")
R("mimiika", "decapodiformes", "ミミイカ", "Euprymna morsei", "耳のようなひれをもつ小さなイカ。昼は砂に潜って過ごす。")
for _id, _t in {"kaiyadoriumigumo": 4, "ryuujinoomukade": 4, "sashihariari": 3, "ootsunohiramushi": 4, "minohiramushi": 4,
                "chigokemushi": 4, "tagayasanminashi": 3, "ashihidanamekuji": 3, "mimiika": 3}.items():
    _find(_id)["tier"] = _t
META["datasetVersion"] = "0.3.10"  # 一覧ページの案（知名度・本家とゲキムズの振り分け）
