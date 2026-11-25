"""The moments that make the app worth installing (30차): the offline emergency screen, the food card,
"Refused?" in three taps, and trip mode (today only, the last day in order, calendar reminders).

Rules for this file:
- Everything here works on the phone alone. Personal choices stay in localStorage; the location is read only on a tap,
  turned into the rescue grid code on the phone, and never sent.
- Every number or rule carries its source (SRC here, TR.SRC, or a guide's own dated facts) and the day it was checked.
- Steps without a source are plain advice, never a claim about Korea.
- zh-cn is written by hand, not converted.
"""
from trouble import t5

CHK = "2026-11-25"   # day the new facts in this file were compared with their sources

SRC = {
    "grid": ("Ministry of the Interior notice: national point number origin (12 Dec 2012)", "https://www.ulex.co.kr/%EB%B2%95%EB%A5%A0/2200000078859-2107849-%EA%B5%AD%EA%B0%80"),
    "gg": ("Gyeonggi Province: the numbers that tell rescuers where you are", "https://www.gg.go.kr/myggd/vol204/3_3.php"),
    "sms119": ("Government24: 119 reports by text, app, web or video (updated 13 Nov 2026)", "https://www.gov.kr/portal/service/serviceInfo/PTR000052060"),
    "sms112": ("Korea policy briefing: reporting to 112 without speaking (27 Oct 2022)", "https://www.korea.kr/multi/visualNewsView.do?newsId=148907462"),
    "label": ("Ministry of Food and Drug Safety: 22 allergens on labels (14 Jul 2021)", "https://www.korea.kr/multi/visualNewsView.do?newsId=148890102"),
    "label28": ("Ministry of Food and Drug Safety: proposed label rule, notice 2026-386 (7 Aug 2026)", "https://mfds.go.kr/brd/m_209/view.do?seq=44285"),
    "icn_tax": ("Incheon Airport: tax refund steps", "https://www.airport.kr/ap_ko/898/subview.do"),
    "icn_customs": ("Incheon Airport Customs: tax refund check", "https://www.customs.go.kr/incheon_airport/cm/cntnts/cntntsView.do?mi=12546&cntntsId=6688"),
    "seoul_tax": ("Visit Seoul: tax refund", "https://english.visitseoul.net/taxrefund"),
    "sik": ("Study in Korea (government): registration and address rules", "https://www.studyinkorea.go.kr/ko/life/residenceAndStayInfo.do"),
    "hanam": ("Hanam City: address change report", "https://www.hanam.go.kr/english/contents.do?key=9642"),
}

# ---------------------------------------------------------------------------------------------- SOS
SOS = {
    "title": t5("Emergency", "緊急のとき", "緊急求助", "紧急求助", "Khẩn cấp"),
    "lede": t5("Call first. Then say where you are.", "まず電話。次に現在地を伝えます。", "先打電話,再說你在哪裡。", "先打电话,再说你在哪里。", "Gọi trước. Rồi nói bạn đang ở đâu."),
    "seo": t5("Emergency in Korea: call 119 or 112 and say exactly where you are, offline",
              "韓国での緊急時:119・112に電話し、現在地を正確に伝える(オフライン対応)",
              "在韓國遇到緊急狀況:打119或112,離線說出你的確切位置",
              "在韩国遇到紧急情况:拨打119或112,离线说出你的确切位置",
              "Khẩn cấp ở Hàn Quốc: gọi 119 hoặc 112 và nói chính xác bạn ở đâu, không cần mạng"),
    "desc": t5("One screen for an emergency in Korea: call 119, 112 or 1330, turn your spot into the rescue grid code on your phone without data, show or read it in Korean, or text it. Nothing is sent by us.",
               "韓国での緊急時に使う1画面。119・112・1330に電話し、現在地を通信なしで救助用の地点番号に変え、韓国語で見せる・読み上げる・文字で送れます。私たちには何も送信されません。",
               "韓國緊急時用的一個畫面:打119、112或1330,不用網路就把位置換成救援用的地點編號,用韓文給人看、唸出來或傳簡訊。我們不會收到任何資料。",
               "韩国紧急时用的一个画面:拨打119、112或1330,不用网络就把位置换成救援用的地点编号,用韩文给人看、念出来或发短信。我们不会收到任何数据。",
               "Một màn hình cho lúc khẩn cấp ở Hàn Quốc: gọi 119, 112 hoặc 1330, đổi vị trí thành mã cứu hộ ngay trên điện thoại không cần mạng, cho xem, đọc hoặc nhắn tin bằng tiếng Hàn. Chúng tôi không nhận gì."),
    "row": t5("SOS: call, and say where you are", "SOS:電話と現在地", "SOS:打電話、說出位置", "SOS:打电话、说出位置", "SOS: gọi và nói vị trí"),
    "short": t5("SOS", "SOS", "SOS", "SOS", "SOS"),
    "n119": t5("Fire, ambulance", "火事・救急", "火災、救護車", "火灾、急救", "Cứu hỏa, cấp cứu"),
    "n112": t5("Police", "警察", "警察", "警察", "Cảnh sát"),
    "n1330": t5("Interpreter, 24 h", "通訳・24時間", "口譯,24小時", "口译,24小时", "Phiên dịch, 24 giờ"),
    "where": t5("Where am I?", "ここはどこ?", "我在哪裡?", "我在哪里?", "Tôi đang ở đâu?"),
    "where_sub": t5("Works without data. Nothing is sent.", "通信なしで使えます。送信はしません。", "不用網路,也不會傳送。", "不用网络,也不会发送。", "Không cần mạng. Không gửi đi đâu."),
    "finding": t5("Finding you…", "現在地を確認中…", "定位中…", "定位中…", "Đang tìm vị trí…"),
    "code_h": t5("Say this code to 119 or 112", "この番号を119・112に伝えます", "把這個編號告訴119或112", "把这个编号告诉119或112", "Nói mã này với 119 hoặc 112"),
    "acc": t5("within about {m} m", "誤差 約{m}m", "誤差約{m}公尺", "误差约{m}米", "sai số khoảng {m} m"),
    "rough": t5("Rough. Allow precise location or step outside, then tap again.", "誤差が大きめです。「正確な位置情報」を許可するか外に出て、もう一度。", "誤差較大。允許精確位置或到室外,再按一次。", "误差较大。允许精确位置或到室外,再按一次。", "Chưa chính xác. Cho phép vị trí chính xác hoặc ra ngoài rồi bấm lại."),
    "slow": t5("Still looking. Without data the first fix can take a minute outdoors. You can call now.", "確認中です。通信なしでは、外でも1分ほどかかることがあります。先に電話できます。", "還在定位。沒有網路時,在室外也可能要一分鐘。可以先打電話。", "还在定位。没有网络时,在室外也可能要一分钟。可以先打电话。", "Vẫn đang tìm. Không có mạng, ngoài trời có thể mất một phút. Bạn có thể gọi trước."),
    "again": t5("Check again", "もう一度", "再定位一次", "再定位一次", "Tìm lại"),
    "denied": t5("Location is off. Allow it for this app in the phone's settings, or read a number near you (below).",
                 "位置情報がオフです。スマホの設定で許可するか、近くの番号を読んでください(下)。",
                 "定位已關閉。請在手機設定允許,或唸附近的編號(見下方)。",
                 "定位已关闭。请在手机设置里允许,或念附近的编号(见下方)。",
                 "Vị trí đang tắt. Hãy cho phép trong cài đặt điện thoại, hoặc đọc số ở gần bạn (bên dưới)."),
    "none": t5("No position yet. Go outside or to a window and tap again.", "位置がまだ取れません。外か窓ぎわで、もう一度。", "還抓不到位置。到室外或窗邊再按一次。", "还定位不到。到室外或窗边再按一次。", "Chưa có vị trí. Ra ngoài hoặc đến gần cửa sổ rồi bấm lại."),
    "out": t5("You are outside Korea. This code covers Korea only.", "韓国の外にいます。この番号は韓国の中だけのものです。", "你不在韓國。這個編號只適用於韓國。", "你不在韩国。这个编号只适用于韩国。", "Bạn đang ở ngoài Hàn Quốc. Mã này chỉ dùng trong Hàn Quốc."),
    "what": t5("What happened?", "何があった?", "發生什麼事?", "发生什么事?", "Chuyện gì xảy ra?"),
    "show": t5("Show in Korean", "韓国語で見せる", "用韓文給人看", "用韩文给人看", "Cho xem tiếng Hàn"),
    "read": t5("Read it out on the call", "電話でこう読みます", "在電話裡這樣唸", "在电话里这样念", "Đọc thế này khi gọi"),
    "text": t5("Text {n}", "{n}に文字で送る", "傳簡訊給{n}", "发短信给{n}", "Nhắn tin {n}"),
    "text_sub": t5("Opens your messages app with the Korean text. You press Send.", "韓国語の文面でメッセージアプリが開きます。送信は自分で押します。", "會開啟簡訊App並帶入韓文,由你按傳送。", "会打开短信App并带入韩文,由你按发送。", "Mở ứng dụng tin nhắn với nội dung tiếng Hàn. Bạn tự bấm Gửi."),
    "cant": t5("Can't talk?", "話せないとき", "不方便說話?", "不方便说话?", "Không nói được?"),
    "cant_t": t5("119 and 112 take reports by text message. Give the place and what happened.", "119と112は文字メッセージでも受け付けます。場所と状況を書きます。", "119和112都接受簡訊報案,寫下地點和狀況。", "119和112都接受短信报警,写下地点和情况。", "119 và 112 nhận báo tin qua tin nhắn. Ghi địa điểm và chuyện xảy ra."),
    "cant_sim": t5("We have not confirmed texts from foreign SIMs. If it fails, call.", "海外SIMからの文字送信は未確認です。送れなければ電話を。", "國外SIM傳簡訊我們尚未確認。傳不出去就打電話。", "国外SIM发短信我们尚未确认。发不出去就打电话。", "Chúng tôi chưa xác nhận tin nhắn từ SIM nước ngoài. Nếu không gửi được, hãy gọi."),
    "web": t5("Data only? 119.go.kr takes reports online (Korean page).", "データ通信だけなら、119.go.krでも通報できます(韓国語ページ)。", "只有網路?可以用119.go.kr線上報案(韓文頁面)。", "只有网络?可以用119.go.kr在线报案(韩文页面)。", "Chỉ có mạng? Báo qua 119.go.kr (trang tiếng Hàn)."),
    "near": t5("No position? Read a number near you", "位置が取れないときは、近くの番号を読む", "抓不到位置?唸附近的編號", "定位不到?念附近的编号", "Không có vị trí? Đọc số ở gần bạn"),
    "near_li": [t5("Power pole: the plate has letters and digits, such as 0213Q552", "電柱:0213Q552のような英数字の札", "電線桿:像0213Q552這樣的英數編號", "电线杆:像0213Q552这样的英数编号", "Cột điện: biển có chữ và số, như 0213Q552"),
                t5("Elevator: the number inside the car", "エレベーター:かごの中の番号", "電梯:車廂裡的編號", "电梯:轿厢里的编号", "Thang máy: số bên trong buồng thang"),
                t5("Mountain or coast: the sign with 2 Korean letters and 8 digits", "山や海岸:ハングル2文字と数字8桁の標識", "山上或海邊:2個韓文字加8位數字的牌子", "山上或海边:2个韩文字加8位数字的牌子", "Núi hoặc biển: biển có 2 chữ Hàn và 8 chữ số"),
                t5("Motorway: the km sign every 200 m or so, with your direction", "高速道路:約200mごとの距離標と進行方向", "高速公路:約每200公尺的里程牌,加上行駛方向", "高速公路:约每200米的里程牌,加上行驶方向", "Cao tốc: biển km khoảng mỗi 200 m, kèm hướng đi")],
    "what_is": t5("Korea is divided into 10 m squares, each with its own code (국가지점번호), made for rescue calls.", "韓国全土を10m四方に区切った番号(국가지점번호)で、救助の通報用です。", "韓國全境以10公尺見方劃分,每格有自己的編號(국가지점번호),供救援通報使用。", "韩国全境以10米见方划分,每格有自己的编号(국가지점번호),供救援报警使用。", "Hàn Quốc được chia thành ô 10 m, mỗi ô có mã riêng (국가지점번호), dùng khi gọi cứu hộ."),
    "stay": t5("I'm at my stay", "宿にいます", "我在住宿地點", "我在住宿地点", "Tôi đang ở chỗ ở"),
    "code_what": t5("What is this code?", "この番号は?", "這是什麼編號?", "这是什么编号?", "Mã này là gì?"),
    "said": t5("Computed on this phone.", "このスマホの中で計算しました。", "在這支手機裡計算。", "在这部手机里计算。", "Tính ngay trên điện thoại này."),
}

