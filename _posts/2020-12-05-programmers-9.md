---
title: "Programmers Practice 9"
date: 2020-12-05
categories: CodingTest
tags: programmers python
languages: python
toc_label: "Contents"
---

## 1. 문제
Programmers - 베스트앨범

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/42579)

## 2. 풀이
딕셔너리를 이중으로 사용해 {"classic":{"0":500,"2":150,"3":800},"pop":{"1":600,"4":2500}} 과 같은 구조를 만들었다. 이후 values sum으로 합산 최다 장르를 하나씩 뽑아오며 나열했다.

```python
def findmaxkey(dictionary):
    answerkey = 0
    for i in dictionary :
        if dictionary[i] == max(list(dictionary.values())):
            answerkey = i
            break
    return answerkey

def solution(genres, plays):
    answer = []

    #total 생성부분
    total = {}
    for i in range(len(plays)):
        temp = {}
        if genres[i] in total:
            total[genres[i]][i] = plays[i]
        else :
            total[genres[i]] = temp
            total[genres[i]][i] = plays[i]

    #장르별 합산 비교 생성부분
    forbestgenre = {}
    for j in total :
        forbestgenre[j] = sum(total[j].values())
        
    #계산부분
    for k in range(len(total)) :
        temp = findmaxkey(forbestgenre)
        temp2 = 0
        for l in range(len(total[temp])):
            if len(total[temp])==0 :
                break
            else:
                index = findmaxkey(total[temp])
                answer.append(index)
                del total[temp][index]
                temp2+=1
                if temp2 == 2:
                    break
        del total[temp]
        del forbestgenre[temp]
        
    return answer
```

