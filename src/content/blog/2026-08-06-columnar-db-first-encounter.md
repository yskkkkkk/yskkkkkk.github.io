---
title: "열 지향 DB라는 걸 오늘 처음 알았습니다"
pubDate: 2026-08-06
description: "같은 조건으로 뽑은 통계가 왜 매번 다르냐는 질문에서 시작해, 스냅샷 테이블과 열 지향 DB까지 알아본 하루를 정리합니다."
tags: ["DB", "TIL", "데이터"]
heroImage: ""
---

기획자분이 찾아와서 물으셨습니다. 지난주에 뽑은 타겟 유저 통계랑 오늘 뽑은 게 왜 다르냐고요. 분명 같은 조건으로 요청했는데 숫자가 안 맞는다는 이야기였습니다.

답은 알고 있었습니다. 운영 DB는 실시간 서비스 처리에 맞춰져 있어서, 마케팅 수신 동의나 회원 등급 같은 값을 UPDATE로 덮어쓰거든요. 어제 동의했다가 오늘 철회한 회원이 있으면 어제 시점으로 되돌려볼 방법이 없습니다. 같은 쿼리라도 돌리는 순간의 최신 상태가 나오는 거고요.

## 지금까지는 문제가 아니었습니다

사실 이 답변이 처음은 아니었습니다. 비슷한 요청을 여러 번 받았고 매번 같은 설명을 했거든요.

그런데도 크게 문제가 되지 않았던 건 용도 때문이었습니다. 제가 뽑아드리던 데이터는 대부분 추이를 보는 용도였습니다. 기획자분들이 기능 개발 방향을 잡을 때 참고하거나, 간략한 성과 보고에 쓰이는 정도요.

세금 계산을 하거나 정산을 때리는 데이터가 아니었으니까요. 소수점까지 맞아떨어질 필요가 없었습니다.

지금까지 일해온 환경이 다 그랬습니다. 업무 테이블에서 바로 뽑아서 드렸고, 그걸로 충분했거든요.

## 대시보드 이야기가 나왔습니다

이번엔 상황이 조금 달랐습니다. 저희 부서가 아닌 다른 부서에서 대시보드를 만든다는 이야기가 나왔거든요.

한 번 뽑고 끝나는 데이터가 아니라, 계속 떠 있는 화면이 생기는 겁니다. 그러면 "지난달에 본 숫자가 왜 지금 다르냐"는 질문이 반복될 수밖에 없습니다.

이야기가 자연스럽게 깊어졌습니다. 통계 테이블이라는 게 필요하겠다는 생각은 막연히 갖고 있었는데, 이번엔 제대로 알아둬야겠다 싶더라고요. 그래서 LLM에게 물어봤습니다.

## 먼저 필요한 건 스냅샷입니다

정리하고 넘어가면, 기획자분 질문에 대한 답 자체는 스냅샷입니다.

매일 특정 시점의 상태를 그대로 찍어서 별도 테이블에 쌓아두는 거요. 그러면 7월 1일 기준으로 회원 등급이 무엇이었는지를 나중에도 그대로 꺼내볼 수 있습니다. 원본이 몇 번을 덮어써지든 상관없이요.

여기까지는 특별할 게 없습니다. 지금 쓰는 DB에 테이블 하나 더 만들면 되는 이야기니까요.

문제는 그 다음이었습니다. 회원이 수백만이면 하루에 수백만 행이 쌓이고, 한 달이면 억 단위가 됩니다. 이걸 어떻게 집계할 거냐는 질문이 따라오거든요.

## 열 지향이라는 방식

그 대목에서 열 지향 DB(Column-oriented DB)라는 걸 처음 들었습니다.

솔직히 오늘이 처음입니다. Java와 Spring으로 일해오면서 MySQL, PostgreSQL 같은 행 지향 RDB만 다뤄왔거든요. 데이터를 컬럼 단위로 쪼개서 저장하는 DB가 따로 있다는 걸 몰랐습니다.

