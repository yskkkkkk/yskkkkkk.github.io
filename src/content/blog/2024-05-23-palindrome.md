---
title: "Palindrome 기초"
pubDate: 2024-05-23
description: "Palindrome - 회문거꾸로 뒤집어도 똑같은 (ex: 토마토, 기러기) 문자 찾기 알고리즘검색 해보니 manacher 알고리즘이 나오는데 감을 찾는 중이라 가장 easy 문제로 접근해보았다. 9. Palindrome-numberGiven an integer x, "
tags: [""]
series: ""
heroImage: ""
draft: false
---

<!-- TODO: migrate images -->

Palindrome - 회문

거꾸로 뒤집어도 똑같은 (ex: 토마토, 기러기) 문자 찾기 알고리즘

검색 해보니 manacher 알고리즘이 나오는데 감을 찾는 중이라 가장 easy 문제로 접근해보았다. 

  

[9. Palindrome-number](https://leetcode.com/problems/valid-palindrome/)

Given an integer `x`, return `true`* if *`x`* is a *

*palindrome*

*, and *`false`* otherwise*.

 

Example 1:

```
Input: x = 121
Output: true
Explanation: 121 reads as 121 from left to right and from right to left.

```

Example 2:

```
Input: x = -121
Output: false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.

```

Example 3:

```
Input: x = 10
Output: false
Explanation: Reads 01 from right to left. Therefore it is not a palindrome.

```

 

Constraints:

- `-231 <= x <= 231 - 1`

  

  

제출 답변 

![](https://blogger.googleusercontent.com/img/a/AVvXsEhsBkTkKr9J6kx8eBALQCty5S9Wc0Fvls50_lSd7RVyLfCG0JOresuGBpeq0Xg-jjSNMQRVlFGaFzw9Wz19JSy2vd__ndfEQ6AU6NviCVxqTVoR9OmNr6T-KNgdx2-qC3wHFLo7tbSHgydipKBlxdzDvLEBRr2I6w1H4FOS_oXPvrncf8oAPZn7hJdo3Dc)[](https://blogger.googleusercontent.com/img/a/AVvXsEhsBkTkKr9J6kx8eBALQCty5S9Wc0Fvls50_lSd7RVyLfCG0JOresuGBpeq0Xg-jjSNMQRVlFGaFzw9Wz19JSy2vd__ndfEQ6AU6NviCVxqTVoR9OmNr6T-KNgdx2-qC3wHFLo7tbSHgydipKBlxdzDvLEBRr2I6w1H4FOS_oXPvrncf8oAPZn7hJdo3Dc)  
  

  

  

  

  

  

  

  

  

StringBuffer으로 변환해서 비교하는 방법은 상당히 느린 걸 볼 수 있다.... 

  

예시 문제에서 힌트를 주었는데 일단 음수는 모두 회문이 아니다. 

그리고 뒤집어서 비교하는 도중 하나만 틀려도 false 를 반환하면 된다. 

  

두가지를 고려한 속도가 개선된 답은 아래와 같다. 

  

![](https://blogger.googleusercontent.com/img/a/AVvXsEjam6Y-POrJ8hRB8gMc1RstC-KEbIRJxIW7Y6SJMgCk7l-PLBaxr03K1aebTdFFk8eOFc9ktVoqgSN-cbfvN1YAM9-jjOojMBS9im4oiQu8WJacMwfEDi5aZOPF53qUr7v3A6BY99yGW4AAmHfpsut4Dxn3GMv3KP-d-XKK9CPTpxlQqzLmNnVGQ5ghfV8)[](https://blogger.googleusercontent.com/img/a/AVvXsEjam6Y-POrJ8hRB8gMc1RstC-KEbIRJxIW7Y6SJMgCk7l-PLBaxr03K1aebTdFFk8eOFc9ktVoqgSN-cbfvN1YAM9-jjOojMBS9im4oiQu8WJacMwfEDi5aZOPF53qUr7v3A6BY99yGW4AAmHfpsut4Dxn3GMv3KP-d-XKK9CPTpxlQqzLmNnVGQ5ghfV8)  
  

  

  

  

  

  

  

  

  

  

  

````**``**

```

```

```

```

```

```

- ``
- ``
[125. Valid PalindromeA phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.Given a string s, return true if it is a palindrome, or false otherwise. Example 1:Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.
Example 2:Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.
Example 3:Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.
 Constraints:1 <= s.length <= 2 * 105s consists only of printable ASCII characters.](https://leetcode.com/problems/valid-palindrome/)

  
[](https://leetcode.com/problems/valid-palindrome/)

  
[](https://leetcode.com/problems/valid-palindrome/)

![](https://blogger.googleusercontent.com/img/a/AVvXsEg3DNXVUAyLxCDGY0A38ozxdUevHfur46c75JfUvUeDC8i53VjLxR-cdqf3b4vn9vVw2Da54-nKC-m_ISFYWViVI02jAZiAjQ3P-5cBec-mh4VWK_FPGdYINw5pqVoKqNMx_x736bhJOnFSIfuYd1F2SBBfHpbf5bhrYUfpDBsHEhgu_ee7t1gXQ74j7m4)[](https://blogger.googleusercontent.com/img/a/AVvXsEg3DNXVUAyLxCDGY0A38ozxdUevHfur46c75JfUvUeDC8i53VjLxR-cdqf3b4vn9vVw2Da54-nKC-m_ISFYWViVI02jAZiAjQ3P-5cBec-mh4VWK_FPGdYINw5pqVoKqNMx_x736bhJOnFSIfuYd1F2SBBfHpbf5bhrYUfpDBsHEhgu_ee7t1gXQ74j7m4)

  
[](https://leetcode.com/problems/valid-palindrome/)

  
[](https://leetcode.com/problems/valid-palindrome/)

  
[](https://leetcode.com/problems/valid-palindrome/)

  
[](https://leetcode.com/problems/valid-palindrome/)

  
[](https://leetcode.com/problems/valid-palindrome/)

  
[](https://leetcode.com/problems/valid-palindrome/)

  
[](https://leetcode.com/problems/valid-palindrome/)

  
[](https://leetcode.com/problems/valid-palindrome/)

  
[](https://leetcode.com/problems/valid-palindrome/)

  
[](https://leetcode.com/problems/valid-palindrome/)

  
[](https://leetcode.com/problems/valid-palindrome/)

  

  

정규식을 통해 영문+숫자를 제외한 단어를 날려주고 비교하기 쉽게 소문자로 변환해주었다.

이제 앞부분과 뒷부분을 자르면서 숫자 비교를 하였는데 이번에도 시간이 좀 .... 

  

시간 단축 버전에서 쓰인 

Character 의 isletterOrDigit 을 고려해보기!