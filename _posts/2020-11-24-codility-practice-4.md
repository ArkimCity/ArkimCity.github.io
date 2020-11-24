---
title: "Codility Practice 4"
date: 2020-11-24
categories: CodingTest
tags: codility python
languages: python
---
Codility lessons 4 - counting_elements - MaxCounters

Question-url : https://app.codility.com/programmers/lessons/4-counting_elements/max_counters/

1차 시도

```python
def solution(N, A):
    cache = {}
    for i in range(1,N+1) :
        cache[i] = 0
    for i in range(len(A)):
        if A[i] <= N :
            if A[i] in cache:
                cache[A[i]] += 1
            else :
                cache[A[i]] = 1
        else :
            for i in range(1, len(cache)+1):
                cache[i] = max(cache.values())
    return list(cache.values())
```

정확도는 백퍼센트지만 효율성테스트에서 빵점이 나왔다.

```python
def solution(N, A):
    cache = {}
    for i in range(1,N+1) :
        cache[i] = 0
    for i in A:
        if i <= N :
            cache[i] += 1
        else :
            maxvalue = max(cache.values())
            for j in range(1, N+1):
                cache[j] = maxvalue
    return list(cache.values())
```

효율성을 위해 조금 발버둥 쳐보았다.

어느정도 나아졌지만 본질적으로 time complexity가 크게 바뀌지 않아 모두 성공하지는 못했다.