## daum tip & video의 경우 url redirect 로 target url을 찾을 수 있다.
## network log check를 통해 redirect 되는 url 찾는다.
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

