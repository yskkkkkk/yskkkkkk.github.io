---
title: "Pet-Pass 개발기 #2: 지도 API 연동과 위치 기반 최적화"
pubDate: 2026-06-12
description: "지도 API를 연동하면서 겪었던 성능 이슈와 좌표 기반 데이터 필터링 경험을 회고합니다."
tags: ["PetPass", "지도API", "최적화", "트러블슈팅"]
series: "Pet-Pass 프로젝트"
heroImage: ""
draft: false
---

> 이 글은 **Pet-Pass** 전용 블로그에서 작성된 개발기의 요약(Teaser) 포스팅입니다.
> Pet-Pass만의 고유한 디자인과 인터랙션이 적용된 원본 블로그에서 전체 내용을 확인하실 수 있습니다.

## 기술적 도전

지도 기반 앱을 만들 때 가장 큰 허들은 역시 "렌더링 성능"과 "데이터 양의 조절"이었습니다.
화면을 이동할 때마다 수백 개의 마커를 새로 불러오고 그리는 과정에서 브라우저가 버벅거리는 현상을 겪었고, 이를 해결하기 위한 여러 최적화 기법을 도입했습니다.

이번 두 번째 개발기에서는:
- 지도 API 초기 연동 과정에서의 시행착오
- 사용자의 Viewport(보이는 화면) 좌표를 기준으로 데이터를 동적 페칭하는 방법
- 마커 클러스터링(Clustering)과 디바운스(Debounce)를 활용한 렌더링 최적화

에 대한 구체적인 코드와 트러블슈팅 과정을 다룹니다.

---

<br/>

<div style="text-align: center; margin: 40px 0;">
  <a href="https://pet-pass.vercel.app/blog/post2" target="_blank" rel="noopener noreferrer" style="background-color: var(--primary); color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    👉 Pet-Pass 오리지널 블로그에서 전체 글 읽기
  </a>
</div>
