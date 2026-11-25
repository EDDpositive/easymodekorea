"""Prices for the daily Seoul price game (33차). One row = one price that a dated official page states.

A row is dropped when no official page gives the number: no guesses, no blogs, no brands, no private shops.
Text order in every "a|b|c|d" string: English | Japanese | Traditional Chinese | Vietnamese (Simplified Chinese is derived).
Append new rows at the end of an ORDER list so that earlier days keep their set. See docs/won-game.md.
"""
CHK = "2026-11-25"  # the day every page below was read
# Won for one unit, Korea Customs Service weekly rate, in force from that Sunday (read 2026-11-25). The Vietnamese page uses the dollar: that list has no dong.
FX = {"src": "https://unipass.customs.go.kr/clip/infocomn/retrieveTrifFxrt.do", "from": "2026-11-22", "USD": 1333.88, "JPY": 8.3599, "TWD": 40.47, "CNY": 199.99}

# key: (official page, date of the value, kind, page name en|ja|tw|vi). kind: survey (monthly average), retail (daily average), fixed (official price list, in force when read)
SRC = {
    "eat": ("https://www.price.go.kr/tprice/portal/servicepriceinfo/dineoutprice/dineOutPriceList.do", "2026-10", "survey", "price.go.kr, eating out|price.go.kr 外食費|price.go.kr 外食價格|price.go.kr, giá ăn ngoài"),
    "svc": ("https://www.price.go.kr/tprice/portal/servicepriceinfo/serviceindustryprice/serviceIndustryPriceList.do", "2026-10", "survey", "price.go.kr, personal services|price.go.kr サービス料金|price.go.kr 個人服務價格|price.go.kr, giá dịch vụ"),
    "pub": ("https://www.price.go.kr/tprice/portal/servicepriceinfo/publicutilitypirce/publicUtilityPirceList.do", "2026-10", "survey", "price.go.kr, public charges|price.go.kr 公共料金|price.go.kr 公共費用|price.go.kr, phí công cộng"),
    "k100": ("https://www.kamis.or.kr/customer/price/agricultureRetail/catalogue.do?action=daily&regday=2026-11-24&countycode=1101&itemcategorycode=100&convert_kg_yn=N", "2026-11-24", "retail", "KAMIS grain prices|KAMIS 穀物価格|KAMIS 穀物價格|KAMIS, giá ngũ cốc"),
    "k200": ("https://www.kamis.or.kr/customer/price/agricultureRetail/catalogue.do?action=daily&regday=2026-11-24&countycode=1101&itemcategorycode=200&convert_kg_yn=N", "2026-11-24", "retail", "KAMIS vegetable prices|KAMIS 野菜価格|KAMIS 蔬菜價格|KAMIS, giá rau"),
    "k300": ("https://www.kamis.or.kr/customer/price/agricultureRetail/catalogue.do?action=daily&regday=2026-11-24&countycode=1101&itemcategorycode=300&convert_kg_yn=N", "2026-11-24", "retail", "KAMIS special crop prices|KAMIS 特用作物価格|KAMIS 特用作物價格|KAMIS, giá nông sản khác"),
    "k400": ("https://www.kamis.or.kr/customer/price/agricultureRetail/catalogue.do?action=daily&regday=2026-11-24&countycode=1101&itemcategorycode=400&convert_kg_yn=N", "2026-11-24", "retail", "KAMIS fruit prices|KAMIS 果物価格|KAMIS 水果價格|KAMIS, giá trái cây"),
    "k600": ("https://www.kamis.or.kr/customer/price/fisheriesRetail/catalogue.do?action=daily&regday=2026-11-24&countycode=1101&itemcategorycode=600&convert_kg_yn=N", "2026-11-24", "retail", "KAMIS seafood prices|KAMIS 水産物価格|KAMIS 水產價格|KAMIS, giá hải sản"),
    "fare": ("https://news.seoul.go.kr/traffic/traffic_price", "2026-11-25", "fixed", "Seoul City fares|ソウル市 交通運賃|首爾市交通費率|Giá vé của thành phố Seoul"),
    "busf": ("https://news.seoul.go.kr/traffic/archives/1706", "2026-11-25", "fixed", "Seoul City bus fares|ソウル市 バス運賃|首爾市公車費率|Giá xe buýt của thành phố Seoul"),
    "taxi": ("https://news.seoul.go.kr/traffic/archives/1659", "2026-11-25", "fixed", "Seoul City taxi fares|ソウル市 タクシー運賃|首爾市計程車費率|Giá taxi của thành phố Seoul"),
    "bike": ("https://www.bikeseoul.com/info/infoCoupon.do", "2026-11-25", "fixed", "Ttareungi (Seoul public bike)|タルンイ（ソウル公共自転車）|叮鈴鈴（首爾公共自行車）|Ttareungi (xe đạp công cộng Seoul)"),
    "boat": ("https://hgbus.co.kr/itc/information/fee?menuId=33", "2026-11-25", "fixed", "Hangang Bus fares|漢江バス 運賃|漢江巴士費率|Giá vé Hangang Bus"),
    "toll": ("https://www.sisul.or.kr/open_content/traffic/toll/guide.jsp", "2026-11-25", "fixed", "Seoul Facilities Corporation|ソウル施設公団|首爾設施公團|Tổng công ty Cơ sở Seoul"),
    "royal": ("https://royal.khs.go.kr/ROYAL/contents/R703000000.do", "2026-11-25", "fixed", "Royal Palaces and Tombs Center|宮陵遺跡本部|宮陵遺跡本部|Trung tâm Cung và Lăng Hoàng gia"),
    "park": ("https://grandpark.seoul.go.kr/conts/contsView/ko/S001001001001.do", "2026-11-25", "fixed", "Seoul Grand Park|ソウル大公園|首爾大公園|Seoul Grand Park"),
    "dal": ("https://mediahub.seoul.go.kr/archives/2017639", "2026-03-31", "fixed", "Seoul City news|ソウル市のお知らせ|首爾市公告|Tin của thành phố Seoul"),
    "swim": ("https://mediahub.seoul.go.kr/archives/2018519", "2026-06", "fixed", "Seoul City news|ソウル市のお知らせ|首爾市公告|Tin của thành phố Seoul"),
    "sema": ("https://sema.seoul.go.kr/kr/visit/seosomun", "2026-11-25", "fixed", "Seoul Museum of Art|ソウル市立美術館|首爾市立美術館|Bảo tàng Mỹ thuật Seoul"),
    "mmca": ("https://www.mmca.go.kr/visitingInfo/seoulInfo.do", "2026-11-25", "fixed", "MMCA Seoul|国立現代美術館ソウル館|國立現代美術館首爾館|MMCA Seoul"),
    "sci": ("https://science.seoul.go.kr/main", "2026-11-25", "fixed", "Seoul Science Center|ソウル市立科学館|首爾市立科學館|Trung tâm Khoa học Seoul"),
    "jail": ("https://mediahub.seoul.go.kr/archives/2013973", "2025-04", "fixed", "Seoul City news|ソウル市のお知らせ|首爾市公告|Tin của thành phố Seoul"),
    "post1": ("https://www.law.go.kr/LSW/flDownload.do?flSeq=166636521", "2026-07-01", "fixed", "Domestic postage notice|国内郵便料金の告示|國內郵資公告|Thông báo cước bưu chính trong nước"),
    "post2": ("https://www.law.go.kr/LSW/flDownload.do?flSeq=166636743", "2026-07-01", "fixed", "International postage notice|国際郵便料金の告示|國際郵資公告|Thông báo cước bưu chính quốc tế"),
    "wage": ("https://www.minimumwage.go.kr/minWage/policy/decisionMain.do", "2026-11-25", "fixed", "Minimum Wage Commission|最低賃金委員会|最低工資委員會|Ủy ban Lương tối thiểu"),
    "keta": ("https://www.k-eta.go.kr/portal/guide/viewetaapplication.do?locale=EN", "2026-11-25", "fixed", "K-ETA official site|K-ETA公式サイト|K-ETA 官方網站|Trang K-ETA chính thức"),
    "tax": ("https://english.visitseoul.net/taxrefund", "2026-11-25", "fixed", "Visit Seoul, tax refund|Visit Seoul 免税案内|Visit Seoul 退稅說明|Visit Seoul, hoàn thuế"),
}

