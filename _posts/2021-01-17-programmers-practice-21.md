---
title: "Programmers Practice 21"
date: 2021-01-17
categories: CodingTest
tags: programmers python
languages: python
---
## 1. 문제 

programmers - 줄 서는 방법

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/12936)


## 2. 풀이

하나 하나 경우의 수를 찾기보다, 연산을 통해 해당 순번의 상황을 연산해내는 게 계산상 훨씬 효율적이기 때문에 이와 같이 풀었다

```python
import math;

def solution(n, k):
    answer = [];
    totalNumber = math.factorial(n);
    numberList = list(range(1, n+1));
    
    for i in range(n):
        
        totalNumber = totalNumber/(n-i);
        tempAnswer = math.ceil(k/totalNumber);
        addAnswer = numberList[tempAnswer-1];
        answer.append(addAnswer);
        numberList.remove(addAnswer);
        k = k - (tempAnswer-1) * totalNumber;
        
    return answer;
```