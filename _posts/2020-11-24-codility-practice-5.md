---
title: "Codility Practice 5"
date: 2020-11-24
categories: CodingTest
tags: codility python
languages: python
---
Codility lessons 4 - counting_elements - MissingInteger

Question-url : https://app.codility.com/programmers/lessons/4-counting_elements/missing_integer/

1차 시도

```python
def solution(A):
    tempmap = {}
    answer = 1
    for i in A :
        if i in tempmap :
            pass
        else :
            tempmap[i]=i
    while True :
        if answer in tempmap:
            answer += 1
        else :
            break
    return answer
```

한번에 통과했다. 딕셔너리 활용을 생활화 해야겠다.