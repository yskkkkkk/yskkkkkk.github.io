---
title: "멀티 인스턴스 환경에서 Caffeine + Redis 캐시 동기화하기 (Pub/Sub)"
pubDate: 2025-09-08
description: "로컬 Caffeine 캐시와 Redis 캐시를 병합 운영하던 중 발생한 인스턴스 간 캐시 불일치를 Redis Pub/Sub 무효화 이벤트로 해결한 과정을 기록합니다."
series: "Redis 프로젝트 회고"
tags: ["redis", "caffeine", "pubsub", "cache", "java", "backend"]
heroImage: ""
---

### 🤦 문제 발생

서비스 구조상 **로컬 Caffeine 캐시 + Redis 캐시**를 병합해서 사용했는데, 데이터 정합성 문제가 자꾸 발생했다.

- 로컬 캐시에만 남아 있는 값이 Redis와 달라 오래된 데이터가 제공됨
- Redis에 업데이트가 발생해도 로컬 캐시 반영이 늦어 사용자마다 결과 불일치
- 서버 인스턴스가 3대라서, 한 곳에서 무효화해도 나머지 노드가 알지 못하는 상황 발생

**멀티 인스턴스 환경에서 캐시 불일치**가 터진 것이다.

---

### 🔍 원인 파악

- Caffeine은 로컬 JVM 내에서만 동작 → 다른 서버와 캐시 동기화 불가
- Redis는 중앙 집중 캐시라서 값이 최신이지만, 로컬 Caffeine은 그대로 남아 있음
- 캐시 정합성 보장을 위해서는 **Pub/Sub 기반 무효화**가 필요했다

---

### ✅ 해결

Redis Pub/Sub을 이용해 **캐시 무효화 이벤트**를 모든 서버에 전파했다.

```java
@PostConstruct
private void initPubSub() {
    clusterPubSubConnection.addListener(new RedisPubSubListener<String, String>() {
        @Override
        public void message(String channel, String message) {
            log.info("[PubSub 구독] 채널={}, 메세지={}", channel, abbrev(message, 70));
            try {
                if (redisInfo.CACHE_INVALIDATION_CHANNEL.equals(channel)) {
                    onInvalidate(message);
                } else if (redisInfo.CACHE_PUT_GOODS_CHANNEL.equals(channel)) {
                    onPutGoods(message);
                }
            } catch (Exception e) {
                log.warn("[PubSub] 핸들 실패: ch={}, head={}", channel, abbrev(message, 200), e);
            }
        }

        @Override
        public void subscribed(String channel, long count) {
            log.info("[PubSub][subscribed] 채널={} (구독 수={})", channel, count);
        }
    });

    pubSubAsync.subscribe(redisInfo.CACHE_INVALIDATION_CHANNEL, redisInfo.CACHE_PUT_GOODS_CHANNEL)
               .toCompletableFuture().join();
}

private void onInvalidate(String key) {
    List<String> keys = Arrays.stream(key.split(","))
            .map(String::trim)
            .filter(s -> !s.isEmpty())
            .toList();
    if (keys.isEmpty()) return;

    asyncStringCaff.synchronous().invalidateAll(keys);
    asyncDynamicStringCaff.synchronous().invalidateAll(keys);
    asyncDynamicStringGoodsCaff.synchronous().invalidateAll(keys);

    keys.forEach(ettlMeta::remove);
    keys.forEach(ttlMap::remove);

    log.info("[PubSub][INVALIDATE] 캐시 갱신 {} keys", keys);
}
```

- `CACHE_INVALIDATION_CHANNEL` → 무효화 이벤트 전파
- `CACHE_PUT_GOODS_CHANNEL` → 상품상세 캐시 갱신 이벤트 전파
- 모든 서버에서 구독해 동시에 캐시를 삭제/갱신 → 데이터 정합성 확보

---

### 🎉 효과 / 깨달음

- 로컬 캐시(Caffeine)와 Redis 캐시의 데이터 정합성을 유지할 수 있게 됐다.
- 서버 인스턴스 3대 모두에서 **동시에 캐시 무효화**가 반영된다.
- "로컬 캐시만 보고 Redis 최신값을 놓치는 문제"가 해결됐다.
- 캐시 계층(L1-L2)을 혼용할 때는 **반드시 Pub/Sub 같은 동기화 장치**가 필요하다.
