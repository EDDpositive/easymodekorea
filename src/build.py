"""Builds EasyModeKorea: checker page, topic pages and a changelog page, in each language.
Run from the repo root:  python korea/src/build.py
Content: data.py (answers) and data_extra.py (hook, short labels, icons, phrases, first 24 hours,
changelog, host-stay strings). Host stay details travel in the link's #g= hash: never sent to a
server or to analytics, and rendered with textContent only.
"""
import datetime, hashlib, html, json, os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
from data import CHECKED, CHECKED_ISO, LANGS, SOURCES, TASK_META  # noqa: E402
from data_extra import ASK, BRAND, FEEDBACK, FEEDBACK_FORM, FEEDBACK_TO, HELP, HELP_PHRASES, ICONS, KEYWORDS, PHRASES, PLAN, QUESTION, SHORT, UX, X  # noqa: E402
import zh_cn  # noqa: E402,F401  (adds Simplified Chinese)
import vi  # noqa: E402,F401  (adds Vietnamese)
from deep import CONTACT_EMAIL, DEEP, HEAD as DEEP_HEAD, PAGES  # noqa: E402
import layout  # noqa: E402
from layout import ADDR_GUIDES, AT, CARDS, COPY, tx  # noqa: E402
import app_shell as A  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
SITE = "https://easymodekorea.com/"
GOAT = "https://eddpositive.goatcounter.com/count"
CSS = open(os.path.join(os.path.dirname(__file__), "style.css"), encoding="utf-8").read()
CSS_V = hashlib.sha256(CSS.encode("utf-8")).hexdigest()[:8]  # cache-busting query for the shared stylesheet
e = lambda s: html.escape(str(s), quote=True)
icon = lambda tid: f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[tid]}</svg>'
FONTS = "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=IBM+Plex+Sans:wght@400;600;700&display=swap"
APP_V = hashlib.sha256(A.APP_JS.encode("utf-8")).hexdigest()[:8]  # cache-busting query for the shared script


def head(lang, title, desc, path, alt_paths, extra="", guide=None, index=True):
    up = up_of(lang)
    alts = "".join(f'<link rel="alternate" hreflang="{LANGS[k]["html_lang"]}" href="{SITE}{p}">' for k, p in alt_paths.items())
    alts += f'<link rel="alternate" hreflang="x-default" href="{SITE}{alt_paths["en"]}">'
    return f"""<!DOCTYPE html>
<html lang="{LANGS[lang]['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#2336e8"><meta name="theme-color" media="(prefers-color-scheme: dark)" content="#4a59ee">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png"><link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png">
<link rel="manifest" href="/manifest.webmanifest"><link rel="apple-touch-icon" href="/icon-192.png"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="{BRAND}">
<title>{e(title)}</title>{'' if index else '<meta name="robots" content="noindex">'}
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">{alts}
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{SITE}{path}"><meta property="og:image" content="{SITE}og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="robots" content="max-snippet:-1, max-image-preview:large">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="{FONTS}" onload="this.onload=null;this.rel='stylesheet'"><noscript><link rel="stylesheet" href="{FONTS}"></noscript>
<link rel="stylesheet" href="{up}style.css?v={CSS_V}">
<script>window.EMK={A.page_config(lang, up, UX[lang], guide)}</script><script defer src="{up}app.js?v={APP_V}"></script>
<script data-goatcounter="{GOAT}" async src="//gc.zgo.at/count.js"></script>{extra}
</head>
<body class="has-tabs">"""


def up_of(lang):
    return "../" if LANGS[lang]["dir"] else ""


def lang_links(cur, rel_paths, prefix):
    out = []
    for k, L in LANGS.items():
        cur_attr = ' aria-current="page"' if k == cur else ""
        out.append(f'<a href="{prefix}{rel_paths[k]}" hreflang="{L["html_lang"]}" lang="{L["html_lang"]}" data-l="{k}"{cur_attr}>{e(L["name"])}</a>')
    label = e(LANGS[cur]["ui"]["langs"])
    return (f'<details class="lang-menu"><summary aria-label="{label}">{A.IC["globe"]}<span>{e(LANGS[cur]["name"])}</span></summary>'
            f'<nav class="langs" aria-label="{label}">' + "".join(out) + "</nav></details>")


HOME_LBL = {"en": "All guides", "ja": "ガイド一覧", "zh-tw": "所有指南", "zh-cn": "所有指南", "vi": "Tất cả hướng dẫn"}


def hero(lang, alt, up, h1, lede, home="./", trust=True, back=False, search=True):
    """Top of every page: logo, search, language menu. Guides (back=True) also get save and share."""
    t = A.T[lang]
    back_a = (f'<div class="guide-bar"><a class="home-link" href="{home}">← {e(HOME_LBL.get(lang, HOME_LBL["en"]))}</a><span class="guide-acts">'
              f'<button class="act" type="button" id="save-btn" aria-pressed="false">{A.IC["save"]}<span>{e(t["save"])}</span></button>'
              f'<button class="act share" type="button" id="share-btn" aria-label="{e(t["share"])}">{A.IC["share"]}<span>{e(t["share"])}</span></button></span></div>') if back else ''
    find = f'<a class="icon-btn" href="{home}#q" aria-label="{e(t["search"])}">{A.IC["search"]}</a>' if search else ''
    return f"""<header class="hero"><div class="wrap">
  <div class="toprow"><a class="logo" href="{home}">EasyMode<b>Korea</b></a><div class="top-actions">{find}{lang_links(lang, alt, up)}</div></div>{back_a}
  {f'<h1>{e(h1)}</h1>' if h1 else ''}{f'<p class="lede">{e(lede)}</p>' if lede else ''}
</div></header>"""


def ask_box(lang):
    a = ASK[lang]
    return f"""<section class="ask" aria-labelledby="ask-t-{lang}"><h2 id="ask-t-{lang}">{e(a['title'])}</h2><p class="hint">{e(a['lead'])}</p>
<form class="ask-form" data-thanks="{e(a['thanks'])}"><textarea name="q" required maxlength="1000" aria-label="{e(a['title'])}" placeholder="{e(a['ph'])}"></textarea>
<input name="em" type="email" maxlength="120" autocomplete="email" aria-label="{e(a['email'])}" placeholder="{e(a['email'])}"><button class="btn" type="submit">{e(a['send'])}</button><p class="fb-done" role="status"></p></form></section>"""


def about(lang, up):
    return ask_box(lang) + _about(lang, up)


def _about(lang, up):
    U = LANGS[lang]["ui"]; x = X[lang]
    return f"""<p class="fb-line"><button type="button" class="linkbtn" data-feedback="">💬 {e(FEEDBACK[lang]['open'])}</button></p><details class="about"><summary>{e(x['about'])}</summary><div class="in">
<p><b>EasyModeKorea</b> (Easy Mode Korea · 이지모드코리아)</p>
<p>{e(U['how'])}</p><p>{e(U['indep'])}</p><p><a href="changes.html">{e(x['nav_changes'])}</a> · {U['hosts'].format(base=up)}</p>
<p>{' · '.join(f'<a href="{t["slug"]}.html">{e(QUESTION[lang][t["id"]])}</a>' for t in task_list(lang))}</p></div></details>"""


def task_list(lang):
    T = LANGS[lang]["tasks"]
    out = []
    for tid, slug, srcs in TASK_META:
        t = dict(T[tid]); t["id"] = tid; t["slug"] = slug; t["short"] = SHORT[lang]["tasks"][tid]
        t["sources"] = [SOURCES[s] for s in srcs]
        t["phrases"] = [[ko, m[lang]] for ko, m in PHRASES.get(tid, [])]
        t["icon"] = icon(tid)
        out.append(t)
    return out


def resolve(t, profile, device):
    if "all" in t: return t["all"]
    v = t["v"][profile]
    if isinstance(v, str): v = t["v"][v]
    if t.get("dev") and device in v: v = v[device]
    return v


SHOW_HTML = lambda lang: f"""<div class="show" id="show" hidden role="dialog" aria-modal="true" aria-labelledby="show-lbl">
  <div class="lbl" id="show-lbl"></div><div class="ko" lang="ko" id="show-ko"></div>
  <div><p class="mean" id="show-mean"></p><button class="btn" type="button" id="show-close">{e(SHORT[lang]['close'])}</button></div>
</div>"""

COMMON_JS = r"""
/* Arriving from a search result: start at the top (the answer box) instead of the middle of the page,
   where Google's highlighted-text links (#:~:text=) jump to. Links with a real #anchor are left alone. */
(function () { try {
  if (location.hash || !/google\.|bing\.|naver\.|yahoo\.|duckduckgo\.|daum\.|baidu\./i.test(document.referrer)) return;
  if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  const top = () => window.scrollTo(0, 0);
  addEventListener("load", () => { top(); setTimeout(top, 60); setTimeout(top, 300); });
} catch (e) {} })();
function el(tag, attrs = {}, kids = []) { const n = document.createElement(tag); for (const [k, v] of Object.entries(attrs)) { if (k === "text") n.textContent = v; else if (k === "html") n.innerHTML = v; else n.setAttribute(k, v); } for (const c of [].concat(kids)) if (c) n.append(c); return n; }
function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
function count(path, title) { try { if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({ path, title, event: true }); } catch (e) {} }
/* Full-screen card to hand the phone to staff or a driver. */
let lastFocus = null;
function show(label, ko, big, mean) {
  lastFocus = document.activeElement;
  document.getElementById("show-lbl").textContent = label;
  const k = document.getElementById("show-ko"); k.textContent = ko;
  if (big) k.append(el("small", { text: big }));
  document.getElementById("show-mean").textContent = mean || "";
  document.getElementById("show").hidden = false; document.getElementById("show-close").focus();
  try { if (navigator.wakeLock) navigator.wakeLock.request("screen").then(l => { wake = l; }).catch(() => {}); } catch (e) {}
  count("show-card", label);
}
let wake = null;
function hideShow() { document.getElementById("show").hidden = true; try { if (wake) wake.release(); } catch (e) {} wake = null; if (lastFocus) lastFocus.focus(); }
document.getElementById("show-close").addEventListener("click", hideShow);
document.addEventListener("keydown", ev => { if (ev.key === "Escape" && !document.getElementById("show").hidden) hideShow(); });
"""


