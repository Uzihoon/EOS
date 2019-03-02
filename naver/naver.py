import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup

class Naver:

  def __init__(self, key, url, search):
    ## regexp
    self.__http_reg = re.compile("^https?://+")
    self.__blog_target_reg = re.compile('blog.naver.com')
    self.__palce_target_reg = re.compile('store.naver.com/restaurants/detail')
    self.__log_reg = re.compile('(?<=logNo=)\w+')
    self.__basic_reg = re.compile('^[^?]+')
    self.__dir_reg = re.compile('(?<=dirId=)\w+')
    self.__doc_reg = re.compile('(?<=docId=)\w+')
    self.__id_reg = re.compile("(?<=id=)\w+")
    
    self.__key = key
    self.__search_key = search
    self.__where = self.search_type(self.__search_key)
    self.__url = self.format_kin_url(url) if self.__search_key == "kin" else self.deleteHttp(url)

    ## naver place 외 default url 적용
    self.__default_url = "https://search.naver.com/search.naver?where={0}&query={1}".format(self.__where, self.__key)
    self.__place_url = "https://store.naver.com/restaurants/list?query={0}".format(self.__key)
    self.__driver_url = self.__place_url if self.__search_key == "place" else self.__default_url

    ## chrome driver
    self.driver = webdriver.Chrome("./chromedriver")
    self.driver.implicitly_wait(1)

    self.__post_rank = None

  ## type에 따른 search key 정해주기
  def search_type(self, search_type):
    return {
      'cafe': 'article',
      'blog': 'post',
      'kin': 'kin',
      'webSite': 'webkr',
      'news': 'news',
      'video': 'video'
    }.get(search_type, 'post')

  ## delete HTTP protocol
  def deleteHttp(self, target):
    url = re.sub(self.__http_reg, '', target)
    return url

  ## 지식in url format
  def format_kin_url(self, url):
    check_url = self.deleteHttp(url)
    reg_url = self.__basic_reg.search(check_url).group()
    if reg_url is not None:
      dirId = self.__dir_reg.search(check_url).group()
      docId = self.__doc_reg.search(check_url).group()
      check_url = "{0}?dirId={1}&docId={2}".format(reg_url, dirId, docId)
    return check_url

  ## place url format
  def format_place_url(self, url):
    check_url = self.deleteHttp(url)
    basic_url = self.__basic_reg.search(check_url).group()
    url_id = self.__id_reg.search(check_url).group()
    check_url = "{0}?id={1}".format(basic_url, url_id)
    return check_url

  ## blog url format
  def format_blog_url(self, url):
    check_url = self.deleteHttp(url)
    reg_url = self.__blog_target_reg.search(check_url)
    if reg_url is not None:
      log_no = self.__log_reg.search(check_url).group()
      basic_url = self.__basic_reg.search(check_url).group()
      check_url = "{0}/{1}".format(basic_url, log_no)
    return check_url

  ## make start str
  def make_start_str(self, key):
      return {
          'kin': '&kin_start=',
          "place": "&page="
      }.get(key, '&start=')

  ## make li select
  def make_li_select(self, key):
      return {
          'webSite': 'li.sh_web_top',
          'kin': 'li',
          'news': 'li',
          'video': 'li.video_item',
          "place": "li.list_item"
      }.get(key, 'li.sh_{0}_top'.format(key))

  ## make a link class
  def make_a_link_class(self, key):
      return {
          'webSite': 'title_link',
          'kin': '',
          'news': '_sp_each_title',
          'video': 'title',
          "place": "name"
      }.get(key, 'sh_{0}_title'.format(self.__search_key))
  
  ## make ul select
  def make_ul_select(self, key):
      return {
          'news': '.type01',
          'video': '.video_lst_vertical._video_lst',
          "place": ".list_place_col1"
      }.get(key, '#elThumbnailResultArea')

  ## make list container
  def make_list_container(self, key):
      return {
          'blog': '.blog.section._blogBase._prs_blg',
          'cafe': '.cafe_article.section._cafeBase',
          'kin': '.kinn.section._kinBase',
          'webSite': '.sp_website.section',
          'news': '.news.mynews.section._prs_nws',
          'video': '.sp_video.section._au_main_video',
          "place": ".list_wrapper_inner"
      }.get(key, '.section')

  ## get post rank
  def rank(self):
    ## chrome driver
    self.driver.get(self.__driver_url)
    time.sleep(1)
    self.__post_rank = self.find_target_post()
    return self.__post_rank

  def find_target_post(self):
    post_rank = None
    ## url
    current = self.driver.current_url
    ## page parameter url
    start_str = self.make_start_str(self.__search_key)
    ## element selector
    a_link_class = self.make_a_link_class(self.__search_key)
    list_container = self.make_list_container(self.__search_key)
    list_item = "{0} > {1}".format(self.make_ul_select(self.__search_key), self.make_li_select(self.__search_key))

    ## naver 탐색
    for x in range(0, 10):

      pages = (x + 1) if self.__search_key == 'place' else (x * 10) + 1
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
        if self.__search_key == 'blog':
          check_url = self.format_blog_url(link)
        elif self.__search_key == 'kin':
          check_url = self.format_kin_url(link)
        elif self.__search_key == 'place':
          check_url = self.format_place_url(link)
        else:
          check_url = self.deleteHttp(link)
        
        if check_url == self.__url:
          isBreak = True
          post_rank = (x * 10 + idx)
          break
      if isBreak:
        return post_rank
