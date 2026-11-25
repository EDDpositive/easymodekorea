"""Checks the built site without a browser. Run from the repo root after a build:
    python tools/check_site.py
Covers what the app experience depends on: every page is app-ready, the offline list is complete,
the manifest and the Android link file are valid, all five languages have the app pages, and no
link inside the site is broken. Exit code 0 means every check passed.
"""
import hashlib, json, os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
import app_shell as A  # noqa: E402

LANG_DIRS = ["", "ja/", "zh-tw/", "zh-cn/", "vi/"]
FAILS = []
rd = lambda rel: open(os.path.join(ROOT, rel), encoding="utf-8").read()
has = lambda rel: os.path.exists(os.path.join(ROOT, rel))
sm_text = lambda: rd("sitemap.xml")


def check(ok, label, detail=""):
    print(("PASS  " if ok else "FAIL  ") + label + (f"  ({detail})" if detail and not ok else ""))
    if not ok: FAILS.append(label)


def png_size(rel):
    b = open(os.path.join(ROOT, rel), "rb").read(24)
    return f"{int.from_bytes(b[16:20], 'big')}x{int.from_bytes(b[20:24], 'big')}"


def main():
    # Text: every language has every string, so nothing falls back to English.
    en = A.T["en"]
    bad = [f"{l}:{k}" for l, t in A.T.items() for k in en if k not in t or not t[k]] + [l for l, t in A.T.items() if len(t["privacy_body"]) != len(en["privacy_body"])]
    check(set(A.T) == {"en", "ja", "zh-tw", "zh-cn", "vi"} and not bad, "app text exists in all five languages", ", ".join(bad[:6]))

    # Offline list: every file named in the worker exists.
    sw = rd("sw.js")
    pre = json.loads(re.search(r"const PRE=(\[[^\]]*\]);", sw).group(1))
    files = [p.split("?")[0] if not p.endswith("/") else (p if p != "./" else "") + "index.html" for p in pre]
    missing = [f for f in files if not has(f)]
    check(not missing, f"all {len(pre)} files in the offline list exist", ", ".join(missing[:6]))
    pages = [f for f in files if f.endswith(".html")]
    need = [d + n for d in LANG_DIRS for n in ("index.html", "phrases.html", "saved.html", "help.html", "privacy.html", "search.json")]
    check(not [n for n in need if n not in files], "app pages and search index are in the offline list for every language")

    # Every page is app-ready.
    css_v, app_v = re.search(r"style\.css\?v=(\w+)", sw).group(1), re.search(r"app\.js\?v=(\w+)", sw).group(1)
    probs = []
    for f in pages:
        if f == "hosts.html": continue  # hand-written page for hosts
        h = rd(f)
        tabs = re.search(r'<nav class="tabbar".*?</nav>', h, re.S)
        if 'rel="manifest" href="/manifest.webmanifest"' not in h: probs.append(f + ": no manifest link")
        if f"app.js?v={app_v}" not in h or f"style.css?v={css_v}" not in h: probs.append(f + ": stale script or stylesheet link")
        if "window.EMK=" not in h: probs.append(f + ": no app settings")
        if not tabs or tabs.group(0).count("<a ") != 4 or tabs.group(0).count('aria-current="page"') > 1: probs.append(f + ": bottom tabs wrong")
    check(not probs, f"{len(pages) - 1} pages have the manifest, shared script and bottom tabs", "; ".join(probs[:4]))

    # Links inside the site resolve.
    broken = []
    for f in pages:
        base = os.path.dirname(f)
        for href in re.findall(r'href="([^"#?]+)(?:[#?][^"]*)?"', rd(f)):
            if re.match(r"^(https?:|mailto:|tel:|sms:|//)", href): continue
            t = href.lstrip("/") if href.startswith("/") else os.path.normpath(os.path.join(base, href)).replace("\\", "/")
            t = "" if t == "." else t
            if not (has(t) and not os.path.isdir(os.path.join(ROOT, t)) or has(os.path.join(t, "index.html"))): broken.append(f"{f} -> {href}")
    check(not broken, "no broken links inside the site", "; ".join(broken[:4]))

    # 30차: the install-worthy screens. Every sentence exists in five languages, every dated item has a source, and nothing on them can send data.
    sys.path.insert(0, os.path.join(ROOT, "src"))
    import moments as M, trouble as TR  # noqa: E402
    import ast
    five = {"en", "ja", "zh-tw", "zh-cn", "vi"}; gaps = []
    def walk(o, at):
        if isinstance(o, dict):
            if "en" in o and all(isinstance(v, str) for v in o.values()):
                if set(o) != five or not all(v.strip() for v in o.values()): gaps.append(at)
            else: [walk(v, f"{at}.{k}") for k, v in o.items()]
        elif isinstance(o, (list, tuple)): [walk(v, f"{at}[{i}]") for i, v in enumerate(o)]
    for n in ("SOS", "SOS_WHAT", "SOS_HELP_M", "ALLERGY", "AVOID", "FOOD_ANS", "CARD", "REFUSED", "RF", "DAYS", "TM", "MOS_LABEL"): walk(getattr(M, n), n)
    for iid, st, w, text, src, d, link, cond in M.DAYS:
        if any(not k.startswith("guide:") and k not in M.SRC and k not in TR.SRC for k in src): gaps.append("source of " + iid)
        if any(not k.startswith("guide:") for k in src) and not d: gaps.append("date of " + iid)
    js = rd("src/moments_js.py")
    send = [w for w in ("fetch(", "XMLHttpRequest", "sendBeacon", "WebSocket", "new Image", "http://", "https://") if w in js.replace("/^http/", "")]
    bad = [f"{d}{n}.html" for d in LANG_DIRS for n in ("sos", "refused", "my-card") if not has(f"{d}{n}.html") or f'"{d}{n}.html"' not in rd("sw.js")]
    for d in LANG_DIRS:
        sos = rd(d + "sos.html")
        if not all(s in sos for s in ('href="tel:119"', 'href="tel:112"', 'href="tel:+82-2-1330"', 'id="sos-find"', 'href="sms:119"')): bad.append(d + "sos.html calls")
        if sos.count('class="ck"') < 3: bad.append(d + "sos.html dates")
        if not all(x in rd(d + "index.html") for x in ('href="sos.html"', 'href="refused.html"', 'href="my-card.html"', 'id="trip-now"')): bad.append(d + "index.html row")
        if 'href="sos.html"' not in rd(d + "help.html") or 'id="days"' not in rd(d + "saved.html"): bad.append(d + "help/trip")
    check(not gaps and not send and not bad, "SOS, Refused, food card, trip mode: five languages, dated and sourced, offline, and their scripts send nothing", "; ".join(gaps[:3] + send + bad[:3]))

    # 32차: the Korean page about Japan's tax refund. It stays apart from the app, shows only dated official procedure and names no refund company.
    import jp_refund as JP
    probs = []; page = rd(JP.PATH); worker = rd("ko/sw.js")
    if f"easymodekorea.com/{JP.PATH}</loc>" not in sm_text(): probs.append("not in the sitemap")
    if JP.PATH in sw or "x.startsWith('emk-')" not in sw or "x.startsWith('jpr-')" not in worker: probs.append("offline copies of the two workers can delete each other")
    if any(f'href="{u}{JP.PATH}"' in rd(d + "index.html") for d in LANG_DIRS for u in ("", "/", "../")): probs.append("linked from a menu before the test says so")
    if any(not u.startswith("https://") or not re.search(r"\.(go\.jp|go\.kr)/", u) for _n, u in JP.SRC.values()): probs.append("a source is not an official page")
    if page.count(f'datetime="{JP.CHK}"') < len(JP.FAQ) or not re.fullmatch(r"\d{4}-\d\d-\d\d", JP.CHK): probs.append("facts without a check date")
    ids = [p[0] for p in JP.AIR_TOP + JP.AIR + JP.SEA]
    if len(set(ids)) != len(ids) or len(JP.AIR_TOP + JP.AIR) != 41: probs.append("airport list")
    # The owner works in payments: no refund company, wallet or card may be named, compared or linked here.
    named = [w for w in ("Global Blue", "글로벌블루", "PIE", "J&J", "Planet", "알리페이", "Alipay", "위챗", "WeChat", "카카오페이", "네이버페이", "토스", "트래블로그", "트래블월렛", "비자카드", "마스터카드", "추천인", "제휴 링크", "amzn", "utm_") if w in page]
    if named: probs.append("names a payment company: " + ", ".join(named))
    if any(w in JP.JS for w in ("fetch(", "XMLHttpRequest", "sendBeacon", "WebSocket", "new Image")): probs.append("its script can send data")
    check(not probs, "Japan tax refund page: in the sitemap only, official dated sources, no payment company named, sends nothing", "; ".join(probs[:4]))

    # 33차: the daily Seoul price game. Five languages, apart from the app; every price comes from a dated official page; nothing played is sent.
    import won as WON, won_data as WD, won_text as WX
    probs = []; pages = {k: rd(WX.DIR[k] + "index.html") for k in WX.LANGS}; wsw = rd("won/sw.js")
    if any(f"easymodekorea.com/{WX.DIR[k]}</loc>" not in sm_text() or pages[k].count('rel="alternate" hreflang=') != 6 for k in WX.LANGS): probs.append("sitemap or language links")
    if any(p.startswith("won") for p in pre) or "x.startsWith('emk-')" not in sw or "k.startsWith('won-')" not in wsw: probs.append("offline copies of the workers can delete each other")
    if any(re.search(r'href="[^"]*\bwon/', rd(d + f)) for d in LANG_DIRS for f in ("index.html", "help.html", "saved.html")): probs.append("linked from a menu before the test says so")
    official = re.compile(r"https://[\w.-]*(\.go\.kr|kamis\.or\.kr|sisul\.or\.kr|bikeseoul\.com|hgbus\.co\.kr|visitseoul\.net)/")
    probs += [f"source {k}" for k, (u, day, kind, n) in WD.SRC.items() if not official.match(u) or not re.fullmatch(r"20\d\d-\d\d(-\d\d)?", day) or day > WD.CHK or kind not in WX.KIND or len(n.split("|")) != 4]
    probs += [f"price {i}" for i, v in WD.ITEMS.items() if not (isinstance(v["p"], int) and v["p"] >= 0)]
    order = [i for c in WD.ORDER.values() for i in c]; scenes = [WD.scene(x) for _n, x in WD.SCENES]
    if len(set(order)) != len(order) or any(i not in WD.ITEMS for i in order) or any(i not in WD.ITEMS for sc in scenes for _q, i in sc): probs.append("question lists")
    at = lambda l, step, i: l[(i + i // len(l) * step) % len(l)]
    for i in range(365):
        day = [at(WD.ORDER[c], t, i) for c, t in (("ride", 3), ("table", 5), ("out", 7), ("market", 11))]
        if set(day) & {x for _q, x in at(scenes, 9, i)}: probs.append(f"day {i + 1} asks a price and then puts it on the bill"); break
    if not all(f"p(D.{n}, {t})" in WON.JS for n, t in (("o.ride", 3), ("o.table", 5), ("o.out", 7), ("o.market", 11), ("s", 9))): probs.append("lap steps differ from this check")
    words = list(WX.T.values()) + WX.HOW + [x for q in WX.FAQ for x in q] + [n for n, _x in WD.SCENES] + [v[3] for v in WD.SRC.values()] + ["|".join(v[f]) for v in WD.ITEMS.values() for f in ("n", "u", "tip") if v[f]]
    hole = lambda t: sorted(re.findall(r"\{\w\}", t))
    probs += [f"text: {w[:30]}" for w in words if len(w.split("|")) != 4 or not all(x.strip() for x in w.split("|")) or len({str(hole(x)) for x in w.split("|")}) != 1][:3]
    left = sorted({c for w in words for c in WX.pick(w, "zh-cn") if ord(c) > 0x3400 and not c.encode("gb2312", "ignore")})
    if left: probs.append("not simplified: " + "".join(left[:8]))
    # The owner works in payments: no payment company, wallet or card is named here. And no other game either.
    named = [w for w in ("Global Blue", "Alipay", "WeChat", "Visa", "Mastercard", "JCB", "UnionPay", "T-money", "Tmoney", "WOWPASS", "NAMANE", "Kakao", "Naver", "Toss", "Wise", "Revolut", "PayPal", "Apple Pay", "Google Pay", "utm_", "amzn", "Wordle", "Costcodle") if any(re.search(rf"\b{re.escape(w)}\b", p, re.I) for p in pages.values())]
    if named: probs.append("names " + ", ".join(named))
    if any(w in WON.JS for w in ("fetch(", "XMLHttpRequest", "sendBeacon", "WebSocket", "new Audio", "AudioContext", "vibrate")) or re.findall(r"\.src = ([^;]{6})", WON.JS) != ["'data:"]: probs.append("its script can send data or make a sound")
    if any(x not in ("gc.zgo.at",) for p in pages.values() for x in re.findall(r'<(?:script|img|link rel="stylesheet")[^>]+(?:src|href)="(?:https?:)?//([^/"]+)', p)): probs.append("loads something from elsewhere")
    if any(not has(f"won/og-{k}.png") or png_size(f"won/og-{k}.png") != "1200x630" for k in WX.LANGS) or any(png_size(f"won/icon-{n}.png") != f"{n}x{n}" for n in (192, 512)): probs.append("pictures")
    if any(json.loads(rd(WX.DIR[k] + "manifest.webmanifest"))["start_url"] != "/" + WX.DIR[k] or f'href="/{WX.DIR[k]}manifest.webmanifest"' not in pages[k] for k in WX.LANGS): probs.append("manifest")
    check(not probs, f"Seoul price game: {len(WD.ITEMS)} prices from dated official pages, five languages, in the sitemap only, nothing sent, no payment company named", "; ".join(probs[:5]))

    # The repo is public: the owner's given name, romanised name, PC account and private mail name must not come back (docs say 운영자).
    # Only the first five hex digits of each hash stand here, so the names cannot be read back out of this file.
    gone = {"43274", "0e75b", "75bf2", "49a69", "758e4"}; seen = {}
    for f in subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True).stdout.decode("utf-8").split("\0"):
        if not re.search(r"\.(md|py|html|js|json|css|txt|xml|yml|ps1|webmanifest)$", f) or not has(f): continue
        t = open(os.path.join(ROOT, f), encoding="utf-8", errors="ignore").read()
        for w in {w[i:i + 2] for w in re.findall(r"[가-힣]{2,}", t) for i in range(len(w) - 1)} | set(re.findall(r"[a-z0-9]{5,}", t.lower())): seen.setdefault(w, f)
    named = sorted({f for w, f in seen.items() if hashlib.sha256(w.encode()).hexdigest()[:5] in gone})
    check(not named, "no personal name or private account stands in the public repo", ", ".join(named[:5]))

    # Search index per language.
    idx_ok = all(len(json.loads(rd(d + "search.json"))["faq"]) > 20 and len(json.loads(rd(d + "search.json"))["cards"]) > 20 for d in LANG_DIRS)
    check(idx_ok, "search index has questions and Korean cards in every language")

    # Sitemap: public pages in, the personal page out.
    sm = rd("sitemap.xml")
    check(all(f"easymodekorea.com/{d}{n}</loc>" in sm for d in LANG_DIRS for n in ("phrases.html", "help.html", "privacy.html")) and "saved.html" not in sm
          and all('content="noindex"' in rd(d + "saved.html") for d in LANG_DIRS), "sitemap lists cards, help and privacy; My trip stays out of search")

    # What sets the site apart from an AI answer: dated facts, sources and logged changes, readable by people and machines.
    slugs = re.findall(r"easymodekorea\.com/([a-z0-9-]+)\.html\): .+\(checked \d{4}-\d\d-\d\d\)", rd("llms.txt"))
    full = rd("llms-full.txt")
    check(len(slugs) >= 21 and all(f"URL: https://easymodekorea.com/{s}.html" in full for s in slugs) and "Sources" in full and "Rule changes logged" in rd("llms.txt"),
          "llms.txt lists every guide with its answer and check date; llms-full.txt has each guide's text and sources", f"{len(slugs)} guides")
    probs = []
    for d in LANG_DIRS:
        g = rd(d + "ktx-train-booking.html"); h = rd(d + "index.html")
        if '"lastReviewed"' not in g or '"citation"' not in g: probs.append(d + "guide: no lastReviewed/citation in JSON-LD")
        if 'class="changed"' not in g: probs.append(d + "guide: no change block")
        if 'class="trust-line"' not in h: probs.append(d + "home: no trust line")
        if 'id="setup"' not in rd(d + "taxi.html"): probs.append(d + "taxi: no setup choice")
        if 'id="places"' not in rd(d + "saved.html"): probs.append(d + "My trip: no places list")
    check(not probs, "guides show what changed, how they were checked and a setup choice; home shows the trust line (all languages)", "; ".join(probs[:4]))

    # Trouble flows and the holiday table: five languages, every sourced step dated, every source a real link.
    import trouble as TR
    iso = re.compile(r"\d{4}-\d\d-\d\d$")
    probs = []
    for f in TR.FLOWS:
        for s in f["steps"]:
            if set(s["t"]) != set(TR.L5) or not all(s["t"].values()): probs.append(f["id"] + ": step text missing a language")
            if bool(s["src"]) != bool(s["d"]) or (s["d"] and not iso.match(s["d"])): probs.append(f["id"] + ": a step has a source without a date, or a date without a source")
            probs += [f["id"] + ": unknown source " + k for k in s["src"] if not k.startswith("guide:") and k not in TR.SRC]
        for d in LANG_DIRS:
            page = d + f["slug"] + ".html"
            if not has(page): probs.append("missing " + page); continue
            h = rd(page)
            if h.count('class="fact-src"') < 2 or '"lastReviewed"' not in h or '"HowTo"' not in h or 'class="sayrow"' not in h: probs.append(page + ": steps, dates or cards missing")
            if page not in files: probs.append(page + ": not in the offline list")
    probs += [k + ": source is not an https link" for k, (_n, u) in TR.SRC.items() if not u.startswith("https://")]
    for a in TR.ALERTS:
        if not (iso.match(a["from"]) and iso.match(a["to"]) and a["from"] <= a["to"]): probs.append(a["id"] + ": dates")
        if any(set(p["t"]) != set(TR.L5) or not p["src"] or any(k not in TR.SRC for k in p["src"]) for p in a["points"]): probs.append(a["id"] + ": a point lacks a language or a source")
    for d in LANG_DIRS:
        if 'id="alerts-data"' not in rd(d + "index.html") or 'id="trip-from"' not in rd(d + "saved.html"): probs.append(d + ": holiday alerts or trip dates missing")
        if 'id="pack"' not in rd(d + "saved.html") or 'id="share-make"' not in rd(d + "saved.html") or 'class="glist flows"' not in rd(d + "help.html"): probs.append(d + ": offline pack, sharing or help hub missing")
    check(not probs, f"{len(TR.FLOWS)} trouble flows and {len(TR.ALERTS)} holiday alerts: all languages, every sourced step dated, on the offline list", "; ".join(probs[:4]))
    check("qr.js" in pre and all(f["slug"] in rd("llms.txt") for f in TR.FLOWS), "share code script is in the offline list; llms.txt lists the trouble flows")

    # Korea Ready check: five languages, built only from dated answers; anything added carries a date and a source, or neither.
    probs = []
    for d in LANG_DIRS:
        page = d + "ready.html"
        if not has(page): probs.append("missing " + page); continue
        h = rd(page)
        data = json.loads(re.search(r'<script type="application/json" id="ready-data">(.*?)</script>', h, re.S).group(1).replace("<\\/", "</"))
        if page not in files or f"easymodekorea.com/{page}</loc>" not in sm: probs.append(page + ": not in the offline list or the sitemap")
        if len(data["tasks"]) < 5 or not all(iso.match(t["d"]) and len(t["v"]) >= 3 for t in data["tasks"]): probs.append(page + ": an app answer has no check date or lacks a setup")
        for k, x in data["x"].items():
            if bool(x.get("d")) != bool(x.get("src")) or (x.get("d") and not iso.match(x["d"])): probs.append(f"{page}: step {k} has a date without a source, or a source without a date")
        for t in data["tasks"]:
            nc = t.get("nc")
            if nc and not (iso.match(nc["d"]) and nc["src"][1].startswith("https://") and nc["t"]): probs.append(f"{page}: 'needs check' note on {t['id']} lacks a date or a source")
        if not all(v for v in data["t"].values()): probs.append(page + ": empty text")
        if re.search(r'<input[^>]+type="(text|search|email|tel)"', h.split('id="ready"')[1].split('id="ready-data"')[0]): probs.append(page + ": the check asks for typing")
        for g in ("index.html", "saved.html", "taxi.html", "foreign-card-declined-korea.html"):
            if 'class="ready-cta" href="ready.html"' not in rd(d + g): probs.append(d + g + ": no way into the Ready check")
    check(not probs and "ready.html" in rd("llms.txt"), "Korea Ready check: all languages, taps only, every added fact dated and sourced, reachable from home, My trip, guides and flows", "; ".join(probs[:4]))

    # Search pages (31차): five languages, Korean only on the cards and in the label words a fact quotes, every fact sourced and dated, each page reachable inside the site, no two titles alike.
    import landing as LD, moments as MO
    probs = []; titles = {}
    def five(o, at):
        if isinstance(o, dict) and set(o) >= set(TR.L5):
            probs.extend(f"{at}: {l} empty or has Korean in it" for l in TR.L5 if not o[l] or (re.search("[가-힣]", o[l]) and ".facts" not in at))
        elif isinstance(o, dict): [five(v, f"{at}.{k}") for k, v in o.items()]
        elif isinstance(o, (list, tuple)): [five(v, at) for v in o]
    for p in LD.FOOD:
        five(p, p["slug"])
        if not all(re.search("[가-힣]", c["ko"]) for c in [p["main"]] + p["more"] + p["ask"]): probs.append(p["slug"] + ": a card has no Korean")
        if not set(p["pick"].split(",")) <= {a[0] for a in MO.ALLERGY + MO.AVOID}: probs.append(p["slug"] + ": picks a food the food card does not have")
        probs += [p["slug"] + ": unknown source " + f["src"] for f in p["facts"] if f["src"] not in LD.SRC and f["src"] not in MO.SRC]
    five(LD.NONUM, LD.NONUM["slug"]); five(LD.T, "text")
    probs += [k + ": source is not an https link" for k, (_n, u) in LD.SRC.items() if not u.startswith("https://")]
    for d in LANG_DIRS:
        for s in LD.SLUGS:
            page = d + s + ".html"
            if not has(page): probs.append("missing " + page); continue
            h = rd(page); ti = re.search("<title>(.*?)</title>", h).group(1)
            if ti in titles: probs.append(f"{page}: same title as {titles[ti]}")
            titles[ti] = page
            if page not in files or f"easymodekorea.com/{page}</loc>" not in sm: probs.append(page + ": not in the offline list or the sitemap")
            if '"FAQPage"' not in h or '"lastReviewed"' not in h or h.count('rel="alternate"') < 5: probs.append(page + ": structured data or language links missing")
            if f'href="{s}.html"' not in rd(d + ("refused.html" if s == LD.NONUM["slug"] else "my-card.html")): probs.append(page + ": no link to it inside the site")
    check(not probs and all(s in rd("llms.txt") for s in LD.SLUGS), f"{len(LD.SLUGS)} search pages: all languages, sourced, linked, on the offline list, no two titles alike", "; ".join(probs[:4]))

    # Web manifest.
    m = json.loads(rd("manifest.webmanifest")); probs = []
    for k in ("id", "name", "short_name", "start_url", "scope", "display", "icons", "theme_color", "background_color"):
        if not m.get(k): probs.append("missing " + k)
    if m.get("display") != "standalone" or m.get("start_url") != "/": probs.append("display or start_url")
    for ic in m["icons"] + [i for s in m.get("shortcuts", []) for i in s["icons"]] + m.get("screenshots", []):
        rel = ic["src"].lstrip("/")
        if not has(rel): probs.append("missing " + rel)
        elif png_size(rel) != ic["sizes"]: probs.append(f"{rel} is {png_size(rel)}, manifest says {ic['sizes']}")
    purposes = {i.get("purpose") for i in m["icons"]}
    if not {"any", "maskable"} <= purposes or not any(i["sizes"] == "192x192" for i in m["icons"]) or not any(i["sizes"] == "512x512" for i in m["icons"]): probs.append("icon set incomplete")
    if any(not has(s["url"].lstrip("/")) for s in m.get("shortcuts", [])): probs.append("shortcut target missing")
    if len(m.get("screenshots", [])) < 2 or len({s["sizes"] for s in m["screenshots"]}) != 1: probs.append("screenshots")
    check(not probs, "web manifest is complete (icons, shortcuts, screenshots)", "; ".join(probs[:4]))

    # Android: link file and wrapper settings agree with each other and with the manifest.
    links = json.loads(rd(".well-known/assetlinks.json")); probs = []
    for entry in links:
        if entry["target"]["package_name"] != A.PACKAGE_ID: probs.append("package name")
        probs += [fp for fp in entry["target"]["sha256_cert_fingerprints"] if not re.fullmatch(r"([0-9A-F]{2}:){31}[0-9A-F]{2}", fp)]
    check(isinstance(links, list) and not probs, "Android link file (assetlinks.json) is valid", "; ".join(probs[:3]))
    if has("android/twa-manifest.json"):
        tw = json.loads(rd("android/twa-manifest.json"))
        ok = (tw["packageId"] == A.PACKAGE_ID and tw["host"] == "easymodekorea.com" and tw["startUrl"] == m["start_url"] and tw["backgroundColor"].lower() == m["background_color"].lower()
              and tw["themeColor"].lower() == m["theme_color"].lower() and tw["display"] == "standalone" and not tw.get("enableNotifications"))
        check(ok, "Android wrapper settings match the web manifest")

    # Play listing: every language within Play's limits, and the count written next to each line is the real one.
    if has("store/listing.md"):
        ls = rd("store/listing.md").replace("\r\n", "\n")
        rows = re.findall(r"\*\*(App name|Short description)\*\* \((\d+)\): `([^`]+)`", ls)
        fulls = re.findall(r"\*\*Full description\*\*\n\n```\n(.*?)\n```", ls, re.S)
        bad = [t for k, n, t in rows if int(n) != len(t) or len(t) > (30 if k == "App name" else 80)] + [t[:30] for t in fulls if len(t) > 4000]
        check(len(rows) == 10 and len(fulls) == 5 and not bad, "Play listing: five languages, every text within Play's limits", "; ".join(bad[:3]))

    # The signing script shows Korean text; Windows PowerShell only reads that right from UTF-8 with a BOM.
    check(open(os.path.join(ROOT, "android", "sign-aab.ps1"), "rb").read(3) == bytes([0xEF, 0xBB, 0xBF]), "signing script is saved as UTF-8 with BOM")

    # No signing keys or app packages in the repo.
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split("\n")
    secrets = [f for f in tracked if re.search(r"\.(jks|keystore|p12|pfx|aab|apk)$", f)]
    check(not secrets, "no signing keys or app packages are committed", ", ".join(secrets))

    print("\n" + ("ALL CHECKS PASSED" if not FAILS else f"{len(FAILS)} CHECK(S) FAILED"))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
