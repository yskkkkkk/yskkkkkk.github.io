---
title: "스프링 트랜잭션 설정 오류와 리팩토링 계획 (feat. 에이전트와의 과외)"
pubDate: "2026-06-23"
description: "AI 에이전트와 코틀린/스프링 공부를 하다가 우연히 발견한 @Transactional 무효화 현상과 이를 해결하기 위한 리팩토링 로드맵"
tags: ["Spring", "Transaction", "AOP", "Refactoring", "TIL"]
heroImage: ""
---

최근에 AI 에이전트들과 과외를 시작했습니다.

주요 과목은 자바 스프링과 코틀린인데, 특히 코틀린은 아직 제가 모르는 부분이 너무 많아서 기초부터 차근차근 배우고 있습니다.

오늘도 에이전트와 트랜잭션, 그리고 AOP 주입에 관해 이런저런 이야기를 나누고 있었습니다.

제가 정확히 이해가 안 가는 부분이 있어서, "우리 프로젝트에 있는 트랜잭션 코드를 보고 설명해 줘" 하면서 운영 소스 일부를 긁어서 주었거든요.

그런데 에이전트가 코드를 빤히 보더니 조심스럽게 한마디 하더군요.

"이거... 트랜잭션 작동 안 하고 있는 것 같은데요?"

에이전트에게 뒤통수를 맞은 기분이었습니다.

설마 하고 설정 파일을 뒤적거려 보니, 진짜였습니다.

스프링 설정 파일에 있어야 할 `<tx:annotation-driven>` 설정이 누락되어 있었던 겁니다.

이로 인해 코드 곳곳에 안전망처럼 걸어둔 `@Transactional` 어노테이션들이 전부 작동하지 않는 가짜(Dead Code)로 방치되고 있었습니다.

---

구체적으로 어떤 상황이었는지 차근차근 팩트 체크를 해보겠습니다.

### 작동하지 않는 어노테이션과 숨어있던 위협

문제의 시작은 다건의 사은품을 지급하는 `selectApplyTicketEventOrder` 로직이었습니다.

개발할 당시에는 "사은품 중 하나라도 오류가 나면 전체를 취소(Rollback)하자"는 명확한 의도로 메서드 상단에 `@Transactional(rollbackFor = Exception.class)`을 야심 차게 적어두었습니다.

하지만 이 어노테이션을 감지하고 프록시를 생성해 주는 `<tx:annotation-driven>` 설정이 설정 파일 어디에도 없었습니다.

결국 이 메서드는 트랜잭션 없이 각 쿼리가 실행되는 족족 Auto-Commit 방식으로 DB에 박히고 있었습니다. 

<div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; font-family: sans-serif; margin: 20px 0;">
  <div style="font-size: 0.85rem; color: #4f46e5; font-weight: 700; margin-bottom: 12px;">Loop: insertApplyTicketEventGift() (총 5개 지급 예정)</div>
  <div style="display: flex; align-items: center; margin-bottom: 10px;">
    <span style="background-color: #dcfce7; color: #15803d; font-size: 0.75rem; font-weight: 700; padding: 3px 8px; border-radius: 6px; margin-right: 12px; min-width: 35px; text-align: center;">성공</span>
    <span style="font-size: 0.9rem; color: #334155;">사은품 1번 등록 <span style="color: #64748b; font-size: 0.8rem;">(Auto-Commit 됨)</span></span>
  </div>
  <div style="display: flex; align-items: center; margin-bottom: 10px;">
    <span style="background-color: #dcfce7; color: #15803d; font-size: 0.75rem; font-weight: 700; padding: 3px 8px; border-radius: 6px; margin-right: 12px; min-width: 35px; text-align: center;">성공</span>
    <span style="font-size: 0.9rem; color: #334155;">사은품 2번 등록 <span style="color: #64748b; font-size: 0.8rem;">(Auto-Commit 됨)</span></span>
  </div>
  <div style="display: flex; align-items: center; border-bottom: 1px dashed #e2e8f0; padding-bottom: 12px; margin-bottom: 12px;">
    <span style="background-color: #fee2e2; color: #b91c1c; font-size: 0.75rem; font-weight: 700; padding: 3px 8px; border-radius: 6px; margin-right: 12px; min-width: 35px; text-align: center;">에러</span>
    <span style="font-size: 0.9rem; color: #dc2626; font-weight: 600;">사은품 3번 등록 실패 <span style="color: #b91c1c; font-size: 0.8rem;">(Exception 발생)</span></span>
  </div>
  <div>
    <h4 style="font-size: 0.9rem; color: #dc2626; margin: 0 0 6px 0; font-weight: 700;">결과: 부분 커밋(Partial Commit)에 따른 데이터 불일치</h4>
    <p style="font-size: 0.85rem; color: #64748b; margin: 0; line-height: 1.6;">하나의 트랜잭션으로 묶여있지 않기 때문에 롤백은 일어나지 않습니다. 시스템 프로세스는 중단되었지만, 이미 입력된 1번, 2번 사은품 내역은 DB에 그대로 남는 불완전한 상태가 됩니다.</p>
  </div>
