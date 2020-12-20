---
title: "Toy Project - 같은 스케일로 도시를 봐보자"
date: 2020-12-20
categories: ToyProjects
tags: GoogleMap
---


## 1. 발단

친구의 "같은 스케일로 도시들을 늘어놓고 비교해보고싶다." 라는 말에 작업해본 토이 프로젝트

## 2. 작업

아주 간단하게 스케일을 4개의 지도 모두 같은 스케일로  리셋시켜주는 리셋버튼과 네개의 지도를 통해 보여주는 화면이다.

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Google Maps in Same Scale</title>
</head>
<body>
  <button type="button" id="button1">스케일 리셋하기</button>
  <br><br><hr>

  <div id="map1" style="width:45%; height: 45vh; float: left; border: 1px;" ></div>
  <script async defer src="https://maps.googleapis.com/maps/api/js?key='Google Map API키 자리입니다. 따옴표까지 지워주세요'&callback=initMap&region=kr"></script>
  <script src="./script.js"></script>

  <div id="map2" style="width:45%; height: 45vh; float: right; border: 1px;"></div>
  <script async defer src="https://maps.googleapis.com/maps/api/js?key='Google Map API키 자리입니다. 따옴표까지 지워주세요'&callback=initMap&region=kr"></script>
  <script src="./script.js"></script>

  <div id="map3" style="width:45%; height: 45vh; float: left; border: 1px;"></div>
  <script async defer src="https://maps.googleapis.com/maps/api/js?key='Google Map API키 자리입니다. 따옴표까지 지워주세요'&callback=initMap&region=kr"></script>
  <script src="./script.js"></script>

  <div id="map4" style="width:45%; height: 45vh; float: right; border: 1px;"></div>
  <script async defer src="https://maps.googleapis.com/maps/api/js?key='Google Map API키 자리입니다. 따옴표까지 지워주세요'&callback=initMap&region=kr"></script>
  <script src="./script.js"></script>

</body>
</html>
```
네개의 지도에 대한 정보를 세팅한다.

```javascript
var map1;
var map2;
var map3;
var map4;

var seoul = { lat: 37.5642135 ,lng: 127.0016985 };
var london = { lat: 51.51531377742486 ,lng: -0.1276970532377955 };
var tokyo = { lat: 35.682636526307334 ,lng: 139.76850437605137 };
var newyork = { lat: 40.7124988481609 ,lng: -74.00921376413213 };

var button1 = document.getElementById('button1');
button1.addEventListener('click', scaleReset);

function initMap() {
    map1 = new google.maps.Map( document.getElementById('map1'), {
        zoom: 12,
        center: seoul
    });

    map2 = new google.maps.Map( document.getElementById('map2'), {
        zoom: 12,
        center: london
    });

    map3 = new google.maps.Map( document.getElementById('map3'), {
        zoom: 12,
        center: tokyo
    });
 
    map4 = new google.maps.Map( document.getElementById('map4'), {
        zoom: 12,
        center: newyork
    });
}

function scaleReset(){
  map1.setZoom(14);
  map2.setZoom(14);
  map3.setZoom(14);
  map4.setZoom(14);
}
```

## 3. 화면

은 다음과 같다.

![MAP_IN_SAME_SCALE]](/assets/images/MAP_IN_SAME_SCALE.jpg)