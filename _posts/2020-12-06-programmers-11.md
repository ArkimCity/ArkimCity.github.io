---
title: "Programmers Practice 11"
date: 2020-12-06
categories: CodingTest
tags: programmers python
languages: python
toc_label: "Contents"
---

## 1. 문제
Programmers - 폰켓몬

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/1845)

## 2. 풀이
n/2가 포켓몬 종류수보다 많다면 포켓몬 종류수를 출력하고,
종류가 충분하다면 그냥 n/2를 출력해주면 된다.

```python
def solution(nums):
    answer = 0
    nums.sort()
    tempanswer = 0
    temp2 = 0
    for i in nums :
        temp1 = temp2
        temp2 = i
        if temp2 != temp1 :
            tempanswer += 1
    if tempanswer >= int(len(nums)/2) :
        return int(len(nums)/2)
    else :
        return tempanswer
```