---
title: "Programmers Practice 7"
date: 2020-12-03
categories: CodingTest
tags: programmers python
languages: python
toc_label: "Contents"
---

## 1. 문제
Programmers - 카펫

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/42842)

## 2. 풀이
```python
def solution(brown, yellow):
    x=(+4+brown+(((4-brown)**2)-16*yellow)**0.5)/4
    y=brown/2-x+2
    return [x,y]
```

완전히 수학문제다

brown = 2x +2y - 4

yellow = (x-2)(y-2)

brown과 yellow는 상수기때문에 서로 다른 두개의 식과 두개의 변수로 필연적으로 답을 찾을 수 있다.

근의 공식의 해는 위와 같다