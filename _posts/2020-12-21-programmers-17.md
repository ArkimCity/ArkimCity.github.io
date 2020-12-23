---
title: "Programmers Practice 17"
date: 2020-12-16
categories: CodingTest
tags: programmers python
languages: python
toc_label: "Contents"
---

## 1. 문제
Programmers - 2 x n 타일링

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/12900)

## 2. 풀이

타일의 첫번쨰가 세로인 경우 한줄을 뺀 나머지 줄 수의 경우의 수

타일의 첫번쨰가 가로인 경우 두줄을 뺀 나머지 줄 수의 경우의 수

이기 때문에 피보나치로 해결이 가능하다

```python
def solution(n):
    a=1
    b=1
    for i in range(n-1):
        temp = a
        a=b
        b = (b + temp)%1000000007
    return b
```

