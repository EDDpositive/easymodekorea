"""EasyModeKorea: hero, trust, phrase cards, first-24-hours, changelog and host-stay strings.
Facts here follow data.py's sources. The changelog is the public record of what we updated.
"""

BRAND = "EasyModeKorea"

X = {
    "en": {
        "hook": "Korea's apps on Hard Mode? Switch to Easy Mode.",
        "lede": "Most Korean apps ask for a Korean phone number. Pick your setup once, and every answer here shows what works for you, with the date we last checked it.",
        "trust": "Made in Seoul. Every answer is checked against official notices and traveler reports, and every check is dated. No app pays to be listed.",
        "glance": "At a glance",
        "staff": "Show this to staff", "means": "Means",
        "others": "Show answers for other setups",
        "your_mode": "Your setup",
        "change_mode": "Change",
        "nav_first": "First 24 hours", "nav_changes": "What changed",
        "first_title": "Your first 24 hours in Korea, in order",
        "first_lead": "The trip goes wrong in the first few hours: at the airport, in the taxi, at check-in. Do these in order.",
        "first": [
            ["Before you fly", "Submit the e-Arrival Card online in the 3 days before you land (e-arrivalcard.go.kr). Check whether your nationality needs a K-ETA (k-eta.go.kr)."],
            ["Before you fly", "Install the apps on your checklist and set them up on home Wi-Fi."],
            ["On landing", "Switch on your eSIM data before you leave the plane, so maps and messages work at immigration."],
            ["At the airport", "Buy a T-money card at an airport convenience store and top it up with cash. On iPhone, Mobile T-money is an option."],
            ["Into the city", "Take the airport railroad (AREX) or an airport bus, or call a taxi with k.ride or Uber."],
            ["At your stay", "Show your host's address card to the driver. If your host sent you a link, it's at the top of this page."],
            ["First evening", "Verify Naver with your passport and set up CatchTable Global, so dinner bookings work."],
        ],
        "changes_title": "What changed in 2026",
        "changes_lead": "Korean apps change often, and old guides don't update. This is our public log of changes we've applied.",
        "changes": [
            ["2026-10-01", "KTX tickets now open two months ahead."],
            ["2026-09-01", "SRT was folded into KORAIL. All high-speed trains are now sold as KTX."],
            ["2026-08", "The KORAIL+ app replaced Korail Talk."],
            ["2026-07", "Baemin: visitors can order with a foreign phone number. Seoul added delivery zones at Han River parks."],
            ["2026-06-02", "Baemin: Apple Pay now accepts foreign cards."],
            ["2026-06-04", "Naver added passport verification, so visitors can book and pay on Naver Map."],
            ["2026-03", "Mobile T-money on iPhone started accepting some foreign cards for top-up."],
            ["2026-02-03", "Baemin added English, Japanese and Chinese."],
            ["2026-02", "The government conditionally approved Google's map-data export. Better Google routing is not confirmed yet."],
        ],
        "stay_title": "Your stay", "stay_from": "Prepared by {h}",
        "taxi_card": "Show this to your taxi driver", "taxi_ko": "기사님, 이 주소로 가 주세요.", "taxi_means": "Please take me to this address.",
        "deliv_card": "Your delivery address", "deliv_ko": "문 앞에 두고 가 주세요.", "deliv_means": "Please leave it at the door.",
        "station": "Nearest station", "checkin": "Check-in", "contact": "Contact your host", "note": "Note from your host",
        "map": "Open in Naver Map",
    },
    "ja": {
        "hook": "韓国のアプリはハードモード? イージーモードに切り替えよう。",
        "lede": "韓国のアプリの多くは韓国の電話番号を求めます。状況を一度選ぶだけで、このサイトのすべての回答があなた向けになり、最後に確認した日付もわかります。",
        "trust": "ソウルで制作。各回答は公式発表と旅行者の報告で確認し、確認日を記録しています。掲載料は受け取っていません。",
        "glance": "ひと目で",
        "staff": "スタッフに見せる", "means": "意味",
        "others": "ほかの状況の回答を見る",
        "your_mode": "あなたの状況", "change_mode": "変更",
        "nav_first": "最初の24時間", "nav_changes": "変更履歴",
        "first_title": "韓国での最初の24時間、この順番で",
        "first_lead": "旅のつまずきは最初の数時間に集中します。空港、タクシー、チェックイン。この順番で進めましょう。",
        "first": [
            ["出発前", "到着前3日以内にe-Arrival Cardをオンラインで提出(e-arrivalcard.go.kr)。自分の国籍にK-ETAが必要か確認(k-eta.go.kr)。"],
            ["出発前", "チェックリストのアプリを入れ、自宅のWi-Fiで設定しておく。"],
            ["着陸したら", "機内でeSIMのデータをオンにして、入国審査のときから地図やメッセージを使えるようにする。"],
            ["空港で", "空港のコンビニでT-moneyカードを買い、現金でチャージ。iPhoneならモバイルT-moneyも使えます。"],
            ["市内へ", "空港鉄道(AREX)か空港バスに乗るか、k.ride・Uberでタクシーを呼ぶ。"],
            ["宿に着いたら", "宿の住所カードを運転手に見せる。宿からリンクが届いていれば、このページの一番上にあります。"],
            ["最初の夜", "Naverをパスポートで認証し、CatchTable Globalを設定して夕食の予約に備える。"],
        ],
        "changes_title": "2026年の変更点",
        "changes_lead": "韓国のアプリはよく変わり、古いガイドは更新されません。私たちが反映した変更を公開しています。",
        "changes": [
            ["2026-10-01", "KTXの予約が2か月前から可能に。"],
            ["2026-09-01", "SRTがKORAILに統合され、高速列車はすべてKTXとして販売。"],
            ["2026-08", "KORAIL+アプリがKorail Talkに代わる。"],
            ["2026-07", "Baemin: 海外の電話番号で注文可能に。ソウル市は漢江公園に配達ゾーンを案内。"],
            ["2026-06-02", "Baemin: Apple Payで海外カードが使えるように。"],
            ["2026-06-04", "Naverがパスポート認証を導入し、旅行者もNaver Mapで予約・決済が可能に。"],
            ["2026-03", "iPhoneのモバイルT-moneyで一部の海外カードからチャージが可能に。"],
            ["2026-02-03", "Baeminが英語・日本語・中国語に対応。"],
            ["2026-02", "政府がGoogleの地図データ持ち出しを条件付きで承認。経路案内の改善は未確認。"],
        ],
        "stay_title": "あなたの宿", "stay_from": "{h}より",
        "taxi_card": "タクシーの運転手に見せる", "taxi_ko": "기사님, 이 주소로 가 주세요.", "taxi_means": "この住所までお願いします。",
        "deliv_card": "デリバリーの届け先", "deliv_ko": "문 앞에 두고 가 주세요.", "deliv_means": "ドアの前に置いてください。",
        "station": "最寄り駅", "checkin": "チェックイン", "contact": "宿への連絡", "note": "宿からのメモ",
        "map": "Naver Mapで開く",
    },
    "zh-tw": {
        "hook": "韓國App是困難模式?切換成簡單模式。",
        "lede": "大多數韓國App都要韓國電話號碼。選一次你的狀況,這裡每個答案都會顯示你能用的方法,還有我們最後確認的日期。",
        "trust": "在首爾製作。每個答案都對照官方公告與旅客回報確認,並標示確認日期。我們不收任何App的上架費。",
        "glance": "一眼看懂",
        "staff": "給店員看", "means": "意思",
        "others": "查看其他狀況的答案",
        "your_mode": "你的狀況", "change_mode": "更改",
        "nav_first": "最初24小時", "nav_changes": "更新紀錄",
        "first_title": "到韓國的最初24小時,照這個順序",
        "first_lead": "旅行最容易卡關的就是剛到的幾小時:機場、計程車、入住。照這個順序做。",
        "first": [
            ["出發前", "在抵達前3天內線上填寫e-Arrival Card(e-arrivalcard.go.kr)。確認你的國籍是否需要K-ETA(k-eta.go.kr)。"],
            ["出發前", "安裝清單上的App,在家裡的Wi-Fi先設定好。"],
            ["降落時", "下飛機前先開啟eSIM上網,入境時就能用地圖和訊息。"],
            ["在機場", "在機場便利商店買T-money卡,用現金儲值。iPhone也可以用Mobile T-money。"],
            ["進市區", "搭機場鐵路(AREX)或機場巴士,或用k.ride、Uber叫計程車。"],
            ["到住宿", "把住宿地址卡給司機看。如果房東傳了連結給你,就在這一頁最上方。"],
            ["第一晚", "用護照完成Naver認證,設定CatchTable Global,晚餐就能訂位。"],
        ],
        "changes_title": "2026年的變動",
        "changes_lead": "韓國App常常變,舊指南卻不會更新。這是我們已反映的變動公開紀錄。",
        "changes": [
            ["2026-10-01", "KTX改為提前兩個月開放訂票。"],
            ["2026-09-01", "SRT併入KORAIL,所有高鐵列車都以KTX名義販售。"],
            ["2026-08", "KORAIL+ App取代Korail Talk。"],
            ["2026-07", "Baemin:可用國外電話號碼下單。首爾市在漢江公園設外送區。"],
            ["2026-06-02", "Baemin:Apple Pay開始接受國外卡。"],
            ["2026-06-04", "Naver推出護照認證,旅客也能在Naver Map訂位和付款。"],
            ["2026-03", "iPhone的Mobile T-money開始接受部分國外信用卡儲值。"],
            ["2026-02-03", "Baemin支援英文、日文和中文。"],
            ["2026-02", "政府有條件批准Google地圖資料出口,導航是否改善尚未確認。"],
        ],
        "stay_title": "你的住宿", "stay_from": "由 {h} 提供",
        "taxi_card": "給計程車司機看", "taxi_ko": "기사님, 이 주소로 가 주세요.", "taxi_means": "請載我到這個地址。",
        "deliv_card": "外送地址", "deliv_ko": "문 앞에 두고 가 주세요.", "deliv_means": "請放在門口。",
        "station": "最近的車站", "checkin": "入住時間", "contact": "聯絡房東", "note": "房東的話",
        "map": "用Naver Map開啟",
    },
}

