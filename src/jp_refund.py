"""One Korean page: Japan's tax-free refund helper (32차, four-week test).

Separate from the rest of the site on purpose: Korean only, not in any menu, its own small offline worker,
no shared stylesheet or script. Everything is worked out on the phone and nothing typed here is sent anywhere.
It never names, compares or links to refund companies, cards or fees: only official procedure.

Facts were read on CHK from the pages in SRC. build.py calls build().
"""
import hashlib, html, json

CHK = "2026-11-25"
SLUG = "japan-tax-refund"
PATH = f"ko/{SLUG}.html"
START = "2026-11-01"      # sales from this day use the refund method (NTA Q&A 8: sale date, not departure date)
FOOD_CUT = "2027-04-01"   # planned lower rate on food (Cabinet decision 2026-09-15, bill not passed yet): no food estimate from here
WIFI, WIFI_PW = "Customs_WiFi_For_TaxRefund", "jcustoms"   # printed on the customs page itself

SRC = {
    "jta": ("일본 관광청 여행자 안내", "https://www.mlit.go.jp/kankocho/tax-free/page01_000001_00021.html"),
    "jta_q": ("일본 관광청 출국·세관 문답", "https://www.mlit.go.jp/kankocho/tax-free/page01_000001_00050.html"),
    "jta_pay": ("일본 관광청 환급 문답", "https://www.mlit.go.jp/kankocho/tax-free/page01_000001_00051.html"),
    "who": ("일본 관광청 대상자 목록", "https://www.mlit.go.jp/kankocho/tax-free/content/001981481.pdf"),
    "cus": ("일본 세관 한국어 안내문", "https://www.customs.go.jp/kaigairyoko/taxrefund/refund_korea.pdf"),
    "map": ("일본 세관 단말기 지도", "https://www.customs.go.jp/kaigairyoko/taxrefund/map.htm"),
    "wifi": ("일본 세관 온라인 절차", "https://www.customs.go.jp/kaigairyoko/taxrefund/vjw.html"),
    "vjw": ("일본 국세청 온라인 절차 안내(한국어)", "https://www.nta.go.jp/publication/pamph/shohi/menzei/201805/format/002/onlinetetsuzuki/guidekor.htm"),
    "vjw_q": ("일본 국세청 온라인 절차 문답(한국어)", "https://www.nta.go.jp/publication/pamph/shohi/menzei/201805/format/002/onlinetetsuzuki/faqkor.htm"),
    "nta": ("일본 국세청 문답(2026년 11월 개정)", "https://www.nta.go.jp/publication/pamph/shohi/menzei/201805/pdf/0025012-025_02.pdf"),
    "nta_kr": ("일본 국세청 한국어 안내문", "https://www.nta.go.jp/publication/pamph/shohi/menzei/201805/pdf/0026011-052_04.pdf"),
    "rate": ("일본 국세청 세율 안내", "https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6303.htm"),
    "food": ("일본 국세청 식품 세율 인하 안내", "https://www.nta.go.jp/taxes/shiraberu/zeimokubetsu/shohi/keigenzeiritsu/zeiritsuhikisage.htm"),
    "kcs": ("한국 관세청 여행자 휴대품", "https://customs.go.kr/kcs/cm/cntnts/cntntsView.do?mi=2837&cntntsId=829"),
}

# Where the tax refund terminals are: Japan Customs' own list (file dated 2026-11-18). "" = the list gives no floor.
# (id, name, place, can use a phone instead)
AIR_TOP = [("NRT1", "나리타 1터미널", "4층", 1), ("NRT2", "나리타 2터미널", "3층", 1), ("NRT3", "나리타 3터미널", "2층", 1),
           ("HND3", "하네다 3터미널", "3층", 1), ("HND2", "하네다 2터미널", "3층 국제선 구역", 1),
           ("KIX1", "간사이 1터미널", "4층", 1), ("KIX2", "간사이 2터미널", "1층", 1), ("FUK", "후쿠오카 국제선", "3층", 1),
           ("CTS", "신치토세(삿포로) 국제선", "3층", 1), ("NGO1", "주부(나고야) 1터미널", "3층", 1), ("NGO2", "주부(나고야) 2터미널", "2층", 1),
           ("OKA", "나하(오키나와)", "3층 국제선 구역", 1)]
AIR = [("KOJ", "가고시마", "국제선 1층", 0), ("KCZ", "고치", "1층", 0), ("KMQ", "고마쓰", "1층", 0), ("UKB", "고베 2터미널", "1층", 0), ("KMJ", "구마모토", "1층", 0),
       ("KKJ", "기타큐슈", "1층", 0), ("NGS", "나가사키", "1층", 0), ("KIJ", "니가타", "1층", 0), ("TAK", "다카마쓰", "1층", 0), ("TKS", "도쿠시마", "1층", 0),
       ("TOY", "도야마", "1층", 0), ("MYJ", "마쓰야마", "1층", 0), ("KMI", "미야자키", "1층", 0), ("HSG", "사가", "1층", 0), ("SDJ", "센다이", "", 0),
       ("FSZ", "시즈오카", "1층", 0), ("SHI", "시모지시마", "", 0), ("AKJ", "아사히카와", "1층", 0), ("AOJ", "아오모리", "1층", 0), ("AXT", "아키타", "", 0),
       ("OKJ", "오카야마", "1층", 0), ("OIT", "오이타", "1층", 0), ("YGJ", "요나고", "1층", 0), ("IBR", "이바라키", "1층", 0), ("ISG", "이시가키", "", 0),
       ("HNA", "하나마키", "1층", 0), ("HKD", "하코다테", "1층", 0), ("FKS", "후쿠시마", "1층", 0), ("HIJ", "히로시마", "", 0)]
SEA = [("S-HKT", "하카타항 국제터미널", "", 0), ("S-SHS", "시모노세키항 국제터미널", "", 0), ("S-OSA", "오사카항 국제페리터미널", "1층", 0), ("S-HTK", "쓰시마 히타카쓰항 국제터미널", "", 0),
       ("S-IZH", "쓰시마 이즈하라항 국제터미널", "", 0), ("S-SMN", "사카이항 유메미나토터미널", "", 0), ("S-MAI", "마이즈루항 제2부두", "1층", 0),
       ("S-TPZ", "오사카항 덴포잔 크루즈", "2층", 0), ("S-UKB", "고베항 포트터미널", "2층", 0), ("S-YOK", "요코하마항 오산바시", "3층", 0), ("S-TYO", "도쿄국제크루즈터미널", "", 0),
       ("S-NGS", "나가사키항 마쓰가에 제2빌딩", "", 0), ("S-SSB", "사세보항 국제터미널", "", 0), ("S-NAH", "나하항 크루즈터미널", "2층", 0), ("S-ISG", "이시가키항 국제터미널", "", 0)]

