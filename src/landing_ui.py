"""Screens for landing.py (31차): one ready-made Korean food card per page, and the page on living without a Korean number.
Nothing here sends anything; the card is shown, read aloud or printed on the phone."""
import json

import app_shell as A
import landing as L_
import moments as M
from data import LANGS, TASK_META
from data_extra import SHORT, UX, X
from moments_js import LANDING_JS
from moments_ui import checked, guide_date

SLUG = {tid: sl for tid, sl, _ in TASK_META}
WORD = {a[0]: (a[2], a[3]) for a in M.ALLERGY}


def stamp(B, lang, keys):
    link = lambda n, u: f'<a href="{B.e(u)}" rel="noopener" target="_blank">{B.e(n)}</a>'
    return f'<p class="fact-src">{checked(B, lang, L_.CHK)} {", ".join(link(*(L_.SRC[k] if k in L_.SRC else M.SRC[k])) for k in keys)}</p>'


def card_attrs(B, lang, c):
    ans = json.dumps([[a, m[lang]] for a, m in M.FOOD_ANS], ensure_ascii=False)
    return f'data-fc="{B.e(c["ko"])}" data-ans="{B.e(ans)}" data-mean="{B.e(c["m"][lang])}"'


def rows(B, lang, cards):
    """A card as a row: tap to show it full screen, with the Korean answers staff can tap."""
    e = B.e
    return "".join(f'<div class="sayrow askrow"><button class="sayrow-main" type="button" {card_attrs(B, lang, c)} aria-label="{e(L_.T["show"][lang])}: {e(c["m"][lang])}">'
                   f'<b lang="ko">{e(c["ko"].replace(chr(10) + L_.ASK, ""))}</b><span>{e(c["m"][lang])}</span><i aria-hidden="true">{A.IC["expand"]}</i></button></div>' for c in cards)


def answer(p, lang, key):
    """The text behind a page's question, taken from what the page already shows."""
    if key == "SAY": return f'{p["say"][0]} ({p["say"][1]})'
    if key == "EGG": return "저는 계란 알레르기가 있어요. (jeoneun gyeran allereugiga isseoyo)"
    if key == "CHAIN": return L_.T["chain"][lang]
    if key.startswith("FACT"): return p["facts"][int(key[4:])]["m"][lang]
    return M.CARD[key][lang]


