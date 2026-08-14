---
title: "RestTemplate 한글 깨짐과 Custom ObjectMapper 미적용 해결하기"
pubDate: 2025-08-27
description: "기본 RestTemplate의 ISO-8859-1 인코딩과 커스텀 ObjectMapper 미반영 문제를 직접 Primary Bean으로 등록해 해결한 과정을 기록합니다."
series: "Redis 프로젝트 회고"
tags: ["spring", "resttemplate", "java", "backend", "utf-8"]
heroImage: ""
---

### 문제 발생

Redis API와 통신하는 RestTemplate을 쓰는데,

- 한글이 깨지고
- JSON 직렬화 시 커스텀한 ObjectMapper 설정이 적용되지 않는 문제가 터졌다.

처음에는 Redis 응답 문제인 줄 알았는데, 로그를 보니 **RestTemplate 자체 설정 문제**였다.

---

### 원인 파악

- 기본 RestTemplate의 `StringHttpMessageConverter`는 **ISO-8859-1**을 사용한다. (한글 깨짐 원인)
- 직접 등록한 Custom ObjectMapper는 기본 RestTemplate에 전혀 반영되지 않는다.

Spring이 제공하는 **기본 RestTemplate은 내 설정대로 동작하지 않는다**는 걸 깨달았다.

---

### 해결

Bean을 직접 만들어 **UTF-8 + Custom ObjectMapper**를 적용했다.

```java
/** @Primary: 기본 RestTemplate */
@Primary
@Bean
public RestTemplate restTemplate(@Qualifier("customObjectMapper") ObjectMapper customObjectMapper) {
    RestTemplate rt = new RestTemplate();

    MappingJackson2HttpMessageConverter jackson = new MappingJackson2HttpMessageConverter();
    jackson.setObjectMapper(customObjectMapper);

    FormHttpMessageConverter form = new FormHttpMessageConverter();
    form.setCharset(StandardCharsets.UTF_8);

    rt.setMessageConverters(Arrays.asList(
            new StringHttpMessageConverter(StandardCharsets.UTF_8),
            form,
            jackson
    ));
    return rt;
}
```

---

### 효과

- 모든 API 호출에서 **한글 깨짐 사라짐**
- JSON 변환 시 **Custom ObjectMapper 설정 반영됨**
- Form 전송도 UTF-8로 문제없이 처리

삽질 끝에 결론: RestTemplate은 **직접 Primary Bean으로 등록**해야 한다.
