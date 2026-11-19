# 다음 변경 요약 (2026-11-19, 기웅 님이 할 일)

머지·배포·게시는 전부 기웅 님이 직접 합니다. 아래 PR은 열려만 있고 자동 머지는 꺼져 있습니다.

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

## 기웅 님이 할 일

1. GitHub 저장소 → Settings → Secrets and variables → Actions → **New repository secret**: 이름 `ANTHROPIC_API_KEY`, 값은 직접 만든 키. (채팅·파일에는 붙여 넣지 마세요.)
2. ①이 PR을 만들려면 Settings → Actions → General → "Allow GitHub Actions to create and approve pull requests"를 켜세요.
3. PR #2(가이드)와 이 PR의 diff를 읽고 이상 없으면 직접 머지.
4. 머지 후 Actions 탭에서 필요할 때 수동 실행. 처음에는 `tasks`를 1~2개로 좁혀서 비용을 확인해 보세요 (전체 = 84건, 출력 상한 336,000토큰).
5. ② 이슈가 열리면 출처를 직접 확인한 뒤 `src/data.py`를 고치고 `python src/build.py`.

## 참고

- 로컬 점검: `python tools/localize_guides.py --dry-run` (키 불필요, 비용 없음).
- 번역 초안은 기계 번역입니다. 검수 후 사용하세요.
