---
title: "git-receive-pack not permitted on  깃 허브 로그인 관련 문제"
pubDate: 2021-08-16
description: "개인적인 알고리즘 연습관련으로 커밋푸쉬를 하고 있는 레파지터리에서 며칠전까지만 해도 잘되던 푸쉬가 갑자기 안되는 이슈가 발생했다. 대략 이와 같은 경고가 뜨면서 발생하는 것이고 이는 깃허브측에서 아이디/비밀번호 인증방식을 더이상 지원하지 않으면서 발생하는 이슈라고 한다"
tags: ["ssafy 6기"]
series: ""
heroImage: ""
draft: false
---

<!-- TODO: migrate images -->

개인적인 알고리즘 연습관련으로 커밋푸쉬를 하고 있는 레파지터리에서 며칠전까지만 해도 잘되던 푸쉬가 갑자기 안되는 이슈가 발생했다. 

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhqV73SXLJ_62xSzyB3txowdKbkocRWBU-R5LUjazj-o_IhyphenhyphenNJxzuLH5jBIEy7v36n0rIaWyeeN-Qw3-vWhUBcbNG6tWovNAD2ecFJEZdMF2vzJELhX9JvUkCkYzO4q2KaFZHZ4yX2N1MU/w354-h323/image.png)[](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhqV73SXLJ_62xSzyB3txowdKbkocRWBU-R5LUjazj-o_IhyphenhyphenNJxzuLH5jBIEy7v36n0rIaWyeeN-Qw3-vWhUBcbNG6tWovNAD2ecFJEZdMF2vzJELhX9JvUkCkYzO4q2KaFZHZ4yX2N1MU/)  
  

  

  

  

  

  

  

  

  

대략 이와 같은 경고가 뜨면서 발생하는 것이고 이는 깃허브측에서 아이디/비밀번호 인증방식을 더이상 지원하지 않으면서 발생하는 이슈라고 한다. 

  

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjuugPU_OfjHUZXK6rCG3BegeXZR4WS7QkCMxfscfEznFk2yEq7fJnw51gyyW_FlkJQdUtfEB4idyDxf105uRJaBK8znbEIbNHwNgHqhvw4vpMpbSxbITwhyizvO-iedyL1m7P_rR7Qk-A/w557-h118/image.png)[](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjuugPU_OfjHUZXK6rCG3BegeXZR4WS7QkCMxfscfEznFk2yEq7fJnw51gyyW_FlkJQdUtfEB4idyDxf105uRJaBK8znbEIbNHwNgHqhvw4vpMpbSxbITwhyizvO-iedyL1m7P_rR7Qk-A/)  

이제 토큰 인증방식을 사용해야 한다고 하니 이에 대해 간략히 정리해 보려고 한다. 

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEimOpVSsBmy9FjoLCltdSfUKxaTUPLzMw7WnnLzQuRwiEUdNw_5cCacjuMZ0wzSsUhm667p1NEmCaqOEuHSLSyhRRMzjfNUeCfeQhNxkjPXkzo2ih3DFdJhyKSUH3mmPlzqoZwZqCLatBI/w225-h458/image.png)[](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEimOpVSsBmy9FjoLCltdSfUKxaTUPLzMw7WnnLzQuRwiEUdNw_5cCacjuMZ0wzSsUhm667p1NEmCaqOEuHSLSyhRRMzjfNUeCfeQhNxkjPXkzo2ih3DFdJhyKSUH3mmPlzqoZwZqCLatBI/)  
토큰 생성을 위해 깃허브에 로그인 후 settings 를 클릭 해준다.  

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjFkiiYN81nn0OywPaWGnBzuNM8dR4CAiYN-TIMEd7YPujVlhghWdY7moNVLk9CJ4J0orT1fLdwObCBRA-fPLmVw6ZluJ-2Bblh9I4YWjGrSTp8xGZJsUhLsYBc5kfSc_LES85y7uztXXg/w401-h312/image.png)[](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjFkiiYN81nn0OywPaWGnBzuNM8dR4CAiYN-TIMEd7YPujVlhghWdY7moNVLk9CJ4J0orT1fLdwObCBRA-fPLmVw6ZluJ-2Bblh9I4YWjGrSTp8xGZJsUhLsYBc5kfSc_LES85y7uztXXg/)

  
Developer settings 를 클릭하고 나서 Personal access tokens 에 들어와주면 새 토큰을 생성할 수 있는 화면이 나온다. 

  

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhEQ8Anpq1RBSAqunucRcVJBnYndDY2t0kH4gzqVvXcY9K5nHK-RuKPyOBuT6qC_t6l8h2ovm_hMas2WPr_hKl8yLpABTu4Z313SkDr4ukI52gZhddFb5k_PMRqpwiq37rD5W3bBIJuwoo/w402-h154/image.png)[](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhEQ8Anpq1RBSAqunucRcVJBnYndDY2t0kH4gzqVvXcY9K5nHK-RuKPyOBuT6qC_t6l8h2ovm_hMas2WPr_hKl8yLpABTu4Z313SkDr4ukI52gZhddFb5k_PMRqpwiq37rD5W3bBIJuwoo/)

  