# Japanese to show. (id, Japanese, Korean meaning)
CARDS_AIR = [("where", "免税手続きの端末はどこですか。", "면세 단말기가 어디예요?"),
             ("ate", "免税品の一部を、食べたり使ったりしました。\n手続きの前に申告したいです。", "면세품 일부를 먹거나 썼어요. 절차 전에 말씀드리고 싶어요."),
             ("gone", "免税品の一部を持っていません。\n手続きの前に申告したいです。", "면세품 일부가 지금 없어요. 절차 전에 말씀드리고 싶어요."),
             ("all", "免税品は全部ここにあります。\n荷物を預ける前に確認をお願いします。", "면세품은 전부 여기 있어요. 짐 부치기 전에 확인 부탁드려요."),
             ("domestic", "国内線から国際線に乗り継ぎます。\n免税手続きはどこでしますか。", "국내선에서 국제선으로 갈아타요. 면세 절차는 어디서 하나요?")]
CARDS_SHOP = [("tax", "免税でお願いします。\nパスポートです。", "면세로 부탁해요. 여권이에요."),
              ("split", "食べ物は、別のレシートにしてください。", "먹을 것은 영수증을 따로 해 주세요."),
              ("how", "返金は、どうやって受け取りますか。\n手数料はありますか。", "환급은 어떻게 받나요? 수수료가 있나요?")]

TIPS = [("여권 실물 챙기기", "면세 가게에서 여권을 보여 줘야 면세로 살 수 있습니다.", "who"),
        ("먹을 것은 영수증을 따로", "영수증 하나에서 하나라도 먹거나 없으면 그 영수증 전체를 못 돌려받습니다.", "jta_q"),
        ("5,000엔은 세금을 빼고", "같은 가게에서 같은 날 산 것을 더합니다. 옷과 식품도 같이 더합니다.", "nta"),
        ("상자와 라벨 버리지 않기", "무엇을 샀는지 알 수 없으면 확인을 못 받을 수 있습니다.", "nta"),
        ("택배로 먼저 보내지 않기", "세관 확인 전에 따로 보내면 못 돌려받습니다.", "cus"),
        ("환급 등록은 가게마다", "맡는 업체가 달라서 가게에서 준 안내로 하나씩 가입·등록해야 합니다. 현금은 안 되는 곳도 있습니다.", "nta_kr")]

FAQ = [("포장을 뜯거나 쓰면 못 돌려받나요?", "옷·신발·가전은 일본에서 써도, 가지고 나가면 됩니다. 음식·화장품·약은 조금이라도 먹거나 쓰면 그 영수증 전체가 안 됩니다. 이때는 단말기를 누르기 전에 세관 직원에게 말합니다.", ["jta_q", "nta"]),
       ("소모품 50만 엔 한도가 있나요?", "없어졌습니다. 밀봉 봉투도 없어졌습니다. 대신 전부 직접 들고 나갈 수 있는 양이어야 합니다.", ["nta", "jta"]),
       ("90일은 언제부터 세나요?", "산 다음 날부터 셉니다. 2026년 11월 1일에 사면 2027년 1월 30일까지 출국하면서 확인을 받아야 합니다.", ["nta"]),
       ("10월 31일까지 산 것은요?", "떠나는 날이 아니라 산 날로 정합니다. 10월 31일까지 산 것은 예전 방식(살 때 세금을 뺌)입니다.", ["nta"]),
       ("짐을 이미 부쳤어요.", "부친 짐은 면세 절차 때문에 다시 찾을 수 없고, 환급도 받을 수 없습니다.", ["jta"]),
       ("공항에서 얼마나 걸리나요?", "단말기는 몇 초면 됩니다. 빨강이 나오면 검사를 받아야 해서 더 걸립니다. 늦어서 비행기를 놓쳐도 보상이 없으니 일찍 가세요.", ["jta_q", "jta"]),
       ("세관 확인이 끝났어요. 이제 뭘 하나요?", "카드 등으로 받기로 했다면 입금을 기다리면 됩니다. 현금으로 받기로 한 것만 그 업체의 현금 창구로 갑니다. 환급 문의는 세관이 아니라 업체나 가게에 합니다.", ["nta_kr", "vjw_q"]),
       ("영수증을 꼭 보여 줘야 하나요?", "꼭은 아닙니다. 다만 세관 직원이 보여 달라고 할 수 있어 가지고 있는 편이 좋습니다.", ["jta_q"]),
       ("단말기 대신 폰으로 할 수 있나요?", "나리타·하네다·간사이·주부·후쿠오카·신치토세·나하 7곳에서 됩니다. 출발 로비의 전용 와이파이에 연결해 Visit Japan Web의 ‘환급 절차’에서 합니다. 안 되면 단말기를 쓰면 됩니다.", ["vjw", "wifi"]),
       ("현금으로 받을 수 있나요?", "가게마다 다릅니다. 산 가게에 물어보세요. 세관은 환급 문의를 받지 않습니다.", ["jta_pay", "nta_kr"]),
       ("일본에서 일하거나 유학 중이에요.", "한국인은 단기체재 등으로 들어와 6개월이 안 된 사람이 대상입니다. 취업·유학 자격은 목록에 없습니다.", ["who"]),
       ("확인을 받고 물건을 두고 오면요?", "돌려받은 세금을 내야 하고 처벌받을 수 있습니다.", ["jta"])]

