"""App shell: the parts that make the site behave like an app on a phone.
Bottom tabs, save and share, the install prompt, the offline and update notices, the Korean cards,
My trip, emergency help and privacy pages, the web manifest and the Android link file.

Text is written per language here (zh-cn by hand, not converted, so mainland wording is right).
build.py imports this file; nothing here imports build.py.
"""
import json

PACKAGE_ID = "com.easymodekorea.app"   # Android application id. Cannot change after the first Play upload.
APP_NAME = "EasyModeKorea"
POLICY_DATE = "2026-11-21"             # ISO date the privacy policy text last changed

T = {
    "en": {
        "nav_label": "Main menu", "nav_guides": "Guides", "nav_cards": "Korean cards", "nav_trip": "My trip", "nav_help": "Help",
        "search": "Search guides", "save": "Save", "saved": "Saved", "share": "Share", "link_copied": "Link copied",
        "saved_toast": "Saved to My trip", "unsaved_toast": "Removed from My trip",
        "install": "Install the app. Guides open without data.", "install_btn": "Install", "later": "Not now",
        "ios_hint": "On iPhone: tap the Share button, then Add to Home Screen.",
        "update": "This page has newer info.", "refresh": "Refresh",
        "trip_title": "My trip", "trip_lede": "Your saved guides, your stay's address and your Korean cards. Everything here stays on this phone.",
        "trip_saved_h": "Saved guides", "trip_saved_empty": "Nothing saved yet. Tap Save at the top of any guide.",
        "trip_recent_h": "Recently opened",
        "trip_more_h": "More for your trip", "trip_cards": "Make a Korean card to show", "trip_setup": "Check what works with your phone", "trip_help": "Emergency numbers",
        "trip_app_h": "This app", "trip_offline": "{n} pages are stored on this phone and open without data.", "trip_install": "Install on this phone",
        "trip_clear": "Erase what I saved on this phone", "trip_clear_q": "Erase your saved guides, address, cards and phone setup from this phone?", "trip_cleared": "Erased.",
        "remove": "Remove",
        "cards_title": "Korean cards to show", "cards_seo": "Korean phrases to show staff and drivers in Korea (offline cards)",
        "cards_desc": "Korean phrases and place names in big letters. Show them to a driver or staff, or copy them into Naver Map. Make your own card too. Works offline.",
        "cards_lede": "Show a card full screen to a driver or staff. Make your own for a hotel name or an allergy.",
        "cards_filter": "Filter: taxi, menu, pharmacy",
        "own_h": "Make your own card", "own_ph": "Type or paste Korean text", "own_show": "Show full screen", "own_save": "Save card", "own_list_h": "Your cards", "own_note": "Kept only on this phone.",
        "basics_h": "Everyday and urgent", "open_guide": "Open the guide",
        "help_title": "Emergency help in Korea", "help_seo": "Emergency numbers in Korea for visitors: 112, 119, 1330",
        "help_desc": "Who to call in Korea: 112 police, 119 ambulance and medical advice, 1330 travel helpline. With Korean cards to show someone. Works offline.",
        "help_lede": "Tap a number to call. If you can't explain, show a Korean card.",
        "help_more_h": "More help", "help_offline": "This page opens without data. Calling needs a phone signal.",
        "deep_faq": "Answered in the guides", "deep_cards": "Korean cards",
        "privacy": "Privacy", "privacy_title": "Privacy policy",
        "privacy_desc": "What EasyModeKorea collects (very little), what stays on your phone, and how to reach us. Covers the website and the Android app.",
        "privacy_updated": "Last updated: {date}",
        "privacy_body": [
            ["In short", "EasyModeKorea has no accounts, no ads and no tracking cookies. The Android app shows this website in full screen. It does not ask for access to your location, contacts, camera or files."],
            ["What stays on your phone", "Your phone setup, saved guides, checklist ticks, your stay's address and the Korean cards you make are stored only in the browser or app on your phone. They are never sent to us. Erase them on the My trip page, or by clearing the site's data in your browser."],
            ["Visit counts", "We count page views and button taps with GoatCounter. It sets no cookies and stores no IP addresses. It shows us totals: which pages were opened, the referring site, browser and system type, screen width, language and country. We cannot tell who you are. If you open a link your host made for you, the name of the stay in that link is counted too."],
            ["Questions and feedback", "When you send a question or feedback, your message, the page you sent it from and your email address (only if you enter one) go to a Google Form that we own. We use them to answer you and to fix the guides. Email us to have a message deleted."],
            ["Other companies' servers", "The site is hosted on GitHub Pages and loads its fonts from Google Fonts, so those servers receive your IP address and browser type when a page loads, as any web server does. If you tap Naver Map on a saved address, that address is sent to Naver as a search. Outside links lead to services with their own policies."],
            ["Children", "EasyModeKorea is written for adult travelers and is not directed at children under 13."],
            ["Contact and changes", "Questions or deletion requests: {email}. When this policy changes, the date below changes."],
        ],
    },
    "ja": {
        "nav_label": "メインメニュー", "nav_guides": "ガイド", "nav_cards": "韓国語カード", "nav_trip": "マイページ", "nav_help": "ヘルプ",
        "search": "ガイドを検索", "save": "保存", "saved": "保存済み", "share": "共有", "link_copied": "リンクをコピーしました",
        "saved_toast": "マイページに保存しました", "unsaved_toast": "マイページから削除しました",
        "install": "アプリを追加。通信なしでもガイドが開けます。", "install_btn": "インストール", "later": "今はしない",
        "ios_hint": "iPhoneの場合: 共有ボタンをタップし、「ホーム画面に追加」を選びます。",
        "update": "このページに新しい情報があります。", "refresh": "更新",
        "trip_title": "マイページ", "trip_lede": "保存したガイド、宿の住所、自分の韓国語カード。すべてこのスマホの中だけに保存されます。",
        "trip_saved_h": "保存したガイド", "trip_saved_empty": "まだ保存していません。ガイド上部の「保存」をタップしてください。",
        "trip_recent_h": "最近開いたガイド",
        "trip_more_h": "旅行に役立つもの", "trip_cards": "見せる韓国語カードを作る", "trip_setup": "自分のスマホで使えるものを確認", "trip_help": "緊急連絡先",
        "trip_app_h": "このアプリ", "trip_offline": "{n}ページがこのスマホに保存され、データ通信なしで開けます。", "trip_install": "このスマホにインストール",
        "trip_clear": "このスマホに保存した内容を消去", "trip_clear_q": "保存したガイド、住所、カード、スマホの設定をこのスマホから消去しますか?", "trip_cleared": "消去しました。",
        "remove": "削除",
        "cards_title": "見せる韓国語カード", "cards_seo": "韓国で店員や運転手に見せる韓国語フレーズ(オフライン対応)",
        "cards_desc": "韓国語のフレーズと地名を大きな文字で表示。運転手や店員に見せたり、Naver Mapにコピーしたりできます。自分のカードも作れます。オフライン対応。",
        "cards_lede": "カードを全画面で運転手や店員に見せられます。ホテル名やアレルギーは自分で作れます。",
        "cards_filter": "絞り込み: タクシー、メニュー、薬局",
        "own_h": "自分のカードを作る", "own_ph": "韓国語を入力または貼り付け", "own_show": "全画面で見せる", "own_save": "保存", "own_list_h": "自分のカード", "own_note": "このスマホの中だけに保存されます。",
        "basics_h": "ふだんの場面と緊急時", "open_guide": "ガイドを開く",
        "help_title": "韓国での緊急時ヘルプ", "help_seo": "韓国の緊急連絡先(旅行者向け): 112・119・1330",
        "help_desc": "韓国で困ったときの連絡先: 112(警察)、119(救急・医療相談)、1330(観光案内)。見せて伝える韓国語カードつき。オフライン対応。",
        "help_lede": "番号をタップすると電話できます。説明が難しいときは韓国語カードを見せてください。",
        "help_more_h": "ほかのヘルプ", "help_offline": "このページはデータ通信なしで開けます。電話には電波が必要です。",
        "deep_faq": "ガイド内の回答", "deep_cards": "韓国語カード",
        "privacy": "プライバシー", "privacy_title": "プライバシーポリシー",
        "privacy_desc": "EasyModeKoreaが集める情報(ごくわずか)、スマホの中だけに残る情報、連絡先。ウェブサイトとAndroidアプリの両方が対象です。",
        "privacy_updated": "最終更新: {date}",
        "privacy_body": [
            ["要点", "EasyModeKoreaにはアカウント登録も広告も追跡用Cookieもありません。Androidアプリはこのウェブサイトを全画面で表示するものです。位置情報、連絡先、カメラ、ファイルへのアクセスは求めません。"],
            ["スマホの中だけに残るもの", "スマホの設定、保存したガイド、チェックリストの印、宿の住所、自分で作った韓国語カードは、あなたのスマホのブラウザまたはアプリの中だけに保存されます。私たちに送信されることはありません。マイページで消去するか、ブラウザでこのサイトのデータを削除すれば消えます。"],
            ["アクセス数の集計", "ページの表示回数とボタンのタップ数をGoatCounterで集計しています。Cookieは使わず、IPアドレスも保存しません。私たちに見えるのは合計だけです(開かれたページ、参照元サイト、ブラウザとOSの種類、画面の幅、言語、国)。個人を特定することはできません。宿の方が作ったリンクを開いた場合は、リンクに含まれる宿の名前も集計されます。"],
            ["質問とフィードバック", "質問やフィードバックを送ると、メッセージ、送信したページ、メールアドレス(入力した場合のみ)が、私たちが管理するGoogleフォームに届きます。返信とガイドの修正のためだけに使います。削除を希望する場合はメールでお知らせください。"],
            ["他社のサーバー", "このサイトはGitHub Pagesで公開し、フォントはGoogle Fontsから読み込んでいます。そのため、ページを開くと、どのウェブサーバーでも同じように、IPアドレスとブラウザの種類がこれらのサーバーに伝わります。保存した住所でNaver Mapをタップすると、その住所が検索語としてNaverに送られます。外部リンク先のサービスには、それぞれのポリシーがあります。"],
            ["お子さまについて", "EasyModeKoreaは大人の旅行者向けに書かれており、13歳未満のお子さまを対象としていません。"],
            ["連絡先と変更", "質問や削除の依頼: {email}。このポリシーを変更したときは、下の日付を更新します。"],
        ],
    },
    "zh-tw": {
        "nav_label": "主選單", "nav_guides": "指南", "nav_cards": "韓文卡", "nav_trip": "我的旅程", "nav_help": "求助",
        "search": "搜尋指南", "save": "收藏", "saved": "已收藏", "share": "分享", "link_copied": "已複製連結",
        "saved_toast": "已存到「我的旅程」", "unsaved_toast": "已從「我的旅程」移除",
        "install": "安裝App,沒有網路也能看指南。", "install_btn": "安裝", "later": "先不要",
        "ios_hint": "iPhone:點「分享」按鈕,再選「加入主畫面」。",
        "update": "這一頁有更新的內容。", "refresh": "重新整理",
        "trip_title": "我的旅程", "trip_lede": "你收藏的指南、住宿地址和自己做的韓文卡。全部只存在這支手機裡。",
        "trip_saved_h": "收藏的指南", "trip_saved_empty": "還沒有收藏。在任何指南上方點「收藏」。",
        "trip_recent_h": "最近看過",
        "trip_more_h": "旅途中用得到", "trip_cards": "做一張給人看的韓文卡", "trip_setup": "查查你的手機能用哪些", "trip_help": "緊急電話",
        "trip_app_h": "這個App", "trip_offline": "這支手機已存好{n}個頁面,沒有網路也能開。", "trip_install": "安裝到這支手機",
        "trip_clear": "清除存在這支手機的內容", "trip_clear_q": "要從這支手機清除收藏的指南、地址、卡片和手機設定嗎?", "trip_cleared": "已清除。",
        "remove": "移除",
        "cards_title": "給人看的韓文卡", "cards_seo": "在韓國給店員和司機看的韓文句子(可離線使用)",
        "cards_desc": "用大字顯示韓文句子和地名,可以給司機或店員看,也能複製到Naver Map。還能自己做卡片。離線也能用。",
        "cards_lede": "把卡片全螢幕給司機或店員看。飯店名稱或過敏原可以自己做一張。",
        "cards_filter": "篩選:計程車、菜單、藥局",
        "own_h": "自己做一張卡", "own_ph": "輸入或貼上韓文", "own_show": "全螢幕顯示", "own_save": "存起來", "own_list_h": "你的卡片", "own_note": "只存在這支手機裡。",
        "basics_h": "日常與緊急", "open_guide": "打開指南",
        "help_title": "在韓國緊急求助", "help_seo": "旅客在韓國的緊急電話:112、119、1330",
        "help_desc": "在韓國該打哪支電話:112警察、119救護車與醫療諮詢、1330觀光諮詢熱線。附上可以給人看的韓文卡。離線也能用。",
        "help_lede": "點號碼就能撥打。說不清楚時,給對方看韓文卡。",
        "help_more_h": "更多協助", "help_offline": "這一頁沒有網路也能開。打電話需要手機訊號。",
        "deep_faq": "指南裡的解答", "deep_cards": "韓文卡",
        "privacy": "隱私權", "privacy_title": "隱私權政策",
        "privacy_desc": "EasyModeKorea蒐集哪些資料(非常少)、哪些只留在你的手機裡,以及如何聯絡我們。適用於網站和Android App。",
        "privacy_updated": "最後更新:{date}",
        "privacy_body": [
            ["重點", "EasyModeKorea沒有帳號、沒有廣告,也沒有追蹤用的Cookie。Android App只是把這個網站以全螢幕顯示,不會要求存取你的位置、通訊錄、相機或檔案。"],
            ["只留在你手機裡的內容", "你的手機設定、收藏的指南、清單勾選、住宿地址和自己做的韓文卡,只存在你手機的瀏覽器或App裡,不會傳給我們。你可以在「我的旅程」頁面清除,或在瀏覽器裡清除本站資料。"],
            ["瀏覽次數統計", "我們用GoatCounter統計頁面瀏覽和按鈕點擊次數。它不使用Cookie,也不儲存IP位址。我們看到的只有總數:哪些頁面被打開、來源網站、瀏覽器和系統類型、螢幕寬度、語言和國家。我們無法得知你是誰。如果你打開房東為你製作的連結,連結裡的住宿名稱也會被計入。"],
            ["提問與意見", "你送出問題或意見時,訊息內容、送出時所在的頁面和電子郵件地址(有填才會有)會傳到我們管理的Google表單。我們只用來回覆你和修正指南。想刪除訊息,請寫信給我們。"],
            ["其他公司的伺服器", "本站架設在GitHub Pages,字型從Google Fonts載入,所以頁面載入時,這些伺服器會收到你的IP位址和瀏覽器類型,任何網站伺服器都是如此。如果你在儲存的地址上點Naver Map,該地址會作為搜尋內容傳給Naver。外部連結通往的服務各有自己的政策。"],
            ["兒童", "EasyModeKorea是寫給成年旅客的,並非以13歲以下兒童為對象。"],
            ["聯絡與變更", "提問或要求刪除:{email}。本政策有變更時,會更新下方日期。"],
        ],
    },
    "zh-cn": {
        "nav_label": "主菜单", "nav_guides": "指南", "nav_cards": "韩文卡", "nav_trip": "我的行程", "nav_help": "求助",
        "search": "搜索指南", "save": "收藏", "saved": "已收藏", "share": "分享", "link_copied": "已复制链接",
        "saved_toast": "已存到“我的行程”", "unsaved_toast": "已从“我的行程”移除",
        "install": "安装App,没有网络也能看指南。", "install_btn": "安装", "later": "暂不",
        "ios_hint": "iPhone:点“分享”按钮,再选“添加到主屏幕”。",
        "update": "这一页有更新的内容。", "refresh": "刷新",
        "trip_title": "我的行程", "trip_lede": "你收藏的指南、住宿地址和自己做的韩文卡。全部只存在这部手机里。",
        "trip_saved_h": "收藏的指南", "trip_saved_empty": "还没有收藏。在任何指南上方点“收藏”。",
        "trip_recent_h": "最近看过",
        "trip_more_h": "旅途中用得到", "trip_cards": "做一张给人看的韩文卡", "trip_setup": "查查你的手机能用哪些", "trip_help": "紧急电话",
        "trip_app_h": "这个App", "trip_offline": "这部手机已存好{n}个页面,没有网络也能打开。", "trip_install": "安装到这部手机",
        "trip_clear": "清除存在这部手机的内容", "trip_clear_q": "要从这部手机清除收藏的指南、地址、卡片和手机设置吗?", "trip_cleared": "已清除。",
        "remove": "移除",
        "cards_title": "给人看的韩文卡", "cards_seo": "在韩国给店员和司机看的韩文句子(可离线使用)",
        "cards_desc": "用大字显示韩文句子和地名,可以给司机或店员看,也能复制到Naver Map。还能自己做卡片。离线也能用。",
        "cards_lede": "把卡片全屏给司机或店员看。酒店名称或过敏原可以自己做一张。",
        "cards_filter": "筛选:出租车、菜单、药店",
        "own_h": "自己做一张卡", "own_ph": "输入或粘贴韩文", "own_show": "全屏显示", "own_save": "保存", "own_list_h": "你的卡片", "own_note": "只存在这部手机里。",
        "basics_h": "日常与紧急", "open_guide": "打开指南",
        "help_title": "在韩国紧急求助", "help_seo": "游客在韩国的紧急电话:112、119、1330",
        "help_desc": "在韩国该打哪个电话:112报警、119救护车与医疗咨询、1330旅游咨询热线。附上可以给人看的韩文卡。离线也能用。",
        "help_lede": "点号码就能拨打。说不清楚时,给对方看韩文卡。",
        "help_more_h": "更多帮助", "help_offline": "这一页没有网络也能打开。打电话需要手机信号。",
        "deep_faq": "指南里的解答", "deep_cards": "韩文卡",
        "privacy": "隐私", "privacy_title": "隐私政策",
        "privacy_desc": "EasyModeKorea收集哪些信息(非常少)、哪些只留在你的手机里,以及如何联系我们。适用于网站和Android App。",
        "privacy_updated": "最后更新:{date}",
        "privacy_body": [
            ["要点", "EasyModeKorea没有账号、没有广告,也没有用于追踪的Cookie。Android App只是把这个网站全屏显示,不会要求访问你的位置、通讯录、相机或文件。"],
            ["只留在你手机里的内容", "你的手机设置、收藏的指南、清单勾选、住宿地址和自己做的韩文卡,只存在你手机的浏览器或App里,不会发送给我们。你可以在“我的行程”页面清除,或在浏览器里清除本站数据。"],
            ["访问次数统计", "我们用GoatCounter统计页面浏览和按钮点击次数。它不使用Cookie,也不保存IP地址。我们看到的只有总数:哪些页面被打开、来源网站、浏览器和系统类型、屏幕宽度、语言和国家。我们无法得知你是谁。如果你打开房东为你制作的链接,链接里的住宿名称也会被计入。"],
            ["提问与反馈", "你提交问题或反馈时,留言内容、提交时所在的页面和电子邮件地址(填写了才会有)会发送到我们管理的Google表单。我们只用来回复你和修正指南。想删除留言,请给我们发邮件。"],
            ["其他公司的服务器", "本站托管在GitHub Pages,字体从Google Fonts加载,所以页面加载时,这些服务器会收到你的IP地址和浏览器类型,任何网站服务器都是如此。如果你在保存的地址上点Naver Map,该地址会作为搜索内容发送给Naver。外部链接通往的服务各有自己的政策。"],
            ["儿童", "EasyModeKorea是写给成年游客的,并非面向13岁以下儿童。"],
            ["联系与变更", "提问或要求删除:{email}。本政策有变更时,会更新下方日期。"],
        ],
    },
    "vi": {
        "nav_label": "Menu chính", "nav_guides": "Hướng dẫn", "nav_cards": "Thẻ tiếng Hàn", "nav_trip": "Của tôi", "nav_help": "Trợ giúp",
        "search": "Tìm hướng dẫn", "save": "Lưu", "saved": "Đã lưu", "share": "Chia sẻ", "link_copied": "Đã sao chép liên kết",
        "saved_toast": "Đã lưu vào mục Của tôi", "unsaved_toast": "Đã bỏ khỏi mục Của tôi",
        "install": "Cài ứng dụng. Xem hướng dẫn cả khi không có mạng.", "install_btn": "Cài đặt", "later": "Để sau",
        "ios_hint": "Trên iPhone: chạm nút Chia sẻ, rồi chọn Thêm vào Màn hình chính.",
        "update": "Trang này có thông tin mới hơn.", "refresh": "Tải lại",
        "trip_title": "Chuyến đi của tôi", "trip_lede": "Hướng dẫn đã lưu, địa chỉ chỗ ở và thẻ tiếng Hàn của bạn. Tất cả chỉ nằm trên điện thoại này.",
        "trip_saved_h": "Hướng dẫn đã lưu", "trip_saved_empty": "Chưa lưu gì. Chạm Lưu ở đầu bất kỳ hướng dẫn nào.",
        "trip_recent_h": "Mới mở gần đây",
        "trip_more_h": "Hữu ích cho chuyến đi", "trip_cards": "Tạo thẻ tiếng Hàn để đưa xem", "trip_setup": "Xem điện thoại của bạn dùng được gì", "trip_help": "Số khẩn cấp",
        "trip_app_h": "Ứng dụng này", "trip_offline": "{n} trang đã lưu trên điện thoại này và mở được khi không có mạng.", "trip_install": "Cài vào điện thoại này",
        "trip_clear": "Xóa những gì đã lưu trên điện thoại này", "trip_clear_q": "Xóa hướng dẫn đã lưu, địa chỉ, thẻ và thiết lập điện thoại khỏi máy này?", "trip_cleared": "Đã xóa.",
        "remove": "Bỏ",
        "cards_title": "Thẻ tiếng Hàn để đưa xem", "cards_seo": "Câu tiếng Hàn để đưa nhân viên và tài xế xem ở Hàn Quốc (dùng offline)",
        "cards_desc": "Câu và tên địa điểm tiếng Hàn bằng chữ lớn. Đưa cho tài xế hoặc nhân viên xem, hoặc sao chép vào Naver Map. Bạn cũng có thể tự tạo thẻ. Dùng được khi không có mạng.",
        "cards_lede": "Hiện thẻ toàn màn hình cho tài xế hoặc nhân viên xem. Tự tạo thẻ cho tên khách sạn hoặc dị ứng.",
        "cards_filter": "Lọc: taxi, thực đơn, hiệu thuốc",
        "own_h": "Tự tạo thẻ", "own_ph": "Gõ hoặc dán chữ tiếng Hàn", "own_show": "Hiện toàn màn hình", "own_save": "Lưu thẻ", "own_list_h": "Thẻ của bạn", "own_note": "Chỉ lưu trên điện thoại này.",
        "basics_h": "Hằng ngày và khẩn cấp", "open_guide": "Mở hướng dẫn",
        "help_title": "Trợ giúp khẩn cấp ở Hàn Quốc", "help_seo": "Số khẩn cấp ở Hàn Quốc cho du khách: 112, 119, 1330",
        "help_desc": "Gọi số nào ở Hàn Quốc: 112 cảnh sát, 119 cấp cứu và tư vấn y tế, 1330 đường dây du lịch. Kèm thẻ tiếng Hàn để đưa người khác xem. Dùng được khi không có mạng.",
        "help_lede": "Chạm vào số để gọi. Nếu khó giải thích, hãy đưa thẻ tiếng Hàn.",
        "help_more_h": "Trợ giúp khác", "help_offline": "Trang này mở được khi không có mạng. Gọi điện cần có sóng điện thoại.",
        "deep_faq": "Giải đáp trong hướng dẫn", "deep_cards": "Thẻ tiếng Hàn",
        "privacy": "Quyền riêng tư", "privacy_title": "Chính sách quyền riêng tư",
        "privacy_desc": "EasyModeKorea thu thập gì (rất ít), những gì chỉ nằm trên điện thoại của bạn và cách liên hệ. Áp dụng cho trang web và ứng dụng Android.",
        "privacy_updated": "Cập nhật lần cuối: {date}",
        "privacy_body": [
            ["Tóm tắt", "EasyModeKorea không có tài khoản, không có quảng cáo và không dùng cookie theo dõi. Ứng dụng Android hiển thị trang web này ở chế độ toàn màn hình. Ứng dụng không xin quyền truy cập vị trí, danh bạ, máy ảnh hay tệp của bạn."],
            ["Những gì chỉ nằm trên điện thoại của bạn", "Thiết lập điện thoại, hướng dẫn đã lưu, các mục đã đánh dấu, địa chỉ chỗ ở và thẻ tiếng Hàn bạn tạo chỉ được lưu trong trình duyệt hoặc ứng dụng trên điện thoại của bạn. Chúng không bao giờ được gửi cho chúng tôi. Bạn có thể xóa ở trang Chuyến đi của tôi, hoặc xóa dữ liệu của trang web trong trình duyệt."],
            ["Đếm lượt truy cập", "Chúng tôi đếm lượt xem trang và lượt chạm nút bằng GoatCounter. Dịch vụ này không đặt cookie và không lưu địa chỉ IP. Chúng tôi chỉ thấy tổng số: trang nào được mở, trang giới thiệu, loại trình duyệt và hệ điều hành, chiều rộng màn hình, ngôn ngữ và quốc gia. Chúng tôi không thể biết bạn là ai. Nếu bạn mở liên kết do chủ nhà tạo cho bạn, tên chỗ ở trong liên kết đó cũng được đếm."],
            ["Câu hỏi và góp ý", "Khi bạn gửi câu hỏi hoặc góp ý, nội dung tin nhắn, trang bạn đang xem và địa chỉ email (chỉ khi bạn nhập) được gửi tới một Google Form do chúng tôi quản lý. Chúng tôi chỉ dùng để trả lời bạn và sửa hướng dẫn. Hãy gửi email nếu bạn muốn xóa tin nhắn."],
            ["Máy chủ của công ty khác", "Trang web được đặt trên GitHub Pages và tải phông chữ từ Google Fonts, nên các máy chủ đó nhận địa chỉ IP và loại trình duyệt của bạn khi trang được tải, giống như mọi máy chủ web. Nếu bạn chạm Naver Map trên địa chỉ đã lưu, địa chỉ đó được gửi tới Naver dưới dạng từ khóa tìm kiếm. Các liên kết ngoài dẫn tới dịch vụ có chính sách riêng."],
            ["Trẻ em", "EasyModeKorea được viết cho du khách người lớn và không hướng tới trẻ em dưới 13 tuổi."],
            ["Liên hệ và thay đổi", "Câu hỏi hoặc yêu cầu xóa: {email}. Khi chính sách này thay đổi, ngày bên dưới sẽ được cập nhật."],
        ],
    },
}

