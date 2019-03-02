## index.py
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import naver_post
import naver

## target type
# 블로그 = blog
# 카페 = cafe
# 지식in = kin
# 웹사이트 = webSite
# 뉴스 = news
# 동영상 = video
# 플레이스 = place
# 포스트 = post
##

## target sort_type
# rel.dsc = 관련도순
# createDate.dsc = 최신순
##

## get db info
search_key = "blog"
db_url = "https://blog.naver.com/digitaldiir/221469517946"
sort_type = "rel.dsc"
key = "쯔위"

class SearchInfo:

  def __init__(self, url, key, search, sort):
    ## target url
    self.url = url
    ## target key
    self.key = key
    ## target type
    self.search = search
    ## target sort type
    self.sort = sort

## db info
info = SearchInfo(db_url, key, search_key, sort_type)

## post rank
naver_data = None
rank = None

## post 일 경우 따로 실행해 준다.
if info.search == "post":
  naver_data = naver_post.NaverPost(info.key, info.url, info.sort)
else:
  naver_data = naver.Naver(info.key, info.url, info.search)

rank = naver_data.rank()

print(rank)
