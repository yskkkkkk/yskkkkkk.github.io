---
title: "피카밈 개발기 — Kotlin/Spring Boot 풀스택 1개월 회고"
description: "동물 사진 + B급 감성 문구 가챠형 밈 생성기를 Kotlin/Spring Boot + Next.js로 만든 1개월 개발 기록. Clean Architecture, Redis 하트 시스템, OAuth2 쿠키 디버깅, Rate Limiting 설계까지."
pubDate: 2026-06-02
tags: ["Kotlin", "Spring Boot", "Next.js", "Redis", "Clean Architecture", "OAuth2", "풀스택", "포트폴리오"]
series: "피카밈 개발기"
draft: false
---

버튼 하나로 동물 사진·문구·스티커가 조합되는 가챠형 밈 생성기 [pick-a-meme](https://pick-a-me.me)을 만들었다. Kotlin/Spring Boot 백엔드와 Next.js 프론트엔드로 구성한 풀스택 프로젝트다.

백엔드 엔지니어 4년 경력을 포트폴리오로 보여주기 위해 시작했다. BaaS를 쓰면 JPA도, Spring Security도, 아키텍처 설계도 들어갈 자리가 없다. 그래서 직접 짰다.

## 주요 기술 선택과 문제들

Gradle 멀티 모듈로 백엔드를 4개 계층으로 분리했다. Clean Architecture + DDD 기반이다.

하트 시스템은 BASIC(시간 충전)과 SPECIAL(미션 획득)을 별도 저장소로 분리했다. Redis Lazy Charging과 PostgreSQL JPA를 각각 담당한다. 두 종류가 충전 방식도, 소비 로직도, 만료 정책도 다르기 때문이다.

OAuth2 로그아웃은 5번 디버깅했다. HttpOnly 쿠키 + SameSite 정책 + CORS가 겹치면서 예상치 못한 조합이 계속 터졌다. 로그아웃이 이렇게 어려운 문제인지 몰랐다.

비로그인 상태에서 밈을 뽑으면 즉시 R2에 저장하지 않는다. 로그인 전환 시점에 서버에 동기화한다. 비로그인 사용자가 대부분인 서비스에서 R2 저장 비용을 줄이기 위한 Lazy Upload 전략이다.

## 전체 개발기

13편으로 구성된 전체 개발기는 [pick-a-me.me/blog](https://pick-a-me.me/blog)에서 읽을 수 있다. 아키텍처 결정부터 OAuth2 디버깅, i18n 설계, Cloudflare 최적화, 1개월 회고까지 순서대로 기록했다.
