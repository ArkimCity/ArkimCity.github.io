---
title: "Programmers Practice 13"
date: 2020-12-08
categories: CodingTest
tags: programmers java
languages: java
toc_label: "Contents"
---

## 1. 문제
Programmers - 예상 대진표

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/12985)

## 2. 풀이

반으로 갈랐을때 같은 그룹에 있다면 계속 갈라가고, 서로 다른 그룹에 있다면 각 그룹의 모든 결투가 끝날때까지 만나지 않는다는 것을 이용했다.

```java
class Solution {
    public int solution(int n, int a, int b) {
        int answer = 0;
        int ntwo = 0;
        int nn = 1;
        
        for (int i = 0 ; true ; i = i + 1) {
            if (nn == n) {
                ntwo = i;
                break;
            }
            nn=nn*2;
        }
        
        for (int i = 0 ; true ; i = i + 1) {
            if (a > n/2) {
                if (b <= n/2) {
                    answer = ntwo - i;
                    break;
                } else {
                    a = a - n/2;
                    b = b - n/2;
                }
            } else {
                if (b > n/2) {
                    answer = ntwo - i;
                    break; 
                }
            }
            n = n/2;
        }
        return answer;
    }
}
```