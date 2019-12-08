import re

http_reg = re.compile("^https?://+")

## delete HTTP protocol
def deleteHttp(target):
    url = re.sub(http_reg, '', target)
    return url