차이는 디스크에 무엇을 붙여서 저장하느냐입니다.

<svg viewBox="0 0 600 215" width="100%" role="img" aria-label="행 지향과 열 지향의 디스크 저장 방식 비교" style="max-width:100%;height:auto;margin:8px 0 4px;font-family:var(--mono)">
  <text x="20" y="14" font-size="12" font-weight="600" fill="var(--text)">행 지향 — 레코드가 통째로 붙어 있음</text>
  <text x="44" y="32" font-size="9" fill="var(--text3)">회원 1</text>
  <text x="220" y="32" font-size="9" fill="var(--text3)">회원 2</text>
  <text x="396" y="32" font-size="9" fill="var(--text3)">회원 3</text>
  <g>
    <rect x="44" y="40" width="40" height="34" rx="3" fill="var(--accent)" fill-opacity="0.14" stroke="var(--accent)" stroke-opacity="0.4"/><text x="64" y="61" font-size="11" text-anchor="middle" fill="var(--text2)">1</text>
    <rect x="84" y="40" width="40" height="34" rx="3" fill="var(--accent)" fill-opacity="0.14" stroke="var(--accent)" stroke-opacity="0.4"/><text x="104" y="61" font-size="11" text-anchor="middle" fill="var(--text2)">김</text>
    <rect x="124" y="40" width="40" height="34" rx="3" fill="var(--accent)" fill-opacity="0.34" stroke="var(--accent)" stroke-width="1.6"/><text x="144" y="61" font-size="11" text-anchor="middle" fill="var(--text)" font-weight="600">서울</text>
    <rect x="164" y="40" width="40" height="34" rx="3" fill="var(--accent)" fill-opacity="0.14" stroke="var(--accent)" stroke-opacity="0.4"/><text x="184" y="61" font-size="11" text-anchor="middle" fill="var(--text2)">VIP</text>
    <rect x="220" y="40" width="40" height="34" rx="3" fill="var(--accent)" fill-opacity="0.14" stroke="var(--accent)" stroke-opacity="0.4"/><text x="240" y="61" font-size="11" text-anchor="middle" fill="var(--text2)">2</text>
    <rect x="260" y="40" width="40" height="34" rx="3" fill="var(--accent)" fill-opacity="0.14" stroke="var(--accent)" stroke-opacity="0.4"/><text x="280" y="61" font-size="11" text-anchor="middle" fill="var(--text2)">이</text>
    <rect x="300" y="40" width="40" height="34" rx="3" fill="var(--accent)" fill-opacity="0.34" stroke="var(--accent)" stroke-width="1.6"/><text x="320" y="61" font-size="11" text-anchor="middle" fill="var(--text)" font-weight="600">부산</text>
    <rect x="340" y="40" width="40" height="34" rx="3" fill="var(--accent)" fill-opacity="0.14" stroke="var(--accent)" stroke-opacity="0.4"/><text x="360" y="61" font-size="11" text-anchor="middle" fill="var(--text2)">일반</text>
    <rect x="396" y="40" width="40" height="34" rx="3" fill="var(--accent)" fill-opacity="0.14" stroke="var(--accent)" stroke-opacity="0.4"/><text x="416" y="61" font-size="11" text-anchor="middle" fill="var(--text2)">3</text>
    <rect x="436" y="40" width="40" height="34" rx="3" fill="var(--accent)" fill-opacity="0.14" stroke="var(--accent)" stroke-opacity="0.4"/><text x="456" y="61" font-size="11" text-anchor="middle" fill="var(--text2)">박</text>
    <rect x="476" y="40" width="40" height="34" rx="3" fill="var(--accent)" fill-opacity="0.34" stroke="var(--accent)" stroke-width="1.6"/><text x="496" y="61" font-size="11" text-anchor="middle" fill="var(--text)" font-weight="600">서울</text>
    <rect x="516" y="40" width="40" height="34" rx="3" fill="var(--accent)" fill-opacity="0.14" stroke="var(--accent)" stroke-opacity="0.4"/><text x="536" y="61" font-size="11" text-anchor="middle" fill="var(--text2)">VIP</text>
  </g>
  <text x="44" y="92" font-size="11" fill="var(--text2)">지역 3칸이 필요한데 12칸을 전부 읽어야 합니다.</text>

  <text x="20" y="128" font-size="12" font-weight="600" fill="var(--text)">열 지향 — 같은 컬럼끼리 모여 있음</text>
  <text x="36" y="146" font-size="9" fill="var(--text3)">id</text>
  <text x="172" y="146" font-size="9" fill="var(--text3)">이름</text>
  <text x="308" y="146" font-size="9" fill="var(--accent)" font-weight="700">지역</text>
  <text x="444" y="146" font-size="9" fill="var(--text3)">등급</text>
  <g>
    <rect x="36" y="154" width="40" height="34" rx="3" fill="var(--bg3)" stroke="var(--border)"/><text x="56" y="175" font-size="11" text-anchor="middle" fill="var(--text3)">1</text>
    <rect x="76" y="154" width="40" height="34" rx="3" fill="var(--bg3)" stroke="var(--border)"/><text x="96" y="175" font-size="11" text-anchor="middle" fill="var(--text3)">2</text>
    <rect x="116" y="154" width="40" height="34" rx="3" fill="var(--bg3)" stroke="var(--border)"/><text x="136" y="175" font-size="11" text-anchor="middle" fill="var(--text3)">3</text>
    <rect x="172" y="154" width="40" height="34" rx="3" fill="var(--bg3)" stroke="var(--border)"/><text x="192" y="175" font-size="11" text-anchor="middle" fill="var(--text3)">김</text>
    <rect x="212" y="154" width="40" height="34" rx="3" fill="var(--bg3)" stroke="var(--border)"/><text x="232" y="175" font-size="11" text-anchor="middle" fill="var(--text3)">이</text>
    <rect x="252" y="154" width="40" height="34" rx="3" fill="var(--bg3)" stroke="var(--border)"/><text x="272" y="175" font-size="11" text-anchor="middle" fill="var(--text3)">박</text>
    <rect x="308" y="154" width="40" height="34" rx="3" fill="var(--accent)" fill-opacity="0.34" stroke="var(--accent)" stroke-width="1.6"/><text x="328" y="175" font-size="11" text-anchor="middle" fill="var(--text)" font-weight="600">서울</text>
    <rect x="348" y="154" width="40" height="34" rx="3" fill="var(--accent)" fill-opacity="0.34" stroke="var(--accent)" stroke-width="1.6"/><text x="368" y="175" font-size="11" text-anchor="middle" fill="var(--text)" font-weight="600">부산</text>
    <rect x="388" y="154" width="40" height="34" rx="3" fill="var(--accent)" fill-opacity="0.34" stroke="var(--accent)" stroke-width="1.6"/><text x="408" y="175" font-size="11" text-anchor="middle" fill="var(--text)" font-weight="600">서울</text>
    <rect x="444" y="154" width="40" height="34" rx="3" fill="var(--bg3)" stroke="var(--border)"/><text x="464" y="175" font-size="11" text-anchor="middle" fill="var(--text3)">VIP</text>
    <rect x="484" y="154" width="40" height="34" rx="3" fill="var(--bg3)" stroke="var(--border)"/><text x="504" y="175" font-size="11" text-anchor="middle" fill="var(--text3)">일반</text>
    <rect x="524" y="154" width="40" height="34" rx="3" fill="var(--bg3)" stroke="var(--border)"/><text x="544" y="175" font-size="11" text-anchor="middle" fill="var(--text3)">VIP</text>
  </g>
  <text x="36" y="206" font-size="11" fill="var(--text2)">지역 컬럼 3칸만 읽고 끝납니다.</text>
