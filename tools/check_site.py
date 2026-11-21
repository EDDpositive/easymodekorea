"""Checks the built site without a browser. Run from the repo root after a build:
    python tools/check_site.py
Covers what the app experience depends on: every page is app-ready, the offline list is complete,
the manifest and the Android link file are valid, all five languages have the app pages, and no
link inside the site is broken. Exit code 0 means every check passed.
"""
import json, os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
import app_shell as A  # noqa: E402

LANG_DIRS = ["", "ja/", "zh-tw/", "zh-cn/", "vi/"]
FAILS = []
rd = lambda rel: open(os.path.join(ROOT, rel), encoding="utf-8").read()
has = lambda rel: os.path.exists(os.path.join(ROOT, rel))


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
            if re.match(r"^(https?:|mailto:|tel:|//)", href): continue
            t = href.lstrip("/") if href.startswith("/") else os.path.normpath(os.path.join(base, href)).replace("\\", "/")
            t = "" if t == "." else t
            if not (has(t) and not os.path.isdir(os.path.join(ROOT, t)) or has(os.path.join(t, "index.html"))): broken.append(f"{f} -> {href}")
    check(not broken, "no broken links inside the site", "; ".join(broken[:4]))

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
