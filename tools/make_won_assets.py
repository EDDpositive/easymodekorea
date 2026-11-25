"""Makes the icons and the link-preview pictures of the daily price game (won/).

Run from the repo root after a build:  python tools/make_won_assets.py
Needs Pillow and Microsoft Edge or Chrome (tools/cdp.py). Everything is drawn from src/won_art.py and src/won_text.py: no photos, no fonts to ship.
"""
import html, io, os, sys, urllib.parse
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path[:0] = [os.path.dirname(os.path.abspath(__file__)), os.path.join(ROOT, "src")]
import cdp  # noqa: E402
import won_art as A  # noqa: E402
import won_data as W  # noqa: E402
import won_text as X  # noqa: E402

SIGN = '<path d="M15 23l8 22 9-22 9 22 8-22M12 32h40" fill="none" stroke="#1b1c1e" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
FONT = 'ui-rounded,system-ui,"Segoe UI",sans-serif'
CJK = {"ja": '"Yu Gothic","Yu Gothic UI",', "zh-tw": '"Microsoft JhengHei","Noto Sans TC",', "zh-cn": '"Microsoft YaHei UI",'}
SHOWN = ["bib", "gyeong", "taxi"]


def snap(w, h, body, path, colours=0):
    b = cdp.Browser(w, h, 1, port=9471)
    try:
        b.go("data:text/html;charset=utf-8," + urllib.parse.quote("<!doctype html><meta name=viewport content='width=device-width'><style>*{box-sizing:border-box}body{margin:0}</style>" + body), wait=.6)
        b.shot(path)
    finally:
        b.close()
    im = Image.open(path).convert("RGB")
    if im.size != (w, h): raise SystemExit(f"{path}: {im.size}")
    if colours: im = im.quantize(colours, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
    im.save(path, optimize=True)


def icon():
    """Full-bleed yellow, the sign well inside the safe circle, so one file also works as a maskable icon."""
    big = os.path.join(ROOT, "won", "icon-512.png")
    snap(512, 512, f'<div style="width:512px;height:512px;background:#ffde45;display:grid;place-items:center"><svg width="340" height="340" viewBox="4 4 56 56">{SIGN}</svg></div>', big, 64)
    Image.open(big).convert("RGB").resize((192, 192), Image.LANCZOS).quantize(64, method=Image.MEDIANCUT, dither=Image.Dither.NONE).save(os.path.join(ROOT, "won", "icon-192.png"), optimize=True)


def pic(i):
    x = W.ITEMS[i]
    return f'<svg width="78" height="78" viewBox="0 0 64 64" fill="none" stroke="#1b1c1e" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{A.ART[x["art"]].replace(chr(34) + "C" + chr(34), chr(34) + x["c"] + chr(34))}</svg>'


def og(lang):
    e = lambda s: html.escape(X.pick(s, lang))
    rows = "".join(f'<div style="display:flex;align-items:center;gap:22px;background:#fffbe8;border-radius:16px;padding:8px 26px 8px 18px;font-size:38px;font-weight:700;line-height:1.1">{pic(i)}<span style="flex:1">{e(W.ITEMS[i]["n"])}</span><b style="font-size:46px;font-weight:900;color:#b5140b">₩ ?</b></div>' for i in SHOWN)
    title = X.pick(X.T["h1"], lang)
    body = f"""<div lang="{X.TAG[lang]}" style="width:1200px;height:630px;background:#c2180e;padding:34px 46px;font-family:{CJK.get(lang, '')}{FONT};color:#1b1c1e;-webkit-text-stroke:{".7px" if lang in ("ja", "zh-tw") else "0"}">
<div style="background:#1b1c1e;border-radius:34px;padding:12px;height:562px;display:flex;flex-direction:column;gap:12px">
<div style="background:#ffde45;border-radius:24px;padding:16px 30px 20px;display:flex;align-items:center;justify-content:space-between;gap:30px">
<div style="font-size:{72 if len(title) < 22 else 64}px;font-weight:900;letter-spacing:-.02em;line-height:1.1">{e(X.T["h1"])}</div>
<div style="display:flex;align-items:center;gap:12px;font-size:32px;font-weight:800;white-space:nowrap"><svg width="54" height="54" viewBox="0 0 64 64"><circle cx="32" cy="32" r="29" fill="#fff" stroke="#1b1c1e" stroke-width="4"/>{SIGN}</svg>{X.BRAND}</div></div>
<div style="display:grid;gap:10px;flex:1;align-content:stretch">{rows}</div>
<div style="color:#ffde45;font-size:{26 if lang == "vi" else 30}px;font-weight:700;text-align:center;padding:2px 0 8px">{e(X.T["lede"])}</div>
</div></div>"""
    snap(1200, 630, body, os.path.join(ROOT, "won", f"og-{lang}.png"), 128)


if __name__ == "__main__":
    icon()
    for k in X.LANGS: og(k)
    for f in sorted(os.listdir(os.path.join(ROOT, "won"))):
        if f.endswith(".png"): print(f, os.path.getsize(os.path.join(ROOT, "won", f)) // 1024, "KB")
