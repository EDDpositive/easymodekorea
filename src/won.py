"""Daily Seoul price game (33차, four-week test): five pages under /won/, one per language.

Apart from the rest of the site on purpose: no menu links, its own look, its own offline worker and icons.
You lay down won for five real Seoul prices, then see the price, its source and its date. Nothing typed or tapped is sent anywhere.
Prices live in won_data.py, drawings in won_art.py, words in won_text.py. build.py calls build(); docs/won-game.md has the upkeep rules.
"""
import hashlib, html, json

import won_art as A
import won_data as W
import won_text as X

START = "2026-11-26"   # day 1
PATHS = [X.DIR[k] for k in X.LANGS]
CATS = ["ride", "table", "out", "market", "bill"]
NOTES = [50000, 10000, 5000, 1000, 500, 100]

CSS = r"""
:root{--bg:#e9efec;--fg:#1b1c1e;--mut:#545c58;--card:#fff;--line:#cfd8d3;--tag:#ffde45;--ink:#1b1c1e;--red:#b5140b;--tray:#26313d;--trayl:#3a4857;--link:#1d4fb8;--ok:#1f7a45;--focus:#1d4fb8;
--n50:#f6c863;--n10:#a5d79c;--n5:#f4a595;--n1:#a3c6ee;--coin:#d9dee2}
@media (prefers-color-scheme:dark){:root{--bg:#111516;--fg:#f1f3f1;--mut:#a7b0ab;--card:#1c2224;--line:#37403f;--tray:#0a0d10;--trayl:#222c35;--link:#9cc0ff;--ok:#7bd69d;--focus:#ffde45}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 ui-rounded,"SF Pro Rounded","Hiragino Maru Gothic ProN",system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans","Noto Sans CJK JP",sans-serif;overflow-wrap:anywhere}
:lang(ja) body,:lang(zh-Hant) body,:lang(zh-Hans) body{word-break:normal;line-break:strict}
a{color:var(--link)}button{font:inherit;color:inherit;touch-action:manipulation;-webkit-tap-highlight-color:transparent}
:focus-visible{outline:3px solid var(--focus);outline-offset:2px}
.w{max-width:460px;margin:0 auto;padding:0 14px}.txt{max-width:720px}
.hd{display:flex;align-items:center;gap:8px;min-height:50px}
.brand{display:flex;align-items:center;gap:8px;font-weight:800;font-size:18px;letter-spacing:-.01em;margin:0;color:inherit;text-decoration:none;min-height:44px}
.brand svg{width:28px;height:28px}
.lg{margin-left:auto;position:relative}.lg summary{list-style:none;cursor:pointer;min-height:44px;min-width:44px;display:flex;align-items:center;justify-content:center;gap:4px;font-weight:700;font-size:14px;padding:0 8px;border-radius:10px}
.lg summary::-webkit-details-marker{display:none}.lg summary::after{content:"";border:5px solid transparent;border-top-color:currentColor;margin-top:5px}
.lg div{position:absolute;right:0;top:46px;z-index:5;background:var(--card);border:2px solid var(--fg);border-radius:12px;padding:6px;min-width:150px;box-shadow:0 10px 24px rgba(0,0,0,.18)}
.lg a{display:block;padding:10px 12px;color:var(--fg);text-decoration:none;border-radius:8px;font-weight:600}.lg a[aria-current]{background:var(--tag);color:var(--ink)}
.top{display:flex;align-items:center;gap:10px;margin:0 0 8px}
.bars{display:flex;gap:4px;flex:1;list-style:none;margin:0;padding:0}.bars li{flex:1;height:7px;border-radius:4px;background:var(--line);overflow:hidden}.bars i{display:block;height:100%;background:var(--ok);border-radius:4px}.bars li.on{background:var(--fg)}
.dt{font-size:13px;font-weight:700;color:var(--mut);white-space:nowrap}
.fr{background:var(--ink);color:#fff;border-radius:12px;padding:8px 12px;font-weight:600;font-size:15px;margin:0 0 10px}
h1.q{font-size:22px;line-height:1.2;margin:2px 0 2px;letter-spacing:-.01em}.how{margin:0 0 10px;color:var(--mut);font-size:14px;line-height:1.4}
.tag{background:var(--tag);color:var(--ink);border:2.5px solid var(--ink);border-radius:16px;padding:0 14px 10px;margin:0 0 10px;overflow:hidden}
.cat{margin:0 -14px 10px;padding:6px 14px 7px;background:var(--ink);color:var(--tag);font-weight:800;font-size:14px;line-height:1.3}
.it{display:flex;gap:12px;align-items:center;min-height:84px}
.ic{width:100%;height:100%;display:block}.pic{flex:none;width:84px;height:84px;background:#fffbe8;border:2.5px solid var(--ink);border-radius:16px;padding:8px}
.it h2{font-size:20px;line-height:1.2;margin:0;letter-spacing:-.01em}.it h2.l{font-size:17px}.ko{margin:2px 0 0;font-size:14px;font-weight:600;line-height:1.3}.u{margin:2px 0 0;font-size:14px;line-height:1.35}
.lines{list-style:none;margin:2px 0 0;padding:0}.lines li{display:flex;align-items:center;gap:10px;min-height:46px;border-top:2px dashed rgba(27,28,30,.28);font-weight:700;line-height:1.25}.lines li:first-child{border-top:0}
.lines .pic{width:38px;height:38px;padding:3px;border-radius:9px;border-width:2px}.lines b{margin-left:auto;font-variant-numeric:tabular-nums;white-space:nowrap}.lines .x{font-weight:800;min-width:30px}
.pr{display:flex;align-items:baseline;justify-content:flex-end;gap:8px;margin:6px 0 0;font-weight:900;font-size:34px;line-height:1.05;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.pr small{font-size:13px;font-weight:700;letter-spacing:0}.pr.in{color:var(--red)}
.tray{background:var(--tray);background-image:repeating-linear-gradient(90deg,var(--trayl) 0 1px,transparent 1px 12px);color:#fff;border-radius:14px;padding:8px 10px;margin:0 0 10px;min-height:70px;display:flex;align-items:center;gap:8px}
.st{display:flex;flex-wrap:wrap;gap:5px;flex:1;min-width:0}.st .em{color:#c9d3db;font-size:14px}
.bl{position:relative;border:2px solid var(--ink);min-width:50px;height:46px;border-radius:7px;padding:0 5px;font-weight:800;font-size:13px;color:var(--ink);cursor:pointer;font-variant-numeric:tabular-nums}
.bl b{position:absolute;right:-5px;top:-7px;background:#fff;border:2px solid var(--ink);border-radius:10px;font-size:11px;line-height:1;padding:2px 4px}
.bl.co{border-radius:50%;min-width:46px;width:46px}
.amt{text-align:right;flex:none}.amt output{display:block;font-weight:900;font-size:23px;line-height:1.1;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.clr{background:none;border:0;color:#fff;text-decoration:underline;min-height:44px;min-width:44px;margin:-7px 0 -8px;padding:0 2px;font-size:13px;cursor:pointer}
.keys{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0 0 10px}
.nt{position:relative;height:54px;border:2.5px solid var(--ink);border-radius:9px;color:var(--ink);font-weight:900;font-size:18px;letter-spacing:-.01em;cursor:pointer;font-variant-numeric:tabular-nums;overflow:hidden;
background-image:repeating-radial-gradient(circle at 8% 120%,rgba(255,255,255,.5) 0 2px,transparent 2px 8px),radial-gradient(circle at 92% 50%,rgba(255,255,255,.65) 0 10px,transparent 11px)}
.nt:active,.pay:active,.bl:active{transform:translateY(2px)}
.n50000{background-color:var(--n50)}.n10000{background-color:var(--n10)}.n5000{background-color:var(--n5)}.n1000{background-color:var(--n1)}.n500,.n100{background-color:var(--coin)}
.nt.co{border-radius:27px;background-image:radial-gradient(circle at 50% 50%,transparent 0 21px,rgba(27,28,30,.35) 21px 22.5px,transparent 22.5px)}
.pay{display:flex;align-items:center;justify-content:center;width:100%;min-height:54px;border:2.5px solid var(--ink);border-radius:14px;background:var(--ink);color:var(--tag);font-weight:800;font-size:18px;line-height:1.2;cursor:pointer;padding:8px 12px;text-align:center;text-decoration:none}
@media (prefers-color-scheme:dark){.pay{background:var(--tag);color:var(--ink)}}
.fx{margin:8px 0 0;font-size:13px;color:var(--mut);text-align:center;line-height:1.35;text-wrap:balance}
.pay.sec{background:transparent;color:var(--fg);border-color:var(--fg);font-size:16px;font-weight:700}
.res{background:var(--card);border-radius:18px;padding:14px;margin:0 0 10px}
.rt{display:flex;align-items:center;gap:12px}.rt p{margin:0}.sc{flex:none;width:72px;height:72px;border-radius:50%;display:grid;place-content:center;text-align:center;background:conic-gradient(var(--ok) calc(var(--v)*1%),var(--line) 0);position:relative}
.sc::before{content:"";position:absolute;inset:7px;border-radius:50%;background:var(--card)}.sc b{position:relative;font-size:24px;line-height:1;font-weight:900}.sc small{position:relative;font-size:11px;font-weight:700;color:var(--mut)}
.you{font-size:15px;color:var(--mut)}.df{font-size:18px;font-weight:800;line-height:1.25}
.gg{position:relative;height:46px;margin:12px 4px 0}.gg::before{content:"";position:absolute;left:0;right:0;top:21px;height:4px;border-radius:2px;background:var(--line)}
.gg i{position:absolute;top:14px;width:18px;height:18px;margin-left:-9px;border-radius:50%;border:3px solid var(--card)}.gg .r{background:#d6281c}.gg .y{background:var(--fg)}.gg s{position:absolute;top:21px;height:4px;background:#d6281c;opacity:.55}
.gl{display:flex;gap:14px;font-size:13px;color:var(--mut);font-weight:600}.gl span{display:flex;align-items:center;gap:5px}.gl i{width:10px;height:10px;border-radius:50%}
.tip{margin:10px 0 0;font-weight:600}.so{margin:8px 0 0;font-size:13px;color:var(--mut);line-height:1.45}.so a{display:inline-block;padding:6px 0;color:var(--link)}
.bd{background:var(--ink);color:#fff;border:3px solid var(--ink);border-radius:18px;overflow:hidden;margin:0 0 12px}
@media (prefers-color-scheme:dark){.bd{border-color:var(--tag)}.tray{box-shadow:inset 0 0 0 1px #3a4857}}
.bh{background:var(--tag);color:var(--ink);padding:10px 14px 12px}.bh .hd2{display:flex;justify-content:space-between;gap:10px;font-weight:800;font-size:14px;margin:0 0 4px}
.bs{display:flex;align-items:center;gap:14px;margin:0}.big{font-weight:900;font-size:60px;line-height:1;letter-spacing:-.03em;font-variant-numeric:tabular-nums;white-space:nowrap}.big small{font-size:18px;letter-spacing:0;font-weight:800;margin-left:6px}
.lv{font-weight:800;font-size:20px;line-height:1.2}
.rl{list-style:none;margin:0;padding:6px;display:grid;gap:6px}.rl li{display:grid;grid-template-columns:44px minmax(0,1fr) auto;gap:0 10px;align-items:center;background:#fffbe8;color:var(--ink);border-radius:9px;padding:6px 10px 6px 6px;font-size:15px;line-height:1.25}
.rl .pic{width:44px;height:44px;padding:3px;border-radius:9px;border:0;background:none}.rl span{font-weight:700}.rl small{display:block;font-weight:500;color:#545c58;font-size:13px;line-height:1.35}.rl .rr{text-align:right;white-space:nowrap}.rl .rr b{display:block;font-size:17px;font-weight:900;letter-spacing:-.01em}
.rl b,.rl .m{font-variant-numeric:tabular-nums}.rl .m{font-weight:800;font-size:15px}
.up{color:#b5140b}.dn{color:#1d4fb8}.ok{color:#1f7a45}
.sum{margin:0;padding:4px 14px 12px;font-weight:700;line-height:1.35;color:var(--tag)}.vs{margin:0;padding:0 14px 12px;font-weight:800}
.acts{display:grid;gap:8px;margin:0 0 12px}.msg{margin:0;font-size:14px;color:var(--mut);min-height:0}.pv{width:100%;height:auto;border-radius:14px;display:block;border:1px solid var(--line)}.pvr{display:grid;grid-auto-flow:column;grid-auto-columns:1fr;gap:8px;margin-top:8px}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0 0 10px}.stats div{background:var(--card);border-radius:14px;padding:10px 6px;text-align:center}.stats b{display:block;font-size:24px;line-height:1.1;font-weight:900}.stats span{font-size:13px;color:var(--mut)}
.tm{margin:0 0 12px;text-align:center;font-weight:700}
.emk{display:block;background:var(--card);border-radius:16px;padding:12px 14px;margin:0 0 12px;color:var(--fg);text-decoration:none}.emk b{display:block}.emk span{color:var(--link);text-decoration:underline}
details.b{background:var(--card);border-radius:14px;margin:0 0 8px}details.b>summary{cursor:pointer;font-weight:700;padding:13px 14px;min-height:48px;line-height:1.35}details.b>div{padding:0 14px 14px}details.b p{margin:0}
.ar{display:grid;grid-template-columns:repeat(auto-fill,minmax(92px,1fr));gap:8px}.ar button{border:2px solid var(--line);background:transparent;border-radius:12px;min-height:54px;padding:4px;font-weight:700;font-size:14px;line-height:1.2;cursor:pointer}.ar button small{display:block;font-weight:600;color:var(--mut)}.ar button[aria-current]{border-color:var(--fg)}
.yl{list-style:none;margin:0;padding:0}.yl li{display:flex;gap:10px;justify-content:space-between;padding:6px 0;border-top:1px solid var(--line)}.yl li:first-child{border-top:0}.yl b{white-space:nowrap}
main.txt{padding-top:18px;padding-bottom:20px}main.txt h2{font-size:21px;line-height:1.25;margin:26px 0 10px}main.txt ol{padding-left:22px;margin:0}main.txt li{margin:0 0 6px}
.pl h3{margin:14px 0 6px;font-size:16px}.pl table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.35}.pl th,.pl td{text-align:left;vertical-align:top;padding:7px 6px 7px 0;border-top:1px solid var(--line)}.pl td:nth-child(2),.pl th:nth-child(2){text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums;font-weight:700}.pl td span{display:block;color:var(--mut);font-size:13px}.pl td a{display:inline-block}
.pl td:nth-child(3){width:36%;padding-right:0}
footer{border-top:1px solid var(--line);margin-top:26px;padding:14px 0 30px;font-size:14px;color:var(--mut)}footer p{margin:0 0 8px}footer a,.lk{display:inline-block;padding:10px 0;min-height:44px}.lk{background:none;border:0;color:var(--link);text-decoration:underline;cursor:pointer;font-size:14px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
#game{min-height:560px}
@media (prefers-reduced-motion:no-preference){.in{animation:pop .32s cubic-bezier(.2,1.4,.4,1)}.res,.bd{animation:rise .3s ease-out}.bl{animation:drop .16s ease-out}
@keyframes pop{from{transform:scale(.7);opacity:0}}@keyframes rise{from{transform:translateY(14px);opacity:0}}@keyframes drop{from{transform:translateY(-10px);opacity:.2}}}
@media (max-height:640px){h1.q{display:none}.how{margin-bottom:6px}.pic{width:68px;height:68px}.it{min-height:68px}.nt{height:48px}.pay{min-height:48px}.pr{font-size:28px;margin-top:2px}}
@media (min-width:700px){h1.q{font-size:26px}.it h2{font-size:22px}}
@media print{#game,.lg{display:none}}
"""

