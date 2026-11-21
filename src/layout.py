"""Short-first layout content: home situation cards, the at-a-glance answer box on each guide,
and Korean names a visitor can copy. Long text stays in data.py and deep*.py; this file only
holds the short layer that sits on top of it.

AT rows are [label key, text, ISO date the fact was last checked]. Keep each under ~12 words.
COPY entries are [Korean text, {lang: what it is}].
Text for each language sits next to the English; zh-cn is converted from zh-tw at import.
"""
from t2s import t2s

UI = {
    "en": {"where": "Where", "cost": "Cost", "time": "Time", "note": "Good to know",
           "stamp": "Checked {date} · {src}", "say_h": "Show this to staff", "full": "Show full screen",
           "copy": "Copy", "copied": "Copied", "names_h": "Korean names to copy",
           "all": "All guides", "intro_h": "About this answer",
           "addr_h": "Your stay's address in Korean", "addr_ph": "Paste the Korean address from your booking", "addr_save": "Save on this phone", "addr_note": "🔒 Only on this phone", "src_short": "Source", "addr_edit": "Change",
           "cards_h": "What do you need right now?", "tool_h": "What works with your phone setup?",
           "offline": "Pages you open keep working offline. Add this site to your home screen for the trip.",
           "lede": "Short answers for visitors in Korea, each checked against an official source, with Korean you can show or copy."},
}

# Guides that show the saved stay address (taxi rides, deliveries, bag delivery, directions, emergencies).
ADDR_GUIDES = {"taxi", "airport", "gimpo", "delivery", "luggage", "maps", "health", "busan", "jeju"}

# Home page: situations a visitor is in, each linking to the guides that answer it.
CARDS = [
    ("landed", "entry", ["entry", "airport", "gimpo", "power"],
     {"en": ["Just landed", "Entry forms, getting from the airport into the city, plugs."]}),
    ("move", "transit", ["transit", "maps", "taxi", "ktx", "transitpass"],
     {"en": ["Getting around", "Subway and bus, maps that work, taxis, trains."]}),
    ("pay", "cash", ["cash", "transit", "transitpass"],
     {"en": ["Paying and cash", "ATMs that take foreign cards, topping up T-money."]}),
    ("phone", "data", ["data", "translate", "maps"],
     {"en": ["Phone and internet", "eSIM or SIM, Korean SMS codes, translation."]}),
    ("eat", "food-booking", ["food-booking", "delivery", "translate"],
     {"en": ["Eating", "Restaurant bookings and waitlists, food delivery."]}),
    ("shop", "shopping", ["shopping", "luggage"],
     {"en": ["Shopping and tax refund", "Tax-free at the till, storing or sending bags."]}),
    ("sick", "health", ["health"],
     {"en": ["Sick or hurt", "Who to call, pharmacies, hospitals with English."]}),
    ("trips", "busan", ["busan", "jeju", "dmz", "krpass", "ktx"],
     {"en": ["Day trips", "Busan, Jeju, the DMZ, rail passes."]}),
]

D17, D20 = "2026-11-17", "2026-11-20"

AT = {
    "entry": [["where", {"en": "Official sites only: k-eta.go.kr and e-arrivalcard.go.kr"}, D20],
              ["cost", {"en": "K-ETA 10,000 won. The e-Arrival Card is free."}, D20],
              ["time", {"en": "e-Arrival Card: within 72 hours before you land"}, D20]],
    "data": [["where", {"en": "eSIM online before you fly, or a telecom counter at the airport"}, D17],
             ["note", {"en": "A data-only eSIM can't receive Korean SMS codes"}, D17]],
    "airport": [["where", {"en": "AREX train from the arrivals floor; follow the Train signs"}, D17],
                ["time", {"en": "AREX Express: about 43 min (T1) or 51 min (T2) to Seoul Station"}, D17],
                ["cost", {"en": "Fares change; check arex.or.kr"}, D17]],
    "gimpo": [["where", {"en": "Gimpo Airport station, a short walk from both terminals"}, D20],
              ["time", {"en": "AREX to Seoul Station: about 20 to 25 min"}, D20],
              ["note", {"en": "T-money works on AREX, Line 5 and Line 9"}, D20]],
    "power": [["note", {"en": "Type C and F sockets, 220 V, 60 Hz"}, D17],
              ["where", {"en": "Bring a Type C adapter; shops in Korea sell them too"}, D17]],
    "transit": [["where", {"en": "Buy T-money at convenience stores; top up with cash at stations"}, D17],
                ["cost", {"en": "Subway from 1,550 won by card"}, D20],
                ["note", {"en": "Refunding a small balance at a store costs 500 won"}, D20]],
    "transitpass": [["note", {"en": "1, 2, 3, 5 and 7-day passes are still sold"}, D17],
                    ["cost", {"en": "Prices vary by source; check Seoul's or T-money's page"}, D17]],
    "maps": [["where", {"en": "Naver Map app, in English, Japanese or Chinese"}, D17],
             ["cost", {"en": "Free"}, D17]],
    "taxi": [["where", {"en": "k.ride or Uber app, or a taxi rank"}, D17],
             ["cost", {"en": "Seoul: from 4,800 won, plus 20% from 22:00 to 04:00 and 40% from 23:00 to 02:00"}, D20]],
    "ktx": [["where", {"en": "KORAIL's English website, with a foreign card"}, D17],
            ["time", {"en": "Seoul to Busan: about 2.5 hours on the fastest trains"}, D17],
            ["note", {"en": "Since 1 Sep 2026, all high-speed trains are sold as KTX"}, D17]],
    "busan": [["time", {"en": "KTX Seoul to Busan: about 2.5 hours"}, D17],
              ["note", {"en": "K-Tour Pass pilot runs until 31 Dec 2026"}, D17]],
    "krpass": [["note", {"en": "Covers KORAIL trains, not AREX or the subway"}, D17],
               ["where", {"en": "You still book each seat after buying the pass"}, D17]],
    "dmz": [["where", {"en": "Guided tours only, booked in advance"}, D17],
            ["note", {"en": "Bring your physical passport on the day"}, D17]],
    "jeju": [["note", {"en": "A rental car needs an International Driving Permit"}, D17],
             ["where", {"en": "Most visitors fly in from Gimpo or Busan"}, D17]],
    "food-booking": [["where", {"en": "CatchTable Global app, or Naver with passport check"}, D17],
                     ["note", {"en": "Each restaurant sets its own deposit and cancellation rules"}, D20]],
    "delivery": [["where", {"en": "Baemin app, in English"}, D17],
                 ["note", {"en": "Takes a foreign phone number and foreign cards in Apple Pay"}, D17]],
    "translate": [["where", {"en": "Papago app: camera mode for menus and signs"}, D17],
                  ["cost", {"en": "Free"}, D17]],
    "shopping": [["where", {"en": "Stores with a TAX FREE sign; show your passport at the till"}, D17],
                 ["cost", {"en": "Purchases from 15,000 won qualify"}, D20]],
    "luggage": [["where", {"en": "Station lockers and staffed luggage counters"}, D17],
                ["cost", {"en": "Set by size and hours; shown on the locker screen and in the T-Locker app"}, D20]],
    "health": [["where", {"en": "Call 119 (ambulance, medical advice, nearest ER). 1330 interprets."}, D20],
               ["cost", {"en": "Calling 119 is free"}, D17],
               ["note", {"en": "Pharmacies have a 약 sign"}, D17]],
    "cash": [["where", {"en": "ATMs marked Global, and convenience stores such as CU, GS25, 7-Eleven"}, D17],
             ["cost", {"en": "A machine fee plus your bank's fee. Choose KRW, not your currency."}, D17]],
}

