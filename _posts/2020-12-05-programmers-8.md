---
title: "Programmers Practice 8"
date: 2020-12-05
categories: CodingTest
tags: programmers python
languages: python
toc_label: "Contents"
---

## 1. 문제
Programmers - 멀리 뛰기

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/12914)

## 2. 풀이
```python
def solution(n):
    a=1
    b=1
    for i in range(n-1):
        temp = a
        a=b
        b = (b + temp)%1234567
    return b
```

피보나치와 같은 방식으로 풀 수 있다.