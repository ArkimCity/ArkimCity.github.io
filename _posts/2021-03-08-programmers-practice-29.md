---
title: "Programmers Practice 29"
date: 2021-03-08
categories: CodingTest
tags: programmers python
languages: python
---
## 1. 문제 

programmers - 타겟 넘버

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/43165)


## 2. 풀이

연산 개수(최대 2*20)를 보았을 때 이중 포문이 더 간단할 것 같아 아래와 같이 풀어보았다.

```python
def solution(numbers, target):
    answer = 0
    tempList = [0]
    for number in numbers:
        for i in range(len(tempList)):
            tempList.append(tempList[i] - number)
            tempList[i] += number
    return tempList.count(target)
```