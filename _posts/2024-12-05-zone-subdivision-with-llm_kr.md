---
layout: post
title:  "Zone Subdivision With LLM - Expanded Self Feedback Cycle"
thumbnail: /assets/images/zone-subdivision-with-llm/Flowchart.png
# tag: "
#     #LLM
#     #Generative AI
#     #PoC
#     #Research
# "
---

## Introduction
이 글에서는 반복적인 사이클을 통해 결과의 품질을 향상시키기 위해 대규모 언어 모델(LLM)을 피드백 루프에서 활용하는 방법을 살펴봅니다. LLM이 제공하는 초기 직관적 결과를 개선하는 것이 목표이며, 이는 LLM 내부의 피드백 메커니즘을 넘어서 LLM 외부의 최적화를 포함한 피드백 사이클을 통해 이루어집니다.

<hr>

## Concept

- LLM은 자체적으로도 피드백을 통해 결과를 개선할 수 있으며, 이는 널리 활용되고 있습니다. 그러나 사용자의 단일 요청만으로 LLM이 제공하는 직관적인 결과가 항상 완전하다고 기대하기는 어렵습니다. 따라서, LLM이 제공한 초기 결과를 다시 요청하여 피드백을 주고받음으로써 답변의 질을 향상시키는 것을 목표로 합니다. 이는 LLM 내부의 피드백에만 의존하는 것을 넘어, LLM과 알고리즘을 포함한 더 큰 사이클에서의 피드백을 통해 결과를 지속적으로 개선할 수 있는지를 확인하는 과정입니다.


- **Self-feedback outside LLM API In This Work:**
  <div style="width: 80vw; max-width: 1000px; margin: 0 auto; display: flex; flex-wrap: wrap; justify-content: center;">
      <img src="{{ '/assets/images/zone-subdivision-with-llm/Flowchart.png' | relative_url }}" alt="Flowchart" style="max-width: 100%;">
  </div>

- **Self-feedback inside LLM API examples:**
  <div style="width: 80vw; max-width: 500px; margin: 0 auto; display: flex; flex-wrap: wrap; justify-content: center;">
      <img src="{{ '/assets/images/zone-subdivision-with-llm/llm_self_feedback_examples.png' | relative_url }}" alt="llm_self_feedback_examples" style="max-width: 100%;">
  </div>

- **LLM을 사용하는 의의**
    - 사용자의 모호한 니즈와 알고리즘의 구체적 기준 사이의 연결 매개체
    - **사이클의 결과를 이해하고, 다음 사이클에 그 결과를 반영해 답변을 개선해가는 과정**

<hr>

## Premises
- **Two Main Components:**
    - **LLM:**
        - 직관적 선택에 사용
        - 사용자의 비교적 모호한 의사를 LLM 은 직관적이고 개략적인 결정들을 만들 수 있습니다.
            - `사용자` - `LLM` - `optimizer` 순으로의 구체화 순서 과정에서,
            - `사용자` - `optimizer` 사이의 갭을 매꿔주는 존재로 사용됩니다.
  - **Heuristic Optimizer (GA):**
        - 상대적으로 구체적인 최적화에 사용

- **Use Cycles:**
    - 사이클의 실행을 반복함으로, 의도에 가까운 결과에 스스로 접근하고자 하는 구조를 만들고자 합니다.

<hr>

## Details

1. **Parameter Conversion:**
    - LLM 과 structured out 을 사용하면, 직관적으로 선택할 내용들을 명확한 파라미터 입력으로 변환해 알고리즘 입력의 input 으로 사용할 수 있습니다.
    - Zone grid 및 grid size 에 따른 각 patch 사이즈를 조절하기 위해, 추가적인 subdivision 개수를 얼마나 받아야 할지 재 요청하며 조정

        ```jsx
        number_additional_subdivision_x: int
        number_additional_subdivision_y: int
        ```

    - 각 용도에 대해 boundary 에 가깝게 위치하는 것을 우선할지 prompt 를 바탕으로 답변을 요구합니다.

        ```jsx
        place_rest_close_to_boundary: bool
        place_office_close_to_boundary: bool
        place_lobby_close_to_boundary: bool
        place_coworking_close_to_boundary: bool
        ```

    - 각 용도가 서로 옆 patch 와 다른 용도이길 원하는 비율에 대해 물어봅니다.

        ```jsx
        percentage_of_mixture: number
        ```

    - 각 용도가 몇퍼센트 정도 차지해야 할 지 물어봅니다.

        ```jsx
        office: number
        coworking: number
        lobby: number
        rest: number
        ```
