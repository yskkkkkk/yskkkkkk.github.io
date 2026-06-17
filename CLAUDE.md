# yskkkkkk.github.io — 코드 에이전트 작업 지침

## 핵심 원칙

이 파일은 AI 코딩 에이전트가 이 저장소를 작업할 때 반드시 먼저 읽어야 하는 주의사항 모음입니다.

> **블로그 글을 쓰거나 어투를 다듬을 때는 반드시 [`WRITING_STYLE.md`](./WRITING_STYLE.md)를 먼저 읽고 따릅니다.**

---

## 중복 렌더링 주의사항

### 시리즈 카드 커버 디자인

시리즈 커버 UI(`series-cover` 내부 HTML)는 **두 파일에 동시 존재**합니다:

| 파일 | 역할 |
|---|---|
| `src/pages/index.astro` | 메인 홈페이지의 아티클 시리즈 섹션 |
| `src/pages/series/index.astro` | `/series` 전용 목록 페이지 |

커버 디자인을 수정할 때는 **반드시 두 파일 모두** 동일하게 업데이트해야 합니다.
한 파일만 고치면 홈과 시리즈 페이지의 UI가 달라집니다.

### 시리즈 메타 데이터 단일 소스

시리즈 배경색(`heroBg`), slug, 설명은 **`src/lib/utils.ts`의 `SERIES_META`** 가 유일한 정의 위치입니다.
새 시리즈를 추가하거나 기존 시리즈 정보를 바꿀 때는 이 파일만 수정하면 됩니다.

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
