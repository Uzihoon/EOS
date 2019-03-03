import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup

class NaverShop:

  def __init__(self, key, keyword, sort_type):
    self.__key = key
    self.__keyword = keyword
    self.__sort_type = sort_type
    self.__driver_url = "https://search.shopping.naver.com/search/all.nhn?query={0}&sort={1}".format(self.__key, self.__sort_type)

    ## element css selector
    self.__container_selector = ".goods_list"
    self.__list_selector = "li[data-tr='slsl']"
    self.__a_link_class = "tit"

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

  def find_target_post(self):
    
    rank = None
    current = self.driver.current_url
    start_str = "pagingIndex"
    isBreak = False
    for x in range(0, 3):
      current_page = "{0}&{1}={2}".format(current, start_str, repr(x + 1))
      self.driver.get(current_page)
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