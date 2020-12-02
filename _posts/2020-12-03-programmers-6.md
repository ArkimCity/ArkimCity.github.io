---
title: "Programmers Practice 5"
date: 2020-12-03
categories: CodingTest
tags: programmers python
languages: python
toc_label: "Contents"
---

## 1. 문제
Programmers - 최솟값 만들기

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/12941)

## 2. 풀이
```python
def solution(A,B):
    answer = 0
    A.sort()
    B.sort()
    for i in range(len(A)):
        answer+=A[i]*B[-i-1]
    return answer
```

곱 값을 최소로 만드는 방법은 크기 순서를 반대로 곱해주는 것이다.
