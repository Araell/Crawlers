# -*- coding: utf-8 -*-
# usage : python get_video_links.py BLOGNAME
import urllib2
import re
import sys
urlopen = urllib2.urlopen
request = urllib2.Request
blogname = sys.argv[1]
# a 以追加模式打开文件（即一打开文件，文件指针自动移到文件末尾），如果文件不存在则创建
# w+ 消除文件内容，然后以读写方式打开文件
video_links_file = open(blogname + '_video_links.txt', 'a')
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}


def get_content_from_url(url):  # 从url中读取页面内容
    print('reading page : ' + url)
    req = request(url, headers=headers)
    attempts = 0
    content = ''
    while attempts < 10:
        print('Attempt counts : ' + str(attempts))
        try:
            content = urlopen(req, data=None, timeout=30).read()
            break
        except Exception, e:
            attempts += 1
            print e
    return content


def extract_video_links(result):
    for item in result:
        video_page = get_content_from_url(item)
        video_link = re.findall(
            '(http[s]*://www.tumblr.com/video_file/[\S]+)[\"|\']', video_page, re.M | re.S)
        if len(video_link) > 0:
            video_links_file.write(video_link[0] + '\n')


base_url = 'http://' + blogname + '.tumblr.com/page/'
page = 1
while True:
    url = base_url + str(page)
    print(url)
    content = get_content_from_url(url)
    result = re.findall(
        '(http[s]*://www.tumblr.com/video/[\S]+)\'', content, re.M | re.S)
    if len(result) == 0:
        break
    else:
        page = page + 1
        extract_video_links(result)

video_links_file.close()
