## index.py
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import daum

## target type
# 블로그 = blog
# 사이트 = site
# 동영상 = video (작업 전)
# 뉴스 = news
# 팁 = tip (작업 전)
##

## target sort_type
##

## URI Type
# youtube: https://youtu.be/qeedIyEjjmQ
# news: daum news url type (daum news 외 url(ex: 외부 사이트)의 경우 확인 불가)
##

## get db info
search_type = "tip"
db_url = "https://tip.daum.net/question/86428255"
sort_type = "null"
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
info = SearchInfo(db_url, key, search_type, sort_type, keyword)

## post rank
daum_data = None
rank = None

## post 일 경우 따로 실행해 준다.
daum_data = daum.Daum(info.key, info.url, info.search)

rank = daum_data.rank()

if rank == -1:
  print("Error")
else:
  print(rank)
