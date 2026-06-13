---
title: "Pet-Pass"
description: "반려동물 동반 가능 매장을 카카오 지도로 탐색하는 서비스. AI 협업(바이브 코딩) 방식으로 3주 만에 완성한 첫 번째 풀스택 프로젝트."
pubDate: 2026-04-01
repoUrl: "https://github.com/yskkkkkk/pet-pass-web"
liveUrl: "https://pet-pass-web.vercel.app"
blogUrl: "https://pet-pass-web.vercel.app/blog"
tags: ["Vanilla JS", "Node.js", "Supabase", "Vercel", "Kakao Maps API", "GitHub Actions"]
featured: false
---

정부 공공데이터에서 반려동물 동반 가능 매장을 수집해 카카오 지도 위에 표시하는 서비스. GitHub Actions 스케줄러가 매일 데이터를 갱신하고, Supabase PostgreSQL에 저장한다.

## 인프라

- **데이터 파이프라인**: 정부 API → Kakao Geocoding → Supabase, GitHub Actions로 일 2회 자동 실행
- **배포**: Vercel Serverless Functions + 보안 헤더 설정 (CSP, HSTS)
- **지도 통합**: Kakao Maps API, 클러스터링 및 모바일 바텀시트 UI

## 주요 기술 과제

- 정부 API 인증키 프록시 처리 (클라이언트 노출 방지)
- CP949 인코딩 엑셀 파일 파싱 문제 해결
- 모바일 지도·스크롤 충돌 — 바텀시트 3차 재설계
- Vercel 환경에서 외부 API 통신 타임아웃 대응

## 회고

3주 만에 완성했지만 지도 서비스의 높은 콜드 진입 장벽과 차별성 부재로 사용자 확보에 실패했다. 이 경험이 다음 프로젝트(피카밈)의 기획 방향을 결정했다.
