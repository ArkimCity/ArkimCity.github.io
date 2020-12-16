---
title: "Programmers Practice 14"
date: 2020-12-16
categories: CodingTest
tags: programmers python
languages: python
toc_label: "Contents"
---

## 1. 문제
Programmers - 영어 끝말잇기

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/12981)

## 2. 풀이

```python
def solution(n, words):
    answer = []
    wordsmap = {}
    i = 0
    for word in words:
        if i > 0 :
            if word in wordsmap or word[0]!=wordsmap[words[i-1]][-1]:
                return [(i)%n+1,int(i/n)+1]
        wordsmap[word] = word
        i += 1
    return [0,0]
```

