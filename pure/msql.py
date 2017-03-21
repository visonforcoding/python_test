# coding:utf-8
print('你好')
import MySQLdb
import MySQLdb.cursors
# 打开数据库连接
db = MySQLdb.connect(host='localhost',
                     user='root',
                     passwd='',
                     db='test',
                     cursorclass=MySQLdb.cursors.DictCursor)

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute("SELECT * from USER  LIMIT 10 ")

# 使用 fetchone() 方法获取一条数据库。
data = cursor.fetchall()

print data

# 关闭数据库连接
db.close()