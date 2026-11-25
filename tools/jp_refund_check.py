"""Compares the airport floors on the Japan tax refund page with Japan Customs' own list (needs the network, not run in CI).

    python tools/jp_refund_check.py

Prints every airport whose floor or phone option differs, and airports the page does not have. Exit code 0 = all the same.
"""
import json, os, re, sys, urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import jp_refund as J  # noqa: E402

URL = "https://www.customs.go.jp/kaigairyoko/taxrefund/js/refund_kioskmap.json"
WIDE = str.maketrans("０１２３４５６７８９", "0123456789")


def main():
    r = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"}), timeout=30)
    print("official file dated", r.headers.get("Last-Modified"))
    off = {}
    for x in json.loads(r.read().decode("utf-8-sig")):
        if x["porttype"] != "Airport": continue
        floor = re.search(r"(\d)階", (x["messageJa"] or "").translate(WIDE)); term = re.search(r"T(\d)", x["terminal"] or "")
        iata = {"SPK": "CTS"}.get(x["iatacode"], x["iatacode"])
        off[iata + (term.group(1) if term and iata in ("NRT", "HND", "KIX", "NGO") else "")] = (floor.group(1) if floor else "", x["VJW"] == "yes")
    bad = 0
    for i, name, place, phone in J.AIR_TOP + J.AIR:
        m = re.search(r"(\d)층", place); mine = (m.group(1) if m else "", bool(phone))
        if off.get(i) != mine: bad += 1; print("DIFFERENT", i, name, "page", mine, "official", off.get(i))
    for k in sorted(set(off) - {p[0] for p in J.AIR_TOP + J.AIR}): bad += 1; print("MISSING", k, off[k])
    print("same" if not bad else f"{bad} to fix")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
