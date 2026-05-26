# Blog Migration Log

## 완료
- [x] Astro + GitHub Pages 세팅
- [x] GitHub Actions 자동 배포
- [x] Velog 글 13개 수동 이전
- [x] Blogger 글 45개 변환 이전 (claude/blogger-migration 브랜치)
  - HTML → Markdown 변환 완료
  - 이미지 원본 URL 유지 (blogger.googleusercontent.com)

## TODO
- [ ] Untitled 글 33개 제목 수동 확인 및 수정
- [ ] PR 머지 (claude/blogger-migration → main)
- [ ] 이미지 273개 로컬 이전 (Blogger 삭제 전에 처리)
  - 이미지 포함 파일 23개에 `<!-- TODO: migrate images -->` 주석 있음
- [ ] pet-pass 블로그 이전
- [ ] pick-a-me 블로그 이전
- [ ] About 페이지 작성
- [ ] 다크/라이트 테마 토글 추가
- [ ] Notion 링크 연결
- [ ] Blogger 포스트 tags 정리 (현재 Blogger 카테고리 그대로 유입됨, 중복/불일치 정리 필요)
- [ ] 루트의 `convert_blogger.py` 및 `src/feed.atom` 삭제 (이관 완료 후 불필요)
- [ ] OG 이미지 / 소셜 메타태그 설정 (heroImage 미설정 포스트 다수)
- [ ] 블로그 목록 페이지 series 별 그룹핑 UI 추가
