"""Builds EasyModeKorea: checker page, topic pages and a changelog page, in each language.
Run from the repo root:  python korea/src/build.py
Content: data.py (answers) and data_extra.py (hook, short labels, icons, phrases, first 24 hours,
changelog, host-stay strings). Host stay details travel in the link's #g= hash: never sent to a
server or to analytics, and rendered with textContent only.
"""
import html, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from data import CHECKED, CHECKED_ISO, LANGS, SOURCES, TASK_META  # noqa: E402
from data_extra import BRAND, FEEDBACK, FEEDBACK_FORM, FEEDBACK_TO, HELP, HELP_PHRASES, ICONS, KEYWORDS, PHRASES, PLAN, QUESTION, SHORT, UX, X  # noqa: E402
import zh_cn  # noqa: E402,F401  (adds Simplified Chinese)
import vi  # noqa: E402,F401  (adds Vietnamese)

ROOT = os.path.join(os.path.dirname(__file__), "..")
SITE = "https://easymodekorea.com/"
GOAT = "https://eddpositive.goatcounter.com/count"
CSS = open(os.path.join(os.path.dirname(__file__), "style.css"), encoding="utf-8").read()
e = lambda s: html.escape(str(s), quote=True)
icon = lambda tid: f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[tid]}</svg>'
FONTS = "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=IBM+Plex+Sans:wght@400;600;700&display=swap"
# Chat assistant (worker/ in this repo). Empty = no widget on the site. Set to the deployed Worker URL,
# e.g. "https://emk-chat.<your-subdomain>.workers.dev/chat", then rebuild. EMK_CHAT_ENDPOINT overrides it for local tests.
CHAT_ENDPOINT = os.environ.get("EMK_CHAT_ENDPOINT", "")
CHAT_UI = {
    "en": {"open": "Ask a question", "title": "Ask EasyModeKorea", "ph": "e.g. Can I use Kakao T with a foreign card?", "send": "Send", "close": "Close", "note": "AI answers from this site's guides. Can be wrong: check the guide it links. Don't share personal details.", "err": "Sorry, the assistant is busy. Try again later, or use Feedback."},
    "ja": {"open": "質問する", "title": "EasyModeKoreaに質問", "ph": "例: 海外カードでカカオTは使えますか?", "send": "送信", "close": "閉じる", "note": "このサイトのガイドを元にAIが答えます。誤りがあり得るので、リンク先のガイドも確認してください。個人情報は書かないでください。", "err": "混み合っています。後でもう一度お試しください。"},
    "zh-tw": {"open": "提問", "title": "問 EasyModeKorea", "ph": "例如:外國信用卡能用 Kakao T 嗎?", "send": "送出", "close": "關閉", "note": "AI 依本站指南回答,可能有誤,請再看它附上的指南。請勿輸入個人資料。", "err": "目前忙碌中,請稍後再試。"},
    "zh-cn": {"open": "提问", "title": "问 EasyModeKorea", "ph": "例如:外国银行卡能用 Kakao T 吗?", "send": "发送", "close": "关闭", "note": "AI 根据本站指南回答,可能有误,请再看它附上的指南。请勿输入个人信息。", "err": "目前繁忙,请稍后再试。"},
    "vi": {"open": "Đặt câu hỏi", "title": "Hỏi EasyModeKorea", "ph": "VD: Thẻ nước ngoài có dùng Kakao T được không?", "send": "Gửi", "close": "Đóng", "note": "AI trả lời dựa trên hướng dẫn của trang này, có thể sai: hãy xem hướng dẫn được dẫn link. Đừng gửi thông tin cá nhân.", "err": "Trợ lý đang bận, vui lòng thử lại sau."},
}


def chat_tag(lang, path):
    if not CHAT_ENDPOINT: return ""
    up = "../" * path.count("/")
    cfg = json.dumps({"endpoint": CHAT_ENDPOINT, "lang": lang, "page": path, **CHAT_UI.get(lang, CHAT_UI["en"])}, ensure_ascii=False)
    return f'\n<script>window.EMK_CHAT={cfg};</script><script defer src="{up}chat.js"></script>'


PWA_HEAD = lambda up: f'\n<link rel="manifest" href="{up}manifest.webmanifest"><link rel="apple-touch-icon" href="{up}icon-192.png"><meta name="apple-mobile-web-app-capable" content="yes">'


