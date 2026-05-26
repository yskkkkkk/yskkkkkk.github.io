---
title: "Redis 키 네이밍 파편화 해결기"
pubDate: 2025-09-01
description: "여기저기서 다른 규칙으로 만들어지던 Redis 키를 단일 진입점으로 강제해 정규화한 과정을 기록합니다."
series: "Redis 프로젝트 회고"
tags: ["redis", "cache", "java", "backend", "refactoring"]
heroImage: ""
---

### 🤦 문제 발생

Redis 키가 여기저기서 **다른 규칙**으로 만들어지고 있었다.

- 어떤 곳은 `mdulInfo_home_main_01` 처럼 **언더스코어** 기반
- 어떤 곳은 `home:main:01` 처럼 **콜론** 기반
- 어떤 곳은 빠른 만료 정책을 표기하려고 뒤에 **`Y`만 덜렁** 붙이기도 — `home:main:01Y`

결과적으로 **캐시 미스**, **중복 저장**, **운영 중 수작업 스캔 난이도**가 상승했다.  
로그 상으로는 "있어야 하는 키가 없거나(미스)" / "같은 데이터가 여러 키로 저장됨(중복)"이 반복됐다.

---

### 🔍 원인 파악

- 과거 코드에서 내려온 `mdulInfo_` 접두사와 언더스코어(`_`) 구분 규칙이 **새 코드로 넘어오며 일관성 없이** 쓰였다.
- 일부 모듈은 `fastExpire` 같은 정책 플래그를 **키 포맷 합의 없이 임의로** 붙여서 파편화를 초래했다.
- 운영/분석 시 Scan 패턴(`SCAN`, `KEYS`)도 제각각이라 **추적 난이도가 높았다**.

핵심은 **규칙(정규화) 부재**였다.

---

### ✅ 해결

키 생성 시 **단일 진입점**을 강제하고, 다음 원칙을 합의했다.

1. **접두사 제거 + 구분자는 콜론(`:`)**
2. **정책 플래그는 별도 세그먼트로 명시** (예: `:Y`)
3. 호출부는 반드시 유틸 메서드만 사용

```java
// 1) mdulInfo_ 접두사 제거 + '_' → ':' 통일
public static String getRedisModuleKey(String moduleKey) {
    return moduleKey.replace("mdulInfo_", "").replace('_', ':');
}
```

```java
// 2) fastExpire 정책 반영: 플래그는 별도 세그먼트로 명시
List<String> redisKeyList = moduleList.stream()
    .map(module -> {
        String moduleKey = RedisUtils.toMduleCode(module); // 내부 도메인 로직 → 최종 키 단위 문자열
        String fastExpire = String.valueOf(module.get(RedisInfo.FAST_EXPIRE));
        String baseKey = RedisUtils.getRedisModuleKey(moduleKey); // 규칙 진입점
        return "Y".equals(fastExpire) ? baseKey + ":Y" : baseKey;
    })
    .collect(Collectors.toList());
```

> **중요 합의**
>
> - 키의 **형태는 `shop:module:group[:flag]`** 로 고정
> - 빠른 만료는 `:Y` 세그먼트로만 표현 (임의 접미 금지)
> - 생성은 **반드시** `getRedisModuleKey(...)`를 통해 수행

---

### 🧪 예/반례로 검증

- 입력: `mdulInfo_home_main_01` → 출력: `home:main:01`
- 입력: `mdulInfo_home_main_01` + fastExpire=Y → `home:main:01:Y`
- ❌ 잘못된 예: `home:main:01Y`, `mdulInfo_home_main_01:Y` (접두사 잔존, 구분자 혼용)

간단한 단위 테스트 스케치:

```java
@Test
void normalizeKey_basic() {
    assertEquals("home:main:01", getRedisModuleKey("mdulInfo_home_main_01"));
}

@Test
void normalizeKey_withFlag() {
    String base = getRedisModuleKey("mdulInfo_home_main_01");
    assertEquals("home:main:01:Y", base + ":Y");
}
```

---

### 🎉 효과 / 깨달음

- **키 충돌·중복 저장 감소**, 운영 스캔/모니터링이 **한결 수월**해졌다.
- 캐시 미스가 줄어들면서 **TTL 정책 실험**(fastExpire vs normal)도 투명해졌다.
- 새/구 코드가 섞여 있어도 **유틸 진입점 강제**만으로 정규화가 유지된다.

결국 캐시의 반은 **네이밍 규칙**이다. 규칙을 코드로 **강제**하지 않으면 반드시 새어 나온다.
