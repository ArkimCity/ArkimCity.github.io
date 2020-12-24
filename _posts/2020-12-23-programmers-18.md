---
title: "Programmers Practice 18"
date: 2020-12-23
categories: CodingTest
tags: programmers python
languages: python
toc_label: "Contents"
---

## 1. 문제
Programmers - 최고의 집합

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/12938#)

## 2. 풀이

최고의 곱셈은 필연적으로 가장 적은 차이를 가진 자연수만 사용해야 한다. 

```python
def solution(n, s):
    answer = []
    addaral = int(s/n)
    if s >= n :
        for i in range(n-s%n):
            answer.append(addaral)
        for j in range(s%n):
            answer.append(addaral+1)
    else :
        answer.append(-1)
    return sorted(answer)
```