# Strings the shared script needs on every page (the rest are only used at build time).
JS_KEYS = ("save", "saved", "share", "link_copied", "saved_toast", "unsaved_toast", "install", "install_btn", "later", "update", "refresh")

SVG = lambda body: f'<svg viewBox="0 0 24 24" aria-hidden="true">{body}</svg>'
IC = {
    "guides": SVG('<path d="M4 11l8-7 8 7v8a1 1 0 0 1-1 1h-4v-6H9v6H5a1 1 0 0 1-1-1z"/>'),
    "cards": SVG('<path d="M4 5h16v11H10l-4.5 4v-4H4z"/><path d="M8 9h8M8 12h5"/>'),
    "trip": SVG('<path d="M7 3h10a1 1 0 0 1 1 1v17l-6-4-6 4V4a1 1 0 0 1 1-1z"/>'),
    "help": SVG('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.6"/><path d="M5.7 5.7l3.7 3.7M14.6 14.6l3.7 3.7M18.3 5.7l-3.7 3.7M9.4 14.6l-3.7 3.7"/>'),
    "search": SVG('<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>'),
    "globe": SVG('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.8 3 2.8 15 0 18M12 3c-2.8 3-2.8 15 0 18"/>'),
    "save": SVG('<path d="M7 3h10a1 1 0 0 1 1 1v17l-6-4-6 4V4a1 1 0 0 1 1-1z"/>'),
    "share": SVG('<path d="M12 15V3M8 7l4-4 4 4"/><path d="M5 12v7a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-7"/>'),
}

