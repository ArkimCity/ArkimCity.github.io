---
title: "Programmers Practice 19"
date: 2020-12-27
categories: CodingTest
tags: programmers python
languages: python
toc_label: "Contents"
---

## 1. 문제
Programmers - 등굣길

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/42898)

## 2. 풀이

재귀에 캐시까지 써서 효율성 통과에 성공했다

```python
def solution(m, n, puddles, __cache__={"1,1":1}) :
    answer = 0
    if str(m)+","+str(n) in __cache__ :
        return __cache__[str(m)+","+str(n)]
    if m > 1 and [m-1, n] not in puddles:
        answer = solution(m-1, n, puddles)
    if n > 1 and [m, n-1] not in puddles:
        answer += solution(m, n-1, puddles)
    __cache__[str(m)+","+str(n)]=answer%1000000007
    return answer%1000000007
```

