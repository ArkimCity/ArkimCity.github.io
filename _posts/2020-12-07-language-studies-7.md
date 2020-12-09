---
title: "Language Study - Google GeoCode API - 주소 값을 넣어 위도와 경도를 받아오자"
date: 2020-12-07
categories: LanguageStudies
tags: java GeoCode
languages: java
---
## 1. 의의

지형 지도 혹은 데이터 시각화에 관심이 있는 사람이라면 누구나 한번쯤은 위도 경도 데이터를 가져오는 것에 관심을 가져본 적이 있을 것이다.

이 글에서는 google maps api의 일종인 GeoCode API를 통해 위도와 경도를 가져오는 방법을 설명하고자 한다.

## 2. 준비

2020년 12월 현재 기준 google maps의 API들을 사용하기 위해서는 api key가 필요하다. 받는 방법은 크게 어렵지 않으니 생략하고자 한다.

추가적으로 이 코드에서는 jsonsimple api가 필요하다. 다운로드하거나 import하는 걸 추천한다.

혹시 못찾으시겠다면 제가 사용한 maven dependency는 다음을 사용하였습니다.

```xml
		<dependency>
			<groupId>com.googlecode.json-simple</groupId>
			<artifactId>json-simple</artifactId>
			<version>1.1.1</version>
		</dependency>
```


## 3. 메소드

실행은 test 패키지 안에 클래스를 만들어주는 것을 예시로 들겠습니다.

google maps api key를 꼭 발급받아 아래에 대체해주셔야 실행됩니다.

```java
package test;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.HashMap;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class GeoCodeTest {
	private static String APIKey = "본인의 google maps api 키를 넣어주세요";

	public static HashMap getGeoCode(String address) {
		HashMap geocode = new HashMap();
		StringBuffer sbuf = new StringBuffer();

		try {
			String geocodeURL = "https://maps.googleapis.com/maps/api/geocode/json?address="
					+ URLEncoder.encode(address, "UTF-8") + "&key=" + APIKey;
			URL url = new URL(geocodeURL);

			URLConnection urlConn = url.openConnection();

			InputStream is = urlConn.getInputStream();
			InputStreamReader isr = new InputStreamReader(is, "UTF-8");
			BufferedReader br = new BufferedReader(isr);

			String str;
			while ((str = br.readLine()) != null) {

				sbuf.append(str + "\r\n");

			}
			geocode = toGeoCode(sbuf.toString());

			is.close();
			isr.close();
			br.close();

		} catch (MalformedURLException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return geocode;
	}

	public static HashMap toGeoCode(String content) {
		HashMap geocode = new HashMap();
		double lattitude = 0;
		double longtitude = 0;
		JSONParser parser = new JSONParser();

		try {

			Object obj = parser.parse(content);

			JSONObject jsonObject = (JSONObject) obj;

			ArrayList j1 = (ArrayList) jsonObject.get("results");

			JSONObject j2 = jsonParser(j1.get(0).toString());
			JSONObject j3 = jsonParser(j2.get("geometry").toString());
			HashMap j4 = (HashMap) j3.get("location");

			lattitude = (double) j4.get("lat");
			longtitude = (double) j4.get("lng");
			
			geocode.put("lattitude", lattitude);
			geocode.put("longtitude", longtitude);
			
			

		} catch (ParseException e) {
			e.printStackTrace();
		}
		return geocode;
	}

   	
	public static JSONObject jsonParser(String content) {
		
		JSONParser parser = new JSONParser();
		JSONObject jsonObject = null;
		try {

			Object obj = parser.parse(content);

			jsonObject = (JSONObject) obj;

		} catch (Exception e) {
			e.printStackTrace();
		}
		return jsonObject;
	}
}

```


## 4.실행
```java
package test;

public class Test {
	public static void main(String[] args) {
		System.out.println(GeoCodeTest.getGeoCode("서울시 마포구 와우산로 94"));
	}
}
```

주소는 아무거나 넣어도 되기는 한데 결론부터 말하자면 GeoCodeTest.getGeoCode(String address) 함수는 HashMap 타입을 반환하도록 만들어두었다.

키값은 {lattitude=37.566535, longtitude=126.9779692} 와 같이 "lattitude"과 "longtitude" 사용하면 되고 함수에서 변경해도 된다.

테스트는 해두었는데 혹시 안되거나 문제가 있는 부분은 댓글로 남겨주시면 감사하겠습니다.

## 5. 추가 설명

처음에 url을 입력하면 

```json
{
   "results" : [
      {
         "address_components" : [
            {
               "long_name" : "테헤란로4길",
               "short_name" : "테헤란로4길",
               "types" : [ "political", "sublocality", "sublocality_level_4" ]
            },
            {
               "long_name" : "역삼1동",
               "short_name" : "역삼1동",
               "types" : [ "political", "sublocality", "sublocality_level_2" ]
            },
            {
               "long_name" : "강남구",
               "short_name" : "강남구",
               "types" : [ "political", "sublocality", "sublocality_level_1" ]
            },
            {
               "long_name" : "서울특별시",
               "short_name" : "서울특별시",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "대한민국",
               "short_name" : "KR",
               "types" : [ "country", "political" ]
            },
            {
               "long_name" : "135-080",
               "short_name" : "135-080",
               "types" : [ "postal_code" ]
            }
         ],
         "formatted_address" : "대한민국 서울특별시 강남구 역삼1동 테헤란로4길",
         "geometry" : {
            "bounds" : {
               "northeast" : {
                  "lat" : 37.4978496,
                  "lng" : 127.0310505
               },
               "southwest" : {
                  "lat" : 37.4953323,
                  "lng" : 127.0291474
               }
            },
            "location" : {
               "lat" : 37.4965345,
               "lng" : 127.0302544
            },
            "location_type" : "APPROXIMATE",
            "viewport" : {
               "northeast" : {
                  "lat" : 37.4979399302915,
                  "lng" : 127.0314479302915
               },
               "southwest" : {
                  "lat" : 37.4952419697085,
                  "lng" : 127.0287499697085
               }
            }
         },
         "place_id" : "ChIJFW7lslChfDURT_0fabrvbec",
         "types" : [ "political", "sublocality", "sublocality_level_4" ]
      }
   ],
   "status" : "OK"
}
```
와 같은 형태로 받아오게 된다. 여기서 안에 있는 "location" 의 lat lng을 return한다