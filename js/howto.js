// 遊び方の例題の自動再生
"use strict";
// ---- 遊び方（例題の自動再生）----
const DEMO = { target: "kabutomushi", guesses: ["hito", "madako", "zuwaigani", "monshirocho", "kabutomushi"],
  // 各段階で「次に何を入れるか」の考え方
  think: [
    "💭 まずは遠い動物で、大きく分けよう。",
    "💭 ヒトの仲間ではない。反対側の枝のタコはどうだ？",
    "💭 タコでもない。種の多い節足動物、カニはどうだ？",
    "💭 カニでもない。同じ汎甲殻類の昆虫、チョウは？",
    "💭 さなぎになる昆虫まで来た。甲虫のカブトムシだ！",
    "💭 遠くで分けて、緑の点の中で別の枝を選ぶのがコツ。"] };
let demoI = 0, demoTimer = null, demoPrevI = -1, demoEdges = null;
function howtoHTML() {
  return (HARD() ? hardHowto() : "") + `<section><h2>遊び方は3つだけ</h2><ol class="steps">
    <li><b>動物を入れる</b><span>答えの動物との共通の祖先がわかり、系統樹に枝が増えます。</span></li>
    <li><b>緑の点の中を探す</b><span>答えの動物は緑の点より先にいます。その中の、まだ試していない仲間を入れます。</span></li>
    <li><b>${MAX} 回以内に当てる</b><span>${HINT1} 回目と ${HINT2} 回目のあとにヒントが使えます。</span></li></ol>
    <div class="legend"><span><i class="lg-dot"></i>答えの動物がいる範囲</span><span><i class="lg-on"></i>答えへの道</span><span><i class="lg-goal"></i><b>？</b> 答えの動物</span><span>名前を押すと説明</span></div></section>
  <details class="doc-more"><summary>くわしいルール</summary><ul>
    <li>名前はひらがな・カタカナ・学名・別名のどれでも探せます。</li>
    <li>左端が動物全体の祖先で、右へ行くほど細かい仲間です。右端の番号は入れた順です。</li>
    <li>「新しい手がかりはありません」は、緑の点より外側の動物を入れたということです。</li>
    <li>ヒント1は残りの候補の数、ヒント2は一歩先の節目です。ヒントを使っても回数は減りません。</li>
    <li>「今日の動物」は日本時間で毎日変わり、誰でも同じ問題です。「フリー」は何度でも遊べます。</li>
    <li>系統樹の節目（分類群）は、すべてクレード（ある祖先とその子孫すべてからなる単系統群）です。魚類や爬虫類のような、子孫の一部を除いたまとまりは使っていません。</li>
    <li><span class="poly">多分岐</span>は系統関係が議論中で、分岐の順を決めていない節目です。</li></ul></details>`;
}
function hardHowto() {
  const s = D.meta.selection;
  return `<section class="hard-rule"><h2>ゲキムズモード（試作）</h2><ul>
    <li>ふつうモードの動物に、日本の魚類・爬虫類・両生類と海の無脊椎動物${(D.meta.counts || {}).land ? "、陸の昆虫・クモ・鳥・貝" : ""}などを加えた ${SP.length.toLocaleString()} 種から出題します。推測にも全種が使えます。</li>
    <li>答えと<b>同じ属</b>の種を入れたらクリア（✅）です。答えの種名はまだ出ないので、続けて種まで当てると 🎯、終えるときは「答えを見る」を押します。成績は属を当てた回数で記録し、種まで当てた回数も残します。</li>
    <li>推測は ${MAX} 回まで。属でクリアしたあとは、それとは別に<b>種探しが ${HUNT} 回</b>あり、その属にあと何種いるかも出ます。</li>
    <li>ヒント1は ふつうモードと同じです。ヒント2は科より下の節目は開かず、代わりに和名の手がかり（文字数と終わり方）を出します。</li>
    <li>和名のない属や科は学名で表示します。</li></ul></section>`;
}
function demoShow(i, typing) {
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
