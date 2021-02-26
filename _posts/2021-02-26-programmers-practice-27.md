---
title: "Programmers Practice 27"
date: 2021-02-26
categories: CodingTest
tags: programmers python
languages: python
---
## 1. 문제 

programmers - 줄 서는 방법

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/12936)


## 2. 풀이

유저들의 리스트에서 정해진 계산을 통해 어떤 번호가 나올지 규칙을 찾는다면 직접 계산하는 것보다 훨씬 효율적으로 찾을 수 있다.

```python
import math

def solution(n, k):
    people = list(range(1, n+1))
    answer = []
    for i in reversed(range(1, n)):
        det = math.factorial(i)
        answer.append(people[math.ceil(k/det)-1])
        del people[math.ceil(k/det)-1]
        k = k - (math.ceil(k/det) - 1)*det
    answer.append(people[0])
    return answer
```