TABS = (("guides", "./", "nav_guides"), ("cards", "phrases.html", "nav_cards"), ("trip", "saved.html", "nav_trip"), ("help", "help.html", "nav_help"))


def esc(s):
    import html
    return html.escape(str(s), quote=True)


def tabbar(lang, active):
    """Bottom tabs. Plain links, so they work without script and offline."""
    t = T[lang]
    cur = ' aria-current="page"'
    items = "".join(f'<a href="{href}" class="tab-{key}"{cur if key == active else ""}>{IC[key]}<span>{esc(t[lbl])}</span></a>' for key, href, lbl in TABS)
    return f'<nav class="tabbar" aria-label="{esc(t["nav_label"])}">{items}</nav>'


def page_config(lang, up, ux, guide=None):
    """Inline settings for app.js: language, path to the site root, and the few strings it shows."""
    t = {k: T[lang][k] for k in JS_KEYS}
    t.update({"offline": ux["offline"], "suggest": ux["suggest"], "switch": ux["switch"], "dismiss": ux["dismiss"]})
    cfg = {"lang": lang, "up": up, "t": t}
    if guide: cfg["guide"] = guide
    return json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/")


# Opens the installed app in the language the visitor picked last time. Goes on the English pages the
# app can start from (home and the three shortcuts); the site is served from the domain root.
LAUNCH_JS = ('<script>try{var l=localStorage.getItem("emk-lang");if(l&&/^(ja|zh-tw|zh-cn|vi)$/.test(l)&&!sessionStorage.getItem("emk-go")&&'
             '(matchMedia("(display-mode: standalone)").matches||navigator.standalone)){sessionStorage.setItem("emk-go","1");location.replace("/"+l+location.pathname+location.hash)}}catch(e){}</script>')