# Phrase cards: Korean sentence to show staff, and what it means in each language.
PHRASES = {
    "data": [["와이파이 비밀번호가 뭐예요?", {"en": "What's the Wi-Fi password?", "ja": "Wi-Fiのパスワードは何ですか?", "zh-tw": "Wi-Fi密碼是什麼?"}]],
    "maps": [["여기 어떻게 가요?", {"en": "How do I get here? (show the map)", "ja": "ここへはどう行けばいいですか?(地図を見せる)", "zh-tw": "這裡要怎麼去?(給對方看地圖)"}]],
    "taxi": [["기사님, 이 주소로 가 주세요.", {"en": "Please take me to this address.", "ja": "この住所までお願いします。", "zh-tw": "請載我到這個地址。"}],
             ["기사님께 직접 결제할게요.", {"en": "I'll pay you directly.", "ja": "運転手さんに直接払います。", "zh-tw": "我直接付給司機。"}]],
    "transit": [["티머니 충전해 주세요. 만 원이요.", {"en": "Please top up my T-money. 10,000 won.", "ja": "T-moneyをチャージしてください。1万ウォンです。", "zh-tw": "請幫我儲值T-money,一萬韓元。"}]],
    "ktx": [["이 표 몇 번 타는 곳이에요?", {"en": "Which platform is this ticket for?", "ja": "この切符は何番乗り場ですか?", "zh-tw": "這張票在第幾月台搭車?"}]],
    "food-booking": [["한국 번호가 없는데 대기 명단에 올려 주실 수 있나요?", {"en": "I don't have a Korean number. Could you add me to the waitlist?", "ja": "韓国の番号がないのですが、順番待ちに入れてもらえますか?", "zh-tw": "我沒有韓國號碼,可以幫我登記候位嗎?"}]],
    "delivery": [["배달 주문 좀 도와주실 수 있나요?", {"en": "Could you help me order delivery? (for your host or front desk)", "ja": "デリバリーの注文を手伝ってもらえますか?(宿やフロントに)", "zh-tw": "可以幫我叫外送嗎?(請房東或櫃台幫忙)"}]],
    "airport": [["공항철도 타는 곳이 어디예요?", {"en": "Where do I catch the airport train (AREX)?", "ja": "空港鉄道の乗り場はどこですか?", "zh-tw": "機場鐵路在哪裡搭?"}]],
    "shopping": [["택스 프리 해 주세요. 한 번에 계산할게요.", {"en": "Tax free, please. I'll pay for everything at once.", "ja": "免税でお願いします。まとめて会計します。", "zh-tw": "麻煩幫我退稅,我一次結帳。"}]],
    "luggage": [["여기 짐 맡길 수 있어요?", {"en": "Can I leave my luggage here?", "ja": "ここに荷物を預けられますか?", "zh-tw": "這裡可以寄放行李嗎?"}]],
    "health": [["열이 나요. 약 있어요?", {"en": "I have a fever. Do you have medicine for it?", "ja": "熱があります。薬はありますか?", "zh-tw": "我發燒了,有藥嗎?"}]],
    "translate": [["영어 메뉴 있어요?", {"en": "Do you have an English menu?", "ja": "英語のメニューはありますか?", "zh-tw": "有英文菜單嗎?"}]],
}

