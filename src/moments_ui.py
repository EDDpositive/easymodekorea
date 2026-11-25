"""Screens for moments.py (30차): emergency, food card, "Refused? 3 taps", and the trip-mode block.

Every builder takes B, the build module, for the shared helpers (app_page, say_row, icon and so on).
Nothing here sends anything: location, allergies and dates are read and kept on the phone.
"""
import json

import app_shell as A
import moments as M
import trouble as TR
from data import LANGS, TASK_META
from data_extra import SHORT, UX
from layout import AT
from moments_js import DAYS_JS, MYCARD_JS, REFUSED_JS, SOS_JS  # noqa: F401  (DAYS_JS is used by build.py)

SLUG = {tid: sl for tid, sl, _ in TASK_META}
js_json = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def guide_date(tid):
    """The oldest check date among a guide's dated facts: the safe date to print next to a one-line summary of it."""
    return min(r[2] for r in AT[tid])


def source_links(B, lang, keys):
    """Links for moments.SRC and trouble.SRC keys and for this site's own guides."""
    out = []
    for k in keys:
        if k.startswith("guide:"): out.append(f'<a href="{SLUG[k[6:]]}.html">{B.e(SHORT[lang]["tasks"][k[6:]])}</a>')
        else:
            n, u = M.SRC[k] if k in M.SRC else TR.SRC[k]
            out.append(f'<a href="{B.e(u)}" rel="noopener" target="_blank">{B.e(n)}</a>')
    return ", ".join(out)


def checked(B, lang, d):
    return f'<time class="ck" datetime="{d}">✓ {B.e(B.fmt_date(d, lang))}</time>'


def build_sos(B, lang):
    """Emergency: call, find the rescue grid code on the phone, show or read it in Korean, or text it."""
    t = {k: v[lang] for k, v in M.SOS.items() if isinstance(v, dict)}; e = B.e
    itp = M.SOS_ITP[lang]
    data = {"lang": lang, "lko": M.SOS_LANG_KO[lang], "t": {k: t[k] for k in ("acc", "where", "finding", "denied", "none", "out", "slow", "show", "text", "stay")},
            "err": M.SOS_ERR, "help": M.SOS_HELP, "helpm": M.SOS_HELP_M[lang], "loc": M.SOS_LOC, "itp": itp[:3], "itpm": itp[3],
            "what": [[w[0], w[1], w[2][lang], w[3], w[4], w[5]] for w in M.SOS_WHAT]}
    call = lambda n, cls: f'<a class="sos-call {cls}" href="tel:{n}" data-n="{n}" aria-label="{e(A.T[lang]["call"])} {n}: {e(t["n" + n])}"><i aria-hidden="true">{A.IC["phone"]}</i><b>{n}</b><span>{e(t["n" + n])}</span></a>'
    near = "".join(f"<li>{e(x[lang])}</li>" for x in M.SOS["near_li"])
    inner = f"""<div id="sos">
<div class="sos-calls">{call("119", "fire")}{call("112", "pol")}</div>
<a class="call sos-1330" href="tel:+82-2-1330" aria-label="{e(A.T[lang]['call'])} 1330: {e(t['n1330'])}"><b>1330</b><span>{e(t['n1330'])}</span><i aria-hidden="true">{A.IC['phone']}</i></a>
<section class="sos-loc" aria-label="{e(t['where'])}">
<button class="sos-find" id="sos-find" type="button"><span class="ic">{A.IC['pin']}</span><span><b id="sos-find-l">{e(t['where'])}</b><small>{e(t['where_sub'])}</small></span></button>
<div id="sos-out" class="sos-out" hidden><p class="sos-lbl">{e(t['code_h'])}</p><p class="sos-code" id="sos-code" lang="ko" aria-live="polite"></p><p class="sos-acc" id="sos-acc"></p><p class="sos-rough" id="sos-rough" hidden>{e(t['rough'])}</p><p class="sos-again"><button class="linkbtn" type="button" id="sos-again">{e(t['again'])}</button><span>{e(t['said'])}</span></p></div>
<div id="sos-stay-on" class="sos-out" hidden><p class="sos-lbl">{e(t['stay'])}</p><p class="sos-addr" id="sos-stay-a" lang="ko"></p><button class="linkbtn" type="button" id="sos-stay-off">{e(t['where'])}</button></div>
<button class="linkbtn sos-stay" id="sos-stay" type="button" hidden>{e(t['stay'])}</button>
<p class="sos-msg" id="sos-msg" role="status" hidden></p></section>
<section aria-labelledby="sw-h"><h2 id="sw-h" class="mc-h">{e(t['what'])}</h2><div class="tgs three" id="sos-what"></div>
<div class="sos-acts"><button class="btn alt" type="button" id="sos-show">🗣 {e(t['show'])}</button><a class="btn ghost" id="sos-text" href="sms:119">{A.IC['sms']}<span id="sos-text-l">{e(t['text'].replace('{n}', '119'))}</span></a></div></section>
<section class="sos-more"><details class="tap" id="sos-read"><summary>{e(t['read'])}</summary><ul class="sos-rom" id="sos-rom"></ul></details>
<details class="tap" id="sos-near"><summary>{e(t['near'])}</summary><ul class="sos-near">{near}</ul><p class="fact-src">{checked(B, lang, M.CHK)} {source_links(B, lang, ['gg'])}</p></details>
<details class="tap"><summary>{e(t['cant'])}</summary><p>{e(t['cant_t'])}</p><p>{e(t['text_sub'])}</p><p>{e(t['cant_sim'])}</p><p><a href="https://www.119.go.kr/" rel="noopener" target="_blank">{e(t['web'])}</a></p><p class="fact-src">{checked(B, lang, M.CHK)} {source_links(B, lang, ['sms119', 'sms112'])}</p></details>
<details class="tap"><summary>{e(t['code_what'])}</summary><p>{e(t['what_is'])}</p><p class="fact-src">{checked(B, lang, M.CHK)} {source_links(B, lang, ['grid', 'gg'])}</p></details></section>
<ul class="glist"><li><a href="help.html"><span class="ic">{A.IC['help']}</span><span>{e(A.T[lang]['help_title'])}</span></a></li></ul>
</div><script type="application/json" id="sos-data">{js_json(data)}</script>"""
    L = LANGS[lang]; path = L["dir"] + "sos.html"
    ld = {"@context": "https://schema.org", "@type": "WebPage", "@id": B.SITE + path, "url": B.SITE + path, "name": t["title"], "description": t["desc"], "inLanguage": L["html_lang"], "lastReviewed": M.CHK}
    return B.app_page(lang, "sos", (t["title"], t["lede"]), t["seo"], t["desc"], inner, "help", SOS_JS, ld=ld, back_to="help.html")