def feedback_html(lang):
    f = FEEDBACK[lang]; c = SHORT[lang]['close']
    cfg = json.dumps({"form": FEEDBACK_FORM, "to": FEEDBACK_TO, "lang": lang, "thanks": f["thanks"]})
    return f"""<div class="sheet" id="fb" hidden role="dialog" aria-modal="true" aria-labelledby="fb-t"><div class="sheet-in">
  <div class="sheet-top"><h2 id="fb-t">{e(f['title'])}</h2><button type="button" class="btn ghost small" id="fb-close">{e(c)}</button></div>
  <p class="hint">{e(f['lead'])}</p>
  <form id="fb-form"><label class="fl" for="fb-msg">{e(f['msg'])}</label><textarea id="fb-msg" required maxlength="2000" placeholder="{e(f['ph'])}"></textarea>
  <label class="fl" for="fb-email">{e(f['email'])}</label><input id="fb-email" type="email" maxlength="120" autocomplete="email">
  <button class="btn" type="submit">{e(f['send'])}</button><p class="fb-done" id="fb-done" role="status"></p></form>
</div></div>
<script>(function () {{
  const C = {cfg}, sh = document.getElementById("fb"); let ctx = "";
  window.openFeedback = function (c) {{ ctx = c || location.pathname; sh.hidden = false; document.getElementById("fb-done").textContent = ""; document.getElementById("fb-msg").focus(); }};
  document.querySelectorAll("[data-feedback]").forEach(b => b.addEventListener("click", () => openFeedback(b.dataset.feedback)));
  document.getElementById("fb-close").addEventListener("click", () => {{ sh.hidden = true; }});
  sh.addEventListener("click", ev => {{ if (ev.target === sh) sh.hidden = true; }});
  document.getElementById("fb-form").addEventListener("submit", async ev => {{
    ev.preventDefault();
    const msg = document.getElementById("fb-msg").value.trim(), em = document.getElementById("fb-email").value.trim(); if (!msg) return;
    const where = C.lang + " " + ctx;
    if (C.form) {{
      const b = new URLSearchParams(); b.set(C.form.msg, msg); b.set(C.form.email, em); b.set(C.form.ctx, where);
      try {{ await fetch(C.form.action, {{ method: "POST", mode: "no-cors", body: b }}); }} catch (e) {{}}
    }} else {{
      location.href = "mailto:" + C.to + "?subject=" + encodeURIComponent("EasyModeKorea feedback (" + where + ")") + "&body=" + encodeURIComponent(msg + (em ? "\\n\\nReply to: " + em : ""));
    }}
    try {{ window.goatcounter && window.goatcounter.count({{ path: "feedback/" + C.lang, title: "feedback", event: true }}); }} catch (e) {{}}
    document.getElementById("fb-msg").value = ""; document.getElementById("fb-done").textContent = C.thanks;
  }});
  document.querySelectorAll(".ask-form").forEach(f => f.addEventListener("submit", async ev => {{
    ev.preventDefault();
    const q = f.q.value.trim(), em = f.em.value.trim(); if (!q) return;
    const where = C.lang + " question " + location.pathname;
    if (C.form) {{
      const b = new URLSearchParams(); b.set(C.form.msg, q); b.set(C.form.email, em); b.set(C.form.ctx, where);
      try {{ await fetch(C.form.action, {{ method: "POST", mode: "no-cors", body: b }}); }} catch (e) {{}}
    }} else {{
      location.href = "mailto:" + C.to + "?subject=" + encodeURIComponent("EasyModeKorea question (" + where + ")") + "&body=" + encodeURIComponent(q);
    }}
    try {{ window.goatcounter && window.goatcounter.count({{ path: "question/" + C.lang, title: "question", event: true }}); }} catch (e) {{}}
    f.q.value = ""; f.querySelector(".fb-done").textContent = f.dataset.thanks;
  }}));
}})();</script>"""


def help_html(lang):
    h = HELP[lang]
    nums = "".join(f'<a class="call" href="tel:{'+82-2-1330' if n == '1330' else n}"><b>{n}</b><span>{e(d)}</span></a>' for n, d in h["nums"])
    ph = "".join(f'<button type="button" class="btn alt" data-ko="{e(ko)}" data-mean="{e(m[lang])}">🗣 {e(m[lang])}</button>' for ko, m in HELP_PHRASES)
    return f"""<div class="sheet" id="help" hidden role="dialog" aria-modal="true" aria-labelledby="help-t"><div class="sheet-in">
  <div class="sheet-top"><h2 id="help-t">{e(h['title'])}</h2><button type="button" class="btn ghost small" id="help-close">{e(SHORT[lang]['close'])}</button></div>
  <p class="sub-h">{e(h['calls'])}</p><div class="calls">{nums}</div>
  <p class="sub-h">{e(h['phrases'])}</p><div class="actions">{ph}</div>
</div></div>"""


def build_tool(lang):
    L = LANGS[lang]; U = L["ui"]; x = X[lang]; S = SHORT[lang]; ux = UX[lang]; d = L["dir"]; up = "../" if d else ""
    path = d
    alt = {k: LANGS[k]["dir"] for k in LANGS}
    topics = "".join(f'<a href="{t["slug"]}.html">{e(t["short"])}</a>' for t in task_list(lang))
    keys = ("staff", "means", "stay_title", "taxi_card", "taxi_ko", "taxi_means", "deliv_card", "deliv_ko", "deliv_means", "station", "checkin", "contact", "note", "map")
    tasks = task_list(lang)
    for t in tasks:
        t["kw"] = (KEYWORDS[t["id"]] + " " + t["short"] + " " + t["title"]).lower()
        for k in ("title", "seo", "intro"): t.pop(k, None)  # not used by the page script
    data = {"ui": U, "x": {k: x[k] for k in keys}, "s": S, "ux": ux, "tasks": tasks, "plan": PLAN[lang], "fbfail": FEEDBACK[lang]["fail"], "checked": CHECKED[lang], "lang": lang,
            "found": [A.T[lang]["deep_faq"], A.T[lang]["deep_cards"]],
            "langs": {k: {"name": LANGS[k]["name"], "dir": LANGS[k]["dir"]} for k in LANGS}, "up": up}
    q1 = "".join(f'<button type="button" class="opt-big" data-p="{p}"><b>{e(ux["q1_opts"][p][0])}</b><span>{e(ux["q1_opts"][p][1])}</span></button>' for p in ("visitor", "krsim", "arc"))
    q2 = "".join(f'<button type="button" class="opt-big" data-d="{v}"><b>{e(U[v])}</b></button>' for v in ("ios", "android"))
    LU = layout.UI.get(lang, layout.UI["en"])
    short_of = {t["id"]: t["short"] for t in tasks}
    slug_of = {t["id"]: t["slug"] for t in tasks}
    cards = []
    for cid, ic, ids, txt in CARDS:
        title, line = tx(txt, lang)
        links = "".join(f'<a href="{slug_of[i]}.html" data-t="{i}">{e(short_of[i])}</a>' for i in ids)
        ckw = (title + " " + line).lower()
        cards.append(f'<article class="sit-card" id="s-{cid}" data-kw="{e(ckw)}"><h3>{icon(ic)}<span>{e(title)}</span></h3><p>{e(line)}</p><p class="sit-links">{links}</p></article>')
    body = f"""
{hero(lang, alt, up, x['hook'], LU['lede'], search=False)}
<div class="wrap pre">
  <div class="banner" id="lang-suggest" hidden></div>
  <section class="stay" id="stay" hidden aria-live="polite"></section>
</div>
<div class="wrap">
  <label class="search"><span class="sr">{e(ux['search'])}</span><input id="q" type="search" placeholder="{e(ux['search'])}" autocomplete="off"></label>
  <p class="hint" id="nores" hidden>{e(ux['nores'])} <button type="button" class="linkbtn" id="clear">{e(ux['clear'])}</button></p>
  <section class="sit" aria-labelledby="sit-h"><h2 id="sit-h">{e(LU['cards_h'])}</h2><div class="sit-grid">{''.join(cards)}</div></section>
  <div class="found" id="found" aria-live="polite"></div>
  <section class="tool" aria-labelledby="tool-h"><h2 id="tool-h" class="tool-h">{e(LU['tool_h'])}</h2>
  <div class="onb" id="onb" aria-live="polite">
    <div id="onb1"><h3>{e(ux['q1'])}</h3><p class="why">{e(ux['why'])}</p><div class="opts-big">{q1}</div></div>
    <div id="onb2" hidden><h3>{e(ux['q2'])}</h3><div class="opts-big two">{q2}</div><button type="button" class="linkbtn" id="onb-back">← {e(ux['back'])}</button></div>
  </div></section>
</div>
<div class="mybar" id="mybar" hidden><div class="wrap"><span id="mysetup"></span><span class="bar-btns"><button type="button" class="btn ghost small" id="help-btn">{e(HELP[lang]['btn'])}</button><button type="button" class="btn ghost small" id="change">{e(ux['change'])}</button></span></div></div>
<div class="wrap" id="main" hidden>
  <main class="rows" id="rows"></main>
  <details class="panel" id="cl"><summary><span id="ptitle"></span> <span class="count" id="pcount"></span></summary><div class="in">
    <div class="progress"><div class="bar"><i id="pbar"></i></div></div>
    <ul class="checks" id="checklist"></ul>
    <div class="actions"><button class="btn" type="button" id="copy-btn">{e(U['copy'])}</button><span class="copied" id="copied" role="status"></span></div>
  </div></details>
</div>
<div class="wrap">
  <p class="offline-note">⚡ {e(LU['offline'])}</p>
  {about(lang, up)}
</div>
{help_html(lang)}
{SHOW_HTML(lang)}
<script>
const D = {json.dumps(data, ensure_ascii=False)};
{COMMON_JS}
{TOOL_JS}
</script>
{footer(lang)}
{feedback_html(lang)}
</body>
</html>
"""
    site_ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "alternateName": ["Easy Mode Korea", "이지모드코리아", "이지모드 코리아", "easymodekorea.com"], "url": SITE, "inLanguage": L["html_lang"]},
               {"@context": "https://schema.org", "@type": "Organization", "name": BRAND, "url": SITE, "logo": SITE + "icon-512.png", "email": "edandco.biz@gmail.com"}]
    extra = ("\n" + A.LAUNCH_JS if lang == "en" else "") + f'\n<script type="application/ld+json">{json.dumps(site_ld, ensure_ascii=False)}</script>'
    write(path + "index.html", head(lang, f"{BRAND} | {x['home_title']}", x["home_desc"], path, alt, extra) + body)
    return path


