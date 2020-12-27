---
title: "Programmers Practice 20"
date: 2020-12-27
categories: CodingTest
tags: programmers python
languages: python
toc_label: "Contents"
---

## 1. 문제
Programmers - 방문 길이

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/49994)

## 2. 풀이

실제 이동한 라인을 직접 사용했다

```python
def solution(dirs):
    lines = []
    answer = 0
    point ={"x":0,"y":0}
    for i in dirs:
        check = False
        templine = []
        templine.append([point["x"], point["y"]])
        if i == "U":
            if point["y"] + 1 <= 5 :
                point["y"] += 1
                check = True
        elif i == "D":
            if point["y"] - 1 >= -5 :
                point["y"] -= 1
                check = True
        elif i == "R":
            if point["x"] + 1 <= 5 :
                point["x"] += 1
                check = True
        elif i == "L":
            if point["x"] - 1 >= -5 :
                point["x"] -= 1
                check = True
        templine.append([point["x"], point["y"]])
        if sorted(templine) not in lines and check:
            print(templine)
            lines.append(sorted(templine))
    return len(lines)
```