def build_mycard(B, lang):
    """Food card: tap once, show one big Korean card; staff tap a Korean answer."""
    t = {k: v[lang] for k, v in M.CARD.items()}; e = B.e
    data = {"t": {k: t[k] for k in ("al_h", "no_h", "sev", "label_no", "label_fish")}, "lbl": SHORT[lang]["show"],
            "al": [[a[0], a[1], a[2], a[3][lang]] for a in M.ALLERGY], "no": [[a[0], a[1], a[2][lang], a[3]] for a in M.AVOID],
            "fko": M.FOOD_KO, "fans": [[ko, m[lang]] for ko, m in M.FOOD_ANS]}
    tg = lambda key, rows: "".join(f'<button type="button" class="tg" data-set="{key}" data-id="{i}" aria-pressed="false">{e(n)}</button>' for i, n in rows)
    first = tg("a", [(a[0], a[3][lang]) for a in M.ALLERGY if a[4]]); more = tg("a", [(a[0], a[3][lang]) for a in M.ALLERGY if not a[4]])
    inner = f"""<div class="mc-top"><p class="mc-prev" id="mc-food-p" lang="ko" hidden></p><p class="mc-empty" id="mc-food-e">{e(t['empty'])}</p><button class="btn alt" type="button" id="mc-food" disabled>🗣 {e(t['food_btn'])}</button></div>
<section class="mc-sec" aria-labelledby="ma1"><h2 id="ma1" class="mc-h">{e(t['al_h'])}</h2><div class="tgs">{first}</div><button type="button" class="tg sev" id="mc-sev" aria-pressed="false" hidden>⚠ {e(t['sev'])}</button><details class="mc-more"><summary>{e(t['more'])}</summary><div class="tgs">{more}</div></details></section>
<section class="mc-label" id="mc-label" aria-labelledby="ml-h" hidden><h2 id="ml-h" class="mc-h">{e(t['label_h'])}</h2><ul class="mc-words" id="mc-words"></ul><div class="mc-off" id="mc-off"></div><p class="mc-off" id="mc-nuts" hidden>{e(t['label_nuts'])}</p><p class="mc-off" id="mc-new" hidden>{e(t['label_new'])}</p><p class="fact-src">{checked(B, lang, M.CHK)} {source_links(B, lang, ['label', 'label28'])}</p></section>
<section class="mc-sec" aria-labelledby="ma2"><h2 id="ma2" class="mc-h">{e(t['no_h'])}</h2><div class="tgs">{tg("n", [(a[0], a[2][lang]) for a in M.AVOID])}</div></section>
<p class="mc-foot"><span>{e(t['note'])}</span><button type="button" class="linkbtn" data-clear>{e(t['clear'])}</button></p>
{B.LU.ready_links(B, lang)}
<script type="application/json" id="mc-data">{js_json(data)}</script>"""
    return B.app_page(lang, "my-card", (t["title"], t["lede"]), t["seo"], t["desc"], inner, "cards", MYCARD_JS, back_to="phrases.html")


