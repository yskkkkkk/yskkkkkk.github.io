---
title: "개인화 추천 모듈의 Redis 캐시 skip을 AtomicReference로 동적 관리하기"
pubDate: 2025-09-10
description: "shopCode 기반 정적 properties 관리의 한계를 넘어, moduleCd와 Redis 헬스 응답을 기반으로 캐시 적용 여부를 런타임에 동적으로 판별하도록 개선한 과정을 기록합니다."
series: "Redis 프로젝트 회고"
tags: ["redis", "java", "concurrency", "atomicreference", "backend", "personalization"]
heroImage: ""
---

### 🤦 문제 발생

초기에는 개인화 추천 영역 중 일부 모듈을 `shopCode`로 관리해서, properties로 고정 처리하도록 운영했다. 개발 초기에는 안정적이었지만 운영 중 아래 문제가 발생했다.

- 운영자가 새 추천 모듈을 추가했는데, 이를 properties에 반영하지 못한 경우가 생겼다.
- 새로 추가된 모듈이 Redis 캐싱 대상으로 들어가면서, 다수 사용자에게 동일한(개인화가 아닌) 데이터가 노출되는 사고가 났다.
- 특정 추천 영역이 의도치 않게 전역 캐시 대상이 되어 개인화 성격이 훼손됐다.

---

### 🔍 원인 파악

**1. shopCode 기반 예외 관리의 한계**

`shopCode`로 모듈을 하드코딩하면, 새로운 모듈 추가 시 운영자가 properties를 편집하지 않으면 기본 캐시 정책이 적용된다. 운영 환경에서 properties 동기화 누락 또는 배포 시점 불일치가 발생하면 예외 처리가 누락된다.

**2. 캐시 적용 범위 결정 로직의 불명확성**

개인화 성격의 컨텐츠(사용자별 다른 값)를 전역 캐시에 넣으면 정합성·보안·비즈니스 측면에서 문제가 된다.

**3. 런타임 정책과 분리된 결정**

캐시 사용 여부를 단순히 properties에 의존하지 않고, 런타임에 Redis 헬스/정책을 조회해 결정하면 운영 편의성과 안전성을 높일 수 있다.

---

### ✅ 해결

**핵심 아이디어**: `shopCode` 기반 고정 처리를 버리고, `moduleCd` 기반으로 추천 영역의 성격을 판별한다. Redis 사용 여부 판단은 Redis 헬스 체크 응답의 `personalizedContents` 데이터를 통해 동적으로 결정한다.

```java
// AtomicReference로 skip 집합을 안전하게 갱신하고 조회
private final AtomicReference<Set<String>> skipMdulCdSet = new AtomicReference<>(Collections.emptySet());
private final AtomicReference<Set<String>> skipBnrDspTypeCdSet = new AtomicReference<>(Collections.emptySet());
private final AtomicReference<Set<String>> skipGdTypeCdSet = new AtomicReference<>(Collections.emptySet());

protected void setSkipModules(RedisCacheDataVO redisCacheDataVO, String personalizedContents) {
    if (redisCacheDataVO == null || redisCacheDataVO.getMdulShopCd() == null
            || redisCacheDataVO.getMdulShopCd().trim().isEmpty()) {
        return; // module 이외의 캐시 데이터는 skip
    }
    try {
        JsonNode root = mapper.readTree(personalizedContents);
        updateRef(root, "mdulCd", skipMdulCdSet);
        updateRef(root, "bnrDspTypeCd", skipBnrDspTypeCdSet);
        updateRef(root, "gdTypeCd", skipGdTypeCdSet);
    } catch (Exception e) {
        skipMdulCdSet.set(Collections.emptySet());
        skipBnrDspTypeCdSet.set(Collections.emptySet());
        skipGdTypeCdSet.set(Collections.emptySet());
    }
}

/**
 * fieldName에 해당하는 JSON 배열을 새 Set으로 만들고,
 * 기존 ref.get()과 비교해 필요 시 CAS로 업데이트
 */
private void updateRef(JsonNode root, String fieldName, AtomicReference<Set<String>> ref) {
    Set<String> newSet = mapper.convertValue(root.get(fieldName), new TypeReference<Set<String>>() {});
    newSet = newSet != null ? Collections.unmodifiableSet(newSet) : Collections.emptySet();

    Set<String> currentSet;
    do {
        currentSet = ref.get();
        if (newSet.equals(currentSet)) return; // 변경 없으면 바로 종료
    } while (!ref.compareAndSet(currentSet, newSet)); // CAS 성공 시 루프 탈출
}

protected boolean getSkipModules(String mdulCd) {
    Set<String> mdulSet = skipMdulCdSet.get();
    Set<String> bnrSet  = skipBnrDspTypeCdSet.get();
    Set<String> gdSet   = skipGdTypeCdSet.get();

    // AtomicReference가 비어 있으면 properties 폴백
    if (mdulSet.isEmpty() && bnrSet.isEmpty() && gdSet.isEmpty()) {
        String skipProp = Optional.ofNullable(PropertyUtil.getString("redis.skip.modules"))
            .filter(s -> !s.trim().isEmpty()).orElse("");
        mdulSet = Arrays.stream(skipProp.split(","))
            .map(String::trim)
            .filter(s -> !s.isEmpty())
            .collect(Collectors.toSet());
    }

    String[] tokens = mdulCd.split("-");
    String bnrDspTypeCd = tokens.length > 2 ? tokens[2] : "";
    String gdTypeCd = tokens.length > 3 && !tokens[3].isEmpty() ? tokens[3].substring(0, 1) : "";

    return mdulSet.contains(mdulCd) || bnrSet.contains(bnrDspTypeCd) || gdSet.contains(gdTypeCd);
}

/** Redis 사용 여부 체크 */
protected boolean skipRedisCondition(RedisCacheDataVO redisCacheDataVO) {
    try {
        // redis health check 로직 ...
        setSkipModules(redisCacheDataVO, String.valueOf(data.get("personalizedContentsVal")));
        return !baseCanUse;
    } catch (Exception e) {
        return true; // Redis API 호출 실패 시 Redis 사용 skip
    }
}
```

---

### 🧪 검증

- `personalizedContentsVal`에 포함된 `mdulCd`/`bnrDspTypeCd`/`gdTypeCd` 필드가 올바른 JSON 배열로 내려오는지 확인했다.
- CAS로 `AtomicReference`가 안정적으로 갱신되는지 단위 테스트를 작성했다.
- 트래픽이 적은 도메인에 먼저 적용해 skip 리스트가 정상 동작하는지 검증한 뒤 점진적으로 확장했다.

---

### 🎉 효과 / 깨달음

- `shopCode` 기반 정적 관리에서 `moduleCd` 기반 동적 판별로 전환하면서, **운영자가 properties를 깜빡해도 안전한 구조**가 됐다.
- Redis 헬스 응답의 `personalizedContentsVal`을 런타임에 반영하니, 새로운 추천 모듈이 추가돼도 즉시 개인화 여부를 제어할 수 있다.
- `AtomicReference` + CAS 패턴으로 멀티스레드 환경에서도 안전하게 skip 집합을 교체할 수 있었다.
- 개인화 영역은 "전역 캐시 허용 여부"를 엄격히 통제해야 하며, 런타임 정책으로 운영 편의성과 안전성을 동시에 달성할 수 있다.
