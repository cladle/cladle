// 遊び方の例題の自動再生
"use strict";
// ---- 遊び方（例題の自動再生）----
// 種は学名で書き、開いているデータの中から探す（ゲキムズは ふつうモードと同じ例題を使う）
const DEMOS = { normal: { target: "Trypoxylus dichotomus", guesses: ["Homo sapiens", "Octopus sinensis", "Chionoecetes opilio", "Pieris rapae", "Trypoxylus dichotomus"],
  // 各段階で「次に何を入れるか」の考え方
  think: [
    "💭 まずは遠い動物で、大きく分けよう。",
    "💭 ヒトの仲間ではない。反対側の枝のタコはどうだ？",
    "💭 タコでもない。種の多い節足動物、カニはどうだ？",
    "💭 カニでもない。同じ汎甲殻類の昆虫、チョウは？",
    "💭 さなぎになる昆虫まで来た。甲虫のカブトムシだ！",
    "💭 遠くで分けて、緑の点の中で別の枝を選ぶのがコツ。"] },
  fish: { target: "Sebastiscus marmoratus", guesses: ["Carcharodon carcharias", "Sardinops melanostictus", "Trachurus japonicus", "Pagrus major", "Chelidonichthys spinosus", "Sebastiscus marmoratus"],
  think: [
    "💭 まずは遠い魚で、大きく分けよう。サメはどうだ？",
    "💭 サメの仲間ではない。硬い骨の魚、イワシはどうだ？",
    "💭 イワシとも別の枝。ひれにとげのある魚、アジは？",
    "💭 スズキ系まで絞れた。タイの仲間、マダイは？",
    "💭 マダイと同じ Eupercaria の中。ホウボウはどうだ？",
    "💭 ペルカ目まで来た。同じ目で、岩場にすむカサゴだ！",
    "💭 遠くで分けて、緑の点の中で別の枝を選ぶのがコツ。"] },
  bird: { target: "Zosterops japonicus", guesses: ["Struthio camelus", "Anas platyrhynchos", "Larus crassirostris", "Astur gentilis", "Corvus macrorhynchos", "Zosterops japonicus"],
  think: [
    "💭 まずは遠い鳥で、大きく分けよう。飛べないダチョウはどうだ？",
    "💭 ダチョウの仲間ではない。新顎類の中の、カモはどうだ？",
    "💭 カモの仲間でもない。新鳥類の中の、ウミネコは？",
    "💭 カモメとも別の枝。タカやスズメの仲間、オオタカはどうだ？",
    "💭 Telluraves まで来た。種の多いスズメ目の、カラスは？",
    "💭 スズメ目の中。小さくて目のまわりが白い、メジロだ！",
    "💭 遠くで分けて、緑の点の中で別の枝を選ぶのがコツ。"] } };
