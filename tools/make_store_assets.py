"""Makes the app icons, the phone screenshots and the Play feature graphic.

Run from the repo root after a build:  python tools/make_store_assets.py
Needs Pillow and Microsoft Edge or Chrome (driven headless by tools/cdp.py; it starts its own local server).
Icons are drawn here, so they can be rebuilt without any design tool.
"""
import os, shutil, sys, time, urllib.parse
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
import cdp  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
BLUE, RED, AMBER, TEAL, WHITE = "#2336e8", "#c62828", "#b45309", "#0f766e", "#ffffff"

def out(rel):
    p = os.path.abspath(os.path.join(ROOT, rel)); os.makedirs(os.path.dirname(p), exist_ok=True); return p


def shortcut(name, bg, draw_glyph):
    """96px launcher shortcut icon: a coloured disc with a white glyph, drawn at 4x and scaled down."""
    s = 384; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([0, 0, s - 1, s - 1], fill=bg); draw_glyph(d, s)
    im.resize((96, 96), Image.LANCZOS).save(out(name), optimize=True)


def glyph_sos(d, s):
    """A siren: dome, base and three rays."""
    d.pieslice([110, 120, 274, 320], 180, 360, fill=WHITE); d.rectangle([110, 218, 274, 244], fill=WHITE)
    d.rounded_rectangle([84, 252, 300, 292], 12, fill=WHITE)
    for x0, y0, x1, y1 in ((192, 62, 192, 98), (98, 98, 124, 124), (286, 98, 260, 124)): d.line([x0, y0, x1, y1], fill=WHITE, width=18)


def glyph_refused(d, s):
    """A bank card with a cross on it."""
    d.rounded_rectangle([76, 112, 308, 272], 26, fill=WHITE); d.rectangle([76, 144, 308, 172], fill=AMBER)
    d.line([160, 194, 224, 252], fill=AMBER, width=18); d.line([224, 194, 160, 252], fill=AMBER, width=18)


def glyph_card(d, s):
    """A fork and a knife."""
    for x in (108, 138, 168): d.rounded_rectangle([x, 80, x + 16, 176], 8, fill=WHITE)
    d.rounded_rectangle([108, 152, 184, 190], 18, fill=WHITE); d.rounded_rectangle([135, 176, 157, 304], 11, fill=WHITE)
    d.pieslice([220, 80, 300, 276], 180, 270, fill=WHITE); d.rectangle([238, 86, 260, 304], fill=WHITE); d.rounded_rectangle([238, 280, 260, 310], 11, fill=WHITE)


def glyph_trip(d, s):
    d.polygon([(124, 88), (260, 88), (260, 300), (192, 250), (124, 300)], fill=WHITE)


def icons():
    shutil.copyfile(os.path.join(ROOT, "icon-512.png"), out("icon-maskable-512.png"))  # the mark already sits inside the safe zone
    shortcut("shortcut-sos.png", RED, glyph_sos); shortcut("shortcut-refused.png", AMBER, glyph_refused); shortcut("shortcut-card.png", TEAL, glyph_card); shortcut("shortcut-trip.png", BLUE, glyph_trip)


# Captions for the framed Play screenshots (store/screenshots/). *words* are drawn in yellow. Each claim is something
# the app really does; keep them in step with store/listing.md.
FRAMES = [("sos", "No data? *Say where you are*", "The rescue code, worked out on your phone"),
          ("food", "Staff *tap the answer*, you read it", "My food card: make it once, use it offline"),
          ("refused", "Refused? *Three taps* to the next step", "Restaurant, taxi, KTX, ATM, app sign-up and more"),
          ("trip", "Each day, *only what matters*", "Tax refund before the bag goes, with reminders"),
          ("list", "Which Korean apps *work with your phone*", "A status for your phone on every guide"),
          ("ready", "Your plan *before the flight*, in one minute", "Taps only. Saved on your phone"),
          ("guide", "Short answers, *checked and dated*", "Each fact shows the day it was checked"),
          ("show", "Show a driver *in big Korean*", "Full screen, even offline")]


