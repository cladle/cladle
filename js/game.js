// ゲームの進行：推測の判定・成績・計測・ヒント
"use strict";
// ---- ゲーム状態 ----
let G = null, mode = "daily";
function newGame(m, code) {
  const c = m === "shared" ? shareDecode(code) : null;
  if (m === "shared" && N[c?.t]?.kind !== "species") { newGame("free"); flash("この共有リンクの動物は、今のデータでは開けませんでした（リンクが途中で切れているか、収録種が変わった可能性があります）。", true); return; }
  if (m !== "shared" && G?.code && /^#((hard|fish)\/)?p=/.test(location.hash)) history.replaceState(null, "", location.pathname + location.search + (BIG() ? "#" + LEVEL : ""));  // 共有された問題から離れたらリンクの印を消す
  mode = m; $("#flash").hidden = true;  // 前のモードの「新しい手がかりはありません」などを残さない
  if (m === "shared") {
    const saved = store.get(KEY("dk-shared"));
    G = saved && saved.code === code ? saved : { code, from: c, target: c.t, guesses: [], done: false, won: false };
  } else if (m === "daily") {
    if (due(D)) { location.reload(); return; }  // 開いたまま次の版の日になった
    const day = todayJST(), saved = store.get(KEY("dk-daily"));
    const target = pick(mulberry(hash("metazoa-ja:" + day + ":" + D.meta.datasetVersion)));
    G = saved && saved.day === day && saved.target === target ? saved : { day, target, guesses: [], done: false, won: false };
  } else {
    const saved = store.get(KEY("dk-free"));
    G = saved && N[saved.target] ? saved : { target: pick(Math.random), guesses: [], done: false, won: false };
  }
  G.guesses = G.guesses.filter(id => N[id]); if (G.reveal && !N[G.reveal]) delete G.reveal;  // データから外れた種・節目
  if (!G.done && G.guesses.length >= limit()) { G.done = true; if (G.gAt) { G.won = true; G.exact = false; } }  // 上限を下げる前の記録
  lastEdges = null; openGrow = G.guesses.length > 0;  // 開いたときは今の木を根元から手早く伸ばす
  G.fresh = null;
  if (m === "daily" && G.done && !STATS.days[G.day]) save();  // 成績を付ける前に解いた日の分
  render();
}
function save() {
  store.set(KEY({ daily: "dk-daily", free: "dk-free", shared: "dk-shared" }[mode]), { ...G, fresh: null });
  if (mode !== "daily") return;
  if (G.done || G.gAt) STATS.days[G.day] = { w: G.won || G.gAt ? 1 : 0, n: G.gAt || G.guesses.length, h: (G.h1 ? 1 : 0) + (G.h2 ? 1 : 0), ...(G.gAt && !G.exact ? { g: 1 } : {}), ...(G.gAt && G.exact ? { s: G.guesses.length - G.gAt } : {}) };
  saveStats();
}
// ---- 成績（今日の動物だけ数える）----
// このブラウザに保存する（別の端末とは共有されない）
let STATS = { days: {} };
mergeStats(store.get(KEY("dk-stats")));
function mergeStats(x) { if (x && x.days) for (const [d, r] of Object.entries(x.days)) if (!STATS.days[d]) STATS.days[d] = r; }
function saveStats() {
  store.set(KEY("dk-stats"), STATS);
}
function prevDay(d) { return new Date(Date.parse(d) - 864e5).toISOString().slice(0, 10); }
function statsSummary() {
  const days = STATS.days, keys = Object.keys(days).sort(), played = keys.length, wins = keys.filter(k => days[k].w).length;
  const dist = Array(MAX + 1).fill(0); let lost = 0;
  for (const k of keys) days[k].w ? dist[Math.min(days[k].n, MAX)]++ : lost++;
  let cur = 0, d = todayJST(); if (!days[d]) d = prevDay(d);
  while (days[d]?.w) { cur++; d = prevDay(d); }
  let best = 0, run = 0, prev = null;
  for (const k of keys) { run = !days[k].w ? 0 : prev === prevDay(k) ? run + 1 : 1; best = Math.max(best, run); prev = k; }
  return { played, wins, rate: played ? Math.round(wins / played * 100) : 0, cur, best, dist, lost };
}
function statsHTML() {
  const t = statsSummary(), today = STATS.days[todayJST()], top = Math.max(1, ...t.dist, t.lost);
  const bar = (label, v, mine) => `<div class="bar"><span>${label}</span><i style="width:${Math.max(6, v / top * 100)}%" class="${mine ? "me" : ""}">${v}</i></div>`;
  return `<div class="stats"><span class="eyebrow">今日の動物の成績</span>
    <div class="nums"><div><b>${t.played}</b><small>プレイ</small></div><div><b>${t.rate}%</b><small>正解率</small></div><div><b>${t.cur}</b><small>連続正解</small></div><div><b>${t.best}</b><small>最長連続</small></div></div>
    <div class="dist">${t.dist.map((v, i) => i ? bar(i, v, today?.w && today.n === i) : "").join("")}${bar("×", t.lost, today && !today.w)}</div>
    <div class="cd">次の問題まで <b id="countdown">${countdown()}</b></div></div>`;
}
function countdown() {
  const now = Date.now() + 9 * 3600e3, left = 864e5 - now % 864e5;
  const h = Math.floor(left / 3600e3), m = Math.floor(left / 60e3) % 60, sec = Math.floor(left / 1e3) % 60;
  return `${h}:${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")}`;
}
setInterval(() => {
  const c = document.getElementById("countdown"); if (!c) return;
  c.textContent = countdown();
  if (mode === "daily" && G?.day && G.day !== todayJST() && (view === "daily")) newGame("daily");  // 日付が変わったら次の問題へ
}, 1000);

// プレイ回数を数える（GoatCounter の出来事として送る。読み込めていなければ何もしない）
const TRACK = { "tab-daily": "タブ：今日の動物", "tab-free": "タブ：フリー", "tab-zukan": "タブ：図鑑", "tab-howto": "タブ：遊び方", "tab-about": "タブ：データ", "zukan-search": "図鑑：検索", "zukan-from-result": "図鑑：結果から開く", "sheet-clade": "詳細：分類群を開く", "sheet-species": "詳細：種を開く", "lookup-wikipedia": "調べる：Wikipedia", "lookup-gbif": "調べる：GBIF", "lookup-image": "調べる：画像検索", "daily-genus": "今日の動物：属でクリア", "free-genus": "フリー：属でクリア", "daily-genusend": "今日の動物：属どまりで終了", "free-genusend": "フリー：属どまりで終了", "daily-reveal": "今日の動物：答えを見る", "free-reveal": "フリー：答えを見る", "daily-hint1": "今日の動物：ヒント1", "daily-hint2": "今日の動物：ヒント2", "free-hint1": "フリー：ヒント1", "free-hint2": "フリー：ヒント2", "free-reset": "フリー：別の問題にする", "level-hard": "ゲキムズに切り替え", "level-fish": "魚編に切り替え", "daily-share-x": "今日の動物：Xでポスト", "free-share-x": "フリー：Xでポスト", "shared-start": "共有された問題：開始", "shared-win": "共有された問題：正解", "shared-lose": "共有された問題：終了（不正解）", "shared-giveup": "共有された問題：降参", "shared-share": "共有された問題：共有", "shared-share-x": "共有された問題：Xでポスト", "shared-genus": "共有された問題：属でクリア", "daily-share": "今日の動物：共有", "free-share": "フリー：共有", "share-visit": "共有から来た人", "daily-giveup": "今日の動物：降参", "free-giveup": "フリー：降参", "daily-start": "今日の動物：開始", "daily-win": "今日の動物：正解", "daily-lose": "今日の動物：終了（不正解）", "free-start": "フリー：開始", "free-win": "フリー：正解", "free-lose": "フリー：終了（不正解）" };
let zkSearched = false;
function track(ev) { const h = typeof BIG === "function" && BIG() && ev !== "share-visit"; try { window.goatcounter?.count?.({ path: (h ? LEVEL + "-" : "") + ev, title: (h ? LV_NAME[LEVEL] + " " : "") + (TRACK[ev] || ev), event: true }); } catch (e) {} }
if (new URLSearchParams(location.search).get("from") === "share") {
  try { history.replaceState(null, "", location.pathname + location.hash); } catch (e) {}
  let n = 0; const t = setInterval(() => { if (window.goatcounter?.count || ++n > 20) { clearInterval(t); track("share-visit"); } }, 500);
}
function guess(id) {
  if (G.done || G.guesses.includes(id)) return;
  const before = deepest();
  G.guesses.push(id);
  if (G.guesses.length === 1) track(mode + "-start");
  const L = lca(id, G.target);
  growId = id;
  if (id === G.target) { G.done = G.won = true; G.exact = true; celebrate = true; $("#flash").hidden = true; }
  else {
    const gained = N[L].depth > N[before].depth;
    // ゲキムズ：属が当たったらクリア（種名は伏せたまま。続けて種を当てるか、答えを見るかを選べる）
    if (!G.gAt && sameClear(id, G.target)) { G.gAt = G.guesses.length; track(mode + "-genus"); flash(`同じ属です！ ${G.gAt} 回でクリア。ここから種探し ${HUNT} 回で種まで当てると 🎯。終えるときは「答えを見る」。`); G.fresh = L; }
    else flash(`${N[id].ja} と答えの動物の共通祖先は「${N[L].ja}」。` + (gained ? "系統が絞れました。" : "新しい手がかりはありません。"), !gained);
    if (G.gAt !== G.guesses.length) G.fresh = gained ? L : null;
    if (G.guesses.length >= limit()) { G.done = true; if (G.gAt) { G.won = true; G.exact = false; } }
  }
  if (G.done) track(mode + (!G.won ? "-lose" : G.exact === false ? "-genusend" : "-win"));  // ゲキムズで属を当てたまま上限まで使ったら属どまり
  save(); render();
  if (!G.won) cueTo(id, L);
}
// 推測した動物と、答えの動物との分かれ目が画面に入るように、系統樹の方へ動かす（見る場所の案内）
// スマホはキーボードが閉じて画面の高さが戻るのを少し待つ。もう見えていれば動かさない
function cueTo(id, L) {
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  setTimeout(() => {
    const a = $(`#board text.tl[data-id="${id}"]`), b = $(`#board .nd[data-id="${L}"]`) || a;
    if (!a) return;
    const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
    const top = Math.min(ra.top, rb.top), bot = Math.max(ra.bottom, rb.bottom), vh = visualViewport?.height || innerHeight;
    if (top >= 70 && bot <= vh - 30) return;
    scrollBy({ top: (top + bot) / 2 - vh / 2, behavior: still ? "auto" : "smooth" });
  }, matchMedia("(pointer: coarse)").matches ? 300 : 0);
}
let celebrate = false, growId = null, lastEdges = null, openGrow = false, animUntil = 0;  // 正解した直後の演出、推測した直後に伸ばす枝、前回描いた枝
function deepest() { return deepestOf(G.target, G.guesses, G.reveal); }
// ゲキムズ：答えと同じ属の種を入れたらクリア（種まで同じならぴったり正解）
function sameClear(a, b) { const r = D.meta.selection?.clearRank; return !!r && N[a].parent === N[b].parent && N[N[b].parent].rank === r; }
const exactWin = () => G.won && G.exact !== false;
const clearN = () => G.gAt || G.guesses.length;  // クリアした回数（ゲキムズは属が当たった回）
// ---- ヒント（推測回数は減らない）----
// ヒント1: 今わかっている節目の中で、どの推測とも矛盾しない未推測の種の数。外れた枝を灰色にする
// ヒント2: 正解への経路で、今わかっている節目より1段深い節目を教える
function candidates() {
  const k = deepest(), out = [];
  for (const s of SP) {
    if (s.answerable === false || G.guesses.includes(s.id) || !path(s.id).includes(k)) continue;
    if (G.guesses.every(g => lca(g, s.id) === lca(g, G.target))) out.push(s.id);
  }
  return out;
}
function useHint(n) {
  if (G.done) return;
  if (n === 1 && G.guesses.length >= HINT1 && !G.h1) { G.h1 = true; track(mode + "-hint1"); }
  if (n === 2 && G.guesses.length >= HINT2) {
    if (!G.h2) track(mode + "-hint2");
    const p = path(G.target), next = p[p.indexOf(deepest()) + 1];
    if (next && next !== G.target && !(BIG() && N[next].rank === "属")) G.reveal = next;
    G.h2 = true;
  }
  save(); render();
}
// ゲキムズのヒント2（属を開かないとき）：和名の文字数と、ほかの種とも共通する終わり方（「…ウロコムシ」など）
function jaClue(id) {
  const ja = N[id].ja; let suf = "";
  for (let k = ja.length - 2; k >= 2 && !suf; k--) { const t = ja.slice(-k); if (SP.filter(s => s.id !== id && s.ja.endsWith(t)).length >= 3) suf = t; }
  return `和名は ${ja.length} 文字` + (suf ? `で、「…${suf}」で終わります。` : `で、「${ja[0]}…」で始まります。`);
}
// 豆知識から正解の名前（和名・別名・学名）を伏せる
function maskFact(id) {
  const s = N[id]; let t = s.fact || "";
  for (const w of [s.ja, ...(s.aliases || []), s.sci, s.sci.split(" ")[0], ...(s.sciSynonyms || []).flatMap(x => [x, x.split(" ")[0]])].filter(w => w && w.length > 1).sort((a, b) => b.length - a.length)) t = t.split(w).join("〇〇");
  return t;
}
// 降参・別の問題（押し間違いで消えないよう、2回押して決める）
function actionsHTML() {
  if (G.done) return mode === "free" ? `<button class="btn" data-act="next">次の問題</button>` : "";
  return (mode === "free" ? `<button class="btn ghost" data-act="reset">別の問題にする</button>` : "")
    + (G.gAt ? `<button class="btn ghost" data-act="reveal">答えを見る</button>` : G.guesses.length ? `<button class="btn ghost" data-act="giveup">降参する</button>` : "");
}
