// 画面の切り替え・ボタンの配線・データの読み込みと起動
"use strict";
// ---- 画面切り替え ----
let view = "daily";
function setView(v) {
  view = v;
  document.querySelectorAll("nav button").forEach(b => b.setAttribute("aria-selected", b.dataset.v === v));
  $("#game").hidden = !(v === "daily" || v === "free"); $("#zukan").hidden = v !== "zukan"; $("#about").hidden = v !== "about"; $("#howto").hidden = v !== "howto"; $("#extra").hidden = v !== "extra";
  if (v === "extra") $("#extraDoc").innerHTML = extraHTML();
  demoStop(); $(".demo").hidden = BIG(); if (v === "howto" && !BIG()) demoPlay();
  if (v === "daily" || v === "free") { if (mode !== v || !G) newGame(v); }
  window.scrollTo(0, 0);
}

function wire() {
  document.querySelectorAll("nav button").forEach(b => b.onclick = () => { if (b.dataset.v !== view) { track("tab-" + b.dataset.v); zkSearched = false; } setView(b.dataset.v); });
  const inp = $("#guess");
  inp.addEventListener("input", showSugg);
  inp.addEventListener("keydown", e => {
    const u = $("#sugg");
    if (e.key === "ArrowDown" || e.key === "ArrowUp") { if (!cur.length) return; e.preventDefault();
      sel = (sel + (e.key === "ArrowDown" ? 1 : -1) + cur.length) % cur.length;
      u.querySelectorAll("li").forEach((li, i) => li.setAttribute("aria-selected", i === sel));
      inp.setAttribute("aria-activedescendant", "o" + sel); }
    else if (e.key === "Enter") { if (!e.isComposing && sel >= 0 && cur[sel]) { e.preventDefault(); choose(cur[sel].s.id); } }
    else if (e.key === "Escape") u.hidden = true;
  });
  $("#sugg").addEventListener("mousedown", e => e.preventDefault());
  $("#sugg").addEventListener("click", e => { const li = e.target.closest("li"); if (li?.dataset.id) choose(li.dataset.id); });
  document.addEventListener("click", e => {
    if (!e.target.closest(".inputbox")) $("#sugg").hidden = true;
    const z = e.target.closest("[data-zk]"); if (z) { zukanGo(z.dataset.zk); return; }
    const b = e.target.closest(".clade, .twig, .clade-mini, .svgnode, .nl, .zk [data-id]:is(button)");
    if (b) { e.preventDefault(); track(N[b.dataset.id]?.kind === "species" ? "sheet-species" : "sheet-clade"); openSheet(b.dataset.id); return; }
    const lk = e.target.closest(".lookup a"); if (lk) track("lookup-" + ({ Wikipedia: "wikipedia", GBIF: "gbif" }[lk.textContent] || "image"));
    const hb = e.target.closest(".hintbtn"); if (hb) { useHint(+hb.dataset.hint); return; }
    const ab = e.target.closest("[data-act]"); if (ab) { act(ab); return; }
    if (e.target.id === "copy") copyShare();
    if (e.target.id === "xpost") track(mode + "-share-x");
    if (e.target.id === "again") { store.set(KEY("dk-free"), null); newGame("free"); }
    if (e.target.id === "goFree") setView("free");
    const mc = e.target.closest("[data-mode]"); if (mc) { if (mc.dataset.mode === LEVEL) setView("daily"); else setLevel(mc.dataset.mode); return; }
    if (e.target.id === "backNormal") { setLevel("normal"); return; }
    if (e.target.id === "toZukan") { track("zukan-from-result"); revealInZukan(G.target); }
    if (e.target.id === "closeSheet" || e.target.id === "scrim") closeSheet();
  });
  document.addEventListener("keydown", e => { if (e.key === "Escape") closeSheet(); });
  let zkT; $("#zkq").addEventListener("input", e => { clearTimeout(zkT); zkT = setTimeout(() => { ZKQ = e.target.value.trim(); renderZukan(); if (ZKQ && !zkSearched) { zkSearched = true; track("zukan-search"); } }, 200); });
  const setHdr = () => document.documentElement.style.setProperty("--hdr", $("header").offsetHeight + "px");
  setHdr(); addEventListener("resize", setHdr);
}
async function copyShare() {
  const t = shareText(), b = $("#copy");
  if (navigator.share && matchMedia("(pointer: coarse)").matches) { try { await navigator.share({ text: t }); track(mode + "-share"); return; } catch (e) { if (e.name === "AbortError") return; } }
  try { await navigator.clipboard.writeText(t); track(mode + "-share"); b.textContent = "コピーしました"; setTimeout(() => b.textContent = "結果を共有", 2000); }
  catch (e) { const r = document.createRange(); r.selectNodeContents($("#shareText")); getSelection().removeAllRanges(); getSelection().addRange(r); b.textContent = "選択しました（長押しでコピー）"; }
}

