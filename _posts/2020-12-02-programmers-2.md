---
title: "Programmers Practice 2"
date: 2020-12-02
categories: CodingTest
tags: programmers java
languages: java
---

## 1. 문제
Programmers 7 - 피보나치 수

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/12945)

## 2. 풀이
```java
class Solution {
    public int solution(int n) {
        int answer = 0;
        int a = 1;
        int b = 1;
        int temp = 0;
        if (n <= 2) {
            return 1;
        }
        for (int i=2 ; i<n ; i++){
            temp = a;
            a = b;
            b = (b + temp)%1234567;
        }
        return b;
    }
}
```
처음에는 피보나치 함수를 직접 만들어 계산해야한다고 생각했었는데,

오히려 단순 계산이 훨씬 합리적인 경우이다.