def head(lang, title, desc, path, alt_paths, extra=""):
    alts = "".join(f'<link rel="alternate" hreflang="{LANGS[k]["html_lang"]}" href="{SITE}{p}">' for k, p in alt_paths.items())
    alts += f'<link rel="alternate" hreflang="x-default" href="{SITE}{alt_paths["en"]}">'
    return f"""<!DOCTYPE html>
<html lang="{LANGS[lang]['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#2336e8">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png"><link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">{alts}
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{SITE}{path}"><meta property="og:image" content="{SITE}og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="robots" content="max-snippet:-1, max-image-preview:large">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="{FONTS}" onload="this.onload=null;this.rel='stylesheet'"><noscript><link rel="stylesheet" href="{FONTS}"></noscript>
<style>
{CSS}</style>
<script data-goatcounter="{GOAT}" async src="//gc.zgo.at/count.js"></script>{chat_tag(lang, path)}{extra}
</head>
<body>"""


def lang_links(cur, rel_paths, prefix):
    out = []
    for k, L in LANGS.items():
        cur_attr = ' aria-current="page"' if k == cur else ""
        out.append(f'<a href="{prefix}{rel_paths[k]}" hreflang="{L["html_lang"]}"{cur_attr}>{e(L["name"])}</a>')
    return f'<nav class="langs" aria-label="{e(LANGS[cur]["ui"]["langs"])}">' + "".join(out) + "</nav>"


def hero(lang, alt, up, h1, lede, home="./", trust=True):
    x = X[lang]
    return f"""<header class="hero"><div class="wrap">
  <div class="toprow"><a class="logo" href="{home}">EasyMode<b>Korea</b></a>{lang_links(lang, alt, up)}</div>
  {f'<h1>{e(h1)}</h1>' if h1 else ''}
</div></header>"""


def about(lang, up):
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
    for t in tasks: t["kw"] = (KEYWORDS[t["id"]] + " " + t["short"] + " " + t["title"]).lower()
    data = {"ui": U, "x": {k: x[k] for k in keys}, "s": S, "ux": ux, "tasks": tasks, "plan": PLAN[lang], "fbfail": FEEDBACK[lang]["fail"], "checked": CHECKED[lang], "lang": lang,
            "langs": {k: {"name": LANGS[k]["name"], "dir": LANGS[k]["dir"]} for k in LANGS}, "up": up}
    q1 = "".join(f'<button type="button" class="opt-big" data-p="{p}"><b>{e(ux["q1_opts"][p][0])}</b><span>{e(ux["q1_opts"][p][1])}</span></button>' for p in ("visitor", "krsim", "arc"))
    q2 = "".join(f'<button type="button" class="opt-big" data-d="{v}"><b>{e(U[v])}</b></button>' for v in ("ios", "android"))
    body = f"""
{hero(lang, alt, up, '', '')}
<h1 class="sr">{e(x['hook'])}</h1>
<div class="wrap pre">
  <div class="banner" id="lang-suggest" hidden></div>
  <section class="stay" id="stay" hidden aria-live="polite"></section>
  <div class="banner" id="install" hidden><span>{e(ux['install'])}</span><button class="btn alt" type="button" id="install-btn">{e(ux['install_btn'])}</button></div>
  <section class="onb" id="onb" aria-live="polite">
    <div id="onb1"><h2>{e(ux['q1'])}</h2><p class="why">{e(ux['why'])}</p><div class="opts-big">{q1}</div></div>
    <div id="onb2" hidden><h2>{e(ux['q2'])}</h2><div class="opts-big two">{q2}</div><button type="button" class="linkbtn" id="onb-back">← {e(ux['back'])}</button></div>
  </section>
</div>
<div class="mybar" id="mybar" hidden><div class="wrap"><span id="mysetup"></span><span class="bar-btns"><button type="button" class="btn ghost small" id="help-btn">{e(HELP[lang]['btn'])}</button><button type="button" class="btn ghost small" id="change">{e(ux['change'])}</button></span></div></div>
<div class="wrap" id="main" hidden>
  <label class="search"><span class="sr">{e(ux['search'])}</span><input id="q" type="search" placeholder="{e(ux['search'])}" autocomplete="off"></label>
  <p class="hint" id="nores" hidden>{e(ux['nores'])} <button type="button" class="linkbtn" id="clear">{e(ux['clear'])}</button></p>
  <main class="rows" id="rows"></main>
  <details class="panel" id="cl"><summary><span id="ptitle"></span> <span class="count" id="pcount"></span></summary><div class="in">
    <div class="progress"><div class="bar"><i id="pbar"></i></div></div>
    <ul class="checks" id="checklist"></ul>
    <div class="actions"><button class="btn" type="button" id="copy-btn">{e(U['copy'])}</button><span class="copied" id="copied" role="status"></span></div>
  </div></details>
  {about(lang, up)}
</div>
{help_html(lang)}
{SHOW_HTML(lang)}
<div class="toast" id="offline" hidden role="status">{e(ux['offline'])}</div>
<script>
const D = {json.dumps(data, ensure_ascii=False)};
{COMMON_JS}
{TOOL_JS}
</script>
{feedback_html(lang)}
</body>
</html>
"""
    site_ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "alternateName": ["Easy Mode Korea", "이지모드코리아", "이지모드 코리아", "easymodekorea.com"], "url": SITE, "inLanguage": L["html_lang"]},
               {"@context": "https://schema.org", "@type": "Organization", "name": BRAND, "url": SITE, "logo": SITE + "icon-512.png", "email": "edandco.biz@gmail.com"}]
    extra = PWA_HEAD(up) + f'\n<script type="application/ld+json">{json.dumps(site_ld, ensure_ascii=False)}</script>'
    write(path + "index.html", head(lang, f"{BRAND} | {x['home_title']}", x["home_desc"], path, alt, extra) + body)
    return path


