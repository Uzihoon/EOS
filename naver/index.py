## index.py
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import naver_post
import naver

## db로부터 받아오는 data
key = '강남'

## search_key
# 블로그 = blog
# 카페 = cafe
# 지식in = kin
# 웹사이트 = webSite
# 뉴스 = news
# 동영상 = video
# 플레이스 = place
# 포스트 = post
##
search_key = "place"

## search url
db_url = "https://store.naver.com/restaurants/detail?id=12783829"

## chrome driver
driver = webdriver.Chrome("./chromedriver")
driver.implicitly_wait(3)

## post rank
post_rank = None

## post 일 경우 따로 실행해 준다.
if search_key == "post":