# What happened: id, number to call, label, Korean, romanization, katakana.
SOS_WHAT = [
    ("hurt", "119", t5("Hurt or sick", "けが・急病", "受傷或生病", "受伤或生病", "Bị thương, ốm"), "사람이 다쳤거나 아파요. 구급차를 보내 주세요.",
     "sarami dachyeotgeona apayo. gugeupchareul bonae juseyo.", "サラミ タチョッコナ アパヨ。クグプチャルル ポネ ジュセヨ。"),
    ("fire", "119", t5("Fire", "火事", "火災", "火灾", "Cháy"), "불이 났어요.", "buri nasseoyo.", "プリ ナッソヨ。"),
    ("crash", "119", t5("Road accident", "交通事故", "交通事故", "交通事故", "Tai nạn"), "교통사고가 났어요.", "gyotong-sagoga nasseoyo.", "キョトンサゴガ ナッソヨ。"),
    ("lost", "119", t5("Lost outdoors", "山・海で遭難", "在野外迷路", "在野外迷路", "Lạc ở núi, biển"), "길을 잃었어요. 구조해 주세요.", "gireul ireosseoyo. gujohae juseyo.", "キルル イロッソヨ。クジョヘ ジュセヨ。"),
    ("threat", "112", t5("In danger", "身の危険", "受到威脅", "受到威胁", "Bị đe dọa"), "위협을 받고 있어요. 경찰을 보내 주세요.", "wihyeobeul batgo isseoyo. gyeongchareul bonae juseyo.", "ウィヒョブル パッコ イッソヨ。キョンチャルル ポネ ジュセヨ。"),
    ("theft", "112", t5("Robbed", "盗難", "被偷或被搶", "被偷或被抢", "Bị cướp, trộm"), "물건을 도둑맞았어요.", "mulgeoneul dodungmajasseoyo.", "ムルゴヌル トドゥンマジャッソヨ。"),
]
SOS_HELP = ("도와주세요.", "dowajuseyo.", "トワジュセヨ。")
SOS_HELP_M = t5("Help", "助けて", "求助", "求助", "Cứu tôi")
# "Please connect a ... interpreter": Korean, romanization, katakana, meaning
SOS_ITP = {
    "en": ("영어 통역을 연결해 주세요.", "yeongeo tongyeogeul yeongyeolhae juseyo.", "ヨンオ トンヨグル ヨンギョレ ジュセヨ。", "English interpreter, please"),
    "ja": ("일본어 통역을 연결해 주세요.", "ilboneo tongyeogeul yeongyeolhae juseyo.", "イルボノ トンヨグル ヨンギョレ ジュセヨ。", "日本語の通訳をお願いします"),
    "zh-tw": ("중국어 통역을 연결해 주세요.", "junggugeo tongyeogeul yeongyeolhae juseyo.", "チュングゴ トンヨグル ヨンギョレ ジュセヨ。", "請接中文口譯"),
    "zh-cn": ("중국어 통역을 연결해 주세요.", "junggugeo tongyeogeul yeongyeolhae juseyo.", "チュングゴ トンヨグル ヨンギョレ ジュセヨ。", "请接中文口译"),
    "vi": ("베트남어 통역을 연결해 주세요.", "beteunameo tongyeogeul yeongyeolhae juseyo.", "ベトゥナモ トンヨグル ヨンギョレ ジュセヨ。", "Xin nối phiên dịch tiếng Việt"),
}
SOS_LOC = ("제 위치는 국가지점번호 {c}입니다.", "je wichineun gukga-jijeom-beonho {c} imnida.", "チェ ウィチヌン クッカ ジジョム ボノ {c} イムニダ。")
SOS_ERR = ("오차는 약 {m}미터입니다.", "ochaneun yak {m} miteo imnida.", "オチャヌン ヤク {m} ミト イムニダ。")
SOS_LANG_KO = {"en": "영어", "ja": "일본어", "zh-tw": "중국어", "zh-cn": "중국어", "vi": "베트남어"}