CSS = r"""
:root{--bg:#f3f5fb;--sf:#fff;--ink:#0e1430;--mut:#444f6b;--ln:#d5dbea;--br:#2336e8;--lk:#2336e8;--ey:#ffd23f;--ok:#0b6e37;--okb:#ddf4e7;--wn:#8a4f00;--wnb:#ffefcf;--no:#c62828;--nob:#fde5e5;--sel:#e7eaff;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--bg:#0b0f1e;--sf:#141a2e;--ink:#eef1fb;--mut:#b3bbd2;--ln:#2d3657;--br:#4a59ee;--lk:#9aa4ff;--ok:#5ad48c;--okb:#11301f;--wn:#f2b453;--wnb:#352610;--no:#ff8a80;--nob:#3a1616;--sel:#222b52;color-scheme:dark}}
*{box-sizing:border-box}[hidden]{display:none!important}
[lang=ja]{word-break:normal;word-break:auto-phrase;line-break:strict}
html{scroll-padding-top:56px;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:400 17px/1.55 system-ui,-apple-system,"Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",sans-serif;word-break:keep-all;overflow-wrap:anywhere;padding-bottom:calc(96px + env(safe-area-inset-bottom))}
a{color:var(--lk)}:focus-visible{outline:3px solid var(--ey);outline-offset:2px;border-radius:8px}
.w{max-width:680px;margin:0 auto;padding:0 16px}
.hd{background:var(--br);color:#fff;padding:18px 0 22px}
.by{margin:0 0 14px;font-size:14px;color:rgba(255,255,255,.85)}.by b{background:var(--ey);color:#0e1430;border-radius:6px;padding:1px 7px;margin-right:6px}
h1{margin:0;font-size:clamp(28px,7.6vw,38px);line-height:1.2;letter-spacing:-.02em;text-wrap:balance}
.lede{margin:10px 0 0;font-size:17px}.lede b{color:var(--ey)}
.chk{margin:8px 0 0;font-size:14px;color:rgba(255,255,255,.85)}
.jump{position:sticky;top:0;z-index:5;background:var(--sf);border-bottom:1px solid var(--ln)}
.jump .w{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding-top:8px;padding-bottom:8px}.jump .w::-webkit-scrollbar{display:none}
.jump a{flex:none;display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border:1px solid var(--ln);border-radius:999px;font-size:15px;font-weight:600;color:var(--ink);text-decoration:none}
h2{margin:30px 0 10px;font-size:22px;line-height:1.3;letter-spacing:-.01em}
.card{background:var(--sf);border:1px solid var(--ln);border-radius:16px;padding:16px;margin:0 0 12px}
.f{display:block;margin:0 0 14px}.f:last-child{margin-bottom:0}
.f>span:first-child,.leg{display:block;font-weight:700;font-size:15px;margin:0 0 6px}.f small,.leg small{font-weight:400;color:var(--mut)}
input[type=date],input[type=text],select{width:100%;min-height:52px;font:inherit;color:var(--ink);background:var(--bg);border:1px solid var(--ln);border-radius:12px;padding:8px 12px}
.dt{display:flex;gap:8px}.f>.dt{margin:0}.dt .btn{flex:none;border-radius:12px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:10px}
fieldset{border:0;margin:0 0 14px;padding:0;min-width:0}legend{padding:0}
.ch{display:grid;gap:8px}
.ch label{display:flex;align-items:center;gap:10px;min-height:52px;padding:8px 14px;border:1.5px solid var(--ln);border-radius:12px;cursor:pointer;line-height:1.35}
.ch label small{display:block;color:var(--mut);font-size:14px}
.ch input{flex:none;width:20px;height:20px;margin:0;accent-color:var(--br)}
.ch label:has(input:checked){border-color:var(--br);background:var(--sel)}
.ch label:has(input:focus-visible){outline:3px solid var(--ey);outline-offset:2px}
.tg{display:flex;align-items:center;gap:10px;min-height:48px;cursor:pointer}.tg input{width:22px;height:22px;margin:0;accent-color:var(--br);flex:none}
.rh{display:flex;justify-content:space-between;align-items:center;margin:0 0 12px;min-height:44px}.rh h3{margin:0;font-size:18px}
.x{min-height:44px;padding:0 8px;border:0;background:none;font:inherit;font-size:15px;color:var(--mut);text-decoration:underline;cursor:pointer}
.res{border-radius:12px;padding:12px 14px;margin-top:14px;background:var(--bg);color:var(--mut)}
.res b{display:block;font-size:19px;line-height:1.3}.res p{margin:4px 0 0}
.res.ok{background:var(--okb);color:var(--ok)}.res.no{background:var(--nob);color:var(--no)}.res.wn{background:var(--wnb);color:var(--wn)}
.res p{color:var(--ink)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:52px;padding:10px 18px;border-radius:14px;border:1.5px solid var(--br);background:var(--br);color:#fff;font-family:inherit;font-weight:700;font-size:17px;line-height:1.3;cursor:pointer;text-decoration:none;text-align:center}
.btn.g{background:none;color:var(--lk);border-color:var(--ln)}.btn.full{width:100%}
.acts{display:grid;gap:10px;margin:12px 0 0}
.sum{background:var(--sf);border:2px solid var(--br);border-radius:16px;padding:16px}
.sum b{font-size:30px;line-height:1.2;display:block;letter-spacing:-.02em}.sum p{margin:4px 0 0}
.mut{color:var(--mut);font-size:15px}
ol.st{list-style:none;margin:0;padding:0;counter-reset:s}
ol.st>li{counter-increment:s;background:var(--sf);border:1px solid var(--ln);border-radius:16px;margin:0 0 10px;padding:14px 16px}
ol.st>li.alert{border-color:var(--no);background:var(--nob)}
.sh{display:flex;gap:12px;align-items:flex-start}
.ck{flex:none;width:44px;height:44px;border-radius:50%;border:2px solid var(--br);background:none;color:var(--lk);font-family:inherit;font-weight:700;font-size:18px;line-height:1;cursor:pointer;padding:0}
.ck::before{content:counter(s)}.ck[aria-pressed=true]{background:var(--okb);border-color:var(--ok);color:var(--ok)}.ck[aria-pressed=true]::before{content:"✓"}
.done .sh strong{color:var(--mut)}
.sh>div{flex:1;min-width:0}.sh strong{display:block;font-size:18px;line-height:1.35;padding-top:8px}.sh p{margin:4px 0 0}
.mini{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.mini .btn{min-height:44px;padding:6px 14px;font-size:15px;border-radius:12px}
code{font:700 14px/1.5 ui-monospace,Consolas,monospace;background:var(--bg);border:1px solid var(--ln);border-radius:8px;padding:2px 6px;overflow-wrap:anywhere}
.say{display:flex;justify-content:space-between;align-items:center;gap:12px;width:100%;min-height:60px;text-align:left;background:var(--sf);border:1px solid var(--ln);border-radius:14px;padding:12px 16px;margin:0 0 8px;color:var(--ink);font:inherit;cursor:pointer}
.say b{display:block;font-size:17px;line-height:1.4}.say small{color:var(--mut);font-size:15px}.say i{font-style:normal;font-size:22px;color:var(--lk)}
.tips{list-style:none;margin:0;padding:0}.tips li{background:var(--sf);border:1px solid var(--ln);border-radius:14px;padding:12px 16px;margin:0 0 8px}.tips b{display:block;font-size:17px}
details{background:var(--sf);border:1px solid var(--ln);border-radius:14px;margin:0 0 8px}
summary{cursor:pointer;min-height:52px;padding:12px 16px;font-weight:700;line-height:1.4;display:flex;align-items:center;justify-content:space-between;gap:10px;list-style:none}summary::-webkit-details-marker{display:none}
summary::after{content:"+";font-size:22px;color:var(--lk)}details[open]>summary::after{content:"–"}
details>div{padding:0 16px 14px}details p{margin:0 0 6px}
.src{font-size:14px;color:var(--mut)}.src a{color:inherit}
table{width:100%;border-collapse:collapse;font-size:16px}th,td{text-align:left;padding:9px 6px;border-bottom:1px solid var(--ln);vertical-align:top}th{font-size:14px;color:var(--mut)}caption{text-align:left;font-weight:700;padding:12px 0 4px}
.bar{position:fixed;left:0;right:0;bottom:0;z-index:6;background:var(--sf);border-top:1px solid var(--ln);padding:10px 0 calc(10px + env(safe-area-inset-bottom));box-shadow:0 -8px 24px -18px rgba(14,20,48,.7)}
.bar .w{display:flex;justify-content:space-between;align-items:center;gap:12px}.bar b{display:block;font-size:18px;line-height:1.25}.bar small{color:var(--mut);font-size:14px}.bar .btn{flex:none;min-height:48px;padding:8px 16px;font-size:16px}
dialog{border:0;padding:0;margin:0;width:100vw;max-width:100vw;height:100vh;height:100dvh;max-height:none;background:#fff;color:#0e1430}
.dl{min-height:100%;display:flex;flex-direction:column;justify-content:space-between;padding:20px 18px calc(20px + env(safe-area-inset-bottom))}
.dl p{margin:0}.dl .big{font-size:clamp(30px,9.2vw,56px);line-height:1.45;font-weight:700;white-space:pre-line;font-family:"Hiragino Sans","Noto Sans JP","Yu Gothic UI",Meiryo,sans-serif;line-break:strict}
.dl .m{color:#444f6b;margin-bottom:14px}
footer{margin-top:34px;padding:20px 0 10px;border-top:1px solid var(--ln);font-size:15px;color:var(--mut)}footer p{margin:0 0 8px}footer a{display:inline-block;padding:10px 0;color:inherit}
"""

