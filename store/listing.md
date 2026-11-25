# Google Play listing kit

Everything to paste into Play Console. Text limits: name 30, short description 80, full description 4,000 characters.
Graphics are in this repo: icon `icon-512.png`, feature graphic `store/feature-graphic.png` (1024x500), phone screenshots `store/screenshots/1-sos.png` to `8-show.png` (8 images, the most Play allows) (1080x1920, a one-line caption above each screen in a phone frame; upload in that order, SOS first). The plain screens in `shots/` are for the web install prompt. Rebuild them with `python tools/make_store_assets.py`.

| Field | Value |
|---|---|
| Package name | `com.easymodekorea.app` (cannot change after the first upload) |
| Category | Travel & Local |
| Price | Free, no ads, no in-app purchases |
| Website | https://easymodekorea.com |
| Privacy policy | https://easymodekorea.com/privacy.html |
| Contact email | edandco.biz@gmail.com (already public on the site) |
| Default language | English (United States); add Korean as a second listing |

## English (default)

**App name** (27): `EasyModeKorea: Korea Travel`

**Short description** (76): `Refused, lost or hungry in Korea? SOS, food card, next steps. Works offline.`

**Full description**

```
Your card is refused. The app wants a Korean phone number. The kitchen can't read your allergy. You can't say where you are. EasyModeKorea gives you the next step in a few taps, even with no signal.

WHEN IT HAPPENS
• SOS: call 119, 112 or the 1330 interpreter line. Tap "Where am I?" and your phone works out the national point number, the location code Korean rescuers use, without data. Say it, show it in Korean, or open your own messages app with the Korean text ready. Nothing is sent unless you press Send.
• My food card: tap what you can't or don't eat, once. Staff read it in big Korean and tap an answer; you read it in your language. It also shows the Korean words to look for on packages.
• Refused? 3 taps: restaurant, taxi, subway and bus, KTX, shop, ATM, app sign-up, online payment. One thing to do now, the Korean to show, and what works with your phone and card, with the date we checked it.
• Your trip days: enter your dates and Home shows only today's steps, from arrival to leaving day in order (tax refund before the bag goes). Add a step to your calendar and it rings even when the app is closed.
• Long-press the app icon for SOS, Refused?, Food card and My trip.

BEFORE YOU FLY
• Korea Ready check: a few taps, no typing, and you get a plan for your own phone, card and trip.
• Short answers first: the verdict, where, cost and time, then numbered steps. Every key fact shows the date it was checked and the source, and each guide lists what changed this year.
• Answers for your phone: say once whether you have a Korean number, and the guides show what works for you.
• Arrival helper: enter your landing time and see when you can submit the e-Arrival Card.
• Holiday alerts for your dates: what Seollal and Chuseok change for a visitor.

WHILE YOU ARE HERE
• Korean cards: show a driver or staff a sentence in big Korean letters. Make your own card for a hotel name. Play a card aloud when your phone has a Korean voice.
• Ask cards: show a question ("Can I pay by card?"), staff tap one of the Korean answers, and you read it in your language.
• Find nearby: one tap opens Naver Map on the right Korean word for a convenience store, restroom, subway station, police box or pharmacy.
• Places to go: save your stay and other places once, show them to a driver full screen, or open them in Naver Map or KakaoMap.
• When something goes wrong: lost phone or passport, missed the last train, card refused, taxi trouble. One screen each, step by step, with call buttons and dated sources.
• A real offline pack: guides, cards, SOS and your trip list open with no signal, and the app tells you when everything is saved.
• Share your stay address and place list with a companion by link or QR code.

TOPICS
Entry rules and arrival forms, airport to the city, subway and bus, transit cards, maps, taxis, KTX trains, mobile data and eSIM, cash and ATMs, restaurant bookings, food delivery, translation, tax-free shopping, luggage storage, power plugs, Busan, Jeju and the DMZ.

FIVE LANGUAGES
English, Japanese, Traditional Chinese, Simplified Chinese and Vietnamese.

PRIVATE BY DESIGN
No account, no ads. Your answers, food card, dates, address and cards stay on your phone. Your location is read only when you tap, worked out on the phone, and never sent to us.

INDEPENDENT
EasyModeKorea is an independent guide, not affiliated with any app, company or government body it writes about. It is not an emergency or medical service: in an emergency call 119 or 112, and ask a doctor or pharmacist about your health. Rules change often, so confirm in the official app or site before you rely on an answer.

Questions or corrections: edandco.biz@gmail.com
```

## Korean (한국어)

**앱 이름** (24): `EasyModeKorea: 한국 여행 도우미`

