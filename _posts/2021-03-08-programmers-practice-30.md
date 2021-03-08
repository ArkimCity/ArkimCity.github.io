---
title: "Programmers Practice 30"
date: 2021-03-08
categories: CodingTest
tags: programmers python
languages: python
---
## 1. 문제 

programmers - K번째수

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/42748)


## 2. 풀이

문제 자체는 간단하지만 한줄 코딩을 시도해 보았다.

```python
def solution(array, commands):
    return list(map(lambda command: sorted(array[command[0]-1:command[1]])[command[2]-1], commands))

```