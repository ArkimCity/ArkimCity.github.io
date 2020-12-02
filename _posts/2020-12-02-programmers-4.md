---
title: "Programmers Practice 4"
date: 2020-12-02
categories: CodingTest
tags: programmers python
languages: python
toc_label: "Contents"
---

## 1. 문제
Programmers - 최댓값과 최솟값

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/12939)


## 2. 풀이
```python
def solution(s):
    list1 = s.split(" ")
    list2 = []
    for i in list1:
        list2.append(int(i))
    list2.sort()
    return str(list2[0])+" "+str(list2[-1])
```

쉬운 문제라 따로 설명은 안붙히겠습니다