<br>
<br>

2. **Optimization Based on LLM Responses:**
    - llm 에게서 돌아온 답변을 토대로 이를 최적화 기준으로 사용하고, 이는 사용자가 가지고 있던 생각들을 구체적인 기준으로 변환하는 과정입니다.

3. **Incorporate Optimization Results into Next Cycle:**
    - 최적화를 통해 나온 결과는 다시 llm 에게 다음 사이클의 질문을 할 때 참고사항으로 삽입해줍니다.
    - 이를 통해 [llm answer - optimize results with the answer] 사이클을 복수 횟수 돌리는 것의 의의를 강화하고 결과를 개선시킵니다.

4. **Cycle Structure:**
    - **한 사이클**
        - **1차 [llm answer - optimize results with the answer]**
            - zone 용도를 Optimizer 하기 전, 입력받은 prompt를 기준으로 subdivision 기준을 LLM에게 물어봅니다.
            - LLM 은 subdivision 의 개략적인 결정을 해주고, optimize 는 구체적인 결과를 생성합니다.
        - **2차  [llm answer - optimize results with the answer]**
            - 입력받은 prompt 를 기준으로, zone 들의 config 관련 직관적인 대답을 LLM에게 요구합니다.
            - LLM 은 zone placement 관련된 직관적인 결정을 해주고, optimize 는 이를 구체적인 결과로 생성합니다.
    - **두번째 사이클 이후**
        - 두번째 사이클 이후에서는, 직전의 LLM 이 돌려줬던 답변과 함께 실제 optimize 결과를 알려주며 답변의 개선을 직접적으로 요구합니다. 사이클을 반복하며 LLM 결과는 업데이트 되고, 이에 따른 optimize 결과도 개선되어갑니다.

<hr>

## Test results

### case 1

- **Prompt:**

    ```jsx
    대공간에서 다같이 한 목표를 위해 가운데 쪽에 office 공간들이 모여있어.
    그밖의 공간들은 boundary 에 가까운 곳에 배치하고싶어.
    ```

- **GIFs:**

    <div style="width: 80vw; max-width: 500px; margin: 0 auto; display: flex; flex-wrap: wrap; justify-content: center;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/0_1_zone_subdivision.gif' | relative_url }}" alt="0_1_zone_subdivision.gif" style="max-width: 49%;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/0_2_zone_placement.gif' | relative_url }}" alt="0_2_zone_placement.if" style="max-width: 49%;">

        <img src="{{ '/assets/images/zone-subdivision-with-llm/1_1_zone_subdivision.gif' | relative_url }}" alt="1_1_zone_subdivision.if" style="max-width: 49%;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/1_2_zone_placement.gif' | relative_url }}" alt="1_2_zone_placement.if" style="max-width: 49%;">

        <img src="{{ '/assets/images/zone-subdivision-with-llm/2_1_zone_subdivision.gif' | relative_url }}" alt="2_1_zone_subdivision.if" style="max-width: 49%;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/2_2_zone_placement.gif' | relative_url }}" alt="2_2_zone_placement.if" style="max-width: 49%;">

        <img src="{{ '/assets/images/zone-subdivision-with-llm/3_1_zone_subdivision.gif' | relative_url }}" alt="3_1_zone_subdivision.if" style="max-width: 49%;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/3_2_zone_placement.gif' | relative_url }}" alt="3_2_zone_placement.if" style="max-width: 49%;">

        <img src="{{ '/assets/images/zone-subdivision-with-llm/4_1_zone_subdivision.gif' | relative_url }}" alt="4_1_zone_subdivision.if" style="max-width: 49%;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/4_2_zone_placement.gif' | relative_url }}" alt="4_2_zone_placement.if" style="max-width: 49%;">
    </div>


### case 2

- **Prompt:**

    ```jsx
    한 팀에는 약 5명 내외로 사일로 한 팀들을 목표로 하고있어.
    때문에 허느 한 용도가 몰려있지 않은 섞인 공간들을 원해.
    ```

