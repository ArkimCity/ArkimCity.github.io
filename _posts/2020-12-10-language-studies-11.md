---
title: "Language Study - GeoJson에 대하여 알아보자"
date: 2020-12-10
categories: LanguageStudies
tags: TypeScript
languages: TypeScript
---


## 1. GeoJson이란?

JSON 형식 중에서도 위치 혹은 도형 정보를 저장하기 위한 하나의 약속으로, 앞서 단순이 위경도를 담는 json 정보와는 방향성이 다르다. 바로 예시를 보고 가자면, 우리가 아는 바로 그 도형의 종류인 점선면에 대한 표현은 다음과 같다.

```json
{
    "type": "Point",
    "coordinates": [0, 0]
}
```

```json
{
    "type": "LineString",
    "coordinates": [
        [0, 0], [10, 10], [10, 20]
    ]
}
```

```json
{
    "type": "Polygon",
    "coordinates": [
        [[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]
    ]
}
```

공통적으로 하나의 가장 작은 단위의 리스트는 점으로 표현하고 있고, 

coordinates 안에 있는 점들은 index 0 부터 차근 차근 다음 인덱스의 점으로 이어지며, 

특히 폴리곤의 경우 저런식으로 끝점과 시작점을 같은 점으로 표기해 닫힌다는 것을 눈으로도 확인할 수 있다.

## 2. 다수 표현

```json
{
    "type": "MultiPoint",
    "coordinates": [
        [10, 40], [40, 30], [20, 20], [30, 10]
    ]
}
```


```json
{
    "type": "MultiLineString",
    "coordinates": [
        [[10, 10], [20, 20], [10, 40]], // line 1 
        [[40, 40], [30, 30], [40, 20], [30, 10]] // line 2
    ]
}
```

```json
{
    "type": "MultiPolygon",
    "coordinates": [
        [
            [[30, 20], [45, 40], [10, 40], [30, 20]] // polygon 1
        ],
        [
            [[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]] // polygon 1
        ]
    ]
}
```


```json
{
    "type": "MultiPolygon",
    "coordinates": [
        [
            [[40, 40], [20, 45], [45, 30], [40, 40]] // polygon 1
        ],
        [
            [[20, 35], [10, 30], [10, 10], [30, 5], [45, 20], [20, 35]],
            [[30, 20], [20, 15], [20, 25], [30, 20]] // polygon 2 that has two geometries
        ]
    ]
}
```

## 3. 폴리곤 내에서의 겹침

다른 부분은 모두 직관적으로 이해가 가능하지만, polygon 안의 polygon 형태가 다소 헷갈려 추가적으로 찾아보았다.

geojson.org의 설명에 따르면

"For type "Polygon", the "coordinates" member must be an array of LinearRing coordinate arrays. For Polygons with multiple rings, the first must be the exterior ring and any others must be interior rings or holes."

즉, 예를 들어 어떤 경계를 이루는 도형이 있다면, 첫번째 집합은 바깥 경계가 되고, 나머지 집합들은 그 안에서 구멍을 뚫는 개념으로 보는 것이다.

위에서 보았던 예시 중,

```json
        [
            [[20, 35], [10, 30], [10, 10], [30, 5], [45, 20], [20, 35]],
            [[30, 20], [20, 15], [20, 25], [30, 20]] // polygon 2 that has two geometries
        ]
```
부분에서 [[20, 35], [10, 30], [10, 10], [30, 5], [45, 20], [20, 35]] 부분이 바로 바깥 경계가 되고, [[30, 20], [20, 15], [20, 25], [30, 20]] 부분이 안에서 구멍을 뚫는 것이다.

## 4. GeometryCollection

이 글의 마지막으로, 위의 기본 자료들을 바탕으로 하나의 컬렉션을 만들어서 하나의 파일로 전달하고자 하는 경우가 대다수일 것이므로, 이를 묶어서 보관하는 형태인 GeometryCollection 을 알아보면,

```json
{
    "type": "GeometryCollection",
    "properties": {
        "value": "foo"
    },
    "geometries": [{
        "type": "Point",
        "coordinates": [0, 0]
    }, {
        "type": "Polygon",
        "coordinates": [[[45, 45], [45, -45], [-45, -45], [-45, 45], [45,45]]]
    }]
}
```

와 같이 타입을 GeometryCollection으로 선언해준 뒤, geometries 안에 도형들이 들어가는 것으로 이해하면 된다.

https://geojson.org/geojson-spec.html 을 살펴보면 알겠지만, 사실 geojson의 내용 중 일부에 해당하므로, 추후 정리할 예정이지만 필요하다면 이 사이트를 참고하는 것이 좋아보인다.

다음 글에서는 이 자료구조가 3d로 표현되는 과정을 보고자 한다.