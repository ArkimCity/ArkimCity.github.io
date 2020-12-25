---
title: "Language Study - JAVA로 크롤링을 해보자(Jsoup)"
date: 2020-12-25
categories: LanguageStudies
tags: Jsoup java
---


## 1. Jsoup?

크롤링에 관심이 있는 분이라면 BeautifulSoup을 들어보신 적이 있을 거라 생각한다. 크롤링을 자바에서 구현해보기 위해 이 라이브러리를 사용했다.

## 2. Dependencies(Maven)

여기서는 크롤링을 위한 jsoup과 json 파싱을 위한 json simple을 사용했다. 

```xml
<dependency>
    <groupId>org.jsoup</groupId>
    <artifactId>jsoup</artifactId>
    <version>1.13.1</version>
</dependency>
<dependency>
    <groupId>com.googlecode.json-simple</groupId>
    <artifactId>json-simple</artifactId>
    <version>1.1.1</version>
</dependency>
```
## 3. Code

여기서 테스트한 방법은 url 구성이 간편한 네이버 맵 모바일 버전을 사용했다.

```java
Elements scripts = doc2.getElementsByTag("script");
```
이 부분에서 이 분서의 클래스 중 script를 한정지어 검색하는 것이고, 


```java
	    String a = null;
	    
	    for (Element element : scripts) {
		       if (element.data().contains("var searchResult")) {
		           Pattern pattern = Pattern.compile(".*var searchResult = ([^;]*);");
		           Matcher matcher = pattern.matcher(element.data());
		           if (matcher.find()) {
		        	   a = matcher.group(1);
		        	   break;
		           } else {
		               System.err.println("No match found!");
		           }
		           break;
		       }
		}
```

이 부분에서 var searchResult 를 포함하는 엘레멘트에서 ".*var searchResult = ([^;]*);" 와 같은 모양을 하고 있는 줄만 가져올 수 있었다.

```java
		for (Object i : (ArrayList<Object>)jsonParser(jsonParser(a).get("site").toString()).get("list")){
			System.out.println(jsonParser(i.toString()).get("id").toString());
			System.out.println(jsonParser(i.toString()).get("name").toString());
			System.out.println(jsonParser(i.toString()).get("abbrAddress").toString());
			System.out.println(jsonParser(i.toString()).get("address").toString());
			System.out.println(jsonParser(i.toString()).get("roadAddress").toString());
			System.out.println(jsonParser(i.toString()).get("category").toString());
			System.out.println();
		}
```

가져온 데이터는 다루기 용이하게 하기 위하여 json 파싱을 사용했다. 이에 대한 메소드 역시 아래에 적혀있다.

풀 코드는 다음과 같다.

```java
package test;

import java.io.IOException;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class JsoupCrawlTest {
	public static void main(String[] args) {
		crawler("시골향기");
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
	
	
	public static void crawler(String search) {
		Document doc2 = null;
		try {
			doc2 = Jsoup.connect("https://m.map.naver.com/search2/search.nhn?query=" + search + "&sm=hty&style=v5").timeout(10000).get();
		} catch (IOException e) {
			e.printStackTrace();
		}
		Elements scripts = doc2.getElementsByTag("script");
	    
	    String a = null;
	    
	    for (Element element : scripts) {
		       if (element.data().contains("var searchResult")) {
		           Pattern pattern = Pattern.compile(".*var searchResult = ([^;]*);");
		           Matcher matcher = pattern.matcher(element.data());
		           if (matcher.find()) {
		        	   a = matcher.group(1);
		        	   break;
		           } else {
		               System.err.println("No match found!");
		           }
		           break;
		       }
		}
	    
		for (Object i : (ArrayList<Object>)jsonParser(jsonParser(a).get("site").toString()).get("list")){
			System.out.println(jsonParser(i.toString()).get("id").toString());
			System.out.println(jsonParser(i.toString()).get("name").toString());
			System.out.println(jsonParser(i.toString()).get("abbrAddress").toString());
			System.out.println(jsonParser(i.toString()).get("address").toString());
			System.out.println(jsonParser(i.toString()).get("roadAddress").toString());
			System.out.println(jsonParser(i.toString()).get("category").toString());
			System.out.println();
		}
	}
}
```

출력은 아래와 같은 내용으로 한정지어보았다.

```java
s33169366
시골향기
신곡리 447-75
경기도 김포시 고촌읍 신곡리 447-75
경기도 김포시 고촌읍 신곡로 114-8
["음식점","한식"]

s37522242
시골향기
운양동 117-8
경기도 김포시 운양동 117-8
경기도 김포시 걸포로 182
["음식점","한식"]

s1196811393
시골향기 작동점
작동 147
경기도 부천시 작동 147
경기도 부천시 여월로 202
["음식점","한식"]

s1859636272
시골향기 인덕원포일점
포일동 503-1 2층
경기도 의왕시 포일동 503-1 2층
경기도 의왕시 안양판교로 115 2층
["한식","보리밥"]

s36761406
시골향기손두부
법곳동 1734-8
경기도 고양시 일산서구 법곳동 1734-8
경기도 고양시 일산서구 법곳길 146
["한식","두부요리"]

s1882741956
시골향기
연하리 180-4
경기도 가평군 상면 연하리 180-4
경기도 가평군 상면 기와집길 7 복식당
["카페,디저트","다방"]

s20467365
시골향기
중도리 485-4
충청남도 금산군 금산읍 중도리 485-4
충청남도 금산군 금산읍 건삼전길 23-1
["음식점","한식"]

s1471858967
시골향기민박
송산리 308-1
전라남도 신안군 자은면 송산리 308-1
전라남도 신안군 자은면 두봉길 711
["숙박","민박"]

s38457381
시골향기
송산리 308-1
전라남도 신안군 자은면 송산리 308-1
전라남도 신안군 자은면 두봉길 711
["쇼핑,유통","가공식품"]

s37951872
시골향기
사직동 44-1
부산광역시 동래구 사직동 44-1
부산광역시 동래구 사직북로33번길 31
["쇼핑,유통","식료품"]

s16744568
시골향기
월길리 640
전라남도 광양시 진월면 월길리 640
전라남도 광양시 진월면 대리동백길 29-6
["농업","채소재배"]

s226613354
시골향기민박
용화리 219
강원도 삼척시 근덕면 용화리 219
강원도 삼척시 근덕면 용화해변1길 23
["숙박","민박"]

s36321055
오즈 포메라니안
소계리 268-2
충청북도 영동군 황간면 소계리 268-2
충청북도 영동군 황간면 민주지산로 4021
["반려동물","반려동물분양"]
```

## 4. JSON

가게 하나당 아래와 같은 형식의 json 문자열을 받을 수 있기 때문에, 구조만 파악한다면 타고 들어가는 것 자체는 어렵지 않다.

```json
{
	"naverBookingUrl": null,
	"telDisplay": "031-997-6993",
	"type": "s",
	"homePage": "",
	"abbrAddress": "신곡리 447-75",
	"ktCallMd": "1e28d7fd80478a7eed185f4ac339b115",
	"indoorMapInfo": null,
	"posExact": "1",
	"hasNPay": false,
	"poiInfo": {
		"hasPolygon": false,
		"hasRoad": false,
		"hasLand": false,
		"polygon": null,
		"road": {
			"shapeKey": null,
			"boundary": null,
			"detail": null,
			"poiShapeType": "1"
		},
		"land": null
	},
	"shopWindowInfo": null,
	"rank": "1",
	"naverEasyOrderUrl": null,
	"tel": "031-997-6993",
	"entranceCoords": {
		"car": [
			{
				"coordType": "5",
				"entranceCoordY": "37.6075420",
				"entranceCoordX": "126.7670540",
				"coordSubType": 1,
				"isRepresentative": "1"
			}
		],
		"walk": [
			{
				"coordType": "5",
				"entranceCoordY": "37.6075420",
				"entranceCoordX": "126.7670540",
				"coordSubType": 1,
				"isRepresentative": "1"
			}
		]
	},
	"id": "s33169366",
	"broadcastInfo": {
		"name": null,
		"menu": null
	},
	"insidePanorama": null,
	"hasBroadcastInfo": false,
	"virtualTel": "",
	"index": "0",
	"couponUrl": null,
	"isCallLink": false,
	"thumUrl": "http:\/\/blogfiles.naver.net\/20160705_72\/balloonjoo_1467706696106oCtJK_JPEG\/image_9828304361467706576936.jpg#3000x2252",
	"indoorPanorama": null,
	"petrolInfo": null,
	"name": "시골향기",
	"isSite": "1",
	"indoor": {
		"underGmid": "0",
		"floor": "0",
		"underMid": "0"
	},
	"x1": null,
	"x2": null,
	"distance": "19169.64",
	"description": "",
	"menuExist": "1",
	"couponUrlMobile": null,
	"isPollingPlace": false,
	"menuInfo": null,
	"roadAddress": "경기도 김포시 고촌읍 신곡로 114-8",
	"theme": null,
	"skyPanorama": {
		"lng": "126.7681351",
		"id": "77YNvQ07FmgfZaFI9IaNLQ==",
		"tilt": "-30.00",
		"pan": "-18.09",
		"fov": "124",
		"lat": "37.6049995"
	},
	"ppc": "1",
	"address": "경기도 김포시 고촌읍 신곡리 447-75",
	"bizhourInfo": null,
	"coupon": "0",
	"display": "<b>시골향기<\/b>",
	"hasNaverBooking": false,
	"streetPanorama": {
		"lng": "126.7673697",
		"id": "fg++Fj4DOHh224xgJ03zXQ==",
		"tilt": "12.38",
		"pan": "-16.34",
		"fov": "50",
		"lat": "37.6072502"
	},
	"interiorPanorama": null,
	"hasCardBenefit": false,
	"x": "126.7672751",
	"y": "37.6076334",
	"category": [
		"음식점",
		"한식"
	],
	"itemLevel": "12"
}
```


