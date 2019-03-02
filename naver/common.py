## common.py
import re

## delete HTTP protocol
regObj = re.compile('^https?://+')

def deleteHttp(target):
  url = re.sub(regObj, '', target)
  return url

