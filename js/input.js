// 入力の補完候補
"use strict";
// ---- 補完 ----
let sel = -1, cur = [], suggMore = 0;
function suggest(q) {
  const n = norm(q); if (!n) return [];
  const out = [];
  for (const s of SP) {
    let best = null;
    for (const k of s.keys) {
      const i = k.n.indexOf(n); if (i < 0) continue;
      const score = (i === 0 ? 0 : 10) + (k.k === "ja" ? 0 : k.k === "alias" || k.k === "subsp" ? 1 : 2) + k.n.length / 100;
      if (!best || score < best.score) best = { s, k, score };
    }
    if (best) out.push(best);
  }
  const cap = HARD() ? 20 : 8; suggMore = out.length - cap;
  return out.sort((a, b) => a.score - b.score).slice(0, cap);
}
function showSugg() {
  const u = $("#sugg"); cur = suggest($("#guess").value); sel = cur.length ? 0 : -1;
  if (!cur.length) { u.hidden = true; $("#guess").setAttribute("aria-expanded", "false"); return; }
  u.innerHTML = cur.map((r, i) => {
    const used = G.guesses.includes(r.s.id);
    const via = r.k.k === "alias" ? `<span class="via">（${esc(r.k.t)}）</span>` : r.k.k === "syn" ? `<span class="via">（旧学名 <i>${esc(r.k.t)}</i>）</span>` : "";
    // 亜種名で当たったときは「亜種名（種名の亜種）」と出し、選ぶと種の推測になる
    const name = r.k.k === "subsp" ? `<span>${esc(r.k.t)}</span><span class="via">（${esc(r.s.ja)}の亜種）</span>` : `<span>${esc(r.s.ja)}</span>${via}`;
    return `<li role="option" id="o${i}" data-id="${r.s.id}" aria-selected="${i === sel}" class="${used ? "used" : ""}">${name}<span class="sci">${esc(r.s.sci)}</span>${used ? `<span class="via">推測済み</span>` : ""}</li>`;
  }).join("") + (HARD() && suggMore > 0 ? `<li class="more" aria-disabled="true">ほか ${suggMore.toLocaleString()} 種（もう少し打つと絞れます）</li>` : "");
  u.hidden = false; $("#guess").setAttribute("aria-expanded", "true");
}
function choose(id) { $("#guess").value = ""; $("#sugg").hidden = true; if (G.guesses.includes(id)) { flash(`${N[id].ja} はもう推測しました。`, true); return; } guess(id);
  // スマホではキーボードを閉じて、伸びた枝が隠れないようにする（PCは続けて打てるよう入力欄に戻す）
  matchMedia("(pointer: coarse)").matches ? $("#guess").blur() : $("#guess").focus(); }
