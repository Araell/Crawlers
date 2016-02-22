# -*- coding: utf-8 -*-
# usage : python tumbrl_image_crawler.py BLOGNAME
import re
import os.path
import threading
import time
import urllib2
import sys
urlopen = urllib2.urlopen
request = urllib2.Request
blogname = sys.argv[1]
baseurl = 'http://' + blogname + '.tumblr.com/page/'
imgdir = 'imgs/' + blogname + '/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}


def get_content_from_url(url):  # 从url中读取页面内容
    print('Get content from url : ' + url)
    req = request(url, headers=headers)
    count = 0
    content = ''
    while count < 5:
        try:
            content = urlopen(req, data=None, timeout=30).read()
            break
        except Exception, e:
            count += 1
            print e
    return content


def extract_img_urls(content):  # 从页面内容中抓出所有图片链接
    # filter avatar img
    imgs = re.findall(
        'img src=[\"|\'](http[s]?://[\d]+.media.tumblr.com/[^\"]+/[^\"]+)[\"|\']', content, re.M | re.S)
    imgs = set(imgs)
    # 抓取photoset页面的链接
    photoset_urls = re.findall(
        '(http[s]*://[\S]+.tumblr.com/post/[\d]+/photoset_iframe/[\S]+)[\"|\']', content, re.M | re.S)
    for photoset in photoset_urls:
        # 获取photoset页面，从页面中抓取图片链接
        photoset_content = get_content_from_url(photoset)
        photos = re.findall(
            'href=[\"|\'](http[s]?://[\d]+.media.tumblr.com/[^\"]+)[\"|\']', photoset_content, re.M | re.S)
        for photo in photos:
            imgs.add(photo)
    return imgs


# 停用
def down_img(img_url):  # 下载图片
    try:
        match_result = re.search('tumblr_.*\.(jpg|png|gif|tiff)', img_url)
        filename = match_result.group()
    except Exception, e:
        print e
        return

    if os.path.exists(imgdir + filename) and os.path.getsize(imgdir + filename) > 0:
        print filename + ' already exists!'
        return
    count = 0
    data = get_content_from_url(img_url)
    if data is '':
        print("Download fail : " + img_url)
        return
    else:
        print(filename)
        try:
            img = open(imgdir + filename, 'wb')
            img.write(data)
            img.close()
        except Exception, e:
            print(e)


# 停用
class downImgThread(threading.Thread):
    imgset = None

    def __init__(self, imgset):
        threading.Thread.__init__(self)
        self.imgset = imgset

    def run(self):
        for img_url in self.imgset:
            down_img(img_url)

img_links_file = open(blogname + '_img_links.txt', 'a')
cur_page = 1
if not os.path.exists(imgdir):
    os.makedirs(imgdir)

while True:
    content = get_content_from_url(baseurl + str(cur_page))
    imgset = extract_img_urls(content)
    if len(imgset) == 0:
        print '-----------end-----------'
        break
    else:
        print('Crawl image links of page ' + str(cur_page))
        # 停用下载
        # 使用chrome应用下载更快
        # downThread = downImgThread(imgset)
        # downThread.start()
        for img_url in imgset:
            img_links_file.write(img_url + '\n')
        cur_page += 1

img_links_file.close()
