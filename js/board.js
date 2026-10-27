// 画面に描く：ボタン・系統樹（SVG）・正解後の結果・共有テキスト
"use strict";
const ACT = { reset: ["別の問題にする", "もう一度押すと別の問題へ"], giveup: ["降参する", "もう一度押すと降参"], reveal: ["答えを見る", "もう一度押すと答えを表示"] };
function act(b) {
  const k = b.dataset.act;
  if (k === "next") { store.set(KEY("dk-free"), null); newGame("free"); return; }
  if (!b.classList.contains("armed")) {
    b.classList.add("armed"); b.textContent = ACT[k][1];
    setTimeout(() => { if (b.isConnected) { b.classList.remove("armed"); b.textContent = ACT[k][0]; } }, 3000);
    return;
  }
  if (k === "reset") { track(mode + "-reset"); store.set(KEY("dk-free"), null); newGame("free"); return; }
  if (G.done) return;
  if (k === "reveal") { track(mode + "-reveal"); G.done = G.won = true; G.exact = false; G.fresh = null; $("#flash").hidden = true; save(); render(); return; }
  G.done = true; G.won = false; G.gaveUp = true; track(mode + "-giveup"); G.fresh = null; $("#flash").hidden = true;
  save(); render();
}
function hintsHTML() {
  if (G.done) return "";
  const n = G.guesses.length, out = [];
  if (mode === "shared" && !n) out.push(`<p class="hint">📮 共有された動物です。解き終わると、共有した人の回数が見られます。</p>`);
  if (G.gAt) { const k = SP.filter(s => s.parent === N[G.target].parent && !G.guesses.includes(s.id)).length;
    out.push(`<p class="hint">✅ ${G.gAt} 回目で同じ属を当ててクリアしました。この属には、まだ推測していない種があと <b>${k}</b> 種います。種探し ${HUNT} 回のうちに種まで当てると 🎯。</p>`); }
  if (G.h1) { const c = candidates().length; out.push(`<p class="hint">💡 「${esc(N[deepest()].ja)}」の中に、候補はあと <b>${c}</b> 種です。</p>`); }
  else if (n >= HINT1) out.push(`<button class="btn ghost hintbtn" data-hint="1">💡 ヒント1</button>`);
  if (G.h2) out.push(G.reveal ? `<p class="hint">💡 答えの動物は「${esc(N[G.reveal].ja)}」の仲間です。</p>` : HARD() ? `<p class="hint">💡 ${esc(jaClue(G.target))}</p>` : `<p class="hint">💡 答えの動物の豆知識：${esc(maskFact(G.target))}</p>`);
  else if (n >= HINT2) out.push(`<button class="btn ghost hintbtn" data-hint="2">💡 ヒント2</button>`);
  return out.join("");
}
function flash(t, err) { const f = $("#flash"); f.textContent = t; f.className = "flash" + (err ? " err" : ""); f.hidden = false; }