## 5. (참고)해당 url의 예시 html 소스

너무 길어 다 읽을 필요는 절대 없고, 이런 구조에서 가져왔구나 만 보시면 될것 같다.


```html




<!DOCTYPE html>
<html lang="ko">
<head>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />


	
	
		
	
	










	<meta property="og:type" content="website"/>
	<meta property="og:site_name" content="네이버 지도"/>
	<meta property="og:title" content="시골향기 : 네이버 지도" /> 
	

	
	<meta property="og:image" content="https://ssl.pstatic.net/static/maps/m/og_map.png" />
	<meta property="twitter:image" content="https://ssl.pstatic.net/static/maps/m/og_map.png" />
	<meta property="og:description" content="자동차/대중교통/자전거/도보 길찾기, 실시간 교통 및 버스위치, CCTV, 지하철, 버스노선, 거리뷰, 뮤지엄뷰 제공."/>
	<meta property="twitter:description" content="자동차/대중교통/자전거/도보 길찾기, 실시간 교통 및 버스위치, CCTV, 지하철, 버스노선, 거리뷰, 뮤지엄뷰 제공."/>
	<meta property="twitter:card" content="summary_large_image"/>



	
	
	
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no" />
	

<link rel="stylesheet" type="text/css" href="/css/w_v1608785351406.css"/>
<link rel="shortcut icon" href="https://ssl.pstatic.net/static/maps/m/icon/ic_ad_map1_96X96.png" />

<meta name="referrer" content="always">

<title>네이버 지도</title>


<script type="text/javascript" src="/js/lib/require_v1608785351430.js"></script>
<script type="text/javascript" src="/js/vendor_v1608785351430.js"></script>
<script type="text/javascript" src="/js/baselib_v1608785351430.js"></script>
<script type="text/javascript">
document.domain = 'naver.com';
// nclicks 적용
//var ccsrv="alpha-cc.naver.com";
window.ccsrv="cc.naver.com";

var browserType = "OTHERS";
var keywordInfo = null;

$(window).load(function(){
	var $body = $("body"),
		$content = $("div#ct");

	var fitter = new nhn.map.mobile.WindowSizeFitter({}, $content);
	fitter.start(this.elMap, resize, resize);

	setTimeout(function() {
		if ($(window).scrollTop() == 0) {
			window.scrollTo(0, 1)
		}
	}, 300);
	if (typeof tabName != "undefined" && $("#" + tabName)) {
		$("#" + tabName).addClass("on");
	}

	function resize(e) {
		var windowHeight = e.height;

		$body.css("height", windowHeight + "px");

		if ($("div._errorMessage").length) {
			fitSizeErrorMessage();
		}
	}

	function fitSizeErrorMessage() {
		var addHeight = $("body").height() - $("div#header").height() - $("div#ct").height();
		$("div._errorMessage").height($("div._errorMessage").height() + addHeight);
	}
});
</script>

<script type="text/javascript" language="javascript">

	
	var g_ssc = "m.map.listview";
	var g_query = "시골향기";

	// 최근검색어 추가
	var $SearchHistoryHandler = new nhn.map.mobile.SearchHistoryHandler();
	var item = {};
		item.query = g_query;
		item.time = (new Date()).getTime();
	$SearchHistoryHandler.addHistory(item);

	
	

var tabName = "tabSearch";
</script>
</head>
<body class="search">
<div id="u_skip" class="u_skip"><a href="#ct">본문 바로가기</a></div>




<div id="u_skip" class="u_skip">
	<a href="#ct">본문 바로가기</a>
</div>

<div id="header" class="_header">
<header class="_gnb">
	<div class="Ngnb is_scale _gnbTopClass">
		<span class="Ngnb_logo _naver" style="display:none;"><a href="http://m.naver.com" onclick="nclk(this, 'gnb.naver', '', '')" class="Nlogo_link"><span class="Nicon_logo">NAVER</span></a></span>
		<span class="Ngnb_navigation _home" style="display:none;"><a href="/" class="Nnavigation_link"><span class="Nicon_home">지도홈</span></a></span>
		<div class="Ngnb_service">
			<h1 class="Nservice_item"><a href="/" class="_gnbTitleLink"><span class="Nicon_service _gnbTitle" style="display:none">지도</span></a></h1>
		</div>
		<div class="Ngnb_tool">
			<!--  button 태그 / a 태그 모두 사용할 수 있음 -->
			<button type="button" class="Ntool_button _toggleSearch" style="display:none;" data-nclicks="gnb.search"><span class="Nicon_search">검색</span></button>
			<a href="#" class="Ntool_button _openAside" data-toggle=".Nsearch|is_something" data-nclicks="gnb.menu"><span class="Nicon_drawer">메뉴보기</span></a>
		</div>
	</div>

	<div id="aside" class="Ndrawer _aside" style="display:none;">
		<div id="asideScrollWrapper" class="Ndrawer_scroll _asideScrollWrapper">
			<div class="_scroller" style="width:100%">
				<div class="Ndrawer_inner">
					<div class="Ndrawer_profile">
						
							<a href="https://nid.naver.com/mobile/user/help/myInfo.nhn" class="Ndrawer_profile_login">
							
						
							<div class="NLogin_thumb">
								<img src="https://static.nid.naver.com/images/web/user/img_aside_photo_default.png" width="36" height="36" class="NLogin_thumb_image _profile" alt="" />
							</div>
							
								<span class="NLogin_name">웅스</span>
									<p class="NLogin_id">jaeung94</p>
								
							
						</a>
						<button type="button" class="Ndrawer_profile_close _close" data-nclicks="gnb.close"><span class="Nclose_icon">닫기</span></button>
					</div>
					<div class="Ndrawer_menu">
						<a id="tabSearch" href="/" onclick="nclk(this, 'cmn.search', '', '')" class="Nmenu_item"><i class="ico_map"></i>지도</a>
						<a id="tabRoute" href="/directions" onclick="nclk(this, 'cmn.route', '', '')" class="Nmenu_item"><i class="ico_route"></i>길찾기</a>
						<a id="tabBus" href="/bus/index.nhn" onclick="nclk(this, 'cmn.bus', '', '')" class="Nmenu_item"><i class="ico_bus"></i>버스</a>
						<a id="tabSubway" href="/subway/subwayLine.nhn" onclick="nclk(this, 'cmn.subway', '', '')" class="Nmenu_item"><i class="ico_subway"></i>지하철</a>
						<a id="tabTraffic" href="/traffic/trafficMap.nhn" onclick="nclk(this, 'cmn.traffic', '', '')" class="Nmenu_item"><i class="ico_traffic"></i>교통정보</a>
					</div>
					<div class="Ndrawer_menu">
						<a href="https://m.help.naver.com/support/service/main.nhn?serviceNo=5637" onclick="nclk(this, 'cmn.help', '', '')" class="Nmenu_item">지도 고객센터</a>
						<a href="https://m.help.naver.com/support/issue/report.nhn?serviceNo=5637" onclick="nclk(this, 'cmn.report', '', '')" class="Nmenu_item">오류신고</a>
						<a href="https://m.smartplace.naver.com/places/user-engagements" onclick="nclk(this, 'cmn.placesubmit', '', '')" class="Nmenu_item">신규장소 등록</a>
						<a href="/menu.nhn?menu=legalNotice" onclick="nclk(this, 'cmn.legalnotice', '', '')" class="Nmenu_item">법적공지</a>
						<a href="/menu.nhn?menu=informationProvider" onclick="nclk(this, 'cmn.provider', '', '')" class="Nmenu_item">정보제공처</a>
					</div>
					<div class="Ndrawer_footer">
						<div class="Ndrawer_footer_links">
							
								<a href="#" onclick="nclk(this, 'cmn.tlogout', '', '');nhn.map.mobile.GlobalFunctions.logout()" class="Nlinks_item">로그아웃</a>
								
							
							<a href="http://map.naver.com/?mobile&query=시골향기&searchCoord=126.9783882;37.5666103" onclick="nclk(this, 'cmn.gopc', '', '');" id="pcWebLink" data-default-href="http://map.naver.com/?mobile&query=시골향기&searchCoord=126.9783882;37.5666103" class="Nlinks_item _pcWebUrl">PC버전</a>
							<a href="http://m.naver.com/services.html?f=svc.map" onclick="nclk(this, 'cmn.sitemap', '', '')" class="Nlinks_item">전체서비스</a>
						</div>
						<a href="http://www.navercorp.com/" class="a_corp" onclick="nclk(this, 'cmn.navercorp', '', '')"><p class="Ndrawer_footer_copyright">ⓒ NAVER Corp.</p></a>
					</div>
				</div>
			</div>
		</div>
	</div>
	<div class="dmm" style="display: none"></div>
	<hr />


	<!-- 쿼리 -->
	<div class="Nsearch _searchKeywordView _searchGuide" style="display:none;">
		<div class="Nsearch_inner">
			<div class="Nsearch_box">
				<div class="Nsearch_box_inner">
					<span class="Nbox_text _textPanel">
						<input type="text" value="시골향기" placeholder="장소, 주소 검색" title="검색어 입력" class="Nbox_input_text _keyword">
					</span>
					<span class="Nbox_tool">
						<button type="button" class="Nbox_button Nbox_delete _clear" style="display:none;"><span class="Nicon_delete">검색어 삭제</span></button>
						<button type="submit" class="Nbox_button Nbox_search _search"><span class="Nicon_submit">검색</span></button>
					</span>
				</div>
			</div>
		</div>
	</div>
	<!--// 쿼리 -->
</header>
</div>
<!--// header -->


<hr />



<div id="ct">

<script src="/adimg3.search/adpost/js/ad.js"></script>

<!-- 검색 영역 -->

	<!-- 키워드검색 -->
	<div class="search _searchView" style="display:none;">
		<div class="Nsearch">
			<form name="form" class="_formSearch" action="#">
			<div class="Nsearch_inner">
				<div class="Nsearch_navigation"><a href="#" class="Nnavigation_link _closeSearchForm" data-nclicks="scw.close"><span class="Nnavigation_icon Nicon_prev">이전으로 돌아가기</span></a></div>
				<div class="Nsearch_box">
					<div class="Nsearch_box_inner">
						<span class="Nbox_text"><input type="search" name="search_query" value="시골향기" maxLength="100" placeholder="장소, 주소 검색" title="검색어 입력" class="Nbox_input_text _search_input"></span>
						<span class="Nbox_tool">
							<button type="button" class="Nbox_button Nbox_delete _clear" data-nclicks="scw.kwdx"><span class="Nicon_delete">검색어 삭제</span></button>
							<button type="submit" class="Nbox_button Nbox_search _search"><span class="Nicon_submit">검색</span></button>
						</span>
					</div>
				</div>
			</div>
			</form>
		</div>
	
		<div id="view" class="_searchAssistView" style="display:none;">
			<div class="search_category_scroll _interestView">
				<div class="_scroller"><a href="#" class="_linkCategory" data-nclicks="scn.restaurant" data-category="DINING"><i class="ico_cate_dining"></i>음식점</a><a
						href="#" class="_linkCategory" data-nclicks="scn.cafe" data-category="CAFE"><i class="ico_cate_cafe"></i>카페</a><a
						href="#" class="_linkCategory" data-nclicks="scn.shopping" data-category="SHOPPING"><span class="sp_map ico_new">new</span><i class="ico_cate_shopping"></i>쇼핑</a><a
						href="#" class="_linkCategory" data-nclicks="scn.accom" data-category="ACCOMMODATION"><i class="ico_cate_accommodation"></i>숙박</a><a
						href="#" class="_linkCategory" data-nclicks="scn.medical" data-category="HOSPITAL"><i class="ico_cate_hospital"></i>병원의료</a><a
						href="#" class="_linkCategory" data-nclicks="scn.bank" data-category="BANK"><i class="ico_cate_bank"></i>은행</a><a
						href="#" class="_linkCategory" data-nclicks="scn.gas" data-category="OIL"><i class="ico_cate_gas"></i>주유소</a><a
						href="#" class="_linkCategory" data-nclicks="scn.mart" data-category="MART"><i class="ico_cate_mart"></i>마트슈퍼</a><a
						href="#" class="_linkCategory" data-nclicks="scn.cvs" data-category="STORE"><i class="ico_cate_store"></i>편의점</a><a
						href="#" class="_linkCategory" data-nclicks="scn.life" data-category="CONVENIENCE"><i class="ico_cate_convenience"></i>생활편의</a><a
						href="#" class="_linkCategory" data-nclicks="scn.sights" data-category="SIGHTS"><i class="ico_cate_touristattraction"></i>명소</a><a
						href="#" class="_linkCategory" data-nclicks="scn.sports" data-category="SPORT"><i class="ico_cate_sport"></i>체육시설</a><a
						href="#" class="_linkCategory" data-nclicks="scn.movie" data-category="CINEMA"><i class="ico_cate_cinema"></i>영화공연</a><a
						href="#" class="_linkCategory" data-nclicks="scn.office" data-category="GOVERNMENT"><i class="ico_cate_government"></i>관공서</a></div>
			</div>
			
			<div class="_searchHistoryDiv">
				<!-- 최근검색 리스트 -->
				<div class="search_atcmp_wrap _searchHistory">
					<div class="bx_atmp">
						<strong class="u_skip">최근검색어</strong>
						<ul class="list_atcp _historyList">
						</ul>
						<div class="atmp_btn">
							<a href="#" class="_delHistory" data-nclicks="scr.delAll">전체삭제</a>
							<span class="bar _bar">|</span>
							<a href="#" class="_offHistory" data-nclicks="scr.auto">자동저장 끄기</a>
						</div>
					</div>
				</div>
				<!-- //최근검색 리스트 -->
				
				<!-- 최근검색 결과없음 -->
				<div class="search_atcmp_wrap search_error_wrap _noHistory" style="display:none;">
					<div class="bx_atmp">
						<p class="msg_atcmp">
							<span class="sp_map spr_ico_msg2"></span>
							최근 검색 기록이 없습니다.
						</p>
						<div class="atmp_btn">
							<a href="#" class="_offHistory" data-nclicks="scr.auto">자동저장 끄기</a>
						</div>
					</div>
				</div>
				
				<!-- 최근검색기능 꺼짐상태알림 -->
				<div class="search_atcmp_wrap search_error_wrap _offedHistory" style="display:none;">
					<div class="bx_atmp">
						<p class="msg_atcmp">
							<span class="sp_map spr_ico_msg2"></span>
							최근 검색어 저장 기능이<br />
							꺼져 있습니다.
						</p>
						<div class="atmp_btn">
							<a href="#" class="_onHistory" data-nclicks="scr.auto">자동저장 켜기</a>
						</div>
					</div>
				</div>
				
			</div>
			
			<div class="search_atcmp_wrap _ac_layer" style="display:none;">
				<div class="bx_atmp">		
					<strong class="u_skip">자동완성 검색어</strong>
					<!-- 자동완성 목록 템플릿 start-->
					<ul class="list_atcp"></ul>
					<!-- 자동완성 목록 템플릿 end -->
				</div>
			</div>
		</div>
	</div>
	<!--// 키워드검색 -->	
	
<!--// 검색 영역 -->




<div class="search_listview _content _ctList">
	

	<!-- 연관검색어/검색어교정 -->
	<div style="display:none;">
		<div class="map_search_keyword _correctWord">
			<strong>제안</strong>
		</div>
	</div>
	<div style="display:none;">
		<div class="map_search_keyword _relationWord">
			<strong>연관</strong>
			<span class="_relationWordList"></span><span class="_relationWordEnd" style="width:1px; height:1px;"></span>
		</div>
	</div>
	<!-- //연관검색어/검색어교정 -->

	<!-- 다른위치 -->
	
	
	<!-- //다른위치 -->
	<div class="search_list_head">
		




<!-- 위치기반  -->
<div class="map_search_location _textComponents" style="display:none">
	
	<strong id="_currentLocation">정자동</strong>
	<div class="location_btn">
		<a href="#" id="_myLocation" class="a_lct" data-nclicks="stp.LOChere"><i class="ico_mylct"></i>내위치</a><a href="#" class="a_sel" id="_changeLocation" data-nclicks="stp.LOCopen">변경</a>
	</div>
</div>

<script type="text/javascript" src="https://ssl.pstatic.net/sstatic.map/widget/scripts/nlocation-widget-1.3.0.js?_v1608785351430"></script>

<script type="text/javascript">
	
	nhn.map.mobile.SelectedSearchPosition = {
		__xpos: "",
		__ypos: "",
		__name: "",
		isExist : function(){
			return (!this.__xpos || !this.__ypos) == false;
		},
		getPosition : function(){
			return {
				name : this.__name +"",
				lng : this.__xpos + "",
				lat : this.__ypos + ""
			}
		}
	};

	
	var currentPage = 'localSearch';

	
	var locationListJson = {
  "currentLocation": null,
  "locationList": [
  ]
};
	var recents = [];

	var locationList = locationListJson.locationList || [];

	for (var i = 0; i < locationList.length; i++){
		recent = {};
		recent.latitude = locationList[i].ypos;
		recent.longitude = locationList[i].xpos;
		recent.name = locationList[i].placeName;

		if (locationList[i].region){
			recent.si = locationList[i].region.si;
			recent.dong = locationList[i].region.dong;
		}

		recents.push(recent);
	}

	if (recents.length == 0) {
		recents = null;
	}

	
	var options = {
			myLocationSuccess: onMyLocationSuccess,
            changeLocationSuccess: onChangeAndRecentLocationSuccess,
            recentLocationSuccess: onChangeAndRecentLocationSuccess,
            serviceName: 'map',
        	myLocationEl: $('#_myLocation')[0],
        	changeLocationEl: $("#_changeLocation")[0],
        	currentLocationEl: $("#_currentLocation")[0],
	        recents: recents,
	        mode: 'real',
			setCookie: true
	    };

	
	new naver.map.api.Geolocation(options);

	
	function onMyLocationSuccess(data) {
		if (currentPage == 'main'){
			reloadMainPageWithCenterCoord(data.latitude, data.longitude);
		}else{
			reloadPageWithCenterCoord(data.latitude, data.longitude);
		}
	}

	function onChangeAndRecentLocationSuccess(data) {
		if (currentPage == 'main'){
   			reloadMainPageWithoutCenterCoord();
   		}else{
   			reloadPageWithoutCenterCoord();
   		}
	}

	
	function reloadMainPageWithCenterCoord(latitude, longitude) {
		var url = "/?centerCoord=" + latitude + ":" + longitude;
		location.href = url;
	}

	function reloadMainPageWithoutCenterCoord() {
		var url = '/';
		location.href = url;
	}

	function reloadPageWithCenterCoord(latitude, longitude) {
		var url = nhn.map.mobile.URLHelper.getCurrentUrlWithAdditionalParam("sm=clk&centerCoord=" + latitude + ":" + longitude);
		location.href = url;
	}

	function reloadPageWithoutCenterCoord() {
		var params = convertQueryStringToObj(location.search);
		var url = location.protocol + '//' + location.host + location.pathname;

		var paramArr = [];

		for (key in params) {
			if (key !== 'centerCoord' && key !== '?centerCoord') {
				paramArr.push(key + '=' + params[key]);
			}
		}

		location.href = url + paramArr.join("&");
	}

	function convertQueryStringToObj(queryStr) {
		var aKVList = queryStr.split("&");
		var obj = {};
		for (var i = 0 ; i < aKVList.length; i++) {
			var KV = aKVList[i].split("=");
			if (KV.length != 2){
				continue;
			}
			obj[KV[0]] = decodeURIComponent(KV[1]);
		}
		return obj;
	}
</script>

		<!-- 검색 결과 -->
		<div class="_resultQuery"></div>
		<!-- //검색 결과 -->

		<!-- 재검색 -->
		<div class="_linkQuery"></div>
		<!-- //재검색 -->

		
	</div>

	<div class="search_list_info _pollingPlaceInfo" style="display:none">
		<p>실제 투표소 정보와 차이가 있을 수 있으니, <a href="http://m.nec.go.kr/m/VtMain.do">선거관리위원회</a>에서 최종 확정된 투표소 정보를 필히 확인하시기 바랍니다.</p>
	</div>

	<div class="search_list_sort _searchSort _textComponents" style="display:none">
		<input type="radio" id="sortOption0" class="_linkSort" name="sortOption" data-nclicks="plc_ntl.relevance" data-site_sort="0"><label for="sortOption0">관련도순</label>
		<input type="radio" id="sortOption1" class="_linkSort" name="sortOption" data-nclicks="plc_ntl.distance" data-site_sort="1"><label for="sortOption1">거리순</label>
		<input type="radio" id="sortOption2" class="_linkSort _petrol" name="sortOption" style="display:none" data-nclicks="plc_ntl.opunfold" data-site_sort="2" data-extension="petrolFilter=1"><label for="sortOption2" class="_petrol" style="display:none">유가순</label>
	</div>

	<div class="search_list_sort_dep2 _petrolFilterOption" style="display:none">
		<input type="radio" id="petrolFilter1" class="_linkSort" name="petrolFilterOption" data-nclicks="plc_ntl.oppetrol" data-site_sort="2" data-extension="petrolFilter=1" data-petrol_sort="1"><label for="petrolFilter1">일반휘발유</label>
		<input type="radio" id="petrolFilter2" class="_linkSort" name="petrolFilterOption" data-nclicks="plc_ntl.ophgpetrol" data-site_sort="2" data-extension="petrolFilter=2" data-petrol_sort="2"><label for="petrolFilter2">고급휘발유</label>
		<input type="radio" id="petrolFilter3" class="_linkSort" name="petrolFilterOption" data-nclicks="plc_ntl.opdiesel" data-site_sort="2" data-extension="petrolFilter=3" data-petrol_sort="3"><label for="petrolFilter3">경유</label>
		<input type="radio" id="petrolFilter4" class="_linkSort" name="petrolFilterOption" data-nclicks="plc_ntl.oplpg" data-site_sort="2" data-extension="petrolFilter=4" data-petrol_sort="4"><label for="petrolFilter4">LPG</label>
	</div>

	<ul class="search_list _items">
	<!-- 업체 출력 List (search.tpl.xml[js]로 이동)-->
		
	</ul>

	<a href="#" data-nclicks="plc_ntl.more" class="btn_search_list_mr _moreBtn" style="display:none">15개 더보기<i class="ico_arrw"></i></a>

	<p class="search_list_msg _requestMoreMsg" style="display:none">&nbsp;</p>

	<div class="search_list_loading _loadingMsg" style="display:none">
		<img src="https://ssl.pstatic.net/static/maps/m/loading_bg.gif" width="20" height="20" alt="로딩중">
	</div>

	<p class="search_list_msg _limitSearch" style="display:none"><i class="ico_i"></i>최대 75개의 검색결과를 제공합니다.</p>

	<a href="#" class="sp_map btn_top _top" style="display:none">TOP</a>
</div>


<hr />
</div>

<hr />

<div class="btn_mapview_wrp _mapViewWrap">
	<div class="tooltip _mapViewTooltip" style="display:block">
		<span class="sp_map txt_tooltip_map">지도에서 보기</span>
	</div>
	<a href="#" class="sp_map btn_mapview _mapView" data-nclicks="plc_ntl.maplist">지도뷰 보기</a>
</div>

<script type="text/javascript">

requirejs.config({
    paths : {
        'mantle' : '/openapi/maps3.js?_v1603082058665',
        'mobile_map_service' : '/js/mobile_map_service_v1608785351430',
        'like_api' : 'https://common.like.naver.com/static/js/likeIt.list.js?v=20201225',
        'search' : '/js/search2_v1608785351430'
    },
    shim: {
        'search': {
            deps: ['like_api'],
            exports: 'nhn.map.mobile.search'
        },
        'mobile_map_service': {
            deps: ['mantle']
        }
    }
});
window.__splugin = new nhn.map.mobile.SocialPlugin2();

requirejs(['search'], function(search) {
	var searchResult = {   "site": {     "sort": "0",     "petrolFilter": null,     "isPetrol": false,     "isIndoorSearch": false,     "distanceSortYN": "1",     "page": 1,     "list": [       {         "index": "0",         "rank": "1",         "id": "s33169366",         "name": "시골향기",         "tel": "031-997-6993",         "isCallLink": false,         "virtualTel": "",         "ppc": "1",         "category": [           "음식점",           "한식"         ],         "address": "경기도 김포시 고촌읍 신곡리 447-75",         "roadAddress": "경기도 김포시 고촌읍 신곡로 114-8",         "abbrAddress": "신곡리 447-75",         "display": "<b>시골향기</b>",         "telDisplay": "031-997-6993",         "ktCallMd": "1e28d7fd80478a7eed185f4ac339b115",         "coupon": "0",         "thumUrl": "http://blogfiles.naver.net/20160705_72/balloonjoo_1467706696106oCtJK_JPEG/image_9828304361467706576936.jpg#3000x2252",         "type": "s",         "isSite": "1",         "posExact": "1",         "x": "126.7672751",         "y": "37.6076334",         "itemLevel": "12",         "streetPanorama": {           "id": "fg++Fj4DOHh224xgJ03zXQ==",           "pan": "-16.34",           "tilt": "12.38",           "lng": "126.7673697",           "lat": "37.6072502",           "fov": "50"         },         "skyPanorama": {           "id": "77YNvQ07FmgfZaFI9IaNLQ==",           "pan": "-18.09",           "tilt": "-30.00",           "lng": "126.7681351",           "lat": "37.6049995",           "fov": "124"         },         "insidePanorama": null,         "interiorPanorama": null,         "indoorPanorama": null,         "theme": null,         "poiInfo": {           "road": {             "poiShapeType": "1",             "shapeKey": null,             "boundary": null,             "detail": null           },           "hasRoad": false,           "land": null,           "hasLand": false,           "polygon": null,           "hasPolygon": false         },         "homePage": "",         "description": "",         "entranceCoords": {           "car": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "126.7670540",               "entranceCoordY": "37.6075420",               "coordSubType": 1             }           ],           "walk": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "126.7670540",               "entranceCoordY": "37.6075420",               "coordSubType": 1             }           ]         },         "isPollingPlace": false,         "bizhourInfo": null,         "menuInfo": null,         "petrolInfo": null,         "couponUrl": null,         "couponUrlMobile": null,         "hasCardBenefit": false,         "indoor": {           "floor": "0",           "underGmid": "0",           "underMid": "0"         },         "indoorMapInfo": null,         "x1": null,         "x2": null,         "menuExist": "1",         "hasNaverBooking": false,         "naverBookingUrl": null,         "hasBroadcastInfo": false,         "broadcastInfo": {           "name": null,           "menu": null         },         "shopWindowInfo": null,         "hasNPay": false,         "naverEasyOrderUrl": null,         "distance": "19169.64"       },       {         "index": "1",         "rank": "2",         "id": "s37522242",         "name": "시골향기",         "tel": "031-997-7579",         "isCallLink": false,         "virtualTel": "",         "ppc": "1",         "category": [           "음식점",           "한식"         ],         "address": "경기도 김포시 운양동 117-8",         "roadAddress": "경기도 김포시 걸포로 182",         "abbrAddress": "운양동 117-8",         "display": "<b>시골향기</b>",         "telDisplay": "031-997-7579",         "ktCallMd": "c554f7693d888acb10297422c40d56fd",         "coupon": "0",         "thumUrl": null,         "type": "s",         "isSite": "1",         "posExact": "1",         "x": "126.7009259",         "y": "37.6468403",         "itemLevel": "12",         "streetPanorama": {           "id": "88ncOKd7WqxqS+7xDqDxbA==",           "pan": "82.77",           "tilt": "3.76",           "lng": "126.7006070",           "lat": "37.6468650",           "fov": "80"         },         "skyPanorama": {           "id": "onhxhmikBJ4eMvWsYtc8zQ==",           "pan": "140.35",           "tilt": "-30.00",           "lng": "126.7002290",           "lat": "37.6476790",           "fov": "124"         },         "insidePanorama": null,         "interiorPanorama": null,         "indoorPanorama": null,         "theme": null,         "poiInfo": {           "road": {             "poiShapeType": "1",             "shapeKey": null,             "boundary": null,             "detail": null           },           "hasRoad": false,           "land": null,           "hasLand": false,           "polygon": null,           "hasPolygon": false         },         "homePage": "",         "description": "",         "entranceCoords": {           "car": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "126.7007060",               "entranceCoordY": "37.6469470",               "coordSubType": 1             }           ],           "walk": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "126.7007060",               "entranceCoordY": "37.6469470",               "coordSubType": 1             }           ]         },         "isPollingPlace": false,         "bizhourInfo": null,         "menuInfo": null,         "petrolInfo": null,         "couponUrl": null,         "couponUrlMobile": null,         "hasCardBenefit": false,         "indoor": {           "floor": "0",           "underGmid": "0",           "underMid": "0"         },         "indoorMapInfo": null,         "x1": null,         "x2": null,         "menuExist": "1",         "hasNaverBooking": false,         "naverBookingUrl": null,         "hasBroadcastInfo": false,         "broadcastInfo": {           "name": null,           "menu": null         },         "shopWindowInfo": null,         "hasNPay": false,         "naverEasyOrderUrl": null,         "distance": "26041.48"       },       {         "index": "2",         "rank": "3",         "id": "s1196811393",         "name": "시골향기 작동점",         "tel": "032-675-7077",         "isCallLink": false,         "virtualTel": "0507-1322-7077",         "ppc": "1",         "category": [           "음식점",           "한식"         ],         "address": "경기도 부천시 작동 147",         "roadAddress": "경기도 부천시 여월로 202",         "abbrAddress": "작동 147",         "display": "<b>시골향기</b> 작동점",         "telDisplay": "032-675-7077",         "ktCallMd": "c4fcb39f03cc867bc411504fe195a74e",         "coupon": "0",         "thumUrl": "https://ldb-phinf.pstatic.net/20180427_68/1524813541125O3wzr_JPEG/7Vvyn8MRl1TEWRqTS0Q1GywK.jpg",         "type": "s",         "isSite": "1",         "posExact": "1",         "x": "126.8208205",         "y": "37.5129767",         "itemLevel": "12",         "streetPanorama": {           "id": "K23KNo6Cw0W1ObIaF19h4A==",           "pan": "175.40",           "tilt": "10.00",           "lng": "126.8208023",           "lat": "37.5131991",           "fov": "120"         },         "skyPanorama": null,         "insidePanorama": null,         "interiorPanorama": null,         "indoorPanorama": null,         "theme": null,         "poiInfo": {           "road": {             "poiShapeType": "1",             "shapeKey": null,             "boundary": null,             "detail": null           },           "hasRoad": false,           "land": null,           "hasLand": false,           "polygon": null,           "hasPolygon": false         },         "homePage": "",         "description": "",         "entranceCoords": {           "car": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "126.8207590",               "entranceCoordY": "37.5130700",               "coordSubType": 1             }           ],           "walk": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "126.8207590",               "entranceCoordY": "37.5130700",               "coordSubType": 1             }           ]         },         "isPollingPlace": false,         "bizhourInfo": null,         "menuInfo": null,         "petrolInfo": null,         "couponUrl": null,         "couponUrlMobile": null,         "hasCardBenefit": false,         "indoor": {           "floor": "0",           "underGmid": "0",           "underMid": "0"         },         "indoorMapInfo": null,         "x1": null,         "x2": null,         "menuExist": "1",         "hasNaverBooking": false,         "naverBookingUrl": null,         "hasBroadcastInfo": false,         "broadcastInfo": {           "name": null,           "menu": null         },         "shopWindowInfo": null,         "hasNPay": false,         "naverEasyOrderUrl": null,         "distance": "15131.72"       },       {         "index": "3",         "rank": "4",         "id": "s1859636272",         "name": "시골향기 인덕원포일점",         "tel": "031-421-6001",         "isCallLink": false,         "virtualTel": "0507-1497-6001",         "ppc": "1",         "category": [           "한식",           "보리밥"         ],         "address": "경기도 의왕시 포일동 503-1 2층",         "roadAddress": "경기도 의왕시 안양판교로 115 2층",         "abbrAddress": "포일동 503-1 2층",         "display": "<b>시골향기</b> 인덕원포일점",         "telDisplay": "031-421-6001",         "ktCallMd": "dc49441c8b88d04cb241cae099c1589b",         "coupon": "0",         "thumUrl": "https://ldb-phinf.pstatic.net/20190509_100/1557381350101Mm9CI_JPEG/5j3_Vc6-r4dnUTPZi8VkexT2.jpg",         "type": "s",         "isSite": "1",         "posExact": "1",         "x": "126.9861986",         "y": "37.3944706",         "itemLevel": "12",         "streetPanorama": {           "id": "3tqnOmT2dCAehb/u3XwjxQ==",           "pan": "46.69",           "tilt": "10.00",           "lng": "126.9860570",           "lat": "37.3943370",           "fov": "120"         },         "skyPanorama": null,         "insidePanorama": null,         "interiorPanorama": null,         "indoorPanorama": null,         "theme": null,         "poiInfo": {           "road": {             "poiShapeType": "1",             "shapeKey": null,             "boundary": null,             "detail": null           },           "hasRoad": false,           "land": null,           "hasLand": false,           "polygon": null,           "hasPolygon": false         },         "homePage": "",         "description": "",         "entranceCoords": {           "car": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "126.9861540",               "entranceCoordY": "37.3944170",               "coordSubType": 1             }           ],           "walk": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "126.9861540",               "entranceCoordY": "37.3944170",               "coordSubType": 1             }           ]         },         "isPollingPlace": false,         "bizhourInfo": null,         "menuInfo": null,         "petrolInfo": null,         "couponUrl": null,         "couponUrlMobile": null,         "hasCardBenefit": false,         "indoor": {           "floor": "0",           "underGmid": "0",           "underMid": "0"         },         "indoorMapInfo": null,         "x1": null,         "x2": null,         "menuExist": "1",         "hasNaverBooking": false,         "naverBookingUrl": null,         "hasBroadcastInfo": false,         "broadcastInfo": {           "name": null,           "menu": null         },         "shopWindowInfo": null,         "hasNPay": false,         "naverEasyOrderUrl": null,         "distance": "19170.00"       },       {         "index": "4",         "rank": "5",         "id": "s36761406",         "name": "시골향기손두부",         "tel": "",         "isCallLink": false,         "virtualTel": "",         "ppc": "0",         "category": [           "한식",           "두부요리"         ],         "address": "경기도 고양시 일산서구 법곳동 1734-8",         "roadAddress": "경기도 고양시 일산서구 법곳길 146",         "abbrAddress": "법곳동 1734-8",         "display": "<b>시골향기</b>손두부",         "telDisplay": "",         "ktCallMd": "d9480b777f68c7c70122d73b94d33806",         "coupon": "0",         "thumUrl": null,         "type": "s",         "isSite": "1",         "posExact": "1",         "x": "126.7225753",         "y": "37.6628940",         "itemLevel": "12",         "streetPanorama": {           "id": "nWM+MC2RUIB+SX/MHy99OQ==",           "pan": "42.15",           "tilt": "10.00",           "lng": "126.7224937",           "lat": "37.6628038",           "fov": "120"         },         "skyPanorama": {           "id": "FfVSrBN/7IQtzVAh0uXgCA==",           "pan": "-76.29",           "tilt": "-30.00",           "lng": "126.7244415",           "lat": "37.6624374",           "fov": "124"         },         "insidePanorama": null,         "interiorPanorama": null,         "indoorPanorama": null,         "theme": null,         "poiInfo": {           "road": {             "poiShapeType": "1",             "shapeKey": null,             "boundary": null,             "detail": null           },           "hasRoad": false,           "land": null,           "hasLand": false,           "polygon": null,           "hasPolygon": false         },         "homePage": "",         "description": "",         "entranceCoords": {           "car": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "126.7225250",               "entranceCoordY": "37.6628220",               "coordSubType": 5             }           ],           "walk": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "126.7225250",               "entranceCoordY": "37.6628220",               "coordSubType": 5             }           ]         },         "isPollingPlace": false,         "bizhourInfo": null,         "menuInfo": null,         "petrolInfo": null,         "couponUrl": null,         "couponUrlMobile": null,         "hasCardBenefit": false,         "indoor": {           "floor": "0",           "underGmid": "0",           "underMid": "0"         },         "indoorMapInfo": null,         "x1": null,         "x2": null,         "menuExist": "0",         "hasNaverBooking": false,         "naverBookingUrl": null,         "hasBroadcastInfo": false,         "broadcastInfo": {           "name": null,           "menu": null         },         "shopWindowInfo": null,         "hasNPay": false,         "naverEasyOrderUrl": null,         "distance": "24968.02"       },       {         "index": "5",         "rank": "6",         "id": "s1882741956",         "name": "시골향기",         "tel": "031-584-5121",         "isCallLink": false,         "virtualTel": "",         "ppc": "1",         "category": [           "카페,디저트",           "다방"         ],         "address": "경기도 가평군 상면 연하리 180-4",         "roadAddress": "경기도 가평군 상면 기와집길 7 복식당",         "abbrAddress": "연하리 180-4",         "display": "<b>시골향기</b>",         "telDisplay": "031-584-5121",         "ktCallMd": "8b0d5b2708f758166b9d221deb22d21e",         "coupon": "0",         "thumUrl": null,         "type": "s",         "isSite": "1",         "posExact": "1",         "x": "127.3560383",         "y": "37.8052139",         "itemLevel": "12",         "streetPanorama": {           "id": "fRHeDcyQxwoSpeXJJXUlYw==",           "pan": "-177.28",           "tilt": "10.00",           "lng": "127.3560459",           "lat": "37.8053680",           "fov": "120"         },         "skyPanorama": null,         "insidePanorama": null,         "interiorPanorama": null,         "indoorPanorama": null,         "theme": null,         "poiInfo": {           "road": {             "poiShapeType": "1",             "shapeKey": null,             "boundary": null,             "detail": null           },           "hasRoad": false,           "land": null,           "hasLand": false,           "polygon": null,           "hasPolygon": false         },         "homePage": "",         "description": "",         "entranceCoords": {           "car": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "127.3560510",               "entranceCoordY": "37.8053260",               "coordSubType": 5             }           ],           "walk": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "127.3560510",               "entranceCoordY": "37.8053260",               "coordSubType": 5             }           ]         },         "isPollingPlace": false,         "bizhourInfo": null,         "menuInfo": null,         "petrolInfo": null,         "couponUrl": null,         "couponUrlMobile": null,         "hasCardBenefit": false,         "indoor": {           "floor": "0",           "underGmid": "0",           "underMid": "0"         },         "indoorMapInfo": null,         "x1": null,         "x2": null,         "menuExist": "0",         "hasNaverBooking": false,         "naverBookingUrl": null,         "hasBroadcastInfo": false,         "broadcastInfo": {           "name": null,           "menu": null         },         "shopWindowInfo": null,         "hasNPay": false,         "naverEasyOrderUrl": null,         "distance": "42560.58"       },       {         "index": "6",         "rank": "7",         "id": "s20467365",         "name": "시골향기",         "tel": "041-752-1101",         "isCallLink": false,         "virtualTel": "",         "ppc": "1",         "category": [           "음식점",           "한식"         ],         "address": "충청남도 금산군 금산읍 중도리 485-4",         "roadAddress": "충청남도 금산군 금산읍 건삼전길 23-1",         "abbrAddress": "중도리 485-4",         "display": "<b>시골향기</b>",         "telDisplay": "041-752-1101",         "ktCallMd": "2380c0147309b574fdea50d27488c7fa",         "coupon": "0",         "thumUrl": null,         "type": "s",         "isSite": "1",         "posExact": "1",         "x": "127.4909360",         "y": "36.1010795",         "itemLevel": "12",         "streetPanorama": {           "id": "aZ5Le/EyX5uW2HKD+9CTeQ==",           "pan": "-86.27",           "tilt": "10.00",           "lng": "127.4910512",           "lat": "36.1010719",           "fov": "120"         },         "skyPanorama": null,         "insidePanorama": null,         "interiorPanorama": null,         "indoorPanorama": null,         "theme": null,         "poiInfo": {           "road": {             "poiShapeType": "1",             "shapeKey": null,             "boundary": null,             "detail": null           },           "hasRoad": false,           "land": null,           "hasLand": false,           "polygon": null,           "hasPolygon": false         },         "homePage": "",         "description": "",         "entranceCoords": null,         "isPollingPlace": false,         "bizhourInfo": null,         "menuInfo": null,         "petrolInfo": null,         "couponUrl": null,         "couponUrlMobile": null,         "hasCardBenefit": false,         "indoor": {           "floor": "0",           "underGmid": "0",           "underMid": "0"         },         "indoorMapInfo": null,         "x1": null,         "x2": null,         "menuExist": "0",         "hasNaverBooking": false,         "naverBookingUrl": null,         "hasBroadcastInfo": false,         "broadcastInfo": {           "name": null,           "menu": null         },         "shopWindowInfo": null,         "hasNPay": false,         "naverEasyOrderUrl": null,         "distance": "169368.75"       },       {         "index": "7",         "rank": "8",         "id": "s1471858967",         "name": "시골향기민박",         "tel": "061-262-7770",         "isCallLink": false,         "virtualTel": "",         "ppc": "1",         "category": [           "숙박",           "민박"         ],         "address": "전라남도 신안군 자은면 송산리 308-1",         "roadAddress": "전라남도 신안군 자은면 두봉길 711",         "abbrAddress": "송산리 308-1",         "display": "<b>시골향기</b>민박",         "telDisplay": "061-262-7770",         "ktCallMd": "178e8cde124a638f5fc77b0005f68ae0",         "coupon": "0",         "thumUrl": "http://ldb.phinf.naver.net/20190811_101/1565533999539dKIHL_JPEG/1zdbxgiYrBEnki5fZ49WS3JV.jpg",         "type": "s",         "isSite": "1",         "posExact": "1",         "x": "126.0660936",         "y": "34.9118308",         "itemLevel": "10",         "streetPanorama": {           "id": "aiK+gwJr57/2Yt9XAFvTmQ==",           "pan": "-108.79",           "tilt": "10.00",           "lng": "126.0664453",           "lat": "34.9119501",           "fov": "120"         },         "skyPanorama": {           "id": "93Wo+qpXxKJsOx0WWKxwpQ==",           "pan": "131.33",           "tilt": "-30.00",           "lng": "126.0651600",           "lat": "34.9126500",           "fov": "124"         },         "insidePanorama": null,         "interiorPanorama": null,         "indoorPanorama": null,         "theme": null,         "poiInfo": {           "road": {             "poiShapeType": "1",             "shapeKey": null,             "boundary": null,             "detail": null           },           "hasRoad": false,           "land": null,           "hasLand": false,           "polygon": null,           "hasPolygon": false         },         "homePage": "",         "description": "",         "entranceCoords": {           "car": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "126.0663520",               "entranceCoordY": "34.9119610",               "coordSubType": 1             }           ],           "walk": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "126.0663520",               "entranceCoordY": "34.9119610",               "coordSubType": 1             }           ]         },         "isPollingPlace": false,         "bizhourInfo": null,         "menuInfo": null,         "petrolInfo": null,         "couponUrl": null,         "couponUrlMobile": null,         "hasCardBenefit": false,         "indoor": {           "floor": "0",           "underGmid": "0",           "underMid": "0"         },         "indoorMapInfo": null,         "x1": null,         "x2": null,         "menuExist": "0",         "hasNaverBooking": false,         "naverBookingUrl": null,         "hasBroadcastInfo": false,         "broadcastInfo": {           "name": null,           "menu": null         },         "shopWindowInfo": null,         "hasNPay": false,         "naverEasyOrderUrl": null,         "distance": "306586.25"       },       {         "index": "8",         "rank": "9",         "id": "s38457381",         "name": "시골향기",         "tel": "010-9194-1420",         "isCallLink": false,         "virtualTel": "0507-1407-1420",         "ppc": "1",         "category": [           "쇼핑,유통",           "가공식품"         ],         "address": "전라남도 신안군 자은면 송산리 308-1",         "roadAddress": "전라남도 신안군 자은면 두봉길 711",         "abbrAddress": "송산리 308-1",         "display": "<b>시골향기</b>",         "telDisplay": "010-9194-1420",         "ktCallMd": "142c7637b86cae57b576757ecaccf27d",         "coupon": "0",         "thumUrl": "http://ldb.phinf.naver.net/20170309_94/1489046102173TaxIh_JPEG/1.jpg",         "type": "s",         "isSite": "1",         "posExact": "1",         "x": "126.0660936",         "y": "34.9118308",         "itemLevel": "10",         "streetPanorama": {           "id": "aiK+gwJr57/2Yt9XAFvTmQ==",           "pan": "-108.79",           "tilt": "10.00",           "lng": "126.0664453",           "lat": "34.9119501",           "fov": "120"         },         "skyPanorama": {           "id": "93Wo+qpXxKJsOx0WWKxwpQ==",           "pan": "131.33",           "tilt": "-30.00",           "lng": "126.0651600",           "lat": "34.9126500",           "fov": "124"         },         "insidePanorama": null,         "interiorPanorama": null,         "indoorPanorama": null,         "theme": null,         "poiInfo": {           "road": {             "poiShapeType": "1",             "shapeKey": null,             "boundary": null,             "detail": null           },           "hasRoad": false,           "land": null,           "hasLand": false,           "polygon": null,           "hasPolygon": false         },         "homePage": "http://blog.daum.net/kingsongh",         "description": "",         "entranceCoords": {           "car": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "126.0663520",               "entranceCoordY": "34.9119610",               "coordSubType": 1             }           ],           "walk": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "126.0663520",               "entranceCoordY": "34.9119610",               "coordSubType": 1             }           ]         },         "isPollingPlace": false,         "bizhourInfo": null,         "menuInfo": null,         "petrolInfo": null,         "couponUrl": null,         "couponUrlMobile": null,         "hasCardBenefit": false,         "indoor": {           "floor": "0",           "underGmid": "0",           "underMid": "0"         },         "indoorMapInfo": null,         "x1": null,         "x2": null,         "menuExist": "1",         "hasNaverBooking": false,         "naverBookingUrl": null,         "hasBroadcastInfo": false,         "broadcastInfo": {           "name": null,           "menu": null         },         "shopWindowInfo": null,         "hasNPay": false,         "naverEasyOrderUrl": null,         "distance": "306586.25"       },       {         "index": "9",         "rank": "10",         "id": "s37951872",         "name": "시골향기",         "tel": "",         "isCallLink": false,         "virtualTel": "",         "ppc": "0",         "category": [           "쇼핑,유통",           "식료품"         ],         "address": "부산광역시 동래구 사직동 44-1",         "roadAddress": "부산광역시 동래구 사직북로33번길 31",         "abbrAddress": "사직동 44-1",         "display": "<b>시골향기</b>",         "telDisplay": "",         "ktCallMd": "7852b2c85bc4c30b7b76f36e814e9549",         "coupon": "0",         "thumUrl": null,         "type": "s",         "isSite": "1",         "posExact": "1",         "x": "129.0581653",         "y": "35.1984936",         "itemLevel": "12",         "streetPanorama": {           "id": "aBH7OO5NVVUTPCSgD5WkqA==",           "pan": "174.84",           "tilt": "10.00",           "lng": "129.0581552",           "lat": "35.1986045",           "fov": "120"         },         "skyPanorama": {           "id": "2aJ1s031a+PTYGPQoSLF4A==",           "pan": "168.68",           "tilt": "-30.00",           "lng": "129.0576935",           "lat": "35.2008324",           "fov": "124"         },         "insidePanorama": null,         "interiorPanorama": null,         "indoorPanorama": null,         "theme": null,         "poiInfo": {           "road": {             "poiShapeType": "1",             "shapeKey": null,             "boundary": null,             "detail": null           },           "hasRoad": false,           "land": null,           "hasLand": false,           "polygon": null,           "hasPolygon": false         },         "homePage": "",         "description": "",         "entranceCoords": {           "car": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "129.0583140",               "entranceCoordY": "35.1984970",               "coordSubType": 5             }           ],           "walk": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "129.0583140",               "entranceCoordY": "35.1984970",               "coordSubType": 5             },             {               "isRepresentative": "0",               "coordType": "2",               "entranceCoordX": "129.0585950",               "entranceCoordY": "35.1983970",               "coordSubType": 5             }           ]         },         "isPollingPlace": false,         "bizhourInfo": null,         "menuInfo": null,         "petrolInfo": null,         "couponUrl": null,         "couponUrlMobile": null,         "hasCardBenefit": false,         "indoor": {           "floor": "0",           "underGmid": "0",           "underMid": "0"         },         "indoorMapInfo": null,         "x1": null,         "x2": null,         "menuExist": "0",         "hasNaverBooking": false,         "naverBookingUrl": null,         "hasBroadcastInfo": false,         "broadcastInfo": {           "name": null,           "menu": null         },         "shopWindowInfo": null,         "hasNPay": false,         "naverEasyOrderUrl": null,         "distance": "322750.43"       },       {         "index": "10",         "rank": "11",         "id": "s16744568",         "name": "시골향기",         "tel": "061-772-7177",         "isCallLink": false,         "virtualTel": "",         "ppc": "1",         "category": [           "농업",           "채소재배"         ],         "address": "전라남도 광양시 진월면 월길리 640",         "roadAddress": "전라남도 광양시 진월면 대리동백길 29-6",         "abbrAddress": "월길리 640",         "display": "<b>시골향기</b>",         "telDisplay": "061-772-7177",         "ktCallMd": "b1374b31f1cfb8b80b1be28cd7a3b64b",         "coupon": "0",         "thumUrl": null,         "type": "s",         "isSite": "1",         "posExact": "1",         "x": "127.7552853",         "y": "35.0364710",         "itemLevel": "12",         "streetPanorama": null,         "skyPanorama": null,         "insidePanorama": null,         "interiorPanorama": null,         "indoorPanorama": null,         "theme": null,         "poiInfo": {           "road": {             "poiShapeType": "1",             "shapeKey": null,             "boundary": null,             "detail": null           },           "hasRoad": false,           "land": null,           "hasLand": false,           "polygon": null,           "hasPolygon": false         },         "homePage": "",         "description": "",         "entranceCoords": null,         "isPollingPlace": false,         "bizhourInfo": null,         "menuInfo": null,         "petrolInfo": null,         "couponUrl": null,         "couponUrlMobile": null,         "hasCardBenefit": false,         "indoor": {           "floor": "0",           "underGmid": "0",           "underMid": "0"         },         "indoorMapInfo": null,         "x1": null,         "x2": null,         "menuExist": "0",         "hasNaverBooking": false,         "naverBookingUrl": null,         "hasBroadcastInfo": false,         "broadcastInfo": {           "name": null,           "menu": null         },         "shopWindowInfo": null,         "hasNPay": false,         "naverEasyOrderUrl": null,         "distance": "290071.43"       },       {         "index": "11",         "rank": "12",         "id": "s226613354",         "name": "시골향기민박",         "tel": "",         "isCallLink": false,         "virtualTel": "",         "ppc": "0",         "category": [           "숙박",           "민박"         ],         "address": "강원도 삼척시 근덕면 용화리 219",         "roadAddress": "강원도 삼척시 근덕면 용화해변1길 23",         "abbrAddress": "용화리 219",         "display": "<b>시골향기</b>민박",         "telDisplay": "",         "ktCallMd": "a94ef2ad3754f43a3674f7fcac631603",         "coupon": "0",         "thumUrl": null,         "type": "s",         "isSite": "1",         "posExact": "1",         "x": "129.3049676",         "y": "37.2891873",         "itemLevel": "12",         "streetPanorama": {           "id": "zK9cyM/OwJjwFwRblMX5gg==",           "pan": "3.00",           "tilt": "10.00",           "lng": "129.3049619",           "lat": "37.2890784",           "fov": "120"         },         "skyPanorama": {           "id": "iBPzO/4r+yuJxCD1tORdCQ==",           "pan": "-19.43",           "tilt": "-30.00",           "lng": "129.3053961",           "lat": "37.2879719",           "fov": "124"         },         "insidePanorama": null,         "interiorPanorama": null,         "indoorPanorama": null,         "theme": null,         "poiInfo": {           "road": {             "poiShapeType": "1",             "shapeKey": null,             "boundary": null,             "detail": null           },           "hasRoad": false,           "land": null,           "hasLand": false,           "polygon": null,           "hasPolygon": false         },         "homePage": "",         "description": "",         "entranceCoords": {           "car": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "129.3050420",               "entranceCoordY": "37.2891070",               "coordSubType": 1             }           ],           "walk": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "129.3050420",               "entranceCoordY": "37.2891070",               "coordSubType": 1             }           ]         },         "isPollingPlace": false,         "bizhourInfo": null,         "menuInfo": null,         "petrolInfo": null,         "couponUrl": null,         "couponUrlMobile": null,         "hasCardBenefit": false,         "indoor": {           "floor": "0",           "underGmid": "0",           "underMid": "0"         },         "indoorMapInfo": null,         "x1": null,         "x2": null,         "menuExist": "0",         "hasNaverBooking": false,         "naverBookingUrl": null,         "hasBroadcastInfo": false,         "broadcastInfo": {           "name": null,           "menu": null         },         "shopWindowInfo": null,         "hasNPay": false,         "naverEasyOrderUrl": null,         "distance": "207918.28"       },       {         "index": "12",         "rank": "13",         "id": "s36321055",         "name": "오즈 포메라니안",         "tel": "010-6360-1244",         "isCallLink": false,         "virtualTel": "",         "ppc": "1",         "category": [           "반려동물",           "반려동물분양"         ],         "address": "충청북도 영동군 황간면 소계리 268-2",         "roadAddress": "충청북도 영동군 황간면 민주지산로 4021",         "abbrAddress": "소계리 268-2",         "display": "오즈 포메라니안",         "telDisplay": "010-6360-1244",         "ktCallMd": "6cc2a088753471ce9b013697db6683e8",         "coupon": "0",         "thumUrl": "http://ldb.phinf.naver.net/20180609_250/1528516650026bxCmP_JPEG/5.jpg",         "type": "s",         "isSite": "1",         "posExact": "1",         "x": "127.9181889",         "y": "36.2232796",         "itemLevel": "12",         "streetPanorama": {           "id": "eAzctp6LpFz1vdJNVockEg==",           "pan": "-151.26",           "tilt": "10.00",           "lng": "127.9183781",           "lat": "36.2236235",           "fov": "120"         },         "skyPanorama": null,         "insidePanorama": null,         "interiorPanorama": null,         "indoorPanorama": null,         "theme": null,         "poiInfo": {           "road": {             "poiShapeType": "1",             "shapeKey": null,             "boundary": null,             "detail": null           },           "hasRoad": false,           "land": null,           "hasLand": false,           "polygon": null,           "hasPolygon": false         },         "homePage": "http://blog.naver.com/club7749",         "description": "",         "entranceCoords": {           "car": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "127.9178750",               "entranceCoordY": "36.2237490",               "coordSubType": 1             }           ],           "walk": [             {               "isRepresentative": "1",               "coordType": "5",               "entranceCoordX": "127.9178750",               "entranceCoordY": "36.2237490",               "coordSubType": 1             }           ]         },         "isPollingPlace": false,         "bizhourInfo": null,         "menuInfo": null,         "petrolInfo": null,         "couponUrl": null,         "couponUrlMobile": null,         "hasCardBenefit": false,         "indoor": {           "floor": "0",           "underGmid": "0",           "underMid": "0"         },         "indoorMapInfo": null,         "x1": null,         "x2": null,         "menuExist": "0",         "hasNaverBooking": false,         "naverBookingUrl": null,         "hasBroadcastInfo": false,         "broadcastInfo": {           "name": null,           "menu": null         },         "shopWindowInfo": null,         "hasNPay": false,         "naverEasyOrderUrl": null,         "distance": "171306.94"       }     ],     "advertiseList": [     ]   },   "address": null,   "queryForDupRegion": "시골향기",   "lbaQuery": null,   "linkQuery": null,   "others": null,   "specificNearbySearch": null,   "siteLocation": "",   "hasPollingPlace": false,   "brandPromotion": null,   "hasSubRegion": true,   "type": "SITE_1",   "code": "0",   "rcode": null,   "totalCount": 13,   "rank": 1,   "pageId": null,   "sessionId": null,   "resultQuery": [     "<strong>'시골향기'</strong>"   ],   "adultKeywordYN": "0",   "adultConfirmYN": "1",   "adultYN": "1",   "boundary": [     "126.0660936",     "37.8052139",     "129.3049676",     "34.9118308"   ],   "searchQuery": null,   "openmapInfo": null,   "hasTimeOutResult": false,   "inputQuery": null,   "tab": [     {       "title": "장소",       "type": "SITE_1",       "rank": 1     }   ],   "relationWords": null };
	var searchService = new nhn.map.mobile.search.SearchService({
		env:{
			param:{"query":"시골향기"},
			page: {
				areaCode:"plc_ntl",
				areaCodeForVirtualTel: "plc_ntl*v",
				isAddressDetail : false,
				autoCompleteUrl: "/ac.map/mobilePlaceAddress/ac",
				displayCount: "15",
				defaultMapLevel:"",
				selectedAddress: "",
				isAvailableShowDistance: "false",
				browserType: "OTHERS",
				moreUrl: "/search2/searchMore.nhn",
				interestSiteType: "",
				selectedCategoryType: "",
				selectedCategoryName: "",
				selectedSubCategoryName: "",
				likeApiDomain: "https://common.like.naver.com",
				photoViewerDomain: "http://m.photoviewer.naver.com",
				supportNavigation: false
			},
			nclickVars : {
				textViewSSC: "m.map.listview",
				mapViewSSC: "m.map.mapview",
				textViewNSC: "Mmap.nearlist",
				mapViewNSC: "Mmap.nearmap"
			},
			gnb: {
				pcWebURL: "http://map.naver.com/?mobile&query=시골향기&searchCoord=126.9783882;37.5666103"
			}
		}
	});
	searchService.init({
		requestBean: {
			type: "ALL",
			petrolFilter: "",
			regionName: ""
		},
		result: searchResult
	});

	window.mobileDeck = new nhn.map.mobile.deck.MobileDeck({"searchBar":true});
	window.mobileDeck.showSearchKeywordView();
	window.mobileDeck.activate();

	searchService.setSearchBar(window.mobileDeck.getSearchBar());
});


BMR.run(location.protocol + "//sp.naver.com/sp");

window.addEventListener("load",
	function() {
		window.nx_usain_beacon && window.nx_usain_beacon.send("https://er.map.naver.com");
	}, false);
</script>
</body>
</html>

```