</svg>

행 지향은 레코드 하나를 통째로 붙여서 저장합니다. 회원 한 명의 아이디, 이름, 지역, 등급이 디스크에서 옆자리에 나란히 놓이는 식이고요.

열 지향은 반대로 같은 컬럼끼리 모읍니다. 아이디는 아이디끼리, 지역은 지역끼리 따로 보관합니다.

이게 왜 중요하냐면, 통계 쿼리는 보통 컬럼 몇 개만 보거든요. 지역별 회원 수를 세려면 지역 컬럼만 있으면 됩니다.

행 지향에서는 그게 안 됩니다. 지역 값 하나를 읽으려고 옆에 붙어 있는 이름, 가입일, 나머지 전부를 디스크에서 같이 퍼 올려야 합니다. 필요 없는 데이터를 읽는 데 대부분의 시간을 쓰는 셈이죠.

압축도 훨씬 잘 됩니다. 같은 컬럼에는 같은 타입의 값이 모여 있고, 지역이나 등급처럼 값의 종류가 적은 컬럼은 반복이 많거든요. 같은 값이 연달아 나오면 "서울이 몇 번 반복" 식으로 줄여서 저장할 수 있습니다.

알고리즘 문제 풀 때나 보던 방식이 실제 DB 저장 구조로 쓰이고 있다는 게 재밌었습니다. 듣자마자 "대용량이면 무조건 이게 낫겠는데?" 싶더라고요.

