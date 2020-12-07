select appuser.id, ulocation, uaddress, need from appuser, uneed where uneed.id=appuser.id and need='수박';




select appuser.id, appuser.ulocation, uaddress, need 
from appuser, uneed, locrelation, 
(select appuser.id, appuser.ulocation, fridge.materialname, buydate, buydate+validdays as expiredate from appuser, fridge, material where fridge.materialname=material.materialname and buydate+validdays<sysdate+3 and fridge.id='ganzi_jang' and fridge.id=appuser.id) sell
where uneed.id=appuser.id and need='수박' and sell.ulocation=adjunctlocation;



(select appuser.id, appuser.ulocation, fridge.materialname, buydate, buydate+validdays as expiredate from appuser, fridge, material where fridge.materialname=material.materialname and buydate+validdays<sysdate+3 and fridge.id='ganzi_jang' and fridge.id=appuser.id);

"ganzi_jang"



(select appuser.id, appuser.ulocation, uaddress, need 
from appuser, uneed, (select appuser.id, appuser.ulocation, fridge.materialname as mname, buydate, buydate+validdays as expiredate from appuser, fridge, material where fridge.materialname=material.materialname and buydate+validdays<sysdate+3 and fridge.id='ganzi_jang' and fridge.id=appuser.id) sell
where uneed.id=appuser.id and need=sell.mname







select buyerid, buyerlocation, need, sellerid, sellerlocation, buyeraddress from
(select appuser.id buyerid, appuser.ulocation buyerlocation, uaddress buyeraddress, need 
from appuser, uneed
where uneed.id=appuser.id) buyer,
(select sellerid, sell.ulocation sellerlocation, adjunctlocation, mname from
(select appuser.id sellerid, appuser.ulocation, fridge.materialname as mname, buydate, buydate+validdays as expiredate from appuser, fridge, material where fridge.materialname=material.materialname and buydate+validdays<sysdate+3 and fridge.id='ganzi_jang' and fridge.id=appuser.id) sell,
locrelation
where locrelation.ulocation=sell.ulocation) seller
where seller.adjunctlocation=buyerlocation and buyer.need=seller.mname;

https://maps.googleapis.com/maps/api/geocode/json?address=%EC%84%9C%EC%9A%B8%EC%8B%9C%EA%B0%95%EB%82%A8%EA%B5%AC%ED%85%8C%ED%97%A4%EB%9E%80%EB%A1%9C4&key=AIzaSyB2Kw4tAxJcTljgHshXI59tCd80WZ2iz-c
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