"""Looks up the daily price game's numbers on their official pages again (needs the network, not run in CI).

    python tools/won_price_check.py

Prints every price that no longer stands on its page, and pages that could not be read. Dated market pages (KAMIS) and postal notices keep their day's
values and are skipped. A free item counts as fine when the page still says 무료. Exit code 0 = nothing to look at.
"""
import gzip, html, os, re, sys, urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import won_data as W  # noqa: E402

SKIP = {"post1", "post2"}  # files, read once by hand


def text(url):
    r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "ko,en"}), timeout=40)
    b = r.read(); b = gzip.decompress(b) if b[:2] == b"\x1f\x8b" else b
    cs = (re.search(rb"charset=[\"']?([\w-]+)", b[:3000]) or [0, b"utf-8"])[1].decode()
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<!--.*?-->", "", b.decode(cs, "replace")))))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    bad = 0
    for k, (url, day, kind, _n) in W.SRC.items():
        mine = [(i, v["p"]) for i, v in W.ITEMS.items() if v["s"].split()[-1] == k]
        if kind == "retail" or k in SKIP or not mine: continue
        try: t = text(url)
        except Exception as x: bad += 1; print("UNREAD ", k, url, str(x)[:80]); continue
        def there(p):
            if p == 0: return any(w in t.lower() for w in ("무료", "무임", "free"))
            return re.search(rf"(?<![\d,]){p:,}(?!\d)|(?<![\d,]){p}(?!\d)" + (rf"|(?<!\d){p // 10000}만 ?원" if p % 10000 == 0 else ""), t)
        gone = [f"{i} {p:,}" for i, p in mine if not there(p)]
        if gone: bad += 1
        print("LOOK   " if gone else "ok     ", k, day, f"{len(mine) - len(gone)}/{len(mine)}", ", ".join(gone), url if gone else "")
    print("nothing to look at" if not bad else f"{bad} page(s) to look at")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