**간단한 설명** (51): `한국에서 거절당하거나 길을 잃었을 때. 위치번호 SOS, 음식 카드, 다음 행동. 오프라인.`

**자세한 설명**

```
카드가 거절되고, 앱이 한국 전화번호를 요구하고, 주방에서 알레르기를 이해하지 못하고, 내가 어디 있는지 말할 수 없을 때. EasyModeKorea는 신호가 없어도 몇 번 눌러서 다음에 할 일을 알려 줍니다.

그 순간에
• SOS: 119, 112, 1330 통역 전화. "Where am I?"를 누르면 폰이 인터넷 없이 국가지점번호(구조대가 쓰는 위치번호)를 계산합니다. 소리 내어 읽거나, 한국어로 보여 주거나, 내 문자 앱에 한국어 문구를 채워 엽니다. 전송을 누르지 않으면 아무것도 보내지 않습니다.
• 내 음식 카드: 못 먹거나 안 먹는 것을 한 번만 고릅니다. 직원은 큰 한국어로 읽고 답을 누르고, 여행자는 자기 언어로 읽습니다. 포장지에서 찾을 한국어 글자도 보여 줍니다.
• 거절당했을 때 3번 누르기: 식당, 택시, 지하철·버스, KTX, 가게, ATM, 앱 가입, 온라인 결제. 지금 할 일 하나, 보여 줄 한국어, 내 폰과 카드로 되는지와 확인 날짜.
• 여행 날짜별 할 일: 날짜를 넣으면 홈에 오늘 할 일만 나옵니다. 도착 날부터 출국 날 순서(짐 부치기 전에 세금 환급)까지. 달력에 넣으면 앱이 닫혀 있어도 알람이 울립니다.
• 앱 아이콘을 길게 누르면 SOS, Refused?, Food card, My trip이 바로 열립니다.

출발 전
• Korea Ready 점검: 입력 없이 몇 번 탭하면 내 폰·카드·일정에 맞춘 준비 계획이 나옵니다.
• 짧은 답 먼저: 결론, 장소, 비용, 시간, 그다음 번호 순서. 핵심 사실마다 확인한 날짜와 출처, 올해 바뀐 내용이 있습니다.
• 내 폰 기준 답: 한국 번호가 있는지 한 번만 알려 주면 나에게 되는 방법을 보여 줍니다.
• 입국 도우미: 도착 시각을 넣으면 전자도착카드를 언제부터 낼 수 있는지 알려 줍니다.
• 여행 날짜에 맞춘 명절 알림: 설과 추석에 여행자에게 달라지는 점.

여행 중
• 한국어 카드: 기사님이나 직원에게 큰 한국어 글씨로 보여 줍니다. 호텔 이름 카드도 직접 만들 수 있습니다. 폰에 한국어 음성이 있으면 소리 내어 읽습니다.
• 답 고르기 카드: 질문("카드 결제 돼요?")을 보여 주면 직원이 한국어 답을 누르고, 여행자는 자기 언어로 읽습니다.
• 주변 찾기: 편의점, 화장실, 지하철역, 파출소, 약국을 맞는 한국어 검색어로 네이버 지도에서 엽니다.
• 갈 곳 목록: 숙소와 장소를 저장해 두고 기사님에게 보여 주거나 네이버 지도·카카오맵으로 엽니다.
• 문제가 생겼을 때: 휴대폰·여권 분실, 막차 놓침, 카드 거절, 택시 문제. 한 화면에 순서대로, 전화 버튼과 날짜 있는 출처.
• 진짜 오프라인 팩: 가이드, 카드, SOS, 여행 목록이 신호 없이 열리고, 모두 저장됐는지 알려 줍니다.
• 숙소 주소와 갈 곳 목록을 링크나 QR로 일행에게 넘길 수 있습니다.

주제
입국 규정과 도착 서류, 공항에서 시내로, 지하철과 버스, 교통카드, 지도, 택시, KTX, 데이터와 eSIM, 현금과 ATM, 식당 예약, 음식 배달, 번역, 면세 쇼핑, 짐 보관, 전원 플러그, 부산·제주·DMZ.

5개 언어
영어, 일본어, 중국어 번체, 중국어 간체, 베트남어. (앱 화면은 한국어를 지원하지 않습니다.)

개인정보를 모으지 않습니다
가입도 광고도 없습니다. 고른 답, 음식 카드, 날짜, 주소, 카드는 폰 안에만 남습니다. 위치는 누를 때만 읽고, 폰 안에서 계산하며, 우리에게 보내지 않습니다.

독립 운영
EasyModeKorea는 독립적으로 운영하는 안내서이며, 소개하는 앱, 회사, 정부 기관과 제휴 관계가 없습니다. 응급·의료 서비스가 아닙니다. 응급이면 119나 112에 전화하고, 건강 문제는 의사나 약사에게 물어보세요. 규정은 자주 바뀌므로 공식 앱이나 사이트에서 한 번 더 확인하세요.

문의·정정: edandco.biz@gmail.com
```

