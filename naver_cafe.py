import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)


## naver 검색
key = '여자+치마+추천'

## search 할 url
target_url = "https://kongminji.tistory.com/263"
blog_url = "https://search.naver.com/search.naver?where=post&query=" + key

## blog 로 이동
driver.get(blog_url)
time.sleep(1)

current = driver.current_url

## blog 탐색
for x in range(0, 10):
  print(x)
  pages = (x * 10 * 1) + 1
  current_page = '&start=' + repr(pages)
  driver.get(current + current_page)
  ## blog 글 가져오기
  html = driver.find_element_by_css_selector('#elThumbnailResultArea').get_attribute('innerHTML')
  ## HTML Parsing
  soup = BeautifulSoup(html, 'html.parser')
  li_list = soup.select('li.sh_blog_top')

  

  for idx, val in enumerate(li_list, 1):
    link = val.find('a', class_='sh_blog_title').get('href')
    ## blog url type check reg
    target_reg = re.compile('blog.naver.com')
    reg_url = target_reg.search(link)
    check_url = str()

    if reg_url is not None:
      log_reg = re.compile('(?<=logNo=)\w+')
      log_no = log_reg.search(link).group()
      basic_reg = re.compile('^[^?]+')
      basic_url = basic_reg.search(link).group()
      check_url = basic_url + '/' + log_no
    else:
      check_url = link

    if check_url == target_url:
      print("Find Target!!")
      print(x * 10 + idx)
  time.sleep(2)
      


time.sleep(10)