# ---------------------------------------------------------------------------------------------- food card
# id, Korean on the card, word to look for on a package (None: not on Korea's label list), names, shown first
ALLERGY = [
    ("peanut", "땅콩", "땅콩", t5("Peanut", "ピーナッツ", "花生", "花生", "Lạc"), 1),
    ("nuts", "견과류", None, t5("Tree nuts", "ナッツ類", "堅果", "坚果", "Các loại hạt"), 1),
    ("shrimp", "새우", "새우", t5("Shrimp", "えび", "蝦", "虾", "Tôm"), 1),
    ("crab", "게", "게", t5("Crab", "かに", "蟹", "蟹", "Cua"), 1),
    ("shell", "조개류", "조개류(굴, 전복, 홍합 포함)", t5("Shellfish", "貝類", "貝類", "贝类", "Sò, hàu"), 1),
    ("fish", "생선", None, t5("Fish", "魚", "魚", "鱼", "Cá"), 1),
    ("egg", "계란", "알류 (계란)", t5("Egg", "卵", "雞蛋", "鸡蛋", "Trứng"), 1),
    ("milk", "우유", "우유", t5("Milk", "乳", "牛奶", "牛奶", "Sữa"), 1),
    ("wheat", "밀", "밀", t5("Wheat", "小麦", "小麥", "小麦", "Lúa mì"), 1),
    ("soy", "콩", "대두", t5("Soy", "大豆", "大豆", "大豆", "Đậu nành"), 1),
    ("sesame", "참깨", None, t5("Sesame", "ごま", "芝麻", "芝麻", "Vừng"), 1),
    ("buckwheat", "메밀", "메밀", t5("Buckwheat", "そば", "蕎麥", "荞麦", "Kiều mạch"), 1),
    ("walnut", "호두", "호두", t5("Walnut", "くるみ", "核桃", "核桃", "Óc chó"), 0),
    ("pine", "잣", "잣", t5("Pine nut", "松の実", "松子", "松子", "Hạt thông"), 0),
    ("mackerel", "고등어", "고등어", t5("Mackerel", "さば", "鯖魚", "鲭鱼", "Cá thu"), 0),
    ("squid", "오징어", "오징어", t5("Squid", "いか", "魷魚", "鱿鱼", "Mực"), 0),
    ("pork", "돼지고기", "돼지고기", t5("Pork", "豚肉", "豬肉", "猪肉", "Thịt lợn"), 0),
    ("beef", "쇠고기", "쇠고기", t5("Beef", "牛肉", "牛肉", "牛肉", "Thịt bò"), 0),
    ("chicken", "닭고기", "닭고기", t5("Chicken", "鶏肉", "雞肉", "鸡肉", "Thịt gà"), 0),
    ("peach", "복숭아", "복숭아", t5("Peach", "桃", "桃子", "桃子", "Đào"), 0),
    ("tomato", "토마토", "토마토", t5("Tomato", "トマト", "番茄", "番茄", "Cà chua"), 0),
    ("sulfite", "아황산류", "아황산류", t5("Sulfites", "亜硫酸塩", "亞硫酸鹽", "亚硫酸盐", "Sunfit"), 0),
]
# Not eaten by choice or belief: id, Korean, names. The first five are whole diets and come first on the card.
AVOID = [
    ("vegan", "저는 비건이에요. 고기, 해산물, 계란, 유제품을 안 먹어요.", t5("Vegan", "ヴィーガン", "純素", "纯素", "Thuần chay"), "diet"),
    ("veg", "저는 채식주의자예요. 고기와 해산물을 안 먹어요.", t5("Vegetarian", "ベジタリアン", "素食", "素食", "Ăn chay"), "diet"),
    ("halal", "저는 할랄 음식을 먹어요. 돼지고기와 술을 안 먹어요.", t5("Halal", "ハラール", "清真", "清真", "Halal"), "diet"),
    ("glu", "저는 글루텐을 못 먹어요. 밀, 보리, 호밀이 들어간 음식을 못 먹어요.", t5("Gluten free", "グルテンフリー", "無麩質", "无麸质", "Không gluten"), "diet"),
    ("kosher", "저는 코셔 음식을 먹어요. 돼지고기와 조개·갑각류를 안 먹어요.", t5("Kosher", "コーシャ", "猶太潔食", "犹太洁食", "Kosher"), "diet"),
    ("a_meat", "고기", t5("Meat", "肉", "肉類", "肉类", "Thịt"), ""),
    ("a_pork", "돼지고기", t5("Pork", "豚肉", "豬肉", "猪肉", "Thịt lợn"), ""),
    ("a_beef", "쇠고기", t5("Beef", "牛肉", "牛肉", "牛肉", "Thịt bò"), ""),
    ("a_sea", "해산물", t5("Seafood", "魚介", "海鮮", "海鲜", "Hải sản"), ""),
    ("a_raw", "날음식", t5("Raw food", "生もの", "生食", "生食", "Đồ sống"), ""),
    ("a_alc", "술", t5("Alcohol", "酒", "酒", "酒", "Rượu"), ""),
    ("a_spicy", "매운 음식", t5("Spicy food", "辛いもの", "辣的食物", "辣的食物", "Đồ cay"), ""),
]
FOOD_KO = {"al": "알레르기가 있어요", "sev": "조금만 들어가도 위험해요.", "no": "안 먹어요", "ask": "이 음식에 들어가나요? 육수, 양념, 소스도 확인해 주세요."}
FOOD_ANS = [("안 들어가요", t5("Not in it", "入っていません", "沒有放", "没有放", "Không có")),
            ("들어가요", t5("It's in it", "入っています", "有放", "有放", "Có")),
            ("빼 드릴 수 있어요", t5("We can leave it out", "抜くことができます", "可以不放", "可以不放", "Có thể bỏ ra")),
            ("다른 메뉴를 드세요", t5("Pick another dish", "別の料理にしてください", "請改點別的", "请改点别的", "Hãy chọn món khác")),
            ("잘 모르겠어요", t5("Not sure", "分かりません", "不確定", "不确定", "Không chắc"))]
