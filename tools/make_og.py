"""Makes the site's link-preview pictures (og.png and og-<lang>.png), one per language.

Run from the repo root after a build:  python tools/make_og.py
Needs Pillow and Microsoft Edge or Chrome (tools/cdp.py). The words come from the built home pages (title and the first
part of the description), so the picture says what the search result says. Fonts are the ones on the PC (Segoe UI,
Yu Gothic, Microsoft JhengHei, Microsoft YaHei, Malgun Gothic): nothing to ship. The old og.png showed empty boxes
instead of 日本語 and 中文 because it was drawn with a font that has no CJK letters.
"""
import html, os, re, sys, urllib.parse
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdp  # noqa: E402

LATIN = '"Segoe UI",system-ui,sans-serif'
FONT = {"en": LATIN, "vi": LATIN, "ja": '"Yu Gothic",' + LATIN, "zh-tw": '"Microsoft JhengHei",' + LATIN,
        "zh-cn": '"Microsoft YaHei",' + LATIN, "ko": '"Malgun Gothic","맑은 고딕",' + LATIN}  # headless Edge draws these three without bold, so their headline gets a thin outline instead (see .h)
LANGS = 'English · <span lang="ja">日本語</span> · <span lang="zh-Hant">繁體中文</span> · <span lang="zh-Hans">简体中文</span> · <span lang="vi" style="font-family:'+LATIN.replace('"',"'")+'">Tiếng Việt</span>'
PAGES = {"en": "index.html", "ja": "ja/index.html", "zh-tw": "zh-tw/index.html", "zh-cn": "zh-cn/index.html", "vi": "vi/index.html", "ko": "hosts.html"}


def words(lang):
    t = open(os.path.join(ROOT, PAGES[lang]), encoding="utf8").read()
    title = html.unescape((re.search(r'<meta property="og:title" content="([^"]*)"', t) or re.search(r"<title>([^<]*)", t)).group(1))
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', t).group(1))
    title = re.sub(r"^EasyModeKorea \| | \| EasyModeKorea$", "", title).replace("[숙소 사장님용] ", "")
    return title, re.split(r"[:：。]|\. ", desc)[0].strip()


def body(lang):
    head, line = words(lang)
    main, _, sub = head.partition("(")  # "(checked monthly)" goes on its own smaller line, so no line breaks in the middle of a word
    sub = "(" + sub if sub else ""
    cjk = lang in ("ja", "zh-tw", "zh-cn", "ko")
    size = 72 if len(main) <= (13 if cjk else 30) else 62
    css = (f"*{{box-sizing:border-box}}body{{margin:0}}.c{{width:1200px;height:630px;background:#2536e8;color:#fff;padding:84px 80px 0;font-family:{FONT[lang]};"
           "display:flex;flex-direction:column}.b{font:800 66px/1 " + LATIN + ";letter-spacing:-1px;display:flex;align-items:center;gap:12px}"
           ".k{background:#ffd23f;color:#101320;border-radius:12px;padding:6px 14px 10px}"
           f".h{{font-weight:{700 if cjk else 800};{'-webkit-text-stroke:1.6px #fff;' if lang in ('ja', 'zh-tw', 'ko') else ''}font-size:{size}px;line-height:1.2;margin-top:72px;max-width:1040px;word-break:{'keep-all' if lang == 'ko' else 'normal'};"
           "overflow-wrap:anywhere;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}"
           ".s{font-size:40px;font-weight:600;color:#ffd23f;margin-top:14px}"
           ".l{margin-top:auto;margin-bottom:60px;font-size:28px;font-weight:600;color:#cfd5ff;line-height:1.5}.l b{color:#fff;font-weight:700}")
    return (f'<style>{css}</style><div class="c" lang="{lang}"><div class="b">EasyMode<span class="k">Korea</span></div>'
            f'<div class="h">{html.escape(main.strip())}</div><div class="s">{html.escape(sub)}</div><div class="l"><b>{html.escape(line)}</b><br>{LANGS}</div></div>')


def snap(lang, path):
    b = cdp.Browser(1200, 630, 1, port=9481)
    try:
        b.go("data:text/html;charset=utf-8," + urllib.parse.quote("<!doctype html><meta name=viewport content='width=device-width'>" + body(lang)), wait=.8)
        if not b.js("document.fonts.check('16px \"Segoe UI\"')"): raise SystemExit("Segoe UI missing: run this on Windows")
        b.shot(path)
    finally:
        b.close()
    im = Image.open(path).convert("RGB")
    if im.size != (1200, 630): raise SystemExit(f"{path}: {im.size}")
    im.quantize(48, method=Image.MEDIANCUT, dither=Image.Dither.NONE).save(path, optimize=True)


if __name__ == "__main__":
    for lang in PAGES:
        out = os.path.join(ROOT, "og.png" if lang == "en" else f"og-{lang}.png")
        snap(lang, out); print(os.path.relpath(out, ROOT), os.path.getsize(out), words(lang))