def build_refused(B, lang):
    """Where, what, then one thing to do now, with the Korean to show and the reader's own dated status."""
    t = {k: v[lang] for k, v in M.RF.items()}; e = B.e; L = LANGS[lang]; U = L["ui"]; ux = UX[lang]
    by = {x["id"]: x for x in B.task_list(lang)}
    ic = {"eat": "food-booking", "taxi": "taxi", "ride": "transit", "train": "ktx", "shop": "shopping", "atm": "cash"}
    glyph = {"app": A.IC["phone"], "web": A.IC["globe"]}
    q, st, tiles, steps, answers, faq = {}, {}, [], [], [], []
    for pid, _tid, name, probs in M.REFUSED:
        q[pid] = [p[0] for p in probs]
        href = f"#{pid}/{probs[0][0]}" if len(probs) == 1 else f"#{pid}"
        tiles.append(f'<a href="{href}"><span class="ic">{glyph.get(pid) or B.icon(ic[pid])}</span><span>{e(name[lang])}</span></a>')
        if len(probs) > 1:
            rows = "".join(f'<li><a href="#{pid}/{p[0]}"><span>{e(p[1][lang])}</span></a></li>' for p in probs)
            steps.append(f'<section class="rf-step" data-p="{pid}" hidden><a class="rf-crumb" href="#">{A.IC["back"]}{e(name[lang])}</a><h2 tabindex="-1">{e(t["q2"])}</h2><ul class="glist rf-list">{rows}</ul></section>')
        for aid, label, now, fail, cards, back in probs:
            tid = back if back and not back.startswith("flow:") else None
            flow = next((f for f in TR.FLOWS if back == "flow:" + f["id"]), None)
            says = "".join(B.addr_card(lang) if c == "ADDR" else B.say_row(lang, c[0], c[1][lang]) for c in cards)
            if tid:
                st.setdefault(tid, {f"{p}|{d}": [B.resolve(by[tid], p, d)[k] for k in ("s", "verdict")] for p in ("visitor", "krsim", "arc") for d in ("ios", "android")})
                mine = (f'<div class="rf-mine" data-tid="{tid}" hidden><p class="rf-lbl">{e(t["mine"])} <small class="rf-who"></small></p><p class="rf-st"><span class="pill"></span> <span class="rf-v"></span></p>'
                        f'<p class="rf-go"><a class="btn ghost" href="{SLUG[tid]}.html">{e(SHORT[lang]["tasks"][tid])}</a>{checked(B, lang, guide_date(tid))}</p></div>')
            elif flow: mine = f'<div class="rf-mine"><p class="rf-go"><a class="btn ghost" href="{flow["slug"]}.html">{e(flow["title"][lang])}</a>{checked(B, lang, min(s["d"] for s in flow["steps"] if s["d"]))}</p></div>'
            else: mine = f'<p class="hint">{e(t["advice"])}</p>'
            up = "#" if len(probs) == 1 else f"#{pid}"
            answers.append(f"""<section class="rf-ans" data-a="{pid}/{aid}" hidden><a class="rf-crumb" href="{up}">{A.IC["back"]}{e(name[lang])}</a><h2 tabindex="-1">{e(label[lang])}</h2>
<div class="rf-now"><p class="rf-lbl">{e(t['now'])}</p><p>{e(now[lang])}</p></div>
<div class="rf-say"><p class="rf-lbl">{e(t['say'])}</p>{says}</div>
<div class="rf-fail"><p class="rf-lbl">{e(t['fail'])}</p><p>{e(fail[lang])}</p></div>
{mine}</section>""")
            faq.append({"@type": "Question", "name": f"{name[lang]}: {label[lang]}", "acceptedAnswer": {"@type": "Answer", "text": f"{now[lang]} {fail[lang]}"}})
    data = {"q": q, "st": st, "tone": ux["tone"], "p": SHORT[lang]["prof"], "d": {d: U[d] for d in ("ios", "android")}}
    inner = f"""<div id="rf"><section id="rf-1"><h2 tabindex="-1">{e(t['q1'])}</h2><nav class="rf-g" aria-label="{e(t['q1'])}">{''.join(tiles)}</nav></section>
{''.join(steps)}{''.join(answers)}</div>
<a class="call rf-1330" href="tel:+82-2-1330" aria-label="{e(A.T[lang]['call'])} 1330: {e(t['stuck'])}"><b>1330</b><span>{e(t['stuck'])}</span><i aria-hidden="true">{A.IC['phone']}</i></a>
{B.LU.nonum_link(B, lang)}
<script type="application/json" id="rf-data">{js_json(data)}</script>"""
    path = L["dir"] + "refused.html"
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "@id": B.SITE + path, "url": B.SITE + path, "name": t["title"], "inLanguage": L["html_lang"], "mainEntity": faq}
    return B.app_page(lang, "refused", (t["title"], t["lede"]), t["seo"], t["desc"], inner, "help", REFUSED_JS, ld=ld, back_to="help.html")