APP_JS = r"""/* EasyModeKorea app shell: offline, install, save, share, notices. Shared by every page. */
(function () {
  "use strict";
  var E = window.EMK || { lang: "en", up: "", t: {} }, T = E.t, d = document;
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function list(k) { try { var a = JSON.parse(get(k) || "[]"); return Array.isArray(a) ? a : []; } catch (e) { return []; } }
  function count(path, title) { try { if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({ path: path, title: title, event: true }); } catch (e) {} }
  function mk(tag, cls, text) { var n = d.createElement(tag); if (cls) n.className = cls; if (text) n.textContent = text; return n; }
  var standalone = !!((window.matchMedia && matchMedia("(display-mode: standalone)").matches) || navigator.standalone === true);
  if (standalone) d.documentElement.classList.add("app");
  try { sessionStorage.setItem("emk-go", "1"); } catch (e) {}

  /* One small notice above the tabs. */
  var note = null, noteTimer = 0;
  function toast(text, actText, act, ms) {
    if (!note) { note = mk("div", "toast app-toast"); note.setAttribute("role", "status"); d.body.appendChild(note); }
    note.textContent = text;
    if (actText) { var b = mk("button", "", actText); b.type = "button"; b.addEventListener("click", act); note.appendChild(b); }
    note.hidden = false; clearTimeout(noteTimer);
    if (ms !== 0) noteTimer = setTimeout(function () { note.hidden = true; }, ms || 2600);
  }
  window.emkToast = toast;

  /* Offline notice. */
  function net() { if (!navigator.onLine) toast(T.offline, null, null, 6000); }
  addEventListener("offline", net); net();

  /* Offline copy of the site, and a notice when the page on screen has a newer version. */
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register(E.up + "sw.js?l=" + E.lang).catch(function () {});
    navigator.serviceWorker.addEventListener("message", function (ev) {
      if (ev.data && ev.data.t === "upd" && ev.data.p === location.pathname) toast(T.update, T.refresh, function () { location.reload(); }, 12000);
    });
  }

  /* Install prompt: shown after the visitor has looked around, never inside the installed app. */
  var deferred = null, bar = null;
  function askInstall() { if (!deferred) return; var p = deferred; deferred = null; hideBar(); p.prompt(); count("install", "install"); }
  function hideBar() { if (bar) { bar.remove(); bar = null; } }
  function showBar() {
    if (bar || !deferred || standalone) return;
    if (Date.now() - Number(get("emk-install-no") || 0) < 14 * 864e5) return;
    bar = mk("div", "install-bar"); bar.setAttribute("role", "region"); bar.setAttribute("aria-label", T.install_btn);
    var go = mk("button", "btn", T.install_btn), no = mk("button", "x", "\u2715"); go.type = no.type = "button"; no.setAttribute("aria-label", T.later);
    go.addEventListener("click", askInstall);
    no.addEventListener("click", function () { set("emk-install-no", String(Date.now())); hideBar(); });
    bar.appendChild(mk("span", "", T.install)); bar.appendChild(go); bar.appendChild(no); d.body.appendChild(bar);
  }
  var views = 0; try { views = Number(sessionStorage.getItem("emk-pv") || 0) + 1; sessionStorage.setItem("emk-pv", String(views)); } catch (e) {}
  addEventListener("beforeinstallprompt", function (ev) {
    ev.preventDefault(); deferred = ev;
    d.dispatchEvent(new CustomEvent("emk-installable"));
    if (views >= 2) showBar(); else setTimeout(showBar, 20000);
  });
  addEventListener("appinstalled", function () { deferred = null; hideBar(); count("installed", "installed"); });
  window.emkInstall = { ready: function () { return !!deferred; }, ask: askInstall, standalone: standalone };

  /* Language: remember the choice, close the menu on an outside tap, suggest the reader's language once. */
  var menu = d.querySelector(".lang-menu");
  d.querySelectorAll(".langs a[data-l]").forEach(function (a) { a.addEventListener("click", function () { set("emk-lang", a.getAttribute("data-l")); }); });
  if (menu) d.addEventListener("click", function (ev) { if (menu.open && !menu.contains(ev.target)) menu.open = false; });
  (function () {
    if (d.getElementById("lang-suggest") || get("wik-lang-dismiss") || get("emk-lang")) return;
    var w = (navigator.language || "").toLowerCase();
    var want = w.indexOf("ja") === 0 ? "ja" : /^zh-(tw|hk|mo|hant)/.test(w) ? "zh-tw" : w.indexOf("zh") === 0 ? "zh-cn" : w.indexOf("vi") === 0 ? "vi" : w.indexOf("en") === 0 ? "en" : "";
    if (!want || want === E.lang) return;
    var a = d.querySelector('.langs a[data-l="' + want + '"]'), hero = d.querySelector(".hero"); if (!a || !hero) return;
    var wrap = mk("div", "wrap pre"), b = mk("div", "banner");
    var go = mk("a", "btn alt", T["switch"]); go.href = a.getAttribute("href");
    go.addEventListener("click", function () { set("emk-lang", want); });
    var no = mk("button", "linkbtn", T.dismiss); no.type = "button";
    no.addEventListener("click", function () { set("wik-lang-dismiss", "1"); wrap.remove(); });
    b.appendChild(mk("span", "", T.suggest.replace("{l}", a.textContent))); b.appendChild(go); b.appendChild(no);
    wrap.appendChild(b); hero.insertAdjacentElement("afterend", wrap);
  })();

  /* Save and share on guide pages. Saved guides and recent guides are lists of slugs kept on this phone. */
  var sv = d.getElementById("save-btn"), sh = d.getElementById("share-btn");
  if (E.guide) {
    var rec = list("emk-recent").filter(function (s) { return s !== E.guide; }); rec.unshift(E.guide); set("emk-recent", JSON.stringify(rec.slice(0, 6)));
  }
  if (sv && E.guide) {
    var paint = function () { var on = list("emk-saved").indexOf(E.guide) >= 0; sv.setAttribute("aria-pressed", String(on)); sv.querySelector("span").textContent = on ? T.saved : T.save; return on; };
    sv.addEventListener("click", function () {
      var s = list("emk-saved"), i = s.indexOf(E.guide);
      if (i >= 0) s.splice(i, 1); else { s.unshift(E.guide); count("save/" + E.guide, "save guide"); }
      set("emk-saved", JSON.stringify(s.slice(0, 40))); toast(paint() ? T.saved_toast : T.unsaved_toast);
    });
    paint();
  }
  if (sh) sh.addEventListener("click", function () {
    var c = d.querySelector('link[rel="canonical"]'), url = c ? c.href : location.href, title = d.title;
    if (location.hostname !== "easymodekorea.com") url = location.href.split("#")[0];
    var copied = function () { toast(T.link_copied); };
    if (navigator.share) { navigator.share({ title: title, url: url }).catch(function () {}); }
    else if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(url).then(copied, function () {}); }
    count("share" + location.pathname, "share");
  });
})();
"""


