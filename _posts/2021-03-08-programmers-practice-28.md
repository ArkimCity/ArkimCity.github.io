---
title: "Programmers Practice 28"
date: 2021-03-08
categories: CodingTest
tags: programmers python
languages: python
---
## 1. 문제 

programmers - 정수 삼각형

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/43105)


## 2. 풀이

삼각형을 잘라서 가지고 들어가려고 하다보니 오히려 연산이 너무 오래걸렸다. 다른 풀이를 보고 좌표를 이용해 추가적인 연산을 줄이니 같은 방법이어도 통과할 수 있었다.

```python
def solution(triangle):
    return dp(triangle,0,0)

def dp(triangle,i,j, __cache__={}):
    strtr, answer = (i,j), triangle[i][j]
    if strtr in __cache__:
        return __cache__[strtr]
    else :
        if len(triangle) > i+1 and len(triangle) > j+1:
            answer += max([dp(triangle, i+1, j), dp(triangle, i+1, j+1)])
        __cache__[strtr]=answer
    return answer
```