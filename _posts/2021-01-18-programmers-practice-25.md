---
title: "Programmers Practice 25"
date: 2021-01-18
categories: CodingTest
tags: programmers python
languages: python
---
## 1. 문제 

programmers - 단속카메라

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/42884)


## 2. 풀이

작은 순서대로 놓으면 안 겹치는 순간 어쩔 수 없이 새로 생기는 경우와 같다.

```python
def solution(routes):
    routes.sort()
    answer = 1
    temp = [-30000, 30000]
    for i in range(len(routes)):
        if temp[0] > routes[i][1] or temp[1] < routes[i][0]:
            answer += 1
            temp = [routes[i][0], routes[i][1]]
        else :
            if temp[0] <= routes[i][1] and temp[0] <= routes[i][0]:
                temp[0] = routes[i][0]
            if temp[1] >= routes[i][0] and temp[1] >= routes[i][1]:
                temp[1] = routes[i][1]
    return answer
```