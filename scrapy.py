# mongodb
# coding=utf-8
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import urllib.request


def scrapy(url):
    headers = {
        'Host': 'www.douban.com',
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Accept-Language': "zh-CN,zh;q=0.8",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36",
        'Connection': "keep-alive",
    }
    req = urllib.request.Request(url,headers=headers)
    res = urllib.request.urlopen(req)
    html = res.read()
    return html.decode('utf-8')


def prase(html):
    # 获取主页地址
    link = re.compile('<a.*href=\"(https://www.douban.com/people/.*/)\".*>')
    homepages = link.findall(html)
    for homepage in homepages:
        print('解析：' + homepage)
        home_data = scrapy(homepage)
        soup = BeautifulSoup(home_data, 'lxml')  # 获取soup对象
        print(soup.select_one('title'))
        #praseHomePage(homepage)
        break


def praseWithSoup(html):
    soup = BeautifulSoup(html, 'lxml')
    print(soup.title.string)

def praseHomePage(homepage):
    douban_user = {}
    douban_user['homepage'] = homepage
    print(homepage)
    home_data = scrapy(homepage)
    soup = BeautifulSoup(home_data, 'lxml')  # 获取soup对象
    print(soup.select_one('title'))
    print(soup.select_one('div.info'))
    return

    nick_tag = soup.select('div.info h1')
    nick = str(nick_tag[0].contents[0]).strip()  # 获取昵称
    douban_user['nick'] = nick

    user_info_tag = soup.select_one('div.user-info')
    # print(user_info_tag.contents)
    location = str(user_info_tag.contents[1].string).strip()  # 获取位置
    douban_user['location'] = location

    user_info_pl_tag = soup.select_one('div.user-info .pl')

    userid = str(user_info_pl_tag.contents[0].string).strip()  # 账号id
    douban_user['userid'] = userid

    join_date_str = str(user_info_pl_tag.contents[2].string).strip()
    date_re = re.match('(.*)加入', join_date_str)
    join_date = date_re.groups()[0]  # 加入日期
    douban_user['join_date'] = join_date

    avatar_tag = soup.select_one('.userface')
    avatar = avatar_tag['src']  # 头像地址
    douban_user['avatar'] = avatar

    following_tag = soup.select_one('#friend h2 a')
    following_str = str(following_tag.string).strip()
    following_re = re.search('成员(.*)', following_str)
    following = following_re.groups()[0]  # 关注的人数
    douban_user['following'] = following

    follower_tag = soup.select_one('.rev-link a')
    follower_link = str(follower_tag['href'])  # 关注人页面
    douban_user['follower_link'] = follower_link

    follower_str = str(follower_tag.string).strip()
    follower_re = re.search('被(.*)人', follower_str)
    follower = follower_re.groups()[0]  # 被关注人数
    douban_user['follower'] = follower

    movies_tag = soup.select('#movie span.pl a')
    want_movie_str = str(movies_tag[1].string).strip()  # 想看电影
    want_movie_re = re.search('([0-9]+)部', want_movie_str)
    want_movie = want_movie_re.groups()[0]
    douban_user['want_movie'] = want_movie

    saw_movie_str = str(movies_tag[2].string).strip()  # 想看电影
    saw_movie_re = re.search('([0-9]+)部', saw_movie_str)
    saw_movie = saw_movie_re.groups()[0]
    douban_user['saw_movie'] = saw_movie
    print(douban_user)

# res = scrapy('https://www.douban.com/explore/')
# print(res)
# prase(res)
# prase(res)

res = scrapy('https://www.douban.com/people/155709891/')
print(res)
# praseHomePage(res)