JS = r"""
(function () {
  'use strict';
  var D = JSON.parse(document.getElementById('won-data').textContent), T = D.t, root = document.getElementById('game'), live = document.getElementById('live');
  var N = [50000, 10000, 5000, 1000, 500, 100], CATS = ['ride', 'table', 'out', 'market', 'bill'], KEY = 'wad1', st = null;
  try { st = JSON.parse(localStorage.getItem(KEY)); } catch (e) { }
  if (!st || typeof st !== 'object' || !st.d) st = { d: {} };
  function save() { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) { } }
  function count(p) { try { window.goatcounter && window.goatcounter.count && window.goatcounter.count({ path: 'won/' + D.lang + '/' + p, title: p, event: true }); } catch (e) { } }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function num(n) { return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, D.sep); }
  function won(n) { return '₩' + num(n); }
  function f(s, o) { return s.replace(/\{(\w)\}/g, function (_, k) { return o[k]; }); }
  function today() { var n = new Date(); return Math.max(1, Math.floor((Date.UTC(n.getFullYear(), n.getMonth(), n.getDate()) - D.start) / 864e5) + 1); }
  function dateOf(d) { return new Date(D.start + (d - 1) * 864e5); }
  function fmt(d, o) { try { return new Intl.DateTimeFormat(D.tag, Object.assign({ timeZone: 'UTC' }, o)).format(dateOf(d)); } catch (e) { return ''; } }

  /* The same five for everyone on one date. Lists of different lengths, and a different start after each lap, keep the mix changing. */
  function setOf(d) {
    var i = d - 1;
    function p(list, step) { return list[(i + Math.floor(i / list.length) * step) % list.length]; }
    function one(c, id) { return { c: c, p: D.i[id][3], l: [[1, id]] }; }
    var s = p(D.s, 9);
    return [one('ride', p(D.o.ride, 3)), one('table', p(D.o.table, 5)), one('out', p(D.o.out, 7)), one('market', p(D.o.market, 11)),
      { c: 'bill', n: s[0], l: s[1], p: s[1].reduce(function (a, x) { return a + x[0] * D.i[x[1]][3]; }, 0) }];
  }
  /* Closeness in percent: the smaller amount over the larger. Free things: one point lost for every 25 won. */
  function pts(g, p) { return p === 0 ? Math.max(0, Math.round(100 - g / 25)) : g === 0 ? 0 : Math.round(100 * Math.min(g, p) / Math.max(g, p)); }
  function score(d, gs) { var q = setOf(d); return Math.round(gs.reduce(function (a, g, i) { return a + pts(g, q[i].p); }, 0) / 5); }
  function level(s) { return T['lv' + (s >= 90 ? 4 : s >= 80 ? 3 : s >= 65 ? 2 : s >= 45 ? 1 : 0)]; }

  var day, friend, Q, tray, hist, shown;
  function rec() { return st.d[day] || (st.d[day] = { g: [] }); }
  function open() {
    var m = /^#(\d{1,4})(?:-(\d{1,3}))?$/.exec(location.hash), t = today();
    day = m && +m[1] >= 1 && +m[1] <= t ? +m[1] : t; friend = m && m[2] && +m[2] <= 100 && day === +m[1] ? +m[2] : null;
    Q = setOf(day); shown = false; tray = {}; hist = [];
    if (friend !== null) count('friend');
    document.querySelectorAll('.lg a').forEach(function (a) { a.hash = location.hash; });
    draw();
  }
  function total() { return N.reduce(function (a, n) { return a + n * (tray[n] || 0); }, 0); }
  function pic(id) { var x = D.i[id]; return '<span class="pic"><svg class="ic" viewBox="0 0 64 64" fill="none" stroke="#1b1c1e" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + D.a[x[4]].split('"C"').join('"' + x[5] + '"') + '</svg></span>'; }
  function price(p) { return p === 0 ? T.isfree : won(p); }

  function bars() {
    var g = rec().g;
    return '<ol class="bars" aria-hidden="true">' + Q.map(function (q, i) {
      var past = i < g.length, cur = i === (shown ? g.length - 1 : g.length);
      return '<li' + (cur && !past ? ' class="on"' : '') + '>' + (past ? '<i style="width:' + Math.max(8, pts(g[i], q.p)) + '%"></i>' : '') + '</li>';
    }).join('') + '</ol>';
  }
  function top() { return '<div class="top">' + bars() + '<span class="dt">#' + day + ' · ' + esc(fmt(day, { day: 'numeric', month: 'short' })) + '</span></div>'; }
  function tag(q, i, done) {
    var body, x;
    if (q.c === 'bill') {
      body = '<h2 class="sr">' + esc(q.n) + '</h2><ul class="lines">' + q.l.map(function (l) { var y = D.i[l[1]]; return '<li>' + pic(l[1]) + '<span class="x">' + l[0] + ' ×</span><span>' + esc(y[0]) + '</span>' + (done ? '<b>' + (y[3] ? won(l[0] * y[3]) : T.isfree) + '</b>' : '') + '</li>'; }).join('') + '</ul>';
    } else {
      x = D.i[q.l[0][1]];
      body = '<div class="it">' + pic(q.l[0][1]) + '<div><h2' + (x[0].length > D.long ? ' class="l"' : '') + '>' + esc(x[0]) + '</h2><p class="ko" lang="ko">' + esc(x[2]) + '</p><p class="u">' + esc(x[1]) + '</p></div></div>';
    }
    return '<article class="tag"><p class="cat">' + esc(T['c_' + q.c]) + (q.n ? ': ' + esc(q.n) : '') + '</p>' + body + '<p class="pr' + (done ? ' in' : '') + '">' + (done ? '<small>' + esc(T.real) + '</small><span id="rp">' + esc(price(q.p)) + '</span>' : '<span aria-hidden="true">₩ ?</span>') + '</p></article>';
  }
  function drawTray() {
    var t = total(), s = document.getElementById('st'), any = false;
    s.innerHTML = N.map(function (n) { if (!tray[n]) return ''; any = true; return '<button type="button" class="bl n' + n + (n < 1000 ? ' co' : '') + '" data-back="' + n + '" aria-label="' + esc(f(T.back, { n: num(n) })) + (tray[n] > 1 ? ' (' + tray[n] + ')' : '') + '">' + num(n) + (tray[n] > 1 ? '<b>×' + tray[n] + '</b>' : '') + '</button>'; }).join('') || '<span class="em">' + esc(T.tray) + '</span>';
    document.getElementById('out').textContent = won(t); document.getElementById('clr').hidden = !any;
    var b = document.getElementById('pay'); b.textContent = t ? f(T.pay, { n: won(t) }) : T.free; b.className = t ? 'pay' : 'pay sec';
  }
  function play() {
    var g = rec().g, i = g.length, q = Q[i];
    root.innerHTML = top() + (friend !== null && !i ? '<p class="fr">' + esc(f(T.friend, { n: friend })) + '</p>' : '')
      + (i === 0 ? '<h1 class="q">' + esc(T.h1) + '</h1><p class="how">' + esc(T.how) + ' ' + esc(T.lede) + '</p>' : '<h1 class="sr">' + esc(T.h1) + '</h1>') + '<p class="sr" id="of">' + esc(f(T.of, { n: i + 1 })) + '</p>'
      + tag(q, i, false)
      + '<div class="keys">' + N.map(function (n) { return '<button type="button" class="nt n' + n + (n < 1000 ? ' co' : '') + '" data-add="' + n + '" aria-label="' + esc(f(T.add, { n: num(n) })) + '">' + num(n) + '</button>'; }).join('') + '</div>'
      + '<div class="tray"><div class="st" id="st"></div><div class="amt"><output id="out"></output><button type="button" class="clr" id="clr">' + esc(T.clear) + '</button></div></div>'
      + '<button type="button" class="pay" id="pay"></button><p class="fx">' + esc(D.fx) + '</p>';
    drawTray();
  }
  function diff(g, p) { return g === p ? T.spot : f(g > p ? T.over : T.under, { n: won(Math.abs(g - p)) }); }
  var calm = matchMedia('(prefers-reduced-motion: reduce)');
  function roll(el, p) {
    if (!el || !p || calm.matches || document.hidden) return;
    var t0 = 0;
    (function step(t) { if (!el.isConnected) return; t0 = t0 || t; var k = t ? Math.min(1, (t - t0) / 620) : 0; el.textContent = k < 1 ? won(Math.round(p * (1 - Math.pow(1 - k, 3)) / 10) * 10) : price(p); if (k < 1) requestAnimationFrame(step); })(0);
  }
  function reveal() {
    var g = rec().g, i = g.length - 1, q = Q[i], v = g[i], s = pts(v, q.p), max = Math.max(v, q.p, 1) * 1.08, ids = q.l.map(function (l) { return l[1]; }), srcs = {}, tip = q.c === 'bill' ? '' : D.i[ids[0]][7];
    ids.forEach(function (id) { D.i[id][6].split(' ').forEach(function (k) { srcs[k] = 1; }); });
    var a = Math.min(v, q.p) / max * 100, b = Math.max(v, q.p) / max * 100;
    root.innerHTML = top() + '<h1 class="sr">' + esc(T.h1) + '</h1>' + tag(q, i, true)
      + '<section class="res"><div class="rt"><div class="sc" style="--v:' + s + '"><b>' + s + '</b><small>' + esc(T.pts) + '</small></div><div><p class="you">' + esc(f(T.paid, { n: won(v) })) + '</p><p class="df">' + esc(diff(v, q.p)) + '</p></div></div>'
      + '<div class="gg" aria-hidden="true"><s style="left:' + a + '%;width:' + (b - a) + '%"></s><i class="r" style="left:' + q.p / max * 100 + '%"></i><i class="y" style="left:' + v / max * 100 + '%"></i></div>'
      + '<div class="gl" aria-hidden="true"><span><i style="background:#d6281c"></i>' + esc(T.real) + '</span><span><i style="background:var(--fg)"></i>' + esc(T.you) + '</span></div>'
      + (tip ? '<p class="tip">' + esc(tip) + '</p>' : '')
      + '<p class="so">' + esc(T.src) + ': ' + Object.keys(srcs).map(function (k) { return '<a href="' + esc(D.r[k][1]) + '" target="_blank" rel="noopener">' + esc(D.r[k][0]) + '</a> (' + esc(D.r[k][2]) + ')'; }).join(', ') + '</p></section>'
      + '<button type="button" class="pay" id="next">' + esc(i === 4 ? T.fin : T.next) + '</button>';
    live.textContent = T.real + ' ' + price(q.p) + '. ' + diff(v, q.p) + '. ' + s + ' ' + T.pts;
    roll(document.getElementById('rp'), q.p);
    var n = document.getElementById('next'); n.focus({ preventScroll: true });
    if (n.getBoundingClientRect().bottom > innerHeight) n.scrollIntoView({ block: 'end', behavior: calm.matches ? 'auto' : 'smooth' });
  }
  function streak() { var t = today(), n = 0, k = st.d[t] && st.d[t].on && st.d[t].g.length === 5 ? t : t - 1; while (st.d[k] && st.d[k].on && st.d[k].g.length === 5) { n++; k--; } return n; }
  function sums() { var g = rec().g; return { a: g.reduce(function (x, y) { return x + y; }, 0), b: Q.reduce(function (x, y) { return x + y.p; }, 0) }; }
  function mark(g, p) { var s = pts(g, p); return s >= 90 ? ['ok', '✓'] : g > p ? ['up', '▲'] : ['dn', '▼']; }
  function name(q) { return q.c === 'bill' ? T.c_bill + ': ' + q.n : D.i[q.l[0][1]][0]; }
  function svg(id) { var x = D.i[id]; return '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 64 64" fill="none" stroke="#1b1c1e" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">' + D.a[x[4]].split('"C"').join('"' + x[5] + '"') + '</svg>'; }
  function image(id) { return new Promise(function (ok) { var im = new Image(); im.onload = function () { ok(im); }; im.onerror = function () { ok(null); }; im.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg(id)); }); }
  function link() { return D.url + '#' + day + '-' + score(day, rec().g); }
  function shareText() { var s = sums(); return D.brand + ' #' + day + ' · ' + score(day, rec().g) + '/100\n' + f(T.mine, { a: won(s.a), b: won(s.b) }) + '\n' + Q.map(function (q, i) { return ['🚌', '🍜', '🎫', '🥬', '💵'][i] + pts(rec().g[i], q.p) + mark(rec().g[i], q.p)[1]; }).join(' ') + '\n' + T.beat; }
  function finish() {
    var g = rec().g, sc = score(day, g), s = sums(), t = today(), all = Object.keys(st.d).filter(function (k) { return st.d[k].g && st.d[k].g.length === 5; });
    var avg = all.length ? Math.round(all.reduce(function (a, k) { return a + score(+k, st.d[k].g); }, 0) / all.length) : 0;
    var old = []; for (var k = t; k >= 1 && old.length < 30; k--) old.push(k);
    root.innerHTML = '<h1 class="sr">' + esc(T.h1) + '</h1><section class="bd" aria-label="' + esc(T.score) + '"><div class="bh"><p class="hd2"><span>' + esc(D.brand) + ' #' + day + '</span><span>' + esc(fmt(day, { day: 'numeric', month: 'short', year: 'numeric' })) + '</span></p>'
      + '<p class="bs"><span class="big">' + sc + '<small>/ 100</small></span><span class="lv">' + esc(level(sc)) + '</span></p></div><ul class="rl">'
      + Q.map(function (q, i) { var m = mark(g[i], q.p); return '<li>' + pic(q.l[0][1]) + '<span>' + esc(name(q)) + '<small>' + esc(f(T.paid, { n: won(g[i]) })) + '</small></span><div class="rr"><b>' + esc(price(q.p)) + '</b><span class="m ' + m[0] + '">' + pts(g[i], q.p) + ' ' + m[1] + '</span></div></li>'; }).join('')
      + '</ul><p class="sum">' + esc(f(T.sum, { a: won(s.a), b: won(s.b) })) + '</p>' + (friend !== null ? '<p class="vs">' + esc(f(T.vs, { a: sc, b: friend })) + '</p>' : '') + '</section>'
      + '<div class="acts"><button type="button" class="pay" id="share">' + esc(T.share) + '</button><button type="button" class="pay sec" id="pic">' + esc(T.pic) + '</button><p class="msg" id="msg" role="status"></p><div id="pvb"></div></div>'
      + '<div class="stats"><div><b>' + streak() + '</b><span>' + esc(T.streak) + '</span></div><div><b>' + all.length + '</b><span>' + esc(T.played) + '</span></div><div><b>' + avg + '</b><span>' + esc(T.avg) + '</span></div></div>'
      + (day === t ? '<p class="tm">' + esc(T.tmrw) + '</p>' : '<button type="button" class="pay sec" data-day="' + t + '" style="margin-bottom:12px">' + esc(T.totoday) + '</button>')
      + '<a class="emk" href="' + esc(D.home) + '" data-emk><b>' + esc(T.emk_h) + '</b><span>' + esc(T.emk_p) + '</span></a>'
      + (old.length > 1 ? '<details class="b"><summary>' + esc(T.earlier) + '</summary><div class="ar">' + old.map(function (k) { var r = st.d[k], d = r && r.g && r.g.length === 5; return '<button type="button" data-day="' + k + '"' + (k === day ? ' aria-current="true"' : '') + '>#' + k + (d ? ' · ' + score(k, r.g) : '') + '<small>' + esc(k === t ? T.today : fmt(k, { day: 'numeric', month: 'short' })) + '</small></button>'; }).join('') + '</div></details>' : '')
      + (day === t && t > 1 ? '<details class="b"><summary>' + esc(T.yest) + '</summary><div><ul class="yl">' + setOf(t - 1).map(function (q) { return '<li><span>' + esc(name(q)) + '</span><b>' + esc(price(q.p)) + '</b></li>'; }).join('') + '</ul></div></details>' : '');
    live.textContent = D.brand + ' #' + day + ': ' + sc + ' / 100. ' + level(sc);
  }
  function draw() { var n = rec().g.length; if (shown) reveal(); else if (n >= 5) finish(); else play(); }
  function pay() {
    var r = rec();
    if (shown || r.g.length >= 5) return;
    if (!r.g.length) count('start');
    r.g.push(total()); if (day === today()) r.on = 1; else if (r.g.length < 5) delete r.on;
    if (r.g.length === 5) count('done');
    save(); tray = {}; hist = []; shown = true; draw();
  }
  function next() { shown = false; draw(); scrollTo({ top: 0 }); var el = root.querySelector('.bd, .tag'); if (el) { el.tabIndex = -1; el.focus({ preventScroll: true }); el.style.outline = 'none'; } }

  /* The picture: a snack-bar wall menu, drawn on the phone. Names and points only, so a friend can still play. */
  function paint() {
    return Promise.all(Q.map(function (q) { return image(q.l[0][1]); })).then(function (ims) {
      var W = 1080, H = 1350, c = document.createElement('canvas'), x = c.getContext('2d'), g = rec().g, sc = score(day, g), s = sums(), F = 'ui-rounded, "SF Pro Rounded", "Hiragino Sans", system-ui, -apple-system, "Segoe UI", "Noto Sans CJK JP", sans-serif', K = '#1b1c1e', Y = '#ffde45';
      c.width = W; c.height = H; c.lang = D.tag;
      function text(t, px, y, size, weight, col, align, max) { x.font = weight + ' ' + size + 'px ' + F; x.fillStyle = col; x.textAlign = align || 'left'; while (max && x.measureText(t).width > max && size > 22) { size -= 1; x.font = weight + ' ' + size + 'px ' + F; } x.fillText(t, px, y); return x.measureText(t).width; }
      function box(l, t, w, h, r, col) { x.fillStyle = col; x.beginPath(); x.moveTo(l + r, t); x.arcTo(l + w, t, l + w, t + h, r); x.arcTo(l + w, t + h, l, t + h, r); x.arcTo(l, t + h, l, t, r); x.arcTo(l, t, l + w, t, r); x.closePath(); x.fill(); }
      x.fillStyle = '#c2180e'; x.fillRect(0, 0, W, H);
      box(48, 48, 984, 1186, 44, K); box(62, 62, 956, 336, 32, Y); x.fillStyle = Y; x.fillRect(62, 330, 956, 68);
      text(D.brand + ' #' + day, 100, 136, 52, '900', K); text(fmt(day, { day: 'numeric', month: 'short', year: 'numeric' }), 980, 134, 36, '700', K, 'right');
      var w = text(String(sc), 96, 340, 210, '900', K); text('/ 100', 96 + w + 20, 340, 54, '800', K);
      var lx = 96 + w + 180; text(T.h1, lx, 236, 40, '700', K, 'left', 980 - lx); text(level(sc), lx, 300, 56, '900', '#b5140b', 'left', 980 - lx);
      Q.forEach(function (q, n) {
        var y = 412 + n * 142, p = pts(g[n], q.p), m = mark(g[n], q.p), col = m[0] === 'ok' ? '#1f7a45' : m[0] === 'up' ? '#b5140b' : '#1d4fb8';
        box(62, y, 956, 130, 22, '#fffbe8');
        if (ims[n]) x.drawImage(ims[n], 82, y + 17, 96, 96);
        text(q.n || name(q), 204, y + 56, 42, '800', K, 'left', 600);
        box(204, y + 78, 560, 24, 12, '#ded8bd'); if (p > 4) box(204, y + 78, 560 * p / 100, 24, 12, col);
        text(p + ' ' + m[1], 984, y + 84, 60, '900', col, 'right');
      });
      text(f(T.mine, { a: won(s.a), b: won(s.b) }), W / 2, 1190, 40, '800', Y, 'center', 900);
      text(D.url.replace('https://', '').replace(/\/$/, ''), W / 2, 1304, 44, '800', '#fff', 'center', W - 120);
      return c;
    });
  }
  function picture() {
    var box = document.getElementById('pvb'), msg = document.getElementById('msg'), d = day; count('pic');
    paint().then(function (c) {
      c.toBlob(function (b) {
        if (!b || !box.isConnected) return;
        var u = URL.createObjectURL(b), file = null, name = 'won-a-day-' + d + '.png';
        try { file = new File([b], name, { type: 'image/png' }); if (!navigator.canShare || !navigator.canShare({ files: [file] }) || !matchMedia('(pointer: coarse)').matches) file = null; } catch (e) { file = null; }
        box.innerHTML = '<img class="pv" width="1080" height="1350" alt="' + esc(D.brand + ' #' + d + ', ' + score(d, rec().g) + ' / 100') + '" src="' + u + '"><div class="pvr">' + (file ? '<button type="button" class="pay sec" id="send">' + esc(T.send) + '</button>' : '') + '<a class="pay sec" download="' + name + '" href="' + u + '">' + esc(T.save) + '</a></div>'; msg.textContent = T.hold;
        if (file) document.getElementById('send').onclick = function () { navigator.share({ files: [file], text: link() }).catch(function () { }); };
        box.scrollIntoView({ block: 'nearest', behavior: calm.matches ? 'auto' : 'smooth' });
      }, 'image/png');
    });
  }
  function share() {
    var text = shareText(), url = link(), msg = document.getElementById('msg'); count('share');
    if (navigator.share && matchMedia('(pointer: coarse)').matches) { navigator.share({ text: text, url: url }).catch(function () { }); return; }
    (navigator.clipboard ? navigator.clipboard.writeText(text + '\n' + url) : Promise.reject()).then(function () { msg.textContent = T.copied; }, function () { msg.textContent = text + ' ' + url; });
  }
  function add(n) { if (total() + n > 999900) return; tray[n] = (tray[n] || 0) + 1; hist.push(n); drawTray(); }
  function back(n) { if (!tray[n]) return; tray[n]--; var k = hist.lastIndexOf(n); if (k >= 0) hist.splice(k, 1); drawTray(); }
  var at = 0;
  root.addEventListener('click', function (e) {
    var b = e.target.closest('button, a'); if (!b) return;
    if (b.dataset.add) add(+b.dataset.add);
    else if (b.dataset.back) { var n = b.dataset.back; back(+n); var nb = root.querySelector('[data-back="' + n + '"]') || root.querySelector('[data-add="' + n + '"]'); if (nb) nb.focus({ preventScroll: true }); }
    else if (b.id === 'clr') { tray = {}; hist = []; drawTray(); root.querySelector('[data-add]').focus({ preventScroll: true }); }
    else if (b.id === 'pay' || b.id === 'next') { if (e.isTrusted && Date.now() - at < 350) return; at = Date.now(); if (b.id === 'pay') pay(); else next(); } /* a double tap must not skip the answer */ else if (b.id === 'share') share(); else if (b.id === 'pic') picture();
    else if (b.dataset.day) { var d = +b.dataset.day; if (d === today() ? location.hash === '' : location.hash === '#' + d) open(); else location.hash = d === today() ? '' : '#' + d; scrollTo({ top: 0 }); }
    else if ('emk' in b.dataset) count('emk');
  });
  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey || !document.getElementById('pay')) return;
    var k = +e.key;
    if (k >= 1 && k <= 6) { add(N[k - 1]); e.preventDefault(); }
    else if (e.key === 'Backspace' && hist.length) { back(hist[hist.length - 1]); e.preventDefault(); }
    else if (e.key === 'Enter' && total() && !/^(BUTTON|A|SUMMARY)$/.test(document.activeElement.tagName)) pay();
  });
  addEventListener('hashchange', open);
  var seen = today();
  document.addEventListener('visibilitychange', function () { if (!document.hidden && today() !== seen) { seen = today(); if (!location.hash && rec().g.length >= 5) open(); } });
  document.getElementById('wipe').addEventListener('click', function () { if (!confirm(T.wipeq)) return; try { localStorage.removeItem(KEY); } catch (e) { } st = { d: {} }; open(); scrollTo({ top: 0 }); });
  if ('serviceWorker' in navigator) navigator.serviceWorker.register(D.up + 'sw.js', { scope: D.up }).then(function () { return navigator.serviceWorker.ready; }).then(function () { document.getElementById('off').hidden = false; }).catch(function () { });
  window.WAD = { setOf: setOf, pts: pts, today: today, paint: paint, text: function () { return shareText() + '\n' + link(); } };
  open();
})();
"""

