# Blog Migration Log

## 완료
- [x] Astro + GitHub Pages 세팅
- [x] GitHub Actions 자동 배포
- [x] Velog 글 13개 수동 이전
- [x] Blogger 글 45개 변환 이전 (claude/blogger-migration 브랜치)
  - HTML → Markdown 변환 완료
  - 이미지 원본 URL 유지 (blogger.googleusercontent.com)
- [x] Untitled 글 33개 제목 수동 확인 및 수정
- [x] About 페이지 작성
- [x] 블로그 목록 페이지 series 별 그룹핑 UI 추가
- [x] 다크/라이트 테마 토글 추가
- [x] Notion 링크 연결
- [x] pet-pass 블로그 연결 (externalUrl 스텁 9편)
- [x] pick-a-me 블로그 연결 (externalUrl 스텁 13편)
  - 완전 이식 대신 스텁 방식 채택 — 시리즈에는 노출되고 클릭 시 외부 원문으로 이동
  - 필터링 규칙은 [`CLAUDE.md`](./CLAUDE.md) 참고
- [x] 소셜 메타태그 설정 (`BaseHead.astro`의 og/twitter 태그, `og-default.png` 폴백)
- [x] 검색엔진 등록 (Google Search Console, 네이버 서치어드바이저)
- [x] 루트의 `convert_blogger.py`·`src/feed.atom` 삭제 (이관 완료 후 불필요, 어디서도 참조되지 않음 확인)

## TODO
- [ ] 이미지 273개 로컬 이전 (Blogger 삭제 전에 처리)
  - 이미지 포함 파일 23개에 `<!-- TODO: migrate images -->` 주석 있음
- [ ] Blogger 포스트 tags 정리 (현재 Blogger 카테고리 그대로 유입됨, 중복/불일치 정리 필요)
- [ ] 포스트별 `heroImage` 지정 검토 (현재 대부분 빈 값 → `og-default.png`로 폴백 중)
  - 이미지 생성 시 AI 티 나는 조명(렌즈 플레어·네온 글로우·보케)을 피할 것
  - 긍정 키워드: flat lighting, overcast sky lighting, matte finish, diffused ambient light, documentary style, low contrast
  - 부정 키워드: volumetric lighting, lens flare, bloom, neon, cinematic lighting, glowing, bokeh, smooth skin

---

## ☁️ R2 CDN 연동 및 미디어 마이그레이션 계획 (예정)
블로그의 깃허브 레포지토리 용량 제한(1GB 권장) 이슈를 방지하고 전 세계 로딩 속도를 최적화하기 위해, 모든 정적 미디어(이미지, 프레젠테이션 등)를 Cloudflare R2 스토리지로 마이그레이션합니다.

### 1. Cloudflare R2 버킷 세팅 (유저 작업)
- Cloudflare 대시보드에서 신규 R2 버킷 생성.
- 외부 접근용 도메인 연결 (Custom Domain 권장) 및 퍼블릭 액세스 활성화.
- API 통신을 위한 Access Key ID 및 Secret Access Key 발급.

### 2. 타사 호스팅 이미지 다운로드
- 파이썬(또는 노드) 자동화 스크립트를 작성하여 마크다운 내부에 남은 타사 호스팅 이미지(`blogger.googleusercontent.com` 등 273개)를 일괄 다운로드.
- `<!-- TODO: migrate images -->` 주석이 달린 23개 파일을 중점으로 스캔.

### 3. R2 일괄 업로드 시스템 구축
- 다운로드 받은 기존 블로거 이미지들과 블로그 내부(`public/images` 등)의 고용량 에셋들을 AWS SDK(S3 Client)를 활용해 R2 버킷으로 일괄 업로드.

### 4. 마크다운 파일 원본 URL 자동 치환
- `src/content/blog/` 내부의 모든 `.md` 파일을 순회.
- 기존의 구글 블로거 이미지 주소 및 로컬 상대 경로(`./image.jpg`)를 모두 `https://[R2퍼블릭도메인]/경로` 로 일괄 변경(정규식 치환).

### 5. 레포지토리 경량화 및 커밋
- 로컬 `public/` 디렉토리 내에 존재하던 무거운 원본 이미지 파일들을 전부 삭제 (git 이력에서도 분리).
- LFS 없이 가벼워진 레포지토리를 원격에 반영하여 빠른 빌드 속도 및 용량 절약 달성.
