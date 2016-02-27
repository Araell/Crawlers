# -*- coding: utf-8 -*-
import re
import os
import urllib
import urllib2
import sys
import cookielib
import threading
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')
request = urllib2.Request

# 创建MozillaCookieJar实例对象
cookie = cookielib.MozillaCookieJar()
# 从文件中读取cookie内容到变量
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
# 利用urllib2的build_opener方法创建一个opener
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))


def get_content_from_url(url):  # 从url中读取页面内容
    print('Get content from url : ' + url)
    req = request(url)
    count = 0
    content = ''
    while count < 5:
        try:
            content = opener.open(req, data=None, timeout=10).read()
            break
        except Exception, e:
            count += 1
            print e
    return content


def extract_m3u8_link(content):
    result = re.search('\"source\":\"(http:[^\"]+)\"', content, re.M | re.S)
    m3u8_url = result.group(1).replace('\\', '')
    return m3u8_url


def extract_ts_links(content):
    result = re.findall('http:[\S]+.ts', content, re.M | re.S)
    return result


def get_post_name(content):
    soup = BeautifulSoup(content, "lxml")
    post_name = soup.find('div', class_='title fl').h1.text
    return post_name.replace(' ', '_')


def download_ts_links(post_name, ts_links):
    print('Strat download : ' + post_name)
    for index in range(len(ts_links)):
        data = get_content_from_url(ts_links[index])
        try:
            ts_file = open(post_name + '_' + str(index) + '.ts', 'wb')
            ts_file.write(data)
            ts_file.close()
        except Exception, e:
            print(e)
    merge_ts_files(post_name, len(ts_links) - 1)


def merge_ts_files(post_name, num):
    # TODO: 文件名转义存在问题
    merged_file = post_name + ".ts"
    os.popen("touch " + merged_file)
    i = 0
    while i <= num:
        command = "cat " + post_name + '_' + \
            str(i) + ".ts " + ">> " + merged_file
        try:
            os.popen(command)
        except:  # 如果没有当前.ts, 打印出错误并跳过
            print "There is no " + str(i) + ".ts"
        i += 1

    rm_cmd = "rm -r " + post_name + '_*.ts'
    try:
        os.popen(rm_cmd)
    except:
        print "rm fail"


class downloadThread(threading.Thread):
    post_name = None
    ts_links = None

    def __init__(self, post_name, ts_links):
        threading.Thread.__init__(self)
        self.post_name = post_name
        self.ts_links = ts_links

    def run(self):
        download_ts_links(self.post_name, self.ts_links)


def extract_audio(url):
    content = get_content_from_url(url)
    post_name = get_post_name(content)
    m3u8_link = extract_m3u8_link(content)
    m3u8_content = get_content_from_url(m3u8_link)
    ts_links = extract_ts_links(m3u8_content)
    # download_ts_links(post_name, ts_links)
    thread = downloadThread(post_name, ts_links)
    thread.start()


if __name__ == '__main__':
    # with open('sounds.txt', 'r') as f:
    #     for line in f:
    #         extract_audio('http://www.app-echo.com' + line)
    extract_audio('http://www.app-echo.com/sound/911759')