# Short tile labels, short setup labels and section labels for the compact layout.
SHORT = {
    "en": {"tasks": {"data": "Phone & data", "airport": "Airport to city", "maps": "Maps", "taxi": "Taxi", "transit": "Subway & bus", "ktx": "KTX trains", "food-booking": "Restaurant booking", "delivery": "Food delivery", "translate": "Translation", "shopping": "Shopping & tax refund", "luggage": "Luggage", "health": "Sick or hurt"},
           "prof": {"visitor": "No Korean number", "krsim": "Korean SIM (010)", "arc": "Resident (ARC)"},
           "show": "Show staff", "show_driver": "Show driver", "close": "Close", "guide": "Full guide",
           "tap": "Tap any row to see how", "before": "Before you fly", "details": "Sources and notes", "setup_q": "Your setup"},
    "ja": {"tasks": {"data": "電話・データ", "airport": "空港から市内", "maps": "地図", "taxi": "タクシー", "transit": "地下鉄・バス", "ktx": "KTX", "food-booking": "飲食店の予約", "delivery": "デリバリー", "translate": "翻訳", "shopping": "買い物と免税", "luggage": "荷物の預け", "health": "病気・けが"},
           "prof": {"visitor": "韓国の番号なし", "krsim": "韓国SIM(010)", "arc": "在住(登録証あり)"},
           "show": "スタッフに見せる", "show_driver": "運転手に見せる", "close": "閉じる", "guide": "詳しいガイド",
           "tap": "項目をタップすると方法が出ます", "before": "出発前", "details": "出典とメモ", "setup_q": "あなたの状況"},
    "zh-tw": {"tasks": {"data": "電話與上網", "airport": "機場到市區", "maps": "地圖", "taxi": "計程車", "transit": "地鐵與公車", "ktx": "KTX火車", "food-booking": "餐廳訂位", "delivery": "叫外送", "translate": "翻譯", "shopping": "購物與退稅", "luggage": "寄放行李", "health": "生病或受傷"},
              "prof": {"visitor": "沒有韓國號碼", "krsim": "韓國SIM(010)", "arc": "居民(有登錄證)"},
              "show": "給店員看", "show_driver": "給司機看", "close": "關閉", "guide": "完整指南",
              "tap": "點一下就能看做法", "before": "出發前", "details": "資料來源與備註", "setup_q": "你的狀況"},
}

