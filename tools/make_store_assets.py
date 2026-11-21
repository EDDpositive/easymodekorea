"""Makes the app icons, the phone screenshots and the Play feature graphic.

Run from the repo root after a build:  python tools/make_store_assets.py
Needs Pillow and Microsoft Edge or Chrome (driven headless by tools/cdp.py; it starts its own local server).
Icons are drawn here, so they can be rebuilt without any design tool.
"""
import os, shutil, sys, time
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
import cdp  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
BLUE, RED, WHITE = "#2336e8", "#c62828", "#ffffff"

def out(rel):
    p = os.path.abspath(os.path.join(ROOT, rel)); os.makedirs(os.path.dirname(p), exist_ok=True); return p


def shortcut(name, bg, draw_glyph):
    """96px launcher shortcut icon: a coloured disc with a white glyph, drawn at 4x and scaled down."""
    s = 384; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([0, 0, s - 1, s - 1], fill=bg); draw_glyph(d, s)
    im.resize((96, 96), Image.LANCZOS).save(out(name), optimize=True)


def glyph_help(d, s):
    c = s // 2; t = 36; r = 104
    d.rounded_rectangle([c - t, c - r, c + t, c + r], 14, fill=WHITE); d.rounded_rectangle([c - r, c - t, c + r, c + t], 14, fill=WHITE)


def glyph_cards(d, s):
    d.rounded_rectangle([84, 96, 300, 250], 30, fill=WHITE); d.polygon([(120, 240), (120, 306), (186, 240)], fill=WHITE)
    try: f = ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf", 120)
    except OSError: f = None
    if f: d.text((192, 168), "가", font=f, fill=BLUE, anchor="mm")


def glyph_trip(d, s):
    d.polygon([(124, 88), (260, 88), (260, 300), (192, 250), (124, 300)], fill=WHITE)


def icons():
    shutil.copyfile(os.path.join(ROOT, "icon-512.png"), out("icon-maskable-512.png"))  # the mark already sits inside the safe zone
    shortcut("shortcut-help.png", RED, glyph_help); shortcut("shortcut-cards.png", BLUE, glyph_cards); shortcut("shortcut-trip.png", BLUE, glyph_trip)


def screenshots():
    """Phone screenshots at 360x640 drawn at 3x (1080x1920, the 9:16 size Play recommends), light theme."""
    srv = cdp.Server(os.path.abspath(ROOT)); b = cdp.Browser(360, 640, 3, "light")
    try:
        for page, name, after in (("", "home", ""), ("ready.html", "ready", ""), ("taxi.html", "guide", ""), ("taxi.html", "show", "document.querySelector('[data-show]').click()"),
                                  ("phrases.html", "cards", "document.getElementById('cards').scrollIntoView()"), ("help.html", "help", "")):
            b.go(srv.url + page)
            if not page:  # keep the install prompt out of the pictures
                b.js("localStorage.setItem('emk-install-no', String(Date.now())); localStorage.setItem('emk-ready', '1')"); b.go(srv.url)
            if name == "ready":  # a finished check with some steps ticked, as a traveler would see it a week before the flight
                b.js("localStorage.setItem('emk-rc', JSON.stringify({p: 'visitor', dev: 'ios', pay: 'card', air: 'icn', city: ['busan'], food: 'no', from: '', to: ''}));"
                     "localStorage.setItem('wik-setup', 'visitor|ios'); localStorage.setItem('wik-plan-en-visitor-ios', '[0,1,2,3,4]'); localStorage.setItem('emk-rc-x', JSON.stringify(['checked', 'pay-card']))")
                b.go(srv.url + page, wait=1.2)
            if after: b.js(after); time.sleep(0.4)
            b.shot(out(f"shots/{name}.png")); flatten(f"shots/{name}.png")
            if name == "ready": b.js("['emk-rc', 'emk-rc-x', 'emk-rc-score', 'wik-setup', 'wik-plan-en-visitor-ios', 'emk-saved'].forEach(k => localStorage.removeItem(k))")
        b.cmd("Emulation.setDeviceMetricsOverride", width=1024, height=500, deviceScaleFactor=1, mobile=False)
        b.go(srv.url + "store/feature.html", wait=2.5); b.shot(out("store/feature-graphic.png")); flatten("store/feature-graphic.png")
    finally:
        b.close(); srv.stop()


def flatten(rel):
    im = Image.open(out(rel)).convert("RGB"); im.save(out(rel), optimize=True)  # 24-bit, no alpha, as Play asks
    print(rel, im.size)


if __name__ == "__main__":
    icons()
    if "--icons-only" not in sys.argv: screenshots()
