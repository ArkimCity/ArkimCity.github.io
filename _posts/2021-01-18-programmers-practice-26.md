---
title: "Programmers Practice 26"
date: 2021-01-18
categories: CodingTest
tags: programmers python
languages: python
---
## 1. 문제 

programmers - 여행경로

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/43164)


## 2. 풀이

노드 탐색을 행하는 건 비슷하지만, 처음에 인천에서 시작해야 한다는 점, 전체 리스트를 구해야 한다는 점이 있다.

```python
def solution(tickets):
    answerList = []
    for i in range(len(tickets)):
        if tickets[i][0] == "ICN":
            tempTickets = tickets.copy()
            tempTicket = tempTickets[i]
            del tempTickets[i]
            for tempAnswer in detector(tempTicket, tempTickets):
                answerList.append(tempTicket + tempAnswer)
    return sorted(answerList)[0]

def detector(ticket, leftTickets):
    answerList = []
    for i in range(len(leftTickets)):
        leftTicket = leftTickets[i]
        if ticket[1] == leftTicket[0]:
            tempTickets = leftTickets.copy()
            del tempTickets[i]
            for tempAnswer in detector(leftTicket, tempTickets):
                answerList.append([leftTickets[i][1]] + tempAnswer)
    if len(leftTickets)==1:
        return [[leftTickets[0][1]]]
    return answerList
```