---
title: "Programmers Practice 23"
date: 2021-01-17
categories: CodingTest
tags: programmers python
languages: python
---
## 1. 문제 

programmers - 숫자 게임

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/12987)


## 2. 풀이

가장 큰것끼리 비교하기 시작하면서, 이길때까지 계속 A의 다음수를 찾아 경우를 더하면 된다.

```python
def solution(A, B):
    answer = 0;
    A.sort();
    B.sort();
    A.reverse();
    B.reverse();
    j = 0;
    for i in range(len(B)):
        detector = False;
        while B[i] <= A[j]:
            if j > len(A) - 2:
                detector = True;
                break;
            j += 1;
        if detector:
            break
        j += 1;
        answer += 1;
        if j > len(A) - 1:
            break;
    return answer;

```