# Colours used by the drawings
R, O, Y, G, B, N, P, W, K = "#e5483f", "#f08a2c", "#ffcb3d", "#4aa564", "#3f78d8", "#8a5a34", "#8d5fc0", "#fff6e0", "#3a3f4a"

ITEMS = {}


def I(iid, art, col, price, src, ko, name, unit="", tip=""):
    assert iid not in ITEMS and all(x in SRC for x in src.split()), iid  # two pages: the rule first, the number last
    ITEMS[iid] = {"art": art, "c": col, "p": price, "s": src, "ko": ko, "n": name.split("|"), "u": unit.split("|"), "tip": tip.split("|") if tip else None}
    assert len(ITEMS[iid]["n"]) == 4 and len(ITEMS[iid]["u"]) == 4 and (not tip or len(ITEMS[iid]["tip"]) == 4), iid


CARD = "Adult, by card|大人、交通カード|成人，刷卡|Người lớn, trả bằng thẻ"
SHOP = "Shop price, Seoul average|店頭価格、ソウル平均|店家售價，首爾平均|Giá cửa hàng, trung bình Seoul"
DISH = "One serving at a restaurant, Seoul average|食堂で1人前、ソウル平均|餐廳一人份，首爾平均|Một suất ở quán, trung bình Seoul"
ADULT = "Adult ticket|大人の入場料|成人門票|Vé người lớn"

