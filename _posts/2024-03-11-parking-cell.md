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
Parking is one of the most frequently encountered and considered important in design automation.
At this time, let's think briefly about how we can look at the data of the parking.

#### conditions of parking

The basic image that comes to mind when you think of a parking lot is as follows.

<img src="/assets/images/parking_cell.png" alt="Parking Cell" height="200"/>

However, there are design contexts and regulations for the parking compartment to be drawn.

Representative content is as follows.

```html
Based on right-angled parking,
   1. A width of 2.5 m shall exist.
   2. A vertical width of 5.0 m shall exist.
   3. There shall be an empty space 2.5 meters wide and 6.0 meters wide, which is the same as the parking compartment, in the entry direction of the parking.
      3-1. The empty space shall basically be located within the site.
      3-2. In special cases, such as when a vacant space is in contact with a narrow road surface,
         It's okay not to have all parts located within the site (parked by outside car)
         3-2-1. There are 8 logarithmic limits if you want to park by being bitten by an external lane.
   4. From the empty space of the entry part of the parking space, or the entry part itself
      It shall be 2.5 meters wide and shall be connected to the road corresponding to the outside of the site.
```

In other words, from the perspective of Computational Design, placing a parking space is a big deal
- As well as placing the square where the car compartment is drawn
- This means that the parking compartment, the entry part of the parking compartment, and the entry part of the parking compartment shall be located from the outside road of the site.

A simple illustration of this is as follows.

<img src="/assets/images/parking_simple_diagram.png" alt="Parking Cell" height="400"/>

Additionally,
- You may need a reference centerline to arrange this parking,
- Whether or not this parking space is parked due to being bitten by an outside lane,
- To see if you're going beyond the logarithmic limits that can be gathered if you're parked after being bitten, what is the corresponding group index

Parking can be arranged accurately only with information such as information, and it can be easily reflected even if post-processing is needed in the future.

In addition, in the process of actual parking arrangements, the information necessary for parking and the information necessary to be contained in each parking space are
It is reflected when you create a class that corresponds to the ParkingCell you want to create while working, making it easier to create criteria for placement.

-------------------------------------------

주차는 설계 자동화에 있어 가장 빈번하게 마주치고 중요하게 여겨지는 대표적인 항목 중에 하나입니다.
이 때, 주차칸이라는 데이터를 어떻게 바라볼 수 있을지 간략하게 생각해보겠습니다.

#### 주차의 조건

주차칸 하면 떠오르는 기본적인 이미지는 아래와 같습니다.

<img src="/assets/images/parking_cell.png" alt="Parking Cell" height="200"/>

하지만 주차칸이 그려지기 위해서는 설계적인 컨텍스트 와 법규 사항이 존재합니다.

대표적인 내용은 다음과 같습니다.

```html
직각 주차를 기준으로,
1. 2.5m 의 가로 폭이 존재해야 한다.
2. 5.0m 의 세로 폭이 존재해야 한다.
3. 주차의 진입방향에 주차칸과 동일한 가로 폭 2.5m에, 세로폭 6.0m 빈 공간이 존재해야 한다.
  3-1. 해당 빈 공간은 기본적으로 대지 내에 위치하여야 한다.
  3-2. 해당 빈 공간은 도로 폭이 좁은 면과 접해있을 경우와 같이 특수한 경우,
       모든 부분이 대지 내에 위치하지 않아도 무방하다. (외부차로 주차)
    3-2-1. 외부차로에 물려 주차를 시키고자 할 경우에는 8대 의 대수 제한이 존재한다.
4. 해당 주차칸의 진입부 빈공간으로부터, 혹은 진입부 그 자체는
   2.5미터의 폭으로 대지의 외부에 해당하는 도로까지 반드시 이어져 있어야 한다.
.
.
.
```

즉 Computational Design 관점에서 주차칸을 배치한다는 것은
- 주차칸이 그려지는 해당 사각형을 배치하는 것 뿐만 아니라
- 해당 주차칸과 해당주차칸의 진입부, 해당 주차칸의 진입부로 대지의 외부 도로부터 도달하는 길이 배치되어야 한다는 것을 뜻합니다.

이를 간단하게 그림으로 나타내면 다음과 같습니다.

<img src="/assets/images/parking_simple_diagram.png" alt="Parking Cell" height="400"/>

추가적으로,
- 이 주차를 배치하기 위해서는 기준이 되는 중심 선이 필요할 수도 있고,
- 이 주차가 외부 차로와 물려서 주차한 주차칸인지 아닌지,
- 물려서 주차한 경우 모여있을 수 있는 대수제한을 넘어가는지 확인하기 위해 해당하는 그룹 인덱스가 무엇인지

등의 정보가 있어야 정확하게 주차를 배치할 수 있고, 또 추후 후처리가 필요할 경우에도 수월한 반영이 가능합니다.

이 밖에도 실제 주차 배치를 하는 과정에서 주차에 필요한 정보, 그리고 각 주차칸에 내제되어야 한다고 필요되는 정보는
작업을 하며 생성할 ParkingCell 에 해당하는 클래스를 생성할 때 반영되어 배치의 기준을 더욱 수월하게 생성할 수 있습니다.
