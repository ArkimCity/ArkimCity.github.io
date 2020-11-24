---
title: "Codility Practice 6"
date: 2020-11-24
categories: CodingTest
tags: codility python
languages: python
---
Codility lessons 4 - counting_elements - PermCheck

Question-url : https://app.codility.com/programmers/lessons/4-counting_elements/perm_check/

1차 시도

```python
def solution(A):
    A.sort()
    answer = 1
    for i in range(len(A)):
        if i+1 != A[i]:
            answer = 0
            break
    return answer
```

리니어 스캔을 전부 해야하는 상황이라 판단했다. 다행히 한번에 통과