TOOL_JS = r"""
const U = D.ui, XS = D.x, S = D.s, UX = D.ux, FB_FAIL = D.fbfail;
const KW = Object.fromEntries(D.tasks.map(t => [t.id, t.kw]));
let P = null, DEV = null;
function resolve(t, p, dev) { if (t.all) return t.all; let v = t.v[p]; if (typeof v === "string") v = t.v[v]; if (t.dev && v[dev]) v = v[dev]; return v; }
function setStep(n) { document.getElementById("onb1").hidden = n !== 1; document.getElementById("onb2").hidden = n !== 2; }
function openOnb(focus) { document.getElementById("onb").hidden = false; document.getElementById("main").hidden = true; document.getElementById("mybar").hidden = true; setStep(1); if (focus) { document.getElementById("tool-h").scrollIntoView(); document.querySelector("#onb1 .opt-big").focus({ preventScroll: true }); } }
function finish() {
  store("wik-setup", P + "|" + DEV); document.body.classList.add("ret");
  document.getElementById("onb").hidden = true; document.getElementById("main").hidden = false; document.getElementById("mybar").hidden = false;
  document.getElementById("mysetup").textContent = S.prof[P] + " · " + U[DEV];
  render(); count("setup/" + D.lang + "/" + P + "/" + DEV, "setup");
  if (fromOnb) document.getElementById("tool-h").scrollIntoView();
}
let fromOnb = false;
/* The phone type is usually readable from the browser, so most people answer one question. */
const UAD = /iPhone|iPad|iPod/.test(navigator.userAgent) ? "ios" : /Android/.test(navigator.userAgent) ? "android" : null;
document.querySelectorAll("[data-p]").forEach(b => b.addEventListener("click", () => { P = b.dataset.p; if (P === "arc") { DEV = "ios"; fromOnb = true; finish(); } else if (UAD) { DEV = UAD; fromOnb = true; finish(); } else { setStep(2); document.querySelector("#onb2 .opt-big").focus(); } }));
document.querySelectorAll("[data-d]").forEach(b => b.addEventListener("click", () => { DEV = b.dataset.d; fromOnb = true; finish(); }));
document.querySelectorAll("#onb [data-p]").forEach(b => b.addEventListener("click", () => { fromOnb = true; }));
/* One answer open at a time keeps the list short on a phone. */
document.getElementById("rows").addEventListener("toggle", ev => {
  const r = ev.target; if (!r.classList || !r.classList.contains("row") || !r.open) return;
  document.querySelectorAll(".row[open]").forEach(o => { if (o !== r) o.open = false; });
  count("open/" + r.id, "open answer");
}, true);
const helpEl = document.getElementById("help");
document.getElementById("help-btn").addEventListener("click", () => { helpEl.hidden = false; document.getElementById("help-close").focus(); count("help", "help"); });
document.getElementById("help-close").addEventListener("click", () => { helpEl.hidden = true; document.getElementById("help-btn").focus(); });
helpEl.addEventListener("click", ev => { if (ev.target === helpEl) helpEl.hidden = true; });
helpEl.querySelectorAll("[data-ko]").forEach(b => b.addEventListener("click", () => show(S.show, b.dataset.ko, "", XS.means + ": " + b.dataset.mean)));
document.addEventListener("keydown", ev => { if (ev.key === "Escape" && !helpEl.hidden && document.getElementById("show").hidden) helpEl.hidden = true; });
document.getElementById("onb-back").addEventListener("click", () => setStep(1));
document.getElementById("change").addEventListener("click", () => openOnb(true));
function render() {
  const open = new Set([...document.querySelectorAll(".row[open]")].map(r => r.id));
  const rows = document.getElementById("rows"); rows.replaceChildren();
  const n = { ok: 0, warn: 0, mixed: 0, bad: 0 };
  let moreShown = false;
  for (const t of D.tasks) {
    if (t.more && !moreShown) { rows.append(el("h2", { class: "more-h", text: UX.more })); moreShown = true; }
    const v = resolve(t, P, DEV); n[v.s]++;
    const row = el("details", { class: "row " + v.s + (t.more ? " more" : ""), id: "task-" + t.id, "data-kw": t.kw });
    if (open.has(row.id)) row.open = true;
    const sum = el("summary");
    const txt = el("span", { class: "txt" }, [el("span", { class: "name", text: t.short }), el("span", { class: "pill " + v.s, text: UX.tone[v.s] })]);
    sum.append(el("span", { class: "ic", html: t.icon }), txt);
    row.append(sum);
    const body = el("div", { class: "body" });
    body.append(el("p", { class: "verdict", text: v.verdict }));
    body.append(el("ol", { class: "steps" }, v.route.map(r => el("li", { text: r }))));
    const fb = el("p", { class: "fallback" }); fb.append(el("b", { text: U.fails.replace(/[:：]\s*$/, "") }), v.fallback); body.append(fb);
    const act = el("div", { class: "actions" });
    for (const [ko, m] of t.phrases) { const b = el("button", { type: "button", class: "btn alt", text: "🗣 " + m }); b.addEventListener("click", () => show(S.show, ko, "", XS.means + ": " + m)); act.append(b); }
    if (act.children.length) body.append(act);
    const det = el("details"); det.append(el("summary", { text: S.details })); const ul = el("ul");
    for (const x of (t.notes || [])) ul.append(el("li", { text: x }));
    for (const [nm, url] of t.sources) { const li = el("li"); li.append(el("a", { href: url, rel: "noopener", target: "_blank", text: nm })); ul.append(li); }
    det.append(ul);
    const gl = el("p"); gl.append(el("a", { href: t.slug + ".html", text: S.guide + " →" })); det.append(gl);
    const key = "wik-report-" + t.id + "-" + P, rep = el("div", { class: "report" }), thx = el("span", { role: "status" });
    for (const [val, txt2] of [["yes", U.worked], ["no", U.failed]]) {
      const b = el("button", { type: "button", "aria-pressed": String(store(key) === val), text: txt2 });
      b.addEventListener("click", () => {
        if (store(key) !== val) count(`report/${D.lang}/${t.id}/${P}/${DEV}/${val}`, `${t.id} ${P} ${val}`);
        store(key, val); rep.querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", String(x === b))); thx.textContent = U.thanks;
        if (val === "no" && window.openFeedback) { const fl = el("button", { type: "button", class: "linkbtn", text: FB_FAIL }); fl.addEventListener("click", () => openFeedback(t.id + " " + P + " " + DEV)); thx.replaceChildren(U.thanks + " ", fl); }
      });
      rep.append(b);
    }
    rep.append(thx);
    ul.prepend(el("li", { text: U.checked + " " + D.checked })); det.append(rep);
    body.append(det);
    row.append(body); rows.append(row);
  }
  checklist(); filter();
}
function checklist() {
  const pl = D.plan, items = pl.items.filter(it => (!it.p || it.p.includes(P)) && (!it.d || P === "arc" || it.d.includes(DEV)));
  document.getElementById("ptitle").textContent = P === "arc" ? pl.title_arc : pl.title;
  const key = "wik-plan-" + D.lang + "-" + P + "-" + DEV;
  let done = []; try { done = JSON.parse(store(key) || "[]"); } catch (e) {}
  const ul = document.getElementById("checklist"); ul.replaceChildren(); let last = "";
  items.forEach((it, i) => {
    if (it.st !== last) { ul.append(el("li", { class: "stage", text: pl.stages[it.st] })); last = it.st; }
    const id = "ck-" + i, cb = el("input", { type: "checkbox", id });
    cb.checked = done.includes(i);
    cb.addEventListener("change", () => { done = cb.checked ? [...new Set([...done, i])] : done.filter(j => j !== i); store(key, JSON.stringify(done)); progress(done.length, items.length); });
    ul.append(el("li", {}, [cb, el("label", { for: id, text: it.t })]));
  });
  progress(done.length, items.length);
}
function progress(d, n) { document.getElementById("pcount").textContent = d + "/" + n; document.getElementById("pbar").style.width = Math.round(100 * d / n) + "%";  }
function filter() {
  const q = document.getElementById("q").value.trim().toLowerCase(); let shown = 0;
  let moreHits = 0;
  document.querySelectorAll(".row").forEach(r => { const ok = !q || r.dataset.kw.includes(q); r.hidden = !ok; if (ok) { shown++; if (r.classList.contains("more")) moreHits++; } });
  const mh = document.querySelector(".more-h"); if (mh) mh.hidden = !!q && !moreHits;
  let cardHits = 0;
  document.querySelectorAll(".sit-card").forEach(c => {
    const links = [...c.querySelectorAll("a[data-t]")];
    let any = false;
    links.forEach(a => { const ok = !q || KW[a.dataset.t].includes(q); a.hidden = !ok; if (ok) any = true; });
    if (!any && c.dataset.kw.includes(q)) { any = true; links.forEach(a => { a.hidden = false; }); }
    c.hidden = !any; if (any) cardHits++;
  });
  /* Deeper matches from the search index: questions answered inside guides, and Korean cards. */
  const found = document.getElementById("found"); found.replaceChildren(); let deep = 0;
  if (q.length >= 2 && IDX) {
    const fq = IDX.faq.filter(x => x[2].toLowerCase().includes(q)).slice(0, 6), cd = IDX.cards.filter(x => (x[0] + " " + x[1]).toLowerCase().includes(q)).slice(0, 6);
    if (fq.length) { found.append(el("h2", { text: D.found[0] }), el("ul", { class: "glist" }, fq.map(x => el("li", {}, el("a", { href: x[0] + ".html#fq-" + x[1], text: x[2] }))))); }
    if (cd.length) { found.append(el("h2", { text: D.found[1] }), el("ul", { class: "glist" }, cd.map(x => { const b = el("button", { type: "button", class: "card-hit" }, [el("b", { lang: "ko", text: x[0] }), el("span", { text: x[1] })]); b.addEventListener("click", () => show(S.show, x[0], "", XS.means + ": " + x[1])); return el("li", {}, b); }))); }
    deep = fq.length + cd.length;
  }
  document.getElementById("nores").hidden = !q || shown + cardHits + deep > 0;
  if (q && shown === 1) { const r = [...document.querySelectorAll(".row")].find(x => !x.hidden); r.open = true; }
}
/* The search index (questions and Korean cards) loads the first time the box is used. */
let IDX = null;
function loadIdx() { if (IDX !== null) return; IDX = false; fetch("search.json").then(r => r.json()).then(j => { IDX = j; filter(); }).catch(() => { IDX = null; }); }
document.getElementById("q").addEventListener("focus", loadIdx);
document.getElementById("q").addEventListener("input", filter);
document.getElementById("clear").addEventListener("click", () => { const q = document.getElementById("q"); q.value = ""; filter(); q.focus(); });
document.getElementById("copy-btn").addEventListener("click", async () => {
  const txt = document.getElementById("ptitle").textContent + "\n" + [...document.querySelectorAll("#checklist li")].map(l => l.classList.contains("stage") ? "\n" + l.textContent : "- " + l.textContent).join("\n") + "\n" + location.origin + location.pathname;
  try { await navigator.clipboard.writeText(txt); document.getElementById("copied").textContent = "✓"; } catch (e) {}
  count("copy-checklist/" + D.lang, "copy checklist");
});
function stay() {
  let g = null;
  try { const m = location.hash.match(/[#&]g=([A-Za-z0-9_-]+)/); if (m) { const b = atob(m[1].replace(/-/g, "+").replace(/_/g, "/")); g = JSON.parse(new TextDecoder().decode(Uint8Array.from(b, c => c.charCodeAt(0)))); } } catch (e) { g = null; }
  if (!g || typeof g !== "object") return;
  const s = (k, n) => String(g[k] || "").slice(0, n);
  const box = document.getElementById("stay");
  box.append(el("h2", { text: XS.stay_title + (s("n", 60) ? ": " + s("n", 60) : "") }));
  const a = s("a", 160);
  if (a) {
    store("emk-addr", a);
    box.append(el("div", { class: "addr", lang: "ko", text: a }));
    const act = el("div", { class: "actions" });
    const t1 = el("button", { type: "button", class: "btn alt", text: S.show_driver }); t1.addEventListener("click", () => show(XS.taxi_card, XS.taxi_ko, a, XS.means + ": " + XS.taxi_means));
    const t2 = el("button", { type: "button", class: "btn ghost", text: XS.deliv_card }); t2.addEventListener("click", () => show(XS.deliv_card, a, XS.deliv_ko, XS.means + ": " + XS.deliv_means));
    const cp = el("button", { type: "button", class: "btn ghost", text: UX.copy_addr });
    cp.addEventListener("click", async () => { try { await navigator.clipboard.writeText(a); cp.textContent = "✓ " + UX.copied; setTimeout(() => { cp.textContent = UX.copy_addr; }, 2000); count("copy-address", "copy address"); } catch (e) {} });
    act.append(t1, cp, t2, el("a", { class: "btn ghost", href: "https://map.naver.com/p/search/" + encodeURIComponent(a), rel: "noopener", target: "_blank", text: XS.map }));
    box.append(act);
  }
  const dl = el("dl", { class: "kv" });
  for (const [k, lbl, n] of [["s", XS.station, 80], ["c", XS.checkin, 40], ["k", XS.contact, 80], ["t", XS.note, 280]]) if (s(k, n)) dl.append(el("dt", { text: lbl }), el("dd", { text: s(k, n) }));
  if (dl.children.length) box.append(dl);
  box.hidden = false;
  if (s("n", 60)) count(`host/${s("n", 60)}`, "host stay page");
}
/* Suggest the reader's language once. */
(function () {
  if (store("wik-lang-dismiss")) return;
  const want = (navigator.language || "").toLowerCase();
  const target = want.startsWith("ja") ? "ja" : (want.startsWith("zh-tw") || want.startsWith("zh-hk") || want.startsWith("zh-mo") || want.startsWith("zh-hant")) ? "zh-tw" : want.startsWith("zh") ? "zh-cn" : want.startsWith("vi") ? "vi" : want.startsWith("en") ? "en" : null;
  if (!target || target === D.lang) return;
  const b = document.getElementById("lang-suggest"), L2 = D.langs[target];
  const go = el("a", { class: "btn alt", href: D.up + L2.dir + location.hash, text: UX.switch }); go.addEventListener("click", () => store("emk-lang", target));
  const no = el("button", { type: "button", class: "linkbtn", text: UX.dismiss }); no.addEventListener("click", () => { store("wik-lang-dismiss", "1"); b.hidden = true; });
  b.append(el("span", { text: UX.suggest.replace("{l}", L2.name) }), go, no); b.hidden = false;
})();
/* Install prompt, offline copy and notices live in app.js, shared by every page. */
if (location.hash === "#q") { const qi = document.getElementById("q"); qi.focus(); loadIdx(); }
const saved = (store("wik-setup") || "").split("|");
if (saved[0] && S.prof[saved[0]] && (saved[1] === "ios" || saved[1] === "android")) { P = saved[0]; DEV = saved[1]; finish(); } else { openOnb(/^#task-/.test(location.hash)); }
stay();
const target = location.hash.match(/^#task-[\w-]+$/); if (target && P) { const r = document.querySelector(target[0]); if (r) { r.open = true; r.scrollIntoView(); } }
"""


