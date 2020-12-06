---
title: "Programmers Practice 10"
date: 2020-12-06
categories: CodingTest
tags: programmers python
languages: python
toc_label: "Contents"
---

## 1. 문제
Programmers - 점프와 순간 이동

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/12980)

## 2. 풀이
이진법으로 나타냈을 때 1의 개수로 치환할 수 있는 문제이다. (2배로 이동하는 건 에너지가 들지 않으므로 한 요소의 두배에 해당하는 건 모두 소거가 가능)

```python
def solution(n):
    answer = 0
    nintwo = 1
    while True:
        nintwo = nintwo*2
        if nintwo >= n :
            break
    while True:
        if n >= nintwo:
            n = n-nintwo
            answer += 1
            if n == 0 :
                break
        nintwo = nintwo/2
    return answer
```

다행히 효율성도 한번에 통과하였다.