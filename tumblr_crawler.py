# -*- coding: utf-8 -*-

import re
import os.path
import threading
import time
import urllib2

urlopen = urllib2.urlopen
request = urllib2.Request
baseurl = "http://girlimg-legs.tumblr.com/page/"
imgdir = 'imgs/girlimg-legs/'

# http_proxy = "http://localhost:8123"
# http_proxys = {'http': http_proxy}


# def install_proxy():
#     if use_proxy == False:
#         return
#     proxy_support = urllib.request.ProxyHandler({"http": http_proxy})
#     opener = urllib.request.build_opener(proxy_support)
#     urllib.request.install_opener(opener)
#     return


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
    return imgs


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
        match_result = re.search('tumblr_.*\.(jpg|png|gif|tiff)', img_url)
        if match_result == None:
            # filter avatar img
            return
        filename = match_result.group()
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


class downImgThread(threading.Thread):
    imgset = None

    def __init__(self, imgset):
        threading.Thread.__init__(self)
        self.imgset = imgset

    def run(self):
        for img_url in self.imgset:
            down_img(img_url)


def main():
    cur_page = 1
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)

    while True:
        print '==crawl page', cur_page
        content = get_content_from_url(baseurl + str(cur_page))
        imgset = extract_img_urls(content)
        if len(imgset) == 0:
            print '-----------end-----------'
            break
        else:
            print '==open thread for download page ', cur_page
            downThread = downImgThread(imgset)
            downThread.start()
            cur_page = cur_page + 1

main()
# video file
# https://www.tumblr.com/video_file/134865539253/tumblr_nz3r6v6faJ1usvyma
# https://vt.tumblr.com/tumblr_nz3r6v6faJ1usvyma.mp4#_=_
