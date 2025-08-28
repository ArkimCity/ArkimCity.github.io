---
layout: post
title:  "Can we determine the optimal building axis from the site at a glance?"
# author: john
categories: [ Automation ]
tags: [ CNN, 건축설계, AI, 딥러닝 ]  # red, yellow
thumbnail: assets/images/find-optimal-axis-of-building/result_analysis.png
description: "CNN을 활용한 건물 최적 축 방향 예측 연구"
featured: true
hidden: false
# rating: 4.5
beforetoc: "목차"
# toc: true
---

## 요약
이 페이지는 건물 설계의 초반 단계에 중요한 부분 중 하나인 건물의 '축'을 찾는 문제에 대해 다룹니다. 이를 해결하기 위해, 기하학적 데이터를 활용하는 방법 중 하나인 CNN(Convolutional Neural Network)을 사용하고 있습니다. 본 페이지에서는 건물과 필지 데이터를 상세히 분석하고, 이를 바탕으로 CNN 모델을 구현하고 학습시킨 결과를 보여줍니다. 실험 결과, 모델은 완전한 랜덤에 비해 약 2배 정도의 정확도를 보였지만, 도형이 복잡할수록 정확도가 떨어진다는 한계점을 가지고 있습니다. 이에 따라 다른 방법들에 대한 시도와 개선이 필요하다는 결론을 내리고 있습니다.

---

## 1. 문제

설계 자동화에 있어서 초반 단계에서 중요한 부분 중에 하나는 설계 결과에 해당한다고 부를 수 있는 건물의 '축'을 찾는 일입니다.

축의 방향을 어느 한가지 경우로 고정하는 것은 리스크를 동반함으로, 스페이스워크를 포함해 다른 제품들에서도 축의 방향 후보를 몇가지 방법으로 추정해 해당 후보군을 테스트하는 방법을 사용할 것입니다. 이는 경우의 수를 늘리는 대표적인 장애물이고, 이를 개선하기 위한 방법을 여러 방면으로 연구해볼 필요성이 존재합니다.

## 2. 목적

모든 필지에 대해 AI를 통해 단 한가지의 정답을 단번에 추론해내는 것은 어려울 수 있습니다. 하지만 예를 들어 4가지 경우의 수를 테스트 해보야 할 경우에 대해 2가지만 테스트해보는 정도로 필요한 경우의 수를 감소시키는 것으로도 연산 시간 최적화와 같은 정도의 임팩트를 줄 수 있을 것으로 기대합니다.

## 3. 방법

### 3.1 CNN 모델 구조

Geometric data를 학습에 사용하는 방법은 여러가지 존재합니다. 해당 페이지에서는 geometry 데이터를 다루는 대표적인 방법 중 하나인 CNN을 사용합니다. regression 문제에 적합한 MSE(각 차이만큼 제곱 후 평균을 내리는) 손실함수와 Adam optimizer를 사용합니다.

![CNN 모델의 구조]({{ site.baseurl }}/assets/images/find-optimal-axis-of-building/cnn_model_structure.png)

**유사 혹은 관련 작업:**
- Convolutional Neural Networks Adapted for Regression Tasks: Predicting the Orientation of Straight Arrows on Marked Road Pavement Using Deep Learning and Rectified Orthophotography

### 3.2 모델 구조 상세

각 레이어를 지나며 (1024개의 학습 input 데이터) 다음과 같은 shape을 같습니다:

- `[1024, 1, 32, 32]` - 인풋 데이터의 모양 각 1개의 32 x 32 이미지
- `[1024, 16, 32, 32]` - 각 16개로 convolution
- `[1024, 16, 16, 16]` - 각 16개의 data를 가볍게 해주는 목적으로 pool
- `[1024, 32, 16, 16]` - from 16 to 32로 convolution
- `[1024, 32, 8, 8]` - 16 to 8로 pool
- `[1024, 2048]` - 32 x 8 x 8 shape를 flatten
- `[1024, 128]` - 2048 to 128 fully connected layer 1
- `[1024, 2]` - 128 to 2 fully connected layer 2

마지막의 fully connected layer는 2차원으로 출력해 x,y 벡터의 형태로 결과를 생성하도록 의도했습니다.

```python
import torch
import torch.nn as nn

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(32 * 8 * 8, 128)
        self.fc2 = nn.Linear(128, 2)  # 2차원으로 출력 (가장 지배적인 축의 방향)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.max_pool2d(x, kernel_size=2, stride=2)
        x = torch.relu(self.conv2(x))
        x = torch.max_pool2d(x, kernel_size=2, stride=2)
        x = x.view(-1, 32 * 8 * 8)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x
```

