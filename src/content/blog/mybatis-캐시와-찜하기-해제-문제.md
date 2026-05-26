---
title: "MyBatis 캐시와 찜하기 해제 문제"
pubDate: 2026-05-26
description: "찜하기 해제 후 상품 조회 API에서 wishYn이 약 1분간 1로 반환되는 현상을 MyBatis 캐시 구조와 함께 분석하고 해결한 과정을 기록합니다."
tags: ["mybatis", "cache", "java", "backend", "troubleshooting"]
heroImage: ""
---

점심 먹고 오후에 화면 개발자 분께서 문의를 주셨다.

> "찜하기 해제 후 상품상세 정보 API를 호출하면 `wishYn`이 `1`로 전달되고 있습니다.  
> 해당 현상 확인 부탁드려도 될까요?"

## 1. 상세 현상 재현

직접 테스트해보니 정확한 조건이 있었다.

1. **셋탑박스로 특정 상품 찜하기**
2. **상품 조회 API를 이용해서 조회**  
   - 이때 `wishYn = 1`로 반환됨.
3. **상품 찜하기 해제**
4. **다시 상품 조회 API 호출**  
   - 약 1분 정도 `wishYn = 1`로 반환되다가 이후 `0`으로 정상 반환됨.

특이한 점은 **2번 과정이 없을 경우, 찜하기 해제 직후에도 `wishYn = 0`으로 정상 반환**된다는 것이었다.  
즉, 찜 여부를 반영하는 데이터가 **캐싱된 것**이 문제라고 판단했다.

비슷한 사례가 있었기에 쉽게 해결할 수 있을 줄 알았다.

---

## 2. 우리 프로젝트의 DB 연결 구조

현재 프로젝트에서는 **4개의 DB 연결 세션**을 사용한다.

1. **PRD DB** (데이터 CUD 가능)
2. **PRD CACHE** (캐시용 DB)
3. **CDC DB** (데이터 READ 전용)
4. **CDC CACHE** (CDC의 캐시용 DB)

그리고 `cache~.xml`에는 다음과 같은 **MyBatis 캐시 설정**이 적용되어 있다.

```xml
<cache eviction="LRU" flushInterval="60000" size="1024" readOnly="true"/>
```

- `flushInterval="60000"` → 60초 동안 캐시 유지
- `eviction="LRU"` → Least Recently Used 방식으로 오래된 데이터부터 삭제
- `size="1024"` → 캐시 크기 제한

즉, 한 번 조회된 데이터는 60초 동안 캐싱되어 같은 요청이 들어오면 기존 데이터를 반환하는 구조다.

---

## 3. 상품 조회 API 코드 분석

```java
List<VodGoodsVO> vodGoodsList = cdcCacheDAO.vodGoods(param);

List<String> goodsCodeList = new ArrayList<>();
for (VodGoodsVO vodGoods : vodGoodsList) {
    goodsCodeList.add(vodGoods.getGoodsCode());
}

List<WishLikeVO> wishList = DAO.wishList(subParam);

// VOD 상품의 찜 여부 설정
for (VodGoodsVO vodGoods : vodGoodsList) {
    for (WishLikeVO wishItem : wishList) {
        if (wishItem.getGoodsCode().equals(vodGoods.getGoodsCode())) {
            vodGoods.setWishYn("1");
            break;
        }
    }
}
```

처음에 봤을 때 **왜 vodGoods에서 한 번에 wishYn을 조회하지 않을까?** 라는 의문이 들었다.  
그러나 코드의 히스토리를 추적하기 어려운 상황이라 찜 여부 조회 부분을 기존 쿼리에 합쳐서 실행해 보았다.

결과는? 똑같았다.  
같은 조건으로 요청하면 이전 쿼리 결과가 그대로 캐싱되었기 때문에 캐시 문제 해결에는 도움이 되지 않았다.

---

## 4. 해결 방법 시도

### 1차 시도: flushCache="true" 추가

MyBatis 매퍼 XML에 `flushCache="true"` 옵션을 추가하여 캐시를 무효화하는 방법을 사용했다.

```xml
<select id="vodGoods" resultMap="vodGoodsResultMap" flushCache="true">
```

- 데이터는 바로 반영됨! ✅
- 하지만 API 호출량이 하루 150만 건 이상이라 캐시를 무효화하면 DB 부하가 심각해짐. ❌
- 결국 이 방법은 포기.

### 2차 시도: resultMap에서 wishYn 제거

MyBatis에서 resultMap 단위로 캐싱된다는 점을 참고하여 resultMap에서 `wishYn`을 제거했다.

- 여전히 `wishYn`이 정상적으로 반환됨. 🤔
- 즉, 이 방법도 캐시 문제 해결에 도움되지 않음. ❌

### 최종 해결 방법

결국 찜 여부를 설정하는 로직을 변경하는 방법을 선택했다.

```java
// VOD 상품의 찜 여부 설정
for (VodGoodsVO vodGoods : vodGoodsList) {
    vodGoods.setWishYn("0"); // 기본값 설정
    for (WishLikeVO wishItem : wishList) {
        if (wishItem.getGoodsCode().equals(vodGoods.getGoodsCode())) {
            vodGoods.setWishYn("1");
            break;
        }
    }
}
```

- 캐시된 데이터가 `wishYn = 1` 상태라면 기본값을 `0`으로 초기화한 후 다시 세팅하는 방식.
- 캐시를 유지하면서도 찜하기 해제 후 데이터를 정상적으로 보정할 수 있음. ✅

---

## 5. 결론

이번 문제는 단순히 캐시를 끄는 것이 아니라, 캐싱을 유지하면서도 즉시 반영할 방법이 필요했다.

결국 `wishYn`을 강제로 `0`으로 초기화 후 다시 세팅하는 방식으로 해결했지만,  
이게 정말 완전한 해결인지에 대해서는 아직도 살펴보고 있다.

아마 나중에 **"찜하기 캐시 문제 - 2편"** 으로 돌아오지 않을까 싶다.
