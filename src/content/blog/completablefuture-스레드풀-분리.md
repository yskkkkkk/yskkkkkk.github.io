---
title: "CompletableFuture 스레드풀 분리로 pool starvation 해결하기"
pubDate: 2025-09-02
description: "ForkJoinPool.commonPool에 블로킹 I/O를 태워 발생한 스레드풀 고갈 현상을 CPU/IO 실행기 분리로 해결한 과정을 기록합니다."
series: "Redis 프로젝트 회고"
tags: ["java", "concurrency", "completablefuture", "spring", "backend", "performance"]
heroImage: ""
---

### 🤦 문제 발생

외부 API 호출, DB 조회, Redis I/O 같은 블로킹 작업을 `CompletableFuture.supplyAsync(...)`로 병렬화했는데, 실행기를 지정하지 않아 `ForkJoinPool.commonPool`을 사용하고 있었다. 당장 장애로 이어진 건 아니었지만, 코드를 점검하는 과정에서 트래픽이 몰리면 문제가 될 수 있는 구조라는 걸 확인했다.

- 블로킹 I/O가 몰리면 p95 응답 시간 급상승 가능
- 내부에서 `join()`/`get()`을 중첩 호출할 경우 응답 멈춤 위험
- 워커 스레드들이 I/O 대기로 묶여 풀 고갈(pool starvation) 우려

대기 중인 태스크들이 스케줄링되지 못하면 서비스 전체가 느려질 수 있는 상황이라, 실제 문제로 번지기 전에 구조를 손보기로 했다.

---

### 🔍 원인 파악

- `ForkJoinPool.commonPool`은 **CPU 바운드 작업**에 맞는 풀로, 기본 병렬도는 코어 수 근처다. 블로킹 I/O에는 적합하지 않다.
- 블로킹이 늘어나면서 워커 스레드가 묶이고, 나머지 태스크는 스케줄링 기회를 잃었다.
- 체인 중간의 `join()`/`get()` 같은 동기화가 스타베이션을 심화시켰다.
- Spring `@Async`도 실행기를 지정하지 않으면 기본 풀에 태워져 같은 문제가 발생한다.

---

### ✅ 해결

CPU와 I/O 실행기를 분리하고, 블로킹 호출은 전용 풀에 태웠다.

#### 1) 실행기 분리

```java
@Bean(name = "cpuExecutor")
public ThreadPoolTaskExecutor cpuExecutor() {
    int cores = Runtime.getRuntime().availableProcessors();
    ThreadPoolTaskExecutor ex = new ThreadPoolTaskExecutor();
    ex.setCorePoolSize(cores);
    ex.setMaxPoolSize(cores);
    ex.setQueueCapacity(0);
    ex.setThreadNamePrefix("cpu-");
    ex.initialize();
    return ex;
}

@Bean(name = "ioExecutor")
public ThreadPoolTaskExecutor ioExecutor() {
    ThreadPoolTaskExecutor ex = new ThreadPoolTaskExecutor();
    ex.setCorePoolSize(16);
    ex.setMaxPoolSize(64);
    ex.setQueueCapacity(1000);
    ex.setKeepAliveSeconds(60);
    ex.setAllowCoreThreadTimeOut(true);
    ex.setThreadNamePrefix("io-");
    ex.initialize();
    return ex;
}
```

#### 2) 블로킹 호출 전용 풀 사용

```java
CompletableFuture<Result> future =
    CompletableFuture.supplyAsync(() -> blockingHttpCall(), ioExecutor);
```

#### 3) 중첩 동기화 제거

`join()`/`get()` 대신 `thenCompose`, `thenApply` 등 비동기 체인을 끝까지 유지한다.

#### 4) 운영 가시성 확보

Micrometer로 스레드풀 메트릭(`active`, `queue size`, `rejections`)을 대시보드에 노출한다.

---

### 🎉 효과 / 깨달음

- CPU와 I/O 분리만으로 공용 풀 스타베이션 위험이 사라졌다.
- 적용 이후 트래픽 스파이크 상황에서도 안정적으로 처리됐다.
- 도메인 한도 기반 동시성 제어로 외부 시스템 과부하도 방지할 수 있다.
- 문제가 터진 뒤 고치는 것보다, 구조적 위험을 미리 걷어내는 쪽이 훨씬 싸게 먹힌다.

`commonPool`은 공짜 점심이 아니다. 블로킹 I/O가 있다면 반드시 전용 실행기를 분리해야 한다.
