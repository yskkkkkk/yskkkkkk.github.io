---
title: "Redis WarmUp 개선과 TTL 다층화로 초반 응답 지연 줄이기"
pubDate: 2025-09-03
description: "캐시가 있음에도 초반 요청이 느린 아이러니를 WarmUp 비동기화, optionTTL 세분화, fastExpire 연계로 해결한 과정을 기록합니다."
tags: ["redis", "cache", "java", "spring", "backend", "performance"]
heroImage: ""
---

### 🤦 문제 발생

Redis 캐시를 쓰면서도 서비스 초반에 **첫 요청이 느려지는 문제**가 반복됐다. 특정 모듈이나 배너 데이터가 Redis에 올라가지 않은 상태에서 요청이 들어오면:

- 최초 호출이 DB/API를 직접 타면서 지연 발생
- 심하면 여러 사용자가 동시에 접근해 **DB 부하 급증**
- 캐시가 차더라도 TTL이 들쑥날쑥해 **warmup 효과가 반감**

결국 "캐시가 있음에도 초반 응답이 느린" 아이러니가 발생했다.

---

### 🔍 원인 파악

- 캐시 미스 시점에만 DB/API를 타도록 설계되어 있었다.
- TTL 관리가 단순해서 모든 데이터가 같은 시점에 만료되고, 특정 시점에 **집중 미스**가 발생했다.
- WarmUp 로직은 있었지만 옵션 TTL, 빠른 만료(`fastExpire`) 정책 등이 반영되지 않아 **균형 잡힌 캐시 적재**가 이뤄지지 않았다.

---

### ✅ 해결

WarmUp 로직을 개선해 **데이터를 미리 Redis에 적재**하고, TTL을 더 세분화했다.

```java
@Override
public void warmUp(RedisCacheDataVO redisCacheDataVO) {
    if (!redisCacheDataVO.isUseCache()) {
        return;
    }

    String redisKey = redisCacheDataVO.getRedisKey();
    String type = redisCacheDataVO.getType();
    Map<String, Object> setMap = buildCachePayload(redisCacheDataVO);

    CompletableFuture.runAsync(() ->
        redisTemplate.exchange(getRedisApiUrl() + RedisInfo.RedisEndpoint.SET_WARMUP.path(type),
            HttpMethod.POST, new HttpEntity<>(setMap),
            new ParameterizedTypeReference<Map<String, Object>>() {})
    ).exceptionally(e -> {
        recordFailure("warmUp", redisKey, e);
        return null;
    });
}

private Map<String, Object> buildCachePayload(RedisCacheDataVO vo) {
    Map<String, Object> copyMap = deepCopy(vo.getData());
    int expireTTL = vo.getExpireTTL();

    // expireTTL의 1/10로 optionTTL 설정, 최대 5분
    int optionTTL = Math.min(expireTTL / 10, 300);
    copyMap.put("optionTTL", optionTTL);

    return copyMap;
}
```

개선 포인트:

- `CompletableFuture.runAsync`로 WarmUp을 비동기 실행 → 응답 경로 방해 최소화
- TTL을 **expireTTL / 10**으로 나눈 `optionTTL`을 추가하되, 최대 5분으로 제한
- 빠른 만료 플래그(`fastExpire`)와 연계해 일부 데이터는 더 짧게 캐싱

---

### 🎉 효과 / 깨달음

- 초반 요청 지연이 크게 줄어들었다 (DB 직접 호출 감소).
- 모든 데이터가 동시에 만료되지 않아 **만료 밀도가 완화**됐다.
- WarmUp이 실제로 운영에 의미 있게 동작하기 시작했다.
- TTL은 단순 숫자가 아니라, **데이터 특성에 따라 다층적으로 관리**해야 한다는 걸 체감했다.
