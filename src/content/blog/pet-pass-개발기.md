---
title: "Pet-Pass 개발기 — AI 협업으로 3주 만에 만든 반려동물 지도 앱"
description: "반려동물 동반 가능 매장을 카카오 지도로 탐색하는 서비스를 바이브 코딩 방식으로 3주 만에 완성한 기록. GitHub Actions 데이터 파이프라인, 모바일 바텀시트 UX, CP949 인코딩 문제까지."
pubDate: 2026-04-15
tags: ["Vanilla JS", "Node.js", "Supabase", "Vercel", "Kakao Maps", "GitHub Actions", "바이브코딩"]
series: "Pet-Pass 개발기"
draft: false
---

반려동물 동반 가능 매장을 카카오 지도 위에서 탐색하는 서비스 [Pet-Pass](https://pet-pass-web.vercel.app)를 만들었다. AI 협업(바이브 코딩) 방식으로 3주 만에 완성했다.

서버리스 Vanilla JS + Node.js + Supabase 스택으로 구성했다. GitHub Actions가 매일 정부 공공데이터를 수집해 Kakao Geocoding을 거쳐 Supabase PostgreSQL에 동기화한다.

## 기술적으로 기억에 남는 것들

정부 API 인증키를 클라이언트에 노출하지 않으려고 Vercel Functions로 프록시 레이어를 만들었다. Kakao Maps API는 잘 됐는데 정부 API만 안 됐다. 원인은 CORS 정책 차이였다.

모바일 지도와 스크롤이 충돌했다. 바텀시트를 세 번 다시 만들었다. 터치 이벤트 처리가 생각보다 훨씬 복잡했다.

엑셀 파일의 `?` 하나가 수십 번의 시도 끝에 CP949 인코딩 문제로 밝혀졌다. Node.js 기본 스트림이 UTF-8을 가정하기 때문에 발생하는 문제였다.

## 결과와 배운 것

서비스는 잘 돌아갔지만 아무도 쓰지 않았다. 지도 앱은 콜드 진입 장벽이 높고, 비슷한 서비스가 이미 많았다. 기술이 있다고 사람이 오는 게 아니라는 걸 확인했다.

이 경험이 다음 프로젝트 피카밈의 기획 방향을 결정했다 — 즉각성, 바이럴, 단순함.

## 전체 개발기

9편으로 구성된 전체 개발기는 [pet-pass-web.vercel.app/blog](https://pet-pass-web.vercel.app/blog)에서 읽을 수 있다.
