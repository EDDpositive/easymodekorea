"""Words on the price game page. Every string is "English | Japanese | Traditional Chinese | Vietnamese"; Simplified Chinese is derived with t2s."""
from t2s import t2s

LANGS = ["en", "ja", "zh-tw", "zh-cn", "vi"]
TAG = {"en": "en", "ja": "ja", "zh-tw": "zh-Hant", "zh-cn": "zh-Hans", "vi": "vi"}
NAME = {"en": "English", "ja": "日本語", "zh-tw": "繁體中文", "zh-cn": "简体中文", "vi": "Tiếng Việt"}
SHORT = {"en": "EN", "ja": "日本語", "zh-tw": "繁體", "zh-cn": "简体", "vi": "VI"}
DIR = {"en": "won/", "ja": "won/ja/", "zh-tw": "won/zh-tw/", "zh-cn": "won/zh-cn/", "vi": "won/vi/"}
HOME = {"en": "", "ja": "ja/", "zh-tw": "zh-tw/", "zh-cn": "zh-cn/", "vi": "vi/"}
OG = {"en": "en_US", "ja": "ja_JP", "zh-tw": "zh_TW", "zh-cn": "zh_CN", "vi": "vi_VN"}
BRAND = "Won a Day"  # working name, see docs/won-game.md

# Characters the shared table does not have yet, then mainland words that differ from the straight conversion
CN_CH = dict(x for x in ("藍蓝 綠绿 紅红 鈴铃 麵面 鍋锅 醬酱 雞鸡 蔘参 鮑鲍 顆颗 葉叶 蝦虾 隻只 魷鱿 乾干 蘿萝 蔔卜 醃腌 蠣蛎 宮宫 廟庙 館馆 髮发 蔥葱 黃黄 鳳凤 鯖鲭 檸柠 鮮鲜 針针 鹽盐 櫛栉 薑姜 凍冻 盤盘 漸渐 "
                        "戰战 組组 繪绘 鈔钞 紙纸 農农 術术 壽寿 摺折 遊游 鈕钮 錄录 貴贵 較较 歲岁 輪轮 漢汉 濟济 鎖锁 薦荐 艙舱 籃篮 煎煎 蔥葱 隧隧 繫系 熱热 慶庆 蓋盖 燙烫 齡龄 氈毡 藝艺 壓压 墜坠 潔洁 齊齐 讓让 憑凭 湯汤 陽阳 學学 漁渔 顏颜 煥焕 餅饼 穀谷 遺遗 跡迹 績绩").split())
CN = [("计程车", "出租车"), ("市内公车", "市内公交"), ("公车", "公交"), ("凤梨", "菠萝"), ("酪梨", "牛油果"), ("番茄", "西红柿"), ("奇异果", "猕猴桃"), ("红萝卜", "胡萝卜"), ("青花菜", "西兰花"),
      ("番薯", "红薯"), ("小黄瓜", "黄瓜"), ("韩国栉瓜", "韩国西葫芦"), ("白带鱼", "带鱼"), ("免注册", "无需注册"), ("储存", "保存"), ("装置", "设备"), ("公尺", "米"), ("公克", "克"), ("公升", "升"),
      ("营运", "运营"), ("造访", "访问"), ("回报", "反馈"), ("整合票", "联票"), ("门票", "门票"), ("车资", "车费"), ("起步里程", "起步里程"), ("手机", "手机"), ("纪录", "记录")]


def pick(s, lang):
    """One language out of an en|ja|tw|vi string (or an already split list)."""
    p = s if isinstance(s, (list, tuple)) else s.split("|")
    if lang != "zh-cn": return p[{"en": 0, "ja": 1, "zh-tw": 2, "vi": 3}[lang]]
    t = "".join(CN_CH.get(c, c) for c in t2s(p[2]))
    for a, b in CN: t = t.replace(a, b)
    return t


M = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MF = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def date(iso, lang):
    y, m, *d = iso.split("-"); m = int(m)
    if lang == "en": return f"{int(d[0])} {M[m - 1]} {y}" if d else f"{MF[m - 1]} {y}"
    if lang == "vi": return f"{int(d[0])}/{m}/{y}" if d else f"tháng {m}/{y}"
    sp = "" if lang == "ja" else " "
    return f"{y}{sp}年{sp}{m}{sp}月" + (f"{sp}{int(d[0])}{sp}日" if d else "")


def fx(r, lang):
    """What ten thousand won is worth, from the customs rate in won_data.FX (won for one unit)."""
    n = 10000 / r[{"en": "USD", "ja": "JPY", "zh-tw": "TWD", "zh-cn": "CNY", "vi": "USD"}[lang]]
    amt = {"en": f"US${n:.2f}", "ja": f"{n:,.0f}円", "zh-tw": f"新臺幣 {n:,.0f} 元", "zh-cn": f"人民币 {n:,.0f} 元", "vi": f"{n:.2f} USD".replace(".", ",")}[lang]
    d = date(r["from"], lang)
    return {"en": f"₩10,000 ≈ {amt} (Korea Customs rate, {d})", "ja": f"₩10,000は約{amt}（韓国関税庁の週間レート、{d}）", "zh-tw": f"₩10,000 約{amt}（韓國關稅廳每週匯率，{d}）",
            "zh-cn": f"₩10,000 约{amt}（韩国海关每周汇率，{d}）", "vi": f"₩10.000 ≈ {amt} (tỷ giá Hải quan Hàn Quốc, {d})"}[lang]


KIND = {"survey": "Seoul average, {d}|ソウル平均、{d}|首爾平均，{d}|trung bình Seoul, {d}",
        "retail": "Seoul shops, {d}|ソウルの店頭、{d}|首爾店家，{d}|cửa hàng ở Seoul, {d}",
        "fixed": "as of {d}|{d}時点|以 {d}為準|tính đến {d}"}

