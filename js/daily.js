// 出題：今日の動物とフリーの種の選び方、日付から作る乱数
"use strict";
// ---- 出題：枠を等確率 → 枠内で門を重みつき → 門内は一様 ----
function pick(rand) {
  const B = pickIn({ ids: BUCKETS, sw: BW, st: BW.reduce((a, b) => a + b, 0) }, rand());
  const tot = B.reduce((s, x) => s + x.w, 0); let r = rand() * tot;
  for (const x of B) { r -= x.w; if (r <= 0) return pickIn(x, rand()); }
  return B[B.length - 1].ids[0];
}
function pickIn(x, u) {
  if (!x.sw) return x.ids[Math.floor(u * x.ids.length)];
  let r = u * x.st;
  for (let i = 0; i < x.ids.length; i++) { r -= x.sw[i]; if (r < 0) return x.ids[i]; }
  return x.ids[x.ids.length - 1];
}
function mulberry(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function hash(s) { let h = 2166136261; for (const c of s) { h ^= c.codePointAt(0); h = Math.imul(h, 16777619); } return h >>> 0; }
function todayJST() { return new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 10); }
function dailyNo(day) { const e = D.meta.selection?.dailyEpoch || "2026-10-21"; return Math.round((Date.parse(day) - Date.parse(e)) / 864e5) + 1; }