SW = r"""/* Offline copy of the daily price game, separate from the rest of the site. Newest first; the saved copy answers without a connection or after three seconds.
   Only the languages opened on this phone are kept. */
const C='won-@V@',S=self.registration.scope;
const key=u=>{u=new URL(u);return u.origin+u.pathname.replace(/index\.html$/,'')};
const fresh=u=>new Request(u,{cache:'reload'});
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil((async()=>{
  const c=await caches.open(C),old=(await caches.keys()).filter(k=>k.startsWith('won-')&&k!==C),want=new Map();
  for(const k of old){const o=await caches.open(k);for(const r of await o.keys())want.set(r.url,await o.match(r))}
  for(const w of await self.clients.matchAll({includeUncontrolled:true,type:'window'}))if(w.url.startsWith(S)&&!want.has(key(w.url)))want.set(key(w.url),null);
  for(const[u,was]of want){try{await c.add(fresh(u))}catch(x){if(was)await c.put(u,was)}}
  await Promise.all(old.map(k=>caches.delete(k)));await self.clients.claim()})()));
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||!r.url.startsWith(S))return;const k=key(r.url);
  e.respondWith((async()=>{const c=await caches.open(C),old=()=>c.match(k);
    const net=fetch(r).then(async x=>{if(x.ok)await c.put(k,x.clone());return x});
    const slow=new Promise(y=>setTimeout(async()=>{const h=await old();if(h)y(h)},3000));
    try{return await Promise.race([net,slow])}catch(x){const h=await old();if(h)return h;if(r.mode==='navigate'){const any=(await c.keys()).find(q=>q.url.endsWith('/'));if(any)return c.match(any)}throw x}})())});
"""

