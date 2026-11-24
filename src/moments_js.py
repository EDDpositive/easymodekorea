"""Page scripts for moments_ui.py (30차). Plain scripts, no network: they read the location only on a tap and keep every
choice in this phone's own storage (emk-food, emk-days, emk-moved, emk-trip)."""

SOS_JS = r"""
/* The rescue grid code (national point number): UTM-K on GRS80, origin moved 300 km west and 700 km south, 10 m squares.
   Worked out on the phone, so it needs no data and nothing is sent. */
window.emkGrid = function (lat, lon) {
  if (!(lat > 32.9 && lat < 38.7 && lon > 124.4 && lon < 132.1) || (lat < 34.85 && lon > 129.1) || (lat < 36.2 && lon > 129.9)) return null;
  const a = 6378137, f = 1 / 298.257222101, k0 = 0.9996, R = Math.PI / 180, e2 = f * (2 - f), ep = e2 / (1 - e2), p = lat * R, p0 = 38 * R;
  const Mr = q => a * ((1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256) * q - (3 * e2 / 8 + 3 * e2 ** 2 / 32 + 45 * e2 ** 3 / 1024) * Math.sin(2 * q)
    + (15 * e2 ** 2 / 256 + 45 * e2 ** 3 / 1024) * Math.sin(4 * q) - (35 * e2 ** 3 / 3072) * Math.sin(6 * q));
  const co = Math.cos(p), t = Math.tan(p), N = a / Math.sqrt(1 - e2 * Math.sin(p) ** 2), T = t * t, C = ep * co * co, K = co * (lon - 127.5) * R;
  const E = k0 * N * (K + (1 - T + C) * K ** 3 / 6 + (5 - 18 * T + T * T + 72 * C - 58 * ep) * K ** 5 / 120) + 1e6;
  const Y = k0 * (Mr(p) - Mr(p0) + N * t * (K * K / 2 + (5 - T + 9 * C + 4 * C * C) * K ** 4 / 24 + (61 - 58 * T + T * T + 600 * C - 330 * ep) * K ** 6 / 720)) + 2e6;
  const x = E - 7e5, y = Y - 13e5, L = "가나다라마바사아", i = Math.floor(x / 1e5), j = Math.floor(y / 1e5);
  if (!L[i] || !L[j]) return null;
  const d = v => String(Math.floor((v % 1e5) / 10)).padStart(4, "0");
  return L[i] + L[j] + " " + d(x) + " " + d(y);
};
(function () {
  const R = document.getElementById("sos"); if (!R) return;
  const D = JSON.parse(document.getElementById("sos-data").textContent), c = D.t, $ = id => document.getElementById(id);
  const ROM = { "가": ["ga", "カ"], "나": ["na", "ナ"], "다": ["da", "タ"], "라": ["ra", "ラ"], "마": ["ma", "マ"], "바": ["ba", "パ"], "사": ["sa", "サ"], "아": ["a", "ア"] };
  const NUM = [["공", "gong", "コン"], ["일", "il", "イル"], ["이", "i", "イ"], ["삼", "sam", "サム"], ["사", "sa", "サ"], ["오", "o", "オ"], ["육", "yuk", "ユク"], ["칠", "chil", "チル"], ["팔", "pal", "パル"], ["구", "gu", "ク"]];
  let fix = null, code = null, what = null, stay = false, watch = null, timer = null, slow = null;
  const addr = (store("emk-addr") || "").trim().slice(0, 160);
  const ja = D.lang === "ja", k = ja ? 2 : 1;
  const spell = s => s.split(" ").map(w => [...w].map(ch => /\d/.test(ch) ? NUM[+ch][k] : (ROM[ch] || [ch, ch])[k - 1]).join(ja ? " " : "-")).join(ja ? "、" : ", ");
  const spoken = s => s.split(" ").map(w => [...w].map(ch => /\d/.test(ch) ? NUM[+ch][0] : ch).join("")).join(", ");
  const num = () => (what && what[1]) || "119";
  const main = () => what ? what[3] : D.help[0];
  const nb = s => s.replace(/ /g, "\u00a0"), off = () => Math.round(fix.accuracy), wide = () => fix && fix.accuracy > 30;   /* a wide fix says so, in Korean too */
  const place = () => stay ? "제 위치는 " + addr + "입니다." : code ? D.loc[0].replace("{c}", code) + (wide() ? "\n" + D.err[0].replace("{m}", off()) : "") : "";
  const lines = s => s.replace(/([.?!]) (?=\S)/g, "$1\n");
  const body = () => { const m = Math.max(1, Math.round(fix ? fix.accuracy : 0));
    const p = stay ? "위치: " + addr : code ? "위치: 국가지점번호 " + code + " (" + fix.latitude.toFixed(5) + ", " + fix.longitude.toFixed(5) + ", 오차 약 " + m + "m)" : "";
    return [main(), p, "외국인이에요. " + D.lko + "로 답해 주세요."].filter(Boolean).join("\n"); };
  function paint() {
    $("sos-out").hidden = !code || stay; $("sos-find").hidden = !!code || stay; $("sos-stay-on").hidden = !stay; $("sos-stay").hidden = !addr || stay;
    if (code) { $("sos-code").textContent = nb(code);
      $("sos-acc").textContent = c.acc.replace("{m}", Math.max(1, Math.round(fix.accuracy))) + " · " + fix.latitude.toFixed(5) + ", " + fix.longitude.toFixed(5);
      $("sos-rough").hidden = fix.accuracy <= 100; }
    const n = num(); $("sos-text").href = "sms:" + n + (/iPhone|iPad|iPod/.test(navigator.userAgent) ? "&" : "?") + "body=" + encodeURIComponent(body());
    $("sos-text-l").textContent = c.text.replace("{n}", n);
    document.querySelectorAll("#sos-what .tg").forEach(b => b.setAttribute("aria-pressed", String(!!what && b.dataset.id === what[0])));
    document.querySelectorAll(".sos-call").forEach(a => a.classList.toggle("on", !!what && a.dataset.n === n));
    const rows = [[what ? what[k + 3] : D.help[k], main()]];
    if (code && !stay) { rows.push([D.loc[k].replace("{c}", spell(code)), D.loc[0].replace("{c}", code)]); if (wide()) rows.push([D.err[k].replace("{m}", off()), D.err[0].replace("{m}", off())]); }
    rows.push([D.itp[k], D.itp[0]]);
    $("sos-rom").replaceChildren(...rows.map(r => el("li", {}, [el("b", { text: r[0] }), el("span", { lang: "ko", text: r[1] })])));
  }
  const msg = t => { $("sos-msg").textContent = t || ""; $("sos-msg").hidden = !t; };
  const stop = () => { if (watch !== null) navigator.geolocation.clearWatch(watch); watch = null; clearTimeout(timer); clearTimeout(slow); R.classList.remove("busy"); $("sos-find-l").textContent = c.where; };
  function find() {
    if (!navigator.geolocation) { msg(c.none); $("sos-near").open = true; return; }
    stop(); stay = false; msg(""); fix = null; code = null; paint();
    R.classList.add("busy"); $("sos-find-l").textContent = c.finding; count("sos/find", "where am I");
    watch = navigator.geolocation.watchPosition(p => { if (fix && p.coords.accuracy >= fix.accuracy) return;
      const g = emkGrid(p.coords.latitude, p.coords.longitude);
      if (!g) { stop(); msg(c.out); paint(); return; }
      fix = p.coords; code = g; msg(""); paint(); if (fix.accuracy <= 12) stop();
    }, er => { if (code) return; stop(); msg(er.code === 1 ? c.denied : c.none); $("sos-near").open = true; paint(); }, { enableHighAccuracy: true, maximumAge: 0, timeout: 75000 });
    /* A phone with no data needs longer for its first satellite fix. */
    slow = setTimeout(() => { if (!code) msg(c.slow); }, 8000);
    timer = setTimeout(() => { if (code) stop(); else timer = setTimeout(stop, 55000); }, 25000);
  }
  $("sos-find").addEventListener("click", find); $("sos-again").addEventListener("click", find);
  D.what.forEach(w => { const b = el("button", { type: "button", class: "tg", "aria-pressed": "false", text: w[2] }); b.dataset.id = w[0];
    b.addEventListener("click", () => { what = what && what[0] === w[0] ? null : w; paint(); if (what) $("sos-show").scrollIntoView({ block: "nearest" }); }); $("sos-what").append(b); });
  $("sos-show").addEventListener("click", () => { const p = place();
    show(c.show, [lines(main()), code && !stay ? p.replace(code, nb(code)) : p, D.itp[0]].filter(Boolean).join("\n"), "", [what ? what[2] : D.helpm, stay ? c.stay : code || "", D.itpm].filter(Boolean).join(" · "), null,
      { list: true, say: [main(), stay || !code ? p : D.loc[0].replace("{c}", spoken(code)) + (wide() ? " " + D.err[0].replace("{m}", off()) : ""), D.itp[0]].filter(Boolean).join(" ") }); });
  $("sos-text").addEventListener("click", () => count("sos/text", "text to 119 or 112"));
  document.querySelectorAll(".sos-call").forEach(a => a.addEventListener("click", () => count("sos/call-" + a.dataset.n, "call")));
  $("sos-stay").addEventListener("click", () => { stay = true; stop(); msg(""); $("sos-stay-a").textContent = addr; paint(); });
  $("sos-stay-off").addEventListener("click", () => { stay = false; paint(); });
  paint();
})();
"""

