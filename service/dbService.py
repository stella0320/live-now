import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

class DbService(object):
    def __init__(self):
        self.__host__ = os.getenv('DB_HOST')
        self.__user__ = os.getenv('DB_USER')
        self.__password__ = os.getenv('DB_PASSWORD')

    def __open__(self):
        try:
            self.__connect = mysql.connector.connect(host = self.__host__, user= self.__user__, password= self.__password__, pool_name = 'mypool', pool_size = 30)
            self.__cursor = self.__connect.cursor()
        except mysql.connector.Error as e:
            # Todo 測試
            print("Error %s" % (e))
                

    def __close__(self):
        self.__connect.close()


    def __commit__(self):
        self.__connect.commit()

    def query_concert_time_table(self, start_day, end_day):
        sql = "select b.concert_info_name, b.concert_info_page_url, a.* from "
        sql += " (select * from live_now.concert_time_table "
        sql += " where concert_time_table_datetime between %s and %s "
        sql += " ) a "
        sql += " left join live_now.concert_info b "
        sql += " on a.concert_info_id = b.concert_info_id "
        sql += " order by a.concert_info_id, a.concert_time_table_id "
        self.__open__()
        self.__cursor.execute(sql, (start_day, end_day, ))
        result = self.__cursor.fetchall()
        self.__close__()
        if result and len(result) > 0:
            list = [dict(zip(self.__cursor.column_names, row)) for row in result]
            return list
        
        return None