# 1. Getting around
I("sub", "subway", B, 1550, "pub", "지하철", "Subway ride|地下鉄 1回|搭一次地鐵|Một lượt tàu điện ngầm", "Adult, by card, first 10 km|大人、交通カード、10kmまで|成人刷卡，10 公里內|Người lớn, trả bằng thẻ, 10 km đầu")
I("subc", "subway", G, 1650, "pub", "지하철 1회권", "Subway single ticket|地下鉄の1回券|地鐵單程票|Vé tàu điện ngầm một lượt", "Adult, paid in cash, first 10 km, deposit not counted|大人、現金、10kmまで、保証金を除く|成人，付現金，10 公里內，不含押金|Người lớn, trả tiền mặt, 10 km đầu, chưa tính tiền cọc")
I("subkid", "kid", Y, 0, "fare", "지하철 6세 미만", "Subway, child under 6|地下鉄、6歳未満の子ども|地鐵，未滿 6 歲兒童|Tàu điện ngầm, trẻ dưới 6 tuổi", "Riding with an adult|大人と一緒に乗る|與大人同行|Đi cùng người lớn", "Up to three children ride free with one adult.|大人1人につき3人まで無料。|每位大人最多可帶三位免費。|Một người lớn được đưa tối đa ba trẻ đi miễn phí.")
I("bus", "bus", B, 1500, "busf", "시내버스", "City bus|市内バス|市內公車|Xe buýt thành phố", "Blue or green bus, adult, by card|青か緑のバス、大人、交通カード|藍色或綠色公車，成人刷卡|Xe xanh dương hoặc xanh lá, người lớn, trả bằng thẻ")
I("early", "bus", Y, 1200, "busf", "조조할인", "City bus before 6:30 am|朝6時半前の市内バス|早上 6:30 前的市內公車|Xe buýt trước 6:30 sáng", "Adult, by card, first ride of the day|大人、交通カード、その日最初の乗車|成人刷卡，當天第一次搭乘|Người lớn, trả bằng thẻ, lượt đầu trong ngày", "The first ride before 6:30 am is 20% off.|朝6時半前の最初の乗車は20%引き。|早上 6:30 前的第一次搭乘打八折。|Lượt đầu trước 6:30 sáng được giảm 20%.")
I("night", "bus", K, 2500, "busf", "심야버스", "Night bus (N)|深夜バス（N）|深夜公車（N）|Xe buýt đêm (N)", CARD)
I("red", "bus", R, 3000, "busf", "광역버스", "Red express bus|赤い広域バス|紅色廣域公車|Xe buýt nhanh màu đỏ", "Seoul and nearby cities, adult, by card|ソウルと近くの都市、大人、交通カード|首爾與鄰近城市，成人刷卡|Seoul và thành phố lân cận, người lớn, trả bằng thẻ")
I("village", "bus", G, 1200, "busf", "마을버스", "Village bus|マウルバス|社區小公車|Xe buýt khu phố", "Small bus inside one neighbourhood, adult, by card|町内を回る小さなバス、大人、交通カード|在社區裡行駛的小公車，成人刷卡|Xe nhỏ chạy trong khu phố, người lớn, trả bằng thẻ")
I("teen", "bus", P, 900, "busf", "시내버스 청소년", "City bus, youth fare|市内バス、青少年料金|市內公車，青少年票|Xe buýt, giá thanh thiếu niên", "By a card registered as youth|青少年として登録したカード|登錄為青少年的交通卡|Thẻ đã đăng ký là thanh thiếu niên")
I("kidbus", "kid", O, 550, "busf", "시내버스 어린이", "City bus, child fare|市内バス、子ども料金|市內公車，兒童票|Xe buýt, giá trẻ em", "By a card registered as child|子どもとして登録したカード|登錄為兒童的交通卡|Thẻ đã đăng ký là trẻ em")
I("xfer", "subway", P, 1550, "fare pub", "환승", "Subway, then a bus within 30 minutes|地下鉄から30分以内にバスへ|地鐵下車後 30 分鐘內轉公車|Đi tàu điện rồi lên xe buýt trong 30 phút", "Both rides together, 10 km in all, adult, by card|2回の合計、あわせて10kmまで、大人、交通カード|兩段合計，共 10 公里內，成人刷卡|Cả hai lượt, tổng 10 km, người lớn, trả bằng thẻ", "Tap out and you pay only the higher base fare, once.|降車時もタッチすれば、高いほうの基本運賃1回分だけ。|下車也刷卡的話，只付一次較高的基本車資。|Nếu quẹt thẻ khi xuống, bạn chỉ trả một lần mức giá cơ bản cao hơn.")
I("taxi", "taxi", O, 4800, "taxi", "택시 기본요금", "Taxi, starting fare|タクシーの初乗り|計程車起步價|Taxi, giá mở cửa", "Regular taxi by day, first 1.6 km|一般タクシー、昼、1.6kmまで|一般計程車，白天，1.6 公里內|Taxi thường, ban ngày, 1,6 km đầu")
I("taxin", "taxi", P, 6700, "taxi", "심야 택시", "Taxi at midnight, starting fare|深夜0時のタクシーの初乗り|半夜 12 點的計程車起步價|Taxi lúc nửa đêm, giá mở cửa", "Regular taxi, 11 pm to 2 am, first 1.6 km|一般タクシー、23時〜2時、1.6kmまで|一般計程車，23 點至 2 點，1.6 公里內|Taxi thường, 23 giờ đến 2 giờ, 1,6 km đầu", "From 11 pm to 2 am the night rate is 40% more.|23時〜2時は深夜割増40%。|23 點至 2 點加收 40% 夜間費用。|Từ 23 giờ đến 2 giờ, giá đêm cao hơn 40%.")
I("taxi3", "taxi", B, 5800, "taxi", "심야 택시", "Taxi at 3 am, starting fare|午前3時のタクシーの初乗り|凌晨 3 點的計程車起步價|Taxi lúc 3 giờ sáng, giá mở cửa", "Regular taxi, 10 to 11 pm and 2 to 4 am, first 1.6 km|一般タクシー、22〜23時と2〜4時、1.6kmまで|一般計程車，22 至 23 點與 2 至 4 點，1.6 公里內|Taxi thường, 22–23 giờ và 2–4 giờ, 1,6 km đầu", "After 2 am the night extra drops from 40% to 20%.|2時を過ぎると割増は40%から20%に下がります。|凌晨 2 點後，夜間加成從 40% 降為 20%。|Sau 2 giờ sáng, phụ phí đêm giảm từ 40% xuống 20%.")
I("taxid", "taxi", K, 7000, "taxi", "모범택시", "Deluxe taxi, starting fare|模範タクシーの初乗り|模範計程車起步價|Taxi cao cấp (mobeom), giá mở cửa", "By day, first 3 km|昼、3kmまで|白天，3 公里內|Ban ngày, 3 km đầu")
I("taxim", "taxi", Y, 100, "taxi", "거리요금", "131 more metres in a taxi|タクシーであと131メートル|計程車再多坐 131 公尺|Thêm 131 m trên taxi", "Regular taxi by day, after the first 1.6 km|一般タクシー、昼、1.6kmを過ぎてから|一般計程車，白天，1.6 公里之後|Taxi thường, ban ngày, sau 1,6 km đầu")
I("apj", "taxi", G, 85000, "taxi", "인천공항 → 종로", "Incheon Airport to Jongno by international taxi|仁川空港から鍾路へ、インターナショナルタクシー|仁川機場到鍾路，國際計程車|Sân bay Incheon đến Jongno, taxi quốc tế", "Fixed fare, regular car, tolls included|定額、一般車、通行料込み|固定車資，一般車，含過路費|Giá cố định, xe thường, gồm phí cầu đường")
I("apg", "taxi", R, 90000, "taxi", "인천공항 → 강남", "Incheon Airport to Gangnam by international taxi|仁川空港から江南へ、インターナショナルタクシー|仁川機場到江南，國際計程車|Sân bay Incheon đến Gangnam, taxi quốc tế", "Fixed fare, regular car, tolls included|定額、一般車、通行料込み|固定車資，一般車，含過路費|Giá cố định, xe thường, gồm phí cầu đường")
I("aph", "taxi", P, 75000, "taxi", "인천공항 → 마포(홍대)", "Incheon Airport to Hongdae by international taxi|仁川空港から弘大へ、インターナショナルタクシー|仁川機場到弘大，國際計程車|Sân bay Incheon đến Hongdae, taxi quốc tế", "Fixed fare to Mapo district, regular car, tolls included|麻浦区まで定額、一般車、通行料込み|到麻浦區固定車資，一般車，含過路費|Giá cố định đến quận Mapo, xe thường, gồm phí cầu đường")
I("ch3", "taxi", Y, 70000, "taxi", "택시 3시간 대절", "International taxi for 3 hours|インターナショナルタクシー3時間貸切|國際計程車包車 3 小時|Thuê taxi quốc tế 3 giờ", "Regular car, tolls not included|一般車、通行料別|一般車，不含過路費|Xe thường, chưa gồm phí cầu đường")
I("ch8", "taxi", G, 160000, "taxi", "택시 8시간 대절", "International taxi for 8 hours|インターナショナルタクシー8時間貸切|國際計程車包車 8 小時|Thuê taxi quốc tế 8 giờ", "Regular car, tolls not included|一般車、通行料別|一般車，不含過路費|Xe thường, chưa gồm phí cầu đường")
I("bike1", "bike", G, 1000, "bike", "따릉이 1시간권", "City bike, 1 hour|市の自転車 1時間|公共自行車 1 小時|Xe đạp công cộng 1 giờ", "Ttareungi day pass, each ride up to 1 hour|タルンイ1日券、1回1時間まで|叮鈴鈴一日券，每次 1 小時內|Vé ngày Ttareungi, mỗi lượt tối đa 1 giờ")
I("bike3", "bike", O, 3000, "bike", "따릉이 3시간권", "City bike, 3 hours|市の自転車 3時間|公共自行車 3 小時|Xe đạp công cộng 3 giờ", "Ttareungi day pass, each ride up to 3 hours|タルンイ1日券、1回3時間まで|叮鈴鈴一日券，每次 3 小時內|Vé ngày Ttareungi, mỗi lượt tối đa 3 giờ")
I("bikey", "bike", R, 30000, "bike", "따릉이 365일권", "City bike, a whole year|市の自転車 1年分|公共自行車一整年|Xe đạp công cộng cả năm", "Ttareungi 365-day pass for members, rides up to 1 hour|会員の365日券、1回1時間まで|會員 365 日券，每次 1 小時內|Vé 365 ngày cho hội viên, mỗi lượt tối đa 1 giờ", "That is ₩82 a day.|1日あたり82ウォンです。|等於一天 82 韓元。|Tức là 82 won một ngày.")
I("bikeo", "bike", Y, 200, "bike", "따릉이 초과요금", "City bike, 5 minutes late|市の自転車、5分の超過|公共自行車超時 5 分鐘|Xe đạp công cộng, trả trễ 5 phút", "Every 5 minutes over the ride time|時間を過ぎたら5分ごと|每超過 5 分鐘|Cứ mỗi 5 phút quá giờ")
I("hbus", "boat", B, 3000, "boat", "한강버스", "Hangang Bus|漢江バス|漢江巴士|Hangang Bus", "Ferry on the river, adult, one ride|川を走る船、大人1回|行駛河上的渡輪，成人單程|Tàu chạy trên sông Hàn, người lớn, một lượt")
I("hbusk", "boat", Y, 1100, "boat", "한강버스 어린이", "Hangang Bus, child|漢江バス、子ども|漢江巴士，兒童|Hangang Bus, trẻ em", "Ferry on the river, age 6 to 12, one ride|川を走る船、6〜12歳、1回|行駛河上的渡輪，6 至 12 歲，單程|Tàu chạy trên sông Hàn, 6–12 tuổi, một lượt")
I("toll", "tunnel", O, 2000, "toll", "남산터널 혼잡통행료", "Namsan Tunnel toll|南山トンネルの通行料|南山隧道通行費|Phí hầm Namsan", "Car with one or two people, weekday daytime, into the centre|1〜2人乗りの車、平日の昼、都心方向|一至兩人乘坐的車，平日白天，往市中心|Xe chở một hoặc hai người, ban ngày ngày thường, vào trung tâm", "With three people in the car it is free.|3人以上で乗れば無料です。|車上有三人以上就免費。|Xe chở từ ba người trở lên thì miễn phí.")