MYCARD_JS = r"""
(function () {
  const D = JSON.parse(document.getElementById("mc-data").textContent), c = D.t, $ = id => document.getElementById(id);
  const get = (k, d) => { try { const o = Object.assign({}, d, JSON.parse(store(k) || "{}")); for (const x in d) if (typeof o[x] !== typeof d[x] || Array.isArray(o[x]) !== Array.isArray(d[x])) o[x] = d[x]; return o; } catch (e) { return d; } };
  let F = get("emk-food", { a: [], n: [], s: 0 });
  const by = rows => Object.fromEntries(rows.map(x => [x[0], x])), A = by(D.al), N = by(D.no);
  const some = o => Object.values(o).some(v => Array.isArray(v) ? v.length : v);
  const put = (k, o) => { if (some(o)) store(k, JSON.stringify(o)); else try { localStorage.removeItem(k); } catch (e) {} };
  const save = () => put("emk-food", F);
  /* The Korean card text, one fact per line, so no grammar has to change with the choice. */
  function food() {
    const al = F.a.filter(i => A[i]), diet = F.n.filter(i => N[i] && N[i][3] === "diet"), no = F.n.filter(i => N[i] && N[i][3] !== "diet"), ko = [], me = [];
    if (al.length) { ko.push(D.fko.al + ": " + al.map(i => A[i][1]).join(", ")); if (F.s) ko.push(D.fko.sev); me.push(c.al_h + ": " + al.map(i => A[i][3]).join(", ")); if (F.s) me.push(c.sev); }
    diet.forEach(i => { ko.push(N[i][1]); me.push(N[i][2]); });
    if (no.length) { ko.push(D.fko.no + ": " + no.map(i => N[i][1]).join(", ")); me.push(c.no_h + ": " + no.map(i => N[i][2]).join(", ")); }
    return ko.length ? [ko.concat(D.fko.ask).join("\n"), me.join(" · ")] : null;
  }
  const of = b => F[b.dataset.set];
  document.querySelectorAll("[data-set]").forEach(b => b.addEventListener("click", () => { const arr = of(b), i = arr.indexOf(b.dataset.id); if (i < 0) arr.push(b.dataset.id); else arr.splice(i, 1); save(); paint(); }));
  $("mc-sev").addEventListener("click", () => { F.s = F.s ? 0 : 1; save(); paint(); });
  function paint() {
    document.querySelectorAll("[data-set]").forEach(b => b.setAttribute("aria-pressed", String(of(b).includes(b.dataset.id))));
    if (!F.a.length) F.s = 0;
    $("mc-sev").setAttribute("aria-pressed", String(!!F.s)); $("mc-sev").hidden = !F.a.length;
    const x = food(); $("mc-food").disabled = !x; $("mc-food-p").textContent = x ? x[0].split("\n").filter(l => l !== D.fko.ask).join("\n") : ""; $("mc-food-p").hidden = !x; $("mc-food-e").hidden = !!x;
    /* Words to look for on packages, and an honest note where the Korean label rule does not cover the allergy. */
    const al = F.a.filter(i => A[i]), words = al.filter(i => A[i][2]), off = al.filter(i => !A[i][2] && i !== "nuts");
    $("mc-label").hidden = !al.length; $("mc-words").replaceChildren(...words.map(i => el("li", {}, [el("b", { lang: "ko", text: A[i][2] }), el("span", { text: A[i][3] })])));
    $("mc-off").replaceChildren(...off.map(i => el("p", { text: c.label_no.replace("{x}", A[i][3]) + (i === "fish" ? " " + c.label_fish : "") })));
    $("mc-nuts").hidden = !al.includes("nuts"); $("mc-new").hidden = !al.some(i => i === "nuts" || i === "sesame");
  }
  $("mc-food").addEventListener("click", () => { const x = food(); if (x) show(D.lbl, x[0], "", x[1], D.fans, { list: true, hot: D.fko.sev }); });
  document.querySelector("[data-clear]").addEventListener("click", () => { F = { a: [], n: [], s: 0 }; save(); paint(); });
  paint();
})();
"""

