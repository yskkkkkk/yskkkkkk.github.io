---
title: "update, delete가 너무 무서운 사람"
pubDate: 2021-03-03
description: "언뜻 듣기로 update문은 delete을 사용하는것보다 더 위험하기 때문에 사용을 지양해야 한다는 이야기를 본적이 있다. 근데 만들어 놓은 기능을 어떻게 안쓰고만 있겠나. 이걸 이리 저리 사용하는데 좀 새로이 알게된 정보들이 존재한다. 워크벤치에서 다수의 데이터가 나"
tags: ["코딩이야기"]
series: ""
heroImage: ""
draft: false
---

<!-- TODO: migrate images -->

언뜻 듣기로 update문은 delete을 사용하는것보다 더 위험하기 때문에 사용을 지양해야 한다는 이야기를 본적이 있다. 근데 만들어 놓은 기능을 어떻게 안쓰고만 있겠나. 이걸 이리 저리 사용하는데 좀 새로이 알게된 정보들이 존재한다.
  

워크벤치에서 다수의 데이터가 나오게끔 update나 delete를 하면(unique값이 아닌 키값으로) safe_mode에 걸려서 에러가 뜬다. 그래서 이걸 각각 유니크 값으로 기능하게 하고 이걸 한 api 안에서 리스트로 돌려서 하는 식이 있다고 하는데, 사실 이렇게 사용안해도 자바에서는 그냥 되는경우가 있더라. 이번에 그룹원 수정_삭제 쪽을 이렇게 구현했는데, 만들고 나서 까먹고 있다가 이걸 프로시저를 사용해야 하나... 어째야하나 고민을 했는데 그냥 아무일도 없이 되고 있더라.

  

업데이트문 안에서 해당 테이블의 데이터를 다시 이용해서 키값을 넣을때가 있다. 이번에 날짜와 금액을 변경하는 update문을 짰었는데, 대충 아래와 같은 모양이었다.  
  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjBVFcknecLY0eCljqD6kCRVm5qDKpK7UTLJgp2kyJrqLNSpIL3u5CNDUx_lbNPKLxF63kgfaKFrNR3ZKmBsOJ9RmLguMSwm1FeEDoo4KKvMoYLtqQLhVCfGOKuNKmNcvWUlauaesD59P4/w546-h99/adada.PNG)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjBVFcknecLY0eCljqD6kCRVm5qDKpK7UTLJgp2kyJrqLNSpIL3u5CNDUx_lbNPKLxF63kgfaKFrNR3ZKmBsOJ9RmLguMSwm1FeEDoo4KKvMoYLtqQLhVCfGOKuNKmNcvWUlauaesD59P4/s498/adada.PNG)

  

이 때 내가 노린것은 아래의 date는 기존 tb_test 테이블의 date 값이었는데 위에서 바뀐다음에 date가 들어간 것이었다. 전체문장이 한번에 바뀌는게 아니라 위에서부터 순차대로 바뀌는 그런 순서를 가진듯 하여 3번 문장과 4번 문장의 순서를 바꿔주자 내가 의도한대로 작동하는걸 확인할 수 있었다.

  

지금 정산관리 쪽을 살펴보며 평소에 오류가 나면 직접 db데이터를 바꿔서 해결했던 아주 나쁜 문제들을 보고 고쳐나가고 앞으로의 해결책을 만들어야 하는데 이과정에서 update를 자주 쓰게 될것 같다. (지금 추가로 만들어 달라는 기능중에 관리자 페이지에서 데이터를 변경하게 해달라는 기능이 많다....)