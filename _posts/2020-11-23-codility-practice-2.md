---
title: "Codility Practice 2"
date: 2020-11-23
categories: CodingTest
tags: codility python
languages: python
---
Codility lessons 3 - time_complexity - TapeEquilibrium

Question : https://app.codility.com/programmers/lessons/3-time_complexity/tape_equilibrium/

직관적인 답은 이렇다.

```python
def solution(A):
    num1 = sum(A)
    num2 = 0
    for i in A:
        num1 -= i
        num2 += i
        if num2 >= num1:
            answer = min(abs(num2 - num1),abs(num2 - num1 - 2 * i))
    return answer
```

하지만 이 경우 리스트가 존재하지 않는 경우를 계산할 수 없다.