JS = r"""
(function () {
  var D = JSON.parse(document.getElementById('jpr-data').textContent), KEY = 'jpr1', P = {};
  D.ports.forEach(function (p) { P[p[0]] = p; });
  function $(i) { return document.getElementById(i); }
  function count(p) { try { window.goatcounter && window.goatcounter.count && window.goatcounter.count({ path: 'jpr/' + p, title: p, event: true }); } catch (e) {} }
  var once = {}; function count1(p) { if (!once[p]) { once[p] = 1; count(p); } }

  /* Dates are plain days (no clock), so the phone's time zone never moves a deadline. */
  function day(s) { var m = /^(\d{4})-(\d\d)-(\d\d)$/.exec(s || ''); return m ? Date.UTC(+m[1], m[2] - 1, +m[3]) : NaN; }
  function add(s, n) { return new Date(day(s) + n * 864e5).toISOString().slice(0, 10); }
  function diff(a, b) { return Math.round((day(b) - day(a)) / 864e5); }
  function ko(s) { var t = new Date(day(s)); return t.getUTCFullYear() + '년 ' + (t.getUTCMonth() + 1) + '월 ' + t.getUTCDate() + '일(' + '일월화수목금토'.charAt(t.getUTCDay()) + ')'; }
  function num(v) { var n = parseInt(String(v || '').replace(/[^0-9]/g, ''), 10); return n > 0 ? Math.min(n, 99999999) : 0; }
  function comma(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }

  /* One receipt: can its tax come back? r = {d: day bought, st: state, a: yen at 10%, b: yen at 8%}, dep = day of leaving Japan or ''. */
  function judge(r, dep) {
    if (!r.d || isNaN(day(r.d))) return { s: '', t: '산 날을 고르면 바로 알려 드려요.', p: [] };
    if (r.d < D.start) return { s: 'wn', t: '예전 방식이에요', p: ['2026년 10월 31일까지 산 것은 살 때 세금을 뺀 방식입니다. 이 화면은 11월 1일부터 산 것만 봅니다.'] };
    if (dep && diff(r.d, dep) < 0) return { s: 'wn', t: '날짜를 확인해 주세요', p: ['일본을 떠나는 날이 산 날보다 빠릅니다.'] };
    var by = add(r.d, 90);
    if (!r.st) return { s: '', t: '지금 상태를 골라 주세요.', p: ['마감은 ' + ko(by) + '입니다.'], by: by };
    if (r.st === 'ate') return { s: 'no', k: 'ate', t: '이 영수증은 전체가 안 돼요', p: ['음식·화장품·약을 조금이라도 먹거나 썼기 때문입니다. 단말기를 누르기 전에 세관 직원에게 말하세요. 다른 영수증은 받을 수 있습니다.'], by: by };
    if (r.st === 'gone') return { s: 'no', k: 'gone', t: '이 영수증은 전체가 안 돼요', p: ['영수증에 있는 것 중 하나라도 지금 없기 때문입니다. 단말기를 누르기 전에 세관 직원에게 말하세요. 다른 영수증은 받을 수 있습니다.'], by: by };
    if (dep && diff(dep, by) < 0) return { s: 'no', t: '90일이 지나서 안 돼요', p: ['마감이 ' + ko(by) + '이었습니다. 떠나는 날이 마감보다 늦습니다.'], by: by };
    var a = num(r.a), b = num(r.b), net = a / 1.1 + b / 1.08, late = r.d >= D.foodCut, out = { s: 'ok', t: '조건에 맞아요', by: by, p: [], tax: 0, sum: a + b };
    if (a + b > 0 && net < 5000 - 1e-6) return { s: 'wn', t: '5,000엔이 안 돼요', p: ['세금을 빼고 ' + comma(Math.floor(net)) + '엔입니다. 같은 가게에서 같은 날 산 것을 모두 더해 5,000엔부터입니다.'], by: by };
    out.tax = Math.floor(a * 10 / 110) + (late ? 0 : Math.floor(b * 8 / 108));
    out.p.push(dep ? (diff(dep, by) === 0 ? '떠나는 날 ' + ko(by) + '이 마감 날입니다.' : '마감 ' + ko(by) + '보다 먼저 떠나서 괜찮습니다.') : ko(by) + '까지 일본을 떠나면서 확인받으세요.');
    if (out.tax) out.p.push('돌려받을 세금 약 ' + comma(out.tax) + '엔');
    if (late && b) out.p.push('2027년 4월부터 식품 세율을 내리는 법안이 있어 식품은 계산하지 않았습니다(통과 전).');
    if (!r.g) out.p.push('가게에서 준 안내로 환급 등록도 하세요.');
    if (r.st === 'used') out.p.push('써 봤어도 가지고 나가면 됩니다. 상자와 라벨은 버리지 마세요.');
    if (a / 1.1 >= 1e6) out.p.push('세금 빼고 한 개 100만 엔 이상인 물건은 보증서나 감정서도 챙기세요.');
    return out;
  }

  var S = { port: '', dep: '', tr: false, rs: [{}], ck: {} };
  try { var o = JSON.parse(localStorage.getItem(KEY)); if (o && o.rs && o.rs.length) { S.port = P[o.port] ? o.port : ''; S.dep = o.dep || ''; S.tr = !!o.tr; S.rs = o.rs; S.ck = o.ck || {}; } } catch (e) {}
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }

  /* Receipts */
  var box = $('rs'), tpl = $('r-tpl');
  function drawReceipts() {
    box.textContent = '';
    S.rs.forEach(function (r, i) {
      var n = tpl.content.cloneNode(true), el = n.querySelector('.rc');
      el.dataset.i = i; el.querySelector('h3').textContent = '영수증 ' + (i + 1); el.querySelector('.x').hidden = S.rs.length < 2;
      el.querySelector('.x').setAttribute('aria-label', '영수증 ' + (i + 1) + ' 지우기');
      el.querySelector('[data-k=d]').value = r.d || ''; el.querySelector('[data-k=a]').value = r.a ? comma(num(r.a)) : ''; el.querySelector('[data-k=b]').value = r.b ? comma(num(r.b)) : '';
      el.querySelector('[data-k=g]').checked = !!r.g;
      el.querySelectorAll('input[type=radio]').forEach(function (x) { x.name = 'st' + i; x.checked = x.value === r.st; });
      box.append(n);
    });
    draw();
  }
  box.addEventListener('input', function (ev) {
    var el = ev.target.closest('.rc'), r = S.rs[+el.dataset.i], k = ev.target.dataset.k;
    if (ev.target.type === 'radio') r.st = ev.target.value; else if (k === 'g') r.g = ev.target.checked; else if (k) r[k] = k === 'd' ? ev.target.value : num(ev.target.value);
    draw();
  });
  box.addEventListener('focusout', function (ev) { var k = ev.target.dataset && ev.target.dataset.k; if (k === 'a' || k === 'b') { var n = num(ev.target.value); ev.target.value = n ? comma(n) : ''; } });
  box.addEventListener('click', function (ev) {
    var t = ev.target;
    if (t.classList.contains('x')) { S.rs.splice(+t.closest('.rc').dataset.i, 1); drawReceipts(); }
    if (t.classList.contains('td')) { ev.preventDefault(); var el = t.closest('.rc'), now = new Date(), v = new Date(now.getTime() - now.getTimezoneOffset() * 6e4).toISOString().slice(0, 10); el.querySelector('[data-k=d]').value = v; S.rs[+el.dataset.i].d = v; draw(); }
  });
  $('add').addEventListener('click', function () { S.rs.push({ d: S.rs[S.rs.length - 1].d || '' }); drawReceipts(); var l = box.lastElementChild; l.scrollIntoView({ block: 'start' }); count1('add'); });

  /* Airport steps, only what fits this trip. */
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function steps(js) {
    var p = P[S.port], sea = p && p[0].charAt(0) === 'S', vjw = !p || p[3], bad = {}, L = [], reg = 0;
    js.forEach(function (j, i) { if (j.k) bad[j.k] = 1; if (j.s === 'ok' && !S.rs[i].g) reg++; });
    var here = p ? p[1] + (p[2] ? ' ' + p[2] : '') : '출발 로비';
    if (vjw) L.push(['v', '전날까지: Visit Japan Web 등록 <small class="mut">(선택)</small>', '폰으로 하려면 여권과 상륙허가 정보를 미리 넣습니다. 안 해도 단말기로 하면 됩니다.', '<a class="btn g" href="' + D.vjw + '" target="_blank" rel="noopener" data-c="vjw">한국어 안내</a>']);
    L.push(['h', '면세품을 모두 가지고 ' + (sea ? '항구' : '공항') + '로', S.tr ? '국내선에서 갈아타면 면세품은 들고 타세요. 부쳤다면 국제선 ' + (sea ? '항구' : '공항') + '에서 짐을 한 번 찾은 뒤 합니다.' : '가방에 넣어도 됩니다. 아직 부치지만 마세요.']);
    if (bad.ate || bad.gone) L.push(['t', '단말기보다 먼저 세관 직원에게', '먹거나 쓴 것, 없는 것이 있다고 말합니다.', '<button class="btn" type="button" data-say="' + (bad.ate ? 'ate' : 'gone') + '">일본어로 보여 주기</button>', 1]);
    L.push(['k', esc(here) + '에서 여권 스캔', '면세 단말기(Tax Refund Kiosk)에 여권을 댑니다. 짐을 부치기 전입니다.' + (vjw && p ? '<br>폰으로 하려면 와이파이<br><code>' + esc(D.wifi) + '</code><br>비밀번호 <code>' + esc(D.pw) + '</code> 연결<br>→ Visit Japan Web → 환급 절차 → Confirm' : ''),
      '<a class="btn g" href="' + D.map + '" target="_blank" rel="noopener" data-c="map">공식 지도</a><button class="btn g" type="button" data-say="where">어디인지 묻기</button>' + (vjw && p ? '<button class="btn g" type="button" data-copy="' + esc(D.pw) + '">비밀번호 복사</button>' : '')]);
    L.push(['c', '초록이면 끝, 빨강이면 세관 검사', '빨강(폰에서는 Not Completed)이면 세관 검사장에서 물건을 보여 줍니다.', '<button class="btn g" type="button" data-say="all">전부 있다고 말하기</button>']);
    L.push(['b', sea ? '그다음 배 타러' : '그다음 짐 부치고 보안 검색', '확인받은 물건은 꼭 일본 밖으로 가지고 나갑니다.']);
    L.push(['m', '돈은 고른 방법으로 기다리기', '카드 등은 입금을 기다리면 끝입니다. 현금으로 고른 것만 그 업체의 현금 창구로 가세요. 환급은 세관에 묻지 않고 업체나 가게에 묻습니다.' + (reg ? '<br><b>환급 등록을 확인할 영수증 ' + reg + '장</b>' : '')]);
    L.push(['r', '한국에서: 800달러를 넘으면 신고', '술·담배·향수는 따로 한도가 있습니다. 스스로 신고하면 관세를 30% 깎아 줍니다.', '<a class="btn g" href="' + D.kcs + '" target="_blank" rel="noopener" data-c="kcs">관세청 안내</a>']);
    $('st').innerHTML = L.map(function (x) {
      return '<li class="' + (x[4] ? 'alert ' : '') + (S.ck[x[0]] ? 'done' : '') + '"><div class="sh"><button class="ck" type="button" data-ck="' + x[0] + '" aria-pressed="' + (S.ck[x[0]] ? 'true' : 'false') + '" aria-label="' + x[1].replace(/<[^>]+>/g, '') + ': 했어요"></button><div><strong>' + x[1] + '</strong><p>' + x[2] + '</p>' + (x[3] ? '<div class="mini">' + x[3] + '</div>' : '') + '</div></div></li>';
    }).join('');
    $('st-for').textContent = (p ? p[1] + '에서 떠날 때. ' : '위에서 공항을 고르면 층까지 나옵니다. ') + '끝난 것은 번호를 누르세요.';
  }

  function draw() {
    var js = S.rs.map(function (r) { return judge(r, S.dep); }), tax = 0, ok = 0, no = 0, amt = 0;
    js.forEach(function (j, i) {
      var el = box.children[i].querySelector('.res');
      el.className = 'res ' + j.s; el.innerHTML = '<b>' + (j.s === 'ok' ? '✓ ' : j.s === 'no' ? '✕ ' : '') + esc(j.t) + '</b>' + j.p.map(function (x) { return '<p>' + esc(x) + '</p>'; }).join('');
      if (j.s === 'ok') { ok++; tax += j.tax; if (j.sum) amt++; } if (j.s === 'no') no++;
    });
    var any = ok + no > 0;
    $('sum').hidden = $('bar').hidden = !any;
    if (any) {
      var head = tax ? '약 ' + comma(tax) + '엔' : ok ? '되는 영수증 ' + ok + '장' : '되는 영수증이 없어요';
      $('sum-b').textContent = head; $('bar-b').textContent = head;
      $('sum-p').textContent = '되는 영수증 ' + ok + '장, 안 되는 영수증 ' + no + '장' + (ok > amt ? '. 금액을 넣으면 돌려받을 세금도 나옵니다.' : '.');
      $('bar-s').textContent = tax ? '돌려받을 세금(수수료 빼기 전)' : '짐 부치기 전에 확인';
      count1('result');
    }
    $('ics').hidden = !S.dep || isNaN(day(S.dep));
    steps(js); save();
  }

  /* Trip */
  $('port').value = S.port; $('dep').value = S.dep; $('tr').checked = S.tr;
  $('port').addEventListener('change', function () { S.port = this.value; draw(); if (S.port) count1('port'); });
  $('dep').addEventListener('input', function () { S.dep = this.value; draw(); });
  $('tr').addEventListener('change', function () { S.tr = this.checked; draw(); });

  /* Show in Japanese */
  var dlg = $('dlg');
  function say(id) { var c = D.cards[id]; if (!c) return; $('dlg-ja').textContent = c[0]; $('dlg-ko').textContent = c[1]; if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', ''); count('card'); }
  $('dlg-x').addEventListener('click', function () { if (dlg.close) dlg.close(); else dlg.removeAttribute('open'); });
  document.addEventListener('click', function (ev) {
    var t = ev.target.closest('[data-say],[data-copy],[data-ck],[data-c]'); if (!t) return;
    if (t.dataset.say) say(t.dataset.say);
    if (t.dataset.c) count(t.dataset.c);
    if (t.dataset.copy) { var txt = t.dataset.copy; (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(function () { t.textContent = '✓ 복사됨'; }, function () { t.textContent = txt; }); }
    if (t.dataset.ck) { var k = t.dataset.ck; if (S.ck[k]) delete S.ck[k]; else { S.ck[k] = 1; count1('step'); } draw(); var b = document.querySelector('[data-ck="' + k + '"]'); b && b.focus(); }
  });

  /* Calendar file made on the phone. */
  function ics() {
    var p = P[S.port], d = S.dep.replace(/-/g, ''), n = add(S.dep, 1).replace(/-/g, ''), z = new Date().toISOString().replace(/[-:]/g, '').slice(0, 15) + 'Z';
    return ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//EasyModeKorea//JPR//KO', 'BEGIN:VEVENT', 'UID:jpr-' + d + '@easymodekorea.com', 'DTSTAMP:' + z, 'DTSTART;VALUE=DATE:' + d, 'DTEND;VALUE=DATE:' + n,
      'SUMMARY:일본 면세 환급: 짐 부치기 전에 세관 단말기', 'DESCRIPTION:' + (p ? p[1] + (p[2] ? ' ' + p[2] : '') + ' · ' : '') + '여권 스캔 → 초록이면 끝 · 빨강이면 세관 검사 · ' + D.url,
      'BEGIN:VALARM', 'ACTION:DISPLAY', 'DESCRIPTION:내일 일본 면세 환급', 'TRIGGER:-PT6H', 'END:VALARM', 'BEGIN:VALARM', 'ACTION:DISPLAY', 'DESCRIPTION:짐 부치기 전에 면세 단말기', 'TRIGGER:PT6H', 'END:VALARM', 'END:VEVENT', 'END:VCALENDAR', ''].join('\r\n');
  }
  $('ics').addEventListener('click', function () { var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([ics()], { type: 'text/calendar' })); a.download = 'japan-tax-refund.ics'; a.click(); count('ics'); });

  /* Share the page (never what was typed). */
  $('share').addEventListener('click', function () {
    var b = this; count('share');
    if (navigator.share) { navigator.share({ title: document.title, url: D.url }).catch(function () {}); return; }
    (navigator.clipboard ? navigator.clipboard.writeText(D.url) : Promise.reject()).then(function () { b.textContent = '✓ 주소 복사됨'; }, function () { b.textContent = D.url; });
  });
  $('wipe').addEventListener('click', function () { if (!confirm('이 폰에 저장된 영수증과 날짜를 지울까요?')) return; try { localStorage.removeItem(KEY); } catch (e) {} S = { port: '', dep: '', tr: false, rs: [{}], ck: {} }; $('port').value = ''; $('dep').value = ''; $('tr').checked = false; drawReceipts(); scrollTo(0, 0); });

  /* Works without data once opened. */
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').then(function () { return navigator.serviceWorker.ready; }).then(function () { $('off').hidden = false; }).catch(function () {});
  window.JPR = { judge: judge, ics: ics, state: function () { return S; } };
  drawReceipts();
})();
"""

