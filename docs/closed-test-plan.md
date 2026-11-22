# 비공개 테스트 계획 (테스터 12명, 14일)

구글 규칙: 개인 개발자 계정은 **테스터 12명 이상이 14일 연속 참여**한 비공개 테스트를 마쳐야 정식 출시를 신청할 수 있습니다. ([공식 안내](https://support.google.com/googleplay/android-developer/answer/14151465))

## 일정
| 시점 | 할 일 | 누가 |
|---|---|---|
| 지금 | 테스터 15명 모으기(지메일 주소 받기). 3명은 여유분 | 기웅 님 |
| 업로드한 날 | 비공개 테스트 버전 올리고 테스터 주소 등록, 검토 요청 | 기웅 님 |
| 검토 통과(보통 며칠) | 참여 링크를 테스터에게 보내기 | 기웅 님 |
| 12명이 참여한 날 = 1일 차 | 플레이 콘솔에서 참여 인원 12명 이상인지 확인 | 기웅 님 |
| 1~14일 차 | 주 2회 인원 확인, 받은 의견 기록. 고칠 것은 Claude에게 전달 | 기웅 님 + Claude |
| 15일 차 | 정식 출시 신청서 작성 | 기웅 님 (초안은 아래) |

14일은 **12명이 모두 참여한 날부터** 셉니다. 중간에 누가 빠져 11명이 되면 다시 세므로 여유 인원이 중요합니다.

## 테스터 조건
- 안드로이드 폰과 구글 계정(지메일)이 있는 실제 사람. 가족, 친구, 동료면 충분합니다.
- 돈을 받고 테스터를 대 주는 업체는 쓰지 않습니다. 구글이 참여 품질을 보고 반려할 수 있습니다.
- 설치만 하고 안 여는 것보다, 14일 동안 몇 번 열어 보는 편이 안전합니다.

## 테스터에게 보낼 글 (그대로 복사)

참여 링크는 패키지 이름으로 정해집니다: **https://play.google.com/apps/testing/com.easymodekorea.app**
테스터 목록에 지메일이 들어간 사람만 열 수 있고, 비공개 테스트 검토가 끝난 뒤부터 작동합니다. 플레이 콘솔 > 비공개 테스트 > 테스터 탭의 "웹에서 참여" 링크와 같은지 한 번 확인하세요.

**1단계: 지메일 주소 받기 (지금 보내기)**
```
EasyModeKorea 앱(한국 여행 안내) 테스트 좀 도와줄래? 2주 동안 깔아만 두면 돼.
안드로이드 폰에서 플레이 스토어에 쓰는 지메일 주소 하나만 알려 줘.
```

**2단계: 참여 링크 보내기 (검토 통과 후)**
```
등록했어! 안드로이드 폰에서 아래 링크 열고 "테스터 되기" → 플레이 스토어에서 설치.
https://play.google.com/apps/testing/com.easymodekorea.app
2주 동안 지우지 말고 두세 번만 열어 봐 줘. 이상한 점은 한 줄만 알려 주면 돼. 고마워!
```

**English**
```
Could you help test the EasyModeKorea app? (2 weeks, about 5 minutes)
It is a guide app for visitors to Korea.

1. Open the link below on your Android phone and tap "Become a tester" (use the Gmail account you use for Play Store).
2. Install the app from Play Store.
3. Keep it installed for 2 weeks and open it two or three times.
4. If anything looks wrong or awkward, send me one line.

Link: https://play.google.com/apps/testing/com.easymodekorea.app
I need your Gmail address first, or the link will not open.
```

## 테스터에게 부탁할 확인 5가지
1. 홈 화면 아이콘으로 열리는가
2. 비행기 모드에서 가이드가 열리는가
3. 한국어 카드를 전체 화면으로 띄울 수 있는가
4. 언어를 바꾸면 다음에 그 언어로 열리는가
5. 읽기 어렵거나 틀린 내용이 있는가

의견은 받은 날짜와 함께 한 줄씩 적어 두세요. 15일 차 신청서에 그대로 씁니다.

## 정식 출시 신청서 초안
구글이 묻는 것은 세 묶음입니다. **대괄호는 실제 있었던 일로 채워야 합니다. 지어내면 안 됩니다.** 영어로 적습니다.

**비공개 테스트에 대해**
- 테스터를 어떻게 모았나: `I invited [number] friends, family members and colleagues who use Android phones, by direct message, and added their Google accounts to the tester list.`
- 테스터의 참여: `Testers installed the app from the closed track and used it over [number] days. They opened guides, used the offline mode and the Korean phrase cards, and switched languages.`
- 받은 의견과 수집 방법: `I collected feedback by direct message and through the in-app feedback form. Main points: [의견 1], [의견 2], [의견 3].`

**앱에 대해**
- 대상: `Foreign visitors to South Korea who do not have a Korean phone number.`
- 가치: `Short, dated answers on which Korean apps and services work for visitors, Korean phrase cards to show staff and drivers, emergency numbers, and offline access. Available in five languages. No account, no ads.`
- 첫해 예상 설치 수: 가장 낮은 구간을 고르는 것이 정직합니다.

**출시 준비에 대해**
- 테스트 뒤 바꾼 것: `[고친 내용. 없으면 "No blocking issues were reported; I fixed [작은 수정]".]`
- 준비됐다고 판단한 근거: `All testers could install and open the app, offline mode and language switching worked on their devices, and automated checks (installability, offline, layout on phone width) pass on every change.`