T = {
    "title": "How much in Seoul? Guess 5 real prices a day|ソウルでいくら？ 1日5問の値段当て|在首爾多少錢？每天猜 5 個真實價格|Ở Seoul giá bao nhiêu? Mỗi ngày đoán 5 giá thật",
    "desc": "A one-minute daily game. Lay down the won you would pay for a bus, a bowl of noodles or a palace ticket, then see the real Seoul price with its source and date. No sign-up, no ads.|1分で終わる毎日のゲーム。バス、麺、宮殿の入場料にいくら払うか、お金を出して当てます。答えは出典と日付つきの本当のソウル価格。登録なし、広告なし。|一分鐘的每日遊戲。公車、一碗麵、宮殿門票，放上你覺得要付的韓元，再看附來源與日期的首爾真實價格。免註冊、無廣告。|Trò chơi một phút mỗi ngày. Đặt số won bạn nghĩ phải trả cho xe buýt, tô mì hay vé vào cung, rồi xem giá thật ở Seoul kèm nguồn và ngày. Không đăng ký, không quảng cáo.",
    "h1": "How much in Seoul?|ソウルでいくら？|在首爾多少錢？|Ở Seoul giá bao nhiêu?",
    "lede": "Five real prices a day, about a minute. No sign-up, no ads.|本物の値段を1日5問、約1分。登録なし、広告なし。|每天五個真實價格，約一分鐘。免註冊、無廣告。|Mỗi ngày năm giá thật, khoảng một phút. Không đăng ký, không quảng cáo.",
    "how": "Tap the money you would hand over, then pay.|払うと思う分のお金を押して、支払います。|點出你覺得要付的錢，再按付款。|Chạm vào số tiền bạn nghĩ phải trả, rồi bấm trả.",
    "c_ride": "Getting around|乗りもの|交通|Đi lại", "c_table": "On the table|食べもの|餐桌上|Món ăn", "c_out": "Out and about|おでかけと暮らし|出門與生活|Đi chơi, đời sống",
    "c_market": "At the market|買いもの|逛市場|Đi chợ", "c_bill": "The bill|お会計|結帳|Hóa đơn",
    "billq": "What does it all add up to?|全部でいくら？|總共多少？|Tổng cộng bao nhiêu?",
    "tray": "Your tray|お金のトレー|你的錢盤|Khay tiền", "clear": "Clear|戻す|清空|Xóa", "back": "Take back ₩{n}|₩{n}を戻す|拿回 ₩{n}|Lấy lại ₩{n}", "add": "Add ₩{n}|₩{n}を出す|放上 ₩{n}|Thêm ₩{n}",
    "pay": "Pay {n}|{n} を払う|付 {n}|Trả {n}", "free": "Pay nothing: it's free|払わない（無料だと思う）|不用付（我猜免費）|Không trả: miễn phí",
    "isfree": "Free|無料|免費|Miễn phí", "paid": "You paid {n}|あなた：{n}|你付了 {n}|Bạn trả {n}", "you": "You|あなた|你|Bạn", "real": "Real price|本当の値段|真實價格|Giá thật",
    "over": "{n} too much|{n} 払いすぎ|多付 {n}|Dư {n}", "under": "{n} short|{n} 足りない|少付 {n}|Thiếu {n}", "spot": "Spot on|ぴったり|完全正確|Chính xác",
    "pts": "points|点|分|điểm", "next": "Next price|次の値段|下一題|Giá tiếp theo", "fin": "See my score|結果を見る|看我的成績|Xem điểm của tôi", "src": "Source|出典|來源|Nguồn",
    "of": "Price {n} of 5|5問中{n}問目|第 {n} 題，共 5 題|Giá {n} trên 5",
    "lv0": "Just landed|着いたばかり|剛下飛機|Vừa xuống máy bay", "lv1": "Still on airport prices|まだ空港の値段|還停在機場物價|Vẫn theo giá sân bay", "lv2": "Getting the feel|感覚をつかみ中|漸漸抓到感覺|Bắt đầu quen giá",
    "lv3": "Market regular|市場の常連|市場熟客|Khách quen của chợ", "lv4": "Could live here|もう住めます|可以住下來了|Sống ở đây được rồi",
    "sum": "You laid down {a} for {b} of Seoul.|ソウルの{b}分に、{a}を出しました。|{b} 的首爾，你付了 {a}。|Bạn trả {a} cho {b} ở Seoul.",
    "mine": "I laid down {a} for {b} of Seoul.|ソウルの{b}分に、{a}を出しました。|{b} 的首爾，我付了 {a}。|Mình trả {a} cho {b} ở Seoul.",
    "beat": "Can you beat it?|超えられる？|你能超過嗎？|Bạn vượt được không?",
    "share": "Share and dare a friend|シェアして友だちに挑戦|分享並挑戰朋友|Chia sẻ và thách bạn bè", "pic": "Result picture|結果の画像|結果圖片|Hình kết quả", "score": "Result|結果|成績|Kết quả", "send": "Send picture|画像を送る|傳送圖片|Gửi hình", "save": "Save picture|画像を保存|儲存圖片|Lưu hình", "copied": "Copied. Paste it anywhere.|コピーしました。貼り付けてください。|已複製，貼到哪裡都可以。|Đã sao chép. Dán ở đâu cũng được.",
    "hold": "Or press and hold the picture to save it.|画像を長押ししても保存できます。|也可以長按圖片儲存。|Hoặc nhấn giữ hình để lưu.",
    "friend": "A friend scored {n} on this set. Your turn.|友だちはこの5問で{n}点。次はあなた。|朋友在這一組拿到 {n} 分，換你了。|Một người bạn được {n} điểm ở bộ này. Đến lượt bạn.", "vs": "You {a}, your friend {b}|あなた{a}点、友だち{b}点|你 {a} 分，朋友 {b} 分|Bạn {a}, bạn của bạn {b}",
    "streak": "Streak|連続日数|連續天數|Chuỗi ngày", "played": "Played|プレイ数|玩過|Đã chơi", "avg": "Average|平均|平均|Trung bình",
    "tmrw": "New prices at midnight, your time.|次の5問は、あなたの時計の午前0時から。|新的五題在你當地午夜 12 點開始。|Giá mới lúc nửa đêm theo giờ của bạn.",
    "earlier": "Play an earlier day|前の日を遊ぶ|玩之前的日子|Chơi ngày trước", "today": "Today|今日|今天|Hôm nay", "yest": "Yesterday's prices|昨日の答え|昨天的答案|Giá hôm qua", "totoday": "Play today's set|今日の5問へ|玩今天的五題|Chơi bộ hôm nay",
    "off": "Saved on this phone: it works offline.|この端末に保存済み。オフラインでも遊べます。|已存在這支手機，離線也能玩。|Đã lưu trên máy: chơi được khi không có mạng.",
    "lang": "Language|言語|語言|Ngôn ngữ", "noscript": "This game needs JavaScript. The price list below works without it.|このゲームにはJavaScriptが必要です。下の価格表はそのまま読めます。|這個遊戲需要 JavaScript。下方的價格表可直接閱讀。|Trò chơi cần JavaScript. Bảng giá bên dưới vẫn đọc được.",
    "emk_h": "Going to Seoul?|ソウルへ行きますか？|要去首爾嗎？|Sắp đến Seoul?", "emk_p": "EasyModeKorea shows what works with a foreign phone and card.|外国の電話とカードで何が使えるかは、EasyModeKoreaで。|外國手機和卡片能用什麼，看 EasyModeKorea。|Xem điện thoại và thẻ nước ngoài dùng được gì tại EasyModeKorea.",
    "h_how": "How it works|遊び方|玩法|Cách chơi", "h_faq": "Questions|よくある質問|常見問題|Câu hỏi", "h_list": "Seoul prices in this game, with dates|このゲームのソウル価格（日付つき）|遊戲中的首爾價格（附日期）|Giá ở Seoul trong trò chơi, kèm ngày",
    "spoil": "Show all {n} prices (this gives away the answers)|{n}件すべて見る（答えが分かります）|顯示全部 {n} 個價格（會看到答案）|Xem cả {n} giá (sẽ lộ đáp án)",
    "col_i": "What|もの|項目|Món", "col_p": "Price|値段|價格|Giá", "col_s": "Source and date|出典と日付|來源與日期|Nguồn và ngày",
    "by": "Made by EasyModeKorea|EasyModeKorea制作|EasyModeKorea 製作|Do EasyModeKorea thực hiện", "contact": "Report a wrong price|間違いを知らせる|回報錯誤價格|Báo giá sai", "wipe": "Erase my scores on this device|この端末の記録を消す|清除這台裝置的紀錄|Xóa điểm trên thiết bị này",
    "wipeq": "Erase every score saved on this device?|この端末に保存した記録をすべて消しますか？|要清除這台裝置上的所有紀錄嗎？|Xóa mọi điểm đã lưu trên thiết bị này?",
    "note": "Prices come only from official pages. This game is not connected with the Korean government or any shop. The money is drawn for the game and is not a copy of Korean notes.|値段は公式ページのものだけです。韓国政府や店とは関係ありません。お金の絵はこのゲーム用に描いたもので、本物の紙幣の写しではありません。|價格只取自官方網頁。本遊戲與韓國政府及任何店家無關。畫面上的錢是為遊戲繪製，並非真鈔圖案。|Giá chỉ lấy từ trang chính thức. Trò chơi không liên quan đến chính phủ Hàn Quốc hay cửa hàng nào. Tiền trong trò chơi là hình vẽ, không phải bản sao tiền thật.",
}

