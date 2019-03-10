import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import common

## naver_post search def
class DaumPlace:

  def __init__(self, key, url, sort_type):
    self.__key = key
    self.__sort_type = sort_type
    self.__url = common.deleteHttp(url)
    self.__driver_url = "https://map.kakao.com/?from=total&q={0}&tab=place&nil_suggest=btn".format(self.__key)

    ## element css selector
    self.__list_container = ".placelist"
    self.__li_select = ".PlaceItem"
    self.__a_link_class = "moreview"

    ## rank
    self.__post_rank = None

    ## chrome driver
    self.driver = webdriver.Chrome("./chromedriver")
    self.driver.implicitly_wait(1)

    self.num_of_page = 2

  ## get post rank
  def rank(self):
    ## chrome driver
    self.driver.get(self.__driver_url)
    time.sleep(1)
    self.__post_rank = self.find_target_post()
    return self.__post_rank

  def check_post_rank(self, li_list):
    post_rank = False
    for idx, val in enumerate(li_list, 1):
      link = val.find('a', class_=self.__a_link_class).get("href")
      check_url = common.deleteHttp(link)
      if check_url == self.__url:
        post_rank = idx
        break

    return post_rank
    
  def get_li_list(self):
    html = self.driver.find_element_by_css_selector(self.__list_container).get_attribute("innerHTML")
    soup = BeautifulSoup(html, "html.parser")
    li_list = soup.select(self.__li_select)
    return li_list

  ## find target
  def find_target_post(self):
    li_list = self.get_li_list()
    post_rank = self.check_post_rank(li_list)

    if post_rank is False:
      for x in range(0, 6):
        btn_id_select = "info.search.page.no1"
        if x > 3:
          if x == 4:
            next_element = self.driver.find_element_by_id("info.search.page.next")
            self.driver.execute_script("arguments[0].click();", next_element)
            time.sleep(0.5)
          btn_id_select = "info.search.page.no{0}".format(x - 3)
        else:
          btn_id_select = "info.search.page.no{0}".format(x + 2)
          
        element = self.driver.find_element_by_id(btn_id_select)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(0.5)

        li_list = self.get_li_list()
        idx = self.check_post_rank(li_list)

        if idx:
          post_rank = 18 + (15 * x) + idx
          break

    return post_rank