- **GIFs:**

    <div style="width: 80vw; max-width: 500px; margin: 0 auto; display: flex; flex-wrap: wrap; justify-content: center;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/0_1_zone_subdivision 1.gif' | relative_url }}" alt="0_1_zone_subdivision 1.if" style="max-width: 49%;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/0_2_zone_placement 1.gif' | relative_url }}" alt="0_2_zone_placement 1.if" style="max-width: 49%;">

        <img src="{{ '/assets/images/zone-subdivision-with-llm/1_1_zone_subdivision 1.gif' | relative_url }}" alt="1_1_zone_subdivision 1.if" style="max-width: 49%;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/1_2_zone_placement 1.gif' | relative_url }}" alt="1_2_zone_placement 1.if" style="max-width: 49%;">

        <img src="{{ '/assets/images/zone-subdivision-with-llm/2_1_zone_subdivision 1.gif' | relative_url }}" alt="2_1_zone_subdivision 1.if" style="max-width: 49%;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/2_2_zone_placement 1.gif' | relative_url }}" alt="2_2_zone_placement 1.if" style="max-width: 49%;">

        <img src="{{ '/assets/images/zone-subdivision-with-llm/3_1_zone_subdivision 1.gif' | relative_url }}" alt="3_1_zone_subdivision 1.if" style="max-width: 49%;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/3_2_zone_placement 1.gif' | relative_url }}" alt="3_2_zone_placement 1.if" style="max-width: 49%;">

        <img src="{{ '/assets/images/zone-subdivision-with-llm/4_1_zone_subdivision 1.gif' | relative_url }}" alt="4_1_zone_subdivision 1.if" style="max-width: 49%;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/4_2_zone_placement 1.gif' | relative_url }}" alt="4_2_zone_placement 1.if" style="max-width: 49%;">
    </div>


### case 3

- **Prompt:**

    ```jsx
    office 가 채광을 받기 쉽도록 boundary 에 가까운 곳에 배치를 우선하고,
    다른 공간들은 안쪽에 배치하고싶어.
    ```

- **GIFs:**

    <div style="width: 80vw; max-width: 500px; margin: 0 auto; display: flex; flex-wrap: wrap; justify-content: center;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/0_1_zone_subdivision 2.gif' | relative_url }}" alt="0_1_zone_subdivision 2.if" style="max-width: 49%;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/0_2_zone_placement 2.gif' | relative_url }}" alt="0_2_zone_placement 2.if" style="max-width: 49%;">

        <img src="{{ '/assets/images/zone-subdivision-with-llm/1_1_zone_subdivision 2.gif' | relative_url }}" alt="1_1_zone_subdivision 2.if" style="max-width: 49%;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/1_2_zone_placement 2.gif' | relative_url }}" alt="1_2_zone_placement 2.if" style="max-width: 49%;">

        <img src="{{ '/assets/images/zone-subdivision-with-llm/2_1_zone_subdivision 2.gif' | relative_url }}" alt="2_1_zone_subdivision 2.if" style="max-width: 49%;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/2_2_zone_placement 2.gif' | relative_url }}" alt="2_2_zone_placement 2.if" style="max-width: 49%;">

        <img src="{{ '/assets/images/zone-subdivision-with-llm/3_1_zone_subdivision 2.gif' | relative_url }}" alt="3_1_zone_subdivision 2.if" style="max-width: 49%;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/3_2_zone_placement 2.gif' | relative_url }}" alt="3_2_zone_placement 2.if" style="max-width: 49%;">

        <img src="{{ '/assets/images/zone-subdivision-with-llm/4_1_zone_subdivision 2.gif' | relative_url }}" alt="4_1_zone_subdivision 2.if" style="max-width: 49%;">
        <img src="{{ '/assets/images/zone-subdivision-with-llm/4_2_zone_placement 2.gif' | relative_url }}" alt="4_2_zone_placement 2.if" style="max-width: 49%;">
    </div>

<hr>

## Conclusion
- llm의 response raw data 만으로 사용자에게 전달할 데이터가 완성되기 어려운 api에 대해, Self Feedback 을 llm 이 아닌 llm 요청 및 최적화와 후처리까지 합친 범위로 확장함으로 최종 결과의 개선을 도모하고자 하는 작업입니다.
cycle 이 반복될수록 의도된 결과에 가까워지는 것을 확인할 수 있었으며, 직관적인 초기값을 llm 에게 의지하는 작업에서 초기값의 불완전할 수 있는 가능성을 감소시킬 수 있습니다.
