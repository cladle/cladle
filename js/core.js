// 共通の道具・データから系統樹を組み立てる・共通祖先（path / lca）
"use strict";
const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const store = {
  get(k) { try { return JSON.parse(localStorage.getItem(k)) } catch (e) { return null } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)) } catch (e) {} }
};

let D, N = {}, SP = [], BUCKETS = [], BW = [], MAX = 15;
// ゲキムズ・魚編：別のデータ（data-hard.json・data-fish.json）に切り替える。成績・途中の問題はモードごとに別に保存する
let LEVEL = "normal";
const DATA = {};
const LV_FILE = { normal: "data.json", hard: "data-hard.json", fish: "data-fish.json" };
const LV_NAME = { normal: "", hard: "ゲキムズ", fish: "魚編" };
const KEY = k => LEVEL === "normal" ? k : k.replace("dk-", `dk-${LEVEL}-`);
const HARD = () => LEVEL === "hard";
const FISH = () => LEVEL === "fish";
const BIG = () => LEVEL !== "normal";  // 種の多いデータ（補完の件数、ヒント2の出し方、図鑑の属・科の表示）
const HINT1 = 10, HINT2 = 13;  // この回数の推測のあとにヒントが押せる
const HUNT = 8;  // ゲキムズ：属でクリアしたあとの種探しの回数（残り回数とは別）
const limit = () => G.gAt ? G.gAt + HUNT : MAX;

// ---- 文字の正規化（カタカナ→ひらがな、全角半角、空白・中黒を除去）----
function norm(s) {
  return String(s).normalize("NFKC").toLowerCase()
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
}
function makeKeys(s) { s.keys = [[s.ja, "ja"], [s.sci, "sci"], ...(s.sciSynonyms || []).map(a => [a, "syn"]), ...s.aliases.map(a => [a, (s.subspeciesAliases || []).includes(a) ? "subsp" : "alias"])].map(([t, k]) => ({ t, k, n: norm(t) })); }
function path(id) { const a = []; while (id) { a.unshift(id); id = N[id].parent; } return a; }
function lca(a, b) { const pa = new Set(path(a)); let x = b; while (!pa.has(x)) x = N[x].parent; return x; }
