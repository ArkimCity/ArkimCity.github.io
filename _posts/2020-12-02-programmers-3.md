---
title: "Programmers Practice 3"
date: 2020-12-02
categories: CodingTest
tags: programmers java
languages: java
toc_label: "Contents"
---

## 1. 문제
Programmers 7 - 숫자의 표현

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/12924)


## 2. 풀이
```java
class Solution {
    public int solution(int n) {
        int answer = 0;
        int j = 1;
        while(true){
            int temp = 0;
            for(int i = 1 ; i <= j ; i++){
                temp += i;
            }
            if (temp>n){
                break;
            }else if ((n-temp)%j==0){
                answer+=1;
            }
            j += 1;
        }
        return answer;
    }
}
```

1에서 j까지 j개의 연속된 수를 더해 원래수에서 뺄 경우 j로 나눠진다면 답에 추가할 수 있다.