보안을 위해 한번 더 비밀번호를 입력 해준 다음   

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhkzygYxHey0UAT-VhgPEXk6BMpItpgVQgcT6vTtwVF49HRAKItGgK-rWSZ7XZMkiMXxF92h8ajq8b8QK5JtxsOIzNrU8EZHK3kY3IO1SZO5NqSZtQHa1Xagk8df-3NF711S6G8PJBqQ_E/w403-h396/image.png)[](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhkzygYxHey0UAT-VhgPEXk6BMpItpgVQgcT6vTtwVF49HRAKItGgK-rWSZ7XZMkiMXxF92h8ajq8b8QK5JtxsOIzNrU8EZHK3kY3IO1SZO5NqSZtQHa1Xagk8df-3NF711S6G8PJBqQ_E/)

  

토큰에 대한 설정 창에서 note에는 이름 아래 만료일에는 날짜를 지정해 줄 수 있다. 

no expiration 도 설정할 수 있으나 만료날짜를 지정해주길 강력히 권고해서 오늘로부터 1년으로 지정해주었다.

  

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgFHPgm0sLL2TpSsJ5rkzaLFE_mJELlqOXgOh80kk823kys72kzwAUeNZcFd0VW3g_8Wca3_TMOiYR_FoVNs2rOUKI2_P66_qziGLJ_zSs8bqBPwzy1WBqIwgUXPej0D4LzukWkABS4oWw/w404-h150/image.png)[](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgFHPgm0sLL2TpSsJ5rkzaLFE_mJELlqOXgOh80kk823kys72kzwAUeNZcFd0VW3g_8Wca3_TMOiYR_FoVNs2rOUKI2_P66_qziGLJ_zSs8bqBPwzy1WBqIwgUXPej0D4LzukWkABS4oWw/)  

각종 권한들을 지정해줄 수 있는데, 뭐가 뭔지는 잘 모르겠고, 그냥 커밋 풀/푸쉬만 해줄 거면 repo에 대한것만 지정해주면 된다고 한다.  

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh7WngWVR9jVfS1QU7wBAccg7iuWCxIfgotWvo8_YRFhatU-2zX9drDhyP2omNTzvB0x-AfiRIKiz646-N30RybmbQI0WQwXzEx4JwXvFmc9EWyPDloOm-pzm9RLs6xBwkSyhoTJHEam8Y/w405-h537/image.png)[](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh7WngWVR9jVfS1QU7wBAccg7iuWCxIfgotWvo8_YRFhatU-2zX9drDhyP2omNTzvB0x-AfiRIKiz646-N30RybmbQI0WQwXzEx4JwXvFmc9EWyPDloOm-pzm9RLs6xBwkSyhoTJHEam8Y/)

  

마지막 이 화면에서 끄지 않고 바로 키값을 복사해두어야 한다. 이후에는 다시 보여 주지 않고 해당 토큰이 가진 설정과 삭제 선택버튼 정도만 보여주니까 해당 키값을 일단 복사해둔다.

  

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjcRToiFoWUJQSB_jd58S92JMVpaug0gb90jtypguKqsCpUZ3DDBGl2B8sNUP8ctAq2fRmNUYBGvk_BQq0fttiXCC6HMA2tXRSD9xWuy249y5UO17HI3P5YOdW5qaLbNv_1v4e3hVvbCx8/w409-h166/image.png)[](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjcRToiFoWUJQSB_jd58S92JMVpaug0gb90jtypguKqsCpUZ3DDBGl2B8sNUP8ctAq2fRmNUYBGvk_BQq0fttiXCC6HMA2tXRSD9xWuy249y5UO17HI3P5YOdW5qaLbNv_1v4e3hVvbCx8/)  

마지막 평소 이클립스와 깃 연동때와 마찬가지로 다시 URI를 복사해서 간 다음 비밀번호 자리에 해당 토큰을 붙여 넣으면 완성 된다. 되던 깃허브 연동이 안되는 경우라 조금 헤맬 수 있지만, 인터넷에 이미 설명이 많아서 그대로 따라가면 되는 이슈 였다.   
  

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEha3o2A32H3MtkKCqnoQhJl4FinB_S0yyKgExKCq-QHNjEdSM1aKwPgfNCFCmG7k8zPihWBEmsDdPP0V-apCKResq_6z-M_mSVEZq_zsjtZVObF-a4AOLVTe08HE19W2Y2cBh1Yn6uvFV8/w408-h449/image.png)[](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEha3o2A32H3MtkKCqnoQhJl4FinB_S0yyKgExKCq-QHNjEdSM1aKwPgfNCFCmG7k8zPihWBEmsDdPP0V-apCKResq_6z-M_mSVEZq_zsjtZVObF-a4AOLVTe08HE19W2Y2cBh1Yn6uvFV8/)