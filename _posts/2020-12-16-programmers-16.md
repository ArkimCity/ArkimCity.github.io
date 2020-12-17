---
title: "Programmers Practice 16"
date: 2020-12-16
categories: CodingTest
tags: programmers python
languages: python
toc_label: "Contents"
---

## 1. 문제
Programmers - 스킬트리

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/49993)

## 2. 풀이

속도를 위해 기본 뺘대는 딕셔너리를 사용했고, 해당 스킬을 비교하면서 이중 브레이크를 사용했다

```python
def solution(skill, skill_trees):
    answer = len(skill_trees)
    for tree in skill_trees :
        minimap = {}
        for i in range(len(tree)):
            minimap[tree[i]] = i
        detector = -1
        for j in range(len(skill)):
            try :
                tempindex = minimap[skill[j]]
                if detector > tempindex :
                    answer -= 1
                    break
                print(tempindex)
                detector = tempindex
            except :
                boolean1 = False
                for k in range(len(skill)-j) :
                    try :
                        temp = minimap[skill[k+j+1]]
                        answer -= 1
                        boolean1 = True
                        break
                    except :
                        pass
                if boolean1 :
                    break
    return answer
```