def screenshots():
    """Phone screenshots at 360x640 drawn at 3x (1080x1920, the 9:16 size Play recommends), light theme."""
    srv = cdp.Server(os.path.abspath(ROOT)); b = cdp.Browser(360, 640, 3, "light")
    try:
        b.cmd("Browser.grantPermissions", origin=srv.url.rstrip("/"), permissions=["geolocation"])
        b.cmd("Emulation.setGeolocationOverride", latitude=35.33697, longitude=127.73053, accuracy=8)
        day = "(n => { const t = new Date(Date.now() + n * 864e5); return t.getFullYear() + '-' + String(t.getMonth() + 1).padStart(2, '0') + '-' + String(t.getDate()).padStart(2, '0'); })"
        for page, name, after in (("", "home", ""), ("ready.html", "ready", ""), ("taxi.html", "guide", ""), ("taxi.html", "show", "document.querySelector('[data-show]').click()"),
                                  ("sos.html", "sos", "document.getElementById('sos-find').click()"),
                                  ("my-card.html", "food", "['peanut', 'shrimp'].forEach(i => document.querySelector('[data-id=' + i + ']').click()); document.getElementById('mc-food').click(); document.querySelectorAll('#ans-btns .ans')[2].click()"),
                                  ("refused.html#eat/card", "refused", ""), ("saved.html", "trip", ""),
                                  ("", "list", "document.querySelector('#jump [data-go=move]').click()")):
            if name == "trip": b.js(f"localStorage.setItem('emk-trip', JSON.stringify({{from: {day}(-7), to: {day}(0)}}))")
            b.go(srv.url + page)
            if not page:  # keep the install prompt out of the pictures
                b.js("localStorage.setItem('emk-install-no', String(Date.now())); localStorage.setItem('emk-ready', '1')"); b.go(srv.url)
            if name == "ready":  # a finished check with some steps ticked, as a traveler would see it a week before the flight
                b.js("localStorage.setItem('emk-rc', JSON.stringify({p: 'visitor', dev: 'ios', pay: 'card', air: 'icn', city: ['busan'], food: 'no', from: '', to: ''}));"
                     "localStorage.setItem('wik-setup', 'visitor|ios'); localStorage.setItem('wik-plan-en-visitor-ios', '[0,1,2,3,4]'); localStorage.setItem('emk-rc-x', JSON.stringify(['checked', 'pay-card']))")
                b.go(srv.url + page, wait=1.2)
            if after: b.js(after); time.sleep(1.2 if name == "sos" else 0.4)
            b.shot(out(f"shots/{name}.png")); flatten(f"shots/{name}.png")
            if name in ("food", "trip"): b.js("['emk-food', 'emk-trip'].forEach(k => localStorage.removeItem(k))")
            if name == "ready": b.js("['emk-rc', 'emk-rc-x', 'emk-rc-score', 'wik-setup', 'wik-plan-en-visitor-ios', 'emk-saved'].forEach(k => localStorage.removeItem(k))")
        b.cmd("Emulation.setDeviceMetricsOverride", width=1024, height=500, deviceScaleFactor=1, mobile=False)
        b.go(srv.url + "store/feature.html", wait=2.5); b.shot(out("store/feature-graphic.png")); flatten("store/feature-graphic.png")
        # Play listing screenshots: the same screens in a phone frame under a one-line benefit, as top travel apps do.
        b.cmd("Emulation.setDeviceMetricsOverride", width=1080, height=1920, deviceScaleFactor=1, mobile=False)
        os.makedirs(out("store/screenshots"), exist_ok=True)
        for n, (name, t, s) in enumerate(FRAMES, 1):
            b.go(srv.url + "store/frame.html?" + urllib.parse.urlencode({"img": f"../shots/{name}.png", "t": t, "s": s}), wait=2.0)
            rel = f"store/screenshots/{n}-{name}.png"; b.shot(out(rel)); flatten(rel)
    finally:
        b.close(); srv.stop()


def flatten(rel):
    im = Image.open(out(rel)).convert("RGB"); im.save(out(rel), optimize=True)  # 24-bit, no alpha, as Play asks
    print(rel, im.size)


if __name__ == "__main__":
    icons()
    if "--icons-only" not in sys.argv: screenshots()