LOGO = '<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="29" fill="#ffde45" stroke="#1b1c1e" stroke-width="4"/><path d="M15 23l8 22 9-22 9 22 8-22M12 32h40" fill="none" stroke="#1b1c1e" stroke-width="4.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def e(s):
    return html.escape(str(s), quote=True)


def js(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def won(n, lang):
    return "₩" + (f"{n:,}".replace(",", ".") if lang == "vi" else f"{n:,}")


def label(src, lang):
    _u, d, kind, _n = W.SRC[src]
    return X.pick(X.KIND[kind], lang).replace("{d}", X.date(d, lang))


def build_lang(B, lang):
    P = lambda s: X.pick(s, lang)
    t = {k: P(v) for k, v in X.T.items()}
    depth = "" if lang == "en" else "../"
    arts = sorted({v["art"] for v in W.ITEMS.values()})
    data = {"lang": lang, "tag": X.TAG[lang], "sep": "." if lang == "vi" else ",", "start": None, "brand": X.BRAND, "url": B.SITE + X.DIR[lang], "up": depth or "./", "home": "/" + X.HOME[lang],
            "long": 26 if lang in ("en", "vi") else 13,
            "i": {i: [P(v["n"]), P(v["u"]), v["ko"], v["p"], v["art"], v["c"], v["s"], P(v["tip"]) if v["tip"] else ""] for i, v in W.ITEMS.items()},
            "r": {k: [P(v[3]), v[0], label(k, lang)] for k, v in W.SRC.items()}, "o": W.ORDER, "s": [[P(n), W.scene(s)] for n, s in W.SCENES], "a": {k: A.ART[k] for k in arts},
            "fx": X.fx(W.FX, lang),
            "t": {k: v for k, v in t.items() if k not in ("title", "desc", "noscript", "h_how", "h_faq", "h_list", "spoil", "col_i", "col_p", "col_s", "by", "contact", "note", "off", "lang", "wipe", "billq")}}
    y, m, d = map(int, START.split("-"))
    import datetime
    data["start"] = int(datetime.datetime(y, m, d, tzinfo=datetime.timezone.utc).timestamp() * 1000)
    title = t["title"] + " | " + X.BRAND
    url = B.SITE + X.DIR[lang]
    alts = "".join(f'<link rel="alternate" hreflang="{X.TAG[k]}" href="{B.SITE}{X.DIR[k]}">' for k in X.LANGS) + f'<link rel="alternate" hreflang="x-default" href="{B.SITE}{X.DIR["en"]}">'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": f"{X.BRAND}: {t['h1']}", "url": url, "inLanguage": X.TAG[lang], "applicationCategory": "GameApplication", "operatingSystem": "Any", "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}, "publisher": {"@type": "Organization", "name": "EasyModeKorea", "url": B.SITE}},
        {"@type": "FAQPage", "inLanguage": X.TAG[lang], "lastReviewed": W.CHK, "mainEntity": [{"@type": "Question", "name": P(q), "acceptedAnswer": {"@type": "Answer", "text": P(a)}} for q, a in X.FAQ]}]}
    def srcs(i):
        return "".join(f'<a href="{e(W.SRC[k][0])}" target="_blank" rel="noopener">{e(P(W.SRC[k][3]))}</a><span>{e(label(k, lang))}</span>' for k in W.ITEMS[i]["s"].split())

    def rows(ids):
        return "".join(f'<tr><td>{e(P(W.ITEMS[i]["n"]))}<span>{e(P(W.ITEMS[i]["u"]))}</span></td><td>{e(t["isfree"] if not W.ITEMS[i]["p"] else won(W.ITEMS[i]["p"], lang))}</td>'
                       f'<td>{srcs(i)}</td></tr>' for i in sorted(ids, key=lambda k: W.ITEMS[k]["p"]))
    tables = "".join(f'<h3>{e(t["c_" + c])}</h3><table><thead><tr><th scope="col">{e(t["col_i"])}</th><th scope="col">{e(t["col_p"])}</th><th scope="col">{e(t["col_s"])}</th></tr></thead><tbody>{rows(W.ORDER[c])}</tbody></table>' for c in CATS[:4])
    langs = "".join(f'<a href="/{X.DIR[k]}" lang="{X.TAG[k]}" hreflang="{X.TAG[k]}"{" aria-current=page" if k == lang else ""}>{X.NAME[k]}</a>' for k in X.LANGS)
    page = f"""<!doctype html>
<html lang="{X.TAG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#e9efec"><meta name="theme-color" media="(prefers-color-scheme: dark)" content="#111516"><meta name="color-scheme" content="light dark">
<link rel="icon" type="image/png" sizes="192x192" href="/won/icon-192.png"><link rel="apple-touch-icon" href="/won/icon-192.png"><link rel="manifest" href="/{X.DIR[lang]}manifest.webmanifest">
<title>{e(title)}</title>
<meta name="description" content="{e(t['desc'])}">
<link rel="canonical" href="{url}">{alts}
<meta property="og:type" content="website"><meta property="og:site_name" content="{X.BRAND}"><meta property="og:locale" content="{X.OG[lang]}"><meta property="og:title" content="{e(t['title'])}"><meta property="og:description" content="{e(t['lede'])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{B.SITE}won/og-{lang}.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<style>{CSS.strip()}</style>
<script type="application/ld+json">{js(ld)}</script>
<script data-goatcounter="{B.GOAT}" async src="//gc.zgo.at/count.js"></script>
</head>
<body>
<header class="w hd"><a class="brand" href="/{X.DIR[lang]}">{LOGO}{X.BRAND}</a>
<details class="lg"><summary aria-label="{e(t['lang'])}">{X.SHORT[lang]}</summary><div>{langs}</div></details></header>
<div class="w"><div id="game"><h1 class="q">{e(t['h1'])}</h1><p class="how">{e(t['lede'])}</p></div><noscript><p>{e(t['noscript'])}</p></noscript><p class="sr" id="live" role="status"></p></div>
<main class="w txt">
<section aria-labelledby="h-how"><h2 id="h-how">{e(t['h_how'])}</h2><ol>{''.join(f'<li>{e(P(x))}</li>' for x in X.HOW)}</ol></section>
<section aria-labelledby="h-faq"><h2 id="h-faq">{e(t['h_faq'])}</h2>{''.join(f'<details class="b"><summary>{e(P(q))}</summary><div><p>{e(P(a))}</p></div></details>' for q, a in X.FAQ)}</section>
<section aria-labelledby="h-list"><h2 id="h-list">{e(t['h_list'])}</h2><details class="b pl"><summary>{e(t['spoil'].replace('{n}', str(len(W.ITEMS))))}</summary><div>{tables}</div></details></section>
<footer><p>{e(t['note'])}</p><p id="off" hidden>{e(t['off'])}</p><p><a href="/{X.HOME[lang]}">{e(t['by'])}</a> · <a href="/{X.HOME[lang]}contact.html">{e(t['contact'])}</a> · <button class="lk" type="button" id="wipe">{e(t['wipe'])}</button></p></footer>
</main>
<script type="application/json" id="won-data">{js(data)}</script>
<script>{JS.strip()}</script>
</body>
</html>
"""
    B.write(X.DIR[lang] + "index.html", page)
    return page


