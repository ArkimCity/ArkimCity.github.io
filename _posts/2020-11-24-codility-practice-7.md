---
title: "Codility Practice 7"
date: 2020-11-24
categories: CodingTest
tags: codility python
languages: python
---
Codility lessons 5 - prefix_sums - CountDiv

Question-url : https://app.codility.com/programmers/lessons/5-prefix_sums/count_div/

frog jump와 마찬가지로 얼핏 생각하면 for을 쓰기 쉽지만 단순 계산이 가장 효율적이다.

```python
def solution(A, B, K):
    if A%K == 0 :
        answer = int((B-A)/K) + 1
    else :
        if (int(A/K) + 1) * K > B:
            answer = 0
        else :
            answer = int((B-(int(A/K) + 1) * K)/K) + 1
    return answer
```

(int(A/K) + 1) * K 는 A 보다 큰 (A와 같을 경우는 위의 if로 빼두었으니 제외) 가장 작은 K로 나눠떨어지는 수를 구하기 위한 계산이다.

이것이 B보다 크면 볼것도 없이 답은 0

나머지의 경우 else: else:에 frogjump와 같은 논리 사용하면 성공