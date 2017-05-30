# coding=utf-8
import pymysql.cursors
import motor.motor_tornado
import tornado.gen
from tornado.ioloop import IOLoop
import time
import threading

select_field = "SELECT `order_id`, `city_id`,`user_id`,`tel`,`driver_id`,`create_time`"

# Connect to the mysql
mysql_conn = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='das',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# connect to mongo
mongo_conn = motor.motor_tornado.MotorClient('192.168.33.10', 27017)


def prep():
    with mysql_conn.cursor() as cursor:
        # Read a single record
        sql = "SELECT count(*) as counts FROM `t_order`"
        cursor.execute(sql)
        result = cursor.fetchone()
        counts = result['counts']
        base_divsor = 10;
        while True:
            if(counts/base_divsor>10):
                base_divsor = base_divsor * 10
            else:
                tnums = counts/base_divsor
                break
        threads = []
        total_t = tnums
        while tnums > 0:
            offset = (tnums -1)*base_divsor
            tnums = tnums -1
            new_th = myThread(total_t-tnums,offset,base_divsor)
            threads.append(new_th)

        for t in threads:
            t.start()



def read_mysql():
    global select_field
    with mysql_conn.cursor() as cursor:
        # Read a single record
        sql = "%s FROM `t_order`" %(select_field)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

def insert_mongo(res):
    for r in res:
        mongo_conn.das.test_coll.insert_one(r)

@tornado.gen.coroutine
def do_insert_mongo():
    res = read_mysql()
    for r in res:
        future = mongo_conn.das.test_coll.insert_one(r)
        result = yield future


# IOLoop.current().run_sync(do_insert_mongo)


class myThread(threading.Thread):

    def __init__(self,threadID,offset,page_size):
        threading.Thread.__init__(self)
        self.mysql_conn = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='das',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        self.name = threadID
        self.offset = offset
        self.page_size = page_size
    def run(self):
        start_time = time.time()
        print '线程%s开启,在:%s' %(self.name,start_time)
        sql = "SELECT `order_id`, `city_id`,`user_id`,`tel`,`driver_id`,`create_time` FROM `t_order` limit %s,%s " %(self.offset,self.page_size)
        print sql
        with self.mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        # IOLoop.current().run_sync(do_insert_mongo(result))
        end_time = time.time()
        speed_time = end_time - start_time
        print '线程%s结束,在:%s.花费%s' %(self.name,end_time,speed_time)


start_time = time.time()
# res = read_mysql()
# insert_mongo(res)
IOLoop.current().run_sync(do_insert_mongo)
end_time = time.time()

speed_time = end_time - start_time

print "花费%s" % speed_time

# prep()
