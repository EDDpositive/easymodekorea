"""Checks the built site in a real (headless) browser at phone size.

Run from the repo root after a build:  python tools/browser_check.py
It starts its own local server, then checks:
  1. the browser finds no reason the site can't be installed as an app,
  2. every page fits a 375px screen and has the bottom tabs and the shared script,
  3. with the server switched off, saved pages still open (true offline test),
  4. opened as an installed app, pages run in app mode and start in the language chosen last time,
  5. tap sizes, the Back button on a full-screen card, and the offline notices.
Exit code 0 means every check passed.
"""
import json, os, re, sys, time

sys.path.insert(0, os.path.dirname(__file__))
import cdp  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FAILS = []


def check(ok, label, detail=""):
    print(("PASS  " if ok else "FAIL  ") + label + (f"  ({detail})" if detail and not ok else ""))
    if not ok: FAILS.append(label)


SWEEP = """(async () => {
  const pages = %s, out = {overflow: [], noTabs: [], noApp: []};
  const one = p => new Promise(res => { const f = document.createElement('iframe');
    f.style.cssText = 'position:fixed;left:-9999px;top:0;width:375px;height:812px;border:0';
    f.onload = () => setTimeout(() => { try { const d = f.contentDocument, w = f.contentWindow;
      if (d.documentElement.scrollWidth > 375) out.overflow.push(p);
      if (p !== 'hosts.html') { if (d.querySelectorAll('.tabbar a').length !== 4) out.noTabs.push(p); if (!w.emkToast) out.noApp.push(p); }
    } catch (e) { out.noApp.push(p + ' ' + e.message); } f.remove(); res(); }, 250);
    f.src = '/' + (p === './' ? '' : p); document.body.append(f); });
  let i = 0; await Promise.all(Array.from({length: 8}, async () => { while (i < pages.length) await one(pages[i++]); }));
  return out; })()"""


# Things people tap with a thumb must be at least 40px tall (most are 44px or more).
TAPS = """(() => {
  const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && !e.closest('[hidden]') && !e.closest('details:not([open]) > :not(summary)'); };
  return [...document.querySelectorAll('.tabbar a, .jump a, .sit-links a, .glist a, .sayrow button, a.call, .act, .icon-btn, .lang-menu > summary, .btn, .chip, .opt-big')]
    .filter(vis).map(e => ({t: (e.innerText || e.getAttribute('aria-label') || e.className).trim().slice(0, 24), h: Math.round(e.getBoundingClientRect().height)})).filter(x => x.h < 40);
})()"""