TOOL_JS = r"""
const U = D.ui, XS = D.x, S = D.s, UX = D.ux, FB_FAIL = D.fbfail;
let P = null, DEV = null;
function resolve(t, p, dev) { if (t.all) return t.all; let v = t.v[p]; if (typeof v === "string") v = t.v[v]; if (t.dev && v[dev]) v = v[dev]; return v; }
function setStep(n) { document.getElementById("onb1").hidden = n !== 1; document.getElementById("onb2").hidden = n !== 2; }
function openOnb() { document.getElementById("onb").hidden = false; document.getElementById("main").hidden = true; document.getElementById("mybar").hidden = true; setStep(1); document.querySelector("#onb1 .opt-big").focus(); }
function finish() {
  store("wik-setup", P + "|" + DEV); document.body.classList.add("ret");
  document.getElementById("onb").hidden = true; document.getElementById("main").hidden = false; document.getElementById("mybar").hidden = false;
  document.getElementById("mysetup").textContent = S.prof[P] + " · " + U[DEV];
  render(); count("setup/" + D.lang + "/" + P + "/" + DEV, "setup");
  if (fromOnb) window.scrollTo(0, 0);
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
const off = () => { document.getElementById("offline").hidden = navigator.onLine; };
window.addEventListener("online", off); window.addEventListener("offline", off); off();
document.getElementById("onb-back").addEventListener("click", () => setStep(1));
document.getElementById("change").addEventListener("click", openOnb);
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
  document.getElementById("nores").hidden = shown > 0;
  if (q && shown === 1) { const r = [...document.querySelectorAll(".row")].find(x => !x.hidden); r.open = true; }
}
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
  const go = el("a", { class: "btn alt", href: D.up + L2.dir + location.hash, text: UX.switch });
  const no = el("button", { type: "button", class: "linkbtn", text: UX.dismiss }); no.addEventListener("click", () => { store("wik-lang-dismiss", "1"); b.hidden = true; });
  b.append(el("span", { text: UX.suggest.replace("{l}", L2.name) }), go, no); b.hidden = false;
})();
/* Installable + offline. */
let deferred = null;
window.addEventListener("beforeinstallprompt", ev => { ev.preventDefault(); deferred = ev; document.getElementById("install").hidden = false; });
document.getElementById("install-btn").addEventListener("click", async () => { if (!deferred) return; deferred.prompt(); try { await deferred.userChoice; } catch (e) {} deferred = null; document.getElementById("install").hidden = true; count("install", "install"); });
if ("serviceWorker" in navigator) navigator.serviceWorker.register(D.up + "sw.js").catch(() => {});
const saved = (store("wik-setup") || "").split("|");
if (saved[0] && S.prof[saved[0]] && (saved[1] === "ios" || saved[1] === "android")) { P = saved[0]; DEV = saved[1]; finish(); } else { openOnb(); }
stay();
const target = location.hash.match(/^#task-[\w-]+$/); if (target && P) { const r = document.querySelector(target[0]); if (r) { r.open = true; r.scrollIntoView(); } }
"""


