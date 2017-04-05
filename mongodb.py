# mongodb
# coding=utf-8
from pymongo import MongoClient
from urllib.request import urlopen
import re


def scrapy(url):
    print('hello,db')
    res = urlopen(url)
    html = res.read()
    return html.decode('utf-8')


def prase(html):
    # 获取主页地址
    link = re.compile('<a.*href=\"(https://www.douban.com/people/.*/)\".*>')
    homepages = link.findall(html)
    for homepage in homepages:
        print(homepage)

res = scrapy('https://www.douban.com/explore/')
# print(res)
prase(res)

# m = re.search('(?<=abc)def', 'abcdef')

# print(m)

# webpage = urlopen('http://www.python.org')
# text = webpage.read()
# t = re.search(b'(?<=abc)def',text,re.IGNORECASE)
# print(t)