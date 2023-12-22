import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()


class SingerInfoService():

    def __init__(self):
        self.__host__ = os.getenv('DB_HOST')
        self.__user__ = os.getenv('DB_USER')
        self.__password__ = os.getenv('DB_PASSWORD')

    def __open__(self):
        try:
            self.__connect = mysql.connector.connect(
                host=self.__host__, user=self.__user__, password=self.__password__, pool_name='mypool', pool_size=30)
            self.__cursor = self.__connect.cursor()
        except mysql.connector.Error as e:
            # Todo 測試
            print("Error %s" % (e))

    def __close__(self):
        self.__connect.close()

    def __commit__(self):
        self.__connect.commit()

    def query_singer_info(self, member_id, singer_name):
        singer_table_sql = 'select * from live_now.singer_info'
        if singer_name:
            singer_table_sql += ' where singer_info_name like %s'
        sql = ' select a.*, b.member_singer_event_id from (' + \
            singer_table_sql + ') a '
        sql += ' left join (select * from live_now.member_singer_event where member_id = %s) b '
        sql += ' on a.singer_info_id = b.singer_info_id '
        sql += ' order by a.singer_info_name '
        sql += ' LIMIT 0,10 '

        self.__open__()
        if singer_name:
            singer_name = '%' + singer_name + '%'
            self.__cursor.execute(sql, (singer_name, member_id, ))
        else:
            self.__cursor.execute(sql, (member_id, ))

        result = self.__cursor.fetchall()
        self.__close__()
        if result and len(result) > 0:
            list = [dict(zip(self.__cursor.column_names, row))
                    for row in result]
            return list

        return None