def build_food(B, lang, p):
    e = B.e; t = {k: v[lang] for k, v in L_.T.items()}; L = LANGS[lang]
    ko, rom, kana = p["say"]
    hear = (f'<span class="lp-rom">{e(kana)}</span>' if lang == "ja" else "") + f'<span class="lp-rom" lang="ko-Latn">{e(rom)}</span>'
    words = "".join(f'<li><b lang="ko">{e(WORD[w][0])}</b><span>{e(WORD[w][1][lang])}</span></li>' for w in p["words"])
    notes = "".join(f'<p class="mc-off">{e(M.CARD[n][lang])}</p>' for n in p["notes"])
    lab = [f for f in p["facts"] if f["src"] == "label"]; rest = [f for f in p["facts"] if f["src"] != "label"]
    pack = ""
    if words or notes or lab:
        pack = (f'<section class="mc-label" aria-labelledby="lp-p"><h2 id="lp-p" class="mc-h">{e(t["pack"])}</h2>' + (f'<ul class="mc-words">{words}</ul>' if words else "")
                + "".join(f'<p class="mc-off">{e(f["m"][lang])}</p>' for f in lab) + notes + stamp(B, lang, ["label", "label28"] if "label_new" in p["notes"] else ["label"]) + "</section>")
    know = "".join(f'<p>{e(f["m"][lang])}</p>{stamp(B, lang, [f["src"]])}' for f in rest) + f'<p>{e(t["chain"])}</p>{stamp(B, lang, ["label"])}'
    others = "".join(f'<li><a href="{q["slug"]}.html"><span>{e(q["nav"][lang])}</span></a></li>' for q in L_.FOOD if q is not p)
    inner = f"""<div class="lp" id="lp" data-lbl="{e(t['show'])}" data-hot="{e(L_.SEV)}">
<section class="mc-top lp-card"><p class="mc-prev" lang="ko">{e(p['main']['ko'])}</p><p class="lp-mean">{e(p['main']['m'][lang])}</p>
<button class="btn alt" type="button" {card_attrs(B, lang, p['main'])}>🗣 {e(t['show'])}</button>
<div class="lp-acts"><a class="btn ghost" href="my-card.html#pick={p['pick']}">{e(t['mine'])}</a><button class="btn ghost" type="button" id="lp-print">{e(t['print'])}</button></div>
<p class="hint">{e(t['ans'])} {e(t['off'])}</p></section>
<section class="sec"><h2 class="mc-h">{e(t['say'])}</h2><p class="lp-say"><b lang="ko">{e(ko)}</b>{hear}</p></section>
<section class="sec"><h2 class="mc-h">{e(t['other'])}</h2>{rows(B, lang, p['more'])}</section>
<section class="sec"><h2 class="mc-h">{e(t['ask'])}</h2>{rows(B, lang, p['ask'])}</section>
{pack}
<section class="sec lp-know"><h2 class="mc-h">{e(t['know'])}</h2>{know}</section>
<ul class="glist lp-nav"><li><a href="sos.html"><span class="ic">{A.IC['sos']}</span><span>{e(t['sos'])}</span></a></li></ul>
<section class="sec"><h2 class="mc-h">{e(t['ready'])}</h2><ul class="glist lp-nav">{others}<li><a href="my-card.html"><span class="ic">{B.icon('food-booking')}</span><span>{e(M.CARD['title'][lang])}</span></a></li></ul></section>
</div>"""
    path = L["dir"] + p["slug"] + ".html"
    faq = [{"@type": "Question", "name": q[lang], "acceptedAnswer": {"@type": "Answer", "text": answer(p, lang, k)}} for q, k in p["faq"]]
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "@id": B.SITE + path, "url": B.SITE + path, "name": p["h1"][lang], "inLanguage": L["html_lang"], "lastReviewed": L_.CHK, "mainEntity": faq}
    return B.app_page(lang, p["slug"], (p["h1"][lang], ""), p["seo"][lang], p["desc"][lang], inner, "cards", LANDING_JS, ld=ld, back_to="my-card.html")


def ready_links(B, lang):
    """On the food card tool: the ready-made cards, one tap each."""
    li = "".join(f'<li><a href="{p["slug"]}.html"><span>{B.e(p["nav"][lang])}</span></a></li>' for p in L_.FOOD)
    return f'<section class="sec"><h2 class="mc-h">{B.e(L_.T["ready"][lang])}</h2><ul class="glist lp-nav">{li}</ul></section>'


def day(B, d, lang):
    """A logged day, or a month when the log only knows the month."""
    if len(d) == 10: return B.fmt_date(d, lang)
    full = B.fmt_date(d + "-01", lang)
    return full[2:] if lang in ("en", "vi") else full[:-2]