# 2. On the table: dishes and famous Korean ingredients
I("bib", "bowl", K, 12077, "eat", "비빔밥", "Bibimbap|ビビンバ|韓式拌飯|Cơm trộn bibimbap", DISH)
I("naeng", "noodle", B, 12692, "eat", "냉면", "Naengmyeon, cold noodles|冷麺|冷麵|Mì lạnh naengmyeon", DISH)
I("kimst", "pot", R, 8846, "eat", "김치찌개백반", "Kimchi stew with rice|キムチチゲ定食|泡菜鍋定食|Canh kim chi kèm cơm", DISH)
I("pork", "grill", O, 21406, "eat", "삼겹살", "Grilled pork belly, 200 g|サムギョプサル 200g|烤五花肉 200 公克|Ba chỉ nướng 200 g", "At a restaurant, Seoul average|食堂で、ソウル平均|餐廳價，首爾平均|Ở quán, trung bình Seoul")
I("jaja", "noodle", K, 7808, "eat", "자장면", "Jajangmyeon, black bean noodles|ジャージャー麺|炸醬麵|Mì tương đen jajangmyeon", DISH)
I("samg", "pot", Y, 18192, "eat", "삼계탕", "Samgyetang, ginseng chicken soup|参鶏湯|人蔘雞湯|Gà hầm sâm samgyetang", DISH)
I("kalg", "noodle", G, 10038, "eat", "칼국수", "Kalguksu, knife-cut noodles|カルグクス|韓式刀切麵|Mì cắt tay kalguksu", DISH)
I("gimb", "roll", G, 3923, "eat", "김밥", "Gimbap, one roll|キンパ 1本|紫菜包飯一條|Gimbap một cuộn", "At a restaurant, Seoul average|食堂で、ソウル平均|餐廳價，首爾平均|Ở quán, trung bình Seoul")
I("gim", "sheet", K, 1342, "k600", "마른김", "Dried laver, 10 sheets|干し海苔 10枚|乾海苔 10 張|Rong biển lá khô, 10 lá", SHOP)
I("tgim", "sheet", G, 2090, "k600", "구운김", "Toasted laver, 10 sheets|焼き海苔 10枚|烤海苔 10 張|Rong biển lá nướng, 10 lá", SHOP)
I("straw", "berry", R, 14750, "k200", "딸기", "Strawberries, 500 g|いちご 500g|草莓 500 公克|Dâu tây 500 g", SHOP)
I("chip", "sack", R, 32233, "k200", "고춧가루", "Korean chili powder, 1 kg|韓国産の唐辛子粉 1kg|韓國產辣椒粉 1 公斤|Ớt bột Hàn Quốc 1 kg", SHOP)
I("abal", "shell", P, 11285, "k600", "전복", "Abalone, five|アワビ 5個|鮑魚 5 顆|Bào ngư, 5 con", SHOP)
I("cabn", "leaf", G, 2269, "k200", "배추", "One napa cabbage|白菜 1株|大白菜一顆|Một cây cải thảo", SHOP)
I("shine", "grape", G, 10037, "k400", "샤인머스켓", "Shine Muscat grapes, 2 kg|シャインマスカット 2kg|麝香葡萄 2 公斤|Nho Shine Muscat 2 kg", SHOP)
I("sesa", "sack", Y, 17825, "k300", "국산 참깨", "Korean sesame seeds, 500 g|韓国産のごま 500g|韓國產芝麻 500 公克|Mè Hàn Quốc 500 g", SHOP, "Imported sesame sells for about a quarter of that (₩4,610).|輸入ごまは約4分の1（₩4,610）。|進口芝麻約為四分之一（₩4,610）。|Mè nhập khẩu chỉ khoảng một phần tư (₩4.610).")
I("oyst", "shell", K, 21558, "k600", "굴", "Oysters, 1 kg|カキ 1kg|牡蠣 1 公斤|Hàu 1 kg", SHOP)
I("pear", "fruit", Y, 28083, "k400", "배", "Ten Korean pears|韓国の梨 10個|韓國梨 10 顆|10 quả lê Hàn Quốc", SHOP)
I("peri", "leaf", G, 1489, "k200", "깻잎", "Perilla leaves, 50 g|エゴマの葉 50g|芝麻葉 50 公克|Lá kkaennip (tía tô Hàn) 50 g", SHOP)
I("saeu", "jar", O, 17375, "k600", "새우젓", "Salted shrimp, 1 kg|アミの塩辛 1kg|醃蝦醬 1 公斤|Mắm tép saeujeot 1 kg", SHOP)
I("tang", "citrus", O, 3532, "k400", "감귤", "Ten tangerines|みかん 10個|橘子 10 顆|10 quả quýt", SHOP)
I("dsq", "squid", O, 72183, "k600", "마른오징어", "Dried squid, ten|するめ 10枚|魷魚乾 10 隻|Mực khô, 10 con", SHOP)
I("rad", "root", W, 1900, "k200", "무", "One Korean radish|大根 1本|白蘿蔔一條|Một củ cải Hàn Quốc", SHOP)
I("pers", "fruit", O, 6463, "k400", "단감", "Five sweet persimmons|甘柿 5個|甜柿 5 顆|5 quả hồng giòn", SHOP)
I("garl", "bulb", W, 10364, "k200", "깐마늘", "Peeled garlic, 1 kg|むきにんにく 1kg|去皮大蒜 1 公斤|Tỏi bóc vỏ 1 kg", SHOP)
I("miy", "sheet", G, 2924, "k600", "마른미역", "Dried seaweed for soup, 100 g|乾燥わかめ 100g|乾海帶芽 100 公克|Rong biển khô nấu canh 100 g", SHOP)
I("cheo", "chili", G, 1229, "k200", "청양고추", "Cheongyang chilies, 100 g|青陽唐辛子 100g|青陽辣椒 100 公克|Ớt Cheongyang 100 g", SHOP)
I("dchi", "chili", R, 18075, "k200", "건고추", "Dried red chilies, 600 g|干し唐辛子 600g|乾辣椒 600 公克|Ớt đỏ khô 600 g", SHOP)

