---
title: "Codility Practice 3"
date: 2020-11-23
categories: CodingTest
tags: codility python
languages: python
---
Codility lessons 4 - counting_elements - FrogRiverOne

Question-url : https://app.codility.com/programmers/lessons/4-counting_elements/frog_river_one/

1차 시도

```python
def solution(X, A):
    answer = 0
    cache = list(range(1, X+1))
    for i in range(len(A)) :
        if A[i] in cache :
            cache.remove(A[i])
        else :
            pass
        if len(cache) == 0 :
            answer = i
            break
    if len(cache) > 0 :
            answer = -1
    return answer
```

시간제한에 맞추지 못했다 remove가 시간을 많이 잡아먹는 것으로 보인다.

다 차는 순간을 찾아야 하기 때문에 linear scan은 포기할 수 없다면

cache를 리스트로 선언한 것이 잘못된 것으로 보인다.
cache를 딕셔너리 방식으로 사용하기 위해 not in 으로 바꾸며 시도했다.

```python
def solution(X, A):
    answer = 0
    cache = {}
    for i in range(len(A)) :
        if A[i] not in cache :
            cache[A[i]]=A[i]
        else :
            pass
        if len(cache) == X :
            answer = i
            break
    if len(cache) < X :
            answer = -1
    return answer
```

효율성까지 성공했다