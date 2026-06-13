---
title: "피카밈 (pick-a-meme)"
description: "동물 사진 + B급 감성 문구 조합 가챠형 밈 생성기. Kotlin/Spring Boot 백엔드와 Next.js 프론트엔드로 구성한 풀스택 포트폴리오 프로젝트."
pubDate: 2026-05-01
repoUrl: "https://github.com/yskkkkkk/pika-a-meme_full"
liveUrl: "https://pick-a-me.me"
blogUrl: "https://pick-a-me.me/blog"
tags: ["Kotlin", "Spring Boot", "Next.js", "PostgreSQL", "Redis", "Cloudflare R2", "Clean Architecture", "JPA"]
featured: true
---

버튼 하나로 동물 사진·문구·스티커가 무작위 조합되는 가챠형 밈 생성기. 비로그인 사용자도 결과를 링크로 공유할 수 있고, 로그인 시 저장·갤러리 기능을 이용할 수 있다.

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
