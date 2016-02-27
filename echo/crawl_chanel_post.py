# -*- coding: utf-8 -*-
import re
import os
import urllib
import urllib2
import sys
import cookielib
from bs4 import BeautifulSoup
from echo_crawler import get_content_from_url, opener

reload(sys)
sys.setdefaultencoding('utf8')

channel_url_prefix = 'http://www.app-echo.com/channel/52?page='
channel_url_postfix = '&per-page=14'
sound_links_file = 'sound_links_file.txt'

with open(sound_links_file, 'a') as f:
    for page in range(1, 36):
        channel_url = channel_url_prefix + str(page) + channel_url_postfix
        content = get_content_from_url(channel_url)
        soup = BeautifulSoup(content, 'lxml')
        f.write('---------- page : ' + str(page) + '----------')
        for link in soup.find_all('a'):
            if link.get('href') and re.match('/sound/[\d]+', link.get('href')) and len(link.text) > 1:
                print(link.text)
                print(link.get('href'))
                f.write(link.text + '\n')
                f.write(link.get('href') + '\n')