def main():
    pre = json.loads(re.search(r"const PRE=(\[[^\]]*\]);", open(os.path.join(ROOT, "sw.js"), encoding="utf-8").read()).group(1))
    pages = [p for p in pre if p.endswith("/") or p.endswith(".html")]
    srv = cdp.Server(ROOT); b = cdp.Browser(375, 812, 1, "light")
    try:
        check(b.go(srv.url), "home page loads")
        man = b.cmd("Page.getAppManifest")
        check(not man.get("errors"), "web manifest has no errors", json.dumps(man.get("errors")))
        errs = b.cmd("Page.getInstallabilityErrors").get("installabilityErrors", [])
        check(not errs, "browser reports the site as installable", json.dumps(errs))

        b.js("navigator.serviceWorker.ready.then(() => true)")
        n = 0
        for _ in range(60):
            n = b.js("caches.keys().then(ks => Promise.all(ks.map(k => caches.open(k).then(c => c.keys())))).then(a => a.flat().length)")
            if n >= 30: break
            time.sleep(0.5)
        check(n >= 30, "offline copy saved on first visit", f"{n} files")
        told = False
        for _ in range(20):
            told = b.js("localStorage.getItem('emk-ready') === '1'")
            if told: break
            time.sleep(0.3)
        check(bool(told), "first visit: the reader is told the guides are now on the phone")
        b.js("localStorage.setItem('emk-install-no', String(Date.now()))")

        small = []
        for page in ("", "taxi.html", "phrases.html", "saved.html", "help.html", "ja/", "vi/phrases.html"):
            b.go(srv.url + page, wait=0.5)
            small += [f"/{page} {x['t']} {x['h']}px" for x in b.js(TAPS)]
        check(not small, "buttons and links are at least 40px tall on the main screens", "; ".join(small[:5]))
        check(b.js("document.querySelectorAll('#jump a').length") == 8 if b.go(srv.url, wait=0.5) else False, "home shows all eight situations as a jump grid")

        b.go(srv.url + "taxi.html", wait=0.5)
        b.js("document.querySelector('[data-show]').click()")
        opened = b.js("!document.getElementById('show').hidden")
        b.js("history.back()"); time.sleep(0.5)
        check(opened and b.js("document.getElementById('show').hidden && location.pathname === '/taxi.html'"), "the Back button closes a full-screen card and stays on the guide")

        b.cmd("Network.enable"); b.cmd("Network.emulateNetworkConditions", offline=True, latency=0, downloadThroughput=-1, uploadThroughput=-1); time.sleep(0.5)
        strip = b.js("(() => { const s = document.querySelector('.net-strip'); return !!s && !s.hidden && s.textContent.length > 5; })()")
        b.cmd("Network.emulateNetworkConditions", offline=False, latency=0, downloadThroughput=-1, uploadThroughput=-1); time.sleep(0.5)
        check(strip and b.js("document.querySelector('.net-strip').hidden"), "an offline strip shows while there is no connection and goes away after")

        r = b.js(SWEEP % json.dumps(pages))
        check(not r["overflow"], f"{len(pages)} pages fit a 375px screen", ", ".join(r["overflow"][:5]))
        check(not r["noTabs"], "every page has the four bottom tabs", ", ".join(r["noTabs"][:5]))
        check(not r["noApp"], "every page loads the shared app script", ", ".join(r["noApp"][:5]))

        srv.stop()  # from here on there is no server: only the copy on the "phone" can answer
        for page in ("", "taxi.html", "phrases.html", "saved.html", "help.html", "privacy.html"):
            ok = b.go(srv.url + page, wait=0.6) and b.js("document.querySelectorAll('.tabbar a').length === 4 && document.title.includes('EasyModeKorea')")
            check(bool(ok), f"offline: /{page} opens")
        # The sweep above saved every page, so take one off the "phone" first (and empty the browser's own short-term cache).
        b.js("caches.keys().then(ks => Promise.all(ks.map(k => caches.open(k).then(c => c.delete(location.origin + '/zh-tw/taxi.html')))))")
        b.cmd("Network.clearBrowserCache")
        ok = b.go(srv.url + "zh-tw/taxi.html", wait=0.8) and b.js("location.pathname.endsWith('/') && !!document.querySelector('.app-toast') && document.querySelector('.app-toast').textContent.length > 10")
        check(bool(ok), "offline: a page that was never saved leads to the home page with an explanation")

        # The browser cannot pretend to be an installed app, so the page is told it is one (the iOS flag app.js also reads).
        b.cmd("Page.addScriptToEvaluateOnNewDocument", source="Object.defineProperty(navigator, 'standalone', {value: true})")
        ok = b.go(srv.url + "taxi.html", wait=0.6) and b.js("document.documentElement.classList.contains('app')")
        check(bool(ok), "opened as an installed app: page runs in app mode")
        b.js("localStorage.setItem('emk-lang', 'ja'); sessionStorage.removeItem('emk-go')")
        b.go(srv.url, wait=1.0)
        check(b.js("location.pathname") == "/ja/", "installed app opens in the language chosen last time")
        b.js("sessionStorage.removeItem('emk-go')"); b.go(srv.url + "help.html", wait=1.0)
        check(b.js("location.pathname") == "/ja/help.html", "an app shortcut opens in that language too")
        if len(sys.argv) > 1: b.shot(sys.argv[1])
    finally:
        b.close(); srv.stop()
    print("\n" + ("ALL CHECKS PASSED" if not FAILS else f"{len(FAILS)} CHECK(S) FAILED"))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