# Simple 24px line icons (stroke uses currentColor).
ICONS = {
    "data": '<rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M10.5 18.5h3"/>',
    "maps": '<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
    "taxi": '<path d="M4 16v-3.5L6 8h12l2 4.5V16"/><path d="M3.5 16h17v2.5h-17z"/><circle cx="7.5" cy="18.5" r="1.4"/><circle cx="16.5" cy="18.5" r="1.4"/><path d="M10 5.5h4"/>',
    "transit": '<rect x="5" y="3" width="14" height="14" rx="3"/><path d="M5 11h14"/><circle cx="8.5" cy="14" r="1"/><circle cx="15.5" cy="14" r="1"/><path d="M8 20l2-3M16 20l-2-3"/>',
    "ktx": '<path d="M5 15V9a5 5 0 0 1 5-5h4a5 5 0 0 1 5 5v6a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2z"/><path d="M5 11h14"/><path d="M8 21l2-4M16 21l-2-4"/>',
    "food-booking": '<path d="M7 3v8a2 2 0 0 0 2 2v8M11 3v6M7 3v6"/><path d="M17 21V3c-2 1.5-3 4-3 7v3h3"/>',
    "delivery": '<path d="M4 7h12v10H4z"/><path d="M16 10h3l2 3v4h-5"/><circle cx="7.5" cy="18" r="1.6"/><circle cx="17.5" cy="18" r="1.6"/>',
    "airport": '<path d="M2.5 19h19"/><path d="M3 13.5l3.5 1 3-1.5-5-6 2-.8 7.5 4.6 4.6-2.3a1.8 1.8 0 0 1 1.6 3.2L8 18"/>',
    "shopping": '<path d="M5 8h14l-1.2 11.2a2 2 0 0 1-2 1.8H8.2a2 2 0 0 1-2-1.8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
    "luggage": '<rect x="6" y="7" width="12" height="13" rx="2"/><path d="M9 7V4h6v3M9 11v6M15 11v6"/>',
    "health": '<path d="M12 21s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.6-7 10-7 10z"/><path d="M12 10v5M9.5 12.5h5"/>',
    "translate": '<path d="M3 5h9M7.5 3v2M5 5c.8 3 2.8 5.3 6 6.5M10 5c-.8 3-2.8 5.3-6 6.5"/><path d="M13 21l4-9 4 9M14.5 18h5"/>',
}

# Toss-style flow: one question at a time, friendly verdict words, search, progress.
UX = {
    "en": {
        "q1": "First, do you have a Korean phone number?",
        "q1_opts": {"visitor": ["No, just my home number or a data eSIM", "Most visitors"], "krsim": ["Yes, a Korean prepaid SIM (010)", "Tourist SIM, no residence card"], "arc": ["Yes, in my own name", "I live here and have a residence card (ARC)"]},
        "q2": "Which phone do you use?", "back": "Back",
        "greet": "Here's Korea in Easy Mode, for your phone.",
        "setup_is": "Your setup", "change": "Change",
        "tone": {"ok": "Good to go", "warn": "One extra step", "mixed": "Reports differ", "bad": "Blocked"},
        "search": "Search: taxi, subway, Wi-Fi", "nores": "Nothing matched. Try another word.",
        "ready": "{d} of {n} done before you fly",
        "suggest": "This page is also in {l}.", "switch": "Switch", "dismiss": "No thanks",
        "install": "Add EasyModeKorea to your home screen. It opens even without data.", "install_btn": "Install",
        "offline": "You're offline. Everything here still works.",
    },
    "ja": {
        "q1": "まず、韓国の電話番号はありますか?",
        "q1_opts": {"visitor": ["ない(自国の番号かデータeSIMだけ)", "ほとんどの旅行者"], "krsim": ["ある(韓国のプリペイドSIM・010)", "旅行者用SIM、登録証なし"], "arc": ["ある(自分名義)", "韓国在住で外国人登録証がある"]},
        "q2": "使っているスマホは?", "back": "戻る",
        "greet": "あなたのスマホ向け、韓国イージーモードです。",
        "setup_is": "あなたの状況", "change": "変更",
        "tone": {"ok": "そのまま使える", "warn": "ひと手間あり", "mixed": "情報が割れている", "bad": "使えない"},
        "search": "検索: タクシー、地下鉄、Wi-Fi", "nores": "見つかりませんでした。別の言葉で試してください。",
        "ready": "出発前の準備 {d}/{n} 完了",
        "suggest": "このページは{l}でも読めます。", "switch": "切り替える", "dismiss": "このままでいい",
        "install": "EasyModeKoreaをホーム画面に追加。データがなくても開けます。", "install_btn": "追加",
        "offline": "オフラインです。このページの内容はそのまま使えます。",
    },
    "zh-tw": {
        "q1": "首先,你有韓國電話號碼嗎?",
        "q1_opts": {"visitor": ["沒有,只有本國號碼或上網eSIM", "大多數旅客"], "krsim": ["有,韓國預付卡(010)", "旅客SIM卡,沒有登錄證"], "arc": ["有,是我名下的", "我住在韓國,有外國人登錄證"]},
        "q2": "你用哪種手機?", "back": "返回",
        "greet": "這是為你的手機準備的韓國簡單模式。",
        "setup_is": "你的狀況", "change": "更改",
        "tone": {"ok": "直接能用", "warn": "多一個步驟", "mixed": "說法不一", "bad": "無法使用"},
        "search": "搜尋:計程車、地鐵、Wi-Fi", "nores": "找不到。換個詞試試。",
        "ready": "出發前準備完成 {d}/{n}",
        "suggest": "這個頁面也有{l}版。", "switch": "切換", "dismiss": "不用了",
        "install": "把EasyModeKorea加到主畫面,沒有網路也能開。", "install_btn": "加入",
        "offline": "目前離線。這頁的內容照樣能用。",
    },
}

