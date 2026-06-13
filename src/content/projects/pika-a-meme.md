---
title: "피카밈 (pick-a-meme)"
description: "가벼운 가챠형 밈 서비스 뒤에 실무 수준 백엔드를 의도적으로 설계한 프로젝트. 토이 프로젝트에도 Clean Architecture·DDD를 적용하고, 분산 락 기반 하트 동시성 제어와 Redis 캐시·Rate Limiting·OAuth2를 다뤘다."
pubDate: 2026-05-01
repoUrl: "https://github.com/yskkkkkk/pika-a-meme_full"
liveUrl: "https://pick-a-me.me"
blogUrl: "https://pick-a-me.me/blog"
tags: ["Kotlin", "Spring Boot", "Next.js", "PostgreSQL", "Redis", "Cloudflare R2", "Clean Architecture", "JPA"]
featured: true
---

Pet-Pass에서 "AI로 빠르게 만들 수 있다"를 확인한 뒤, 이번엔 "BaaS 없이 백엔드 역량을 그대로 증명한다"를 목표로 잡았다. 가챠형 밈 생성기라는 가벼운 외형을 택한 건, 그 뒤에 실무 수준의 아키텍처와 동시성 제어를 넣기 위해서였다. 버튼 한 번에 동물 사진·문구·스티커가 조합되는 단순한 화면 아래에서, 실제로 풀고 싶었던 건 다음 문제들이다.

## 아키텍처

Gradle 멀티 모듈로 백엔드를 4개 계층으로 분리했다. Clean Architecture + DDD 기반으로 설계해 도메인 로직이 인프라 의존성 없이 테스트 가능하도록 구성했다.

하트 시스템은 BASIC(시간 충전)과 SPECIAL(미션 획득)을 별도 저장소로 분리했다. BASIC은 Redis의 Lazy Charging 방식으로, SPECIAL은 PostgreSQL JPA로 관리한다.

## 주요 기술 과제

- **Lazy Upload**: 비로그인 밈은 R2 저장을 생략하고 로그인 전환 시 서버 동기화
- **Rate Limiting**: Redis 기반 "느린 DDoS" 방어 전략 설계
- **HttpOnly Cookie + OAuth2**: 로그아웃 5차례 디버깅 끝에 쿠키 정책 안정화
- **OAuth2 state 유실**: STATELESS 환경에서 state 파라미터 보존 문제 해결
- **i18n 구조 결정**: 백엔드·프론트엔드 번역 분리 기준 수립
- **@Cacheable 전략**: 캐시 적재 방어 로직 및 키 네이밍 설계
