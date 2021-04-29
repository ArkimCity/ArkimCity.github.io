---
title: "Language Study - multiprocessing"
date: 2021-04-29
categories: LanguageStudies
tags: python
---
<!-- https://niceman.tistory.com/145 -->
<!-- https://dailyheumsi.tistory.com/105 -->

## 1. multiprocessing

어떤 function에 대한 연산을 다수의 코어가 존재하는 컴퓨터에게 병렬처리 하는 것을 도와주는 파이썬 라이브러리

multiprocessing 시 다른 함수 실행과 잘못 중첩되면 오히려 속도가 매우 느려지는 경우도 있고, 

정말 필요하지 않을 경우에 굳이 사용하면 이 과정에서 오히려 속도가 더 느려지는 경우, 매모리 점유 증가 등의 이슈를 인지하고 사용해야 한다고 한다.

## 2. Pool - map

대표적인 라이브러리인 pool 사용 례

공통부
```python
import time
import multiprocessing

custom_list = list(range(40000))

def custom_function(injected_from_list):
    return injected_from_list, sum(range(10000))
```

pool test
```python
start_time = time.time()

if __name__ == '__main__':
    p = multiprocessing.Pool(processes=4)
    result = p.map(custom_function, custom_list)
    print(type(result))

print(time.time() - start_time)
# 2.2002766132354736
```

일반 사용 례
```python
start_time = time.time()

result = list(map(custom_function, custom_list))
print(len(result))

print(time.time() - start_time)
# 6.068422794342041
```

다소 긴 연산이 필요한 작업을 시켰을 때, 약 세배의 가까운 차이가 난 것을 볼 수 있다.