SW = r"""/* Offline copy of one page, japan-tax-refund.html. Newest first: the rules are new, so a phone with data always gets the fresh page. */
const C='jpr-@V@',F='@F@';
const key=()=>new URL(F,self.registration.scope).href;
self.addEventListener('install',e=>e.waitUntil(caches.open(C).then(c=>c.add(new Request(key(),{cache:'reload'}))).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x.startsWith('jpr-')&&x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin+u.pathname!==key())return;
  e.respondWith((async()=>{const c=await caches.open(C),old=()=>c.match(key());
    const net=fetch(e.request).then(async r=>{if(r.ok)await c.put(key(),r.clone());return r});
    const slow=new Promise(r=>setTimeout(async()=>{const h=await old();if(h)r(h)},3000));
    try{return await Promise.race([net,slow])}catch(err){const h=await old();if(h)return h;throw err}})())});
"""


def e(s):
    return html.escape(s, quote=True)


def src(keys):
    return '<p class="src">' + ", ".join(f'<a href="{e(SRC[k][1])}" target="_blank" rel="noopener">{e(SRC[k][0])}</a>' for k in keys) + f' · <time datetime="{CHK}">{CHK}</time> 확인</p>'


def say(c):
    return f'<button class="say" type="button" data-say="{c[0]}"><span><b lang="ja">{e(c[1].replace(chr(10), " "))}</b><small>{e(c[2])}</small></span><i aria-hidden="true">⤢</i></button>'