async function setLevel(lv) {
  if (lv === LEVEL || !DATA.normal) return;
  const bs = document.querySelectorAll(".level"), off = d => bs.forEach(b => b.disabled = d); off(true);
  try { DATA[lv] ||= await loadData(LV_FILE[lv]); }
  catch (e) { flash(`${LV_NAME[lv]}のデータを読み込めませんでした（${e.message}）`, true); off(false); return; }
  off(false);
  if (lv !== "normal") track("level-" + lv);  // 切り替える前に送る（切り替えた先の印が付かないように）
  LEVEL = lv; store.set("dk-level", lv);
  N = {}; SP = [];
  build(DATA[lv]); applyLevel();
  STATS = { days: {} }; mergeStats(store.get(KEY("dk-stats")));
  G = null; ZK = null; ZKQ = ""; ZKHIT = null; $("#zkq").value = ""; renderZukan();
  setView(view === "about" || view === "howto" || view === "zukan" ? view : view === "free" ? "free" : "daily");
}
function applyLevel() {
  const h = HARD();
  $("#level").setAttribute("aria-pressed", h);
  document.documentElement.classList.toggle("hard", h); document.documentElement.classList.toggle("fish", FISH());
  $("#levelNote").hidden = !BIG();
  if (h) $("#levelNote").innerHTML = `<b>ゲキムズ（試作）</b>：${SP.length.toLocaleString()} 種の動物から出題。同じ属でクリア、種まで当てれば 🎯。`;
  if (FISH()) $("#levelNote").innerHTML = `<b>魚編（試作）</b>：日本の魚 ${SP.length.toLocaleString()} 種から出題。種まで当てれば正解。<button class="back" id="backNormal">ふつうに戻る</button>`;
  $("#doc").innerHTML = aboutHTML();
  $("#howtoDoc").innerHTML = howtoHTML();
}
// 予約：data.json の meta.next = { from: "YYYY-MM-DD", file } があれば、その日からは次の版のファイルを使う
// （前もって置いておけば、日付が変わった時点でそろって切り替わる）
const due = data => data.meta.next && data.meta.next.from <= todayJST();
async function loadData(f = "data.json") {
  let data;
  for (let i = 0; i < 30; i++) {
    const r = await fetch(f);
    if (!r.ok) { if (data) break; throw new Error(r.status); }  // 予約の先のファイルが無い（古い data.json がキャッシュに残っていたときなど）は今の版のまま
    data = await r.json(); if (!due(data)) break; f = data.meta.next.file;
  }
  return data;
}
loadData().then(async data => {
  DATA.normal = data;
  const m = location.hash.match(/^#?(hard|fish)/), want = m ? m[1] : location.hash === "#normal" ? "normal" : store.get("dk-level") || "normal";
  if (LV_FILE[want] && want !== "normal") try { DATA[want] = await loadData(LV_FILE[want]); LEVEL = want; STATS = { days: {} }; mergeStats(store.get(KEY("dk-stats"))); } catch (e) {}
  build(DATA[LEVEL]); wire(); applyLevel();
  $("#level").onclick = () => setLevel(HARD() ? "normal" : "hard");
  renderZukan();
  $("#doc").innerHTML = aboutHTML();
  $("#howtoDoc").innerHTML = howtoHTML();
  $("#demoPrev").onclick = () => { demoStop(); demoShow(demoI - 1, false); };
  $("#demoNext").onclick = () => { demoStop(); demoShow(demoI + 1, false); };
  $("#demoReplay").onclick = demoPlay;
  const h = location.hash.slice(1).replace(/^(hard|fish)\/?/, "");
  if (h.startsWith("p=")) openShared(h.slice(2));
  else setView(["free", "zukan", "about", "howto", "extra"].includes(h) ? h : "daily");
  addEventListener("hashchange", () => { const m = location.hash.match(/^#(?:(hard|fish)\/)?p=(.+)$/); if (m && (m[1] || "normal") === LEVEL) openShared(m[2]); });
}).catch(err => {
  $("#board").innerHTML = `<p class="empty">データ（data.json）を読み込めませんでした（${esc(err.message)}）。index.html と同じフォルダに data.json を置き、ページを再読み込みしてください。</p>`;
});
