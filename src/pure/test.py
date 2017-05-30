import requests
import hashlib
import random

print(random.randrange(10))

m = hashlib.md5()

m.update('admin'.encode())
print(m.hexdigest())

proxies = {
  "http": "http://1.27.202.173",
  "https": "http://1.27.202.173",
}
headers = {
    # 'User-Agent': ua.random
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

proxy_url = 'http://www.xicidaili.com/nn/1'
# res = requests.get(proxy_url,proxies=proxies)
res = requests.get(proxy_url,headers=headers,timeout=30)
print(res.text)

# #print(res)
# a = '123'
# def foo():
#     print(a)
#
# foo()