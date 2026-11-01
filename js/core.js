// 共通の道具・データから系統樹を組み立てる・共通祖先（path / lca）
"use strict";
const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const store = {
  get(k) { try { return JSON.parse(localStorage.getItem(k)) } catch (e) { return null } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)) } catch (e) {} }
};

let D, N = {}, SP = [], BUCKETS = [], BW = [], MAX = 15;
// ゲキムズ・魚編・鳥編・昆虫編：別のデータ（data-hard.json・data-fish.json・data-bird.json・data-insect.json）に切り替える。成績・途中の問題はモードごとに別に保存する
let LEVEL = "normal";
const DATA = {};
const LV_FILE = { normal: "data.json", hard: "data-hard.json", fish: "data-fish.json", bird: "data-bird.json", insect: "data-insect.json" };
const LV_NAME = { normal: "", hard: "ゲキムズ", fish: "魚編", bird: "鳥編", insect: "昆虫編" };
const KEY = k => LEVEL === "normal" ? k : k.replace("dk-", `dk-${LEVEL}-`);
const HARD = () => LEVEL === "hard";
const FISH = () => LEVEL === "fish";
const BIRD = () => LEVEL === "bird";
const INSECT = () => LEVEL === "insect";
const BIG = () => LEVEL !== "normal";  // 種の多いデータ（補完の件数、ヒント2の出し方、図鑑の属・科の表示）
const HINT1 = 10, HINT2 = 13;  // この回数の推測のあとにヒントが押せる
const HUNT = 8;  // ゲキムズ：属でクリアしたあとの種探しの回数（残り回数とは別）
const limit = () => G.gAt ? G.gAt + HUNT : MAX;

// ---- 文字の正規化（カタカナ→ひらがな、全角半角、空白・中黒を除去）----
function norm(s) {
  s = String(s);
  // ASCII とふつうのカタカナだけなら NFKC は何も変えないので省く（ゲキムズの2万種で起動が重くならないように）
  return (/[^\u0020-\u007e\u30a1-\u30f6\u30fc\u30fb]/.test(s) ? s.normalize("NFKC") : s).toLowerCase()
    .replace(/[ァ-ヶ]/g, c => String.fromCharCode(c.charCodeAt(0) - 0x60))
    .replace(/[\s・･\-‐.]/g, "");
}

function build(data) {
  D = data; MAX = data.meta.selection?.maxGuesses || 15;
  for (const c of data.clades) N[c.id] = { ...c, kind: "clade", kids: [] };
  for (const s of data.species) { N[s.id] = { ...s, kind: "species", kids: [] }; SP.push(N[s.id]); }
  for (const n of Object.values(N)) if (n.parent) N[n.parent].kids.push(n.id);
  const walk = (id, d) => { const n = N[id]; n.depth = d; n.count = n.kind === "species" ? 1 : 0;
    for (const k of n.kids) { walk(k, d + 1); n.count += N[k].count; } };
  const root = data.clades.find(c => !c.parent).id; walk(root, 0); D.root = root;
  // 出題：まず枠（主要な門ごと＋その他の門）を等確率で選び、枠の中は門ごとに重みをつけて選ぶ
  // ゲキムズは枠を綱などの大きなまとまり、枠の中を目（bucketRank）で分ける
  const sel = data.meta.selection || {}, named = sel.buckets || [], rank = sel.bucketRank || "門";
  for (const s of SP) {
    const p = path(s.id);
    s.phylum = p.find(id => N[id].rank === rank);
    s.bucket = named.find(b => p.includes(b)) || "_other";
    makeKeys(s);
  }
  const byB = {};
  for (const s of SP) {
    if (s.answerable === false) continue;
    const b = s.bucket;
    ((byB[b] ||= {})[s.phylum] ||= []).push(s.id);
  }
  // 門の中では、知名度の低い種（tier が大きい種）を段階的に出にくくする
  const TW = sel.tierWeights || { 2: .9, 3: .8, 4: .7 }, tw = id => TW[N[id].tier] ?? 1;
  BUCKETS = Object.values(byB).map(ph => Object.values(ph).map(ids => {
    const x = { ids, w: sel.phylumWeight === "equal" ? 1 : Math.sqrt(ids.length) };
    if (ids.some(id => tw(id) !== 1)) { x.sw = ids.map(tw); x.st = x.sw.reduce((a, b) => a + b, 0); }
    return x;
  }));
  // 枠の選び方：既定は等確率。"sqrt" なら枠内の重みの合計の平方根に比例させる
  BW = BUCKETS.map(B => sel.bucketWeight === "sqrt" ? Math.sqrt(B.reduce((a, x) => a + (x.st ?? x.ids.length), 0)) : 1);
  if (sel.realCounts) byRealCounts(sel.realCounts, tw);
}
// 実際の種数で群を選ぶ（meta.selection.realCounts、tools/real_counts.py が数える）
// 収録数の多い・少ないに左右されないよう、群（ranks[0]、例：門・目）を実際の種数（top が "sqrt" ならその平方根）に比例して選び、
// 群の中は ranks[1]（例：綱）の実際の種数に比例して選ぶ。ranks[1] の無い種・数の無い群の種は「残り」にまとめ、
// 群の種数から中の群の種数を引いた数を重みにする。最後に、選んだまとまりの中から知名度の重みで種を選ぶ
function byRealCounts(rc, tw) {
  const [r0, r1] = rc.ranks, n = sci => rc.n[sci];
  const top = {}, sub = {};
  for (const c of Object.values(N)) if (c.kind === "clade" && c.rank === r1 && n(c.sci) != null) {
    const t = path(c.id).find(id => N[id].rank === r0);
    if (t) sub[t] = (sub[t] || 0) + n(c.sci);
  }
  for (const s of SP) {
    if (s.answerable === false) continue;
    const p = path(s.id), t = p.find(id => N[id].rank === r0);
    let u = r1 && p.find(id => N[id].rank === r1);
    if (!u || n(N[u].sci) == null) u = "_rest";
    if (!t || n(N[t].sci) == null) continue;  // 数の無い群は出さない（tools/check.py が知らせる）
    ((top[t] ||= {})[u] ||= []).push(s.id);
  }
  const T = Object.keys(top);
  BUCKETS = T.map(t => Object.entries(top[t]).map(([u, ids]) => {
    const x = { ids, w: !r1 ? 1 : u === "_rest" ? Math.max(0, n(N[t].sci) - (sub[t] || 0)) : n(N[u].sci) };
    x.sw = ids.map(tw); x.st = x.sw.reduce((a, b) => a + b, 0);
    return x;
  })).map(B => B.some(x => x.w > 0) ? B.filter(x => x.w > 0) : B.map(x => ({ ...x, w: 1 })));
  BW = T.map(t => rc.top === "sqrt" ? Math.sqrt(n(N[t].sci)) : n(N[t].sci));
}
function makeKeys(s) { s.keys = [[s.ja, "ja"], [s.sci, "sci"], ...(s.sciSynonyms || []).map(a => [a, "syn"]), ...s.aliases.map(a => [a, (s.subspeciesAliases || []).includes(a) ? "subsp" : "alias"])].map(([t, k]) => ({ t, k, n: norm(t) })); }
function path(id) { const a = []; while (id) { a.push(id); id = N[id].parent; } return a.reverse(); }
function lca(a, b) { const pa = new Set(path(a)); let x = b; while (!pa.has(x)) x = N[x].parent; return x; }