function render() {
  $("#modeLabel").textContent = (HARD() ? "ゲキムズ " : "") + (mode === "daily" ? `今日の動物 #${dailyNo(G.day)}` : mode === "shared" ? "共有された問題" : "フリープレイ");
  const hunt = G.gAt && !G.done, base = hunt ? G.gAt : 0;
  $("#leftLabel").textContent = hunt ? "種探し 残り" : "残り";
  $("#left").textContent = hunt ? limit() - G.guesses.length : MAX - Math.min(G.guesses.length, MAX);
  $("#meter").innerHTML = Array.from({ length: hunt ? HUNT : MAX }, (_, i) => `<i class="${i < G.guesses.length - base ? "used" : ""}"></i>`).join("");
  $("#guess").disabled = G.done;
  if (!G.guesses.length) $("#flash").hidden = true;

  const h = treeHTML(G.target, G.guesses, G.done, G.fresh, $("#board").clientWidth, { reveal: G.reveal, dim: G.h1 && !G.done, win: celebrate, grow: celebrate || openGrow ? { id: G.target, prev: new Set(), all: true, fast: openGrow && !celebrate } : growId && lastEdges ? { id: growId, prev: lastEdges } : null });
  lastEdges = treeHTML.edges; growId = null; openGrow = false; animUntil = Date.now() + treeHTML.animEnd * 1000;
  $("#board").innerHTML = h;
  $("#hints").innerHTML = hintsHTML(); $("#hints").hidden = !$("#hints").innerHTML;
  $("#actions").innerHTML = actionsHTML();
  $("#result").innerHTML = G.done ? resultHTML() : "";
  if (celebrate) {
    celebrate = false;
    const r = $("#result .result"), still = matchMedia("(prefers-reduced-motion: reduce)").matches, wait = still ? 0 : treeHTML.animEnd + .3;
    if (r) { r.classList.add("celebrate"); r.style.animationDelay = wait + "s"; }
    const msg = exactWin() ? `正解！ ${N[G.target].ja} でした。` : `属まで正解！ 答えは ${N[G.target].ja} でした。`;
    if (still) flash(msg); else setTimeout(() => { if (G.won) flash(msg); }, (wait - .3) * 1000);
    setTimeout(() => r?.scrollIntoView({ behavior: still ? "auto" : "smooth", block: "start" }), wait * 1000 + 500);
  }
}
function deepestOf(target, guesses, reveal) {
  let best = reveal && path(target).includes(reveal) ? reveal : D.root;
  for (const g of guesses) { const L = g === target ? target : lca(g, target); if (N[L].depth > N[best].depth) best = L; }
  return best;
}
// 推測した動物と「？」（正解）を葉にした系統樹（左の中央が根、右に葉が並ぶ）。
// 枝分かれしない途中の節目は省き、分岐点だけを残す。
function treeHTML(target, guesses, done, fresh, width, opt = {}) {
  const W = Math.max(280, width || 358);
  const known = done ? target : deepestOf(target, guesses, opt.reveal);
  const tips = new Set(guesses.filter(g => g !== target || done));
  if (done) tips.add(target);
  const U = new Set(path(known));
  for (const g of tips) for (const x of path(g)) U.add(x);
  const onPath = new Set(path(known));
  const kids = {};
  for (const x of U) if (N[x].parent) (kids[N[x].parent] ||= []).push(x);
  const Q = "?goal";
  const keep = x => x === D.root || tips.has(x) || x === known || (kids[x] || []).length + (!done && x === known ? 1 : 0) >= 2;
  const below = x => (kids[x] || []).flatMap(c => keep(c) ? [c] : below(c));
  const num = {}; guesses.forEach((g, i) => num[g] = i + 1);
  // 圧縮した木を作る
  const T = {};
  const on = id => id === Q || onPath.has(id) || id === target;
  const build = (x, d) => {
    const ch = below(x);
    if (!done && x === known) ch.push(Q);
    T[x] = { id: x, d, ch };
    for (const c of ch) c === Q ? (T[Q] = { id: Q, d: d + 1, ch: [], pid: x }) : build(c, d + 1);
  };
  build(D.root, 0);
  const nLeaves = id => T[id].ch.length ? T[id].ch.reduce((a, c) => a + nLeaves(c), 0) : 1;
  // 正解へ続く枝をまっすぐ中央に通し、ほかの枝は上下に振り分ける
  let up = 0, down = 0;
  const arrange = id => {
    const n = T[id], main = n.ch.find(on);
    if (!main) return;
    const above = [], belowS = [];
    for (const c of n.ch) if (c !== main) { if (up <= down) { above.push(c); up += nLeaves(c); } else { belowS.push(c); down += nLeaves(c); } }
    n.ch = [...above.reverse(), main, ...belowS];
    arrange(main);
  };
  arrange(D.root);
  const leaves = Object.values(T).filter(n => !n.ch.length);
  const maxD = Math.max(...Object.values(T).filter(n => n.ch.length).map(n => n.d), 0);
  // 葉の名前の幅を実際に測り、入りきらない分だけ省略する
  const ctx = (treeHTML.cv ||= document.createElement("canvas")).getContext("2d");
  ctx.font = `14px ${getComputedStyle(document.body).fontFamily}`;
  const tipText = id => id === Q ? "？" : (num[id] ? num[id] + " " : "") + N[id].ja;
  const maxLabel = W * 0.42;
  const fit = id => { let t = id === Q ? "？" : N[id].ja; while (t.length > 2 && ctx.measureText((num[id] ? num[id] + " " : "") + t).width > maxLabel) t = t.slice(0, -1); return t === N[id]?.ja || id === Q ? t : t.slice(0, -1) + "…"; };
  const labelW = Math.min(maxLabel, Math.max(...leaves.map(n => ctx.measureText(tipText(n.id)).width), 20)) + 12;
  const left = 6, tipX = W - labelW, dx = Math.max(14, (tipX - left - 6) / Math.max(maxD + 1, 1));
  const ROW = 34, top = 18;
  // 葉は上から順に並べ、節目は子の真ん中に置く（根は左の中央に来る）
  let row = 0;
  const place = n => {
    if (!n.ch.length) { n.y = top + row++ * ROW; n.x = tipX; return; }
    n.ch.forEach(c => place(T[c]));
    const ys = n.ch.map(c => T[c].y);
    n.y = (Math.min(...ys) + Math.max(...ys)) / 2; n.x = left + n.d * dx;
  };
  place(T[D.root]);
  const H = top + (row - 1) * ROW + 24;
  let lines = "", nodes = "", texts = "";
  // 伸ばす枝：前回の図に無かった枝のうち、推測した動物へ続くものと、新しくできた分かれ目から出るもの。
  // 伸ばす枝より先にある枝も一緒に伸ばし直す（途中で浮いて見えないように）。正解時は木全体を根から伸ばす
  const G2 = opt.grow, edges = new Set(), DUR = G2?.fast ? .22 : opt.win ? .5 : .55, STEP = DUR;  // 枝は一本ずつ順に（前の枝が届いてから次が伸びる）
  const onGrow = id => !!G2 && (id === G2.id || T[id].ch.some(onGrow));
  const animE = new Map(), late = new Map();  // 枝 → 伸び始める時刻、点 → 枝が届く時刻
  if (G2) {
    const prevNodes = new Set(); for (const e of G2.prev) e.split(">").forEach(x => prevNodes.add(x));
    const mark = (id, inh) => { for (const c of T[id].ch) {
      const key = id + ">" + c, a = G2.all || inh || (!G2.prev.has(key) && (c === Q || onGrow(c) || !prevNodes.has(id)));
      if (a) animE.set(key, T[id].d); mark(c, a); } };
    mark(D.root, false);
    const base = Math.min(...animE.values());
    for (const [k, d] of animE) { const t = (d - base) * STEP; animE.set(k, t); late.set(k.split(">")[1], t + DUR); }
  }
  const animEnd = Math.max(0, ...late.values());
  // 点・名前は枝が届いてから出す
  const lateStyle = id => late.has(id) ? ` style="animation-delay:${late.get(id).toFixed(2)}s"` : "";
  const cand = [];
  for (const n of Object.values(T)) {
    for (const c of n.ch) {
      const k = T[c], cls = c === Q ? "ln goal" : on(c) ? "ln on" : "ln";
      const key = n.id + ">" + c; edges.add(key);
      const t0 = animE.get(key), ga = t0 == null ? "" : `${c === Q ? "" : ' pathLength="1"'} style="animation-delay:${t0.toFixed(2)}s"`;
      lines += `<path class="${cls}${ga ? (c === Q ? " fade" : " grow") : ""}"${ga} d="M${n.x},${n.y} V${k.y} H${k.x - 4}"/>`;
    }
  }
  for (const n of Object.values(T)) {
    if (n.id === Q) {
      const fa = lateStyle(Q);
      nodes += `<text class="tq${fa ? " fade" : ""}"${fa} x="${n.x}" y="${n.y + 5}">？</text>`;
    } else if (!n.ch.length) {
      const hit = n.id === target;
      const fa = lateStyle(n.id);
      const last = !done && num[n.id] === guesses.length;  // 直前に推測した動物は太字で示す
      nodes += `<text class="svgnode tl${hit ? " hit" : ""}${last ? " last" : ""}${fa && !(opt.win && hit) ? " fade" : ""}"${fa} data-id="${n.id}" role="button" tabindex="0" x="${n.x}" y="${n.y + 5}">${num[n.id] ? `<tspan class="n">${num[n.id]} </tspan>` : ""}${esc(fit(n.id))}</text>`;
    } else {
      const st = n.id === known && !done, cls = ["svgnode", "nd", on(n.id) ? "on" : "", st ? "stop" : "", n.id === fresh ? "new" : ""].join(" ");
      const la = lateStyle(n.id);
      nodes += `<g class="${cls}${la ? " fade" : ""}"${la} data-id="${n.id}" role="button" tabindex="0"><circle cx="${n.x}" cy="${n.y}" r="${st ? 6 : 3.5}"/></g>`;
      cand.push({ n, st, prio: st || n.id === D.root ? 0 : on(n.id) ? 1 : 2 });
    }
  }
  // 節目の名前は線や他の名前と重ならない場所にだけ書く（現在地と根を先に、次に正解側の深い順）。書けなかった名前はタップか下の一覧で見られる
  const seg = [];
  for (const n of Object.values(T)) for (const c of n.ch) {
    const k = T[c];
    seg.push({ x1: n.x - 2, x2: n.x + 2, y1: Math.min(n.y, k.y), y2: Math.max(n.y, k.y) }, { x1: n.x, x2: k.x, y1: k.y - 2, y2: k.y + 2 });
  }
  const placed = [];
  const hits = (r, list) => list.some(q => r.x1 < q.x2 && q.x1 < r.x2 && r.y1 < q.y2 && q.y1 < r.y2);
  cand.sort((a, b) => a.prio - b.prio || b.n.d - a.n.d);
  for (const { n, st } of cand) {
    ctx.font = `${st ? "700 13px" : "11px"} ${getComputedStyle(document.body).fontFamily}`;
    const kin = kinLabel(n.id);
    let w = ctx.measureText(N[n.id].ja).width; const g = st ? 9 : 5, kh = kin ? 11 : 0;
    if (kin) { ctx.font = `10px ${getComputedStyle(document.body).fontFamily}`; w = Math.max(w, ctx.measureText(kin).width); }
    // 右・枝の上（左寄せ）・右上・右下の順に試す
    const all = [[n.x + g, 0], [n.x - 3 - w, -9], [n.x + 3, -11], [n.x + 3, 14]]
      .map(([x, dy]) => ({ x, y: n.y + dy, r: { x1: x - 1, x2: x + w + 1, y1: n.y + dy - 7, y2: n.y + dy + 5 + kh } }));
    const spots = all.filter(sp => sp.r.x1 >= 0 && sp.r.x2 <= tipX - 2);
    // 現在地と根は必ず書く。狭い画面で葉の手前に収まらないときは、葉の文字の列にはみ出してもよい
    const wide = all.filter(sp => sp.r.x1 >= 0);
    const sp = spots.find(sp => !hits(sp.r, placed) && !hits(sp.r, seg))
      || (st || n.id === D.root ? spots.find(sp => !hits(sp.r, placed)) || wide.find(sp => !hits(sp.r, placed) && !hits(sp.r, seg)) || wide.find(sp => !hits(sp.r, placed)) || spots[0] || wide[0] : null);
    if (!sp) continue;
    placed.push(sp.r);
    const la = lateStyle(n.id);
    texts += `<text class="nl${on(n.id) ? " on" : ""}${st ? " stop" : ""}${la ? " fade" : ""}"${la} x="${sp.x}" y="${sp.y + 4}" data-id="${n.id}">${esc(N[n.id].ja)}${kin ? `<tspan class="kin" x="${sp.x}" dy="11">${esc(kin)}</tspan>` : ""}</text>`;
  }
  treeHTML.edges = edges; treeHTML.animEnd = animEnd;
  const tip = !store.get("dk-tip") && !opt.demo ? `<p class="tip">下の名前や図の名前を押すと、その仲間の説明が見られます。</p>` : "";
  const crumb = `${tip}<div class="crumb"><span class="eyebrow">${done ? "答えの動物までの系統" : "答えの動物が入っている分類群"}</span><div>${path(known).map(x => `<button class="clade-mini${x === known ? " here" : ""}" data-id="${x}">${esc(N[x].ja)}</button>`).join(`<span class="sep">›</span>`)}</div></div>`;
  // 推測したときは、伸びる枝の先に小さな点を付けて、分かれ目から推測した動物まで進める（見る場所の案内）
  let tipDot = "";
  if (G2 && !G2.all && !opt.win && T[G2.id] && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const par = {}; for (const n of Object.values(T)) for (const c of n.ch) par[c] = n.id;
    const chain = []; for (let id = G2.id; id; id = par[id]) chain.unshift(id);
    const seg = []; for (let i = 1; i < chain.length; i++) { const k = chain[i - 1] + ">" + chain[i]; if (animE.has(k)) seg.push([T[chain[i - 1]], T[chain[i]], animE.get(k)]); }
    if (seg.length) {
      const t0 = seg[0][2], dur = seg.length * DUR, lens = seg.map(([a, c]) => Math.abs(c.y - a.y) + Math.abs(c.x - 4 - a.x)), tot = lens.reduce((x, y) => x + y, 0) || 1;
      let acc = 0; const kp = [0, ...lens.map(l => (acc += l) / tot)].map(x => Math.min(1, x).toFixed(4)).join(";"), kt = seg.map((_, i) => (i / seg.length).toFixed(4)).concat("1").join(";");
      const d = `M${seg[0][0].x},${seg[0][0].y} ` + seg.map(([a, c]) => `V${c.y} H${c.x - 4}`).join(" ");
      tipDot = `<circle class="tipdot" r="4" opacity="0"><set attributeName="opacity" to="1" begin="${t0.toFixed(2)}s"/>`
        + `<animateMotion path="${d}" begin="${t0.toFixed(2)}s" dur="${dur.toFixed(2)}s" fill="freeze" calcMode="spline" keyPoints="${kp}" keyTimes="${kt}" keySplines="${seg.map(() => ".42 0 .58 1").join(";")}"/>`
        + `<animate attributeName="opacity" from="1" to="0" begin="${(t0 + dur).toFixed(2)}s" dur=".35s" fill="freeze"/></circle>`;
    }
  }
  return `<div class="cgwrap"><svg class="cgsvg${opt.dim ? " dim" : ""}${opt.win ? " win" : ""}" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="系統樹">${lines}${nodes}${texts}${tipDot}</svg></div>${guesses.length && !done ? crumb : ""}`;
}
// 英字（学名）のままの分類群に、一番近い和名の門・綱・目を添える（例：腹足綱の中の目）。和名が定着していない群は自作の読みを付けない方針のため
function kinLabel(id) {
  const n = N[id]; if (!n || n.kind === "species" || !/^[A-Za-z][A-Za-z .\-]*$/.test(n.ja)) return "";
  let p = n.parent; while (p && !(["門", "綱", "目"].includes(N[p].rank) && !/^[A-Za-z]/.test(N[p].ja))) p = N[p].parent;
  return p ? `${N[p].ja}の中の${n.rank === "クレード" ? "まとまり" : n.rank}` : "";
}
// 別名（和名）・旧学名・そのほかの検索語
function namesHTML(n) {
  const ja = n.aliases.filter(a => /[ぁ-んァ-ヶ一-龠]/.test(a)), other = n.aliases.filter(a => !ja.includes(a) && !(n.sciSynonyms || []).includes(a));
  return [ja.length && `別名：${esc(ja.join("、"))}`, n.sciSynonyms?.length && `旧学名：<i>${n.sciSynonyms.map(esc).join("、")}</i>`, other.length && `検索語：${esc(other.join("、"))}`]
    .filter(Boolean).map(x => `<div class="path names">${x}</div>`).join("");
}
function cladeBtn(n) {
  const v = n.verify ? `<span class="badge-v">要確認</span>` : "";
  const p = n.polytomy ? `<span class="poly">多分岐</span>` : "";
  return `<button class="clade" data-id="${n.id}"><span class="ja">${esc(n.ja)}</span><span class="sci">${esc(n.sci)}</span>${n.rank ? `<span class="rank">${esc(n.rank)}</span>` : ""}${p}${v}</button>`;
}
function resultHTML() {
  const t = N[G.target];
  const head = G.won ? (exactWin() ? `正解！ ${esc(t.ja)}` : `属まで正解！ 答えは ${esc(t.ja)} でした`) : `${G.gaveUp ? "降参。" : ""}答えは ${esc(t.ja)} でした`;
  const hints = (G.h1 ? 1 : 0) + (G.h2 ? 1 : 0);
  return `<section class="result${G.won ? " won" : ""}"><h2>${head}</h2>
    <div class="sci">${esc(t.sci)} ${t.verify ? `<span class="badge-v">要確認</span>` : ""}</div>
    ${namesHTML(t)}
    ${t.fact ? `<p class="fact">${esc(t.fact)}</p>` : ""}
    <div class="lookup">調べる：${lookupLinks(t)}</div>
    <div class="score"><span><b>${G.won ? clearN() : "×"}</b> / ${MAX} 回</span>${hints ? `<span>💡 ヒント ${hints} 回</span>` : ""}${G.won && HARD() ? `<span>${G.gAt ? `✅ 属は ${G.gAt} 回` : ""}${G.gAt && exactWin() ? "・" : ""}${exactWin() ? (G.gAt ? `🎯 種探し ${G.guesses.length - G.gAt} 回` : "🎯 種までぴったり") : ""}</span>` : ""}${mode === "shared" ? `<span class="from">共有した人：${sharedFrom(G.from)}</span>` : ""}</div>
    <div class="share-row"><button class="btn share-btn" id="copy">結果を共有</button><a class="btn ghost xpost" id="xpost" href="https://x.com/intent/tweet?text=${encodeURIComponent(shareText())}" target="_blank" rel="noopener">Xでポスト</a></div>
    ${mode === "daily" ? "" : `<p class="hint">共有したリンクから、相手も同じ動物で遊べます。</p>`}
    <pre class="share" id="shareText">${esc(shareText())}</pre>
    <div class="fullpath"><div>${path(t.parent).map(x => `<button class="clade-mini" data-id="${x}">${esc(N[x].ja)}</button>`).join(`<span class="sep">›</span>`)}<span class="sep">›</span><b>${esc(t.ja)}</b></div></div>
    ${kinHTML(t)}
    <div class="row"><button class="btn ghost" id="toZukan">図鑑でこの動物を見る</button>
    ${mode === "free" ? `<button class="btn ghost" id="again">次の問題</button>` : `<button class="btn ghost" id="goFree">フリープレイへ</button>`}</div>
    ${mode === "daily" ? statsHTML() : ""}</section>`;
}
// 近い仲間：正解のすぐ上で、ほかの収録種がいる節目を紹介する
function kinHTML(t) {
  let a = t.parent;
  while (N[a].parent && N[a].count < 2) a = N[a].parent;
  const n = N[a], all = [];
  const walk = id => N[id].kind === "species" ? all.push(id) : N[id].kids.forEach(walk);
  walk(a);
  const others = all.filter(id => id !== t.id), MAXK = all.length <= 16 ? 16 : 12;
  const name = /^[ぁ-んァ-ヶー一-龠]/.test(n.ja) ? n.ja : `${n.ja}（${n.rank}）`;
  return `<div class="sub"><span class="eyebrow">近い仲間</span>
    <h3><span>${esc(n.ja)}</span><span class="sci" style="font-weight:400;color:var(--muted);font-size:.85rem">${esc(n.sci)}</span><span class="rank">${esc(n.rank)}</span></h3>
    <p>${esc(n.desc)}</p>
    <p style="font-size:.85rem;color:var(--muted)">${esc(name)}には、ほかに次の動物が収録されています。</p>
    <div class="kin">${others.slice(0, MAXK).map(id => `<button class="twig${G.guesses.includes(id) ? " me" : ""}" data-id="${id}">${esc(N[id].ja)}</button>`).join("")}</div>
    ${others.length > MAXK ? `<button class="kin-more" data-zk="${a}">ほか ${others.length - MAXK} 種を図鑑で見る</button>` : ""}</div>`;
}
// 写真は載せず（権利と同定の問題）、外部の図鑑・検索へのリンクにする
function lookupLinks(t) {
  const q = encodeURIComponent;
  return [["Wikipedia", `https://ja.wikipedia.org/w/index.php?search=${q(t.ja)}`],
    t.gbif && ["GBIF", `https://www.gbif.org/species/${t.gbif}`],
    ["画像検索", `https://www.google.com/search?tbm=isch&q=${q(t.ja + " " + t.sci)}`]]
    .filter(Boolean).map(([l, u]) => `<a href="${u}" target="_blank" rel="noopener noreferrer">${l}</a>`).join("");
}
function shareText() {
  const td = N[G.target].depth;
  const marks = G.guesses.map(g => {
    if (g === G.target) return "🎯";
    if (sameClear(g, G.target)) return "✅";
    const r = N[lca(g, G.target)].depth / (td - 1);
    return r >= 1 ? "🟩" : r >= .66 ? "🟧" : r >= .33 ? "🟨" : "⬜";
  });
  const title = (HARD() ? "Cladle ゲキムズ" : "Cladle") + (mode === "daily" ? ` #${dailyNo(G.day)}` : mode === "shared" ? "（共有された問題）" : "（フリー）");
  const lines = [];
  for (let i = 0; i < marks.length; i += 10) lines.push(marks.slice(i, i + 10).join(""));
  const hints = (G.h1 ? 1 : 0) + (G.h2 ? 1 : 0);
  return `${title}  ${G.won ? clearN() : "×"}/${MAX}${HARD() && exactWin() ? `  🎯${G.gAt ? G.guesses.length - G.gAt : ""}` : ""}${hints ? `  💡×${hints}` : ""}\n${lines.join("\n")}${mode === "daily" ? "\nhttps://cladle.github.io/cladle/?from=share" + (HARD() ? "#hard" : "") : ""}${playLine()}`;
}