TOPIC_JS = r"""
(function () {
  document.querySelectorAll("[data-show]").forEach(b => b.addEventListener("click", () => show(b.dataset.lbl, b.dataset.show, "", b.dataset.mean)));
  const saved = (store("wik-setup") || "visitor|ios").split("|");
  document.querySelectorAll("[data-copy]").forEach(b => b.addEventListener("click", async () => {
    let ok = false;
    try { await navigator.clipboard.writeText(b.dataset.copy); ok = true; } catch (e) {}
    if (!ok) { const ta = document.createElement("textarea"); ta.value = b.dataset.copy; ta.setAttribute("readonly", ""); ta.style.cssText = "position:fixed;opacity:0"; document.body.append(ta); ta.select(); try { ok = document.execCommand("copy"); } catch (e) {} ta.remove(); }
    if (!ok) { const t = b.querySelector("[lang=ko]") || b.closest(".say")?.querySelector(".say-ko"); if (t) { const r = document.createRange(); r.selectNodeContents(t); const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r); } return; }
    const was = b.innerHTML; b.classList.add("done"); b.setAttribute("aria-label", b.dataset.done);
    const tip = document.createElement("span"); tip.className = "tip"; tip.textContent = b.dataset.done; tip.setAttribute("role", "status"); b.append(tip);
    setTimeout(() => { b.innerHTML = was; b.classList.remove("done"); b.removeAttribute("aria-label"); }, 1600);
    count("copy/" + location.pathname, "copy korean");
  }));
  /* The stay address lives only in this browser (localStorage), never in a URL or a request. */
  const ma = document.getElementById("myaddr");
  if (ma) {
    const has = document.getElementById("ma-has"), form = document.getElementById("ma-form"), inp = document.getElementById("ma-in");
    const paint = () => {
      const a = (store("emk-addr") || "").slice(0, 160);
      has.hidden = !a; form.hidden = !!a;
      if (a) { document.getElementById("ma-text").textContent = a; document.getElementById("ma-copy").dataset.copy = a; document.getElementById("ma-map").href = "https://map.naver.com/p/search/" + encodeURIComponent(a); }
    };
    form.addEventListener("submit", ev => { ev.preventDefault(); const v = inp.value.trim(); if (v) { store("emk-addr", v); count("addr-saved", "address saved"); } paint(); });
    document.getElementById("ma-edit").addEventListener("click", () => { inp.value = store("emk-addr") || ""; has.hidden = true; form.hidden = false; inp.focus(); });
    document.getElementById("ma-show").addEventListener("click", () => show(ma.dataset.card, ma.dataset.ko, store("emk-addr") || "", ma.dataset.mean));
    ma.hidden = false; paint();
  }
  /* A link to a folded section opens it. */
  const h = location.hash && document.getElementById(location.hash.slice(1)); if (h && h.tagName === "DETAILS") h.open = true;
  const blocks = [...document.querySelectorAll(".pv[data-p]")];
  if (blocks.length < 2) return;
  let shown = 0;
  for (const b of blocks) { const ok = b.dataset.p === saved[0] && (!b.dataset.d || b.dataset.d === saved[1]); b.hidden = !ok; if (ok) shown++; }
  if (!shown) { blocks.forEach(b => b.hidden = false); return; }
  const btn = document.getElementById("show-all"); btn.hidden = false;
  btn.addEventListener("click", () => { blocks.forEach(b => b.hidden = false); btn.hidden = true; });
})();
"""