def build_nonum(B, lang):
    """One row per service, read from the guides: status, one line, the day it was checked."""
    e = B.e; N = {k: (v[lang] if isinstance(v, dict) else v) for k, v in L_.NONUM.items()}; L = LANGS[lang]; U = L["ui"]; tone = UX[lang]["tone"]
    by = {x["id"]: x for x in B.task_list(lang)}; out, faq = [], []
    for tid in N["tasks"]:
        a, b = B.resolve(by[tid], "visitor", "ios"), B.resolve(by[tid], "visitor", "android")
        lines = [("", a)] if a["verdict"] == b["verdict"] else [(U["ios"], a), (U["android"], b)]
        txt = "".join(f'<p class="lp-v"><span class="pill {v["s"]}">{e(tone[v["s"]])}</span>{f"<small>{e(d)}</small>" if d else ""}<span>{e(v["verdict"])}</span></p>' for d, v in lines)
        name = SHORT[lang]["tasks"][tid]
        out.append(f'<li class="lp-row"><a href="{SLUG[tid]}.html"><span class="ic">{B.icon(tid)}</span><b>{e(name)}</b></a>{txt}{checked(B, lang, guide_date(tid))}</li>')
        faq.append({"@type": "Question", "name": N["faq_q"].replace("{x}", name), "acceptedAnswer": {"@type": "Answer", "text": " ".join((f"{d}: " if d else "") + v["verdict"] for d, v in lines)}})
    en = [text for _d, text in X["en"]["changes"]]
    chg = [X[lang]["changes"][next(i for i, text in enumerate(en) if text.startswith(c))] for c in L_.NONUM["changes"]]
    chl = "".join(f'<li><time datetime="{d}">{e(day(B, d, lang))}</time> {e(text)}</li>' for d, text in sorted(chg, reverse=True))
    inner = f"""<div class="lp"><p class="lp-mean">{e(N['lede'])}</p><ul class="lp-rows">{''.join(out)}</ul>
<section class="sec lp-know"><h2 class="mc-h">{e(N['chg'])}</h2><ul class="lp-chg">{chl}</ul></section>
<ul class="glist lp-nav"><li><a href="refused.html#app"><span class="ic">{A.IC['refused']}</span><span><b>{e(N['stuck'])}</b><small>{e(N['stuck_t'])}</small></span></a></li></ul>
<p class="hint">{e(N['who'])}</p></div>"""
    path = L["dir"] + N["slug"] + ".html"
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "@id": B.SITE + path, "url": B.SITE + path, "name": N["h1"], "inLanguage": L["html_lang"], "lastReviewed": min(guide_date(x) for x in N["tasks"]), "mainEntity": faq}
    return B.app_page(lang, N["slug"], (N["h1"], ""), N["seo"], N["desc"], inner, "help", "", ld=ld, back_to="./")


def build_all(B, lang):
    return [build_food(B, lang, p) for p in L_.FOOD] + [build_nonum(B, lang)]


def nonum_link(B, lang):
    """On Refused?: the page that lists what works without a Korean number."""
    return f'<ul class="glist lp-nav"><li><a href="{L_.NONUM["slug"]}.html"><span class="ic">{A.IC["phone"]}</span><span>{B.e(L_.NONUM["h1"][lang])}</span></a></li></ul>'


def llms_full(B):
    """The same pages as plain text for AI search and assistants."""
    src = lambda k: " ".join(L_.SRC[k] if k in L_.SRC else M.SRC[k])
    out = []
    for p in L_.FOOD:
        out += ["", f"## {p['h1']['en']}", f"URL: {B.SITE}{p['slug']}.html", f"Last checked: {L_.CHK}", "", "Korean to show: " + p["main"]["ko"].replace("\n", " / "), f"Say: {p['say'][0]} ({p['say'][1]})"]
        out += [f"- {c['ko'].replace(chr(10), ' / ')} = {c['m']['en']}" for c in p["more"] + p["ask"]]
        if p["words"]: out.append("Words to look for on packages: " + ", ".join(f"{WORD[w][0]} ({WORD[w][1]['en']})" for w in p["words"]))
        out += [M.CARD[n]["en"] for n in p["notes"]] + [f"{f['m']['en']} (checked {L_.CHK}; source: {src(f['src'])})" for f in p["facts"]]
        out.append(f"{L_.T['chain']['en']} (checked {L_.CHK}; source: {src('label')})")
    N = L_.NONUM; by = {x["id"]: x for x in B.task_list("en")}
    out += ["", f"## {N['h1']['en']}", f"URL: {B.SITE}{N['slug']}.html", f"Last checked: {min(guide_date(x) for x in N['tasks'])}"]
    for tid in N["tasks"]:
        a, b = (B.resolve(by[tid], "visitor", d) for d in ("ios", "android"))
        out.append(f"- {SHORT['en']['tasks'][tid]}: " + (a["verdict"] if a["verdict"] == b["verdict"] else f"iPhone: {a['verdict']} Android: {b['verdict']}") + f" (checked {guide_date(tid)})")
    return out
