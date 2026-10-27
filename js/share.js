// 共有された問題：同じ動物で遊べるリンク
"use strict";
// ---- 共有された問題：同じ動物で遊べるリンク ----
const SHARE_KEY = "cladle-share";
function shareMix(b) { return b.map((v, i) => v ^ SHARE_KEY.charCodeAt(i % SHARE_KEY.length) ^ (i * 37 & 255)); }
function shareEncode(o) { return btoa(String.fromCharCode(...shareMix(new TextEncoder().encode(JSON.stringify(o))))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); }
function shareDecode(c) {
  try { return JSON.parse(new TextDecoder().decode(shareMix(Uint8Array.from(atob(String(c).replace(/-/g, "+").replace(/_/g, "/")), x => x.charCodeAt(0))))); }
  catch (e) { return null; }
}
function playLine() {
  if (mode === "daily") return "";
  const c = shareEncode({ t: G.target, w: G.won ? 1 : 0, n: G.won ? clearN() : G.guesses.length, h: (G.h1 ? 1 : 0) + (G.h2 ? 1 : 0), ...(HARD() && exactWin() ? { x: G.gAt ? G.guesses.length - G.gAt : 0 } : {}), ...(G.gaveUp ? { g: 1 } : {}) });
  return `\nこの動物で遊ぶ → https://cladle.github.io/cladle/?from=share#${HARD() ? "hard/" : ""}p=${c}`;
}
function sharedFrom(c) {
  if (!c.w) return c.g ? "降参" : "当てられず";
  return `${c.n} 回${c.x != null ? `（🎯${c.x ? `種探し ${c.x} 回` : "種まで"}）` : ""}${c.h ? `・💡${c.h}` : ""}`;
}
function openShared(code) { setView("free"); newGame("shared", code); }