def manifest(lang):
    """One per language, so a home-screen icon opens the language it was added from."""
    icon = lambda n, p: {"src": f"/won/icon-{n}.png", "sizes": f"{n}x{n}", "type": "image/png", "purpose": p}
    return json.dumps({"id": "/" + X.DIR[lang], "name": f"{X.BRAND}: {X.pick(X.T['h1'], lang)}", "short_name": X.BRAND, "lang": X.TAG[lang], "start_url": "/" + X.DIR[lang], "scope": "/won/", "display": "standalone",
                       "background_color": "#e9efec", "theme_color": "#e9efec", "icons": [icon(192, "any"), icon(512, "any"), icon(512, "maskable")]}, ensure_ascii=False, indent=1) + "\n"


def build(B):
    pages = "".join(build_lang(B, k) for k in X.LANGS)
    for k in X.LANGS: B.write(X.DIR[k] + "manifest.webmanifest", manifest(k))
    B.write("won/sw.js", SW.replace("@V@", hashlib.sha256((pages + SW).encode()).hexdigest()[:8]))
    return list(PATHS)


def alternates(site):
    """hreflang lines for the sitemap."""
    return "".join(f'<xhtml:link rel="alternate" hreflang="{X.TAG[k]}" href="{site}{X.DIR[k]}"/>' for k in X.LANGS) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{site}{X.DIR["en"]}"/>'
