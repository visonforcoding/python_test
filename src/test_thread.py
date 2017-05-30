import threading
import time

class mythread(threading.Thread):
    def __init__(self,threadId,name,nums):
        threading.Thread.__init__(self)
        self.name = name
        self.nums = nums
        self.threadId = threadId

    def run(self):
        print("开始线程：" + self.name)
        while self.nums > 10:
            self.nums -=1
            time.sleep(1)
            if(self.threadId == 1):
                print('线程1')
            print("%s: %s %s" % (self.name,self.nums,time.ctime(time.time())))
        print("退出线程:"+self.name)

nums = 22
t1 = mythread(1,"t1",nums)
t2 = mythread(2,"t2",nums)

t1.start()
t2.start()

t1.join()
t2.join()
print ("退出主线程")