# Search words per task (all languages share one list; matching is case-insensitive substring).
KEYWORDS = {
    "data": "esim sim phone number 010 data wifi wi-fi internet roaming 電話 データ 番号 上網 電話號碼 網路 와이파이",
    "maps": "map maps google naver directions navigation route 地図 グーグル 地圖 導航 路線",
    "taxi": "taxi cab uber kakao k.ride tada taba ride タクシー 計程車 叫車",
    "transit": "subway metro bus tmoney t-money transit card top up recharge 地下鉄 バス 交通カード 地鐵 公車 交通卡 儲值",
    "ktx": "ktx train korail srt rail busan station 鉄道 電車 列車 火車 高鐵 釜山",
    "food-booking": "restaurant reservation booking waitlist catchtable naver queue レストラン 予約 順番待ち 餐廳 訂位 候位",
    "delivery": "delivery food baemin coupang eats shuttle order chicken デリバリー 出前 外送 外賣",
    "airport": "airport incheon icn gimpo arex train bus limousine seoul station arrival 空港 仁川 リムジン 機場 仁川 巴士 機場巴士",
    "shopping": "shopping tax free tax refund vat olive young oliveyoung daiso musinsa cosmetics beauty souvenir 買い物 免税 オリーブヤング ダイソー 購物 退稅 免稅 美妝 大創",
    "luggage": "luggage bag suitcase locker storage delivery t-locker t-luggage 荷物 ロッカー コインロッカー 行李 寄放 置物櫃",
    "health": "sick hospital pharmacy doctor medicine er emergency ambulance 119 1339 fever 病院 薬局 薬 救急 醫院 藥局 藥 急診 發燒",
    "translate": "translate translation papago menu sign korean language 翻訳 メニュー 翻譯 菜單",
}

for _l, _t in {"en": "About this guide", "ja": "このガイドについて", "zh-tw": "關於這份指南"}.items():
    X[_l]["about"] = _t

for _l, _t in {"en": ("We'll show which Korean apps work for you.", "Clear"), "ja": ("あなたに使える韓国アプリを表示します。", "クリア"), "zh-tw": ("我們會告訴你哪些韓國App能用。", "清除")}.items():
    UX[_l]["why"], UX[_l]["clear"] = _t

