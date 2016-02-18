# -*- coding: utf-8 -*-
# get_page_content
import urllib2
import re
import sys
urlopen = urllib2.urlopen
blogname = sys.argv[1]
video_links_file = open(blogname + '.txt', 'w+')


def get_content_from_url(url):  # 从url中读取页面内容
    attempts = 0
    content = ''
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
    result = re.findall(
        '(http[s]*://www.tumblr.com/video/[\S]+)\'', content, re.M | re.S)
    if len(result) == 0:
        break
    else:
        page = page + 1
        extract_video_links(result)

video_links_file.close()
