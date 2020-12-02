---
title: "Programmers Practice 5"
date: 2020-12-03
categories: CodingTest
tags: programmers python
languages: python
toc_label: "Contents"
---

## 1. 문제
Programmers - N개의 최소공배수

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/12953)


## 2. 풀이
```python
def solution(arr):
    answer = 0
    i=1
    while True:
        temp=0
        i+=1
        for j in arr:
            if i%j==0:
                temp+=1
            else:
                break
        if temp==len(arr):
            answer=i
            break
    return answer
```

솔직히 썩 시원한 답은 아니지만 가장 직관적인 방법입니다.