let DEMO = null;
function demoData() {
  const d = DEMOS[LEVEL] || DEMOS.normal, id = sci => SP.find(s => s.sci === sci)?.id;
  return { target: id(d.target), guesses: d.guesses.map(id).filter(Boolean), think: d.think };
}
let demoI = 0, demoTimer = null, demoPrevI = -1, demoEdges = null;
function howtoHTML() {
  return (HARD() ? hardHowto() : FISH() ? fishHowto() : BIRD() ? birdHowto() : "") + `<section><h2>遊び方は3つだけ</h2><ol class="steps">
    <li><b>動物を入れる</b><span>答えの動物との共通の祖先がわかり、系統樹に枝が増えます。</span></li>
    <li><b>緑の点の中を探す</b><span>答えの動物は緑の点より先にいます。その中の、まだ試していない仲間を入れます。</span></li>
    <li><b>${MAX} 回以内に当てる</b><span>${HINT1} 回目と ${HINT2} 回目のあとにヒントが使えます。</span></li></ol>
    <div class="legend"><span><i class="lg-dot"></i>答えの動物がいる範囲</span><span><i class="lg-on"></i>答えへの道</span><span><i class="lg-goal"></i><b>？</b> 答えの動物</span><span>名前を押すと説明</span></div></section>
  <details class="doc-more"><summary>くわしいルール</summary><ul>
    <li>名前はひらがな・カタカナ・学名・別名のどれでも探せます。</li>
    <li>左端が${FISH() ? "脊椎動物" : BIRD() ? "鳥" : "動物全体"}の祖先で、右へ行くほど細かい仲間です。右端の番号は入れた順です。</li>
    <li>「新しい手がかりはありません」は、緑の点より外側の動物を入れたということです。</li>
    <li>1回目のヒントは残りの候補の数、2回目は一歩先の節目です。ヒントを使っても回数は減りません。</li>
    <li>「今日の動物」は日本時間で毎日変わり、誰でも同じ問題です。「フリー」は何度でも遊べます。</li>
    <li>系統樹の節目（分類群）は、すべてクレード（ある祖先とその子孫すべてからなる単系統群）です。魚類や爬虫類のような、子孫の一部を除いたまとまりは使っていません。</li>
    <li><span class="poly">多分岐</span>は系統関係が議論中で、分岐の順を決めていない節目です。</li></ul></details>`;
}
function fishHowto() {
  return `<section class="hard-rule"><h2>魚編（試作）</h2><ul>
    <li>魚類 ${SP.length.toLocaleString()} 種から出題します。日本産魚類全種目録に標準和名のある種に、和名が確かめられた外国の魚（シーラカンス・ハイギョ・ゼブラフィッシュなど）を加えています。推測にも全種が使え、どの種も同じ確率で出ます。</li>
    <li>「魚類」は、四肢動物を除いた残りのまとまり（側系統群）なので、節目にはしていません。系統樹の左端は脊椎動物の祖先で、円口類（ヌタウナギ・ヤツメウナギ）、軟骨魚類（サメ・エイ・ギンザメ）、条鰭類、肉鰭類（シーラカンス・ハイギョ）に分かれます。</li>
    <li>推測は ${MAX} 回まで。種まで当てたら正解です。</li>
    <li>1回目のヒントはふつうモードと同じです。2回目は、答えへの道で今より一段先の節目を教えます。一段先が属のときは属を開かず、代わりに和名の手がかり（文字数と終わり方）を出します。</li>
    <li>和名のない属は学名で表示します。</li></ul></section>`;
}
function birdHowto() {
  return `<section class="hard-rule"><h2>鳥編（試作）</h2><ul>
    <li>日本の鳥を中心に ${SP.length.toLocaleString()} 種から出題します。日本の鳥は日本鳥類目録改訂第8版に載っている種（外来種を含む）で、ほかにふつうモードのダチョウ・ペンギンなど外国の鳥を入れています。推測にも全種が使え、どの種も同じ確率で出ます。</li>
    <li>系統樹の左端は鳥の祖先で、ダチョウなどの古顎類と、それ以外の新顎類に分かれます。目・科・属は日本鳥類目録に従っています。新鳥類の中の目どうしの分岐の順は、研究によって結果が割れるので決めていません。</li>
    <li>推測は ${MAX} 回まで。種まで当てたら正解です。</li>
    <li>ヒント1はふつうモードと同じです。ヒント2は、答えへの道で今より一段先の節目を教えます。一段先が属のときは属を開かず、代わりに和名の手がかり（文字数と終わり方）を出します。</li>
    <li>和名のない属は学名で表示します。</li></ul></section>`;
}
function hardHowto() {
  const s = D.meta.selection;
  return `<section class="hard-rule"><h2>ゲキムズモード（試作）</h2><ul>
    <li>ふつうモードの動物に、日本の魚類・爬虫類・両生類と海の無脊椎動物${(D.meta.counts || {}).land ? "、陸の昆虫・クモ・鳥・貝" : ""}などを加えた ${SP.length.toLocaleString()} 種から出題します。推測にも全種が使えます。</li>
    <li>答えと<b>同じ属</b>の種を入れたらクリア（✅）です。答えの種名はまだ出ないので、続けて種まで当てると 🎯、終えるときは「答えを見る」を押します。成績は属を当てた回数で記録し、種まで当てた回数も残します。</li>
    <li>推測は ${MAX} 回まで。属でクリアしたあとは、それとは別に<b>種探しが ${HUNT} 回</b>あり、その属にあと何種いるかも出ます。</li>
    <li>1回目のヒントはふつうモードと同じです。2回目は、答えへの道で今より一段先の節目を教えます。一段先が属のときは属を開かず、代わりに和名の手がかり（文字数と終わり方）を出します。</li>
    <li>和名のない属や科は学名で表示します。</li></ul></section>`;
}
function demoShow(i, typing) {
  if (!DEMO || DEMO.level !== LEVEL) { DEMO = demoData(); DEMO.level = LEVEL; demoEdges = null; demoPrevI = -1; }
  const t = DEMO.target, gs = DEMO.guesses.filter(g => N[g]), n = gs.length;
  demoI = Math.max(0, Math.min(i, n));
  const done = gs.slice(0, demoI), last = done[done.length - 1];
  $("#demoStep").textContent = demoI ? `${demoI} 回目` : "スタート";
  const before = deepestOf(t, done.slice(0, -1)), now = deepestOf(t, done);
  let cap;
  if (!demoI) cap = `答えの動物は伏せられています（この例では ${N[t].ja}）。まず思いついた動物を入れてみます。`;
  else if (last === t) cap = `「${N[t].ja}」で正解。${demoI} 回でたどり着きました。`;
  else cap = `「${N[last].ja}」と答えの動物の共通祖先は「${N[lca(last, t)].ja}」。` + (N[now].depth > N[before].depth ? "答えの動物はこの節目の中にいると絞れました。" : "新しい手がかりはありません。");
  $("#demoCap").textContent = cap;
  $("#demoThink").textContent = DEMO.think[demoI] || "";
  const fwd = demoI === demoPrevI + 1 && demoEdges;
  $("#demoBoard").innerHTML = treeHTML(t, done, last === t, now !== before ? now : null, $("#demoBoard").clientWidth, { demo: true, win: fwd && last === t, grow: fwd ? { id: last, prev: last === t ? new Set() : demoEdges } : null });
  demoEdges = treeHTML.edges; demoPrevI = demoI;
  $("#demoPrev").disabled = demoI === 0; $("#demoNext").disabled = demoI === n;
  const next = gs[demoI];
  const typed = $("#demoTyped");
  if (typing && next) {
    const word = N[next].ja.replace(/[ァ-ヶ]/g, c => String.fromCharCode(c.charCodeAt(0) - 0x60));
    let k = 0; typed.textContent = "";
    const step = () => { if (view !== "howto") return; typed.textContent = word.slice(0, ++k); if (k < word.length) demoTimer = setTimeout(step, 140); else demoTimer = setTimeout(() => demoShow(demoI + 1, true), 900); };
    // 説明と💭を読み終えられるだけ待ってから次を打ち始める（1文字およそ0.1秒）
    demoTimer = setTimeout(step, Math.max(3000, treeHTML.animEnd * 1000 + 1500, 1200 + (cap.length + (DEMO.think[demoI] || "").length) * 100));
  } else typed.textContent = next ? "" : "";
}
function demoStop() { clearTimeout(demoTimer); demoTimer = null; }
function demoPlay() { demoStop(); demoShow(0, !matchMedia("(prefers-reduced-motion: reduce)").matches); }