SW_JS = r"""const C='emk-0';const PRE=[];
/* EasyModeKorea offline worker. The line above is rewritten by src/build.py on every build.
   Pages: answer from the copy on the phone at once, fetch a fresh copy in the background, and tell
   the page when the fresh copy differs. Versioned files (?v=) never change, so the copy is final. */
const L=new URL(self.location).searchParams.get('l')||'en',D=L==='en'?'':L+'/',LD=['ja/','zh-tw/','zh-cn/','vi/'];
const ROOT=self.registration.scope;
const own=p=>D?p.startsWith(D):!LD.some(x=>p.startsWith(x));
/* Keep the reader's own language (pages and search index), every language's home page, and shared files. */
const MINE=PRE.filter(p=>p.endsWith('/')||!/\.(html|json)$/.test(p)||own(p));
const isPage=u=>u.pathname.endsWith('/')||u.pathname.endsWith('.html');
const keyOf=u=>isPage(u)?u.origin+u.pathname:u.href;
const clean=r=>r.redirected?new Response(r.body,{status:r.status,statusText:r.statusText,headers:r.headers}):r;
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>Promise.all(MINE.map(p=>{const u=new URL(p,ROOT);
  return fetch(new Request(u.href,{cache:'reload'})).then(r=>r.ok?c.put(keyOf(u),clean(r)):null).catch(()=>null)}))).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
/* Only what the reader sees counts as newer info: a new stylesheet or script name in the head does not. */
const body=t=>t.slice(Math.max(0,t.indexOf('<body')));
const tell=p=>new Promise(r=>setTimeout(r,1500)).then(()=>self.clients.matchAll({type:'window'})).then(cs=>cs.forEach(cl=>{if(new URL(cl.url).pathname===p)cl.postMessage({t:'upd',p})}));
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET')return;
  const u=new URL(r.url);if(u.origin!==location.origin||u.pathname.endsWith('/sw.js'))return;
  const nav=r.mode==='navigate',k=nav?u.origin+u.pathname:u.href;
  e.respondWith((async()=>{
    const c=await caches.open(C),hit=await c.match(k);
    if(hit&&u.search.startsWith('?v='))return hit;
    const old=hit&&nav?hit.clone():null;
    const net=fetch(r).then(async res=>{
      if(res.ok&&res.type==='basic'){const fresh=clean(res.clone());
        if(old){const a=await old.text(),b=await fresh.clone().text();await c.put(k,fresh);if(body(a)!==body(b))await tell(u.pathname)}
        else await c.put(k,fresh)}
      return res});
    if(hit){e.waitUntil(net.catch(()=>{}));return hit}
    try{return clean(await net)}catch(err){
      if(nav){const home=await c.match(new URL(D||'./',ROOT).href)||await c.match(ROOT);if(home)return home}
      throw err}
  })())});
"""