TOPIC_JS = r"""
(function () {
  document.querySelectorAll("[data-show]").forEach(b => b.addEventListener("click", () => show(b.dataset.lbl, b.dataset.show, "", b.dataset.mean)));
  const saved = (store("wik-setup") || "visitor|ios").split("|");
  const blocks = [...document.querySelectorAll(".card[data-p]")];
  if (blocks.length < 2) return;
  let shown = 0;
  for (const b of blocks) { const ok = b.dataset.p === saved[0] && (!b.dataset.d || b.dataset.d === saved[1]); b.hidden = !ok; if (ok) shown++; }
  if (!shown) { blocks.forEach(b => b.hidden = false); return; }
  const btn = document.getElementById("show-all"); btn.hidden = false;
  btn.addEventListener("click", () => { blocks.forEach(b => b.hidden = false); btn.hidden = true; });
})();
"""


def build_topic(lang, t):
    L = LANGS[lang]; U = L["ui"]; x = X[lang]; S = SHORT[lang]; d = L["dir"]; up = "../" if d else ""
    path = f"{d}{t['slug']}.html"
    alt = {k: f"{LANGS[k]['dir']}{t['slug']}.html" for k in LANGS}
    fail_lbl = U["fails"].strip().rstrip(":：").strip()
    blocks = []
    profiles = ["visitor", "krsim", "arc"] if "all" not in t else [None]
    for p in profiles:
        devices = ["ios", "android"] if t.get("dev") and p != "arc" else [None]
        for dv in devices:
            v = resolve(t, p or "visitor", dv or "ios")
            heading = U["for_profile"][p] if p else UX[lang]["tone"][v["s"]]
            if dv: heading += f" · {U[dv]}"
            route = "".join(f"<li>{e(r)}</li>" for r in v["route"])
            attrs = (f' data-p="{p}"' if p else "") + (f' data-d="{dv}"' if dv else "")
            blocks.append(f"""<article class="card {v['s']}"{attrs}><div class="actions" style="justify-content:space-between;align-items:center"><h2>{e(heading)}</h2><span class="pill {v['s']}">{e(UX[lang]['tone'][v['s']])}</span></div>
<p class="verdict">{e(v['verdict'])}</p><ol class="steps">{route}</ol><p class="fallback"><b>{e(fail_lbl)}</b>{e(v['fallback'])}</p></article>""")
    phrases = "".join(f'<button class="btn alt" type="button" data-show="{e(ko)}" data-lbl="{e(S["show"])}" data-mean="{e(x["means"])}: {e(m)}">🗣 {e(m)}</button>' for ko, m in t["phrases"])
    notes = "".join(f"<li>{e(n)}</li>" for n in t.get("notes", []))
    srcs = "".join(f'<li><a href="{e(u)}" rel="noopener" target="_blank">{e(n)}</a></li>' for n, u in t["sources"])
    others = "".join(f'<a href="{o["slug"]}.html">{e(o["short"])}</a>' for o in task_list(lang) if o["id"] != t["id"])
    body = f"""
{hero(lang, alt, up, QUESTION[lang][t['id']], '')}
<div class="wrap">
  <div class="actions"><a class="btn" href="./#task-{t['id']}">{e(U['open_tool'])}</a>{phrases}</div>
  <main class="cards">{''.join(blocks)}<button class="linkbtn" type="button" id="show-all" hidden>{e(x['others'])}</button></main>
  <details class="panel"><summary>{e(S['details'])}</summary><div class="in notes"><ul><li>{e(U['checked'])} {e(CHECKED[lang])}</li>{notes}{srcs}</ul></div></details>
  <nav class="topics">{others}</nav>
  {about(lang, up)}
</div>
{SHOW_HTML(lang)}
<script>{COMMON_JS}{TOPIC_JS}</script>
{feedback_html(lang)}
</body>
</html>
"""
    first = resolve(t, "visitor", "ios")
    answer = first["verdict"] + " " + " ".join(first["route"])
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": t["seo"], "dateModified": CHECKED_ISO, "inLanguage": L["html_lang"], "url": SITE + path, "publisher": {"@type": "Organization", "name": BRAND, "url": SITE}},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": BRAND, "item": SITE + L["dir"]}, {"@type": "ListItem", "position": 2, "name": t["short"], "item": SITE + path}]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": QUESTION[lang][t["id"]], "acceptedAnswer": {"@type": "Answer", "text": answer}}]}]
    ldtag = f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    write(path, head(lang, f"{t['seo']} | {BRAND}", t["intro"], path, alt, ldtag) + body)
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
  <p class="fb-line"><button type="button" class="linkbtn" data-feedback="changes">💬 {e(FEEDBACK[lang]['open'])}</button></p>
