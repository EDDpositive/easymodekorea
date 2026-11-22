"""Prints how many words a visitor sees on the main screens at 375x812: on the first screen and on the whole page
(closed sections stay closed). Run after a build:  python tools/text_density.py [--max]
With --max it fails when an English screen goes over LIMITS (the standing rule in docs/critique.md 26차).
tools/browser_check.py runs the same check."""
import os, sys

sys.path.insert(0, os.path.dirname(__file__))
import cdp  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
JS = open(os.path.join(os.path.dirname(__file__), "text_density.js"), encoding="utf-8").read()
# A finished Korea Ready check, so the result screen is measured too.
READY = ("localStorage.setItem('emk-rc', JSON.stringify({p: 'visitor', dev: 'android', pay: 'card', air: 'icn', city: ['busan'], food: 'no', from: '', to: ''}));"
         "localStorage.setItem('emk-install-no', String(Date.now())); localStorage.setItem('emk-ready', '1')")
# app: tool screens, labels and one-line items. answer: a guide or a "something went wrong" flow, which also shows
# the dated facts. list: the Korean cards, a long list of short labels (no whole-page limit).
# "sentences" counts text pieces longer than 8 words on the first screen.
LIMITS = {"app": {"first": 70, "sentences": 3, "all": 300},
          "answer": {"first": 130, "sentences": 8, "all": 330},   # 27차: the slimmer top bar fits more of the answer on one screen
          "list": {"first": 90, "sentences": 3, "all": 10 ** 6}}   # 27차: the first screen is the cards themselves (Korean + meaning)
PAGES = [("", "home", "app"), ("taxi.html", "guide: taxi", "answer"), ("incheon-airport-to-seoul.html", "guide: airport", "answer"),
         ("ready.html", "ready: result", "app"), ("saved.html", "my trip", "app"), ("phrases.html", "korean cards", "list"),
         ("help.html", "help", "app"), ("foreign-card-declined-korea.html", "flow: card", "answer")]


def main():
    srv = cdp.Server(ROOT); b = cdp.Browser(375, 812, 1, "light"); out = []
    try:
        b.go(srv.url, wait=0.3); b.js(READY)
        for lang in ("", "ja/"):
            for page, name, kind in PAGES:
                b.go(srv.url + lang + page, wait=0.4)
                r = b.js(JS); out.append((lang + name, kind, r["first"], r["sentences"], r["all"]))
    finally:
        b.close(); srv.stop()
    over = []
    for name, kind, f, n, a in out:
        lim = LIMITS[kind]; bad = not name.startswith("ja/") and (f > lim["first"] or n > lim["sentences"] or a > lim["all"])
        print(f"{name:24} first screen {f:4} words, {n:2} long lines   whole page {a:5}{'   OVER' if bad else ''}")
        if bad: over.append(name)
    if "--max" in sys.argv and over:
        print("over the limit: " + ", ".join(over)); sys.exit(1)


if __name__ == "__main__":
    main()
