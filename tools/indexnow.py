"""Tells IndexNow search engines (Bing, Naver, Yandex and others) which pages exist, so new and changed
pages are picked up without waiting for a crawl. Bing's index also feeds several AI search products.

Run by hand AFTER a release is live, and only when the owner has agreed to it:
    python tools/indexnow.py            (prints what it would send)
    python tools/indexnow.py --send     (sends it)

It sends only public page addresses from sitemap.xml and the public key in <key>.txt at the site root.
Google does not use IndexNow; for Google, submit the sitemap in Search Console.
"""
import json, os, re, sys, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HOST = "easymodekorea.com"


def main():
    keys = [f[:-4] for f in os.listdir(ROOT) if re.fullmatch(r"[0-9a-f]{32}\.txt", f)]
    if not keys: sys.exit("No key file at the site root.")
    urls = re.findall(r"<loc>([^<]+)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read())
    body = {"host": HOST, "key": keys[0], "keyLocation": f"https://{HOST}/{keys[0]}.txt", "urlList": urls}
    print(f"{len(urls)} page addresses, key file https://{HOST}/{keys[0]}.txt")
    if "--send" not in sys.argv:
        print("Dry run. Add --send to submit."); return
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=json.dumps(body).encode("utf-8"), headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r: print("IndexNow answered", r.status)


if __name__ == "__main__":
    main()
