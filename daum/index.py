## index.py
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import daum
import daum_place
import daum_shop

## target type
# 블로그 = blog
# 사이트 = site
# 동영상 = video (작업 전)
# 뉴스 = news
# 팁 = tip (작업 전)
# 카페 = cafe
# 장소 = place
# 쇼핑 = shop
##

## target sort_type
# cefe: acc = 정확도
# cefe: date = 최신
# shop: shophow = 쇼핑하우 랭킹순
# shop: price_asc = 낮은가격순(배송비 미포함)
# shop: price_asc_a = 낮은가격순(배송비 포함)
# shop: price_dsc = 높은가격순(배송비 미포함)
# shop: price_dsc_a = 높은가격순(배송비 포함)
# shop: review = 상품평순
# shop: date = 최신순
# shop: star = 만족도순
##

## URI Type
# youtube: https://youtu.be/qeedIyEjjmQ
# news: daum news url type (daum news 외 url(ex: 외부 사이트)의 경우 확인 불가)
##

## TODO Video Type일 경우, youtube는 link 가져와서 sort 가능, kakao TV의 경우 request URL과 response URL이 달라서 구분이 불가능함.
## TODO Tip Type일 경우 list에 있는 URL은 answer 기준 URL, question URL ID를 가져와야 함.

## get db info
search_type = "shop"
db_url = "https://place.map.kakao.com/1193848374"
sort_type = "shophow"
key = "쯔위"
keyword = "[코코블링] 아즈나브르 에어플레인 멀티 이어링 E1289 (포카리스웨트 CF 트와이스 쯔위 협찬 귀걸이)"

class SearchInfo:
  def __init__(self, url, key, search, sort, keyword):
    ## target url
    self.url = url
    ## target key
    self.key = key
    ## target type
    self.search = search
    ## target sort type
    self.sort = sort
    ## target key word
    self.keyword = keyword

## db info
info = SearchInfo(db_url, key, search_type, sort_type, keyword)

## post rank
daum_data = None
rank = None

## post 일 경우 따로 실행해 준다.
if info.search == "place":
  daum_data = daum_place.DaumPlace(info.key, info.url, info.sort)
elif info.search == "shop":
  daum_data = daum_shop.DaumShop(info.key, info.keyword, info.sort)
else:
  daum_data = daum.Daum(info.key, info.url, info.search, info.sort)

rank = daum_data.rank()

if rank == -1:
  print("Error")
else:
  print(rank)
