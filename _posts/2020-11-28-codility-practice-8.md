---
title: "Codility Practice 8"
date: 2020-11-28
categories: CodingTest
tags: codility python
languages: python
---
Codility lessons 6 - sorting - Distinct

Question-url : https://app.codility.com/programmers/lessons/6-sorting/distinct/

이전 것과 비교하는 걸 이제까지 인덱스를 많이 사용했는데, 생각해보니 그냥 detector를 따로 지정해주는게 더 효율적으로 보인다.

```python
def solution(A):
    A.sort()
    answer = []
    detector = 1000001
    for i in A:
        if i==detector:
            detector=i
        else : 
            answer.append(i)
            detector=i
    return len(answer)
```

성공