def manifest(desc, shots):
    """Web manifest. Absolute paths, so the same file serves every language folder."""
    m = {
        "id": "/", "name": APP_NAME, "short_name": "EasyMode", "description": desc,
        "lang": "en", "dir": "ltr", "start_url": "/", "scope": "/", "display": "standalone",
        "background_color": "#ffffff", "theme_color": "#2336e8", "categories": ["travel", "navigation"],
        "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
                  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
                  {"src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
        "shortcuts": [
            {"name": T["en"]["help_title"], "short_name": "Help", "url": "/help.html", "icons": [{"src": "/shortcut-help.png", "sizes": "96x96", "type": "image/png"}]},
            {"name": T["en"]["cards_title"], "short_name": "Korean cards", "url": "/phrases.html", "icons": [{"src": "/shortcut-cards.png", "sizes": "96x96", "type": "image/png"}]},
            {"name": T["en"]["trip_title"], "short_name": "My trip", "url": "/saved.html", "icons": [{"src": "/shortcut-trip.png", "sizes": "96x96", "type": "image/png"}]},
        ],
        "screenshots": [{"src": f"/{name}", "sizes": f"{w}x{h}", "type": "image/png", "form_factor": "narrow", "label": label} for name, w, h, label in shots],
    }
    return json.dumps(m, ensure_ascii=False, indent=1) + "\n"


def assetlinks(fingerprints):
    """Digital Asset Links file that lets the Android app open the site without a browser bar.
    Fingerprints are public SHA-256 certificate fingerprints (Play app signing key, upload key)."""
    if not fingerprints: return "[]\n"
    return json.dumps([{"relation": ["delegate_permission/common.handle_all_urls"],
                        "target": {"namespace": "android_app", "package_name": PACKAGE_ID, "sha256_cert_fingerprints": fingerprints}}], indent=1) + "\n"
