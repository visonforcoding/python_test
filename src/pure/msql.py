# coding:utf-8
print('你好')
import MySQLdb
import MySQLdb.cursors

# 打开数据库连接
db = MySQLdb.connect(host='localhost',
                     user='root',
                     passwd='',
                     db='test',
                     charset="utf8",
                     use_unicode= True,
                     cursorclass=MySQLdb.cursors.DictCursor)

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute("SELECT * from USER ORDER BY id DESC LIMIT 10 ")

# 使用 fetchone() 方法获取所有数据行
datas = cursor.fetchall()

for user in datas:
    user_list = user.items();
    for user_l in user_list:
        print user_l[0],user_l[1]


# 关闭数据库连接
db.close()