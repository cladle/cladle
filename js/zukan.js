// 節目・種の詳細シートと図鑑
"use strict";
// ---- 詳細シート ----
function openSheet(id) {
  const n = N[id], isSp = n.kind === "species";
  if (!isSp && !store.get("dk-tip")) { store.set("dk-tip", 1); document.querySelectorAll(".tip").forEach(e => e.remove()); }
  const hide = isSp && id === G?.target && !G.done && view !== "zukan";
  let h = `<h3><span>${esc(n.ja)}</span><span class="sci" style="font-weight:400;font-size:1rem">${esc(n.sci)}</span></h3>
    <div class="row"><span class="rank">${isSp ? "種" : esc(n.rank)}</span>${n.verify ? `<span class="badge-v">要確認</span>` : ""}${n.jaStatus === "provisional" ? `<span class="badge-v">和名なし・仮表記</span>` : ""}</div>`;
  if (!isSp && kinLabel(id)) h += `<div class="kin-n">${esc(kinLabel(id))}（定着した和名が無いため学名で表示）</div>`;
  if (!hide) h += `<p style="margin:0">${esc(isSp ? n.fact : n.desc)}</p>`;
  if (!isSp && view === "zukan") h += `<div class="path">収録 ${n.count} 種</div>`;
  if (!hide && isSp && !n.fact && BIG()) h += `<p style="margin:0;color:var(--muted);font-size:.85rem">${esc(N[n.parent].ja)}（${esc(N[n.parent].rank)}） › ${esc(path(n.id).map(x => N[x]).filter(x => x.rank === "科")[0]?.ja || "")}</p>`;
  if (n.polytomy) h += `<div class="note poly-n"><b>多分岐の理由：</b>${esc(n.polytomy)}</div>`;
  if (n.verify) h += `<div class="note v-n"><b>要確認：</b>${esc(Object.entries(n.verify).map(([k, v]) => ({ ja: "和名", sci: "学名", placement: "位置" }[k] || k) + "：" + v).join("／"))}</div>`;
  if (isSp) h += namesHTML(n);
  if (isSp && !hide) h += `<div class="lookup">調べる：${lookupLinks(n)}</div>`;
  // 道筋の名前を押すとその分類群の説明へ。「図鑑で見る」で図鑑のその階層（種は入っている階層）へ移る
  h += hide ? `<div class="path">${path(n.parent || id).map(x => esc(N[x].ja)).join(" › ")}</div>`
    : `<div class="path sheet-path">${path(n.parent || id).map(x => `<button data-id="${x}">${esc(N[x].ja)}</button>`).join("<span>›</span>")}</div>`;
  h += `<div class="row sheet-act">${hide || (isSp && view === "zukan") ? "" : `<button class="btn ghost" ${isSp ? `data-zkreveal="${id}"` : `data-zk="${id}"`}>図鑑で見る</button>`}<button class="btn ghost close" id="closeSheet">閉じる</button></div>`;
  $("#sheetIn").innerHTML = h; $("#sheet").hidden = $("#scrim").hidden = false; $("#closeSheet").focus();
}
function closeSheet() { $("#sheet").hidden = $("#scrim").hidden = true; }

// ---- 図鑑 ----
let ZK = null, ZKQ = "", ZKHIT = null;
function zkRow(id) {
  const n = N[id], sp = n.kind === "species";
  return sp
    ? `<li class="sp${id === ZKHIT ? " hit" : ""}" data-sp="${id}"><button data-id="${id}"><span class="ja">${esc(n.ja)}</span><span class="side">${n.verify ? `<span class="badge-v">要確認</span>` : ""}</span><span class="sci">${esc(n.sci)}</span></button></li>`
    : `<li class="cl"><button data-zk="${id}"><span class="ja">${esc(n.ja)}</span><span class="side"><span class="rank">${esc(n.rank)}</span>${n.count}</span><span class="sci">${esc(n.sci)}</span></button></li>`;
}
function renderZukan() {
  const box = $("#zk"); if (!box || !D) return;
  if (ZKQ) {  // 検索中は一致したものを平らに並べる
    const q = norm(ZKQ), hits = Object.values(N).filter(x => [x.ja, x.sci, ...(x.aliases || []), ...(x.sciSynonyms || []), ...(x.groups || [])].some(t => norm(t).includes(q)));
    hits.sort((a, b) => (a.kind === "species") - (b.kind === "species") || norm(a.ja).indexOf(q) - norm(b.ja).indexOf(q));
    box.innerHTML = hits.length ? `<div class="zk-sec">${hits.length} 件</div><ul class="zk-list">${hits.slice(0, 80).map(x => zkRow(x.id).replace("</button>", `<span class="where">${esc(path(x.parent || x.id).slice(-3, x.parent ? undefined : -1).map(y => N[y].ja).join(" › "))}</span></button>`)).join("")}</ul>` : `<p class="zk-sec">見つかりませんでした。</p>`;
    return;
  }
  const id = ZK || D.root, n = N[id];
  const kids = [...n.kids].sort((a, b) => (N[a].kind === "species") - (N[b].kind === "species"));
  const cl = kids.filter(k => N[k].kind !== "species"), sp = kids.filter(k => N[k].kind === "species");
  box.innerHTML = `<nav class="zk-crumb" aria-label="系統の道筋">${path(id).slice(0, -1).map(x => `<button data-zk="${x}">${esc(N[x].ja)}</button><span>›</span>`).join("")}</nav>
    <div class="zk-head"><h2>${esc(n.ja)}<span class="sci">${esc(n.sci)}</span></h2>
      <div class="meta"><span class="rank">${esc(n.rank)}</span>${n.polytomy ? `<span class="poly">多分岐</span>` : ""}${n.verify ? `<span class="badge-v">要確認</span>` : ""}<span>収録 ${n.count} 種</span></div>
      ${kinLabel(id) ? `<div class="kin-n">${esc(kinLabel(id))}（定着した和名が無いため学名で表示）</div>` : ""}<p>${esc(n.desc)}</p>${n.polytomy ? `<div class="note poly-n"><b>多分岐の理由：</b>${esc(n.polytomy)}</div>` : ""}</div>
    ${cl.length ? `<div class="zk-sec">下位のグループ</div><ul class="zk-list">${cl.map(zkRow).join("")}</ul>` : ""}
    ${sp.length ? `<div class="zk-sec">種</div><ul class="zk-list">${sp.map(zkRow).join("")}</ul>` : ""}`;
}
function zukanGo(id) { closeSheet(); if (view !== "zukan") setView("zukan"); ZK = id; ZKHIT = null; ZKQ = ""; $("#zkq").value = ""; renderZukan(); $("#zk").scrollIntoView({ block: "start" }); scrollTo({ top: 0 }); }
function revealInZukan(id) {
  closeSheet(); setView("zukan");
  ZK = N[id].parent; ZKQ = ""; ZKHIT = id; $("#zkq").value = ""; renderZukan();
  document.querySelector(`#zk li[data-sp="${id}"]`)?.scrollIntoView({ block: "center" });
}
