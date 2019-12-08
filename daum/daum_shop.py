import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup

class DaumShop:

  def __init__(self, key, keyword, sort_type):
    self.__key = key
    self.__keyword = keyword
    self.__sort_type = self.sort_type(sort_type)
    self.__driver_url = "http://shopping.daum.net/search/{0}/sort_type:{1}&view_type:list&image_filter_cnt:200".format(self.__key, self.__sort_type)

    ## element css selector
    self.__container_selector = ".list_prod_type1 "
    self.__list_selector = "li.wrap_prod"
    self.__a_link_class = "link_g"

    ## rank
    self.__post_rank = None

    ## chrome driver
    self.driver = webdriver.Chrome("./chromedriver")
    self.driver.implicitly_wait(1)

  
  ## get post rank
  def rank(self):
    ##chrome start
    self.driver.get(self.__driver_url)
    time.sleep(1)
    self.__post_rank = self.find_target_post()
    return self.__post_rank
  
  ## sort type select
  def sort_type(self, sort):
    return {
      "shophow": "1",
      "price_asc": "3",
      "price_asc_a": "3a",
      "price_dsc": "4",
      "price_dsc_a": "4a",
      "review": "6",
      "date": "5",
      "star": "9",
    }.get(sort, "1")

  def find_target_post(self):
    
    rank = None
    current = self.driver.current_url
    start_str = "page"
    isBreak = False
    for x in range(0, 3):
      current_page = "{0}&{1}:{2}".format(current, start_str, repr(x + 1))
      self.driver.get(current_page)
      time.sleep(1)
      find_list = self.driver.find_element_by_css_selector(self.__container_selector).get_attribute("innerHTML")
      soup = BeautifulSoup(find_list, "html.parser")
      post_list = soup.select(self.__list_selector)
      for idx, val in enumerate(post_list, 1):
        a_link_text = val.find('a', class_=self.__a_link_class).getText()
        title = a_link_text.strip()
        if title == self.__keyword:
          isBreak = True
          rank = (x * 40 + idx)
          break
      if isBreak:
        return rank