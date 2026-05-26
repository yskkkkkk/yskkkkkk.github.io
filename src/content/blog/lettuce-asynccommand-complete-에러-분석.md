---
title: "Lettuce AsyncCommand.complete() 에러 분석과 mget 체인 단순화"
pubDate: 2025-09-05
description: "RedisFuture를 toCompletableFuture()로 브리지한 mget 비동기 체인에서 간헐적으로 발생한 complete() 예외를 분석하고, 브리지 제거와 명시적 타임아웃 처리로 해결한 과정을 기록합니다."
series: "Redis 프로젝트 회고"
tags: ["redis", "lettuce", "java", "concurrency", "backend", "debugging"]
heroImage: ""
---

### 🤦 문제 발생

몇 달간 잘 돌던 GNB 캐시 경로에서, 특정 날부터 간헐적으로 아래 지점에서 터졌다.

```java
public class AsyncCommand<K, V, T> extends CompletableFuture<T> implements RedisCommand<K, V, T>, RedisFuture<T>, CompleteableCommand<T>, DecoratedCommand<K, V, T> {

    public void complete() {
        if (COUNT_UPDATER.decrementAndGet(this) == 0) {
            this.completeResult();
            this.command.complete();
        }
    }
}
```

디버그를 찍어보면 `return Optional.of(result);` 직전까지는 값이 정상인데, 그 다음 체인 완료 시점에 위 `complete()`에서 예외가 났다. 문제가 재현된 호출부는 아래와 같은 **mget 비동기 체인**이었다.

```java
return asyncStringConn.async()
    .mget(boKey, goodsKey, personalizedContents, boMisKey, boTotMisKey, membGbCacheAllow, redisStockTTL)
    .toCompletableFuture()
    .thenApply(kvs -> {
        if (kvs == null || kvs.isEmpty()) {
            log.error("redisEnable/goodsKey/personalizedContents/misCount/totMisCount/memb ...");
        }
        // ... result 구성
        return Optional.of(result);
    });
```

---

### 🔍 원인 파악

- **이종 Future 브리지**: Lettuce의 `RedisFuture`를 `toCompletableFuture()`로 감싼 뒤, 추가로 `thenApply`/`join` 등이 섞이며 **완료 신호가 두 레이어에서 경합**하는 구간이 있었다.
- **타임아웃과 재시도 간섭**: 간헐적으로 느려지는 시점에 상위 재시도/취소와 클라이언트 내부 완료 시그널이 맞물려 `complete()` 경로에서 중복 완료/취소가 충돌했을 가능성이 있다.
- **파이프라인 묶음 응답**: `mget`에 다수 키를 한 번에 태우는 동안, 일부 키에서 오류가 나면 **부분 실패 전파**가 체인에서 처리되지 않고 터지는 케이스가 관찰됐다.

> 라이브러리 자체 버그라는 의미가 아니라, **우리 체인 구성(브리지 + 재시도/취소 타이밍)** 이 경합을 유발할 소지가 있었다는 점이다.

---

### ✅ 해결

핵심은 두 가지다. **(1) 브리지 제거**로 체인 단순화, **(2) 명시적 타임아웃/예외 처리**를 호출부에서 통일.

#### 1) `RedisFuture` 직접 사용 + IO 풀에서 블로킹 회수

Java 8 환경이라 `orTimeout`/`completeOnTimeout`을 쓰지 않고, **I/O 전용 스레드풀**에서 `get(timeout)`으로 회수한다.

```java
private final ExecutorService ioExecutor = Executors.newFixedThreadPool(16, r -> {
    Thread t = new Thread(r, "io-mget-");
    t.setDaemon(true);
    return t;
});

private static final long TIMEOUT_MS = 1500;

public Optional<Result> loadByMget() {
    return CompletableFuture.supplyAsync(() -> {
        try {
            RedisFuture<List<String>> fut = asyncStringConn.async()
                .mget(boKey, goodsKey, personalizedContents, boMisKey, boTotMisKey, membGbCacheAllow, redisStockTTL);

            List<String> kvs = fut.get(TIMEOUT_MS, TimeUnit.MILLISECONDS);
            if (kvs == null || kvs.isEmpty()) {
                log.warn("mget empty: keys={}", Arrays.asList(boKey, goodsKey, personalizedContents));
                return Optional.<Result>empty();
            }
            Result result = mapToResult(kvs);
            return Optional.of(result);
        } catch (TimeoutException te) {
            log.error("mget timeout {}ms", TIMEOUT_MS);
            futCancelQuietly();
            return Optional.empty();
        } catch (Exception e) {
            log.error("mget failed", e);
            return Optional.empty();
        }
    }, ioExecutor).join();
}
```

- `toCompletableFuture()` 브리지를 제거하고 **하나의 완료 경로**만 유지했다.
- 타임아웃은 **호출부에서 단일 책임**으로 처리해 취소와 로깅을 일관화했다.

#### 2) 부분 실패 방지: 키 배치 정규화

문제 재현 구간에서는 키 배열에 `null`/빈 키가 섞인 경우가 있었다. 사전에 **키 필터링** 후 `mget`을 호출한다.

```java
String[] keys = Stream.of(boKey, goodsKey, personalizedContents, boMisKey, boTotMisKey, membGbCacheAllow, redisStockTTL)
    .filter(k -> k != null && !k.isEmpty())
    .toArray(String[]::new);

RedisFuture<List<String>> fut = asyncStringConn.async().mget(keys);
```

#### 3) 예외 전파 정책 단일화

상위 레이어에서 재시도할지, 빈 응답으로 폴백할지를 **한 곳에서 결정**하도록 `Optional<Result>`로 수렴했다.

---

### 🧪 검증

- 동일 트래픽/동일 키 세트로 재현 테스트를 진행했다.
- `AsyncCommand.complete()` 경로 예외가 **미발생**으로 확인됐다 (운영/스테이징 모두).
- mget 타임아웃/에러 카운트가 지표에 **명시적으로** 찍히기 시작했다. 이전에는 체인 중간에서 누락되는 케이스가 있었다.

---

### 🎉 효과 / 깨달음

- **이종 Future 브리지(`toCompletableFuture`)** 는 편하지만, 경합 구간에서 디버깅 포인트를 늘린다. 한 가지 모델만 쓰는 게 단순하고 안전하다.
- 타임아웃/취소는 호출부에서 **명시적으로** 처리하는 편이 라이브러리 내부 완료·취소 시그널과 충돌하지 않는다.
- 배치 키는 항상 **정규화/필터 후**에 보낸다. 빈/`null` 키가 섞이면 진단이 불필요하게 어려워진다.
- 문제를 재현할 수 있는 **작은 경로(키 세트 + 타임아웃)** 를 확보해 두면, 다음에 비슷한 증상이 왔을 때 빠르게 잡을 수 있다.