# Related guides shown under each guide, with the question as descriptive anchor text.
# First publish dates (ISO) for the Article schema; pages not listed fall back to the checked date.
PUBLISHED = {"k-eta-entry-requirements": "2026-11-19", "atm-foreign-card-cash": "2026-11-19", "korea-power-plug-voltage": "2026-11-19",
             "seoul-to-busan-k-tour-pass": "2026-11-19", "kr-pass-korail-pass": "2026-11-19", "dmz-jsa-tour-booking": "2026-11-19",
             "jeju-getting-around": "2026-11-19", "seoul-tourist-transit-pass": "2026-11-19",
             "gimpo-airport-to-seoul": "2026-11-20"}
FIRST_PUBLISH = "2026-11-17"

RELATED = {
    "data": ["entry", "airport", "taxi", "power"],
    "airport": ["transit", "luggage", "taxi", "gimpo"],
    "maps": ["translate", "taxi", "transit"],
    "taxi": ["maps", "airport", "data", "jeju"],
    "transit": ["airport", "cash", "maps", "transitpass"],
    "ktx": ["transit", "food-booking", "luggage", "busan", "krpass"],
    "food-booking": ["delivery", "translate", "cash"],
    "delivery": ["food-booking", "translate", "data"],
    "translate": ["maps", "food-booking", "health"],
    "shopping": ["cash", "luggage", "transit"],
    "luggage": ["airport", "ktx", "shopping"],
    "health": ["translate", "data", "entry"],
    "entry": ["data", "airport", "cash", "power"],
    "cash": ["transit", "shopping", "entry"],
    "power": ["data", "entry", "airport"],
    "gimpo": ["transit", "taxi", "jeju", "airport"],
    "busan": ["ktx", "luggage", "cash", "krpass"],
    "krpass": ["ktx", "busan", "transit"],
    "dmz": ["ktx", "data", "translate"],
    "jeju": ["gimpo", "taxi", "cash"],
    "transitpass": ["transit", "airport", "maps"],
}


def fmt_date(iso, lang):
    y, m, d = iso.split("-")
    if lang == "en": return f"{int(d)} {['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(m)-1]} {y}"
    if lang == "vi": return f"{int(d)}/{int(m)}/{y}"
    return f"{y}年{int(m)}月{int(d)}日"


def build_topic(lang, t):
    """Guide page, short first: answer box (verdict, key facts with check dates, source stamp),
    numbered steps, phrase and copy cards, then the long-form detail folded in <details>."""
    L = LANGS[lang]; U = L["ui"]; x = X[lang]; S = SHORT[lang]; d = L["dir"]; up = "../" if d else ""
    LU = layout.UI.get(lang, layout.UI["en"]); H = DEEP_HEAD[lang]
    path = f"{d}{t['slug']}.html"
    alt = {k: f"{LANGS[k]['dir']}{t['slug']}.html" for k in LANGS}
    fail_lbl = U["fails"].strip().rstrip(":：").strip()
    tops, dos = [], []
    profiles = ["visitor", "krsim", "arc"] if "all" not in t else [None]
    for p in profiles:
        devices = ["ios", "android"] if t.get("dev") and p != "arc" else [None]
        for dv in devices:
            v = resolve(t, p or "visitor", dv or "ios")
            heading = U["for_profile"][p] if p else UX[lang]["tone"][v["s"]]
            if dv: heading += f" · {U[dv]}"
            attrs = (f' data-p="{p}"' if p else "") + (f' data-d="{dv}"' if dv else "")
            route = "".join(f"<li>{e(r)}</li>" for r in v["route"])
            tops.append(f'<div class="pv {v["s"]}"{attrs}><div class="ans-top"><h2{'' if p else ' class="sr"'}>{e(heading)}</h2><span class="pill {v["s"]}">{e(UX[lang]["tone"][v["s"]])}</span></div><p class="verdict">{e(v["verdict"])}</p></div>')
            dos.append(f'<div class="pv"{attrs}><ol class="steps">{route}</ol><p class="fallback"><b>{e(fail_lbl)}</b>{e(v["fallback"])}</p></div>')
    rows = AT.get(t["id"], [])
    glance = "".join(f'<div><dt>{e(LU[k])}</dt><dd>{e(tx(m, lang))} <time class="ck" datetime="{dt}">✓ {e(fmt_date(dt, lang))}</time></dd></div>' for k, m, dt in rows)
    stamp_date = max([r[2] for r in rows] or [CHECKED_ISO])
    g = DEEP.get(t["id"])
    src_name, src_url = (g["cites"][0] if g else t["sources"][0])
    stamp = LU["stamp"].format(src=f'<a href="{e(src_url)}" rel="noopener" target="_blank">{e(src_name)}</a>', date=f'<time datetime="{stamp_date}">{e(fmt_date(stamp_date, lang))}</time>')
    first_s = resolve(t, "visitor", "ios")["s"]
    say = "".join(f'<div class="say"><p class="say-ko" lang="ko">{e(ko)}</p><p class="say-mean">{e(m)}</p><div class="actions"><button class="btn alt" type="button" data-show="{e(ko)}" data-lbl="{e(S["show"])}" data-mean="{e(x["means"])}: {e(m)}">🗣 {e(LU["full"])}</button><button class="btn ghost" type="button" data-copy="{e(ko)}" data-done="✓ {e(LU["copied"])}">📋 {e(LU["copy"])}</button></div></div>' for ko, m in t["phrases"])
    names = "".join(f'<li><button class="chip" type="button" data-copy="{e(ko)}" data-done="✓ {e(LU["copied"])}"><span lang="ko">{e(ko)}</span><small>{e(tx(m, lang))}</small><i aria-hidden="true">📋</i></button></li>' for ko, m in COPY.get(t["id"], []))
    addr_html = addr_card(lang) if t["id"] in ADDR_GUIDES else ""
    names_html = f'<section class="names" aria-labelledby="nm-{t["id"]}"><h2 id="nm-{t["id"]}">{e(LU["names_h"])}</h2><ul>{names}</ul></section>' if names else ""
    notes = "".join(f"<li>{e(n)}</li>" for n in t.get("notes", []))
    srcs = "".join(f'<li><a href="{e(u)}" rel="noopener" target="_blank">{e(n)}</a></li>' for n, u in t["sources"])
    others = "".join(f'<a href="{o["slug"]}.html">{e(o["short"])}</a>' for o in task_list(lang) if o["id"] != t["id"])
    slug_of = {tid: sl for tid, sl, _ in TASK_META}
    related = "".join(f'<li><a href="{slug_of[r]}.html">{e(QUESTION[lang][r])}</a></li>' for r in RELATED.get(t["id"], []))
    deep, faq_extra = deep_html(lang, t["id"])
    body = f"""
<a class="skip" href="#answer">{e(H['skip'])}</a>
{hero(lang, alt, up, QUESTION[lang][t['id']], '', back=True)}
<div class="wrap">
  <main id="answer">
  <section class="answer {first_s}">{''.join(tops)}<dl class="glance">{glance}</dl><p class="stamp">{stamp}</p></section>
  <button class="linkbtn" type="button" id="show-all" hidden>{e(x['others'])}</button>
  <section class="do" aria-labelledby="do-{t['id']}"><h2 id="do-{t['id']}" class="sr">{e(H['steps'])}</h2>{''.join(dos)}</section>
  {f'<section class="says" aria-labelledby="say-{t["id"]}"><h2 id="say-{t["id"]}">{e(LU["say_h"])}</h2>{say}</section>' if say else ''}
  {names_html}
  {addr_html}
  <div class="actions"><a class="btn" href="./#task-{t['id']}">{e(U['open_tool'])}</a></div>
  {deep}
  <details class="more"><summary>{e(S['details'])}</summary><div class="in notes"><p>{e(t['intro'])}</p><ul><li>{e(U['checked'])} {e(CHECKED[lang])}</li>{notes}{srcs}</ul></div></details>
  </main>
  <section class="related"><h2>{e(x['related'])}</h2><ul>{related}</ul></section>
  <details class="more"><summary>{e(LU['all'])}</summary><nav class="topics">{others}</nav></details>
  <p class="host-cta">🏠 {U['hosts'].format(base=up)}</p>
  {about(lang, up)}
</div>
{SHOW_HTML(lang)}
<script>{COMMON_JS}{TOPIC_JS}</script>
{footer(lang)}
{feedback_html(lang)}
</body>
</html>
"""
    first = resolve(t, "visitor", "ios")
    answer = first["verdict"] + " " + " ".join(first["route"])
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": t["seo"], "description": t["intro"], "datePublished": PUBLISHED.get(t["slug"], FIRST_PUBLISH), "dateModified": page_date(path, body), "inLanguage": L["html_lang"], "url": SITE + path, "mainEntityOfPage": SITE + path, "image": SITE + "og.png", "author": {"@type": "Organization", "name": BRAND, "url": SITE + L["dir"] + "about.html"}, "publisher": {"@type": "Organization", "name": BRAND, "url": SITE, "logo": {"@type": "ImageObject", "url": SITE + "icon-512.png"}}},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": BRAND, "item": SITE + L["dir"]}, {"@type": "ListItem", "position": 2, "name": t["short"], "item": SITE + path}]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": QUESTION[lang][t["id"]], "acceptedAnswer": {"@type": "Answer", "text": answer}}] + [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_extra]}]
    ldtag = f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    write(path, head(lang, f"{t['seo']} | {BRAND}", t["intro"], path, alt, ldtag, guide=t["slug"]) + body)
    return path