# One plan, in time order, filtered to the reader's setup. Replaces the old
# "before you fly" checklist and "first 24 hours" timeline, which overlapped.
# p: profiles it applies to (default: all); d: devices (default: all).
V, K, A = "visitor", "krsim", "arc"
PLAN = {
    "en": {
        "title": "Your trip plan", "title_arc": "Your setup list",
        "stages": {"before": "Before you fly", "land": "When you land", "city": "Into the city", "eve": "First evening", "setup": "Set up once"},
        "items": [
            {"st": "before", "p": [V, K], "t": "Submit the e-Arrival Card online within 3 days of landing (e-arrivalcard.go.kr). Check if you need a K-ETA (k-eta.go.kr)."},
            {"st": "before", "p": [V], "t": "Buy a Korea eSIM for data. Pick one with a 010 number if you want Korean SMS codes."},
            {"st": "before", "p": [K], "t": "Make sure your Korean SIM is active and note your 010 number."},
            {"st": "before", "p": [V, K], "t": "Install Naver Map and Papago. Download Papago's Korean offline pack."},
            {"st": "before", "p": [V, K], "t": "Install k.ride or Uber for taxis."},
            {"st": "before", "p": [V, K], "t": "Install CatchTable Global and sign up by email."},
            {"st": "before", "p": [V, K], "d": ["ios"], "t": "Install Mobile T-money and test a top-up with your card."},
            {"st": "before", "p": [V, K], "t": "Taking a train? Book KTX on KORAIL's English site. Tickets open two months ahead."},
            {"st": "land", "p": [V, K], "t": "Turn on mobile data before you leave the plane."},
            {"st": "land", "p": [V, K], "d": ["android"], "t": "Buy a T-money card at an airport convenience store. Top it up with cash."},
            {"st": "land", "p": [V, K], "d": ["ios"], "t": "If Mobile T-money didn't take your card, buy a physical T-money card at a convenience store."},
            {"st": "city", "p": [V, K], "t": "Take the airport railroad (AREX), an airport bus, or a taxi with k.ride or Uber."},
            {"st": "city", "p": [V, K], "t": "Show your host's address card to the driver."},
            {"st": "eve", "p": [V, K], "t": "Verify Naver with your passport, so you can book restaurants on Naver Map."},
            {"st": "eve", "p": [V, K], "t": "Install Baemin for food delivery and set it to English."},
            {"st": "setup", "p": [A], "t": "Set up PASS identity verification with your carrier."},
            {"st": "setup", "p": [A], "t": "Install Naver Map, Kakao T and Papago."},
            {"st": "setup", "p": [A], "t": "Add T-money to your phone, or use a transit-enabled Korean card."},
            {"st": "setup", "p": [A], "t": "Install Baemin or Coupang Eats for delivery."},
            {"st": "setup", "p": [A], "t": "Book KTX on the KORAIL+ app or the English site."},
        ],
    },
    "ja": {
        "title": "あなたの旅の準備", "title_arc": "最初にやる設定",
        "stages": {"before": "出発前", "land": "到着したら", "city": "市内へ", "eve": "最初の夜", "setup": "最初に一度"},
        "items": [
            {"st": "before", "p": [V, K], "t": "到着前3日以内にe-Arrival Cardをオンライン提出(e-arrivalcard.go.kr)。K-ETAが必要か確認(k-eta.go.kr)。"},
            {"st": "before", "p": [V], "t": "データ用の韓国eSIMを買う。韓国のSMS認証が必要なら010番号付きを選ぶ。"},
            {"st": "before", "p": [K], "t": "韓国SIMが開通しているか確認し、010番号を控えておく。"},
            {"st": "before", "p": [V, K], "t": "Naver MapとPapagoを入れる。Papagoの韓国語オフラインパックをダウンロード。"},
            {"st": "before", "p": [V, K], "t": "タクシー用にk.rideかUberを入れる。"},
            {"st": "before", "p": [V, K], "t": "CatchTable Globalを入れてメールで登録。"},
            {"st": "before", "p": [V, K], "d": ["ios"], "t": "モバイルT-moneyを入れ、カードでチャージを試す。"},
            {"st": "before", "p": [V, K], "t": "列車に乗るなら、KORAILの英語サイトでKTXを予約。2か月前から買えます。"},
            {"st": "land", "p": [V, K], "t": "飛行機を降りる前にモバイルデータをオンに。"},
            {"st": "land", "p": [V, K], "d": ["android"], "t": "空港のコンビニでT-moneyカードを買い、現金でチャージ。"},
            {"st": "land", "p": [V, K], "d": ["ios"], "t": "モバイルT-moneyでカードが使えなかったら、コンビニでT-moneyカードを買う。"},
            {"st": "city", "p": [V, K], "t": "空港鉄道(AREX)、空港バス、またはk.ride・Uberのタクシーで移動。"},
            {"st": "city", "p": [V, K], "t": "宿の住所カードを運転手に見せる。"},
            {"st": "eve", "p": [V, K], "t": "パスポートでNaverを認証。Naver Mapで店の予約ができるように。"},
            {"st": "eve", "p": [V, K], "t": "デリバリー用にBaeminを入れ、日本語か英語に設定。"},
            {"st": "setup", "p": [A], "t": "通信会社でPASSの本人認証を設定。"},
            {"st": "setup", "p": [A], "t": "Naver Map、Kakao T、Papagoを入れる。"},
            {"st": "setup", "p": [A], "t": "スマホにT-moneyを追加するか、交通機能付きの韓国カードを使う。"},
            {"st": "setup", "p": [A], "t": "デリバリー用に配達の民族かCoupang Eatsを入れる。"},
            {"st": "setup", "p": [A], "t": "KTXはKORAIL+アプリか英語サイトで予約。"},
        ],
    },
    "zh-tw": {
        "title": "你的旅程準備", "title_arc": "第一次要做的設定",
        "stages": {"before": "出發前", "land": "落地時", "city": "進市區", "eve": "第一個晚上", "setup": "一次設定好"},
        "items": [
            {"st": "before", "p": [V, K], "t": "在入境前3天內線上填寫e-Arrival Card(e-arrivalcard.go.kr)。確認是否需要K-ETA(k-eta.go.kr)。"},
            {"st": "before", "p": [V], "t": "買上網用的韓國eSIM。需要韓國簡訊驗證碼的話,選有010號碼的方案。"},
            {"st": "before", "p": [K], "t": "確認韓國SIM卡已開通,記下你的010號碼。"},
            {"st": "before", "p": [V, K], "t": "安裝Naver Map和Papago。下載Papago的韓語離線包。"},
            {"st": "before", "p": [V, K], "t": "安裝k.ride或Uber叫計程車。"},
            {"st": "before", "p": [V, K], "t": "安裝CatchTable Global,用電子郵件註冊。"},
            {"st": "before", "p": [V, K], "d": ["ios"], "t": "安裝行動T-money,用你的卡試著儲值。"},
            {"st": "before", "p": [V, K], "t": "要搭火車的話,在KORAIL英文網站訂KTX。兩個月前開賣。"},
            {"st": "land", "p": [V, K], "t": "下飛機前打開行動數據。"},
            {"st": "land", "p": [V, K], "d": ["android"], "t": "在機場便利商店買T-money卡,用現金儲值。"},
            {"st": "land", "p": [V, K], "d": ["ios"], "t": "如果行動T-money不接受你的卡,就到便利商店買實體T-money卡。"},
            {"st": "city", "p": [V, K], "t": "搭機場鐵路(AREX)、機場巴士,或用k.ride、Uber叫車。"},
            {"st": "city", "p": [V, K], "t": "把住宿的地址卡給司機看。"},
            {"st": "eve", "p": [V, K], "t": "用護照驗證Naver,就能在Naver Map訂餐廳。"},
            {"st": "eve", "p": [V, K], "t": "安裝Baemin叫外送,語言設成中文。"},
            {"st": "setup", "p": [A], "t": "向電信公司設定PASS身分驗證。"},
            {"st": "setup", "p": [A], "t": "安裝Naver Map、Kakao T和Papago。"},
            {"st": "setup", "p": [A], "t": "在手機加入T-money,或使用有交通功能的韓國卡。"},
            {"st": "setup", "p": [A], "t": "外送安裝外送民族或Coupang Eats。"},
            {"st": "setup", "p": [A], "t": "KTX用KORAIL+ App或英文網站訂票。"},
        ],
    },
}

