import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()


class ConcertTimeTableService(object):
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

    def query_concert_time_table_by_id_and_type(self, concert_info_id, concert_time_table_type):

        concert_info_sql = "select * from live_now.concert_time_table "
        concert_info_sql += "  where concert_info_id = %s and concert_time_table_type = %s"

        self.__open__()
        self.__cursor.execute(
            concert_info_sql, (concert_info_id, concert_time_table_type, ))
        result = self.__cursor.fetchall()
        self.__close__()
        if result and len(result) > 0:
            list = [dict(zip(self.__cursor.column_names, row))
                    for row in result]
            return list

        return None


if __name__ == '__main__':
    test = ConcertTimeTableService()
    obj = test.query_concert_time_table_by_id_and_type(405, '演出時間')
    print(obj)