def build(B):
    ports = AIR_TOP + AIR + SEA
    opt = lambda rows: "".join(f'<option value="{i}">{e(n)}</option>' for i, n, _f, _v in rows)
    trs = lambda rows: "".join(f"<tr><td>{e(n)}</td><td>{e(f or '지도에서 확인')}</td><td>{'됨' if v else '안 됨'}</td></tr>" for _i, n, f, v in rows)
    table = lambda cap, rows: f'<table><caption>{cap}</caption><thead><tr><th scope="col">어디</th><th scope="col">단말기</th><th scope="col">폰으로</th></tr></thead><tbody>{trs(rows)}</tbody></table>'
    data = {"ports": ports, "start": START, "foodCut": FOOD_CUT, "wifi": WIFI, "pw": WIFI_PW, "vjw": SRC["vjw"][1], "map": SRC["map"][1], "kcs": SRC["kcs"][1],
            "url": B.SITE + PATH, "cards": {c[0]: [c[1], c[2]] for c in CARDS_AIR + CARDS_SHOP}}
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": "일본 면세 환급 도우미", "url": B.SITE + PATH, "inLanguage": "ko", "applicationCategory": "TravelApplication", "operatingSystem": "Any", "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}},
        {"@type": "FAQPage", "inLanguage": "ko", "lastReviewed": CHK, "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a, _s in FAQ]}]}
    js = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
    title = "일본 면세 환급 도우미: 되는지, 언제까지, 공항 몇 층 (2026년 11월 새 제도)"
    desc = "영수증마다 환급이 되는지, 90일 마감이 언제인지, 나리타·간사이·후쿠오카 공항 단말기가 몇 층인지 바로 알려 줍니다. 일본 관광청·세관·국세청 안내 기준(2026-11-25 확인). 광고 없음."
    page = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#2336e8"><meta name="theme-color" media="(prefers-color-scheme: dark)" content="#4a59ee">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png"><link rel="apple-touch-icon" href="/icon-192.png">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{B.SITE}{PATH}">
<meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:title" content="일본 면세 환급, 내 영수증은 될까?"><meta property="og:description" content="되는지, 언제까지인지, 공항 몇 층인지 바로 확인"><meta property="og:url" content="{B.SITE}{PATH}"><meta property="og:image" content="{B.SITE}ko/og-japan-tax-refund.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<style>{CSS.strip()}</style>
<script type="application/ld+json">{js(ld)}</script>
<script data-goatcounter="{B.GOAT}" async src="//gc.zgo.at/count.js"></script>
</head>
<body>
<header class="hd"><div class="w"><p class="by"><b>EasyModeKorea</b>광고·제휴 없음</p>
<h1>일본 면세 환급, 내 영수증은 될까?</h1>
<p class="lede">11월 1일부터는 세금을 내고 산 뒤, 출국할 때 <b>짐 부치기 전에</b> 확인받고 돌려받습니다.</p>
<p class="chk">일본 관광청·세관·국세청 안내를 <time datetime="{CHK}">2026년 11월 25일</time>에 확인</p></div></header>
<nav class="jump" aria-label="바로 가기"><div class="w"><a href="#mine">내 영수증</a><a href="#airport">공항 순서</a><a href="#say">일본어 카드</a><a href="#shop">살 때</a><a href="#faq">자주 묻는 것</a><a href="#where">공항별 위치</a></div></nav>
<main class="w">
<section id="mine" aria-labelledby="h-mine"><h2 id="h-mine">내 영수증 확인</h2>
<div class="card"><label class="f"><span>어디서 일본을 떠나나요?</span><select id="port"><option value="">공항이나 항구 고르기</option><optgroup label="많이 가는 공항">{opt(AIR_TOP)}</optgroup><optgroup label="다른 공항">{opt(AIR)}</optgroup><optgroup label="배(페리·크루즈)">{opt(SEA)}</optgroup></select></label>
<label class="f"><span>일본을 떠나는 날</span><input type="date" id="dep" min="{START}"></label>
<label class="tg"><input type="checkbox" id="tr"><span>일본 국내선을 타고 와서 갈아타요</span></label></div>
<p class="mut">면세(Tax-free) 가게에서 여권을 보여 주고 산 영수증만 넣으세요.</p>
<div id="rs"></div>
<template id="r-tpl"><div class="card rc"><div class="rh"><h3>영수증</h3><button class="x" type="button">지우기</button></div>
<label class="f"><span>산 날</span><span class="dt"><input type="date" data-k="d"><button class="btn g td" type="button">오늘</button></span></label>
<fieldset><legend class="leg">지금 상태</legend><div class="ch">
<label><input type="radio" value="all"><span>전부 그대로 있어요</span></label>
<label><input type="radio" value="used"><span>옷·신발·가전을 써 봤어요<small>전부 가지고는 있어요</small></span></label>
<label><input type="radio" value="ate"><span>먹거나 바른 것이 있어요<small>음식·화장품·약</small></span></label>
<label><input type="radio" value="gone"><span>하나라도 지금 없어요<small>버림·선물·택배로 보냄</small></span></label></div></fieldset>
<p class="leg">금액 <small>세금 포함, 안 넣어도 됩니다</small></p>
<div class="two"><label class="f"><span><small>일반·술 10% (엔)</small></span><input type="text" inputmode="numeric" autocomplete="off" data-k="a" placeholder="0"></label><label class="f"><span><small>식품·음료 8% (엔)</small></span><input type="text" inputmode="numeric" autocomplete="off" data-k="b" placeholder="0"></label></div>
<label class="tg"><input type="checkbox" data-k="g"><span>이 가게 환급 등록을 했어요</span></label>
<div class="res" aria-live="polite"></div></div></template>
<button class="btn g full" type="button" id="add">+ 영수증 더하기</button>
<div class="sum" id="sum" hidden style="margin-top:14px"><p class="mut">돌려받을 세금</p><b id="sum-b"></b><p id="sum-p"></p><p class="mut">세율로 계산한 어림값이고 수수료를 빼기 전입니다. 되는지는 일본 세관이 정합니다.</p></div>
</section>
<section id="airport" aria-labelledby="h-air"><h2 id="h-air">공항에서 이 순서대로</h2><p class="mut" id="st-for"></p><ol class="st" id="st"></ol>
<div class="acts"><button class="btn full" type="button" id="ics" hidden>떠나는 날 달력에 넣기</button><button class="btn g full" type="button" id="share">같이 가는 사람에게 보내기</button></div>
<p class="mut" id="off" hidden>✓ 이 화면은 인터넷이 없어도 다시 열립니다.</p>{src(["cus", "nta_kr", "map", "wifi", "vjw", "kcs"])}</section>
<section id="say" aria-labelledby="h-say"><h2 id="h-say">일본어로 보여 주기</h2><p class="mut">누르면 크게 나옵니다. 공항에서</p>{''.join(say(c) for c in CARDS_AIR)}<p class="mut">가게에서</p>{''.join(say(c) for c in CARDS_SHOP)}</section>
<section id="shop" aria-labelledby="h-shop"><h2 id="h-shop">살 때 이것만</h2><ul class="tips">{''.join(f'<li><b>{e(t)}</b>{e(x)}</li>' for t, x, k in TIPS)}</ul>{src(list(dict.fromkeys(k for _t, _x, k in TIPS)))}</section>
<section id="faq" aria-labelledby="h-faq"><h2 id="h-faq">자주 묻는 것</h2>{''.join(f'<details><summary>{e(q)}</summary><div><p>{e(a)}</p>{src(s)}</div></details>' for q, a, s in FAQ)}</section>
<section id="where" aria-labelledby="h-where"><h2 id="h-where">공항별 면세 단말기 위치</h2><p class="mut">모두 짐을 부치기 전 출발 로비에 있습니다.</p>
<details open><summary>많이 가는 공항</summary><div>{table("터미널과 층", AIR_TOP)}</div></details><details><summary>다른 공항 {len(AIR)}곳</summary><div>{table("공항과 층", AIR)}</div></details><details><summary>배 타는 곳 {len(SEA)}곳</summary><div>{table("항구와 층", SEA)}<p class="mut">여기 없는 항구는 아래 공식 지도에서 봅니다. 단말기를 늘 두지 않는 항구도 있습니다.</p></div></details>{src(["map"])}</section>
<footer><p>이 화면은 공식 안내를 옮겨 계산해 주는 도우미이고, 일본 정부나 환급 회사와 관계가 없습니다. 환급 회사·카드·수수료는 비교하지 않습니다.</p>
<p>세율 10%·8%: <a href="{e(SRC['rate'][1])}" target="_blank" rel="noopener">{e(SRC['rate'][0])}</a> · 식품 세율 인하 예정: <a href="{e(SRC['food'][1])}" target="_blank" rel="noopener">{e(SRC['food'][0])}</a></p>
<p>입력한 내용은 이 폰에만 저장되고 보내지 않습니다. 방문 수와 버튼 누른 수만 셉니다(쿠키 없음).</p>
<p><button class="x" type="button" id="wipe">입력한 것 지우기</button></p><p><a href="../contact.html">틀린 곳 알려 주기(영어 화면, 한국어로 써도 됩니다)</a></p></footer>
</main>
<div class="bar" id="bar" hidden><div class="w"><div><b id="bar-b"></b><small id="bar-s"></small></div><a class="btn" href="#airport">공항 순서</a></div></div>
<dialog id="dlg" aria-labelledby="dlg-ko"><div class="dl"><p class="big" id="dlg-ja" lang="ja"></p><div><p class="m" id="dlg-ko"></p><button class="btn full" type="button" id="dlg-x">닫기</button></div></div></dialog>
<script type="application/json" id="jpr-data">{js(data)}</script>
<script>{JS.strip()}</script>
</body>
</html>
"""
    B.write(PATH, page)
    ver = hashlib.sha256((page + SW).encode()).hexdigest()[:8]
    B.write("ko/sw.js", SW.replace("@V@", ver).replace("@F@", SLUG + ".html"))
    return PATH
