import redis
print('这一节我们来连接redis')

r = redis.StrictRedis()
res = r.set('foo','bar')
print(res)
print(r)