# The question people actually type, per task. Shown as the topic page's
# first heading and sent as FAQPage data so search and AI answers can quote it.
QUESTION = {
    "en": {"data": "Do I need a Korean phone number in Korea?", "airport": "How do I get from Incheon Airport to Seoul?", "maps": "Does Google Maps work in Korea?", "taxi": "Can I call a taxi in Korea without a Korean number?",
           "transit": "Can I top up T-money with a foreign card?", "ktx": "How do I book a KTX train as a foreigner?", "food-booking": "Can I book restaurants in Korea without a Korean number?",
           "delivery": "Can I order food delivery in Korea as a tourist?", "translate": "What is the best translation app for Korea?", "shopping": "How do I get a tax refund when shopping in Korea?", "luggage": "Where can I store luggage in Seoul?", "health": "What do I do if I get sick in Korea?"},
    "ja": {"data": "韓国で韓国の電話番号は必要?", "airport": "仁川空港からソウル市内への行き方は?", "maps": "韓国でGoogleマップは使える?", "taxi": "韓国の番号なしでタクシーを呼べる?",
           "transit": "T-moneyに海外カードでチャージできる?", "ktx": "外国人がKTXを予約するには?", "food-booking": "韓国の番号なしでレストランを予約できる?",
           "delivery": "旅行者でも韓国でデリバリーを頼める?", "translate": "韓国旅行におすすめの翻訳アプリは?", "shopping": "韓国で買い物の免税(タックスリファンド)を受けるには?", "luggage": "ソウルで荷物を預けられる場所は?", "health": "韓国旅行中に体調を崩したらどうする?"},
    "zh-tw": {"data": "在韓國需要韓國電話號碼嗎?", "airport": "仁川機場怎麼到首爾市區?", "maps": "Google地圖在韓國能用嗎?", "taxi": "沒有韓國號碼能在韓國叫計程車嗎?",
              "transit": "T-money可以用國外信用卡儲值嗎?", "ktx": "外國人怎麼訂KTX?", "food-booking": "沒有韓國號碼能在韓國訂餐廳嗎?",
              "delivery": "觀光客能在韓國叫外送嗎?", "translate": "去韓國用哪個翻譯App最好?", "shopping": "在韓國購物怎麼退稅?", "luggage": "在首爾哪裡可以寄放行李?", "health": "在韓國生病了怎麼辦?"},
}


# Help: emergency numbers and survival phrases. Numbers checked against Korea
# Tourism Organization and city sites (1330 is 24h in EN/JA/ZH).
HELP = {
    "en": {"btn": "Help", "title": "Help", "calls": "Call", "phrases": "Show someone",
           "nums": [["112", "Police"], ["119", "Fire and ambulance"], ["1330", "Travel helpline, 24h in English. From a foreign SIM: +82-2-1330"], ["1339", "Medical advice and the nearest open ER, 24h"]]},
    "ja": {"btn": "ヘルプ", "title": "ヘルプ", "calls": "電話する", "phrases": "見せて伝える",
           "nums": [["112", "警察"], ["119", "消防・救急"], ["1330", "観光案内ダイヤル(日本語24時間)。海外のSIMからは +82-2-1330"], ["1339", "医療相談と近くの救急室の案内(24時間)"]]},
    "zh-tw": {"btn": "求助", "title": "求助", "calls": "打電話", "phrases": "給對方看",
              "nums": [["112", "警察"], ["119", "消防與救護車"], ["1330", "觀光諮詢熱線(中文24小時)。用國外SIM請撥 +82-2-1330"], ["1339", "醫療諮詢與最近急診室資訊(24小時)"]]},
}
HELP_PHRASES = [
    ["도와주세요.", {"en": "Please help me.", "ja": "助けてください。", "zh-tw": "請幫幫我。"}],
    ["병원에 가야 해요.", {"en": "I need to go to a hospital.", "ja": "病院に行かなければなりません。", "zh-tw": "我需要去醫院。"}],
    ["가까운 약국이 어디예요?", {"en": "Where is the nearest pharmacy?", "ja": "近くの薬局はどこですか?", "zh-tw": "最近的藥局在哪裡?"}],
    ["화장실이 어디예요?", {"en": "Where is the restroom?", "ja": "トイレはどこですか?", "zh-tw": "洗手間在哪裡?"}],
    ["견과류 알레르기가 있어요.", {"en": "I'm allergic to nuts.", "ja": "ナッツアレルギーがあります。", "zh-tw": "我對堅果過敏。"}],
    ["매운 음식을 못 먹어요.", {"en": "I can't eat spicy food.", "ja": "辛い料理が食べられません。", "zh-tw": "我不能吃辣。"}],
    ["길을 잃었어요.", {"en": "I'm lost.", "ja": "道に迷いました。", "zh-tw": "我迷路了。"}],
]

