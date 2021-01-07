---
title: "Language Study - D3.js 맛보기"
date: 2021-01-06
categories: LanguageStudies
tags: D3.js javascript
---


## 1. D3.js?

데이터 시각화에서 가장 유명한 라이브러리 중에 하나로 다짜고짜 완성 예시부터 보여드리겠습니다.

![계층 사진](https://github.com/ArkimCity/ArkimCity.github.io/blob/main/assets/images/d3_h_s.PNG?raw=true)

## 2. index.html

꼭 이렇게 해야하는 건 아니지만, 인터넷에서 예제를 찾을 때 저와 같은 고생을 하지 않도록 이렇게 보여드리겠습니다.

기본 뼈대가 되는 index.html은 요로코롬 생겼다.
여기서 d3js.org가 가지고 있는 d3.v4.min.js 자바스크립트 파일을 로드하고,
(<script src="//d3js.org/d3.v4.min.js"></script>)

아래에 쓸 index.js 자바스크립트 파일을 로드하는 것으로 기본 틀은 완성된다.

style 태그에 있는 내용들은 여기에서 사용할 노드들의 생김새를 결정해주는 문장이다.

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    .node circle {
      fill: #999;
    }
    .node text {
      font: 10px sans-serif;
    }
    .node--internal circle {
      fill: #555;
    }
    .node--internal text {
      text-shadow: 0 1px 0 #fff, 0 -1px 0 #fff, 1px 0 0 #fff, -1px 0 0 #fff;
    }
    .link {
      fill: none;
      stroke: #555;
      stroke-opacity: 0.4;
      stroke-width: 1.5px;
    }
  </style>
</head>
<body>
  <script src="//d3js.org/d3.v4.min.js"></script>
  <script src="index.js"></script>
</body>
</html>
```

## 3. index.js

index.js의 내용은 아래와 같다. 

```javascript
const width = 960;
const height = 900;

const svg = d3
    .select("body")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

const g = svg
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + (height / 2 + 20) + ")");

const cluster = d3.cluster().size([360, width / 2 - 120]);

d3.json("dataResCopy.json", (error, data) => {
    if (error) throw error;

    const root = d3
        .hierarchy(data)
        .eachBefore(d => {
            d.data.id = (d.parent ? d.parent.data.id + "." : "") + d.data.name;
        })
        .sort((a, b) => {
            return a.height - b.height || a.data.id.localeCompare(b.data.id);
        });

    cluster(root);

    const link = g
        .selectAll(".link")
        .data(root.descendants().slice(1))
        .enter()
        .append("path")
        .attr("class", "link")
        .attr("d", d => {
            return (
                "M" +
        project(d.x, d.y) +
        "C" +
        project(d.x, (d.y + d.parent.y) / 2) +
        " " +
        project(d.parent.x, (d.y + d.parent.y) / 2) +
        " " +
        project(d.parent.x, d.parent.y)
            );
        });

    const node = g
        .selectAll(".node")
        .data(root.descendants())
        .enter()
        .append("g")
        .attr("class", d => {
            return "node" + (d.children ? " node--internal" : " node--leaf");
        })
        .attr("transform", d => "translate(" + project(d.x, d.y) + ")");

    node.append("circle").attr("r", 2.5);

    node
        .append("text")
        .attr("dy", "0.31em")
        .attr("x", d => (d.x < 180 === !d.children ? 6 : -6))
        .style("text-anchor", d => (d.x < 180 === !d.children ? "start" : "end"))
        .attr("transform", d => "rotate(" + (d.x < 180 ? d.x - 90 : d.x + 90) + ")")
        .text(d => d.data.id.substring(d.data.id.lastIndexOf(".") + 1));
});

