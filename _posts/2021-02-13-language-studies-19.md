---
title: "Language Study - 내가 궁금해서 만든 2021 대한민국 예산 버블 다이어그램"
date: 2021-02-13
categories: LanguageStudies
tags: D3.js
---


## 1. D3.js

기본 틀은 D3 js를 사용했고, 지료는 [국회 예산 정책처 2021년도 예산안 분석](https://www.nabo.go.kr/Sub/01Report/01_02_Board.jsp?funcSUB=view&bid=19&arg_cid1=0&arg_cid2=0&arg_class_id=0&currentPage=0&pageSize=10&currentPageSUB=0&pageSizeSUB=10&key_typeSUB=&keySUB=&search_start_dateSUB=&search_end_dateSUB=&department=0&department_sub=0&etc_cate1=A&etc_cate2=&sortBy=reg_date&ascOrDesc=desc&search_key1=&etc_1=0&etc_2=1&tag_key=%EC%98%88%EC%82%B0%EB%B6%84%EC%84%9D&arg_id=7370&item_id=7370&etc_1=1&etc_2=1&name2=1)를 엑셀로 불러와 사용했다.


## 2. 결과 사진

결과 사진은 아래와 같다. 사실 전년도와 큰 차이는 없는데, 의외로 보건복지부와 교육부의 비율이 높아 좀 놀랐다.

![](https://github.com/ArkimCity/ArkimCity.github.io/blob/main/assets/images/budget2021_d3.jpg?raw=true)

## 2021 한국 예산 json

필자는 색이나 표현 등을 위해 약간의 가공을 했지만, 혹시 필요하신 분들을 위해 최대한 기본 형으로 적어놓고자 한다.

```json
{
    "name": "budget2021",
    "children": [
        {"name": "보건복지부", "size": 901536},
        {"name": "교육부", "size": 763332},
        {"name": "행정안전부", "size": 568275},
        {"name": "국토교통부", "size": 567249},
        {"name": "국방부", "size": 377458},
        {"name": "고용노동부", "size": 354808},
        {"name": "기획재정부", "size": 311637},
        {"name": "인사혁신처", "size": 213587},
        {"name": "과학기술정보통신부", "size": 176439},
        {"name": "중소벤처기업부", "size": 173493},
        {"name": "방위사업청", "size": 170642},
        {"name": "농림축산식품부", "size": 161324},
        {"name": "경찰청", "size": 119530},
        {"name": "산업통상자원부", "size": 111592},
        {"name": "환경부", "size": 110777},
        {"name": "문화체육관광부", "size": 68273},
        {"name": "해양수산부", "size": 61440},
        {"name": "국가보훈처", "size": 57866},
        {"name": "법무부", "size": 41573},
        {"name": "외교부", "size": 28432},
        {"name": "산림청", "size": 24303},
        {"name": "대법원", "size": 20605},
        {"name": "국세청", "size": 18679},
        {"name": "금융위원회", "size": 17200},
        {"name": "해양경찰청", "size": 15425},
        {"name": "통일부", "size": 14607},
        {"name": "여성가족부", "size": 11466},
        {"name": "문화재청", "size": 11241},
        {"name": "농촌진흥청", "size": 10876},
        {"name": "국가정보원", "size": 7460},
        {"name": "국회", "size": 6989},
        {"name": "국무조정실 및 국무총리비서실", "size": 6433},
        {"name": "식품의약품안전처", "size": 6044},
        {"name": "관세청", "size": 6024},
        {"name": "특허청", "size": 5237},
        {"name": "기상청", "size": 4296},
        {"name": "통계청", "size": 4161},
        {"name": "행정중심복합도시건설청", "size": 4136},
        {"name": "중앙선거관리위원회", "size": 3853},
        {"name": "새만금개발청", "size": 2833},
        {"name": "병무청", "size": 2436},
        {"name": "조달청", "size": 2241},
        {"name": "소방청", "size": 2206},
        {"name": "원자력안전위원회", "size": 1545},
        {"name": "공정거래위원회", "size": 1466},
        {"name": "감사원", "size": 1358},
        {"name": "대통령비서실 및 국가안보실", "size": 980},
        {"name": "대통령경호처", "size": 929},
        {"name": "국민권익위원회", "size": 909},
        {"name": "헌법재판소", "size": 530},
        {"name": "방송통신위원회", "size": 521},
        {"name": "법제처", "size": 412},
        {"name": "국가인권위원회", "size": 383},
        {"name": "개인정보보호위원회", "size": 365},
        {"name": "민주평화통일자문회의", "size": 326},
        {"name": "5・18민주화운동 진상규명조사위원회", "size": 102},
        {"name": "가습기살균제사건과4・16", "size": 58},
        {"name": "세월호참사 특별조사위원회", "size": 0}
    ]
}
```