CARD = {
    "title": t5("My food card", "食事カード", "我的飲食卡", "我的饮食卡", "Thẻ ăn uống của tôi"),
    "short": t5("Food card", "食事カード", "飲食卡", "饮食卡", "Thẻ ăn"),
    "lede": t5("Tap once. Staff read it in Korean and tap an answer.", "一度選ぶだけ。スタッフは韓国語で読み、答えを押します。", "點選一次就好。店員看韓文並點選回答。", "点选一次就好。店员看韩文并点选回答。", "Chọn một lần. Nhân viên đọc tiếng Hàn và chạm câu trả lời."),
    "seo": t5("Korean food allergy and diet card you make by tapping (offline)", "タップで作る韓国語の食物アレルギー・食事カード(オフライン)", "點選製作的韓文食物過敏與飲食卡(離線)", "点选制作的韩文食物过敏与饮食卡(离线)", "Thẻ dị ứng thức ăn và ăn kiêng tiếng Hàn tạo bằng cách chạm (ngoại tuyến)"),
    "desc": t5("Tap the foods you can't or don't eat once. Get one big Korean card for restaurants, where staff tap a Korean answer you can read. Shows the Korean words to look for on packages. Stays on your phone.",
               "食べられないもの、食べないものを一度選ぶだけ。食堂で見せる大きな韓国語カードができ、スタッフが韓国語の答えを押すとあなたの言語で表示されます。包装で探す韓国語も表示。情報はスマホの中だけ。",
               "把不能吃、不吃的東西點選一次,就有一張給餐廳看的韓文大卡,店員點韓文回答,你看得懂。還會列出包裝上要找的韓文字。資料只留在手機裡。",
               "把不能吃、不吃的东西点选一次,就有一张给餐厅看的韩文大卡,店员点韩文回答,你看得懂。还会列出包装上要找的韩文字。数据只留在手机里。",
               "Chạm một lần để chọn món không ăn được hoặc không ăn. Có thẻ tiếng Hàn lớn cho nhà hàng: nhân viên chạm câu trả lời, bạn đọc được. Hiện cả từ tiếng Hàn cần tìm trên bao bì. Chỉ lưu trên điện thoại."),
    "al_h": t5("I'm allergic to", "アレルギーがある", "我對這些過敏", "我对这些过敏", "Tôi dị ứng với"),
    "no_h": t5("I don't eat", "食べないもの", "我不吃", "我不吃", "Tôi không ăn"),
    "more": t5("More", "もっと見る", "更多", "更多", "Thêm"),
    "sev": t5("Even a little is dangerous", "少しでも危険", "一點點也危險", "一点点也危险", "Chỉ một chút cũng nguy hiểm"),
    "food_btn": t5("Show to staff", "スタッフに見せる", "給店員看", "给店员看", "Cho nhân viên xem"),
    "empty": t5("Tap what applies to you.", "当てはまるものを選びます。", "點選符合你的項目。", "点选符合你的项目。", "Chạm vào mục đúng với bạn."),
    "label_h": t5("Look for these words on packages", "包装でこの文字を探します", "在包裝上找這些字", "在包装上找这些字", "Tìm các chữ này trên bao bì"),
    "label_no": t5("Korean labels don't have to list {x}. Ask.", "韓国の表示義務に {x} は入っていません。確認してください。", "韓國標示不強制列出{x},請詢問。", "韩国标签不强制列出{x},请询问。", "Nhãn Hàn Quốc không bắt buộc ghi {x}. Hãy hỏi."),
    "label_fish": t5("Only mackerel among fish is on the list.", "魚で対象なのはさばだけです。", "魚類只有鯖魚在清單上。", "鱼类只有鲭鱼在清单上。", "Trong các loại cá chỉ có cá thu nằm trong danh sách."),
    "label_nuts": t5("Walnut, pine nut and peanut must be on labels. Almond and cashew need not be. Ask.",
                     "くるみ・松の実・落花生は表示義務あり、アーモンドとカシューナッツは義務なしです。確認してください。",
                     "核桃、松子、花生必須標示;杏仁和腰果不強制,請詢問。",
                     "核桃、松子、花生必须标示;杏仁和腰果不强制,请询问。",
                     "Óc chó, hạt thông và lạc bắt buộc ghi trên nhãn; hạnh nhân và hạt điều thì không. Hãy hỏi."),
    "label_new": t5("Proposed in August 2026, not in force: adding sesame, perilla, almond and cashew.",
                    "2026年8月の改正案(未施行):ごま、えごま、アーモンド、カシューナッツを追加。",
                    "2026年8月的草案(尚未施行):加入芝麻、紫蘇籽、杏仁和腰果。",
                    "2026年8月的草案(尚未施行):加入芝麻、紫苏籽、杏仁和腰果。",
                    "Dự thảo tháng 8/2026, chưa có hiệu lực: thêm vừng, tía tô, hạnh nhân và hạt điều."),
    "note": t5("🔒 Kept only on this phone.", "🔒 このスマホの中だけに保存。", "🔒 只存在這支手機裡。", "🔒 只存在这部手机里。", "🔒 Chỉ lưu trên điện thoại này."),
    "clear": t5("Clear", "消す", "清除", "清除", "Xóa"),
    "row": t5("My food card", "食事カード", "我的飲食卡", "我的饮食卡", "Thẻ ăn uống của tôi"),
    "link_food": t5("My food card", "食事カード", "我的飲食卡", "我的饮食卡", "Thẻ ăn uống của tôi"),
    "set": t5("Saved", "保存済み", "已儲存", "已保存", "Đã lưu"),
    "unset": t5("Make it in 10 seconds", "10秒で作れます", "10秒完成", "10秒完成", "Tạo trong 10 giây"),
}

# ---------------------------------------------------------------------------------------------- Refused? in three taps
# problem: id, label, do now, if that fails, Korean cards (ko + meaning), guide whose dated answer backs it (None = plain advice), link to a trouble screen
_c = lambda ko, *m: (ko, t5(*m))
K_INSERT = _c("카드를 꽂아서 결제해 주세요.", "Please insert the card instead of tapping.", "カードを挿して決済してください。", "請插卡付款。", "请插卡付款。", "Vui lòng cắm thẻ thay vì chạm.")
K_WON = _c("원화로 결제해 주세요.", "Please charge me in Korean won.", "ウォン建てで決済してください。", "請用韓元結帳。", "请用韩元结账。", "Vui lòng tính bằng won Hàn Quốc.")
K_OTHER = _c("카드가 안 돼요. 다른 방법으로 결제할 수 있나요?", "My card isn't working. Can I pay another way?", "カードが使えません。別の方法で払えますか?", "卡刷不過,可以用別的方式付款嗎?", "卡刷不了,可以用别的方式付款吗?", "Thẻ của tôi không dùng được. Tôi trả cách khác được không?")
K_KIOSK = _c("키오스크에서 결제가 안 돼요. 카운터에서 계산해도 되나요?", "The kiosk won't take my card. Can I pay at the counter?", "キオスクで決済できません。レジで払えますか?", "自助點餐機刷不過,可以在櫃檯付嗎?", "自助机刷不了,可以在柜台付吗?", "Máy không nhận thẻ. Tôi trả ở quầy được không?")
K_WAIT = _c("한국 번호가 없는데 대기 명단에 올려 주실 수 있나요?", "I don't have a Korean number. Could you add me to the waitlist?", "韓国の番号がありません。順番待ちに入れてもらえますか?", "我沒有韓國號碼,可以幫我登記候位嗎?", "我没有韩国号码,可以帮我登记排队吗?", "Tôi không có số Hàn. Thêm tôi vào danh sách chờ được không?")
K_DIRECT = _c("기사님께 직접 결제할게요.", "I'll pay you directly.", "運転手さんに直接払います。", "我直接付給司機。", "我直接付给司机。", "Tôi sẽ trả trực tiếp cho tài xế.")
K_METER = _c("미터기를 켜 주세요.", "Please turn on the meter.", "メーターを使ってください。", "請開表。", "请打表。", "Vui lòng bật đồng hồ.")
K_TAXI_CALL = _c("택시를 불러 주실 수 있나요?", "Could you call a taxi for me?", "タクシーを呼んでもらえますか?", "可以幫我叫計程車嗎?", "可以帮我叫出租车吗?", "Bạn gọi taxi giúp tôi được không?")
K_TOPUP = _c("티머니 충전해 주세요. 만 원이요.", "Please top up my T-money. 10,000 won.", "T-moneyに1万ウォンチャージしてください。", "請幫我加值T-money一萬韓元。", "请给我的T-money充一万韩元。", "Nạp T-money giúp tôi, 10.000 won.")
K_GATE = _c("개찰구에서 카드가 안 찍혀요. 도와주세요.", "My card won't work at the gate. Please help.", "改札でカードが反応しません。助けてください。", "閘門刷不過卡,請幫忙。", "闸机刷不了卡,请帮忙。", "Thẻ không qua được cổng. Giúp tôi với.")
K_TRAIN = _c("창구에서 외국 카드로 표를 살 수 있어요?", "Can I buy a ticket here with a foreign card?", "窓口で海外カードで切符を買えますか?", "櫃檯可以用國外卡買票嗎?", "窗口可以用外国卡买票吗?", "Tôi mua vé ở quầy bằng thẻ nước ngoài được không?")
K_ATM = _c("외국 카드 되는 ATM이 어디 있어요?", "Where is an ATM that takes foreign cards?", "海外カードが使えるATMはどこですか?", "哪裡有可用國外卡的ATM?", "哪里有可用外国卡的ATM?", "ATM nhận thẻ nước ngoài ở đâu?")
K_ATE = _c("ATM에서 카드가 안 나와요. 도와주세요.", "The ATM kept my card. Please help.", "ATMからカードが出てきません。助けてください。", "ATM把我的卡吃掉了,請幫忙。", "ATM吞了我的卡,请帮忙。", "ATM nuốt thẻ của tôi. Giúp tôi với.")
K_TAXFREE = _c("택스 프리 해 주세요. 한 번에 계산할게요.", "Tax free, please. I'll pay for everything at once.", "免税でお願いします。まとめて会計します。", "請辦退稅,我一次結帳。", "请办退税,我一次结账。", "Cho tôi hoàn thuế. Tôi trả một lần.")
K_ORDER = _c("배달 주문 좀 도와주실 수 있나요?", "Could you help me order delivery?", "出前の注文を手伝ってもらえますか?", "可以幫我叫外送嗎?", "可以帮我点外卖吗?", "Bạn giúp tôi đặt giao đồ ăn được không?")
K_NOKR = _c("한국 전화번호가 없어요. 다른 방법이 있나요?", "I don't have a Korean phone number. Is there another way?", "韓国の電話番号がありません。別の方法はありますか?", "我沒有韓國電話號碼,有別的方法嗎?", "我没有韩国电话号码,有别的方法吗?", "Tôi không có số Hàn Quốc. Có cách nào khác không?")

