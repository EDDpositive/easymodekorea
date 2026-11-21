/* EasyModeKorea app shell: offline, install, save, share, notices. Shared by every page. */
(function () {
  "use strict";
  var E = window.EMK || { lang: "en", up: "", t: {} }, T = E.t, d = document;
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function list(k) { try { var a = JSON.parse(get(k) || "[]"); return Array.isArray(a) ? a : []; } catch (e) { return []; } }
  function count(path, title) { try { if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({ path: path, title: title, event: true }); } catch (e) {} }
  function mk(tag, cls, text) { var n = d.createElement(tag); if (cls) n.className = cls; if (text) n.textContent = text; return n; }
  var standalone = !!((window.matchMedia && matchMedia("(display-mode: standalone)").matches) || navigator.standalone === true);
  if (standalone) d.documentElement.classList.add("app");
  try { sessionStorage.setItem("emk-go", "1"); } catch (e) {}

  /* One small notice above the tabs. */
  var note = null, noteTimer = 0;
  function toast(text, actText, act, ms) {
    if (!note) { note = mk("div", "toast app-toast"); note.setAttribute("role", "status"); d.body.appendChild(note); }
    note.textContent = text;
    if (actText) { var b = mk("button", "", actText); b.type = "button"; b.addEventListener("click", act); note.appendChild(b); }
    note.hidden = false; clearTimeout(noteTimer);
    if (ms !== 0) noteTimer = setTimeout(function () { note.hidden = true; }, ms || 2600);
  }
  window.emkToast = toast;

  /* Offline notice. */
  function net() { if (!navigator.onLine) toast(T.offline, null, null, 6000); }
  addEventListener("offline", net); net();

  /* Offline copy of the site, and a notice when the page on screen has a newer version. */
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register(E.up + "sw.js?l=" + E.lang).catch(function () {});
    navigator.serviceWorker.addEventListener("message", function (ev) {
      if (ev.data && ev.data.t === "upd" && ev.data.p === location.pathname) toast(T.update, T.refresh, function () { location.reload(); }, 12000);
    });
  }

  /* Install prompt: shown after the visitor has looked around, never inside the installed app. */
  var deferred = null, bar = null;
  function askInstall() { if (!deferred) return; var p = deferred; deferred = null; hideBar(); p.prompt(); count("install", "install"); }
  function hideBar() { if (bar) { bar.remove(); bar = null; } }
  function showBar() {
    if (bar || !deferred || standalone) return;
    if (Date.now() - Number(get("emk-install-no") || 0) < 14 * 864e5) return;
    bar = mk("div", "install-bar"); bar.setAttribute("role", "region"); bar.setAttribute("aria-label", T.install_btn);
    var go = mk("button", "btn", T.install_btn), no = mk("button", "x", "\u2715"); go.type = no.type = "button"; no.setAttribute("aria-label", T.later);
    go.addEventListener("click", askInstall);
    no.addEventListener("click", function () { set("emk-install-no", String(Date.now())); hideBar(); });
    bar.appendChild(mk("span", "", T.install)); bar.appendChild(go); bar.appendChild(no); d.body.appendChild(bar);
  }
  var views = 0; try { views = Number(sessionStorage.getItem("emk-pv") || 0) + 1; sessionStorage.setItem("emk-pv", String(views)); } catch (e) {}
  addEventListener("beforeinstallprompt", function (ev) {
    ev.preventDefault(); deferred = ev;
    d.dispatchEvent(new CustomEvent("emk-installable"));
    if (views >= 2) showBar(); else setTimeout(showBar, 20000);
  });
  addEventListener("appinstalled", function () { deferred = null; hideBar(); count("installed", "installed"); });
  window.emkInstall = { ready: function () { return !!deferred; }, ask: askInstall, standalone: standalone };

  /* Language: remember the choice, close the menu on an outside tap, suggest the reader's language once. */
  var menu = d.querySelector(".lang-menu");
  d.querySelectorAll(".langs a[data-l]").forEach(function (a) { a.addEventListener("click", function () { set("emk-lang", a.getAttribute("data-l")); }); });
  if (menu) d.addEventListener("click", function (ev) { if (menu.open && !menu.contains(ev.target)) menu.open = false; });
  (function () {
    if (d.getElementById("lang-suggest") || get("wik-lang-dismiss") || get("emk-lang")) return;
    var w = (navigator.language || "").toLowerCase();
    var want = w.indexOf("ja") === 0 ? "ja" : /^zh-(tw|hk|mo|hant)/.test(w) ? "zh-tw" : w.indexOf("zh") === 0 ? "zh-cn" : w.indexOf("vi") === 0 ? "vi" : w.indexOf("en") === 0 ? "en" : "";
    if (!want || want === E.lang) return;
    var a = d.querySelector('.langs a[data-l="' + want + '"]'), hero = d.querySelector(".hero"); if (!a || !hero) return;
    var wrap = mk("div", "wrap pre"), b = mk("div", "banner");
    var go = mk("a", "btn alt", T["switch"]); go.href = a.getAttribute("href");
    go.addEventListener("click", function () { set("emk-lang", want); });
    var no = mk("button", "linkbtn", T.dismiss); no.type = "button";
    no.addEventListener("click", function () { set("wik-lang-dismiss", "1"); wrap.remove(); });
    b.appendChild(mk("span", "", T.suggest.replace("{l}", a.textContent))); b.appendChild(go); b.appendChild(no);
    wrap.appendChild(b); hero.insertAdjacentElement("afterend", wrap);
  })();

  /* Save and share on guide pages. Saved guides and recent guides are lists of slugs kept on this phone. */
  var sv = d.getElementById("save-btn"), sh = d.getElementById("share-btn");
  if (E.guide) {
    var rec = list("emk-recent").filter(function (s) { return s !== E.guide; }); rec.unshift(E.guide); set("emk-recent", JSON.stringify(rec.slice(0, 6)));
  }
  if (sv && E.guide) {
    var paint = function () { var on = list("emk-saved").indexOf(E.guide) >= 0; sv.setAttribute("aria-pressed", String(on)); sv.querySelector("span").textContent = on ? T.saved : T.save; return on; };
    sv.addEventListener("click", function () {
      var s = list("emk-saved"), i = s.indexOf(E.guide);
      if (i >= 0) s.splice(i, 1); else { s.unshift(E.guide); count("save/" + E.guide, "save guide"); }
      set("emk-saved", JSON.stringify(s.slice(0, 40))); toast(paint() ? T.saved_toast : T.unsaved_toast);
    });
    paint();
  }
  if (sh) sh.addEventListener("click", function () {
    var c = d.querySelector('link[rel="canonical"]'), url = c ? c.href : location.href, title = d.title;
    if (location.hostname !== "easymodekorea.com") url = location.href.split("#")[0];
    var copied = function () { toast(T.link_copied); };
    if (navigator.share) { navigator.share({ title: title, url: url }).catch(function () {}); }
    else if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(url).then(copied, function () {}); }
    count("share" + location.pathname, "share");
  });
})();