COPY = {
    "airport": [["인천국제공항 제1여객터미널", {"en": "Incheon Airport Terminal 1"}], ["인천국제공항 제2여객터미널", {"en": "Incheon Airport Terminal 2"}], ["서울역", {"en": "Seoul Station"}]],
    "gimpo": [["김포공항역", {"en": "Gimpo Airport station"}], ["김포공항 국제선", {"en": "Gimpo international terminal"}]],
    "taxi": [["택시 승차장", {"en": "Taxi rank"}]],
    "transit": [["티머니", {"en": "T-money"}], ["교통카드 충전", {"en": "Transit card top-up"}]],
    "transitpass": [["기후동행카드", {"en": "Climate Card"}]],
    "maps": [["네이버 지도", {"en": "Naver Map"}]],
    "entry": [["전자도착카드", {"en": "e-Arrival Card"}]],
    "data": [["유심", {"en": "SIM card"}], ["데이터 로밍", {"en": "Data roaming"}]],
    "cash": [["글로벌 ATM", {"en": "Global ATM"}], ["환전소", {"en": "Currency exchange"}]],
    "power": [["여행용 어댑터", {"en": "Travel plug adapter"}]],
    "ktx": [["서울역", {"en": "Seoul Station"}], ["부산역", {"en": "Busan Station"}]],
    "busan": [["부산역", {"en": "Busan Station"}], ["해운대", {"en": "Haeundae"}]],
    "krpass": [["코레일", {"en": "KORAIL"}]],
    "dmz": [["임진각", {"en": "Imjingak"}], ["판문점", {"en": "Panmunjom (JSA)"}]],
    "jeju": [["제주국제공항", {"en": "Jeju Airport"}], ["국제운전면허증", {"en": "International Driving Permit"}]],
    "food-booking": [["캐치테이블", {"en": "CatchTable"}], ["웨이팅", {"en": "Waitlist"}]],
    "delivery": [["배달의민족", {"en": "Baemin"}]],
    "translate": [["파파고", {"en": "Papago"}]],
    "shopping": [["택스 리펀드", {"en": "Tax refund"}], ["올리브영", {"en": "Olive Young"}]],
    "luggage": [["물품보관함", {"en": "Lockers"}], ["짐 보관", {"en": "Luggage storage"}]],
    "health": [["약국", {"en": "Pharmacy"}], ["응급실", {"en": "Emergency room"}]],
}

try:
    import layout_i18n  # noqa: F401  (ja, zh-tw, vi text, added after the English layout settled)
except ImportError:
    pass


def _cn(m):
    if "zh-tw" in m and "zh-cn" not in m: m["zh-cn"] = t2s(m["zh-tw"])


if "zh-tw" in UI: UI["zh-cn"] = {k: t2s(v) for k, v in UI["zh-tw"].items()}
for _, _, _, m in CARDS:
    if "zh-tw" in m: m["zh-cn"] = [t2s(s) for s in m["zh-tw"]]
for rows in AT.values():
    for r in rows: _cn(r[1])
for rows in COPY.values():
    for r in rows: _cn(r[1])


def tx(m, lang):
    """Text for lang, falling back to English (the build warns when it falls back)."""
    if lang in m: return m[lang]
    MISSING.add(lang)
    return m["en"]


MISSING = set()