_CASH = t5("Pay cash. Global ATMs and those in CU, GS25 and 7-Eleven take foreign cards. Choose KRW.", "現金で払います。GlobalのATMやCU・GS25・セブンのATMで海外カードが使えます。KRWを選びます。", "付現金。標示Global的ATM和CU、GS25、7-Eleven的ATM可用國外卡,選KRW。", "付现金。标有Global的ATM和CU、GS25、7-Eleven的ATM可用外国卡,选KRW。", "Trả tiền mặt. ATM có chữ Global và ATM ở CU, GS25, 7-Eleven nhận thẻ nước ngoài. Chọn KRW.")
_NOW_TILL = t5("Ask them to insert the card, charged in won. Then try your other card.", "挿し込み+ウォン建てを頼みます。次に別のカードを試します。", "請店員插卡、用韓元結帳,再試另一張卡。", "请店员插卡、用韩元结账,再试另一张卡。", "Nhờ cắm thẻ và tính bằng won. Rồi thử thẻ khác.")

REFUSED = [
    ("eat", "food-booking", t5("Restaurant", "食堂", "餐廳", "餐厅", "Nhà hàng"), [
        ("card", t5("Card refused", "カードが通らない", "刷卡失敗", "刷卡失败", "Thẻ bị từ chối"), _NOW_TILL, _CASH, [K_INSERT, K_WON, K_OTHER], "cash"),
        ("kiosk", t5("Kiosk won't work", "キオスクが使えない", "點餐機不能用", "自助机不能用", "Máy gọi món không được"),
         t5("Ask to order and pay at the counter.", "レジで注文と会計を頼みます。", "請在櫃檯點餐和結帳。", "请在柜台点餐和结账。", "Nhờ gọi món và trả tiền ở quầy."), _CASH, [K_KIOSK], "cash"),
        ("num", t5("Waitlist wants a Korean number", "順番待ちに韓国の番号が必要", "候位要韓國號碼", "排队要韩国号码", "Danh sách chờ cần số Hàn"),
         t5("Ask staff to add you by hand.", "スタッフに手入力を頼みます。", "請店員手動幫你登記。", "请店员手动帮你登记。", "Nhờ nhân viên ghi tên giúp."),
         t5("Next time, book on CatchTable Global (email sign-up).", "次回はCatchTable Global(メール登録)で予約を。", "下次用CatchTable Global(電子郵件註冊)訂位。", "下次用CatchTable Global(邮箱注册)订位。", "Lần sau đặt qua CatchTable Global (đăng ký bằng email)."), [K_WAIT], "food-booking"),
    ]),
    ("taxi", "taxi", t5("Taxi", "タクシー", "計程車", "出租车", "Taxi"), [
        ("app", t5("App refuses card or number", "アプリでカード・番号が通らない", "App不收卡或號碼", "App不收卡或号码", "Ứng dụng từ chối thẻ, số"),
         t5("Use k.ride (Google, Apple or email sign-up) or Uber. In Kakao T choose pay-to-driver.", "k.ride(Google・Apple・メール登録)かUberを使います。Kakao Tなら運転手に直接払いを選びます。", "用k.ride(Google、Apple或電子郵件註冊)或Uber。Kakao T選直接付給司機。", "用k.ride(Google、Apple或邮箱注册)或Uber。Kakao T选直接付给司机。", "Dùng k.ride (đăng ký bằng Google, Apple hoặc email) hoặc Uber. Với Kakao T, chọn trả cho tài xế."),
         t5("Go to a taxi rank, or ask your hotel to call one.", "タクシー乗り場へ行くか、宿に呼んでもらいます。", "到計程車招呼站,或請飯店叫車。", "到出租车站,或请酒店叫车。", "Ra bến taxi hoặc nhờ khách sạn gọi."), [K_DIRECT, K_TAXI_CALL], "taxi"),
        ("addr", t5("Driver doesn't know the place", "場所が通じない", "司機不知道地方", "司机不知道地方", "Tài xế không biết chỗ"),
         t5("Show the address in Korean, full screen.", "韓国語の住所を全画面で見せます。", "用全螢幕出示韓文地址。", "用全屏出示韩文地址。", "Cho xem địa chỉ tiếng Hàn toàn màn hình."),
         t5("Call 1330 and hand over the phone.", "1330に電話して、電話を渡します。", "打1330,把電話交給司機。", "拨打1330,把电话交给司机。", "Gọi 1330 rồi đưa máy cho tài xế."), ["ADDR"], "taxi"),
        ("fare", t5("Overcharged", "高く請求された", "被多收錢", "被多收钱", "Bị tính đắt"),
         t5("Ask for the meter and a receipt. Don't argue in the car.", "メーターと領収書を頼みます。車内で言い争わないこと。", "要求開表和收據,不要在車上爭執。", "要求打表和收据,不要在车上争执。", "Yêu cầu bật đồng hồ và lấy hóa đơn. Đừng cãi trên xe."),
         t5("See the taxi trouble screen for where to report.", "通報先は「タクシーのトラブル」の画面へ。", "檢舉方式見「計程車糾紛」畫面。", "举报方式见“出租车纠纷”画面。", "Xem màn hình sự cố taxi để biết nơi báo."), [K_METER, _c("영수증 주세요.", "A receipt, please.", "領収書をください。", "請給我收據。", "请给我收据。", "Cho tôi hóa đơn.")], "flow:taxi"),
    ]),
    ("ride", "transit", t5("Subway, bus", "地下鉄・バス", "地鐵、公車", "地铁、公交", "Tàu điện, xe buýt"), [
        ("top", t5("Can't top up", "チャージできない", "無法加值", "无法充值", "Không nạp được"),
         t5("Top up in cash: convenience store counter or station machine.", "現金でチャージ:コンビニのレジか駅の機械。", "用現金加值:便利商店櫃檯或車站機器。", "用现金充值:便利店柜台或车站机器。", "Nạp bằng tiền mặt: quầy cửa hàng tiện lợi hoặc máy ở ga."), _CASH, [K_TOPUP], "transit"),
        ("gate", t5("Gate won't open", "改札が開かない", "閘門不開", "闸机不开", "Cổng không mở"),
         t5("Press the help button at the gate, or show this to staff.", "改札の呼び出しボタンを押すか、駅員にこれを見せます。", "按閘門旁的呼叫鈕,或給站務員看這張。", "按闸机旁的呼叫按钮,或给站务员看这张。", "Bấm nút trợ giúp ở cổng hoặc cho nhân viên xem."),
         t5("Buy a T-money card at a convenience store.", "コンビニでT-moneyカードを買います。", "在便利商店買T-money卡。", "在便利店买T-money卡。", "Mua thẻ T-money ở cửa hàng tiện lợi."), [K_GATE], "transit"),
        ("last", t5("No more trains", "終電がない", "沒有末班車了", "没有末班车了", "Hết tàu"),
         t5("Look for an N night bus in Naver Map, or take a taxi.", "Naver MapでN(深夜)バスを探すか、タクシーで。", "在Naver Map找N字頭夜間公車,或搭計程車。", "在Naver Map找N字头夜间公交,或打车。", "Tìm xe buýt đêm N trong Naver Map hoặc đi taxi."),
         t5("See the missed-last-train screen.", "「終電を逃した」の画面へ。", "見「錯過末班車」畫面。", "见“错过末班车”画面。", "Xem màn hình lỡ chuyến cuối."), [K_TAXI_CALL], "flow:train"),
    ]),
    ("train", "ktx", t5("KTX train", "KTX", "KTX", "KTX", "Tàu KTX"), [
        ("pay", t5("Card refused online", "オンラインでカードが通らない", "線上刷卡失敗", "网上刷卡失败", "Thẻ bị từ chối trên mạng"),
         t5("Use KORAIL's English site. If it fails: KORAIL+ app, or Klook.", "KORAILの英語サイトで。だめならKORAIL+アプリかKlook。", "用KORAIL英文網站;不行就用KORAIL+或Klook。", "用KORAIL英文网站;不行就用KORAIL+或Klook。", "Dùng trang tiếng Anh của KORAIL. Nếu lỗi: KORAIL+ hoặc Klook."),
         t5("Buy at a station counter.", "駅の窓口で買います。", "到車站櫃檯買。", "到车站窗口买。", "Mua ở quầy ga."), [K_TRAIN], "ktx"),
        ("num", t5("Asks for a Korean number", "韓国の番号を求められる", "要韓國號碼", "要韩国号码", "Đòi số Hàn"),
         t5("Book on the English site with your passport details.", "英語サイトでパスポート情報を使って予約します。", "在英文網站用護照資料訂票。", "在英文网站用护照资料订票。", "Đặt trên trang tiếng Anh bằng hộ chiếu."),
         t5("Buy at a station counter.", "駅の窓口で買います。", "到車站櫃檯買。", "到车站窗口买。", "Mua ở quầy ga."), [K_TRAIN], "ktx"),
    ]),
    ("shop", "shopping", t5("Shop", "お店", "商店", "商店", "Cửa hàng"), [
        ("card", t5("Card refused", "カードが通らない", "刷卡失敗", "刷卡失败", "Thẻ bị từ chối"), _NOW_TILL, _CASH, [K_INSERT, K_WON, K_OTHER], "cash"),
        ("tax", t5("No tax refund", "免税にならない", "不能退稅", "不能退税", "Không hoàn thuế"),
         t5("Show your actual passport and pay 15,000 won or more in one payment.", "本物のパスポートを見せ、1回で15,000ウォン以上払います。", "出示護照正本,一次付滿15,000韓元。", "出示护照原件,一次付满15,000韩元。", "Đưa hộ chiếu gốc và trả từ 15.000 won trong một lần."),
         t5("Not a tax-free shop? Then no refund. Look for the Tax Free sign.", "免税店でなければ対象外です。Tax Freeの表示を探します。", "不是退稅店就無法退,請找Tax Free標誌。", "不是退税店就无法退,请找Tax Free标志。", "Không phải cửa hàng Tax Free thì không hoàn. Tìm biển Tax Free."), [K_TAXFREE], "shopping"),
    ]),
    ("atm", "cash", t5("ATM", "ATM", "ATM", "ATM", "ATM"), [
        ("rej", t5("Rejects my card", "カードを受け付けない", "不收我的卡", "不收我的卡", "Từ chối thẻ"),
         t5("Find one marked Global, or in CU, GS25 or 7-Eleven. Use a debit card, choose KRW.", "Globalの表示か、CU・GS25・セブンのATMへ。デビットカードでKRWを選びます。", "找標示Global的,或CU、GS25、7-Eleven的ATM。用金融卡,選KRW。", "找标有Global的,或CU、GS25、7-Eleven的ATM。用借记卡,选KRW。", "Tìm máy có chữ Global hoặc ở CU, GS25, 7-Eleven. Dùng thẻ ghi nợ, chọn KRW."),
         t5("Try a big bank such as KB or Woori, or exchange cash.", "KBやWooriなど大手銀行のATMか、両替で。", "試KB、Woori等大銀行的ATM,或換錢。", "试KB、Woori等大银行的ATM,或换钱。", "Thử ngân hàng lớn như KB, Woori, hoặc đổi tiền mặt."), [K_ATM], "cash"),
        ("kept", t5("Kept my card", "カードが出てこない", "吃卡了", "吞卡了", "Nuốt thẻ"),
         t5("Call the number on the machine, and block the card with your bank.", "機械に書かれた番号に電話し、自分の銀行でカードを止めます。", "打機器上的電話,並向你的銀行停卡。", "打机器上的电话,并向你的银行挂失。", "Gọi số ghi trên máy và khóa thẻ với ngân hàng của bạn."),
         t5("1330 can interpret the call.", "1330が通訳してくれます。", "1330可以協助口譯。", "1330可以协助口译。", "1330 có thể phiên dịch."), [K_ATE], None),
    ]),
    ("app", "data", t5("App sign\u2011up", "アプリ登録", "App註冊", "App注册", "Đăng ký ứng dụng"), [
        ("food", t5("Food delivery", "フードデリバリー", "外送", "外卖", "Giao đồ ăn"),
         t5("Baemin: set English, use your home number or order as a guest.", "Baeminを英語にし、自国の番号かゲスト注文で。", "Baemin設成英文,用本國號碼或訪客下單。", "Baemin设成英文,用本国号码或访客下单。", "Baemin: chọn tiếng Anh, dùng số của bạn hoặc đặt với tư cách khách."),
         t5("Ask your host or front desk to order.", "宿の人に注文を頼みます。", "請住宿人員代訂。", "请住宿人员代订。", "Nhờ chủ nhà hoặc lễ tân đặt."), [K_ORDER], "delivery"),
        ("book", t5("Restaurant booking", "レストラン予約", "餐廳訂位", "餐厅订位", "Đặt bàn"),
         t5("CatchTable Global: sign up by email. Naver: verify with your passport.", "CatchTable Globalはメール登録。Naverはパスポート認証。", "CatchTable Global用電子郵件註冊;Naver用護照驗證。", "CatchTable Global用邮箱注册;Naver用护照验证。", "CatchTable Global: đăng ký bằng email. Naver: xác minh bằng hộ chiếu."),
         t5("Go in person and join the waitlist.", "お店に行って順番待ちに入ります。", "到店登記候位。", "到店登记排队。", "Đến tận nơi ghi danh sách chờ."), [K_WAIT], "food-booking"),
        ("id", t5("Identity check (본인인증)", "本人認証(본인인증)", "身分驗證(본인인증)", "身份验证(본인인증)", "Xác minh danh tính (본인인증)"),
         t5("Stop here. Without an ARC it usually fails, even with a Korean number.", "ここで止めます。外国人登録証がないと、韓国の番号があってもたいてい通りません。", "到此為止。沒有外國人登錄證,就算有韓國號碼通常也過不了。", "到此为止。没有外国人登录证,就算有韩国号码通常也过不了。", "Dừng ở đây. Không có thẻ cư trú thì thường không qua, dù có số Hàn."),
         t5("Use passport verification where offered, such as Naver.", "Naverのようにパスポート認証がある所ではそれを使います。", "有護照驗證的服務(如Naver)就用護照。", "有护照验证的服务(如Naver)就用护照。", "Dùng xác minh hộ chiếu nơi có, như Naver."), [K_NOKR], "data"),
        ("sms", t5("Code never arrives", "認証番号が届かない", "收不到驗證碼", "收不到验证码", "Không nhận được mã"),
         t5("A data-only eSIM can't receive Korean codes. You need a plan with a 010 number.", "データ専用eSIMでは韓国の認証番号は届きません。010番号つきのプランが必要です。", "純數據eSIM收不到韓國驗證碼,需要有010號碼的方案。", "纯数据eSIM收不到韩国验证码,需要有010号码的套餐。", "eSIM chỉ có dữ liệu không nhận được mã Hàn. Cần gói có số 010."),
         t5("Use an app that takes email or Google sign-up (see the guides).", "メールやGoogleで登録できるアプリを使います(ガイド参照)。", "改用可用電子郵件或Google註冊的App(見指南)。", "改用可用邮箱或Google注册的App(见指南)。", "Dùng ứng dụng đăng ký bằng email hoặc Google (xem hướng dẫn)."), [K_NOKR], "data"),
    ]),
    ("web", None, t5("Paying online", "ネット決済", "線上付款", "网上付款", "Thanh toán mạng"), [
        ("card", t5("Korean site refuses my card", "韓国サイトでカードが通らない", "韓國網站不收我的卡", "韩国网站不收我的卡", "Trang Hàn từ chối thẻ"),
         t5("Call your card issuer: allow payments in Korea and online. Then look for the English version of the site.", "カード会社に電話し、韓国とオンラインの決済を許可してもらいます。次に英語版サイトを探します。", "打給發卡銀行開通韓國與線上消費,再找該網站的英文版。", "打给发卡行开通韩国与线上消费,再找该网站的英文版。", "Gọi ngân hàng: cho phép thanh toán ở Hàn và trên mạng. Rồi tìm bản tiếng Anh của trang."),
         t5("Pay in person, or use a prepaid card for visitors (see Card refused).", "窓口で払うか、旅行者向けプリペイドカードを(「カードが使えない」参照)。", "現場付款,或用旅客預付卡(見「刷卡失敗」)。", "现场付款,或用旅客预付卡(见“刷卡失败”)。", "Trả trực tiếp, hoặc dùng thẻ trả trước cho khách (xem Thẻ bị từ chối)."), [K_OTHER], "flow:card"),
    ]),
]
RF = {
    "title": t5("Refused? 3 taps", "断られたら3タップ", "被拒絕?點三下", "被拒绝?点三下", "Bị từ chối? 3 lần chạm"),
    "short": t5("Refused?", "断られた", "被拒絕?", "被拒绝?", "Bị từ chối?"),
    "lede": t5("Where, what, then the one thing to do now.", "どこで、何が。今すぐやることを1つ。", "在哪裡、什麼事,然後告訴你現在做什麼。", "在哪里、什么事,然后告诉你现在做什么。", "Ở đâu, chuyện gì, rồi một việc cần làm ngay."),
    "seo": t5("Card refused or Korean number required in Korea? What to do now, by place", "韓国でカードや電話番号が通らないとき:場所別に今すぐやること", "在韓國被拒刷卡或要求韓國號碼?依地點告訴你現在怎麼做", "在韩国被拒刷卡或要求韩国号码?按地点告诉你现在怎么做", "Thẻ bị từ chối hoặc đòi số Hàn? Việc cần làm ngay theo từng nơi"),
    "desc": t5("Three taps: where you are, what was refused, and the one thing to do now with the Korean to show. Dated answers for restaurants, taxis, subway, KTX, shops, ATMs, app sign-ups and online payments. Works offline.",
               "3タップで、場所、断られた内容、今すぐやることと見せる韓国語。食堂、タクシー、地下鉄、KTX、お店、ATM、アプリ登録、オンライン決済の日付つきの答え。オフライン対応。",
               "點三下:你在哪裡、什麼被拒絕、現在做什麼和要出示的韓文。餐廳、計程車、地鐵、KTX、商店、ATM、App註冊、線上付款都有附日期的答案。離線可用。",
               "点三下:你在哪里、什么被拒绝、现在做什么和要出示的韩文。餐厅、出租车、地铁、KTX、商店、ATM、App注册、线上付款都有带日期的答案。离线可用。",
               "Ba lần chạm: bạn ở đâu, bị từ chối gì, và việc cần làm ngay cùng câu tiếng Hàn để cho xem. Câu trả lời có ngày cho nhà hàng, taxi, tàu điện, KTX, cửa hàng, ATM, đăng ký ứng dụng và thanh toán mạng. Dùng ngoại tuyến."),
    "row": t5("Refused? What to do now", "断られたとき、今やること", "被拒絕時現在怎麼做", "被拒绝时现在怎么做", "Bị từ chối? Việc cần làm ngay"),
    "q1": t5("Where?", "どこで?", "在哪裡?", "在哪里?", "Ở đâu?"),
    "q2": t5("What happened?", "何が?", "什麼狀況?", "什么情况?", "Chuyện gì?"),
    "now": t5("Do this now", "今すぐやること", "現在這樣做", "现在这样做", "Làm ngay"),
    "say": t5("Show this", "これを見せる", "給對方看", "给对方看", "Cho xem"),
    "fail": t5("If that fails", "だめなら", "還是不行", "还是不行", "Nếu không được"),
    "mine": t5("For your phone", "あなたのスマホの場合", "以你的手機來說", "以你的手机来说", "Với điện thoại của bạn"),
    "stuck": t5("Still stuck? 1330 interprets by phone", "まだ困ったら1330が電話で通訳", "還是卡住?1330電話口譯", "还是卡住?1330电话口译", "Vẫn kẹt? 1330 phiên dịch qua điện thoại"),
    "addr_none": t5("Save your stay address first (My trip).", "先に宿の住所を保存します(マイトリップ)。", "先儲存住宿地址(我的旅程)。", "先保存住宿地址(我的行程)。", "Lưu địa chỉ chỗ ở trước (Chuyến đi của tôi)."),
    "advice": t5("Plain advice, not a rule", "一般的な助言", "一般建議", "一般建议", "Lời khuyên chung"),
}