def build_changes(lang):
    L = LANGS[lang]; x = X[lang]; d = L["dir"]; up = "../" if d else ""
    path = f"{d}changes.html"
    alt = {k: f"{LANGS[k]['dir']}changes.html" for k in LANGS}
    rows = "".join(f'<li><b>{e(dt)}</b>{e(tx)}</li>' for dt, tx in x["changes"])
    body = f"""
{hero(lang, alt, up, x['changes_title'], '')}
<div class="wrap">
  <section class="panel" style="margin-top:18px"><div class="in timeline" style="padding-top:16px"><ol>{rows}</ol></div></section>
  <div class="actions"><a class="btn" href="./">{e(L['ui']['open_tool'])}</a></div>
  {ask_box(lang)}
  <p class="fb-line"><button type="button" class="linkbtn" data-feedback="changes">💬 {e(FEEDBACK[lang]['open'])}</button></p>
</div>
{footer(lang, "")}
{feedback_html(lang)}
</body>
</html>
"""
    write(path, head(lang, f"{x['changes_title']} | {BRAND}", x["changes_lead"], path, alt) + body)
    return path


# Per-page modified dates. src/page_dates.json stores a hash of each page's content and the
# date it last changed, so the sitemap and dateModified move only for pages that changed.
DATES_FILE = os.path.join(os.path.dirname(__file__), "page_dates.json")
DATES = json.load(open(DATES_FILE, encoding="utf-8")) if os.path.exists(DATES_FILE) else {}
DATED = set()  # pages already dated from their body during this build
TODAY = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().isoformat()


def page_date(path, content):
    h = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
    DATED.add(path)
    rec = DATES.get(path)
    if not rec or rec["h"] != h:
        DATES[path] = rec = {"h": h, "d": TODAY}
    return rec["d"]


def footer(lang, tab="guides"):
    """Site links, then the bottom tabs (tab names the active one)."""
    P = PAGES[lang]; up = "../" if LANGS[lang]["dir"] else ""
    links = [("about.html", P["about"]), ("contact.html", P["contact"]), ("changes.html", P["changes"]), ("privacy.html", A.T[lang]["privacy"]), (f"{up}hosts.html", P["hosts"])]
    return ('<footer class="foot"><div class="wrap"><nav aria-label="EasyModeKorea">' + " · ".join(f'<a href="{h}">{e(t)}</a>' for h, t in links)
            + f'</nav><p>EasyModeKorea · <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p></div></footer>\n' + A.tabbar(lang, tab))


def addr_card(lang):
    """The saved stay address: show a driver, copy, open in Naver Map. Kept on the phone only."""
    x = X[lang]; S = SHORT[lang]; LU = layout.UI.get(lang, layout.UI["en"])
    return f"""<section class="myaddr" id="myaddr" hidden aria-labelledby="ma-h" data-card="{e(x['taxi_card'])}" data-ko="{e(x['taxi_ko'])}" data-mean="{e(x['means'])}: {e(x['taxi_means'])}"><h2 id="ma-h">{e(LU['addr_h'])}</h2>
<div id="ma-has" hidden><p class="addr" lang="ko" id="ma-text"></p><div class="actions"><button class="btn alt" type="button" id="ma-show">🚕 {e(S['show_driver'])}</button><button class="btn ghost" type="button" id="ma-copy" data-copy="" data-done="✓ {e(LU['copied'])}">📋 {e(UX[lang]['copy_addr'])}</button><a class="btn ghost" id="ma-map" href="#" rel="noopener" target="_blank">{e(x['map'])}</a><button class="linkbtn" type="button" id="ma-edit">{e(LU['addr_edit'])}</button></div></div>
<form id="ma-form" hidden><input id="ma-in" type="text" lang="ko" maxlength="160" autocomplete="street-address" aria-label="{e(LU['addr_h'])}" placeholder="{e(LU['addr_ph'])}"><button class="btn" type="submit">{e(LU['addr_save'])}</button></form><p class="hint">{e(LU['addr_note'])}</p></section>"""


def say_card(lang, ko, mean, kw=""):
    """One Korean card: big Korean, its meaning, show full screen, copy."""
    x = X[lang]; S = SHORT[lang]; LU = layout.UI.get(lang, layout.UI["en"])
    return (f'<div class="say" data-kw="{e((mean + " " + ko + " " + kw).lower())}"><p class="say-ko" lang="ko">{e(ko)}</p><p class="say-mean">{e(mean)}</p><div class="actions">'
            f'<button class="btn alt" type="button" data-show="{e(ko)}" data-lbl="{e(S["show"])}" data-mean="{e(x["means"])}: {e(mean)}">🗣 {e(LU["full"])}</button>'
            f'<button class="btn ghost" type="button" data-copy="{e(ko)}" data-done="✓ {e(LU["copied"])}">📋 {e(LU["copy"])}</button></div></div>')


def app_page(lang, name, title, seo, desc, inner, tab, script="", index=True, ld=None):
    """Shared frame for the app pages (Korean cards, My trip, help, privacy)."""
    L = LANGS[lang]; d = L["dir"]; up = "../" if d else ""
    path = f"{d}{name}.html"
    alt = {k: f"{LANGS[k]['dir']}{name}.html" for k in LANGS}
    body = f"""
<a class="skip" href="#main">{e(DEEP_HEAD[lang]['skip'])}</a>
{hero(lang, alt, up, title[0], title[1])}
<div class="wrap"><main id="main" class="app-main">{inner}</main>
</div>
{SHOW_HTML(lang)}
<script>{COMMON_JS}{TOPIC_JS}{script}</script>
{footer(lang, tab)}
{feedback_html(lang)}
</body>
</html>
"""
    ldtag = f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ""
    write(path, head(lang, f"{seo} | {BRAND}", desc, path, alt, ldtag, index=index) + body)
    return path


CARDS_JS = r"""
(function () {
  /* Filter the cards, and keep the visitor's own cards on this phone. */
  const q = document.getElementById("cq"), nores = document.getElementById("cnores");
  const run = () => { const v = q.value.trim().toLowerCase(); let n = 0;
    document.querySelectorAll("#cards .say, #cards .names li").forEach(c => { const ok = !v || (c.dataset.kw || c.textContent.toLowerCase()).includes(v); c.hidden = !ok; if (ok) n++; });
    document.querySelectorAll("#cards .cgroup").forEach(g => { g.hidden = !g.querySelector(".say:not([hidden]), .names li:not([hidden])"); });
    nores.hidden = !v || n > 0; };
  q.addEventListener("input", run);
  const cfg = document.getElementById("own").dataset, inp = document.getElementById("own-in"), box = document.getElementById("own-list"), wrap = document.getElementById("own-wrap");
  const load = () => { try { const a = JSON.parse(store("emk-cards") || "[]"); return Array.isArray(a) ? a.filter(s => typeof s === "string").slice(0, 30) : []; } catch (e) { return []; } };
  const paint = () => { const a = load(); box.replaceChildren(); wrap.hidden = !a.length;
    a.forEach((txt, i) => { const b = el("button", { type: "button", class: "chip", "aria-label": cfg.show + ": " + txt }, [el("span", { lang: "ko", text: txt }), el("small", { text: cfg.show }), el("i", { "aria-hidden": "true", text: "🗣" })]);
      b.addEventListener("click", () => show(cfg.lbl, txt, "", ""));
      const x = el("button", { type: "button", class: "linkbtn rm", text: cfg.remove }); x.addEventListener("click", () => { const n = load(); n.splice(i, 1); store("emk-cards", JSON.stringify(n)); paint(); });
      box.append(el("li", {}, [b, x])); }); };
  document.getElementById("own-show").addEventListener("click", () => { const v = inp.value.trim(); if (v) { show(cfg.lbl, v.slice(0, 200), "", ""); count("own-card-show", "own card"); } else inp.focus(); });
  document.getElementById("own").addEventListener("submit", ev => { ev.preventDefault(); const v = inp.value.trim().slice(0, 200); if (!v) { inp.focus(); return; }
    const a = load().filter(s => s !== v); a.unshift(v); store("emk-cards", JSON.stringify(a.slice(0, 30))); inp.value = ""; paint(); count("own-card-save", "own card saved"); });
  paint();
})();
"""


def build_cards(lang):
    """Every Korean card on one page, grouped by guide, plus cards the visitor makes."""
    t = A.T[lang]; S = SHORT[lang]; LU = layout.UI.get(lang, layout.UI["en"]); ux = UX[lang]
    own = f"""<form class="own" id="own" data-lbl="{e(S['show'])}" data-show="{e(t['own_show'])}" data-remove="{e(t['remove'])}"><h2>{e(t['own_h'])}</h2>
<textarea id="own-in" lang="ko" maxlength="200" rows="1" aria-label="{e(t['own_h'])}" placeholder="{e(t['own_ph'])}"></textarea>
<div class="actions"><button class="btn alt" type="button" id="own-show">🗣 {e(t['own_show'])}</button><button class="btn ghost" type="submit">{e(t['own_save'])}</button></div><p class="hint">{e(t['own_note'])}</p></form>
<section id="own-wrap" class="names" hidden><h2>{e(t['own_list_h'])}</h2><ul id="own-list"></ul></section>"""
    groups = [f'<section class="cgroup"><h2>{e(t["basics_h"])}</h2>' + "".join(say_card(lang, ko, m[lang]) for ko, m in HELP_PHRASES) + "</section>"]
    for tk in task_list(lang):
        names = COPY.get(tk["id"], [])
        if not tk["phrases"] and not names: continue
        kw = tk["short"] + " " + KEYWORDS[tk["id"]]
        says = "".join(say_card(lang, ko, m, kw) for ko, m in tk["phrases"])
        chips = "".join(f'<li data-kw="{e((ko + " " + tx(m, lang) + " " + kw).lower())}"><button class="chip" type="button" data-copy="{e(ko)}" data-done="✓ {e(LU["copied"])}"><span lang="ko">{e(ko)}</span><small>{e(tx(m, lang))}</small><i aria-hidden="true">📋</i></button></li>' for ko, m in names)
        groups.append(f'<section class="cgroup"><h2>{tk["icon"]}<a href="{tk["slug"]}.html">{e(tk["short"])}</a></h2>{says}' + (f'<div class="names"><ul>{chips}</ul></div>' if chips else "") + "</section>")
    inner = f"""{own}
<label class="search"><span class="sr">{e(t['cards_filter'])}</span><input id="cq" type="search" placeholder="{e(t['cards_filter'])}" autocomplete="off"></label>
<p class="hint" id="cnores" hidden>{e(ux['nores'])}</p>
<div id="cards">{''.join(groups)}</div>"""
    return app_page(lang, "phrases", (t["cards_title"], t["cards_lede"]), t["cards_seo"], t["cards_desc"], inner, "cards", CARDS_JS)