def days_json(B, lang, full=False):
    """Trip items for one language. Home gets the short form (no sources)."""
    t = M.TM; items = []
    for iid, st, w, text, src, d, link, cond in M.DAYS:
        l = None
        if link:
            if link.startswith("guide:"): l = [SHORT[lang]["tasks"][link[6:]], SLUG[link[6:]] + ".html"]
            elif link == "my-card.html": l = [M.CARD["title"][lang], link]
            else: l = [A.T[lang][M.FOLD_LBL[link]], link]
        gd = next((k[6:] for k in src if k.startswith("guide:")), None)
        row = {"id": iid, "st": st, "w": list(w) if w else None, "t": text[lang], "l": l, "c": cond}
        if full:
            srcs = [[SHORT[lang]["tasks"][k[6:]], SLUG[k[6:]] + ".html"] if k.startswith("guide:") else list(M.SRC[k]) for k in src]
            row.update({"src": [s for s in srcs if not l or s[1] != l[1]] or srcs[:1], "d": d or (guide_date(gd) if gd else "")})
        items.append(row)
    ui = {k: t[k][lang] for k in ("to_go", "tomorrow", "day", "leaving", "nothing", "over", "remind", "saved", "now", "next", "all", "moved", "by")}
    ui["stages"] = {k: v[lang] for k, v in t["stages"].items()}
    return f'<script type="application/json" id="days-data">{js_json({"t": ui, "items": items, "bell": A.IC["bell"]})}</script>'


def days_block(B, lang):
    """My trip: the whole trip in order, with ticks and calendar reminders."""
    t = M.TM; e = B.e; a = TR.ALERT_TX
    return f"""<section class="sec days" id="days" aria-labelledby="dy-h"><div class="dy-head"><h2 id="dy-h">{e(t['h'][lang])}</h2><b id="days-now" class="dy-now" hidden></b></div>
<div id="days-need" hidden><p class="hint">{e(t['need'][lang])}</p><div class="trip-dates"><label>{e(a['from'][lang])}<input id="day-from" type="date"></label><label>{e(a['to'][lang])}<input id="day-to" type="date"></label></div></div>
<div id="days-list" class="dgs"></div><p class="hint" id="days-note" hidden>{e(t['remind_note'][lang])}</p></section>{days_json(B, lang, True)}"""


def home_row(B, lang):
    """Home: the three one-tap moments."""
    e = B.e
    b = lambda href, cls, svg, txt: f'<a class="mo {cls}" href="{href}"><span class="ic">{svg}</span><b>{e(txt)}</b></a>'
    return (f'<nav class="mos" aria-label="{e(M.MOS_LABEL[lang])}">{b("sos.html", "mo-sos", A.IC["sos"], M.SOS["short"][lang])}'
            f'{b("refused.html", "mo-rf", A.IC["refused"], M.RF["short"][lang])}{b("my-card.html", "mo-card", B.icon("food-booking"), M.CARD["short"][lang])}</nav>')


def help_rows(B, lang):
    """Help tab: emergency and refused first, as two large rows."""
    e = B.e
    row = lambda href, cls, ic, t: f'<a class="mo-row {cls}" href="{href}"><span class="ic">{A.IC[ic]}</span><span><b>{e(t["title"][lang])}</b><small>{e(t["lede"][lang])}</small></span></a>'
    return f'<nav class="mo-rows" aria-label="{e(M.MOS_LABEL[lang])}">{row("sos.html", "mo-sos", "sos", M.SOS)}{row("refused.html", "mo-rf", "refused", M.RF)}</nav>'


def card_links(B, lang):
    """Cards tab: the food card as a row, with 'saved' or 'make it' as its state."""
    e = B.e; t = M.CARD
    return (f'<ul class="glist mc-links"><li><a href="my-card.html"><span class="ic">{B.icon("food-booking")}</span><span>{e(t["link_food"][lang])}</span>'
            f'<small class="mc-st" data-k="emk-food" data-on="{e(t["set"][lang])}">{e(t["unset"][lang])}</small></a></li></ul>')