# 3. Out and about: tickets, services, everyday life
I("gyeong", "palace", G, 3000, "royal", "경복궁", "Gyeongbokgung Palace|景福宮|景福宮|Cung Gyeongbokgung", ADULT)
I("changd", "palace", B, 3000, "royal", "창덕궁", "Changdeokgung Palace|昌徳宮|昌德宮|Cung Changdeokgung", ADULT)
I("secret", "tree", G, 5000, "royal", "창덕궁 후원", "Secret Garden at Changdeokgung|昌徳宮の後苑（秘苑）|昌德宮後苑（秘苑）|Vườn Bí mật ở cung Changdeokgung", "On top of the palace ticket, adult|宮殿の入場料とは別、大人|宮殿門票之外另付，成人|Ngoài vé vào cung, người lớn")
I("changg", "palace", O, 1000, "royal", "창경궁", "Changgyeonggung Palace|昌慶宮|昌慶宮|Cung Changgyeonggung", ADULT)
I("deok", "palace", P, 1000, "royal", "덕수궁", "Deoksugung Palace|徳寿宮|德壽宮|Cung Deoksugung", ADULT)
I("jong", "palace", K, 1000, "royal", "종묘", "Jongmyo Shrine|宗廟|宗廟|Miếu Jongmyo", ADULT)
I("tomb", "mound", G, 1000, "royal", "선정릉", "Seonjeongneung royal tombs|宣靖陵|宣靖陵|Lăng Seonjeongneung", ADULT)
I("combo", "palace", R, 6000, "royal", "궁궐 통합관람권", "Four palaces and Jongmyo, one ticket|四つの宮殿と宗廟の共通券|四大宮與宗廟通票|Vé chung bốn cung và Jongmyo", "Good for 6 months, Secret Garden not included|6か月有効、後苑は別|6 個月內有效，不含後苑|Dùng trong 6 tháng, không gồm Vườn Bí mật", "Buying the five one by one costs ₩9,000.|5か所を別々に買うと9,000ウォン。|五處分開買要 9,000 韓元。|Mua lẻ năm nơi hết 9.000 won.")
I("hanbok", "hanbok", P, 0, "royal", "한복 입고 경복궁", "Gyeongbokgung in a hanbok|韓服を着て景福宮へ|穿韓服進景福宮|Mặc hanbok vào cung Gyeongbokgung", ADULT, "The palace rules let anyone wearing a hanbok in free.|宮殿の規定で、韓服を着た人は無料。|依宮殿規定，穿韓服者免費。|Theo quy định của cung, người mặc hanbok được vào miễn phí.")
I("zoo", "paw", O, 5000, "park", "서울동물원", "Seoul Zoo|ソウル動物園|首爾動物園|Sở thú Seoul", ADULT, "Seoul runs it, but it sits just outside the city, in Gwacheon.|ソウル市の動物園ですが、場所は隣の果川市。|由首爾市營運，但位在隔壁的果川市。|Do Seoul quản lý nhưng nằm ngay ngoài thành phố, ở Gwacheon.")
I("theme", "tree", R, 2000, "park", "서울대공원 테마가든", "Seoul Grand Park Theme Garden|ソウル大公園テーマガーデン|首爾大公園主題花園|Vườn chủ đề Seoul Grand Park", ADULT)
I("dal", "balloon", Y, 25000, "dal", "서울달", "Seoul Dal balloon ride|係留気球「ソウルダル」|Seoul Dal 繫留氣球|Khinh khí cầu Seoul Dal", "Adult, about 15 minutes, Yeouido Park|大人、約15分、汝矣島公園|成人，約 15 分鐘，汝矣島公園|Người lớn, khoảng 15 phút, công viên Yeouido")
I("pool", "pool", B, 5000, "swim", "한강 수영장", "Han River outdoor pool|漢江の屋外プール|漢江露天游泳池|Hồ bơi ngoài trời sông Hàn", "Adult, summer 2026|大人、2026年夏|成人，2026 年夏天|Người lớn, hè 2026")
I("sunbed", "parasol", O, 10000, "swim", "한강 수영장 선베드", "Sunbed at a Han River pool|漢江プールのサンベッド|漢江泳池躺椅|Ghế nằm ở hồ bơi sông Hàn", "Morning, afternoon or night, summer 2026|午前・午後・夜のどれか、2026年夏|上午、下午或晚間一場，2026 年夏天|Một buổi sáng, chiều hoặc tối, hè 2026")
I("play", "pool", G, 3000, "swim", "한강 물놀이장", "Han River water playground|漢江の水遊び場|漢江戲水場|Khu chơi nước sông Hàn", "Adult, summer 2026|大人、2026年夏|成人，2026 年夏天|Người lớn, hè 2026")
I("sema", "frame", Y, 0, "sema", "서울시립미술관", "Seoul Museum of Art|ソウル市立美術館|首爾市立美術館|Bảo tàng Mỹ thuật Seoul", "Seosomun main building, adult|西小門本館、大人|西小門本館，成人|Tòa nhà chính Seosomun, người lớn", "Special exhibitions can cost money.|特別展は有料のことがあります。|特展可能要收費。|Triển lãm đặc biệt có thể mất phí.")
I("mmcan", "frame", K, 0, "mmca", "국립현대미술관 야간", "MMCA Seoul on a Saturday night|国立現代美術館ソウル館、土曜の夜|國立現代美術館首爾館，週六晚上|MMCA Seoul, tối thứ Bảy", "Adult, Wednesday or Saturday, 6 to 9 pm|大人、水曜か土曜の18〜21時|成人，週三或週六 18 至 21 點|Người lớn, thứ Tư hoặc thứ Bảy, 18–21 giờ")
I("mmca", "frame", P, 10000, "mmca", "국립현대미술관 통합권", "MMCA Seoul, combined ticket|国立現代美術館ソウル館の統合券|國立現代美術館首爾館整合票|MMCA Seoul, vé chung", "By day, when three or more special exhibitions are on|昼、企画展が3つ以上のとき|白天，有三個以上特展時|Ban ngày, khi có từ ba triển lãm đặc biệt")
I("sci", "flask", G, 0, "sci", "서울시립과학관", "Seoul Science Center|ソウル市立科学館|首爾市立科學館|Trung tâm Khoa học Seoul", "Exhibitions, adult|展示、大人|展覽，成人|Triển lãm, người lớn", "Some hands-on programmes are paid.|一部の体験は有料。|部分體驗活動要收費。|Một số chương trình trải nghiệm có thu phí.")
I("prison", "gate", R, 3000, "jail", "서대문형무소역사관", "Seodaemun Prison History Hall|西大門刑務所歴史館|西大門刑務所歷史館|Nhà tù lịch sử Seodaemun", ADULT)
I("mcut", "scissors", B, 13462, "svc", "이용(남자 커트)", "Men's haircut|男性のカット|男士剪髮|Cắt tóc nam", "Cut only, Seoul average|カットのみ、ソウル平均|只剪髮，首爾平均|Chỉ cắt, trung bình Seoul")
I("wcut", "scissors", R, 24462, "svc", "미용(여자 커트)", "Women's haircut|女性のカット|女士剪髮|Cắt tóc nữ", "Cut only, Seoul average|カットのみ、ソウル平均|只剪髮，首爾平均|Chỉ cắt, trung bình Seoul")
I("bath", "bath", B, 11000, "svc", "대중목욕탕", "Public bathhouse|銭湯（大衆湯）|大眾澡堂|Nhà tắm công cộng", "Adult, Seoul average|大人、ソウル平均|成人，首爾平均|Người lớn, trung bình Seoul")
I("dry", "jacket", K, 11846, "svc", "양복 세탁", "Dry-cleaning a suit|スーツのクリーニング|乾洗一套西裝|Giặt khô một bộ vest", "Jacket and trousers, pressed, Seoul average|上下、アイロン込み、ソウル平均|上下一套含熨燙，首爾平均|Áo và quần, gồm ủi, trung bình Seoul")
I("inn", "bed", R, 53000, "svc", "여관", "One night at an inn|旅館に1泊|旅館住一晚|Một đêm ở nhà trọ", "Yeogwan room with its own bath, Seoul average|ヨグァン（小さな宿）、風呂付き1室、ソウル平均|韓式小旅館附浴室一間，首爾平均|Phòng yeogwan có phòng tắm riêng, trung bình Seoul")
I("trash", "bag", W, 490, "pub", "종량제봉투", "Official rubbish bag, 20 litres|指定ごみ袋 20リットル|專用垃圾袋 20 公升|Túi rác quy định 20 lít", "Seoul|ソウル|首爾|Seoul", "Seoul homes must use these paid bags for rubbish.|ソウルの家庭ごみは、この有料袋で出します。|首爾家庭垃圾須用這種付費垃圾袋。|Ở Seoul, rác sinh hoạt phải bỏ trong túi trả tiền này.")
I("water", "drop", B, 12680, "pub", "상수도", "Tap water, 20,000 litres|水道水 2万リットル|自來水 2 萬公升|Nước máy, 20.000 lít", "Home rate, Seoul|家庭用、ソウル|家庭用，首爾|Giá hộ gia đình, Seoul")
I("letter", "mail", R, 500, "post1", "국내 편지", "Stamp for a letter inside Korea|韓国内の手紙の切手|韓國國內信件郵票|Tem thư trong nước Hàn Quốc", "Standard letter, up to 25 g|定形、25gまで|標準信件，25 公克內|Thư thường, đến 25 g")
I("postc", "postcard", B, 430, "post2", "국제 우편엽서", "Airmail postcard abroad|海外への航空はがき|寄往國外的航空明信片|Bưu thiếp gửi ra nước ngoài", "Any country, by air|どの国へも、航空便|任何國家，航空|Mọi quốc gia, đường hàng không", "Cheaper than a letter inside Korea (₩500).|韓国内の手紙（₩500）より安い。|比韓國國內信件（₩500）還便宜。|Rẻ hơn cả thư trong nước Hàn Quốc (₩500).")
I("aero", "mail", B, 480, "post2", "항공서간", "Aerogramme|航空書簡|航空郵簡|Thư gấp hàng không", "Fold-up airmail letter, any country|折りたたむ航空便、どの国へも|摺疊式航空信，任何國家|Thư gấp gửi đường hàng không, mọi quốc gia")
I("wage", "clock", Y, 10320, "wage", "2026년 최저임금", "One hour at the 2026 minimum wage|2026年の最低賃金で1時間|以 2026 年最低工資工作一小時|Một giờ theo lương tối thiểu 2026", "All of Korea|韓国全国|全韓國|Toàn Hàn Quốc")
I("wage27", "clock", O, 10700, "wage", "2027년 최저임금", "One hour at the 2027 minimum wage|2027年の最低賃金で1時間|以 2027 年最低工資工作一小時|Một giờ theo lương tối thiểu 2027", "All of Korea, from 1 January 2027|韓国全国、2027年1月1日から|全韓國，2027 年 1 月 1 日起|Toàn Hàn Quốc, từ 1/1/2027")
I("keta", "passport", B, 10000, "keta", "K-ETA", "K-ETA application|K-ETAの申請|K-ETA 申請|Đơn xin K-ETA", "Per person, official site, online fee not counted|1人、公式サイト、決済手数料は別|每人，官方網站，不含線上手續費|Mỗi người, trang chính thức, chưa gồm phí thanh toán")
I("taxfree", "shopbag", G, 15000, "tax", "면세 최소 구매금액", "Smallest tax-free purchase|免税になる最低の買い物|可退稅的最低消費|Mức mua tối thiểu để được hoàn thuế", "One shop, one payment|1店で1回の支払い|同一店家一次付款|Một cửa hàng, một lần trả tiền")

