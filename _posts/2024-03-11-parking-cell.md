---
layout: post
title:  "Parking Cell"
# author: john
categories: [ Parking, Automation ]
tags: []  # red, yellow
# image: assets/images/11.jpg
description: "설계 자동화에서 주차칸을 배치하고자 할 떄의 필요한 데이터는 무엇일까."
featured: false
hidden: false
# rating: 4.5
beforetoc: "test"
toc: false
---

주차는 설계 자동화에 있어 가장 빈번하게 마주치고 중요하게 여겨지는 대표적인 항목 중에 하나이다. 이 때, 주차칸이라는 데이터를 어떻게 바라볼 수 있을까.

#### Parking Cell

주차칸 하면 떠오르는 기본적인 이미지는 아래와 같다.

<img src="/assets/images/parking_cell.png" alt="Parking Cell" height="200"/>

하지만 주차칸이 그려지기 위해서는 설계적인 컨텍스트 와 법규 사항이 존재한다.

대표적인 내용은 다음과 같다.

```html
직각 주차를 기준으로,
1. 2.5m 의 가로 폭이 존재해야 한다.
2. 5.0m 의 세롶 폭이 존재해야 한다.
3. 주차의 진입방향에 주차칸과 동일한 가로 폭 2.5m에, 세로폭 6.0m 빈 공간이 존재해야 한다.
  3-1. 해당 빈 공간은 기본적으로 대지 내에 위치하여야 한다.
  3-2. 해당 빈 공간은 도로 폭이 좁은 면과 접해있을 경우와 같이 특수한 경우,
       모든 부분이 대지 내에 위치하지 않아도 무방하다. (외부차로 주차)
4. 해당 주차칸의 진입부 빈공간으로부터, 혹은 진입부 그 자체는
   2.5미터의 폭으로 대지의 외부에 해당하는 도로까지 반드시 이어져 있어야 한다.
```

```Python

```
