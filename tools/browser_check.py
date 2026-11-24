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
import text_density as TD  # noqa: E402

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
  /* A page that failed while eight were loading at once gets a second look on its own. */
  const again = [...new Set([...out.overflow, ...out.noTabs, ...out.noApp.map(s => s.split(' ')[0])])];
  out.overflow = []; out.noTabs = []; out.noApp = [];
  for (const p of again) await one(p);
  return out; })()"""


# Things people tap with a thumb must be at least 44px tall (28차; links inside a sentence are exempt).
TAPS = """(() => {
  const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && !e.closest('[hidden]') && !e.closest('details:not([open]) > :not(summary)'); };
  return [...document.querySelectorAll('.tabbar a, .jump a, .sit-links a, .glist a, .sayrow button, a.call, .act, .icon-btn, .lang-menu > summary, .btn, .chip, .opt-big, .ready-cta, .rd-app > summary, .steps summary, .flow-steps summary, '
      + '.mo, .mo-row, .sos-call, .sos-find, .sos-more summary, .tg, .seg a, .rf-g a, .rf-crumb, .dy-t, .dy-bell, .dg > summary, .mc-more summary, .all-row, .fold > summary, .near-a, .ans, .stamp a, .stamp .linkbtn, .trust-line a, #setup-now .linkbtn, #show-all, .setbar .btn, .foot nav a')]
    .filter(vis).map(e => ({t: (e.innerText || e.getAttribute('aria-label') || e.className).trim().slice(0, 24), h: Math.round(e.getBoundingClientRect().height)})).filter(x => x.h < 44);
})()"""


# Korea Ready check, answered by taps alone: no Korean number, (Android when asked), phone wallet only, Incheon, Busan, a food rule, dates.
READY_RUN = """(() => { const o = () => [...document.querySelectorAll('#rd-opts .opt-big')], n = () => document.getElementById('rd-next'); let taps = 0;
  const tap = e => { e.click(); taps++; };
  tap(o()[0]);
  if (document.getElementById('rd-qh').textContent === JSON.parse(document.getElementById('ready-data').textContent).q2) tap(o()[1]);
  tap(o()[1]); tap(o()[0]); tap(o()[0]); tap(n()); tap(o()[0]);
  document.getElementById('rd-from').value = '2027-02-05'; document.getElementById('rd-to').value = '2027-02-12'; tap(n());
  return taps; })()"""


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
        for page in ("", "taxi.html", "phrases.html", "saved.html", "help.html", "foreign-card-declined-korea.html", "ja/", "vi/phrases.html",
                     "sos.html", "refused.html", "refused.html#taxi", "refused.html#eat/card", "my-card.html", "vi/my-card.html", "vi/sos.html"):
            b.go(srv.url + page, wait=0.5)
            small += [f"/{page} {x['t']} {x['h']}px" for x in b.js(TAPS)]
        check(not small, "buttons and links are at least 44px tall on the main screens", "; ".join(small[:5]))
        check(b.js("document.querySelectorAll('#jump a').length") == 8 if b.go(srv.url, wait=0.5) else False, "home shows all eight situations as a jump grid")

        # 28차: home is one screen (your trip, tiles, All guides); a tile opens that situation's list; Back returns home.
        home0 = b.js("[document.getElementById('tool').hidden, !document.getElementById('jump').hidden, !document.getElementById('all-row').hidden].join()")
        b.js("document.querySelector('#jump [data-go=move]').click()"); time.sleep(0.3)
        lst = b.js("""(() => { const rows = [...document.querySelectorAll('#main li[data-t]')].filter(li => !li.hidden && li.closest('.gcat:not([hidden])'));
          return [location.hash, document.getElementById('jump').hidden, rows.length, rows.every(li => li.closest('.gcat').dataset.cat === 'move'), document.getElementById('tool-h').textContent].join('|'); })()""")
        b.js("history.back()"); time.sleep(0.4)
        back = b.js("[location.hash, document.getElementById('tool').hidden, !document.getElementById('jump').hidden].join()")
        check(home0 == "true,true,true" and lst.startswith("#c=move|true|") and "|true|" in lst and back == ",true,true", "home shows one screen; a tile opens only that situation's guides, and Back returns home", f"{home0} / {lst} / {back}")
        b.js("document.getElementById('all-row').click()"); time.sleep(0.3)
        n_all = b.js("[...document.querySelectorAll('#main li[data-t]')].filter(li => !li.hidden).length")
        check(n_all == 21, "All guides lists every guide once", str(n_all))

        # Ask cards: staff tap a Korean answer on the full-screen card and the reader sees it in their language.
        b.go(srv.url + "phrases.html", wait=0.5)
        ask = b.js("""(() => { document.querySelector('.sayrow.askrow .sayrow-main').click(); const a = [...document.querySelectorAll('#ans-btns .ans')];
          a[1].click(); const o = document.getElementById('ans-out'); return [a.length, !o.hidden, o.textContent, a[1].getAttribute('aria-pressed')].join('|'); })()""")
        b.js("history.back()"); time.sleep(0.3)
        plain = b.js("(() => { document.querySelector('.sayrow:not(.askrow) .sayrow-main').click(); return document.getElementById('show-ans').hidden; })()")
        b.js("history.back()"); time.sleep(0.3)
        check(ask.startswith("3|true|") and "No, it doesn't" in ask and ask.endswith("|true") and plain, "an ask card shows three Korean answers; a tap shows that answer in English; plain cards show none", ask)

        # Korean cards fold to one row per group with a count; one opens at a time; search opens only groups with a match (29차).
        cf = b.js("""(() => { const f = [...document.querySelectorAll('#cards > details.fold')].filter(x => !x.hidden), vh = innerHeight;
          f[0].open = true; f[1].open = true; const one = f.filter(x => x.open).length; f.forEach(x => x.open = false);
          const fit = f[f.length - 1].getBoundingClientRect().bottom <= vh;
          const ph = document.getElementById('f-pharm'), pa = ph.querySelectorAll('.askrow').length, pn = ph.querySelectorAll('.sayrow').length;
          const q = document.getElementById('cq'); q.value = 'pork'; q.dispatchEvent(new Event('input'));
          const shown = [...document.querySelectorAll('#cards > details.fold')].filter(x => !x.hidden && x.open).map(x => x.id).join(',');
          q.value = ''; q.dispatchEvent(new Event('input'));
          const back = [...document.querySelectorAll('#cards > details.fold')].filter(x => !x.hidden && !x.open).length;
          return [f.length, one, fit, document.querySelector('#fs-pharm .sr').textContent, pa, pn, shown, back === f.length].join('|'); })()""")
        check(cf.startswith("7|1|true|18 cards|4|18|") and "f-ask" in cf and "f-food" in cf and "f-pharm" not in cf.split("|")[6] and cf.endswith("|true"),
              "Korean cards show seven group rows on one screen with counts, one open at a time; search opens only groups with a match", cf)
        b.go(srv.url + "phrases.html#f-pharm", wait=0.5)
        ph = b.js("[document.getElementById('f-pharm').open, document.querySelectorAll('#cards > details.fold[open]').length].join()")
        b.go(srv.url + "help.html", wait=0.5)
        hl = b.js("!!document.querySelector('.near a[href=\"phrases.html#f-pharm\"]')")
        check(ph == "true,1" and hl, "Help links to the pharmacist cards, and the link opens that group", f"{ph} / {hl}")

        # 30차. SOS: the location is read only on a tap, turned into the rescue grid code on the phone, and put into the Korean text.
        org = srv.url.rstrip("/")
        b.cmd("Browser.grantPermissions", origin=org, permissions=["geolocation"])
        b.cmd("Emulation.setGeolocationOverride", latitude=35.33697, longitude=127.73053, accuracy=8)
        b.go(srv.url + "sos.html", wait=0.6)
        b.js("window.__geo = 0; const w0 = navigator.geolocation.watchPosition.bind(navigator.geolocation); navigator.geolocation.watchPosition = (...a) => { window.__geo++; return w0(...a); }")
        grid = b.js("[[37.57097, 126.97694], [35.33697, 127.73053], [35.1152, 129.0414], [37.23917, 131.86972], [33.59, 130.4], [34.2, 129.3], [40, 127], [35.68, 139.76]].map(p => emkGrid(...p) || '-').join('|')")
        idle = b.js("window.__geo + '|' + document.getElementById('sos-out').hidden")
        b.js("document.querySelector('#sos-what .tg[data-id=lost]').click(); document.getElementById('sos-find').click()"); time.sleep(1.2)
        sos = b.js("""(() => { const t = decodeURIComponent(document.getElementById('sos-text').href); document.getElementById('sos-show').click();
          const k = document.getElementById('show-ko').innerText.replace(/\u00a0/g, ' '); return [window.__geo, document.getElementById('sos-code').textContent.replace(/\u00a0/g, ' '), t.startsWith('sms:119'), t.includes('국가지점번호 라마 2094 0462 (35.33697, 127.73053, 오차 약 8m)') && t.includes('길을 잃었어요') && t.includes('영어로 답해'),
          k.includes('라마 2094 0462입니다') && k.includes('영어 통역'), SAY.includes('라마, 이공구사, 공사육이'), document.getElementById('sos-rom').textContent.includes('ra-ma, i-gong-gu-sa, gong-sa-yuk-i')].join('|'); })()""")
        b.js("history.back()"); time.sleep(0.3)
        police = b.js("(() => { document.querySelector('#sos-what .tg[data-id=theft]').click(); return document.getElementById('sos-text').href.startsWith('sms:112') && document.querySelector('.sos-call.pol').classList.contains('on'); })()")
        b.cmd("Emulation.setGeolocationOverride", latitude=37.57097, longitude=126.97694, accuracy=900)
        b.js("document.getElementById('sos-again').click()"); time.sleep(1.0)
        rough = b.js("!document.getElementById('sos-rough').hidden && document.getElementById('sos-rom').textContent.includes('900미터')")
        b.cmd("Emulation.setGeolocationOverride", latitude=35.68, longitude=139.76, accuracy=10)
        b.go(srv.url + "ja/sos.html", wait=0.6); b.js("document.getElementById('sos-find').click()"); time.sleep(1.0)
        out = b.js("document.getElementById('sos-out').hidden && !document.getElementById('sos-msg').hidden && document.getElementById('sos-msg').textContent.includes('韓国の外')")
        check(grid == "다사 5381 5252|라마 2094 0462|마라 4046 8109|사사 8768 2454|-|-|-|-" and idle == "0|true", "SOS works out the rescue grid code for known points, none outside Korea, and reads no location before a tap", grid + " " + idle)
        check(sos == "1|라마 2094 0462|true|true|true|true|true" and police and rough and out, "SOS puts the code, the situation and the language into the Korean text, the full-screen card and the reading; a wide fix says so; outside Korea it says so", f"{sos} {police} {rough} {out}")
        b.cmd("Browser.resetPermissions")

        # Food card: taps make one Korean card; staff answers come back in the reader's language; nothing leaves the phone.
        b.js("localStorage.removeItem('emk-food')")
        b.go(srv.url + "my-card.html", wait=0.5)
        empty = b.js("document.getElementById('mc-food').disabled")
        fc = b.js("""(() => { ['peanut', 'fish', 'vegan', 'a_alc'].forEach(i => document.querySelector('[data-id=' + i + ']').click()); document.getElementById('mc-sev').click(); document.getElementById('mc-food').click();
          const k = document.getElementById('show-ko').innerText; const a = [...document.querySelectorAll('#ans-btns .ans')]; a[1].click();
          return [k.includes('땅콩, 생선') && k.includes('조금만 들어가도 위험해요') && k.includes('비건') && k.includes('술') && k.includes('육수'), a.length, document.getElementById('ans-out').textContent.includes("It's in it"),
            document.getElementById('mc-words').textContent.includes('땅콩'), document.getElementById('mc-off').textContent.includes('Fish') && document.getElementById('mc-off').textContent.includes('mackerel'), localStorage.getItem('emk-food')].join('|'); })()""")
        b.js("history.back()"); time.sleep(0.3)
        b.go(srv.url + "ja/my-card.html", wait=0.5)
        mc = b.js("""(() => { document.getElementById('mc-food').click(); const k = document.getElementById('show-ko').innerText;
          return [k.includes('땅콩, 생선'), document.getElementById('show-mean').textContent.includes('ピーナッツ'), document.querySelectorAll('#ans-btns .ans').length].join('|'); })()""")
        b.js("history.back()"); time.sleep(0.3)
        b.go(srv.url + "phrases.html", wait=0.5)
        st = b.js("[...document.querySelectorAll('.mc-st')].map(s => s.textContent).join() + '|' + document.querySelector('#fs-own [aria-hidden]').textContent")
        b.js("localStorage.removeItem('emk-food')")
        check(empty and fc == 'true|5|true|true|true|{"a":["peanut","fish"],"n":["vegan","a_alc"],"s":1}' and mc == "true|true|5" and st == "✓ Saved|1",
              "taps make a Korean food card with staff answers and label words; it opens ready in another language and the cards tab shows it as saved", f"{empty} {fc} / {mc} / {st}")

        # Refused? place, problem, one answer with Korean cards, the reader's own status and a date; Back walks the steps.
        b.js("localStorage.setItem('wik-setup', 'arc|android')")
        b.go(srv.url + "refused.html", wait=0.5)
        rf0 = b.js("document.querySelectorAll('.rf-g a').length + '|' + [...document.querySelectorAll('.rf-g a')].every(a => a.getBoundingClientRect().bottom < innerHeight - 60)")
        b.js("document.querySelector('.rf-g a[href=\"#app\"]').click()"); time.sleep(0.3)
        rf1 = b.js("[...document.querySelectorAll('.rf-step')].filter(s => !s.hidden).map(s => s.querySelectorAll('.rf-list a').length).join()")
        b.js("document.querySelector('.rf-step:not([hidden]) .rf-list a[href=\"#app/id\"]').click()"); time.sleep(0.3)
        rf2 = b.js("""(() => { const a = [...document.querySelectorAll('.rf-ans')].filter(s => !s.hidden); return [a.length, a[0].dataset.a, a[0].querySelectorAll('.sayrow').length, a[0].querySelector('.pill').className, a[0].querySelector('.rf-who').textContent, !!a[0].querySelector('time.ck[datetime]')].join('|'); })()""")
        b.js("history.back()"); time.sleep(0.3); b.js("history.back()"); time.sleep(0.3)
        rf3 = b.js("!document.getElementById('rf-1').hidden")
        bad = b.js("""(() => { const D = JSON.parse(document.getElementById('rf-data').textContent), out = []; for (const p in D.q) for (const a of D.q[p]) { const s = document.querySelector('.rf-ans[data-a="' + p + '/' + a + '"]');
          if (!s || !s.querySelector('.rf-now p:last-child').textContent || !s.querySelector('.rf-fail p:last-child').textContent || !(s.querySelector('.sayrow') || s.querySelector('#myaddr')) || !(s.querySelector('time.ck') || s.querySelector('.hint'))) out.push(p + '/' + a); } return out.join(); })()""")
        b.js("localStorage.removeItem('wik-setup')")
        check(rf0 == "8|true" and rf1 == "4" and rf2 == "1|app/id|1|pill ok|Resident (ARC) · Android|true" and rf3 and not bad, "Refused? gives one dated answer with Korean to show in two taps, for the reader's setup, and Back walks the steps", f"{rf0} {rf1} {rf2} {rf3} {bad}")

        # Trip mode: home shows only what is due; My trip opens the current stage; a reminder is a valid calendar file made on the phone.
        trip = lambda a, z: f"(() => {{ const p = n => {{ const t = new Date(Date.now() + n * 864e5); return t.getFullYear() + '-' + String(t.getMonth() + 1).padStart(2, '0') + '-' + String(t.getDate()).padStart(2, '0'); }}; localStorage.setItem('emk-trip', JSON.stringify({{from: p({a}), to: p({z})}})); }})()"
        see = "[(document.querySelector('#trip-now .tn-h b') || {}).textContent, document.querySelectorAll('#trip-now .tn li').length, document.querySelector('#today .ready-cta').hidden, document.getElementById('trip-now').hidden].join('|')"
        got = []
        for a, z in ((3, 10), (0, 7), (-3, 4), (-6, 1), (-7, 0), (-12, -5)):
            b.js(trip(a, z)); b.go(srv.url, wait=0.4); got.append(b.js(see))
        check(got[0] == "3 days to go|2|false|false" and got[1] == "Day 1 of 8|2|true|false" and got[2] == "Day 4 of 8|1|true|false" and got[3] == "Day 7 of 8|2|true|false" and got[4] == "You leave today|2|true|false" and got[5].endswith("|false|true"),
              "trip mode: home shows the countdown, the day, and only what is due; after the trip it steps aside", " / ".join(map(str, got)))
        b.js(trip(-6, 1)); b.go(srv.url + "saved.html", wait=0.5)
        dg = b.js("""(() => { const o = [...document.querySelectorAll('.dg[open]')], li = o[0].querySelector('li'); li.querySelector('.dy-t').click();
          const f = emkIcs('x', 'a, b; c', Date.UTC(2027, 0, 5), '19'), BS = String.fromCharCode(92), NL = String.fromCharCode(13, 10); return [o.length, document.querySelector('.dg') === o[0], li.className, localStorage.getItem('emk-days'),
            f.startsWith('BEGIN:VCALENDAR' + NL + 'VERSION:2.0') && f.includes('DTSTART:20270105T190000') && f.includes('SUMMARY:a' + BS + ', b' + BS + '; c') && f.includes('BEGIN:VALARM') && f.endsWith('END:VCALENDAR' + NL) && f.split(NL).every(l => new TextEncoder().encode(l).length <= 75)].join('|'); })()""")
        b.js("['emk-trip', 'emk-days'].forEach(k => localStorage.removeItem(k)); localStorage.setItem('wik-setup', 'arc|android'); localStorage.setItem('emk-moved', '2030-03-01')")
        b.go(srv.url + "saved.html", wait=0.5)
        arc = b.js("[document.querySelectorAll('.dg').length, (document.querySelector('.dy-by') || {}).textContent].join('|')")
        b.js("['wik-setup', 'emk-moved'].forEach(k => localStorage.removeItem(k))")
        check(dg == '1|true|off|["eve_bag"]|true' and arc == "1|Report by Mar 15 · F-4: Mar 14", "My trip opens the current stage, remembers ticks, and makes a valid calendar reminder; residents get the address-report date", f"{dg} / {arc}")

        # Find nearby: six Korean search words that open Naver Map.
        b.go(srv.url + "help.html", wait=0.5)
        near = b.js("[...document.querySelectorAll('.near-a')].map(a => decodeURIComponent(a.href)).join(' ')")
        check(near.count("map.naver.com/p/search/") == 6 and "약국" in near and "응급실" in near, "Help finds a pharmacy, ER and four more nearby in Naver Map with the Korean word", near[:120])

        # My trip: tools fold to rows that show their state; one opens at a time.
        b.js("localStorage.setItem('emk-addr', 'FOLD TEST 1'); localStorage.setItem('emk-places', JSON.stringify(['A', 'B']))")
        b.go(srv.url + "saved.html", wait=0.5)
        fl = b.js("""(() => { const f = [...document.querySelectorAll('#folds > details.fold')], st = id => document.getElementById('fs-' + id).textContent;
          f[0].open = true; f[1].open = true; return [f.length, f.filter(x => x.open).length, st('addr'), st('places')].join('|'); })()""")
        b.js("localStorage.removeItem('emk-addr'); localStorage.removeItem('emk-places')")
        check(fl == "7|1|FOLD TEST 1|2 saved", "My trip folds its tools to seven rows with their state, one open at a time", fl)
        b.go(srv.url + "taxi.html", wait=0.5)
        check(b.js("[...document.querySelectorAll('.guide-acts .act')].every(x => { const c = getComputedStyle(x); return c.backgroundColor !== c.color; })"), "save and share buttons on a guide are visible (icon colour differs from the button)")

        # Standing rule (docs/critique.md 26차): short lines, details behind a tap. Words a reader sees on a 375px phone.
        b.js(TD.READY); over = []
        for page, name, kind in TD.PAGES:
            b.go(srv.url + page, wait=0.5); r = b.js(TD.JS); lim = TD.LIMITS[kind]
            if r["first"] > lim["first"] or r["sentences"] > lim["sentences"] or r["all"] > lim["all"]: over.append(f"{name} {r['first']}/{r['sentences']}/{r['all']}")
        b.js("localStorage.removeItem('emk-rc'); localStorage.removeItem('emk-rc-score')")
        check(not over, "main screens stay short: words on the first screen, long lines and whole page within the limits", "; ".join(over))

        b.go(srv.url + "taxi.html", wait=0.5)
        b.js("document.querySelector('[data-show]').click()")
        opened = b.js("!document.getElementById('show').hidden")
        b.js("history.back()"); time.sleep(0.5)
        check(opened and b.js("document.getElementById('show').hidden && location.pathname === '/taxi.html'"), "the Back button closes a full-screen card and stays on the guide")

        # Setup choice on a guide: one tap switches the answer and is remembered.
        b.js("localStorage.removeItem('wik-setup')"); b.go(srv.url + "taxi.html", wait=0.5)
        before = b.js("[...document.querySelectorAll('.answer .pv')].filter(x => !x.hidden).length")
        b.js("document.getElementById('setup-change').click(); document.querySelector('#setup [data-p=arc]').click()")
        check(before == 1 and b.js("localStorage.getItem('wik-setup') === 'arc|ios' && document.querySelector('.answer .pv:not([hidden])').dataset.p === 'arc'"), "a guide lets the reader pick a setup in one tap and remembers it")
        b.js("localStorage.removeItem('wik-setup')")

        # Places to go: a Google Maps link gives up its place name; each place opens in Naver Map and KakaoMap.
        b.go(srv.url + "saved.html", wait=0.5)
        add = "(v => { document.getElementById('pl-in').value = v; document.getElementById('pl-form').requestSubmit(); return (document.querySelector('#pl-list b') || {}).textContent || ''; })"
        name = b.js(add + "('https://www.google.com/maps/place/Gyeongbokgung+Palace/@37.57,126.97,17z')")
        links = b.js("[...document.querySelectorAll('#pl-list li:first-child a')].map(a => a.href).join(' ')")
        check(name == "Gyeongbokgung Palace" and "map.naver.com/p/search/Gyeongbokgung" in links and "map.kakao.com/link/search/Gyeongbokgung" in links, "places list reads a Google Maps link and opens the place in Naver Map and KakaoMap", name)
        b.js("document.querySelector('#pl-list .pl-name').click()")
        check(b.js("!document.getElementById('show').hidden && document.getElementById('show-ko').textContent.includes('Gyeongbokgung')"), "a saved place shows full screen for a driver in one tap")
        b.js("history.back(); localStorage.removeItem('emk-places'); localStorage.setItem('emk-addr', 'TEST ADDRESS 110')"); time.sleep(0.3)
        b.go(srv.url, wait=0.5)
        check(b.js("!!document.querySelector('.quick-driver') && document.querySelector('.quick-driver b').textContent === 'TEST ADDRESS 110'"), "with a stay address saved, the home screen offers the driver card in one tap")
        b.js("localStorage.removeItem('emk-addr')")

        # Holiday alerts follow the trip dates: Seollal 2027 shows for a trip over 6 to 9 Feb, and nothing shows for a June trip.
        b.js("localStorage.setItem('emk-trip', JSON.stringify({from: '2027-02-04', to: '2027-02-10'}))"); b.go(srv.url, wait=0.5)
        inside = b.js("!document.getElementById('alerts-wrap').hidden && document.querySelectorAll('#alerts .alert').length === 1")
        b.js("localStorage.setItem('emk-trip', JSON.stringify({from: '2027-06-01', to: '2027-06-10'}))"); b.go(srv.url, wait=0.5)
        check(inside and b.js("document.getElementById('alerts-wrap').hidden"), "holiday alerts show only for holidays inside the trip dates")
        b.js("localStorage.removeItem('emk-trip')")

        # Offline pack: My trip reports every file for this language as saved.
        b.go(srv.url + "saved.html", wait=0.5); state = ""
        for _ in range(30):
            state = b.js("document.getElementById('pk-bar').style.width")
            if state == "100%": break
            time.sleep(0.4)
        check(state == "100%" and b.js("document.getElementById('pk-state').classList.contains('ok')"), "offline pack reports the whole language pack as saved", state)

        # Sharing: the list travels in the link; the other phone asks first and adds it only on a tap.
        b.js("localStorage.setItem('emk-addr', 'STAY 110'); localStorage.setItem('emk-places', JSON.stringify(['PLACE A', 'PLACE B']))")
        b.go(srv.url + "saved.html", wait=0.5); b.js("document.getElementById('share-make').click()")
        link = b.js("document.getElementById('share-out').dataset.link || ''")
        qr = b.js("!!document.querySelector('#share-qr svg')")
        b.js("localStorage.removeItem('emk-addr'); localStorage.removeItem('emk-places')")   # now it is the companion's phone
        b.go(link, wait=0.6)
        asked = b.js("!document.getElementById('import').hidden && !localStorage.getItem('emk-places')")
        b.js("document.getElementById('import-yes').click()"); time.sleep(1.0)
        got = b.js("[localStorage.getItem('emk-addr'), localStorage.getItem('emk-places'), location.hash].join('|')")
        check("#t=" in link and qr and asked and got == 'STAY 110|["PLACE A","PLACE B"]|', "a shared link or QR copies the stay address and places to another phone after asking", got)
        b.js("localStorage.removeItem('emk-addr'); localStorage.removeItem('emk-places')")

        # e-Arrival Card helper: landing 10 Jan 2030 12:00 Korea time means the window opens 7 Jan 12:00; landing in 30 hours means it is open now.
        b.go(srv.url + "k-eta-entry-requirements.html", wait=0.5)
        setv = "(v => { const i = document.getElementById('ar-in'); i.value = v; i.dispatchEvent(new Event('input')); return document.querySelector('.ar-main').textContent + '|' + document.querySelector('.ar-state').className; })"
        far = b.js(setv + "('2030-01-10T12:00')")
        soon = b.js(setv + "(new Date(Date.now() + 39 * 3600e3).toISOString().slice(0, 16))")
        check("Jan 7" in far and "12:00" in far and far.endswith("wait") and soon.endswith("open"), "arrival helper works out the 72-hour window in Korea time", far)
        b.js("localStorage.removeItem('emk-landing')")

        # Korea Ready check: taps only; the plan, the score, My trip and the home screen follow the answers.
        b.js("['wik-setup', 'emk-rc', 'emk-rc-x', 'emk-rc-score', 'emk-trip', 'emk-saved'].forEach(k => localStorage.removeItem(k))")
        b.go(srv.url + "ready.html", wait=0.5)
        first = b.js("!document.getElementById('rd-q').hidden && document.querySelectorAll('#rd-opts .opt-big').length === 3 && document.getElementById('rd-result').hidden")
        small = [f"{x['t']} {x['h']}px" for x in b.js(TAPS)]
        taps = b.js(READY_RUN)
        res = b.js("""(() => { const D = JSON.parse(document.getElementById('ready-data').textContent), m = /(\\d+)\\/(\\d+)/.exec(document.getElementById('rd-score').textContent) || [0, -1, -1];
          return { shown: !document.getElementById('rd-result').hidden, d: +m[1], n: +m[2], apps: document.querySelectorAll('#rd-apps details').length,
            dated: [...document.querySelectorAll('#rd-apps details')].every(x => x.querySelector('time.ck[datetime]')), nc: document.querySelectorAll('#rd-apps .rd-nc').length,
            wallet: !!document.querySelector('#rd-steps label[for="rd-x-pay-wallet"] a[href*="koreajoongangdaily"]'), later: document.querySelectorAll('#rd-later input').length,
            setup: localStorage.getItem('wik-setup'), trip: localStorage.getItem('emk-trip'), busan: (localStorage.getItem('emk-saved') || '').includes(D.guides.busan[0]),
            card: document.getElementById('rd-card').toDataURL().length }; })()""")
        small += [f"result {x['t']} {x['h']}px" for x in b.js(TAPS)]
        check(first and taps <= 9 and res["shown"] and res["d"] == 1 and res["n"] >= 9 and res["apps"] >= 5 and res["dated"] and res["nc"] >= 1 and res["wallet"] and res["later"] >= 3,
              "Korea Ready check: taps only give a dated plan for this phone setup, with the open question marked 'needs check'", json.dumps(res))
        check(str(res["setup"]).startswith("visitor|") and "2027-02-05" in str(res["trip"]) and res["busan"] and res["card"] > 5000 and not small,
              "Korea Ready check fills My trip (setup, dates, guides), draws the share card, and its buttons are thumb-sized", json.dumps(res) + " " + "; ".join(small[:4]))
        b.js("document.querySelector('#rd-steps input:not(:checked):not(:disabled)').click()")
        b.go(srv.url, wait=0.5)
        home = b.js("(() => { const a = document.querySelector('.ready-cta.done .ready-sub'); return (a ? a.textContent : '') + '|' + !document.getElementById('alerts-wrap').hidden; })()")
        b.go(srv.url + "ja/ready.html", wait=0.5)
        ja = b.js("document.getElementById('rd-score').textContent + '|' + document.querySelectorAll('#rd-apps details').length + '|' + !document.getElementById('rd-result').hidden")
        b.js("document.getElementById('rd-redo').click()")
        again = b.js("!document.getElementById('rd-q').hidden && document.getElementById('rd-result').hidden")
        check(f"2/{res['n']}" in home and home.endswith("|true") and f"/{res['n']}|" in ja and ja.endswith("|true") and again,   # ticks are kept per language, the answers are shared
              "after the check, the home screen shows the plan's progress and the holiday inside the trip; the result reopens in other languages and answers can be changed", home + " " + ja)
        b.js("localStorage.removeItem('emk-trip'); localStorage.removeItem('emk-saved'); localStorage.removeItem('wik-setup')")

        b.cmd("Network.enable"); b.cmd("Network.emulateNetworkConditions", offline=True, latency=0, downloadThroughput=-1, uploadThroughput=-1); time.sleep(0.5)
        strip = b.js("(() => { const s = document.querySelector('.net-strip'); return !!s && !s.hidden && s.textContent.length > 5; })()")
        b.cmd("Network.emulateNetworkConditions", offline=False, latency=0, downloadThroughput=-1, uploadThroughput=-1); time.sleep(0.5)
        check(strip and b.js("document.querySelector('.net-strip').hidden"), "an offline strip shows while there is no connection and goes away after")

        r = b.js(SWEEP % json.dumps(pages))
        check(not r["overflow"], f"{len(pages)} pages fit a 375px screen", ", ".join(r["overflow"][:5]))
        check(not r["noTabs"], "every page has the four bottom tabs", ", ".join(r["noTabs"][:5]))
        check(not r["noApp"], "every page loads the shared app script", ", ".join(r["noApp"][:5]))

        # The sweep opened pages in five languages, so the worker may still be switching language packs: let it finish first.
        # A reader uses one language at a time: open the English home and wait until its worker is the active one and nothing is queued.
        b.go(srv.url, wait=0.5)
        for _ in range(75):
            if b.js("navigator.serviceWorker.getRegistration().then(r => !!r && !!r.active && /l=en$/.test(r.active.scriptURL) && !r.installing && !r.waiting)"): break
            time.sleep(0.2)
        time.sleep(1.0)
        srv.stop()  # from here on there is no server: only the copy on the "phone" can answer
        for page in ("", "taxi.html", "phrases.html", "saved.html", "help.html", "privacy.html", "lost-phone-wallet-passport.html", "foreign-card-declined-korea.html", "ready.html", "sos.html", "refused.html", "my-card.html"):
            ok = b.go(srv.url + page, wait=0.6) and b.js("document.querySelectorAll('.tabbar a').length === 4 && document.title.includes('EasyModeKorea')")
            why = b.last_error or (b.js("location.href + ' | ' + document.title + ' | tabs ' + document.querySelectorAll('.tabbar a').length") if not ok else "")
            check(bool(ok), f"offline: /{page} opens", why)
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