TRIP_JS = r"""
(function () {
  /* My trip: everything on this page is read from this phone's own storage. */
  const G = JSON.parse(document.getElementById("trip-data").textContent), cfg = document.getElementById("trip").dataset;
  const arr = k => { try { const a = JSON.parse(store(k) || "[]"); return Array.isArray(a) ? a.filter(s => G[s]) : []; } catch (e) { return []; } };
  const item = (slug, rm) => { const a = el("a", { href: slug + ".html" }, [el("span", { class: "ic", html: G[slug][1] }), el("span", { text: G[slug][0] })]); const li = el("li", {}, a);
    if (rm) { const b = el("button", { type: "button", class: "linkbtn rm", text: cfg.remove, "aria-label": cfg.remove + ": " + G[slug][0] }); b.addEventListener("click", () => { store("emk-saved", JSON.stringify(arr("emk-saved").filter(s => s !== slug))); paint(); }); li.append(b); }
    return li; };
  function paint() {
    const s = arr("emk-saved"), r = arr("emk-recent").filter(x => !s.includes(x));
    document.getElementById("saved-list").replaceChildren(...s.map(x => item(x, true)));
    document.getElementById("saved-empty").hidden = s.length > 0;
    document.getElementById("recent").hidden = !r.length;
    document.getElementById("recent-list").replaceChildren(...r.map(x => item(x, false)));
  }
  paint();
  /* How much is ready offline, and the install button. */
  if (window.caches) caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("emk-")).map(k => caches.open(k).then(c => c.keys())))).then(all => {
    const n = new Set(all.flat().map(r => new URL(r.url).pathname).filter(p => p.endsWith("/") || p.endsWith(".html"))).size;
    if (n) { const p = document.getElementById("off-n"); p.textContent = "✓ " + cfg.offline.replace("{n}", n); p.hidden = false; }
  }).catch(() => {});
  const ib = document.getElementById("app-install"), I = window.emkInstall;
  const ready = () => { if (I && I.ready()) ib.hidden = false; };
  document.addEventListener("emk-installable", ready); ready();
  ib.addEventListener("click", () => { if (I) I.ask(); ib.hidden = true; });
  if (/iPhone|iPad|iPod/.test(navigator.userAgent) && !(I && I.standalone)) document.getElementById("ios-hint").hidden = false;
  document.getElementById("clear").addEventListener("click", () => {
    if (!confirm(cfg.ask)) return;
    try { Object.keys(localStorage).filter(k => /^(emk|wik)-/.test(k)).forEach(k => localStorage.removeItem(k)); } catch (e) {}
    document.getElementById("cleared").textContent = cfg.cleared; paint();
    const ma = document.getElementById("ma-has"), mf = document.getElementById("ma-form"); if (ma && mf) { ma.hidden = true; mf.hidden = false; }
  });
})();
"""


def build_trip(lang):
    """My trip: saved and recent guides, the stay address, and what this app keeps on the phone."""
    t = A.T[lang]; P = PAGES[lang]
    G = {tk["slug"]: [tk["short"], tk["icon"]] for tk in task_list(lang)}
    link = lambda href, key, text: f'<li><a href="{href}"><span class="ic">{A.IC[key]}</span><span>{e(text)}</span></a></li>'
    inner = f"""<div id="trip" data-remove="{e(t['remove'])}" data-offline="{e(t['trip_offline'])}" data-ask="{e(t['trip_clear_q'])}" data-cleared="{e(t['trip_cleared'])}">
<section class="sec" aria-labelledby="sv-h"><h2 id="sv-h">{e(t['trip_saved_h'])}</h2><ul class="glist" id="saved-list"></ul><p class="hint" id="saved-empty">{e(t['trip_saved_empty'])}</p></section>
<section class="sec" id="recent" hidden aria-labelledby="rc-h"><h2 id="rc-h">{e(t['trip_recent_h'])}</h2><ul class="glist" id="recent-list"></ul></section>
{addr_card(lang)}
<section class="sec" aria-labelledby="mr-h"><h2 id="mr-h">{e(t['trip_more_h'])}</h2><ul class="glist">{link('phrases.html', 'cards', t['trip_cards'])}{link('./#tool-h', 'guides', t['trip_setup'])}{link('help.html', 'help', t['trip_help'])}</ul></section>
<section class="sec" aria-labelledby="ap-h"><h2 id="ap-h">{e(t['trip_app_h'])}</h2>
<p class="hint" id="off-n" hidden></p><p class="hint" id="ios-hint" hidden>{e(t['ios_hint'])}</p>
<div class="actions"><button class="btn" type="button" id="app-install" hidden>{e(t['trip_install'])}</button><button class="btn ghost" type="button" id="clear">{e(t['trip_clear'])}</button></div><p class="hint" id="cleared" role="status"></p>
<p class="hint"><a href="privacy.html">{e(t['privacy_title'])}</a> · <a href="about.html">{e(P['about'])}</a> · <a href="changes.html">{e(P['changes'])}</a></p></section>
</div><script type="application/json" id="trip-data">{json.dumps(G, ensure_ascii=False).replace("</", "<\\/")}</script>"""
    return app_page(lang, "saved", (t["trip_title"], t["trip_lede"]), t["trip_title"], t["trip_lede"], inner, "trip", TRIP_JS, index=False)


def build_help(lang):
    """Emergency numbers and the Korean cards to show someone. Facts come from HELP in data_extra.py."""
    t = A.T[lang]; h = HELP[lang]; slug_of = {tid: sl for tid, sl, _ in TASK_META}
    nums = "".join(f'<a class="call" href="tel:{"+82-2-1330" if n == "1330" else n}"><b>{n}</b><span>{e(d)}</span></a>' for n, d in h["nums"])
    says = "".join(say_card(lang, ko, m[lang]) for ko, m in HELP_PHRASES[:4]) + "".join(say_card(lang, ko, m[lang]) for ko, m in PHRASES["health"])
    more = "".join(f'<li><a href="{slug_of[i]}.html"><span class="ic">{icon(i)}</span><span>{e(QUESTION[lang][i])}</span></a></li>' for i in ("health", "translate"))
    inner = f"""<section class="sec" aria-labelledby="cl-h"><h2 id="cl-h">{e(h['calls'])}</h2><div class="calls">{nums}</div><p class="hint">{e(t['help_offline'])}</p></section>
<section class="sec says" aria-labelledby="sh-h"><h2 id="sh-h">{e(h['phrases'])}</h2>{says}</section>
{addr_card(lang)}
<section class="sec" aria-labelledby="mh-h"><h2 id="mh-h">{e(t['help_more_h'])}</h2><ul class="glist">{more}<li><a href="phrases.html"><span class="ic">{A.IC['cards']}</span><span>{e(t['cards_title'])}</span></a></li></ul></section>"""
    return app_page(lang, "help", (t["help_title"], t["help_lede"]), t["help_seo"], t["help_desc"], inner, "help")


def build_privacy(lang):
    t = A.T[lang]; L = LANGS[lang]
    mail = f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>'
    inner = "".join(f'<section class="deep"><h2>{e(hd)}</h2><p>{e(tx_).replace("{email}", mail)}</p></section>' for hd, tx_ in t["privacy_body"])
    date = f'<time datetime="{A.POLICY_DATE}">{e(fmt_date(A.POLICY_DATE, lang))}</time>'
    inner += f'<p class="hint">{e(t["privacy_updated"]).replace("{date}", date)}</p>'
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": t["privacy_title"], "url": SITE + L["dir"] + "privacy.html", "inLanguage": L["html_lang"], "dateModified": A.POLICY_DATE}
    return app_page(lang, "privacy", (t["privacy_title"], t["privacy_desc"]), t["privacy_title"], t["privacy_desc"], inner, "", ld=ld)


def search_index(lang):
    """Questions answered inside guides and every Korean card, for the home page search box."""
    faq = [[sl, tid, q] for tid, sl, _ in TASK_META for q, _a in (DEEP.get(tid, {}).get(lang, {}).get("faq", []))]
    cards = [[ko, m[lang]] for ko, m in HELP_PHRASES] + [[ko, m[lang]] for lst in PHRASES.values() for ko, m in lst]
    seen = set(c[0] for c in cards)
    for rows in COPY.values():
        for ko, m in rows:
            if ko not in seen: seen.add(ko); cards.append([ko, tx(m, lang)])
    return json.dumps({"faq": faq, "cards": cards}, ensure_ascii=False, separators=(",", ":"))


# App and topic names that get a link to their guide the first time they appear in a guide's
# long-form text (Latin names, so the same list works in every language). Longest first.
LINK_TERMS = [("CatchTable Global", "food-booking"), ("e-Arrival Card", "entry"), ("Climate Card", "transitpass"),
              ("Naver Map", "maps"), ("KR Pass", "krpass"), ("T-money", "transit"), ("K-ETA", "entry"),
              ("Papago", "translate"), ("k.ride", "taxi"), ("Baemin", "delivery"), ("AREX", "airport"), ("Gimpo", "gimpo"), ("金浦", "gimpo"), ("KTX", "ktx"), ("eSIM", "data")]

