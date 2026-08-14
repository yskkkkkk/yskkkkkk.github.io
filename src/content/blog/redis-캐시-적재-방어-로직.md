---
title: "Redis 캐시 적재 중 NPE와 캐스팅 에러 방어하기"
pubDate: 2025-09-04
description: "외부 API에서 bnrSeq가 누락되거나 타입이 섞여 들어오는 케이스를 instanceof 타입 가드와 방어 로직으로 안전하게 처리한 과정을 기록합니다."
series: "Redis 프로젝트 회고"
tags: ["redis", "cache", "java", "backend", "defensive-programming"]
heroImage: ""
---

### 문제 발생

배너 데이터를 Redis에 저장하면서, `bnrSeq` 값이 없는 케이스가 종종 들어왔다. 원래는 무조건 존재한다고 가정하고 Map을 파싱했는데:

- `bnrSeq`가 `null`이거나 비어 있는 경우 → NPE 발생
- 리스트 안에 Map이 섞여 들어오는 경우도 있어서 캐스팅 에러 발생
- 결국 캐시 로딩이 중간에 터져서 나머지 데이터도 못 올라감

---

### 원인 파악

- 데이터 제공 API가 간헐적으로 `bnrSeq`를 내려주지 않는 경우가 있었다.
- VO 변환 시 타입 체크를 제대로 하지 않아서 `List<Object>` 안에 Map이 섞이면 런타임 에러가 발생했다.
- 개발 단계에서는 테스트 데이터가 항상 정상이라 실서버에서만 문제가 드러났다.

---

### 해결

안전하게 `bnrSeq`를 꺼내도록 방어 로직을 넣고, 리스트/맵 타입을 먼저 점검하도록 수정했다.

```java
private String safeGetBnrSeq(Object obj) {
    if (obj instanceof Map) {
        Object seq = ((Map<?, ?>) obj).get("bnrSeq");
        return seq != null ? String.valueOf(seq) : "";
    }
    return "";
}

public void processBannerList(List<Object> list) {
    for (Object o : list) {
        String bnrSeq = safeGetBnrSeq(o);
        if (StringUtils.isNotBlank(bnrSeq)) {
            // 정상 케이스만 Redis에 적재
            redisService.set("bnr:" + bnrSeq, o.toString(), 3600);
        } else {
            log.warn("bnrSeq 누락 데이터 무시: {}", o);
        }
    }
}
```

포인트:

- `instanceof`로 타입 보장
- `bnrSeq`가 없으면 빈 문자열을 반환하고 무시 처리
- Redis에 올라가는 값은 항상 key-value가 보장된 상태

---

### 효과 / 깨달음

- 런타임 에러가 사라지고, 문제가 되는 데이터는 무시 처리로 전환해 서비스 안정성을 확보했다.
- 로그로만 기록하니 원본 데이터 문제도 쉽게 트래킹 가능해졌다.
- **외부 데이터는 절대 신뢰하면 안 된다**. 캐시 적재 전에 무조건 필터링과 검증이 필요하다.
