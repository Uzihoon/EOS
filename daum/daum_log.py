## daum tip & video의 경우 url redirect 로 target url을 찾을 수 있다.
## network log check를 통해 redirect 되는 url 찾는다.
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class DaumLog:

  def __init__(self, url):
    self.__url = url
    

  def get_target_url(self):
    caps = DesiredCapabilities.CHROME
    caps['loggingPrefs'] = {'performance': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=caps)

    driver.get(self.__url)

    for entry in driver.get_log('performance'):
      print(entry)
    
    driver.close()
    return self.__url
  
    