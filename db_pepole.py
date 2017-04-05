from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import urllib.request
import requests
from PIL import Image

s = requests.session()

login_url = 'https://www.douban.com/accounts/login'
# username = input('请输入手机号或者邮箱:')
# passwd = input('请输入密码:')
username = '18316629973'
passwd = 'pwd'
data = {
    'form_email': username,
    'form_password': passwd,
    'login': '登录'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
# r = requests.post(login_url, data=data, verify=False, headers=headers)

r = s.post(login_url,data=data,verify=True,headers=headers)

#获取图片验证码
soup = BeautifulSoup(r.text,'lxml')
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

print(r.text)

