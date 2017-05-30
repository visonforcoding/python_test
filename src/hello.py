from faker import Factory
fake = Factory.create('zh_CN')
for _ in range(0,10):
    print(fake.name()+"-"+fake.address())



