import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)

## delete HTTP protocol
regObj = re.compile('^https?://+')
blog_target_reg = re.compile('blog.naver.com')
place_target_reg = re.compile('store.naver.com/restaurants/detail')
log_reg = re.compile('(?<=logNo=)\w+')
basic_reg = re.compile('^[^?]+')
dir_reg = re.compile('(?<=dirId=)\w+')
doc_reg = re.compile('(?<=docId=)\w+')
id_reg = re.compile('(?<=id=)\w+')

def deleteHttp(target):
  url = re.sub(regObj, '', target)
  return url

## type에 따른 search key 정해주기
def search_type(x):
    return {
        'cafe': 'article',
        'blog': 'post',
        'kin': 'kin',
        'webSite': 'webkr',
        'news': 'news',
        'video': 'video'
    }.get(x, 'post')

## 지식in url format
def format_kin_url(url):
  check_url = deleteHttp(url)
  reg_url = basic_reg.search(check_url).group()
  if reg_url is not None:
    dirId = dir_reg.search(check_url).group()
    docId = doc_reg.search(check_url).group()
    check_url = reg_url + '?' + 'dirId=' + dirId + '&docId=' + docId
  return check_url

## place url format
def format_place_url(url):
  check_url = deleteHttp(url)
  basic_url = basic_reg.search(check_url).group()
  url_id = id_reg.search(check_url).group()
  check_url = basic_url + '?id=' + url_id
  return check_url

## blog url format
def format_blog_url(url):
  check_url = deleteHttp(url)
  reg_url = blog_target_reg.search(check_url)
  if reg_url is not None:
    log_no = log_reg.search(check_url).group()
    basic_url = basic_reg.search(check_url).group()
    check_url = basic_url + '/' + log_no
  return check_url

## make start str
def make_start_str(key):
    return {
        'kin': '&kin_start=',
        "place": "&page="
    }.get(key, '&start=')
  
## make li select
def make_li_select(key):
    return {
        'webSite': 'li.sh_web_top',
        'kin': 'li',
        'news': 'li',
        'video': 'li.video_item',
        "place": "li.list_item"
    }.get(key, 'li.sh_{0}_top'.format(key))

## make a link class
def make_a_link_class(key):
    return {
        'webSite': 'title_link',
        'kin': '',
        'news': '_sp_each_title',
        'video': 'title',
        "place": "name"
    }.get(key, 'sh_{0}_title'.format(search_key))

## make ul select
def make_ul_select(key):
    return {
        'news': '.type01',
        'video': '.video_lst_vertical._video_lst',
        "place": ".list_place_col1"
    }.get(key, '#elThumbnailResultArea')

## make list container
def make_list_container(key):
    return {
        'blog': '.blog.section._blogBase._prs_blg',
        'cafe': '.cafe_article.section._cafeBase',
        'kin': '.kinn.section._kinBase',
        'webSite': '.sp_website.section',
        'news': '.news.mynews.section._prs_nws',
        'video': '.sp_video.section._au_main_video',
        "place": ".list_wrapper_inner"
    }.get(key, '.section')


## naver 검색
key = '강남'

## search_key
# 블로그 = blog
# 카페 = cafe
# 지식in = kin
# 웹사이트 = webSite
# 뉴스 = news
# 동영상 = video
# 플레이스 = place
##
search_key = 'place'

param = search_type(search_key)

## search 할 url
db_url = "https://store.naver.com/restaurants/detail?id=12783829"
target_url = format_kin_url(db_url) if search_key == 'kin' else deleteHttp(db_url)
default_url = "https://search.naver.com/search.naver?where={0}&query={1}".format(param, key)
place_url = "https://store.naver.com/restaurants/list?query={0}".format(key)
search_url = place_url if search_key == "place" else default_url

## site 이동
driver.get(search_url)
time.sleep(1)

current = driver.current_url
start_str = make_start_str(search_key)
a_link_class = make_a_link_class(search_key)
list_container = make_list_container(search_key)
list_item = "{0} > {1}".format(make_ul_select(search_key), make_li_select(search_key))

## naver 탐색
for x in range(0, 10):
  pages = (x + 1) if search_key == 'place' else (x * 10) + 1
  current_page = start_str + repr(pages)
  driver.get(current + current_page)
  ## naver list container element 가져오기
  html = driver.find_element_by_css_selector(list_container).get_attribute('innerHTML')
  #html = driver.find_element_by_css_selector(ul_select).get_attribute('innerHTML')
  ## HTML Parsing
  soup = BeautifulSoup(html, 'html.parser')
  li_list = soup.select(list_item)
  isBreak = False
  for idx, val in enumerate(li_list, 1):
    a_tag = val.find('a', class_= a_link_class)
    link = str()
    if a_tag is not None:
      link = a_tag.get('href')
    check_url = str()
    if search_key == 'blog':
      check_url = format_blog_url(link)
    elif search_key == 'kin':
      check_url = format_kin_url(link)
    elif search_key == 'place':
      check_url = format_place_url(link)
    else:
      check_url = deleteHttp(link)
    
    if check_url == target_url:
      print("Find Target!!")
      print(x * 10 + idx)
      isBreak = True
      break
  if isBreak:
    break



time.sleep(10)