HOW = [
    "Every day brings five new questions: getting around, food, an outing or a service, the market, and one bill that adds several prices together.|毎日、新しい5問が出ます。乗りもの、食べもの、おでかけや暮らし、買いもの、そして何品かを足すお会計です。|每天有五題新題目：交通、食物、出門或服務、市場，最後一題是把幾個價格加起來的結帳。|Mỗi ngày có năm câu mới: đi lại, món ăn, đi chơi hoặc dịch vụ, đi chợ, và một hóa đơn cộng nhiều giá.",
    "Lay down notes and coins for what you think it costs. You get one guess for each.|いくらだと思うか、お札と硬貨を出します。答えは1問につき1回です。|放上你覺得的紙鈔和硬幣，每題只能猜一次。|Đặt tiền giấy và tiền xu bằng số bạn nghĩ. Mỗi câu chỉ đoán một lần.",
    "Points show how close you came. For something that costs ₩10,000, paying ₩5,000 gives 50 points, and so does paying ₩20,000. ▲ means you paid too much, ▼ too little, ✓ very close.|点数は近さです。₩10,000のものに₩5,000を出すと50点、₩20,000でも50点。▲は払いすぎ、▼は足りない、✓はほぼ正解です。|分數代表接近程度。₩10,000 的東西付 ₩5,000 得 50 分，付 ₩20,000 也是 50 分。▲ 是多付，▼ 是少付，✓ 是非常接近。|Điểm cho biết bạn đoán gần đến đâu. Món giá ₩10.000 mà trả ₩5.000 thì được 50 điểm, trả ₩20.000 cũng 50 điểm. ▲ là trả dư, ▼ là trả thiếu, ✓ là rất gần.",
    "Some things in Seoul are free. If you think so, pay nothing.|ソウルには無料のものもあります。そう思ったら、何も出さずに答えます。|首爾有些東西是免費的。這樣想的話，就什麼都不要放。|Ở Seoul có thứ miễn phí. Nếu bạn nghĩ vậy, đừng trả gì cả.",
]

