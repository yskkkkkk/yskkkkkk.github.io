# yskkkkkk.github.io — 코드 에이전트 작업 지침

## 핵심 원칙

이 파일은 AI 코딩 에이전트가 이 저장소를 작업할 때 반드시 먼저 읽어야 하는 주의사항 모음입니다.

> **블로그 글을 쓰거나 어투를 다듬을 때는 반드시 [`WRITING_STYLE.md`](./WRITING_STYLE.md)를 먼저 읽고 따릅니다.**

---

## 커밋 작성자 설정 (세션 시작 시 필수)

이 저장소는 Claude Code 기본 identity(`Claude <noreply@anthropic.com>`)로 커밋하면
GitHub 컨트리뷰션 그래프에 하나도 집계되지 않습니다. 원격 컨테이너는 세션마다 새로
생성되어 이전 설정이 초기화되므로, **작업을 시작하기 전에 매번 아래를 실행합니다.**

```bash
git config user.name "yskkkkkk"
git config user.email "fb1014@naver.com"
```

(`--global`이 아니라 이 저장소에만 적용되는 local 설정입니다. 전역 설정은 건드리지 않습니다.)

---

## 보류 중인 초안

**새 글 소재를 논의할 때는 아래 목록을 먼저 확인하고, 관련된 항목이 있으면 글쓴이에게 먼저 알립니다.**
발행을 미뤄둔 원재료가 있는데 그걸 모르고 새로 쓰기 시작하면, 살릴 수 있는 소재를 놓치게 됩니다.

| 파일 | 보류 사유 | 살릴 조건 |
|---|---|---|
| `src/content/blog/2026-08-11-내부-용어로-나를-설명하고-있었다.md` | 일화 하나로는 소재가 얇아 한 편을 못 버팀 | **이력서·포트폴리오** 관련 다른 경험이 생기면 그중 한 사례로 묶어서 쓸 것 |

보류 초안은 `draft: true`로 두면 블로그 목록·검색·RSS·`llms.txt`·개별 페이지 생성에서 모두 제외됩니다.
파일 상단 인용 블록에 보류 사유와 향후 방향을 적어두고, 발행할 때 `draft` 줄과 그 블록을 함께 제거합니다.

---

## 중복 렌더링 주의사항

### 홈과 `/series`의 시리즈 UI는 서로 다릅니다

두 페이지가 같은 데이터(`SERIES_META` + 포스트 통계)를 쓰지만 **UI 구현은 완전히 다릅니다.**

| 파일 | UI |
|---|---|
| `src/pages/index.astro` | 컴팩트 시리즈 칩 (`series-chip-item`) — 이름 + 편수만, 최신 3개 |
| `src/pages/series/index.astro` | 시리즈 카드 커버 (`series-cover`) — 시리즈별 커스텀 인라인 디자인 |

커버 디자인(`series-cover` 내부 HTML)은 **`src/pages/series/index.astro`에만 존재**합니다.
홈에는 커버가 없으니 커버를 수정할 때 홈을 같이 건드릴 필요가 없습니다.

단, `src/pages/series/[slug].astro`의 히어로 배너에도 시리즈별 커스텀 디자인이 있습니다.
시리즈를 추가·변경할 때는 **`series/index.astro`(카드 커버)와 `series/[slug].astro`(히어로)** 두 곳을 함께 확인해야 합니다.

### 시리즈 메타 데이터 단일 소스

시리즈 배경색(`heroBg`), slug, 설명은 **`src/lib/utils.ts`의 `SERIES_META`** 가 유일한 정의 위치입니다.
새 시리즈를 추가하거나 기존 시리즈 정보를 바꿀 때는 이 파일만 수정하면 됩니다.

### 날짜·읽기시간 헬퍼는 반드시 `utils.ts`에서 import

날짜 포맷과 읽기 시간 계산은 **`src/lib/utils.ts`에만 정의**합니다.
페이지·레이아웃에서 지역 함수로 다시 정의하지 않습니다.

| 함수 | 출력 |
|---|---|
| `formatDate(date)` | `2026년 7월 28일` (ko-KR 긴 형식) |
| `formatShortDate(date)` | `2026.07.28` |
| `formatYearMonth(date)` | `2026.07` |
| `readingTime(body)` | 분 단위 정수 (마크다운 문법 제거 후 200단어/분) |

> 과거에 `formatDate`·`calculateReadingTime`이 4개 파일에 각각 정의되어 있었고,
> 읽기 시간 알고리즘이 파일마다 달라(180 vs 200단어/분) **같은 글이 페이지마다 다른 분 수로 표시되는 버그**가 있었습니다.
> 지역 재정의를 추가하면 이 문제가 재발합니다.

---

## 시리즈 관련 필터링 규칙

| 용도 | 필터 조건 |
|---|---|
| 블로그 글 목록 (`/blog`) | `!draft && !externalUrl` |
| 최근 글 (홈) | `!draft && !externalUrl` |
| 시리즈 카드 통계 (홈·`/series`) | `!draft && !!series` (externalUrl 스텁 포함) |
| 정적 페이지 생성 (`[...slug].astro`) | `!draft && !externalUrl` |
| 검색 인덱스 | `!draft && !externalUrl` |

externalUrl 스텁 포스트는 시리즈 편수 카운트·링크에는 표시되지만,
블로그 목록·홈 최신 글·검색·정적 생성에서는 제외됩니다.

---

## 빌드 검증

작업 후 반드시 실행:

```bash
npx astro check   # TypeScript 오류 0건 확인
npx astro build   # 빌드 성공 확인
```

---

## 브랜치 전략

- `main` 최신화 → 새 feature 브랜치 생성 → 작업 → 커밋/푸시
- main에 직접 커밋하지 않습니다.