# 4. At the market
I("onio", "bulb", O, 1699, "k200", "양파", "Onions, 1 kg|玉ねぎ 1kg|洋蔥 1 公斤|Hành tây 1 kg", SHOP)
I("wmel", "wmelon", G, 22933, "k200", "수박", "One watermelon|すいか 1個|西瓜一顆|Một quả dưa hấu", SHOP)
I("mack", "fish", B, 4202, "k600", "고등어", "One fresh mackerel, large|生サバ 1匹（大）|新鮮鯖魚一條（大）|Một con cá thu tươi, cỡ lớn", SHOP)
I("rice", "sack", W, 64163, "k100", "쌀 20kg", "Rice, 20 kg|米 20kg|白米 20 公斤|Gạo 20 kg", SHOP)
I("avo", "avocado", G, 2085, "k400", "아보카도", "One avocado|アボカド 1個|酪梨一顆|Một quả bơ", SHOP)
I("lemo", "citrus", Y, 10635, "k400", "레몬", "Ten lemons|レモン 10個|檸檬 10 顆|10 quả chanh vàng", SHOP)
I("gron", "bunch", G, 2456, "k200", "대파", "Green onions, 1 kg|長ねぎ 1kg|大蔥 1 公斤|Hành lá 1 kg", SHOP)
I("cucu", "long", G, 10217, "k200", "오이", "Ten cucumbers|きゅうり 10本|小黃瓜 10 條|10 quả dưa leo", SHOP)
I("pine", "pine", Y, 7437, "k400", "파인애플", "One pineapple|パイナップル 1個|鳳梨一顆|Một quả dứa", SHOP)
I("enok", "mushroom", W, 511, "k300", "팽이버섯", "Enoki mushrooms, 150 g|えのき 150g|金針菇 150 公克|Nấm kim châm 150 g", SHOP)
I("appl", "fruit", R, 15711, "k400", "사과", "Ten Fuji apples|ふじりんご 10個|富士蘋果 10 顆|10 quả táo Fuji", SHOP, "A year ago the same ten cost ₩26,018.|1年前は同じ10個が26,018ウォンでした。|一年前同樣 10 顆是 26,018 韓元。|Một năm trước, 10 quả này giá 26.018 won.")
I("shri", "shrimp", O, 4557, "k600", "흰다리새우", "Ten white-leg shrimp|バナメイエビ 10尾|白蝦 10 隻|10 con tôm thẻ", SHOP)
I("carr", "root", O, 4754, "k200", "당근", "Carrots, 1 kg|にんじん 1kg|紅蘿蔔 1 公斤|Cà rốt 1 kg", SHOP)
I("mang", "fruit", Y, 6313, "k400", "망고", "One mango|マンゴー 1個|芒果一顆|Một quả xoài", SHOP)
I("salt", "sack", W, 10433, "k600", "천일염", "Sea salt, 5 kg|天日塩 5kg|天日鹽 5 公斤|Muối biển 5 kg", SHOP)
I("toma", "fruit", R, 3621, "k200", "토마토", "Tomatoes, 1 kg|トマト 1kg|番茄 1 公斤|Cà chua 1 kg", SHOP, "Half of last year's price (₩7,190).|去年（₩7,190）の半分です。|只有去年（₩7,190）的一半。|Bằng một nửa năm ngoái (₩7.190).")
I("cutl", "fish", W, 12233, "k600", "갈치", "One large cutlassfish|太刀魚 1匹（大）|白帶魚一條（大）|Một con cá hố, cỡ lớn", SHOP)
I("zucc", "long", G, 1394, "k200", "애호박", "One Korean zucchini|韓国かぼちゃ（エホバク）1本|韓國櫛瓜一條|Một quả bí ngòi Hàn Quốc", SHOP)
I("kiwi", "citrus", G, 15160, "k400", "골드키위", "Ten gold kiwis|ゴールドキウイ 10個|黃金奇異果 10 顆|10 quả kiwi vàng", SHOP)
I("redb", "sack", R, 12797, "k100", "붉은 팥", "Korean red beans, 500 g|韓国産の小豆 500g|韓國產紅豆 500 公克|Đậu đỏ Hàn Quốc 500 g", SHOP)
I("swee", "root", P, 4767, "k100", "고구마", "Sweet potatoes, 1 kg|さつまいも 1kg|番薯 1 公斤|Khoai lang 1 kg", SHOP)
I("melo", "melon", G, 11336, "k200", "멜론", "One melon|メロン 1個|哈密瓜一顆|Một quả dưa lưới", SHOP)
I("squi", "squid", P, 5333, "k600", "물오징어", "One large squid, frozen|冷凍イカ 1杯（大）|冷凍魷魚一隻（大）|Một con mực đông lạnh, cỡ lớn", SHOP)
I("papr", "pepper", R, 1219, "k200", "파프리카", "One bell pepper|パプリカ 1個|甜椒一顆|Một quả ớt chuông", SHOP)
I("clam", "shell", W, 10677, "k600", "바지락", "Clams, 1 kg|あさり 1kg|蛤蜊 1 公斤|Nghêu 1 kg", SHOP)
I("broc", "broccoli", G, 2184, "k200", "브로콜리", "One broccoli|ブロッコリー 1個|青花菜一顆|Một cây bông cải xanh", SHOP)
I("blue", "grape", B, 10655, "k400", "냉동 블루베리", "Frozen blueberries, 1 kg|冷凍ブルーベリー 1kg|冷凍藍莓 1 公斤|Việt quất đông lạnh 1 kg", SHOP)
I("ging", "root", Y, 9650, "k200", "생강", "Ginger, 1 kg|しょうが 1kg|生薑 1 公斤|Gừng 1 kg", SHOP)

