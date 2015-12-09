# -*- coding: utf-8 -*-

import re
import os.path
import threading
import time
import urllib2

urlopen = urllib2.urlopen
request = urllib2.Request
baseurl = "http://lizclimo.tumblr.com/page/"
imgdir = 'imgs/lizclimo/'


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


def extract_img_urls(content):  # 从页面内容中抓出所有图片链接
    imgs = re.findall('img src=\"(http[^\"]+)\"', content, re.M | re.S)
    imgs = set(imgs)
    if len(imgs) <= 0:
        return 1
    for img in imgs:
        down_img(img)
        return -1


def get_binary_from_req(req):  # 从请求中获取binary数据
    attempts = 0
    binary = ''
    while attempts < 10:
        print 'get_binary_from_req -- cur attempts : ', attempts
        try:
            binary = urlopen(req, data=None, timeout=5).read()
            break
        except Exception, e:
            attempts += 1
            print e
            raise
    return binary


def down_img(img_url):  # 下载图片
    try:
        filename = re.search('tumblr_.*\.(jpg|png|gif|tiff)', img_url).group()
    except Exception, e:
        print e
        return

    if os.path.exists(imgdir + filename) and os.path.getsize(imgdir + filename) > 0:
        print filename + ' already exists!'
        return
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}
    req = request(img_url, headers=headers)

    try:
        data = get_binary_from_req(req)
        print 'saving img :', filename
        img = open(imgdir + filename, 'wb')
        if data is '':
            return
        else:
            img.write(data)
            img.close()
    except Exception, e:
        print(e)


def main():
    cur_page = 27

    while True:
        print 'crawl page', cur_page
        content = get_content_from_url(baseurl + str(cur_page))
        print 'page ' + str(cur_page) + ' complete'
        is_end = extract_img_urls(content)
        if is_end == 1:
            print '-----------end-----------'
            break
        else:
            cur_page = cur_page + 1

main()
