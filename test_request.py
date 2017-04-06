from bs4 import BeautifulSoup
import urllib.request
import requests
import certifi

s = requests.session()

login_url = 'https://www.douban.com/accounts/login'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
# r = requests.post(login_url, data=data, verify=False, headers=headers)
# print(certifi.where())
r = s.post(login_url, verify=True)
