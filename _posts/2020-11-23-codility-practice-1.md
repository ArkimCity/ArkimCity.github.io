---
title: "Codility Practice 1"
date: 2020-11-23
categories: CodingTest
tags: codility python
languages: python
---
Codility lessons 3 - time_complexity - FrogJump

Question-url : https://app.codility.com/programmers/lessons/3-time_complexity/frog_jmp/

frog 와 jump라는 단어때문에 for을 통한 반복을 연상하기 쉽다.

```python
def solution(X, Y, D):
    answer = 0
    while True :
      X += D
      answer += 1
      if Y <= X :
        break
    return answer
```

하지만, 실제로는 간단한 계산을 통한 답이 훨씬 효율적이다.

```python
def solution(X, Y, D):
    answer = int((Y-X)/D+1)
    return answer
```

와 같은 기본 뼈대가 만들어지고, 여기에 나누어 떨어지는 경우를 분리해주면 된다.

```python
def solution(X, Y, D):
    if (Y-X)%D == 0 :
        answer = (Y-X)/D
    else :
        answer = int((Y-X)/D+1)
    return answer
```
