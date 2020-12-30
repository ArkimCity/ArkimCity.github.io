---
title: "Codility Practice 8"
date: 2020-11-28
categories: CodingTest
tags: codility python
languages: python
---
## 1. 문제 

Codility lessons 8 - Leader - Dominator

[Question-url](https://app.codility.com/programmers/lessons/8-leader/dominator/)


## 2. 풀이

아주 간단한 찾기 문제이다. 찾는 방법을 딕셔너리를 활용해 속도를 높이려 해보았다.

```python
def solution(A):
    if len(A) == 0 :
        return -1
    answer = -1
    indicator = len(A)/2
    atomap = {}
    
    for i in A :
        if i in atomap :
            atomap[i] += 1
        else :
            atomap[i] = 1
        if atomap[i] > indicator :
            answer = A.index(i)
            break

    return answer
```

성공