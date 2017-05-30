from pymongo import MongoClient
from bs4 import BeautifulSoup
import urllib.request
import requests
from PIL import Image
from fake_useragent import  UserAgent
import sys
import re
import random
import time


start_page = 'https://www.douban.com/people/fengs/'

#登录
s = requests.session()

proxies = {
  "http": "http://1.27.202.173",
  "https": "http://1.27.202.173",
}

login_url = 'https://www.douban.com/accounts/login'
# username = input('请输入手机号或者邮箱:')
# passwd = input('请输入密码:')
username = '18316629973'
passwd = 'cwp348462402'
data = {
    'redir': start_page,
    'form_email': username,
    'form_password': passwd,
    'login': '登录'
}
ua = UserAgent()
headers = {
    # 'User-Agent': ua.random
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
# r = requests.post(login_url, data=data, verify=False, headers=headers)

r = s.post(login_url,data=data,verify=True,headers=headers,proxies=proxies)

#获取图片验证码
soup = BeautifulSoup(r.text,'lxml')
captcha = soup.find('img',id='captcha_image')
if captcha != None:
    captchaAddr = soup.find('img',id='captcha_image')['src']
    captchaId = soup.select_one('input[name="captcha-id"]')['value']
    #显示图片
    urllib.request.urlretrieve(captchaAddr,'code.jpg')
    img = Image.open('code.jpg')
    img.show()
    vcode = input('输入你看到的验证码:')

    data['captcha-solution'] = vcode
    data['captcha-id'] = captchaId
    #再次请求
    r = s.post(login_url,data=data,verify=True,headers=headers)

if r.url != start_page:
    print(r.text)
    sys.exit('登录错误!')
else:
    print('登入成功!')

#开始抓取个人页
def praseHomePage(homepage):
    douban_user = {}
    douban_user['homepage'] = homepage.url
    home_data = homepage.text
    soup = BeautifulSoup(home_data, 'lxml')  # 获取soup对象
    print(soup.select_one('title').string)

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
    if len(movies_tag)==2:
        want_index = 0
    elif len(movies_tag)==3:
        want_index = 1
    elif len(movies_tag)==0:
        douban_user['want_movie'] = 0
        douban_user['saw_movie'] = 0
        return douban_user
    want_movie_str = str(movies_tag[want_index].string).strip()  # 想看电影
    want_movie_re = re.search('([0-9]+)部', want_movie_str)
    want_movie = want_movie_re.groups()[0]
    douban_user['want_movie'] = want_movie
    saw_movie_str = str(movies_tag[want_index+1].string).strip()  # 想看电影
    saw_movie_re = re.search('([0-9]+)部', saw_movie_str)
    saw_movie = saw_movie_re.groups()[0]
    douban_user['saw_movie'] = saw_movie
    return douban_user

home_user = praseHomePage(r)
#解析follower_link

def praseFollowerPage(follower_page):
    r = s.get(follower_page)
    follower_soup = BeautifulSoup(r.text,'lxml')
    follower_items = follower_soup.select('dl.obu a.nbg')
    page_tag = follower_soup.select_one('span.thispage')
    total_page = page_tag['data-total-page']
    this_page  = page_tag.string
    print(this_page)

    for follower in follower_items:
        print(follower['href'])
        time.sleep(random.randrange(5))
        # follower_homepage = follower['href']
        # print(follower_homepage)
        # follower_user = praseHomePage(s.get(follower_homepage))
        # praseFollowerPage(follower_user['follower_link'],s)
    while this_page <= total_page:
        netx_page = re.sub(r'(.*=)(\d+)',r'\1',follower_page)+str(int(this_page)*70)
        print(netx_page)
        praseFollowerPage(netx_page)
    else:
        print('当前用户的关注者已遍历完')


praseFollowerPage(home_user['follower_link']+'?start=0')