### 3.3 데이터 처리

**Input 데이터:**
- 필지 도형 데이터는 geometry를 32 x 32의 pixel tensor로 구성해 사용합니다
- 각 값은 0 or 1입니다

![입력 데이터 예시]({{ site.baseurl }}/assets/images/find-optimal-axis-of-building/input_data_example.png)

**Output 데이터:**
- 축 벡터는 해당 필지 위의 건물의 shapely의 minimum_rotated_rectangle의 x,y 모두 양의 방향으로 해당하는 벡터를 사용합니다
- vector의 길이는 각 도형을 32 x 32로 표현할 수 있는 크기로 노말라이즈된 것을 사용합니다

![출력 데이터 예시]({{ site.baseurl }}/assets/images/find-optimal-axis-of-building/output_data_example.png)

### 3.4 데이터셋

**학습 데이터:**
- 서울의 일부 지역에 해당합니다
- 건물과 필지 데이터 모두 매치되어있는 1024개의 건물 및 필지 데이터를 사용합니다

**테스트 데이터:**
- 서울의 일부 지역에 해당합니다
- 건물과 필지 데이터 모두 매치되어있는 64개의 건물 및 필지 데이터를 사용합니다
- 학습 데이터와는 중복되지 않습니다

![데이터셋 예시]({{ site.baseurl }}/assets/images/find-optimal-axis-of-building/dataset_example.png)

## 4. 실행 결과

### 4.1 학습 과정

2000 epochs로 학습을 진행했습니다. 약 1000 epochs 이후로는 의미있는 수준의 개선이 이루어지지는 않았습니다.

![학습 과정]({{ site.baseurl }}/assets/images/find-optimal-axis-of-building/learning_process.gif)

### 4.2 테스트 결과

초록색은 label 생성과 같은 로직으로 만들어진 축, 빨간색은 output 결과입니다.

![테스트 결과]({{ site.baseurl }}/assets/images/find-optimal-axis-of-building/test_result.png)

**정확도 분석:**
비교는 64개의 케이스로 랜덤일 경우와 label 값과 동일한 방식으로 생성한 결과값, 그리고 추론으로 생성한 결과값의 세가지 경우를 이용했습니다. (90도 차이는 동일한 것으로 가정)

- 로직 생성값과 2도 내에 들어오는 경우
  - random → 4개
  - 모델 결과 → 9개
- 로직 생성값과 5도 내에 들어오는 경우
  - random → 9개
  - 모델 결과 → 17개
- 로직 생성값과 10도 내에 들어오는 경우
  - random → 17개
  - 모델 결과 → 35개

![결과 분석]({{ site.baseurl }}/assets/images/find-optimal-axis-of-building/result_analysis.png)

## 5. 결론

### 5.1 평가

- 완전한 랜덤에 비해 약 2배 정도의 정확도를 보여주었습니다. (64 x 64로 테스트 했을 경우에도 유사한 결과)
- 하지만 도형이 단순할 수록 정확도가 높아지는 경향을 보이며, 복잡한 도형에 적용하는 것에 의의가 있는 만큼 실질적으로 적용하기에는 개선이 필요해보입니다.

### 5.2 한계 및 향후 연구 방향

**결론 및 한계:**
- RNN (LSTM, GRU), Transformer, Graph 역시 시퀀스 데이터를 학습하는데 사용되는 대표적인 방법으로 알려져 있습니다. 이후 도형 및 평면의 데이터를 학습하는 실험에 있어 더 유효한 방법이 될 수 있어 시도해보고자 합니다.
- 마치 classification처럼 각도를 output 및 label로 설정하는 방법도 있을 수 있어 보입니다.
- 필지 유형을 분리해본다.

### 5.3 코드 및 참고 자료

위 내용은 아래에서 확인하실 수 있습니다:

[GitHub Repository](https://github.com/ArkimCity/find-optimal-axis-of-a-building/blob/90f86e2309027316c6fda67bde85c5e6342f1a42/predict_main_axis_vector_from_site.py)

---

**참고 자료:**
1. CNN 설명 - [https://rubber-tree.tistory.com/116](https://rubber-tree.tistory.com/116)
2. [https://medium.com/@polanitzer/building-a-convolutional-neural-network-in-python-predict-digits-from-gray-scale-images-of-550d79b358b](https://medium.com/@polanitzer/building-a-convolutional-neural-network-in-python-predict-digits-from-gray-scale-images-of-550d79b358b)
3. [https://www.mdpi.com/2079-9292/12/18/3980](https://www.mdpi.com/2079-9292/12/18/3980)
