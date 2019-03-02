import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import types

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)

## delete HTTP protocol
regObj = re.compile('^https?://+')
vol_reg = re.compile('(?<=volumeNo=)\w+')
rank_reg = re.compile('(?<=searchRank=)\w+')


def deleteHttp(target):
  url = re.sub(regObj, '', target)
  return url

## naver 검색
key = '쯔위'

## list 정렬 방식
# rel.dsc = 관련도순
# createDate.dsc = 최신순
##
sort_type = "rel.dsc"

## search 할 url
db_url = "https://post.naver.com/viewer/postView.nhn?volumeNo=3388602&memberNo=11036773"
search_url = "https://post.naver.com/search/post.nhn?keyword={0}&sortType={1}".format(key, sort_type)

## post list 가져와서 link 랑 check
def check_post_rank(post_list):
  for idx, val in enumerate(post_list, 1):
    link = val.find('a', class_=a_link_class).get('href')
    target_vol = vol_reg.search(db_url).group()
    vol = vol_reg.search(link).group()
    rank = rank_reg.search(link).group()
    if vol == target_vol:
      return rank

## site 이동
driver.get(search_url)
time.sleep(1)

first_list_select = '#el_list_container'
list_select = 'ul.lst_feed > li.check_visible'
li_select = '.check_visible'
a_link_class = 'link_end'

## 첫 게시물 가져오기
first_list = driver.find_element_by_css_selector(first_list_select).get_attribute('innerHTML')
soup = BeautifulSoup(first_list, 'html.parser')
post_list = soup.select(list_select)

post_rank = check_post_rank(post_list)
find_element = True
num_of_page = 2

if post_rank:
  print(post_rank)
else:
  # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  while find_element:
    driver.find_element_by_css_selector(".btn_lst_more").click()
    time.sleep(0.5)
    num_of_page += 1
    ## 게시물 가져오기
    ul_list = driver.find_element_by_css_selector("#_list_container > .lst_feed:last-child").get_attribute("innerHTML")
    soup = BeautifulSoup(ul_list, "html.parser")
    post_list = soup.select(li_select)
    found_post = check_post_rank(post_list)
    if found_post:
      post_rank = found_post
      find_element = False
    elif num_of_page == 11:
      post_rank = False
      find_element = False

## 최종 rank 출력
print(post_rank)

time.sleep(10)