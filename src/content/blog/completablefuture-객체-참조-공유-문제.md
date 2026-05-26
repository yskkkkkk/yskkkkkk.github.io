---
title: "CompletableFuture에서 객체 참조 공유로 인한 데이터 오염 해결하기"
pubDate: 2025-09-07
description: "여러 Future에서 같은 객체 인스턴스를 공유하다 발생한 데이터 정합성 문제를 깊은 복사(Deep Copy)로 해결한 과정을 기록합니다."
series: "Redis 프로젝트 회고"
tags: ["java", "concurrency", "completablefuture", "deep-copy", "backend"]
heroImage: ""
---

### 🤦 문제 발생

`CompletableFuture`를 이용해 비동기 캐싱 로직을 짜던 중, 같은 객체 인스턴스를 여러 Future에서 공유하다 예상치 못한 문제가 터졌다.

- 어떤 Future에서 데이터를 수정하면, 이미 캐시에 올라간 객체까지 같이 변경됨 → 원치 않는 데이터 오염 발생
- 특정 시점에 전달된 객체의 값과, 나중에 캐싱된 값이 달라지는 **정합성 깨짐** 현상 발생

참조형 객체를 그대로 캐싱하거나 넘겨주는 건 위험했다.

---

### 🔍 원인 파악

Java의 참조 타입 특성상, 같은 객체를 여러 Future에서 공유하면 메모리 주소가 같으므로 **하나의 객체를 수정할 때 모든 참조자가 영향을 받는다.**

- `CompletableFuture` 체인에서 같은 객체를 돌려 쓰는 구조
- 불변 객체(Immutable)가 아닌 VO/DTO 구조
- 깊은 복사(Deep Copy)가 구현되지 않아 참조 공유 문제 발생

---

### ✅ 해결

객체를 넘기기 전 **깊은 복사 메서드**를 만들어 새로운 인스턴스를 반환하도록 수정했다.

```java
public class GoodsVO implements Serializable {
    private String goodsId;
    private String goodsName;
    private int price;

    // ... getter / setter ...

    public GoodsVO deepCopy() {
        GoodsVO copy = new GoodsVO();
        copy.setGoodsId(this.goodsId);
        copy.setGoodsName(this.goodsName);
        copy.setPrice(this.price);
        return copy;
    }
}
```

사용 예시:

```java
CompletableFuture.supplyAsync(() -> {
    GoodsVO origin = goodsService.getGoods(goodsId);
    return origin.deepCopy(); // 안전하게 복제 후 캐싱
});
```

---

### 🎉 효과 / 깨달음

- 객체 복제를 통해 **데이터 오염 방지**
- Future 체인과 캐시 간 **정합성 확보**
- 불변 객체 패턴(Immutable Object)을 적극 고려해야겠다는 교훈
