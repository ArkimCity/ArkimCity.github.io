---
title: "Language Study - https://mapshaper.org/ - SHP파일을 GeoJson으로 사용하고싶다면"
date: 2021-02-09
categories: LanguageStudies
tags: GeoJson
---


## 1. Shp to GeoJson

도형 및 지도 관련 정보를 사용하다보면 심심찮게 Shp 파일을 마주하게 되는데, Gis 관련에서는 좋아도 웹에서 인식시키거나 내가 보기에도 이해하기 편하기 위한 경우,  GeoJson으로 변환해서 사용할 경우는 분명히 있다.

데이터는 [국가공간정보포털](http://openapi.nsdi.go.kr/nsdi/eios/OpenapiList.do?provOrg=NIA&gubun=F) 에서 찾을 수 있고, A*형식의 해당 칼럼 정보는 동봉된 hwp 파일 안에 설명되어있다.

(필자는 여기에서 GIS건물통합정보 페이지를 사용했다. 참고로 내가 받은 자료는 인코딩이 cp949로 되어있었다. 이를 확인하는 방법은 다양하지만 파이썬에서 가볍게 체크할 수 있는 chardet 이라는 라이브러리가 있다.)


이번에 사용한 사이트는 [https://mapshaper.org/](https://mapshaper.org/) 로, 꼭 이 사이트를 사용할 필요는 없고 

SHP파일과 GeoJson의 차이를 간략히라도 이해하고 사용할 수 있으면 될것 같다.

여기서는 간략히

shp,shx를 합쳐 형태 혹은 공간 데이터, 

dbf를 그 데이터의 속성 정보라고 이해할 수 있다.

자세하게 알고싶은 분들은 [https://endofcap.tistory.com/3](https://endofcap.tistory.com/3) 에 정리가 잘 되어있는 것 같아 첨부한다.


## 2. GeoJson으로 변환한 한줄 예시

보이는 바와 같이 컬럼 정보가 properties에 담기고 도형 정보가 geometry, type, coordinates에 담겨서 GeoJson 형식으로 사용이 가능하다. GeoJson 의 활용방법은 다양함으로 우선 이와 같은 내용으로 이번 글을 마무리하고자 한다. 

```json
{
            "type": "Feature",
                "geometry": { 
                    "type": "Polygon", 
                    "coordinates": [
                        [
                            [197110.51400000043, 453120.7530000005], [197110.31400000025, 453120.5529999994], [197110.51400000043, 453120.3530000001], [197110.7139999997, 453120.5529999994], [197110.51400000043, 453120.7530000005]
                        ]
                    ] 
                }, 
                "properties": { 
                    "A0": "0000197110514531205500000000", "A1": "1111011000100760000", "A2": "1111011000", "A3": "서울특별시 종로구 누하동", "A4": "1", "A5": "일반", "A6": "76", "A7": "24944", "A8": "1", "A9": "일반건축물", "A10": "2", "A11":  "일반건축물대방", "A12": "", "A13": "0", "A14": "111102100002", "A15": "11003", "A16": "0", "A17": "00049", "A18": "00009", "A19": "", "A20": "0", "A21": "주건축물", "A22": 0, "A23": 0, "A24": 42.98, "A25": 0, "A26": 0, "A27": "51", "A28": "일반목구조", "A29": "01000", "A30": "단독주택", "A31": 0, "A32": 1, "A33": 0, "A34": "", "A35": "", "A36": 0, "A37": 0, "A38": "2020-09-16T00:00:00.000Z" 
                }
        },
```