</div>
{feedback_html(lang)}
</body>
</html>
"""
    write(path, head(lang, f"{x['changes_title']} | {BRAND}", x["changes_lead"], path, alt) + body)
    return path


def write(rel, text):
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    open(full, "w", encoding="utf-8").write(text)


def main():
    paths = []
    for lang in LANGS:
        paths.append(build_tool(lang))
        paths.append(build_changes(lang))
        for t in task_list(lang):
            paths.append(build_topic(lang, t))
    paths.append("hosts.html")
    by_rel = {}
    for p in paths:
        lang = next((k for k in LANGS if LANGS[k]["dir"] and p.startswith(LANGS[k]["dir"])), "en")
        by_rel.setdefault(p[len(LANGS[lang]["dir"]):], {})[lang] = p
    def url(p):
        rel = p[len(next((LANGS[k]["dir"] for k in LANGS if LANGS[k]["dir"] and p.startswith(LANGS[k]["dir"])), "")):]
        alts = by_rel.get(rel, {})
        links = "" if len(alts) < 2 else "".join(f'<xhtml:link rel="alternate" hreflang="{LANGS[k]["html_lang"]}" href="{SITE}{q}"/>' for k, q in alts.items()) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{alts.get("en", p)}"/>'
        return f"<url><loc>{SITE}{p}</loc><lastmod>{CHECKED_ISO}</lastmod>{links}</url>\n"
    urls = "".join(url(p) for p in paths)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{urls}</urlset>\n')
    write("chat-kb.txt", chat_kb())
    print(f"built {len(paths)} pages")


PROFILE_NAMES = {"visitor": "Visitor with no Korean phone number and a foreign card", "krsim": "Visitor with a Korean prepaid SIM (010 number)", "arc": "Resident with an ARC (alien registration card)"}


def chat_kb():
    """Plain-text knowledge base the chat Worker reads (English; the bot answers in the visitor's language)."""
    out = [f"EasyModeKorea knowledge base. Source: {SITE}. Last checked: {CHECKED['en']}.", ""]
    for t in task_list("en"):
        out += [f"## {t['title']}", f"Question: {QUESTION['en'][t['id']]}", f"Guide: {SITE}{t['slug']}.html", t["intro"]]
        if "all" in t:
            cases = [("Everyone", t["all"])]
        else:
            cases = []
            for prof, label in PROFILE_NAMES.items():
                v = t["v"][prof]
                if isinstance(v, str): v = t["v"][v]
                if t.get("dev") and isinstance(v, dict) and "verdict" not in v:
                    cases += [(f"{label}, {dev}", vv) for dev, vv in v.items()]
                else:
                    cases.append((label, v))
        for label, v in cases:
            out.append(f"- {label}: {v.get('verdict', '')}")
            out += [f"  * {r}" for r in v.get("route", [])]
            if v.get("fallback"): out.append(f"  If that fails: {v['fallback']}")
        out.append("")
    out.append("## Emergency and help numbers")
    out += [f"- {n}: {d}" for n, d in HELP["en"]["nums"]]
    out += ["", f"Contact / feedback: the Feedback button on any page, or email {FEEDBACK_TO}.", f"Korean host (guesthouse/Airbnb) link maker: {SITE}hosts.html"]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    main()
