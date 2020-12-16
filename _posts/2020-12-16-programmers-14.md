---
title: "Programmers Practice 14"
date: 2020-12-16
categories: CodingTest
tags: programmers python
languages: python
toc_label: "Contents"
---

## 1. 문제
Programmers - 구명보트

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/42885)

## 2. 풀이

보트의 정원이 두명밖에 되지 않으므로 제일 큰 것과 제일 작은 것의 합을 비교해나가는 것으로 풀이가 가능하다

```python
def solution(people, limit):
    answer = 0
    people.sort()
    people.reverse()
    j = len(people) - 1
    for i in range(len(people)):
        if people[i] + people[j] > limit :
            answer += 1
        else :
            j -= 1
            answer += 1
        if i >= j :
            break
    return answer
```