## 그럼 운영 DB도 이걸로 하면 되지 않나

당연히 이 생각이 따라왔습니다. 읽는 게 이렇게 빠르면 처음부터 다 열 지향으로 쓰면 되지 않나 싶었거든요.

그런데 쓰기를 생각하면 답이 나옵니다.

회원 한 명이 가입할 때 행 지향에서는 한 자리에 한 번 쓰면 끝입니다. 열 지향에서는 아이디 저장소, 이름 저장소, 지역 저장소를 각각 찾아가서 한 조각씩 나눠 써야 하고요.

수정은 더 껄끄럽습니다. 압축해서 뭉쳐둔 덩어리 안의 값 하나를 바꿔야 하니까요. 그래서 열 지향 DB들은 아예 즉시 수정을 포기하고, 변경 사항을 따로 기록해뒀다가 나중에 몰아서 정리하는 방식을 씁니다.

이커머스는 주문과 결제가 실시간으로 들어옵니다. 한 건 한 건을 빠르고 안전하게 처리하는 게 핵심이고요. 여기에 열 지향을 쓰면 안 되는 이유가 분명합니다.

## 나눠 쓰는 이유

그래서 두 개를 나눠 쓴다는 걸 알게 됐습니다.

운영 시스템은 행 지향으로 실시간 트랜잭션을 처리하고(OLTP), 분석 시스템은 그 데이터를 배치나 파이프라인으로 넘겨받아 열 지향에 쌓아두고 무거운 집계를 전담합니다(OLAP).

그동안 통계 요청이 들어오면 운영 DB에 인덱스를 어떻게 걸지, 쿼리를 어떻게 비틀지만 고민했거든요. 애초에 다른 판에서 푸는 문제였던 셈입니다.

## 마치며

실제로 제가 한 건 없습니다.

데이터 추출을 담당하시는 개발자분이 따로 계시고, 저는 업무 영역이 겹쳐서 이야기를 많이 나눈 정도입니다. 대시보드도 여러 한계 때문에 회원 정보에 한해서는 업무 데이터로 통계를 보여주기로 정리됐고요.

주문 데이터는 이미 배치로 정제하는 과정이 있다고 들었는데, 그게 오늘 알게 된 형태인지는 아직 모릅니다.

시간이 없어서 여기까지만 알아봤습니다. 그래도 눈이 번쩍 뜨인 날에 써두는 게 나을 것 같아서 남겨둡니다...