## App content forms (draft answers)

Check each answer against the form in front of you: Google rewords these forms from time to time.

| Form | Answer |
|---|---|
| App access | All functionality is available without special access (no login). |
| Ads | No, the app does not contain ads. |
| Target audience | 18 and over. The app is not designed for children. |
| News app | No. |
| Government app | No. |
| Financial features | None. |
| Health | "My app doesn't provide any health features" (read the note below first) |

### Health question: why the health card was taken out (read 2026-11-25)

- Google asks for an **organization** account for "Health apps, such as medical apps and human subjects research apps" ([Choose a developer account type](https://support.google.com/googleplay/android-developer/answer/13634885), [Play Console Requirements](https://support.google.com/googleplay/android-developer/answer/10788890)). This developer account is personal.
- Every app must answer the [Health apps declaration](https://support.google.com/googleplay/android-developer/answer/14738291), closed tests included, and the answer must match what the app does.
- So the first version has no card for illnesses, medicines or blood type. What is left: a restaurant card for foods (a translated phrase), emergency phone numbers, the location code and a Korean sentence to show, and the pharmacy phrases that were there before. No diagnosis, no first-aid instructions, no health records, no sensor or health permission.
- Not confirmed: whether a reviewer counts the SOS screen as "Emergency and First Aid" (Google's wording: emergency preparedness, first aid instructions, disaster response information) or the food card as "Nutrition" (apps focused on specific dietary needs). If a review says an organization account is needed, stop and ask; do not change the answer just to pass.
- The long description keeps one plain line: not an emergency or medical service, ask a doctor or pharmacist.

### Data safety

| Question | Answer |
|---|---|
| Does the app collect or share any required user data types? | Yes |
| Is all collected data encrypted in transit? | Yes (HTTPS only) |
| Can users request that data be deleted? | Yes. By email; method described at https://easymodekorea.com/privacy.html |

| Data type | Collected | Shared | Optional? | Purpose | Why |
|---|---|---|---|---|---|
| App activity: App interactions | Yes | No | Required | Analytics | Page views and button taps are counted with GoatCounter (no cookies, no IP addresses stored, no user profile). |
| Location: Approximate location | Yes | No | Required | Analytics | The analytics service keeps the visitor's country, worked out from the IP address. Declared to be safe. It can be switched off in GoatCounter's settings; then answer No. |
| Personal info: Email address | Yes | No | Optional | App functionality | Only if the user types it into the question or feedback form, to get a reply. |
| App activity: Other user-generated content | Yes | No | Optional | App functionality | The text of a question or feedback the user sends. |

Not collected: name, phone number, precise location, health info, contacts, photos, files, payment info, device IDs, messages.

- **Precise location**: read only when the user taps "Where am I?", turned into a code in the page, kept in memory, never stored or sent. Google says data that is processed only on the device need not be declared ([Data safety help](https://support.google.com/googleplay/android-developer/answer/10787469), read 2026-11-25). The app itself asks for no location permission; the browser inside it asks (the build fails if a location permission appears).
- **Food card, trip dates, ticks, stay address, saved guides, Korean cards**: stored on the phone only, so they are not "collected".
- **Text 119 / Text 112**: opens the user's own messages app with the words filled in. The user presses Send, so the app does not send or collect messages.

"Shared" stays No: GoatCounter, Google Forms and the hosts only process data for the site, which Google does not count as sharing.

### Content rating (IARC questionnaire)

- Category: Reference, News, or Educational.
- Violence, sexual content, profanity, drugs, alcohol, tobacco, gambling: No to all.
- Users can communicate with each other or share content publicly: No (questions go to the developer by form, nothing is shown to other users).
- Shares the user's location with other users: No (the SOS screen fills a text to 119 or 112 in the user's own messages app; the user sends it). Digital purchases: No.
- Expected result: Everyone / PEGI 3 / 전체이용가.

## Notes for later

- The home-screen name is `EasyMode` (the short name in the web manifest). To change it, edit `launcherName` in `android/twa-manifest.json` and `short_name` in `src/app_shell.py`.
- Screenshots show the English app in the light theme. Japanese or Chinese sets can be added to those listings later.
