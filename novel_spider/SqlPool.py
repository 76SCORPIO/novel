"""
数据库连接池工具
"""

import pymysql
from dbutils.pooled_db import PooledDB
# conn = pymysql.connect(host='localhost',
#                        port=3306,
#                        user='root',
#                        passwd='lhw100418',
#                        db='mysql',
#                        charset='utf8')
class OPMySql:
    def __init__(self,db):
        # 连接池允许的最大连接数，0和None表示没有限制
        self.maxconnections = 0
        # 初始化时，连接池至少创建的空闲连接，0表示不创建
        self.mincached = 2
        # 连接池空闲的最多连接数，0和None表示没有限制
        self.maxcached = 5
        # 连接池中最多共享连接数量，0和None表示全部共享（并没有什么用，始终是所有连接共享）
        self.maxshared = 3
        # 连接池中如果没有可用共享连接后，是否阻塞等待，True表示等待，False表示不等待然后报错
        self.blocking = True
        # 开始会话前执行的命令
        self.setsession = []
        # ping mysql 服务端 检查服务是否可用
        self.ping = 0
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.passwd = 'lhw100418'
        self.db = db
        self.charset = 'utf8'

        try:
            self.pool = PooledDB(
                pymysql,
                maxconnections=self.maxconnections,
                mincached=self.mincached,
                maxcached=self.maxcached,
                blocking=self.blocking,
                ping=self.ping,
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.passwd,
                db=self.db,
                charset=self.charset
            )
        except Exception as e:
            print(f"{e},数据库连接失败！")
        else:
            print("数据库连接成功！")

    def getConn(self):
        con = self.pool.connection()
        cur = con.cursor()
        return con,cur

    def handleSql(self,conn,cur,sql,type):
        if type == "SELECT":
            try:
                cur.execute(sql)
                result_one = cur.fetchone()
                result_all = cur.fetchall()
            except Exception as e:
                print(f"{e},查询失败！")
            else:
                print("查询成功！")
                return result_one,result_all

        elif type == "INSERT":
            try:
                cur.execute(sql)
                conn.commit()
            except Exception as e:
                print(f"{e},插入失败！")
                conn.rollback()
                return False
            else:
                print("插入成功！")
                return True

        elif type == "UPDATE":
            try:
                cur.execute(sql)
                conn.commit()
            except Exception as e:
                print(f"{e},更新失败！")
                conn.rollback()
                return False
            else:
                print("更新成功！")
                return True
        elif type == "DELETE":
            try:
                cur.execute(sql)
                conn.commit()
            except Exception as e:
                print(f"{e},,删除失败！")
                conn.rollback()
                return False
            else:
                print("删除成功！")
                return True



