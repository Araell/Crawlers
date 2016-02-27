# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import json
import re

filename = 'cookie.txt'
# 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
loginUrl = "http://www.app-echo.com/index/login"
login_name = ''
login_pw = ''

res = opener.open(loginUrl)
content = res.read()
_csrf = re.search('name=\"_csrf\" value=\"([^\"]+)\"', content).group(1)

req = urllib2.Request(loginUrl, urllib.urlencode(
    {'_csrf': _csrf, 'login_form[name]': login_name, 'login_form[password]': login_pw}))
result = opener.open(req)
print(result.read())
cookie.save(ignore_discard=True, ignore_expires=True)


'''
channelUrl = 'http://www.app-echo.com/channel/52?page=2&per-page=14'
result = opener.open(channelUrl)
print(result.read())
'''

'''
opener.addheaders = [
    ('Accept', 'application/json, text/javascript, */*; q=0.01'),
    ('Accept-Encoding', 'gzip, deflate'),
    ('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2'),
    ('Connection', 'keep-alive'),
    ('Content-Length', '135'),
    ('X-Requested-With', 'XMLHttpRequest'),
    ('Referer', 'http://www.app-echo.com/index/login'),
    ('Host', 'www.app-echo.com'),
    ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
    ('Origin', 'http://www.app-echo.com'),
    ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'),
    ('Cookie', cookie)
]
'''
