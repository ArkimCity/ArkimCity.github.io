---
title: "Programmers Practice 12"
date: 2020-12-08
categories: CodingTest
tags: programmers python
languages: python
toc_label: "Contents"
---

## 1. 문제
Programmers - 기능개발

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/42586)

## 2. 풀이
필요한 날짜를 쭉 늘어놓고 계산을 시작하는 지점마다 그거보다 큰게 나오면 스톱시켜주는 방식으로 더해주었다.

```python
def solution(progresses, speeds):
    answer = []
    needdays = []
    temp = 0
    temp2 = 0
    
    for i in range(len(progresses)):
        if (100-progresses[i])%speeds[i]==0:
            needdays.append((100-progresses[i])/speeds[i])
        else :
            needdays.append(int((100-progresses[i])/speeds[i]+1))
        
    for j in range(len(needdays)) : 
        if needdays[j] > temp2:
            answer.append(j - temp)
            temp = j
            temp2 = needdays[j]
        
    answer.append(len(progresses) - sum(answer))
    del answer[0]
    return answer
```