import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup

## naver_post search def
class NaverPost:

  def __init__(self, key, url, sort_type):
    self.__key = key
    self.__sort_type = sort_type
    self.__url = url
    self.__driver_url = "https://post.naver.com/search/post.nhn?keyword={0}&sortType={1}".format(self.__key, self.__sort_type)

    ## regex
    self.__vol_reg = re.compile('(?<=volumeNo=)\w+')
    self.__rank_reg = re.compile('(?<=searchRank=)\w+')

    ## element css selector
    self.__first_list_select = "#el_list_container"
    self.__list_select = "ul.lst_feed > li.check_visible"
    self.__li_select = ".check_visible"
    self.__a_link_class = "link_end"

    ## rank
    self.__post_rank = None

    ## chrome driver
    self.driver = webdriver.Chrome("./chromedriver")
    self.driver.implicitly_wait(1)

    self.num_of_page = 2

  ## post list 가져와서 link check
  def check_post_rank(self, post_list):
    for idx, val in enumerate(post_list, 1):
      link = val.find('a', class_=self.__a_link_class).get('href')
      target_vol = self.__vol_reg.search(self.__url).group()
      vol = self.__vol_reg.search(link).group()
      rank = self.__rank_reg.search(link).group()
      if vol == target_vol:
        return rank

  ## get post rank
  def rank(self):
    ## chrome driver
    self.driver.get(self.__driver_url)
    time.sleep(1)
    self.__post_rank = self.find_target_post()
    return self.__post_rank


  ## find target
  def find_target_post(self):
    first_list = self.driver.find_element_by_css_selector(self.__first_list_select).get_attribute('innerHTML')
    soup = BeautifulSoup(first_list, 'html.parser')
    post_list = soup.select(self.__list_select)

    post_rank = self.check_post_rank(post_list)

    ## return rank. if couldn't find, return False
    if post_rank:
      return post_rank
    else:
      # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      while True:
        ## click more btn
        self.driver.find_element_by_css_selector(".btn_lst_more").click()
        time.sleep(0.5)
        self.num_of_page += 1
        ## 게시물 가져오기
        ul_list = self.driver.find_element_by_css_selector("#_list_container > .lst_feed:last-child").get_attribute("innerHTML")
        soup = BeautifulSoup(ul_list, "html.parser")
        post_list = soup.select(self.__li_select)
        post_rank = self.check_post_rank(post_list)
        if post_rank:
          return post_rank
        elif self.num_of_page == 11:
          return False
