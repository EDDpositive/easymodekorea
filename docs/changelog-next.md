# 다음 변경 요약 (2026-11-19, 운영자가 할 일)

머지·배포·게시는 전부 운영자가 직접 합니다. 아래 PR은 열려만 있고 자동 머지는 꺼져 있습니다.

## PR 두 개

1. **새 가이드 2개** — https://github.com/EDDpositive/easymodekorea/pull/2
   - `k-eta-entry-requirements`: 2026년 K-ETA 면제와 전자도착카드(e-Arrival Card)
   - `atm-foreign-card-cash`: 외국 카드로 현금 인출 (Global ATM, 수수료, 현지통화 결제 주의)
   - 5개 언어(영어·일본어·번체·간체·베트남어), 제목·메타 설명·내부 링크·사이트맵·llms.txt·오프라인 캐시(sw.js) 반영. 빌드 확인 완료(81페이지).
   - **머지 전 확인**: K-ETA 면제가 2026-12-31까지라는 점, 전자도착카드 규칙을 공식 사이트(k-eta.go.kr)에서 한 번 더 보세요. 2027년 규정은 아직 미발표라 연말에 갱신이 필요합니다.
2. **Claude API 자동화 3종** — 이 PR (`feat/claude-api-automation`)
   - ① `localize-guides.yml` (수동 실행): 가이드를 ja, zh-tw, es, vi, id, th로 번역해 **초안 PR**을 엽니다. 결과는 `i18n-drafts/` JSON이며 빌드는 아직 읽지 않습니다. es·id·th를 실제 페이지로 내보내려면 `build.py`에 언어 추가가 따로 필요합니다(후속 작업).
   - ② `freshness-check.yml` (매주 월요일 + 수동): 각 가이드의 출처 페이지를 가져와 바뀐 사실이 있으면 **이슈**로 알려 줍니다. 가이드는 수정하지 않습니다. 시크릿이 없으면 조용히 건너뜁니다.
   - ④ `localize-promo.yml` (수동 실행): `overnight-promo.md`의 `### 3-x` 초안 블록을 붙여 넣으면 커뮤니티별 번역 초안 파일(Actions 아티팩트, 7일 보관)을 만듭니다. 게시·커밋은 하지 않습니다.
   - 공통: `claude-opus-5-5`, Batch API, 프롬프트 캐싱, 실행당 출력 토큰 상한(상한 초과 시 실행 중단). 키는 `ANTHROPIC_API_KEY` GitHub Secret에서만 읽습니다. 이번 작업에서는 API를 한 번도 호출하지 않았고(`--dry-run`만 확인), 비용은 발생하지 않았습니다.

## 운영자가 할 일

1. GitHub 저장소 → Settings → Secrets and variables → Actions → **New repository secret**: 이름 `ANTHROPIC_API_KEY`, 값은 직접 만든 키. (채팅·파일에는 붙여 넣지 마세요.)
2. ①이 PR을 만들려면 Settings → Actions → General → "Allow GitHub Actions to create and approve pull requests"를 켜세요.
3. PR #2(가이드)와 이 PR의 diff를 읽고 이상 없으면 직접 머지.
4. 머지 후 Actions 탭에서 필요할 때 수동 실행. 처음에는 `tasks`를 1~2개로 좁혀서 비용을 확인해 보세요 (전체 = 84건, 출력 상한 336,000토큰).
5. ② 이슈가 열리면 출처를 직접 확인한 뒤 `src/data.py`를 고치고 `python src/build.py`.

## 참고

- 로컬 점검: `python tools/localize_guides.py --dry-run` (키 불필요, 비용 없음).
- 번역 초안은 기계 번역입니다. 검수 후 사용하세요.

---

## 검색 유입 개선 라운드 (PR #4: https://github.com/EDDpositive/easymodekorea/pull/4)

PR #4는 PR #2(K-ETA·ATM 가이드)를 포함합니다. #4만 머지해도 되고, #2 먼저 머지해도 충돌 없습니다.

1. 구조화 데이터: Article에 이미지·작성자·발행처 로고·발행일 추가.
2. 내부 링크: 모든 가이드 하단에 질문형 앵커 텍스트의 "관련 가이드" 블록 추가.
3. 새 가이드: 전원 플러그·전압 (Type C/F, 220V).
4. 새 가이드: 서울→부산 + K-Tour Pass 시범(2026-10-01 시작, 12/31까지), KR Pass 가치 판단.
5. 새 가이드: DMZ·JSA 투어 예약 (여권 원본 필수 등).
6. 새 가이드: 제주 이동 (국제운전면허, 버스·택시).
7. 새 가이드: 서울 관광객 교통패스 (30일 기후동행카드 종료 후 현황).
8. 제목: 영어 제목을 키워드 우선·짧게(브랜드 제외 62자 이하) 재작성해 검색 결과에서 잘리지 않게 함.
9. 홈페이지: 홈 목록이 JS로 그려져 크롤러가 보기 어려워서, 모든 가이드를 설명과 함께 정적 목록으로 추가.
10. 신뢰 신호: 각 가이드 본문에 "확인일" 표시.

검증: 111페이지 빌드, canonical·hreflang·내부 링크·JSON-LD·사이트맵 검사 문제 0건.

**머지 순서 (트래픽 기준)**: ① PR #4(새 가이드 7개 + 홈 정적 목록 + 제목 개선, 효과가 가장 큼) → ② PR #2는 #4에 포함되므로 별도 불필요 → ③ PR #3(자동화, 시크릿 설정 후).

머지 전 직접 확인: K-Tour Pass 조건, e-Arrival Card, DMZ 규정, 교통패스(가격은 출처마다 달라 싣지 않음). 베트남어 제목은 아직 긴 편이라 후속 개선 여지가 있습니다.
