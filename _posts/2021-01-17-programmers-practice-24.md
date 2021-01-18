---
title: "Programmers Practice 24"
date: 2021-01-17
categories: CodingTest
tags: programmers python
languages: python
---
## 1. 문제 

programmers - 단어 변환

[Question-url](https://programmers.co.kr/learn/courses/30/lessons/43163)


## 2. 풀이

문자열 비교만 별도로 만드는 것을 제외하면 노드식으로 탐색해 가장 짧은 연결길이를 역으로(연결에 필요없는 단어의 수가 가장 긴 답을) 리턴하는 방식을 사용했다.

```python
def solution(begin, target, words):
    detected = (detector(begin, target, words));
    if detected == 0 :
        return 0;
    else :
        return len(words) - detected;
    
def detector(begin, target, words):
    answer = 0;
    for word in words:
        tempWords = {}
        for word2 in words:
            tempWords[word2] = word2;
        if simTest(begin, word):
            del tempWords[word];
            if word == target:
                return len(tempWords);
            tempAnswer = detector(word, target, tempWords);
            if answer < tempAnswer:
                answer = tempAnswer;
    return answer

def simTest(str1, str2):
    detector = True;
    temp = 0;
    for i in range(len(str1)):
        if str1[i] != str2[i] :
            temp += 1;
            if temp > 1:
                detector = False;
                break;
    return detector;

```