ORDER = {
    "ride": "taxi bikey night hbus subkid apj bus xfer taxin bike1 red toll taxim early aph village sub bikeo taxid kidbus ch8 subc hbusk taxi3 bike3 apg teen ch3".split(),
    "table": "bib gim straw kimst chip abal naeng cabn shine gimb sesa oyst jaja pear peri pork saeu tang samg dsq rad kalg pers tgim garl miy cheo dchi".split(),
    "out": "gyeong mcut hanbok postc dal bath trash secret wage sema inn zoo letter combo keta dry jong mmca water pool wcut deok mmcan taxfree changd aero prison sunbed sci changg wage27 theme tomb play".split(),
    "market": "onio wmel mack rice avo lemo gron cucu pine enok appl shri carr mang salt toma cutl zucc kiwi redb swee melo squi papr clam broc blue ging".split(),
}

# Round five, the bill: (title en|ja|tw|vi, "2 sub, 2 gyeong, ...")
# The order (with the lap step of 9 in won.py) keeps a price off the bill on a day that already asked it: check_site.py tests a year of days.
SCENES = [
    ("Up in the balloon|気球に乗る日|搭氣球的一天|Ngày đi khinh khí cầu", "2 dal, 2 naeng"),
    ("Kids on the river|子どもと川へ|帶孩子遊河|Đưa trẻ ra sông", "2 hbusk, 2 hbus, 3 gimb"),
    ("Laundry and rubbish day|洗濯とごみの日|洗衣倒垃圾的日子|Ngày giặt đồ và đổ rác", "1 dry, 10 trash"),
    ("A royal walk|王家の散歩道|王室散步|Đi dạo hoàng gia", "1 jong, 1 changg, 2 village, 1 bib"),
    ("First night in Seoul|ソウルの最初の夜|在首爾的第一晚|Đêm đầu tiên ở Seoul", "1 aph, 2 kimst"),
    ("Late dinner, night bus home|遅い夕食と深夜バス|宵夜後搭深夜公車|Ăn tối muộn, về bằng xe buýt đêm", "2 pork, 1 night"),
    ("A day at the zoo|動物園の一日|動物園一日|Một ngày ở sở thú", "2 zoo, 2 sub, 3 gimb"),
    ("An afternoon on the river|川で過ごす午後|河上的午後|Một buổi chiều trên sông", "1 hbus, 1 bike1, 1 gimb"),
    ("Breakfast for the week|1週間の朝ごはん|一週的早餐|Bữa sáng cho cả tuần", "3 gim, 2 mack, 1 garl"),
    ("Hanbok day|韓服の日|韓服日|Ngày mặc hanbok", "2 hanbok, 2 sub, 2 bib"),
    ("Grill night for two|2人で焼肉の夜|兩人烤肉之夜|Tối nướng thịt, hai người", "3 pork, 1 taxin"),
    ("A bag of salad|サラダの材料|沙拉食材|Một túi rau trộn", "1 toma, 2 papr, 2 avo"),
    ("Airport taxi and dinner|空港タクシーと夕食|機場計程車加晚餐|Taxi sân bay và bữa tối", "1 apj, 2 samg"),
    ("Pancake night|チヂミの夜|煎餅之夜|Tối bánh xèo Hàn", "2 zucc, 1 gron, 1 onio, 1 shri"),
    ("Every palace in one day|一日で宮殿めぐり|一天走遍宮殿|Các cung trong một ngày", "1 combo, 2 bus, 1 bib"),
    ("Summer at the pool|プールの夏|泳池的夏天|Mùa hè ở hồ bơi", "2 pool, 1 sunbed, 2 gimb"),
    ("A fresh look|さっぱりする日|煥然一新|Một diện mạo mới", "1 mcut, 1 bath, 1 jaja"),
    ("Making winter kimchi|冬のキムチ作り|做冬天的泡菜|Làm kim chi mùa đông", "10 cabn, 3 rad, 1 chip"),
    ("A rainy day indoors|雨の日は屋内で|下雨天待室內|Ngày mưa ở trong nhà", "2 sema, 2 kalg, 4 sub"),
    ("Noodle lunch for three|3人で麺のランチ|三人吃麵午餐|Bữa trưa mì, ba người", "2 kalg, 1 jaja, 3 bus"),
    ("Inn, taxi and stew|宿とタクシーとチゲ|旅館、計程車和泡菜鍋|Nhà trọ, taxi và canh", "1 inn, 1 taxi, 1 kimst"),
    ("At the fish market|魚市場で|在魚市場|Ở chợ cá", "1 abal, 1 oyst, 1 shri"),
    ("Seoul on a shoestring|節約ソウル|省錢玩首爾|Seoul tiết kiệm", "1 deok, 1 gimb, 1 bike1, 1 sub"),
    ("The Secret Garden for two|2人で秘苑へ|兩人逛秘苑|Vườn Bí mật, hai người", "2 changd, 2 secret, 4 sub"),
    ("A student's day|学生の一日|學生的一天|Một ngày của học sinh", "2 teen, 2 gimb, 1 theme"),
    ("Soup on a cold day|寒い日のスープ|冷天喝湯|Món canh ngày lạnh", "2 samg, 2 sub"),
    ("A fruit platter|フルーツの盛り合わせ|水果拼盤|Một đĩa trái cây", "1 straw, 1 shine, 1 pine"),
    ("Palace morning for two|2人で宮殿の朝|兩人的宮殿早晨|Buổi sáng ở cung, hai người", "2 sub, 2 gyeong, 2 gimb"),
    ("Postcards home|家族へはがき|寄明信片回家|Gửi bưu thiếp về nhà", "5 postc, 1 aero, 1 sub"),
]


def scene(s):
    return [(int(q), i) for q, i in (x.split() for x in s.split(", "))]