# ---------------------------------------------------------------------------------------------- trip mode
# id, stage, when, text, source keys (SRC / TR.SRC / guide:<task id>), check date (None = plain advice or the guide's own date), link, condition
#   when: ("from", -3) = days relative to arrival; ("to", 0) = relative to departure; ("day", n) = the n-th day
#   condition: "busan" (Busan picked in the Ready check), "visitor" (not arc), "long" (stay over 90 days or arc), None
DAYS = [
    ("ktx", "before", ("from", -60), t5("KTX tickets open two months ahead. Book yours.", "KTXの切符は2か月前から。予約しましょう。", "KTX票兩個月前開賣,可以訂了。", "KTX票两个月前开售,可以订了。", "Vé KTX mở bán trước hai tháng. Hãy đặt."), ["guide:ktx"], None, "guide:ktx", "busan"),
    ("keta", "before", ("from", -14), t5("Check if your passport needs K-ETA", "K-ETAが必要か確認", "確認護照是否需要K-ETA", "确认护照是否需要K-ETA", "Kiểm tra có cần K-ETA không"), ["guide:entry"], None, "guide:entry", "visitor"),
    ("card", "before", ("from", -7), t5("Make your food card", "食事カードを作る", "製作飲食卡", "制作饮食卡", "Tạo thẻ ăn uống"), [], None, "my-card.html", None),
    ("addr", "before", ("from", -7), t5("Save your stay address in Korean", "宿の住所を韓国語で保存", "儲存韓文住宿地址", "保存韩文住宿地址", "Lưu địa chỉ chỗ ở bằng tiếng Hàn"), [], None, "#f-addr", None),
    ("eac", "before", ("from", -3), t5("e-Arrival Card opens: 72 hours before landing", "e-Arrival Card受付開始(到着72時間前)", "e-Arrival Card開放(抵達前72小時)", "e-Arrival Card开放(抵达前72小时)", "e-Arrival Card mở: 72 giờ trước khi hạ cánh"), ["guide:entry"], None, "#f-arrive", "visitor"),
    ("off", "before", ("from", -1), t5("Check the offline pack is complete", "オフラインパックを確認", "確認離線包已下載完", "确认离线包已下载完", "Kiểm tra gói ngoại tuyến đã đủ"), [], None, "#f-pack", None),
    ("tmoney", "arrive", ("from", 0), t5("Buy T-money at a convenience store, top up in cash", "コンビニでT-moneyを買い、現金でチャージ", "在便利商店買T-money並用現金加值", "在便利店买T-money并用现金充值", "Mua T-money ở cửa hàng tiện lợi, nạp tiền mặt"), ["guide:transit"], None, "guide:transit", None),
    ("city", "arrive", ("from", 0), t5("To the city: train, bus or taxi", "市内へ:鉄道・バス・タクシー", "進市區:鐵路、巴士或計程車", "进市区:铁路、巴士或出租车", "Vào thành phố: tàu, xe buýt hoặc taxi"), ["guide:airport"], None, "guide:airport", None),
    ("tax1", "trip", ("day", 2), t5("Shopping? Carry your passport. Tax Free shops refund tax from 15,000 won in one payment", "買い物はパスポート持参。Tax Freeの店なら1回15,000ウォンから免税", "購物帶護照:Tax Free商店單筆滿15,000韓元可退稅", "购物带护照:Tax Free商店单笔满15,000韩元可退税", "Mua sắm nhớ mang hộ chiếu: cửa hàng Tax Free hoàn thuế từ 15.000 won mỗi lần trả"), ["seoul_tax", "icn_tax"], CHK, "guide:shopping", "visitor"),
    ("eve_bag", "eve", ("to", -1), t5("Pack tax-refund goods unopened and within reach", "免税品は未開封のまま、すぐ出せる所へ", "退稅商品別拆封,放在好拿的地方", "退税商品别拆封,放在好拿的地方", "Để hàng hoàn thuế còn nguyên, dễ lấy ra"), ["icn_tax"], CHK, None, "visitor"),
    ("eve_tm", "eve", ("to", -1), t5("Use up your T-money: refunding a small balance costs 500 won", "T-moneyは使い切る(少額の払い戻しは手数料500ウォン)", "用完T-money餘額:小額退款收500韓元", "用完T-money余额:小额退款收500韩元", "Dùng hết T-money: hoàn số dư nhỏ mất 500 won"), ["guide:transit"], "2026-11-20", "guide:transit", None),
    ("eve_bus", "eve", ("to", -1), t5("Check the first train or bus to the airport", "空港行きの始発を確認", "查往機場的首班車", "查往机场的首班车", "Xem chuyến đầu ra sân bay"), [], None, "guide:airport", None),
    ("go_bag", "leave", ("to", 0), t5("Refund goods in a checked bag? Tell the airline at check-in and get the tagged bag back (Incheon)", "預ける荷物に免税品があれば、チェックインで伝え、タグつきで返してもらう(仁川)", "托運行李有退稅品?報到時告訴航空公司,掛牌後先拿回行李(仁川)", "托运行李有退税品?值机时告诉航空公司,挂牌后先拿回行李(仁川)", "Hàng hoàn thuế trong hành lý ký gửi? Báo hãng khi check-in và nhận lại vali đã gắn thẻ (Incheon)"), ["icn_tax"], CHK, None, "visitor"),
    ("go_kiosk", "leave", ("to", 0), t5("Refund kiosk: scan passport and refund slips before the bag goes (Incheon)", "荷物を預け切る前に、免税キオスクでパスポートと書類を読み取る(仁川)", "行李送走前,先在退稅機掃護照和退稅單(仁川)", "行李送走前,先在退税机扫护照和退税单(仁川)", "Máy hoàn thuế: quét hộ chiếu và phiếu trước khi gửi hành lý (Incheon)"), ["icn_customs", "icn_tax"], CHK, None, "visitor"),
    ("go_cust", "leave", ("to", 0), t5("Kiosk says inspection? Customs desk: passport, unopened goods, slips", "検査と出たら税関カウンターへ:パスポート・未開封の品・書類", "顯示要查驗?到海關櫃檯:護照、未拆封商品、退稅單", "显示要查验?到海关柜台:护照、未拆封商品、退税单", "Máy báo kiểm tra? Đến quầy hải quan: hộ chiếu, hàng chưa mở, phiếu"), ["icn_tax"], CHK, None, "visitor"),
    ("go_cash", "leave", ("to", 0), t5("After security: refund machines 24 h, desks 7:00 to 22:00 (T1) or 21:30 (T2) (Incheon)", "保安検査後:払い戻し機は24時間、窓口は7時〜22時(T1)・21時30分(T2)(仁川)", "安檢後:退稅機24小時,櫃檯7:00–22:00(T1)、21:30止(T2)(仁川)", "安检后:退税机24小时,柜台7:00–22:00(T1)、21:30止(T2)(仁川)", "Sau an ninh: máy hoàn thuế 24 giờ, quầy 7:00–22:00 (T1) hoặc 21:30 (T2) (Incheon)"), ["icn_tax"], CHK, None, "visitor"),
    ("arc", "long", ("from", 90), t5("Staying over 90 days: register by this date", "90日を超える滞在:この日までに外国人登録", "停留超過90天:在這天前辦外國人登錄", "停留超过90天:在这天前办外国人登录", "Ở trên 90 ngày: đăng ký trước ngày này"), ["sik"], CHK, None, "long"),
    ("move", "long", None, t5("Moved? Report the new address within 15 days (14 for F-4 overseas Koreans)", "引っ越したら15日以内に住所変更を届け出(F-4の在外同胞は14日)", "搬家後15天內申報新地址(F-4海外同胞為14天)", "搬家后15天内申报新地址(F-4海外同胞为14天)", "Chuyển nhà? Báo địa chỉ mới trong 15 ngày (F-4 kiều bào: 14 ngày)"), ["sik", "hanam"], CHK, None, "long"),
]
TM = {
    "h": t5("Your days", "旅のしおり", "你的日程", "你的日程", "Lịch của bạn"),
    "need": t5("Add your dates. This screen then shows only what is due.", "日程を入れると、今やることだけが出ます。", "填入日期,這裡只顯示該做的事。", "填入日期,这里只显示该做的事。", "Nhập ngày, màn hình chỉ hiện việc đến hạn."),
    "cta": t5("Add your trip dates", "旅行の日程を入れる", "填入旅行日期", "填入旅行日期", "Nhập ngày đi"),
    "stages": {"before": t5("Before you fly", "出発前", "出發前", "出发前", "Trước khi bay"), "arrive": t5("Arrival day", "到着日", "抵達日", "抵达日", "Ngày đến"),
               "trip": t5("During the trip", "旅行中", "旅途中", "旅途中", "Trong chuyến đi"), "eve": t5("Day before you leave", "出発前日", "離開前一天", "离开前一天", "Ngày trước khi về"),
               "leave": t5("Leaving day, in this order", "帰国日(この順で)", "離開當天,照這個順序", "离开当天,按这个顺序", "Ngày về, theo thứ tự"), "long": t5("Staying longer", "長期滞在", "長期停留", "长期停留", "Ở lâu dài")},
    "to_go": t5("{n} days to go", "あと{n}日", "還有{n}天", "还有{n}天", "Còn {n} ngày"),
    "tomorrow": t5("You fly tomorrow", "明日出発", "明天出發", "明天出发", "Mai bay"),
    "day": t5("Day {n} of {m}", "{m}日中{n}日目", "第{n}天,共{m}天", "第{n}天,共{m}天", "Ngày {n}/{m}"),
    "leaving": t5("You leave today", "今日が帰国日", "今天離開", "今天离开", "Hôm nay về"),
    "nothing": t5("Nothing due today. Enjoy.", "今日の予定はありません。楽しんで。", "今天沒有要辦的事,好好玩。", "今天没有要办的事,好好玩。", "Hôm nay không có việc đến hạn."),
    "over": t5("Trip over? Erase your trip data.", "旅が終わったら、データを消せます。", "旅程結束?可清除旅程資料。", "行程结束?可清除行程数据。", "Hết chuyến? Xóa dữ liệu chuyến đi."),
    "remind": t5("Add to calendar", "カレンダーに追加", "加入行事曆", "加入日历", "Thêm vào lịch"),
    "remind_note": t5("🔔 saves a calendar file. Your calendar app rings, even if this app is closed.", "🔔 でカレンダー用のファイルを保存。このアプリを閉じていても、カレンダーが知らせます。", "🔔 會存一個行事曆檔。就算關掉本App,行事曆也會提醒。", "🔔 会保存一个日历文件。就算关掉本App,日历也会提醒。", "🔔 lưu tệp lịch. Ứng dụng lịch sẽ nhắc, kể cả khi đóng ứng dụng này."),
    "saved": t5("Calendar file saved. Open it to add.", "カレンダー用ファイルを保存しました。開いて追加します。", "已存行事曆檔,打開即可加入。", "已保存日历文件,打开即可加入。", "Đã lưu tệp lịch. Mở tệp để thêm."),
    "moved": t5("Moved on", "引っ越した日", "搬家日期", "搬家日期", "Ngày chuyển"),
    "by": t5("Report by {d}", "{d}までに届け出", "{d}前申報", "{d}前申报", "Báo trước {d}"),
    "next": t5("Next", "次", "下一步", "下一步", "Tiếp theo"),
    "now": t5("Now", "今", "現在", "现在", "Ngay bây giờ"),
    "all": t5("See all days", "すべて見る", "看全部", "看全部", "Xem tất cả"),
}
MOS_LABEL = t5("Quick help", "すぐ使う", "快速求助", "快速求助", "Trợ giúp nhanh")
FOLD_LBL = {"#f-addr": "f_addr", "#f-arrive": "f_arrive", "#f-pack": "pack_h"}   # keys of app_shell.T, for links to a My trip row
