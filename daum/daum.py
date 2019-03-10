import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import common
import urllib.request

class Daum:

  def __init__(self, key, url, search, sort):
    ## regexp
    self.__blog_target_reg = re.compile('blog.naver.com')
    self.__basic_reg = re.compile('^[^?]+')
    self.__log_reg = re.compile('(?<=logNo=)\w+')
    self.__blog_id_reg = re.compile('(?<=blogId=)\w+')
    self.__news_id_reg = re.compile("\d+")

    self.__key = key
    self.__search_type = search
    self.__where = self.search_type(self.__search_type)
    self.__url = self.format_id_url(url) if (self.__search_type == "news" or self.__search_type == "tip") else common.deleteHttp(url)
    self.__sort_type = sort

    self.__default_url = "https://search.daum.net/search?q={0}&w={1}".format(self.__key, self.__where)
    self.__cafe_url = "http://top.cafe.daum.net/_c21_/search?search_opt=board&q={0}&sort_type={1}".format(self.__key, self.__sort_type)
    self.__driver_url = self.__cafe_url if self.__search_type == "cafe" else self.__default_url

    ## chrome driver
    self.driver = webdriver.Chrome("./chromedriver")
    self.driver.implicitly_wait(1)

    self.__post_rank = None

  ## type에 따른 search key 정해주기
  def search_type(self, search_type):
    return {
      "blog": "blog",
      "site": "site",
      "video": "vclip",
      "news": "news",
      "tip": "knowledge",
      "cafe": "cafe"
    }.get(search_type, 'post')

  ## make start str
  def make_start_str(self, key):
      return {
          "news": "&p=",
          "cafe": "&p="
      }.get(key, '&page=')

  ## get post rank
  def rank(self):
    ## chrome driver
    self.driver.get(self.__driver_url)
    time.sleep(1)
    self.__post_rank = self.find_target_post()
    return self.__post_rank

  ## make a link class
  def make_a_link_class(self, key):
      return {
          "news": "f_nb",
          "tip": "f_link_b",
          "cafe": "link_url"
      }.get(key, 'f_url')

   ## make ul select
  def make_ul_select(self, key):
      return {
          "blog": ".list_info",
          "video": "#vclipList",
          "news": "#clusterResultUL",
          "tip": "#knowResultUL",
          "cafe": ".list_scafe"
      }.get(key, '.list_info')

  ## make list container
  def make_list_container(self, key):
      return {
          "blog": ".coll_cont",
          "news": ".coll_cont",
          "tip": "#knowResultWrapper",
          "cafe": '.scafe_fulltxt'
      }.get(key, '.mg_cont')
  
  ## make li select
  def make_li_select(self, key):
      return {
          'blog': 'li',
      }.get(key, "li")
  
  ## blog url format
  def format_blog_url(self, url):
    check_url = common.deleteHttp(url)
    reg_url = self.__blog_target_reg.search(check_url)
    if reg_url is not None:
      log_no = self.__log_reg.search(check_url).group()
      blog_id = self.__blog_id_reg.search(check_url).group()
      check_url = "{0}/{1}/{2}".format(reg_url.group(), blog_id, log_no)
    return check_url

  ## news url format
  def format_id_url(self, url):
    check_url = self.__news_id_reg.search(common.deleteHttp(url)).group()
    return check_url

  ## cafe url format
  def format_cafe_url(self, url):
    check_url = self.__basic_reg.search(common.deleteHttp(url)).group()
    return check_url

  def find_target_post(self):
    post_rank = None
    ## url
    current = self.driver.current_url
    ## page parameter url
    start_str = self.make_start_str(self.__search_type)
    ## element selector
    a_link_class = self.make_a_link_class(self.__search_type)
    list_container = self.make_list_container(self.__search_type)
    list_item = "{0} > {1}".format(self.make_ul_select(self.__search_type), self.make_li_select(self.__search_type))

    ## naver 탐색
    for x in range(0, 10):

      pages = x + 1
      current_page = start_str + repr(pages)
      self.driver.get(current + current_page)

      ## naver list container element 가져오기
      html = self.driver.find_element_by_css_selector(list_container).get_attribute('innerHTML')

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
          if self.__search_type == 'blog':
            check_url = self.format_blog_url(link)
          elif self.__search_type == "news" or self.__search_type == "tip":
            check_url = self.format_id_url(link)
          elif self.__search_type == "cafe":
            check_url = self.format_cafe_url(link)
          else:
            check_url = common.deleteHttp(link)
          if check_url == self.__url:
            isBreak = True
            post_rank = (x * 10 + idx)
            break
        else:
          pass
      if isBreak:
        return post_rank
