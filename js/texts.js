// 画面の説明文：データ欄・遊び方の文章
"use strict";
// ---- 説明 ----
function hardAboutHTML() {
  const a = (u, t) => `<a href="${u}" target="_blank" rel="noopener noreferrer">${t}</a>`, k = D.meta.counts || {}, f = n => (n || 0).toLocaleString();
  return `  <section><h2>ゲキムズモードについて</h2><ul>
    <li>試作版です。ふつうモードの ${f(k.main)} 種に、標準和名のある日本産の魚類・爬虫類・両生類 ${f(k.fishherp)} 種と、${k.worms ? `Catalogue of Life と WoRMS に日本語名がある無脊椎動物 ${f(k.col + k.worms + (k.extra || 0))}` : `Catalogue of Life に日本語名がある無脊椎動物 ${f(k.col)}`} 種${k.land ? `、陸の昆虫・クモ・鳥・哺乳類と陸や淡水の貝 ${f(k.land)} 種` : ""}を加えています（重なる種は一つにまとめています）。</li>
    <li>Catalogue of Life 由来の和名は、ほとんどが BISMaL（海洋生物多様性情報システム）からのものです。ワラジムシ類とタナイス類は研究者の種リストと、学名と科は WoRMS と照合して直しました。そのほかの和名は BISMaL だけが出典で、iNaturalist などと食い違うものには「要確認」の印を付けています。コガネムシ上科の昆虫は、日本産昆虫目録とは照合できておらず、和名の出典は記録の論文です。</li>${k.worms ? `
    <li>Catalogue of Life に日本語名の無いエビ・ヤドカリ類などは、WoRMS の日本語名（同じく BISMaL 由来）から足しました。Catalogue of Life と和名が食い違うものと、一つの和名に学名が複数あるものは入れていません。</li>` : ""}
${k.land ? `
    <li>陸の生き物は、環境省の「種の多様性調査 対象種一覧」（昆虫のトンボ・チョウ・セミと水生半翅類・ガ・甲虫、陸と淡水の貝、鳥、哺乳類）と Japan Spider Catalog（クモ）から足しました。学名は Catalogue of Life に合わせ、鳥と哺乳類は日本鳥類目録改訂第8版・世界哺乳類標準和名リストにある種だけを、そのリストの和名で入れています。環境省の一覧は1997年のもので、iNaturalist と和名が食い違うものには「要確認」の印を付けています。</li>` : ""}
    <li>系統は、ふつうモードの節目を骨組みにし、その下に目録・リスト・Catalogue of Life${k.worms ? "・WoRMS" : ""} の分類（目・科・属など）をつなげています。側系統群とされる群（多毛綱、甲殻亜門、トカゲ亜目など）は節目にしていません。どこに入るか決めていない群は、上の節目の下にまとめて置いています。</li>
    <li>和名のない属や科は学名で表示しています。</li>
    <li>誤りに気づいたら ${a("https://github.com/cladle/cladle/issues", "GitHub の Issues")} へお寄せください。</li></ul></section>
  <section><h2>出典</h2><ul>
    <li>魚類：本村浩之．2026．日本産魚類全種目録．これまでに記録された日本産魚類全種の現在の標準和名と学名．Online ver. 42（2026-08-27）．${a("https://www.museum.kagoshima-u.ac.jp/staff/motomura/jaf.html", "鹿児島大学総合研究博物館")}</li>
    <li>爬虫類・両生類：日本爬虫両棲類学会 (2026) 日本産爬虫両生類標準和名リスト（2026年7月2日版）. ${a("https://herpetology.jp/wamei/", "https://herpetology.jp/wamei/")} (2026年10月24日アクセス)</li>
    <li>無脊椎動物の日本語名・分類：Catalogue of Life Checklist（ChecklistBank 3LR、2026-10-14 版）. ${a("https://www.catalogueoflife.org/", "catalogueoflife.org")}（CC BY 4.0）。日本語名の多くは Japan Agency for Marine-Earth Science and Technology (2009) Biological Information System for Marine Life (BISMaL) による</li>
    ${k.worms ? `<li>無脊椎動物の日本語名・分類（追加分）：WoRMS Editorial Board. World Register of Marine Species（ChecklistBank 2011）. ${a("https://www.marinespecies.org/", "marinespecies.org")}（CC BY 4.0、2026-10-25 参照）。日本語名は BISMaL による</li>` : ""}
${k.land ? `<li>陸の昆虫・貝・鳥・哺乳類の対象種：環境省自然環境局生物多様性センター「種の多様性調査（動物分布調査）対象種一覧」（${a("https://www.biodic.go.jp/", "biodic.go.jp")}、公共データ利用規約 第1.0版）を加工して作成（学名を Catalogue of Life に合わせ、和名の一部を学会のリストに合わせた）</li>
    <li>クモ：Japan Spider Catalog. (2026). Japan Spider Catalog（種リスト 2026-10-24 生成分）. ${a("https://japan-spider-catalog.pages.dev/", "https://japan-spider-catalog.pages.dev/")} (accessed 2026-10-25). 日本産クモ類目録（谷川 2026）に準拠。Cladle が加工して作成</li>
    <li>鳥類：日本鳥学会（2024）日本鳥類目録 改訂第8版（和名・学名リスト 2023-09-30 公開版）</li>
    <li>哺乳類：川田伸一郎ほか（2021）世界哺乳類標準和名リスト 2021年度版．${a("https://www.mammalogy.jp/list/index.html", "日本哺乳類学会")}</li>
    ` : ""}<li>無脊椎動物の照合：日本甲殻類学会ワラジムシ亜目研究グループ 日本産ワラジムシ亜目種リスト（${a("https://www.warajimushi.com/", "warajimushi.com")}）／角井敬知 日本近海産タナイス目リスト／WoRMS Editorial Board, World Register of Marine Species（${a("https://www.marinespecies.org/", "marinespecies.org")}、2026-10-24 参照）</li>
    ${(D.meta.japaneseNameSources || []).filter(x => x.startsWith("コガネムシ上科")).map(x => `<li>${esc(x)}</li>`).join("")}
    <li>魚類の目より上の系統：Betancur-R. et al. (2017) BMC Evol. Biol. 17:162 ／ Near &amp; Thacker (2024) Bull. Peabody Mus. Nat. Hist. 65:3–302</li>
    <li>ふつうモードの種と節目の出典は、ふつうモードのデータ欄を見てください。</li></ul></section>`;
}
// 番外編：ふつうモードとは別の、出題する範囲を決めたモード。足すときはここに1行
const EXTRA = [
  { lv: "fish", name: "魚編", note: "日本の魚を中心に約 4,800 種から出題。種まで当てれば正解。推測は 20 回まで。" },
];
function extraHTML() {
  return `<section><h2>番外編</h2><p>ふつうモードとは別に、決まった範囲の動物だけで遊ぶモードです。成績はふつうモードとは別に記録します。</p>
    <div class="modes">${EXTRA.map(m => `<button class="mode-card" data-mode="${m.lv}" aria-current="${LEVEL === m.lv}"><b>${esc(m.name)}（試作）</b><span>${esc(m.note)}</span></button>`).join("")}</div></section>`;
}
function fishAboutHTML() {
  const a = (u, t) => `<a href="${u}" target="_blank" rel="noopener noreferrer">${t}</a>`;
  return `  <section><h2>魚編について</h2><ul>
    <li>試作版です。ゲキムズモードのデータから、脊椎動物のうち四肢動物を除いた ${SP.length.toLocaleString()} 種を取り出しています。ほとんどは日本産魚類全種目録に標準和名のある日本の魚で、ほかにふつうモードのシーラカンス・ハイギョ・ゼブラフィッシュを含みます。</li>
    <li>系統は、目より上を魚類の分子系統の論文に、目・科を日本産魚類全種目録（Catalog of Fishes の体系）に従っています。側系統群は節目にしていません。</li>
    <li>和名のない属は学名で表示しています。</li>
    <li>誤りに気づいたら ${a("https://github.com/cladle/cladle/issues", "GitHub の Issues")} へお寄せください。</li></ul></section>
  <section><h2>出典</h2><ul>
    <li>本村浩之．2026．日本産魚類全種目録．これまでに記録された日本産魚類全種の現在の標準和名と学名．Online ver. 42（2026-08-27）．${a("https://www.museum.kagoshima-u.ac.jp/staff/motomura/jaf.html", "鹿児島大学総合研究博物館")}</li>
    <li>魚類の目より上の系統：Betancur-R. et al. (2017) BMC Evol. Biol. 17:162 ／ Near &amp; Thacker (2024) Bull. Peabody Mus. Nat. Hist. 65:3–302</li>
    <li>ふつうモードの種と節目の出典は、ふつうモードのデータ欄を見てください。</li></ul></section>
  <section><h2>ライセンス・注記</h2><ul>
    <li>成績はこの端末のブラウザにだけ保存され、送信されません。ふつうモード・ゲキムズとは別に記録します。</li></ul></section>`;
}
function aboutHTML() {
  if (HARD()) return hardAboutHTML();
  if (FISH()) return fishAboutHTML();
  const nv = SP.filter(s => s.verify).length;
  const a = (u, t) => `<a href="${u}" target="_blank" rel="noopener noreferrer">${t}</a>`;
  return `  <section><h2>このゲームについて</h2><ul>
    <li>作者が動物の系統を学ぶために、AI（Claude）を使って作った個人の試作版です。</li>
    <li>名前や系統に誤りがあるかもしれません。お気づきの点は ${a("https://github.com/cladle/cladle/issues", "GitHub の Issues")} へお寄せください。</li>
    <li>ゲームの形は ${a("https://metazooa.com/", "Metazooa")}（Trainwreck Labs）に着想を得ています。</li>
    <li>収録：${D.clades.filter(c => c.rank === "門").length} 門・${SP.length} 種（うち「要確認」${nv} 種）。系統は分子系統の論文を参考にし、位置が議論中のグループは多分岐で示しています。</li>
    <li>収録種は作者の気が向いたときに足したり、足さなかったりします。</li></ul></section>
  <section><h2>出典</h2><ul>
    <li>学名：GBIF Secretariat. GBIF Backbone Taxonomy. ${a("https://doi.org/10.15468/39omei", "doi:10.15468/39omei")}（CC BY 4.0）</li>
    <li>学名：Catalogue of Life Checklist. Catalogue of Life Foundation, Amsterdam. ${a("https://www.catalogueoflife.org/", "catalogueoflife.org")}（CC BY 4.0、2026-10-22 参照）</li>
    <li>学名：WoRMS Editorial Board (2026). World Register of Marine Species. ${a("https://doi.org/10.14284/170", "doi:10.14284/170")}（CC BY 4.0）</li>
    <li>魚類の標準和名・学名：本村浩之．2026．日本産魚類全種目録．これまでに記録された日本産魚類全種の現在の標準和名と学名．Online ver. 42．${a("https://www.museum.kagoshima-u.ac.jp/staff/motomura/jaf.html", "鹿児島大学総合研究博物館")}</li>
    <li>和名の照合：${a("https://www.wikidata.org/", "Wikidata")}（CC0）、${a("https://www.inaturalist.org/", "iNaturalist")}、GBIF</li>
    <li>系統：${a("https://tree.opentreeoflife.org/", "Open Tree of Life")}、${a("https://www.ncbi.nlm.nih.gov/taxonomy", "NCBI Taxonomy")}、各系統解析の論文</li>
    <li>節目の和名：遠藤広光（高知大学）動物分類体系／長谷川政美『すべての生き物をめぐる100の系統樹』／藤田敏彦（2010）『動物の系統分類と進化』／町田龍一郎ほか 科研費報告（25440201）／吉澤和徳（2016）昆蟲（ニューシリーズ）19(3)。文献で確かめられない節目は学名で表記しています。</li></ul></section>
  <section><h2>ライセンス・注記</h2><ul>
    <li>上の情報源のデータを丸ごと収録してはいません。名前は照合した結果を一つずつ記載しています。</li>
    <li>成績はこの端末のブラウザにだけ保存され、送信されません。ブラウザの履歴やサイトデータを消すと消え、別の端末には引き継がれません。</li></ul></section>`;
}