FAQ = [
    ("Where do the prices come from?|値段はどこから？|價格從哪裡來？|Giá lấy từ đâu?",
     "Only from official pages that state the number: Korea's national price survey (price.go.kr), the KAMIS farm and fish price service, Seoul City, the royal palaces, museums and the post office. Every answer shows its source and date.|数字を載せている公式ページだけです。韓国の物価調査（price.go.kr）、農水産物価格のKAMIS、ソウル市、王宮、美術館、郵便など。どの答えにも出典と日付が出ます。|只用明確寫出數字的官方網頁：韓國物價調查（price.go.kr）、農漁產品價格 KAMIS、首爾市、王宮、美術館和郵局。每個答案都會顯示來源和日期。|Chỉ từ trang chính thức có ghi con số: khảo sát giá quốc gia (price.go.kr), KAMIS về giá nông thủy sản, thành phố Seoul, các cung điện, bảo tàng và bưu điện. Mỗi đáp án đều có nguồn và ngày."),
    ("How old are the prices?|いつの値段？|是什麼時候的價格？|Giá của khi nào?",
     "Restaurant and service prices are Seoul averages for October 2026. Market prices are Seoul shop averages for 24 November 2026. Fares and tickets were read on the official page, most of them on 25 November 2026.|食堂とサービスは2026年10月のソウル平均、買いものは2026年11月24日のソウル店頭平均です。運賃と入場料は公式ページで確認し、ほとんどが2026年11月25日です。|餐廳和服務是 2026 年 10 月的首爾平均，市場價格是 2026 年 11 月 24 日的首爾店家平均。交通和門票則查自官方網頁，多數為 2026 年 11 月 25 日。|Giá quán ăn và dịch vụ là trung bình Seoul tháng 10/2026. Giá chợ là trung bình cửa hàng Seoul ngày 24/11/2026. Giá vé được đọc trên trang chính thức, phần lớn vào ngày 25/11/2026."),
    ("Will I pay exactly this in Seoul?|ソウルで本当にこの値段？|在首爾真的是這個價格嗎？|Đến Seoul có trả đúng giá này không?",
     "Fares and tickets, yes, until they change. Meals, haircuts and groceries are averages: a place next to a famous sight often costs more, a neighbourhood place less.|運賃と入場料は、改定されるまで同じです。食事や散髪、食材は平均なので、名所のそばは高め、住宅街は安めのことがあります。|交通和門票在調整前都是這個價格。餐點、剪髮和食材是平均值：景點旁常較貴，住宅區較便宜。|Vé xe và vé vào cửa thì đúng, cho đến khi thay đổi. Bữa ăn, cắt tóc và thực phẩm là giá trung bình: chỗ gần điểm nổi tiếng thường đắt hơn, quán trong khu dân cư rẻ hơn."),
    ("Is a bowl of noodles really over ₩10,000?|麺1杯が本当に1万ウォン以上？|一碗麵真的超過一萬韓元？|Một tô mì thật sự hơn 10.000 won?",
     "On average, yes. In October 2026 the Seoul average was ₩12,692 for naengmyeon and ₩10,038 for kalguksu, while jajangmyeon was ₩7,808.|平均ではそうです。2026年10月のソウル平均は冷麺₩12,692、カルグクス₩10,038、ジャージャー麺は₩7,808でした。|平均來說是的。2026 年 10 月首爾平均冷麵 ₩12,692、刀切麵 ₩10,038，炸醬麵則是 ₩7,808。|Tính trung bình thì đúng. Tháng 10/2026, trung bình ở Seoul là ₩12.692 cho naengmyeon, ₩10.038 cho kalguksu, còn jajangmyeon là ₩7.808."),
    ("Do I need an account?|登録は必要？|需要註冊嗎？|Có cần tài khoản không?",
     "No. Your scores stay on this device and your guesses are not sent anywhere. The page only counts visits and a few button presses, without cookies.|いりません。記録はこの端末だけに残り、答えはどこにも送りません。訪問数とボタンの回数だけをクッキーなしで数えます。|不需要。紀錄只存在這台裝置，你的猜測不會傳送到任何地方。網頁只統計造訪次數和部分按鈕次數，不用 cookie。|Không. Điểm chỉ lưu trên thiết bị này và câu đoán của bạn không gửi đi đâu. Trang chỉ đếm lượt xem và vài lần bấm nút, không dùng cookie."),
    ("When do the prices change?|次の問題はいつ？|什麼時候換新題目？|Khi nào có câu mới?",
     "At midnight on your device's clock. Everyone gets the same five on the same date, so you can compare with friends.|端末の時計で午前0時です。同じ日付なら全員が同じ5問なので、友だちと比べられます。|依你裝置的時間，午夜 12 點。同一天大家都是相同的五題，可以和朋友比較。|Lúc nửa đêm theo đồng hồ của thiết bị. Cùng một ngày, ai cũng nhận năm câu giống nhau nên có thể so với bạn bè."),
    ("Can I play without a connection?|オフラインでも遊べる？|離線也能玩嗎？|Chơi không cần mạng được không?",
     "Yes, once you have opened the page with a connection. Older days are open too, below your result.|はい。一度つながった状態で開けば遊べます。前の日の問題も、結果の下から選べます。|可以，連線打開過一次就行。之前的題目也能從結果下方選來玩。|Được, sau khi đã mở trang một lần khi có mạng. Các ngày trước cũng chơi được, ở dưới phần kết quả."),
    ("Which notes and coins does Korea use?|韓国のお札と硬貨は？|韓國有哪些紙鈔和硬幣？|Hàn Quốc dùng những tờ tiền nào?",
     "Notes are ₩50,000, ₩10,000, ₩5,000 and ₩1,000. The coins you meet most are ₩500 and ₩100. The colours in the game follow the real ones: yellow, green, red and blue.|お札は₩50,000、₩10,000、₩5,000、₩1,000、よく使う硬貨は₩500と₩100です。ゲームの色も本物と同じ順に、黄、緑、赤、青です。|紙鈔有 ₩50,000、₩10,000、₩5,000、₩1,000，常見硬幣是 ₩500 和 ₩100。遊戲的顏色和真鈔一樣，依序是黃、綠、紅、藍。|Tiền giấy có ₩50.000, ₩10.000, ₩5.000 và ₩1.000. Tiền xu hay gặp là ₩500 và ₩100. Màu trong trò chơi giống tiền thật: vàng, xanh lá, đỏ và xanh dương."),
]
