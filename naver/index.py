## index.py
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import naver_post
import naver
import naver_shop

## target type
# 블로그 = blog
# 카페 = cafe
# 지식in = kin
# 웹사이트 = webSite
# 뉴스 = news
# 동영상 = video
# 플레이스 = place
# 포스트 = post
# 쇼핑 = shop
##

## target sort_type
# rel.dsc = 관련도순
# createDate.dsc = 최신순
# rel = 네이버 쇼핑 랭킹순
# price_asc = 낮은 가격 순
# price_dsc = 높은 가격 순
# date = 등록일 순
# review = 리뷰 많은 순
##

## URI Type
# https://kin.naver.com/qna/detail.nhn?dirId=811&docId=315382080
##

## get db info
search_key = "kin"
db_url = "https://blog.naver.com/ideamode/221327332564"
sort_type = "review"
key = "쯔위"
keyword = "TWICE 트와이스 쯔위 굿즈- 15장 포토스탠드"

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
info = SearchInfo(db_url, key, search_key, sort_type, keyword)

## post rank
naver_data = None
rank = None

## post 일 경우 따로 실행해 준다.
if info.search == "post":
  naver_data = naver_post.NaverPost(info.key, info.url, info.sort)
elif info.search == "shop":
  naver_data = naver_shop.NaverShop(info.key, info.keyword, info.sort)
else:
  naver_data = naver.Naver(info.key, info.url, info.search)

rank = naver_data.rank()

if rank == -1:
  print("Error")
else:
  print(rank)