REFUSED_JS = r"""
(function () {
  const R = document.getElementById("rf"); if (!R) return;
  const D = JSON.parse(document.getElementById("rf-data").textContent);
  const [P0, V0] = (store("wik-setup") || "").split("|"), P = /^(visitor|krsim|arc)$/.test(P0) ? P0 : "visitor", V = /^(ios|android)$/.test(V0) ? V0 : /iPhone|iPad|iPod/.test(navigator.userAgent) ? "ios" : "android";
  /* The reader's own status for the guide behind each answer, from the same data the guides use. */
  document.querySelectorAll(".rf-mine").forEach(b => { const a = (D.st[b.dataset.tid] || {})[P + "|" + V]; if (!a) return;
    const p = b.querySelector(".pill"); p.className = "pill " + a[0]; p.textContent = D.tone[a[0]]; b.querySelector(".rf-v").textContent = a[1]; b.querySelector(".rf-who").textContent = D.p[P] + " · " + D.d[V]; b.hidden = false; });
  let was = null;
  function go() {
    const [p, a] = location.hash.slice(1).split("/"), step = D.q[p] ? (a && D.q[p].includes(a) ? 3 : 2) : 1;
    document.getElementById("rf-1").hidden = step !== 1;
    document.querySelectorAll(".rf-step").forEach(s => { s.hidden = !(step === 2 && s.dataset.p === p); });
    document.querySelectorAll(".rf-ans").forEach(s => { s.hidden = !(step === 3 && s.dataset.a === p + "/" + a); });
    if (was !== null) { scrollTo(0, 0); const h = R.querySelector(":scope > :not([hidden]) h2"); if (h) h.focus({ preventScroll: true }); }
    was = step; if (step === 3) count("refused/" + p + "-" + a, "refused answer");
  }
  addEventListener("hashchange", go); go();
})();
"""

