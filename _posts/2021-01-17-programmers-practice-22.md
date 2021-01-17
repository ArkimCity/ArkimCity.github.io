---
title: "Programmers Practice 22"
date: 2021-01-17
categories: CodingTest
tags: programmers python
languages: python
---
## 1. 문제 

programmers - 네트워크

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/43162)


## 2. 풀이

네트워크 탐색을 편하게 하기 위해 딕셔너리로 변환하고, 내부 탐색을 실행한다

```python
def detect(inputKey, computerMap, detectedMap):
    innerList = computerMap[inputKey];
    for j in range(len(innerList)):
        if j not in detectedMap and j != inputKey and innerList[j] == 1:
            detectedMap[j] = j;
            detectedMap.update(detect(j, computerMap, detectedMap));
    return detectedMap;
    
def solution(n, computers):
    answer = 0;
    computerMap = {};
    detectedMap = {};
    for i in range(n):
        computerMap[i] = computers[i];
    for computerKey in computerMap:
        if computerKey not in detectedMap:
            detectedMap.update(detect(computerKey, computerMap, {computerKey:computerKey}));
            answer += 1;
    return answer;
```