# Feedback. FORM is a Google Form (owned by edandco.biz) once it exists:
# {"action": "https://docs.google.com/forms/d/e/<id>/formResponse", "msg": "entry.N", "email": "entry.N", "ctx": "entry.N"}
# Until then, sending opens a prefilled email to the business address.
FEEDBACK_FORM = {"action": "https://docs.google.com/forms/d/e/1FAIpQLSfCghsXyPnhlsgILMa_OWagIrsNzKf6kWCPqErBNAXVXlhNkA/formResponse", "msg": "entry.1067526763", "email": "entry.203830250", "ctx": "entry.1755038916"}
FEEDBACK_TO = "edandco.biz@gmail.com"
FEEDBACK = {
    "en": {"open": "Send feedback", "title": "Tell us anything", "lead": "Something wrong, missing, or confusing? Ideas for us? We read every message.",
           "msg": "Your message", "ph": "What worked, what didn't, what should we add?", "email": "Email (optional, only if you'd like a reply)",
           "send": "Send", "thanks": "Thank you! We read every message.", "fail": "Tell us what happened"},
    "ja": {"open": "ご意見を送る", "title": "なんでも教えてください", "lead": "間違い、足りない情報、わかりにくい所、アイデアなど。すべて読んでいます。",
           "msg": "メッセージ", "ph": "使えたこと、使えなかったこと、追加してほしいこと", "email": "メール(任意。返信が必要な場合のみ)",
           "send": "送信", "thanks": "ありがとうございます。すべて読んでいます。", "fail": "何があったか教えてください"},
    "zh-tw": {"open": "提供意見", "title": "什麼都可以告訴我們", "lead": "有錯誤、缺少的資訊、看不懂的地方或建議嗎?每則訊息我們都會看。",
              "msg": "你的訊息", "ph": "哪些能用、哪些不行、希望我們加什麼?", "email": "電子郵件(選填,需要回覆再填)",
              "send": "送出", "thanks": "謝謝!每則訊息我們都會看。", "fail": "告訴我們發生了什麼"},
}

for _l, _t in {"en": ("Copy address", "Copied"), "ja": ("住所をコピー", "コピーしました"), "zh-tw": ("複製地址", "已複製")}.items():
    UX[_l]["copy_addr"], UX[_l]["copied"] = _t

for _l, _t in {"en": "While you're here", "ja": "滞在中に", "zh-tw": "旅途中"}.items():
    UX[_l]["more"] = _t

# Home page title and description as they appear in search results: plain and specific.
for _l, (_t, _d) in {
    "en": ("Which Korean apps work for visitors (checked monthly)", "Taxi, subway, KTX, restaurant booking, delivery and tax refunds: see what works with a foreign phone number and card, based on your setup. Free, no sign-up."),
    "ja": ("旅行者が使える韓国アプリ早見表(毎月確認)", "タクシー、地下鉄、KTX、レストラン予約、デリバリー、免税。海外の電話番号とカードで使えるものを、あなたの状況別に確認できます。無料・登録不要。"),
    "zh-tw": ("旅客能用的韓國App一覽(每月確認)", "計程車、地鐵、KTX、餐廳訂位、外送、退稅:依你的狀況查看用國外號碼和信用卡能用哪些。免費、免註冊。"),
}.items():
    X[_l]["home_title"], X[_l]["home_desc"] = _t, _d

# "Didn't find it?" question box at the end of pages. Sent to the same Google Form as feedback (no API, no new account).
ASK = {
    "en": {"title": "Didn't find what you need?", "lead": "Ask your question. We answer by adding it to the guides, and by email if you leave one.",
           "ph": "e.g. Can I book a KTX seat with a foreign Visa card?", "email": "Email (optional, for a reply)", "send": "Send question", "thanks": "Thanks! Your question has been sent."},
    "ja": {"title": "知りたい情報が見つかりませんか?", "lead": "質問をどうぞ。ガイドに追記して回答します。メールを書いていただければ返信もします。",
           "ph": "例: 海外のVisaカードでKTXを予約できますか?", "email": "メール(任意。返信用)", "send": "質問を送る", "thanks": "ありがとうございます。質問を受け付けました。"},
    "zh-tw": {"title": "沒找到需要的資訊嗎?", "lead": "留下你的問題。我們會補充到指南中;若留下電子郵件,也會回信。",
              "ph": "例如:外國 Visa 卡可以訂 KTX 嗎?", "email": "電子郵件(選填,用於回覆)", "send": "送出問題", "thanks": "謝謝!已收到你的問題。"},
    "zh-cn": {"title": "没找到需要的信息吗?", "lead": "留下你的问题。我们会补充到指南里;如果留下邮箱,也会回信。",
              "ph": "例如:外国 Visa 卡可以订 KTX 吗?", "email": "邮箱(选填,用于回复)", "send": "发送问题", "thanks": "谢谢!已收到你的问题。"},
    "vi": {"title": "Không tìm thấy thông tin bạn cần?", "lead": "Hãy gửi câu hỏi. Chúng tôi sẽ bổ sung vào hướng dẫn, và trả lời qua email nếu bạn để lại.",
           "ph": "VD: Thẻ Visa nước ngoài có đặt vé KTX được không?", "email": "Email (không bắt buộc, để nhận trả lời)", "send": "Gửi câu hỏi", "thanks": "Cảm ơn! Câu hỏi của bạn đã được gửi."},
}
