#import requests
import hashlib

m = hashlib.md5()

m.update('admin'.encode())
print(m.hexdigest())

#res = requests.get('https://github.com', verify=True)

#print(res)