DAYS_JS = r"""
(function () {
  /* Trip mode: the dates on this phone decide what shows. Home shows only what is due; My trip shows the whole list in order.
     A reminder is a calendar file made here, so the phone's own calendar rings even when this app is closed. */
  const J = document.getElementById("days-data"); if (!J) return;
  const D = JSON.parse(J.textContent), c = D.t, home = document.getElementById("trip-now"), box = document.getElementById("days"), DAY = 864e5;
  const day = s => { const m = /^(\d{4})-(\d\d)-(\d\d)$/.exec(s || ""); return m ? Date.UTC(+m[1], m[2] - 1, +m[3]) : NaN; };
  const loc = document.documentElement.lang || "en", fmt = (t, y) => new Intl.DateTimeFormat(loc, { day: "numeric", month: "short", ...(y ? { year: "numeric" } : {}), timeZone: "UTC" }).format(new Date(t));
  const now = new Date(), today = Date.UTC(now.getFullYear(), now.getMonth(), now.getDate());
  const obj = k => { try { return JSON.parse(store(k) || "{}") || {}; } catch (e) { return {}; } };
  const tr = obj("emk-trip"), from = day(tr.from), to = day(tr.to), has = !isNaN(from) && !isNaN(to) && to >= from;
  const arc = /^arc/.test(store("wik-setup") || ""), busan = [].concat(obj("emk-rc").city || []).includes("busan"), long = has && to - from > 90 * DAY;
  let done = []; try { done = JSON.parse(store("emk-days") || "[]"); if (!Array.isArray(done)) done = []; } catch (e) {}
  const fits = i => !i.c || (i.c === "busan" ? busan : i.c === "visitor" ? !arc : arc || long);
  const when = i => !i.w ? NaN : i.w[0] === "day" ? from + (i.w[1] - 1) * DAY : (i.w[0] === "from" ? from : to) + i.w[1] * DAY;
  const list = D.items.filter(fits).map(i => ({ ...i, at: has ? (i.id === "arc" ? from + 89 * DAY : when(i)) : NaN })).filter(i => i.st !== "trip" || isNaN(i.at) || i.at < to);
  const tick = id => { done = done.includes(id) ? done.filter(x => x !== id) : done.concat(id); store("emk-days", JSON.stringify(done)); };
  const n = Math.round((from - today) / DAY), len = Math.round((to - from) / DAY) + 1;
  const label = !has ? "" : n > 1 ? c.to_go.replace("{n}", n) : n === 1 ? c.tomorrow : today === to ? c.leaving : today < to ? c.day.replace("{n}", 1 - n).replace("{m}", len) : c.over;
  const stage = !has ? "" : n > 0 ? "before" : today === to ? "leave" : today === to - DAY && today !== from ? "eve" : today === from ? "arrive" : today < to ? "trip" : "over";
  /* Calendar file for one item: a timed event with an alarm. Long lines are folded by bytes, as the format asks. */
  const fold = s => { const out = []; let cur = "", b = 0; for (const ch of s) { const w = new TextEncoder().encode(ch).length; if (b + w > 72) { out.push(cur); cur = " "; b = 1; } cur += ch; b += w; } out.push(cur); return out.join("\r\n"); };
  const esc = s => s.replace(/[\\;,]/g, m => "\\" + m).replace(/\n/g, "\\n");
  window.emkIcs = (id, text, at, hh) => { const d = new Date(at).toISOString().slice(0, 10).replace(/-/g, ""), st = new Date().toISOString().replace(/[-:]/g, "").slice(0, 15) + "Z";
    return ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//EasyModeKorea//Trip//EN", "BEGIN:VEVENT", "UID:" + id + "-" + d + "@easymodekorea.com", "DTSTAMP:" + st, "DTSTART:" + d + "T" + hh + "0000", "DTEND:" + d + "T" + hh + "1500",
      "SUMMARY:" + esc(text), "DESCRIPTION:EasyModeKorea", "BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:" + esc(text), "TRIGGER:PT0S", "END:VALARM", "END:VEVENT", "END:VCALENDAR", ""].map(fold).join("\r\n"); };
  const bell = (id, text, at, hh) => { const b = el("button", { type: "button", class: "dy-bell", "aria-label": c.remind + ": " + text, html: D.bell });
    b.addEventListener("click", () => { const a = el("a", { href: URL.createObjectURL(new Blob([emkIcs(id, text, at, hh)], { type: "text/calendar;charset=utf-8" })), download: "easymodekorea-" + id + ".ics" });
      document.body.append(a); a.click(); a.remove(); count("days/remind", "calendar reminder"); if (window.emkToast) emkToast("🔔 " + c.saved); });
    return b; };
  const hour = i => i.st === "eve" ? "19" : i.st === "leave" ? "08" : "10";
  const tk = (i, after) => { const b = el("button", { type: "button", class: "dy-t", "aria-pressed": String(done.includes(i.id)), "aria-label": i.t }, el("i", { "aria-hidden": "true" }));
    b.addEventListener("click", () => { tick(i.id); const on = done.includes(i.id); b.setAttribute("aria-pressed", String(on)); b.closest("li").classList.toggle("off", on); if (after) after(); }); return b; };
  if (home && has && stage !== "over") {
    const due = list.filter(i => !done.includes(i.id) && i.st !== "long" && (i.st === "before" ? n > 0 && i.at <= today : i.st === "trip" ? stage === "trip" && i.at <= today : i.st === stage));
    const next = list.filter(i => i.at > today && !done.includes(i.id) && i.st !== "long").sort((a, b) => a.at - b.at)[0];
    home.replaceChildren(el("p", { class: "tn-h" }, [el("b", { text: label }), el("a", { href: "saved.html#days", text: c.all })]));
    if (due.length) home.append(el("ul", { class: "tn" }, due.slice(0, 2).map(i => el("li", {}, [tk(i), el("a", { href: i.l ? i.l[1].replace(/^#/, "saved.html#") : "saved.html#days", text: i.t })]))));
    else home.append(el("p", { class: "tn-next" }, next ? [el("small", { text: c.next + " · " + fmt(next.at) }), el("span", { text: next.t })] : [el("span", { text: c.nothing })]));
    home.hidden = false;
    /* Once the trip has started, what is due today replaces the pre-trip check. */
    if (n <= 0) { const r = document.querySelector("#today .ready-cta"); if (r) r.hidden = true; }
  }
  if (!box) return;
  const L = document.getElementById("days-list"), need = document.getElementById("days-need"), head = document.getElementById("days-now");
  need.hidden = has; head.hidden = !has; head.textContent = label;
  const df = document.getElementById("day-from"), dt = document.getElementById("day-to");
  const put = () => { if (df.value && dt.value && dt.value >= df.value) { store("emk-trip", JSON.stringify({ from: df.value, to: dt.value })); location.reload(); } };
  df.addEventListener("change", put); dt.addEventListener("change", put);
  const ORD = ["before", "arrive", "trip", "eve", "leave"], at0 = ORD.indexOf(stage);
  const ord = !has ? (arc ? ["long"] : []) : at0 < 0 ? ORD.concat("long") : ORD.slice(at0).concat("long", ORD.slice(0, at0));
  for (const g of ord) {
    const items = list.filter(i => i.st === g); if (!items.length) continue;
    const cnt = el("span", { class: "dg-n" }), left = () => { const k = items.filter(x => !done.includes(x.id)).length; cnt.textContent = k ? String(k) : "✓"; };
    left();
    const d = el("details", { class: "dg", name: "dg" }), same = items.every(i => i.at === items[0].at) && !isNaN(items[0].at);
    d.append(el("summary", {}, [el("b", { text: c.stages[g] }), same ? el("small", { text: fmt(items[0].at) }) : null, cnt]));
    if (g === stage || (!has && g === "long")) d.open = true;
    const ul = el("ul", { class: "dy" });
    for (const i of items) {
      const info = [], line = [el("span", { text: i.t })]; if (!isNaN(i.at) && !same) line.push(el("small", { text: g === "before" && i.at <= today ? c.now : fmt(i.at) }));
      if (i.l) info.push(el("a", { class: "btn ghost", href: i.l[1], text: i.l[0] }));
      if (i.src.length) info.push(el("p", { class: "fact-src" }, [i.d ? el("time", { class: "ck", datetime: i.d, text: "✓ " + fmt(day(i.d), 1) + " " }) : null].concat(i.src.map(s => el("a", { href: s[1], ...(/^http/.test(s[1]) ? { target: "_blank", rel: "noopener" } : {}), text: s[0] + " " })))));
      const li = el("li", { class: done.includes(i.id) ? "off" : "" }, [tk(i, left), info.length ? el("details", { class: "dy-d" }, [el("summary", {}, line), el("div", {}, info)]) : el("div", { class: "dy-d" }, line)]);
      if (!isNaN(i.at) && (i.at > today || (i.at === today && now.getHours() < +hour(i)))) li.append(bell(i.id, i.t, i.at, hour(i)));
      if (i.id === "move") li.append(mover(i));
      ul.append(li);
    }
    d.append(ul); L.append(d);
  }
  document.getElementById("days-note").hidden = !L.querySelector(".dy-bell");
  function mover(i) {   /* Moved on this date: the last day to report it, counted on the safe side. */
    const inp = el("input", { type: "date" }), out = el("p", { class: "dy-by", role: "status" });
    const calc = () => { const m = day(inp.value); out.replaceChildren(); if (isNaN(m)) return; store("emk-moved", inp.value); const by = m + 14 * DAY;
      out.append(el("span", { text: c.by.replace("{d}", fmt(by)) + " · F-4: " + fmt(m + 13 * DAY) })); if (by >= today) out.append(bell("move", i.t, Math.max(today, by - 3 * DAY), "10")); };
    inp.value = store("emk-moved") || ""; inp.addEventListener("change", calc); calc();
    return el("div", { class: "dy-mv" }, [el("label", {}, [el("span", { text: c.moved }), inp]), out]); }
  if (location.hash === "#days") box.scrollIntoView();
})();
"""
