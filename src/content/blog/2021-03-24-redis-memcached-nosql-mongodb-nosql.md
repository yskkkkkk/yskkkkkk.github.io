---
title: "Untitled"
pubDate: 2021-03-24
description: "- redis, memcached > nosql - mongodb > nosql Redis 와 Memcached 는 모두 nosql 중 key-value 형 데이터베이스로 빠른 속도가 장점인 데이터 베이스다. 메모리 데이터 저장소. 캐시 형태로 데이터를 사용한다. Me"
tags: ["코딩이야기"]
series: ""
heroImage: ""
draft: false
---

- redis, memcached > nosql 

- mongodb > nosql 

Redis 와 Memcached 는 모두 nosql 중 key-value 형 데이터베이스로 빠른 속도가 장점인 데이터 베이스다. 메모리 데이터 저장소. 캐시 형태로 데이터를 사용한다. 

Memcached 는 문자열의 데이터구조만 처리한다. 백업 불가능. 메모리 재사용

Redis 는 싱글쓰레드. 스프링의 세션 클러스터링. 메모리와 디스크. 속도차이를 감수 하고도 운영적 기능에 중점

mongodb는 도큐멘트 지향 데이터 베이스로 json 데이터 구조로 저장한다. 스키마가 없다.  물리디스크에 저장.

  

- get post put delete > http , restful

- restful, msa

REpresentational State Transfer, MSA(Micro Service Architecture)

  

- 람다 vs for문 선호 하는거 > 

람다는 자원소모가 크고, 일부 상황에 따라 처리 속도가 느리다. but 깔끔한 코드 스크립트 언어 기술이라 아직 자바에서는 조금 최적화가 덜 된편

  

- 자바 메모리관리에 대해 고민해본적잇는지

- garbage collection

    아직 그렇게 큰 규모의 프로젝트는 진행하지 않아서 gc 믿고 한다.  

- java 1.8 특징, 자바 특징

- [Lambda Expression (람다표현식)](https://marrrang.tistory.com/17)
- [Method Reference (메소드 참조)](https://marrrang.tistory.com/18)
- [Stream (스트림)](https://marrrang.tistory.com/19) 
- [Default Method](https://marrrang.tistory.com/36) - interface의 모호함 제거
- Optional - null처리 
- Joda Time - localdatetime

- 자바 메모리영역  

heap vs non-heap 

- git (rebase, cherrypick)

merge가 브랜치 자체를 합치는 거라면 

rebase 는 깃트리 관리를 위해서 **Rebase는 기존의 커밋을 그대로 사용하는 것이 아니라 내용은 같지만 다른 커밋을 새로 만듭니다.**

cherrypick은 특정 커밋한 현재 브랜치에 합치는 것 

- 암호화방식 > 복호화가 가능한 암호화, 불가능한 암호화

비밀번호 단방향 sha + salt 추가 

다른애들은 양방향 aes url 단축에 써봤음 

- 개발하면서 중요하게 생각하는것 (ex. 중복코드처리, 테스트 등?)

	- 재사용성, but 자기 설명이 쉬워야 함

  

- 쿠키와 세션 차이

http 의 보안요소로 데이터를 저장하지 않는점 을 보완하기 위해 사용 

세션은 서버에 저장, 쿠키는 사용자의 컴퓨터에 저장 (쿠키는 빠르고, 세션은 보안 좋다)

- TDD, BDD, DDD  > 

테스트/행동/도메인 주도개발 로 가독성 안전성 확장가능성 객체지향성 상승 

- 패턴 > 

- 애자일 > vs 폭포수 모델

테스트를 해보는 개발 방법

- spring에서 @Controller, @RestController 차이 > @responsebody

view를 반환하는가 data를 반환하는가 

- jpa 영속성과 영속성 사이클 

- orm (객체-관계 매핑)

  

- jvm 구조

- oop > vs aop

  

- rxjava, webflux > spring stream

  

- static inner class 

  

- http, https차이 > 보안

  

- 쓰레드 

- 하이브리드앱, 네이티브앱, 웹앱 차이

- 트랜잭션 > about db

  

- sql 인젝션 (보안공격)

대응방안 - 입력값에 대한 검증(화이트리스트대상), Prepared Statement 사용, error message 노출 x, 웹방화벽 

- db index ****

db에서 효율적인 검색을 위한 것

- aws > ec2, sns, sqs, kubernetes	> server

- docker				> server