import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()


class ConcertInfoService(object):
    def __init__(self):
        self.__host__ = os.getenv('DB_HOST')
        self.__user__ = os.getenv('DB_USER')
        self.__password__ = os.getenv('DB_PASSWORD')
        self.__database = os.getenv('DB_DATABASE')

    def __open__(self):
        try:
            self.__connect = mysql.connector.connect(
                host=self.__host__, user=self.__user__, database=self.__database,password=self.__password__, pool_name='mypool', pool_size=30)
            self.__cursor = self.__connect.cursor()
        except mysql.connector.Error as e:
            # Todo 測試
            print("Error %s" % (e))

    def __close__(self):
        self.__cursor.close()
        self.__connect.close()

    def __commit__(self):
        self.__connect.commit()

    def query_concert_info_by_id(self, id):

        concert_info_sql = "SELECT e.singer_info_name, f.concert_location_name, d.* FROM ( "
        concert_info_sql += "  select * from live_now.concert_info where concert_info_is_display = 'Y' and concert_info_id = %s"
        concert_info_sql += " ) d"
        concert_info_sql += " left join live_now.singer_info e"
        concert_info_sql += " on d.concert_info_singer_id = e.singer_info_id"
        concert_info_sql += " left join live_now.concert_location f"
        concert_info_sql += " on d.concert_info_location_id = f.concert_location_id"

        self.__open__()
        self.__cursor.execute(concert_info_sql, (id, ))
        result = self.__cursor.fetchall()
        self.__close__()
        if result and len(result) > 0:
            list = [dict(zip(self.__cursor.column_names, row))
                    for row in result]
            return list[0]

        return None


if __name__ == '__main__':
    test = ConcertInfoService()
    obj = test.query_concert_info_by_id(405)
    print(obj)