</div>

물론 시스템이 아예 엉망으로 굴러가진 않았습니다.

과거에 이름 규칙으로 묶어둔 구형 XML AOP 설정 덕분에, 메서드 이름이 `Tx`로 끝나는 일부 로직들은(예: `~ServiceImpl.*Tx(..)`) 트랜잭션이 작동하고 있긴 했습니다.

다만 이것도 가성비가 썩 좋지 않았습니다.

단일 쿼리만 실행하는 단순 메서드조차 이름 끝에 `Tx`가 붙어 있다는 이유로 굳이 트랜잭션이 발동되어, 네트워크 통신 시 `SET autocommit=0`과 `COMMIT` 통신이 강제로 얹어지면서 통신 낭비(Round-trip 3배 증가)가 발생하고 있었습니다. 

편지 봉투 한 장 배달하는데 굳이 현금 수송 차량을 부르는 격이었달까요.

---

### 데드 코드가 만든 '역설적인 안전'

하지만 진짜 아이러니는 외부 결제(PG사) 연동 인터페이스에서 일어났습니다.

코드 전수 조사를 하다 보니 외부 통신을 담당하는 `TossInterface.cardApproval` 메서드에도 `@Transactional`이 자랑스럽게 붙어 있는 것을 보았습니다.

이건 외부 API를 호출하는 네트워크 I/O 작업이라 시간이 꽤 걸리는 부분입니다.

만약 이 어노테이션이 실제로 작동했다면 어떤 일이 벌어졌을까요?

첫째로, 메서드가 시작되자마자 DB 커넥션 풀에서 커넥션을 획득하게 됩니다.

둘째로, 이 커넥션을 손에 꼭 쥔 채로 외부 PG사 응답이 올 때까지 3~5초 동안 멍하니 대기합니다.

피크 타임에 결제 요청이 수십 개만 동시에 몰려도 DB 커넥션 풀이 순식간에 말라버렸을 겁니다.

결국 결제와 아무 상관 없는 단순 조회 화면조차 응답 대기 상태(Hang)로 들어가며 서버가 다운되었겠지요.

다행히 스프링 설정 누락으로 `@Transactional`이 완벽하게 무효화되어 있었던 덕분에, 외부 I/O가 돌 때 DB 커넥션을 점유하지 않아 시스템 전체가 셧다운되는 최악의 장애는 피해 갈 수 있었습니다.

데이터 정합성은 찢어졌는데, 인프라의 목숨은 건진 웃픈 '역설적인 안전'이 유지되고 있었던 겁니다.

---

### 해결책과 점진적 리팩토링 로드맵

이 문제를 해결하기 위해서는 외부 결제 통신과 내부 DB 작업을 철저히 쪼개야 합니다.

이를 위해 Facade 패턴을 도입하여 구조를 개편하기로 했습니다.

```java
// 1. [트랜잭션 밖] DB 점유 없이 PG사 외부 통신 완료
TossResult result = tossInterface.cardApproval(request); 

// 2. [트랜잭션 안] 결제 통신이 성공한 경우에만 내부 DB 로직을 단일 트랜잭션으로 묶음
if (result.isSuccess()) {
    orderService.processOrderCompleteTx(order, stock, log);
}
```

한 번에 모든 걸 뜯어고치다간 또 다른 사이드 이펙트가 발생할 수 있어, 다음과 같이 3단계 로드맵을 세워 점진적으로 마이그레이션할 계획입니다.

- **Phase 1 (즉시):** 당장 시급한 외부 통신과 DB 트랜잭션을 분리하고, 기존 XML AOP 규칙(`~Tx` 명명)을 활용해 연관된 DB 로직들을 단일 흐름으로 묶어 급한 불을 끕니다.
- **Phase 2 (단기):** `<tx:annotation-driven>` 설정을 활성화하여 안전망을 복원하고, 기존의 가짜 `@Transactional` 데드 코드를 전수 정비하여 필요한 곳에만 올바르게 배치합니다.
- **Phase 3 (장기):** 이름 매핑(`~Tx`)에 의존해 커넥션을 무의미하게 소모하던 낡은 XML 설정을 완전히 걷어내고, 명시적인 어노테이션 기반 트랜잭션으로 100% 전환합니다.

---

의외의 곳에서 과외 공부 효과를 톡톡히 보고 있네요.

이번 트랜잭션 회고 내용은 잘 정리해서 다가올 6월 팀 회고 때 공유할 생각입니다.

이후에는 또 어떤 잠재 버그들이 발각될지 벌써부터 기대 반 두려움 반입니다...

아래 슬라이드는 6월 팀 회고 발표를 위해 작성해 본 HTML 프레젠테이션 자료입니다. 슬라이드를 넘기며 자세한 내용과 시각적 다이어그램을 확인해 보실 수 있습니다.

### 프레젠테이션 슬라이드 (직접 넘겨보세요!)

<iframe 
  src="/presentations/retrospective-202606/index.html" 
  width="100%" 
  height="600px" 
  style="border: 1px solid #ddd; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"
  allowfullscreen>
</iframe>