function project(x, y) {
    const angle = (x - 90) / 180 * Math.PI;
    const radius = y;
    return [radius * Math.cos(angle), radius * Math.sin(angle)];
}
```

## 4. json 파일(여기선 dataRes.json)

D3.js heirarchy에서 중요한 데이터 키 값은 name 과 children 이다. 

아래에서 처럼 name 과 children을 제외한 데이터가 혼재되어있어도 javascript object 에서 키값으로 데이터를 받는 데는 문제가 없기 때문에 괜찮다.

children 에 해당하는 array에는 마찬가지로 각 name 과 children(선택사항) 을 가지고있는 자료들이 들어있다. 이 방식의 반복이다.

```json
{
    "name": "역명",
    "DESCRIPTION": {
        "USE_DT": "사용일자",
        "name": "역명",
        "WORK_DT": "등록일자",
        "size": "승차총승객수",
        "line_name": "호선명",
        "ALIGHT_PASGR_NUM": "하차총승객수"
    },
    "children": [
        {
            "name": "우이신설선",
            "children": [
                {
                    "line_num": "우이신설선",
                    "ride_pasgr_num": 2661,
                    "alight_pasgr_num": 2498,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "4.19민주묘지"
                },
                {
                    "line_num": "우이신설선",
                    "ride_pasgr_num": 3889,
                    "alight_pasgr_num": 3632,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "가오리"
                }
            ]
        },
        {
            "name": "경원선",
            "children": [
                {
                    "line_num": "경원선",
                    "ride_pasgr_num": 6415,
                    "alight_pasgr_num": 6082,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "가능"
                },
                {
                    "line_num": "경원선",
                    "ride_pasgr_num": 8222,
                    "alight_pasgr_num": 7609,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "광운대"
                }
            ]
        },
        {
            "name": "8호선",
            "children": [
                {
                    "line_num": "8호선",
                    "ride_pasgr_num": 8056,
                    "alight_pasgr_num": 9185,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "가락시장"
                },
                {
                    "line_num": "8호선",
                    "ride_pasgr_num": 10698,
                    "alight_pasgr_num": 10761,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "강동구청"
                },
                {
                    "line_num": "8호선",
                    "ride_pasgr_num": 13071,
                    "alight_pasgr_num": 11044,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "남한산성입구(성남법원.검찰청)"
                }
            ]
        },
        {
            "name": "3호선",
            "children": [
                {
                    "line_num": "3호선",
                    "ride_pasgr_num": 9723,
                    "alight_pasgr_num": 9491,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "가락시장"
                },
                {
                    "line_num": "3호선",
                    "ride_pasgr_num": 19602,
                    "alight_pasgr_num": 19822,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "경복궁(정부서울청사)"
                },
                {
                    "line_num": "3호선",
                    "ride_pasgr_num": 7736,
                    "alight_pasgr_num": 7680,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "경찰병원"
                },
                {
                    "line_num": "3호선",
                    "ride_pasgr_num": 48088,
                    "alight_pasgr_num": 51047,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "고속터미널"
                },
                {
                    "line_num": "3호선",
                    "ride_pasgr_num": 14687,
                    "alight_pasgr_num": 9692,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "교대(법원.검찰청)"
                },
                {
                    "line_num": "3호선",
                    "ride_pasgr_num": 21486,
                    "alight_pasgr_num": 19967,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "구파발"
                },
                {
                    "line_num": "3호선",
                    "ride_pasgr_num": 8766,
                    "alight_pasgr_num": 7885,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "금호"
                },
                {
                    "line_num": "3호선",
                    "ride_pasgr_num": 32344,
                    "alight_pasgr_num": 34074,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "남부터미널(예술의전당)"
                },
                {
                    "line_num": "3호선",
                    "ride_pasgr_num": 15306,
                    "alight_pasgr_num": 12893,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "녹번"
                }
            ]
        },
        {
            "name": "7호선",
            "children": [
                {
                    "line_num": "7호선",
                    "ride_pasgr_num": 44574,
                    "alight_pasgr_num": 45217,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "가산디지털단지"
                },
                {
                    "line_num": "7호선",
                    "ride_pasgr_num": 16050,
                    "alight_pasgr_num": 18435,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "강남구청"
                },
                {
                    "line_num": "7호선",
                    "ride_pasgr_num": 12579,
                    "alight_pasgr_num": 13721,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "건대입구"
                },
                {
                    "line_num": "7호선",
                    "ride_pasgr_num": 17895,
                    "alight_pasgr_num": 14853,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "고속터미널"
                },
                {
                    "line_num": "7호선",
                    "ride_pasgr_num": 12136,
                    "alight_pasgr_num": 11831,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "공릉(서울과학기술대)"
                },
                {
                    "line_num": "7호선",
                    "ride_pasgr_num": 23299,
                    "alight_pasgr_num": 22842,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "광명사거리"
                },
                {
                    "line_num": "7호선",
                    "ride_pasgr_num": 14748,
                    "alight_pasgr_num": 11419,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "군자(능동)"
                },
                {
                    "line_num": "7호선",
                    "ride_pasgr_num": 8704,
                    "alight_pasgr_num": 9087,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "굴포천"
                },
                {
                    "line_num": "7호선",
                    "ride_pasgr_num": 7615,
                    "alight_pasgr_num": 7047,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "까치울"
                },
                {
                    "line_num": "7호선",
                    "ride_pasgr_num": 15479,
                    "alight_pasgr_num": 16375,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "남구로"
                },
                {
                    "line_num": "7호선",
                    "ride_pasgr_num": 11742,
                    "alight_pasgr_num": 10177,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "남성"
                },
                {
                    "line_num": "7호선",
                    "ride_pasgr_num": 15246,
                    "alight_pasgr_num": 15450,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "내방"
                },
                {
                    "line_num": "7호선",
                    "ride_pasgr_num": 20891,
                    "alight_pasgr_num": 23384,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "노원"
                }
            ]
        },
        {
            "name": "경부선",
            "children": [
                {
                    "line_num": "경부선",
                    "ride_pasgr_num": 17423,
                    "alight_pasgr_num": 19838,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "가산디지털단지"
                },
                {
                    "line_num": "경부선",
                    "ride_pasgr_num": 7049,
                    "alight_pasgr_num": 6605,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "관악"
                },
                {
                    "line_num": "경부선",
                    "ride_pasgr_num": 3428,
                    "alight_pasgr_num": 2974,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "광명"
                },
                {
                    "line_num": "경부선",
                    "ride_pasgr_num": 17967,
                    "alight_pasgr_num": 18379,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "구로"
                },
                {
                    "line_num": "경부선",
                    "ride_pasgr_num": 7145,
                    "alight_pasgr_num": 6883,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "군포"
                },
                {
                    "line_num": "경부선",
                    "ride_pasgr_num": 25136,
                    "alight_pasgr_num": 25098,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "금정"
                },
                {
                    "line_num": "경부선",
                    "ride_pasgr_num": 11614,
                    "alight_pasgr_num": 11316,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "금천구청"
                },
                {
                    "line_num": "경부선",
                    "ride_pasgr_num": 9991,
                    "alight_pasgr_num": 10590,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "남영"
                },
                {
                    "line_num": "경부선",
                    "ride_pasgr_num": 9940,
                    "alight_pasgr_num": 9176,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "노량진"
                }
            ]
        },
        {
            "name": "9호선",
            "children": [
                {
                    "line_num": "9호선",
                    "ride_pasgr_num": 22493,
                    "alight_pasgr_num": 21156,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "가양"
                },
                {
                    "line_num": "9호선",
                    "ride_pasgr_num": 2822,
                    "alight_pasgr_num": 2004,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "개화"
                },
                {
                    "line_num": "9호선",
                    "ride_pasgr_num": 14137,
                    "alight_pasgr_num": 18900,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "고속터미널"
                },
                {
                    "line_num": "9호선",
                    "ride_pasgr_num": 2862,
                    "alight_pasgr_num": 2969,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "공항시장"
                },
                {
                    "line_num": "9호선",
                    "ride_pasgr_num": 3345,
                    "alight_pasgr_num": 3571,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "구반포"
                },
                {
                    "line_num": "9호선",
                    "ride_pasgr_num": 19065,
                    "alight_pasgr_num": 19280,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "국회의사당"
                },
                {
                    "line_num": "9호선",
                    "ride_pasgr_num": 8679,
                    "alight_pasgr_num": 13903,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "김포공항"
                },
                {
                    "line_num": "9호선",
                    "ride_pasgr_num": 5447,
                    "alight_pasgr_num": 4138,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "노들"
                },
                {
                    "line_num": "9호선",
                    "ride_pasgr_num": 29521,
                    "alight_pasgr_num": 29381,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "노량진"
                },
                {
                    "line_num": "9호선",
                    "ride_pasgr_num": 7273,
                    "alight_pasgr_num": 7721,
                    "work_dt": "20200703",
                    "use_dt": "20200630",
                    "name": "흑석(중앙대입구)"
                }
            ]
        },
        {
            "name": "경의선",
            "children": [
                {
                    "line_num": "경의선",
                    "ride_pasgr_num": 5769,
                    "alight_pasgr_num": 5070,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "가좌"
                },
                {
                    "line_num": "경의선",
                    "ride_pasgr_num": 3117,
                    "alight_pasgr_num": 2508,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "강매"
                },
                {
                    "line_num": "경의선",
                    "ride_pasgr_num": 609,
                    "alight_pasgr_num": 638,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "곡산"
                },
                {
                    "line_num": "경의선",
                    "ride_pasgr_num": 3688,
                    "alight_pasgr_num": 3343,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "공덕"
                },
                {
                    "line_num": "경의선",
                    "ride_pasgr_num": 4629,
                    "alight_pasgr_num": 4475,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "금릉"
                },
                {
                    "line_num": "경의선",
                    "ride_pasgr_num": 6398,
                    "alight_pasgr_num": 6218,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "금촌"
                }
            ]
        },
        {
            "name": "분당선",
            "children": [
                {
                    "line_num": "분당선",
                    "ride_pasgr_num": 5451,
                    "alight_pasgr_num": 6032,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "가천대"
                },
                {
                    "line_num": "분당선",
                    "ride_pasgr_num": 9911,
                    "alight_pasgr_num": 11336,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "강남구청"
                },
                {
                    "line_num": "분당선",
                    "ride_pasgr_num": 3835,
                    "alight_pasgr_num": 3948,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "개포동"
                },
                {
                    "line_num": "분당선",
                    "ride_pasgr_num": 1742,
                    "alight_pasgr_num": 1543,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "구룡"
                },
                {
                    "line_num": "분당선",
                    "ride_pasgr_num": 4892,
                    "alight_pasgr_num": 4916,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "구성"
                },
                {
                    "line_num": "분당선",
                    "ride_pasgr_num": 9412,
                    "alight_pasgr_num": 8801,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "기흥"
                }
            ]
        },
        {
            "name": "경춘선",
            "children": [
                {
                    "line_num": "경춘선",
                    "ride_pasgr_num": 1709,
                    "alight_pasgr_num": 1873,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "가평"
                },
                {
                    "line_num": "경춘선",
                    "ride_pasgr_num": 3003,
                    "alight_pasgr_num": 2546,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "갈매"
                },
                {
                    "line_num": "경춘선",
                    "ride_pasgr_num": 392,
                    "alight_pasgr_num": 438,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "강촌"
                },
                {
                    "line_num": "경춘선",
                    "ride_pasgr_num": 150,
                    "alight_pasgr_num": 137,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "굴봉산"
                },
                {
                    "line_num": "경춘선",
                    "ride_pasgr_num": 1488,
                    "alight_pasgr_num": 1417,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "금곡"
                },
                {
                    "line_num": "경춘선",
                    "ride_pasgr_num": 226,
                    "alight_pasgr_num": 238,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "김유정"
                },
                {
                    "line_num": "경춘선",
                    "ride_pasgr_num": 2733,
                    "alight_pasgr_num": 2984,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "남춘천"
                }
            ]
        },
        {
            "name": "경인선",
            "children": [
                {
                    "line_num": "경인선",
                    "ride_pasgr_num": 5881,
                    "alight_pasgr_num": 5544,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "간석"
                },
                {
                    "line_num": "경인선",
                    "ride_pasgr_num": 21819,
                    "alight_pasgr_num": 21759,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "개봉"
                },
                {
                    "line_num": "경인선",
                    "ride_pasgr_num": 7335,
                    "alight_pasgr_num": 7524,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "구일"
                }
            ]
        },
        {
            "name": "2호선",
            "children": [
                {
                    "line_num": "2호선",
                    "ride_pasgr_num": 98692,
                    "alight_pasgr_num": 104043,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "강남"
                },
                {
                    "line_num": "2호선",
                    "ride_pasgr_num": 35322,
                    "alight_pasgr_num": 35490,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "강변(동서울터미널)"
                },
                {
                    "line_num": "2호선",
                    "ride_pasgr_num": 37814,
                    "alight_pasgr_num": 43208,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "건대입구"
                },
                {
                    "line_num": "2호선",
                    "ride_pasgr_num": 35034,
                    "alight_pasgr_num": 40248,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "교대(법원.검찰청)"
                },
                {
                    "line_num": "2호선",
                    "ride_pasgr_num": 64341,
                    "alight_pasgr_num": 63608,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "구로디지털단지"
                },
                {
                    "line_num": "2호선",
                    "ride_pasgr_num": 24571,
                    "alight_pasgr_num": 23244,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "구의(광진구청)"
                },
                {
                    "line_num": "2호선",
                    "ride_pasgr_num": 29573,
                    "alight_pasgr_num": 26632,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "낙성대(강감찬)"
                }
            ]
        },
        {
            "name": "5호선",
            "children": [
                {
                    "line_num": "5호선",
                    "ride_pasgr_num": 21380,
                    "alight_pasgr_num": 18550,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "강동"
                },
                {
                    "line_num": "5호선",
                    "ride_pasgr_num": 6760,
                    "alight_pasgr_num": 6650,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "개롱"
                },
                {
                    "line_num": "5호선",
                    "ride_pasgr_num": 5387,
                    "alight_pasgr_num": 4928,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "개화산"
                },
                {
                    "line_num": "5호선",
                    "ride_pasgr_num": 7919,
                    "alight_pasgr_num": 7352,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "거여"
                },
                {
                    "line_num": "5호선",
                    "ride_pasgr_num": 9081,
                    "alight_pasgr_num": 8847,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "고덕"
                },
                {
                    "line_num": "5호선",
                    "ride_pasgr_num": 14956,
                    "alight_pasgr_num": 16214,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "공덕"
                },
                {
                    "line_num": "5호선",
                    "ride_pasgr_num": 13017,
                    "alight_pasgr_num": 11467,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "광나루(장신대)"
                },
                {
                    "line_num": "5호선",
                    "ride_pasgr_num": 33516,
                    "alight_pasgr_num": 36637,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "광화문(세종문화회관)"
                },
                {
                    "line_num": "5호선",
                    "ride_pasgr_num": 10951,
                    "alight_pasgr_num": 12202,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "군자(능동)"
                },
                {
                    "line_num": "5호선",
                    "ride_pasgr_num": 9276,
                    "alight_pasgr_num": 8572,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "굽은다리(강동구민회관앞)"
                },
                {
                    "line_num": "5호선",
                    "ride_pasgr_num": 7668,
                    "alight_pasgr_num": 7979,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "길동"
                },
                {
                    "line_num": "5호선",
                    "ride_pasgr_num": 7721,
                    "alight_pasgr_num": 8015,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "김포공항"
                },
                {
                    "line_num": "5호선",
                    "ride_pasgr_num": 30034,
                    "alight_pasgr_num": 27521,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "까치산"
                }
            ]
        },
        {
            "name": "공항철도 1호선",
            "children": [
                {
                    "line_num": "공항철도 1호선",
                    "ride_pasgr_num": 7673,
                    "alight_pasgr_num": 7335,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "검암"
                },
                {
                    "line_num": "공항철도 1호선",
                    "ride_pasgr_num": 10132,
                    "alight_pasgr_num": 8857,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "계양"
                },
                {
                    "line_num": "공항철도 1호선",
                    "ride_pasgr_num": 2372,
                    "alight_pasgr_num": 3110,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "공덕"
                },
                {
                    "line_num": "공항철도 1호선",
                    "ride_pasgr_num": 2247,
                    "alight_pasgr_num": 2474,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "공항화물청사"
                },
                {
                    "line_num": "공항철도 1호선",
                    "ride_pasgr_num": 12233,
                    "alight_pasgr_num": 7171,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "김포공항"
                }
            ]
        },
        {
            "name": "경강선",
            "children": [
                {
                    "line_num": "경강선",
                    "ride_pasgr_num": 7059,
                    "alight_pasgr_num": 6545,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "경기광주"
                },
                {
                    "line_num": "경강선",
                    "ride_pasgr_num": 1947,
                    "alight_pasgr_num": 1852,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "곤지암"
                }
            ]
        },
        {
            "name": "과천선",
            "children": [
                {
                    "line_num": "과천선",
                    "ride_pasgr_num": 1333,
                    "alight_pasgr_num": 1359,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "경마공원"
                },
                {
                    "line_num": "과천선",
                    "ride_pasgr_num": 5000,
                    "alight_pasgr_num": 4328,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "과천"
                }
            ]
        },
        {
            "name": "6호선",
            "children": [
                {
                    "line_num": "6호선",
                    "ride_pasgr_num": 8125,
                    "alight_pasgr_num": 7381,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "고려대(종암)"
                },
                {
                    "line_num": "6호선",
                    "ride_pasgr_num": 19817,
                    "alight_pasgr_num": 19484,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "공덕"
                },
                {
                    "line_num": "6호선",
                    "ride_pasgr_num": 9460,
                    "alight_pasgr_num": 8911,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "광흥창(서강)"
                },
                {
                    "line_num": "6호선",
                    "ride_pasgr_num": 7424,
                    "alight_pasgr_num": 5472,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "구산"
                },
                {
                    "line_num": "6호선",
                    "ride_pasgr_num": 5430,
                    "alight_pasgr_num": 5342,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "녹사평(용산구청)"
                },
                {
                    "line_num": "6호선",
                    "ride_pasgr_num": 6850,
                    "alight_pasgr_num": 6041,
                    "work_dt": "20200703",
                    "use_dt": "20200630",
                    "name": "효창공원앞"
                }
            ]
        },
        {
            "name": "안산선",
            "children": [
                {
                    "line_num": "안산선",
                    "ride_pasgr_num": 7712,
                    "alight_pasgr_num": 7462,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "고잔"
                }
            ]
        },
        {
            "name": "중앙선",
            "children": [
                {
                    "line_num": "중앙선",
                    "ride_pasgr_num": 14055,
                    "alight_pasgr_num": 14250,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "구리"
                },
                {
                    "line_num": "중앙선",
                    "ride_pasgr_num": 710,
                    "alight_pasgr_num": 733,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "국수"
                }
            ]
        },
        {
            "name": "4호선",
            "children": [
                {
                    "line_num": "4호선",
                    "ride_pasgr_num": 20993,
                    "alight_pasgr_num": 19353,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "길음"
                },
                {
                    "line_num": "4호선",
                    "ride_pasgr_num": 1296,
                    "alight_pasgr_num": 1070,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "남태령"
                },
                {
                    "line_num": "4호선",
                    "ride_pasgr_num": 20773,
                    "alight_pasgr_num": 24183,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "노원"
                }
            ]
        },
        {
            "name": "수인선",
            "children": [
                {
                    "line_num": "수인선",
                    "ride_pasgr_num": 1961,
                    "alight_pasgr_num": 2171,
                    "work_dt": "20200810",
                    "use_dt": "20200807",
                    "name": "남동인더스파크"
                }
            ]
        }
    ]
}
```
