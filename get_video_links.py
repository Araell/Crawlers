# -*- coding: utf-8 -*-
# usage : python get_video_links.py BLOGNAME
import urllib2
import re
import sys
urlopen = urllib2.urlopen
blogname = sys.argv[1]
# a 以追加模式打开文件（即一打开文件，文件指针自动移到文件末尾），如果文件不存在则创建
# w+ 消除文件内容，然后以读写方式打开文件
video_links_file = open(blogname + '.txt', 'a')


def get_content_from_url(url):  # 从url中读取页面内容
    attempts = 0
    content = None
    while attempts < 10:
        print 'get_content_from_url -- cur attempts : ', attempts
        try:
            content = urlopen(url, data=None, timeout=10).read()
            break
        except Exception, e:
            attempts += 1
            print e
    return content


def extract_video_links(result):
    for item in result:
        print item
        video_page = get_content_from_url(item)
        if video_page is not None:
            video_link = re.findall(
                '(http[s]*://www.tumblr.com/video_file/[\S]+)[\"|\']', video_page, re.M | re.S)
            print video_link
            if len(video_link) > 0:
                video_links_file.write(video_link[0] + '\n')


base_url = 'http://' + blogname + '.tumblr.com/page/'
page = 1
while True:
    url = base_url + str(page)
    print(url)
    content = get_content_from_url(url)
    if content is not None:
        result = re.findall(
            '(http[s]*://www.tumblr.com/video/[\S]+)\'', content, re.M | re.S)
        if len(result) == 0:
            break
        else:
            page = page + 1
            extract_video_links(result)

video_links_file.close()