def deep_html(lang, tid):
    """Long-form block for guides that have one in deep.py. Returns (html, faq pairs)."""
    g = DEEP.get(tid)
    if not g or lang not in g: return "", []
    c = g[lang]; H = DEEP_HEAD[lang]
    slug_of = {i: sl for i, sl, _ in TASK_META}
    used = {tid}
    def link(text):
        """Escape text and link the first mention of each app or topic on the page to its guide."""
        out = e(text)
        for term, target in LINK_TERMS:
            if target in used or term not in out: continue
            out = out.replace(term, f'<a href="{slug_of[target]}.html">{term}</a>', 1); used.add(target)
        return out
    def step(s):
        if isinstance(s, (list, tuple)):
            return f"<li>{link(s[0])}<!-- screenshot: {e(s[1])} --></li>"
        return f"<li>{link(s)}</li>"
    steps = "".join(step(s) for s in c["steps"])
    errs = "".join(f'<li><p class="prob"><b>{e(a)}</b></p><p>{link(b)}</p></li>' for a, b in c["errors"])
    faq = "".join(f'<h3>{e(q)}</h3><p>{link(a)}</p>' for q, a in c["faq"])
    cites = "".join(f'<li><a href="{e(u)}" rel="noopener" target="_blank">{e(n)}</a></li>' for n, u in g["cites"])
    out = f"""<details class="more deep" id="st-{tid}"><summary>{e(H['steps'])}</summary><div class="in"><ol class="steps full">{steps}</ol></div></details>
<details class="more deep" id="er-{tid}"><summary>{e(H['errors'])}</summary><div class="in"><ul class="errs">{errs}</ul></div></details>
<details class="more deep faq" id="fq-{tid}"><summary>{e(H['faq'])}</summary><div class="in">{faq}</div></details>
<details class="more deep" id="ct-{tid}"><summary>{e(H['cites'])}</summary><div class="in"><ul class="cites">{cites}</ul></div></details>"""
    return out, c["faq"]


def build_info(lang, kind):
    """About or contact page. kind is 'about' or 'contact'."""
    P = PAGES[lang]; L = LANGS[lang]; d = L["dir"]; up = "../" if d else ""
    path = f"{d}{kind}.html"
    alt = {k: f"{LANGS[k]['dir']}{kind}.html" for k in LANGS}
    if kind == "about":
        title, desc = P["about_title"], P["about_desc"]
        inner = "".join(f'<section class="deep"><h2>{e(h)}</h2><p>{e(t)}</p></section>' for h, t in P["about_body"])
        inner += f'<section class="deep"><h2>{e(P["contact"])}</h2><p><a href="contact.html">{e(P["contact_title"])}</a> · <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p></section>'
        ld = {"@context": "https://schema.org", "@type": "AboutPage", "name": title, "url": SITE + path, "inLanguage": L["html_lang"],
              "mainEntity": {"@type": "Organization", "name": BRAND, "url": SITE, "email": CONTACT_EMAIL, "logo": SITE + "icon-512.png"}}
    else:
        title, desc = P["contact_title"], P["contact_desc"]
        inner = f'<section class="deep"><p>{e(P["contact_lead"])}</p><p><b>{e(P["contact_email"])}:</b> <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p><p>{e(P["contact_ask"])}</p></section>' + ask_box(lang)
        ld = {"@context": "https://schema.org", "@type": "ContactPage", "name": title, "url": SITE + path, "inLanguage": L["html_lang"],
              "mainEntity": {"@type": "Organization", "name": BRAND, "url": SITE, "email": CONTACT_EMAIL}}
    body = f"""
{hero(lang, alt, up, title, desc)}
<div class="wrap"><main>{inner}</main>
  <div class="actions"><a class="btn" href="./">{e(L['ui']['open_tool'])}</a></div>
  <p class="fb-line"><button type="button" class="linkbtn" data-feedback="{kind}">💬 {e(FEEDBACK[lang]['open'])}</button></p>
</div>
{footer(lang, "")}
{feedback_html(lang)}
</body>
</html>
"""
    ldtag = f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    write(path, head(lang, f"{title} | {BRAND}", desc, path, alt, ldtag) + body)
    return path


def build_404():
    """GitHub Pages serves /404.html for any missing path, so every link here is absolute."""
    homes = " · ".join(f'<a href="/{LANGS[k]["dir"]}" lang="{LANGS[k]["html_lang"]}">{e(LANGS[k]["name"])}</a>' for k in LANGS)
    guides = "".join(f'<li><a href="/{t["slug"]}.html">{e(QUESTION["en"][t["id"]])}</a></li>' for t in task_list("en"))
    write("404.html", f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#2336e8">
<link rel="icon" href="/favicon.ico" sizes="any">
<title>Page not found | {BRAND}</title>
<link rel="stylesheet" href="/style.css?v={CSS_V}">
</head>
<body>
<header class="hero"><div class="wrap">
  <div class="toprow"><a class="logo" href="/">EasyMode<b>Korea</b></a></div>
  <h1>This page isn't here</h1><p class="lede">The link may be old. Pick a guide below, or start from the home page in your language: {homes}</p>
</div></header>
<div class="wrap"><main><section class="related"><h2>Guides</h2><ul>{guides}</ul></section>
<div class="actions"><a class="btn" href="/">Check your own setup</a></div></main></div>
</body>
</html>
""")


def write(rel, text):
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    open(full, "w", encoding="utf-8").write(text)


def png_size(rel):
    """Width and height of a PNG in the repo, read from its header."""
    b = open(os.path.join(ROOT, rel), "rb").read(24)
    return int.from_bytes(b[16:20], "big"), int.from_bytes(b[20:24], "big")


# Phone screenshots shown in the install dialog (and reused for the store listing).
SHOTS = [("shots/home.png", "Pick what you need right now"), ("shots/guide.png", "A short answer with the date it was checked"),
         ("shots/cards.png", "Korean cards to show a driver or staff"), ("shots/help.png", "Emergency numbers, one tap away")]
LINKS_FILE = os.path.join(ROOT, "android", "fingerprints.json")


def main():
    paths = []; local = []
    for lang in LANGS:
        paths.append(build_tool(lang))
        paths.append(build_changes(lang))
        paths.append(build_info(lang, "about"))
        paths.append(build_info(lang, "contact"))
        for t in task_list(lang):
            paths.append(build_topic(lang, t))
        paths += [build_cards(lang), build_help(lang), build_privacy(lang)]
        local.append(build_trip(lang))  # personal page: offline copy, but not in the sitemap
        write(LANGS[lang]["dir"] + "search.json", search_index(lang)); local.append(LANGS[lang]["dir"] + "search.json")
    paths.append("hosts.html")
    build_404()
    by_rel = {}
    for p in paths:
        lang = next((k for k in LANGS if LANGS[k]["dir"] and p.startswith(LANGS[k]["dir"])), "en")
        by_rel.setdefault(p[len(LANGS[lang]["dir"]):], {})[lang] = p
    def url(p):
        rel = p[len(next((LANGS[k]["dir"] for k in LANGS if LANGS[k]["dir"] and p.startswith(LANGS[k]["dir"])), "")):]
        alts = by_rel.get(rel, {})
        links = "" if len(alts) < 2 else "".join(f'<xhtml:link rel="alternate" hreflang="{LANGS[k]["html_lang"]}" href="{SITE}{q}"/>' for k, q in alts.items()) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{alts.get("en", p)}"/>'
        d = DATES[p]["d"] if p in DATED else page_date(p, open(os.path.join(ROOT, (p + "index.html") if (p == "" or p.endswith("/")) else p), encoding="utf-8").read())
        return f"<url><loc>{SITE}{p}</loc><lastmod>{d}</lastmod>{links}</url>\n"
    urls = "".join(url(p) for p in paths)
    write("style.css", CSS)
    write("app.js", A.APP_JS)
    shots = [(n, *png_size(n), lbl) for n, lbl in SHOTS if os.path.exists(os.path.join(ROOT, n))]
    write("manifest.webmanifest", A.manifest(layout.UI["en"]["lede"], shots))
    prints = json.load(open(LINKS_FILE, encoding="utf-8"))["sha256_cert_fingerprints"] if os.path.exists(LINKS_FILE) else []
    write(".well-known/assetlinks.json", A.assetlinks(prints))
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{urls}</urlset>\n')
    # Offline: precache every page, so a guide opened once (or not yet) still works without signal.
    pre = ["./", "ja/", "zh-tw/", "zh-cn/", "vi/", "icon-192.png", "manifest.webmanifest", f"style.css?v={CSS_V}", f"app.js?v={APP_V}"] + [p for p in paths + local if p and not p.endswith("/")]
    # The cache name changes whenever any page, the stylesheet, the script or the worker itself changes.
    ver = hashlib.sha256(("".join(DATES[p]["h"] for p in sorted(DATES)) + CSS_V + APP_V + A.SW_JS + "".join(sorted(pre))).encode()).hexdigest()[:8]
    sw = re.sub(r"const C='[^']*';const PRE=\[[^\]]*\];", lambda m: f"const C='emk-{ver}';const PRE={json.dumps(pre)};", A.SW_JS, count=1)
    write("sw.js", sw)
    open(DATES_FILE, "w", encoding="utf-8").write(json.dumps(dict(sorted(DATES.items())), indent=0, ensure_ascii=False) + "\n")
    if layout.MISSING: print("warning: layout.py text falls back to English for: " + ", ".join(sorted(layout.MISSING)))
    print(f"built {len(paths)} pages")


if __name__ == "__main__":
    main()
