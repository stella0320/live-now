import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()


class DbService(object):
    def __init__(self):
        self.__host__ = os.getenv('DB_HOST')
        self.__user__ = os.getenv('DB_USER')
        self.__password__ = os.getenv('DB_PASSWORD')
        self.__database = os.getenv('DB_DATABASE')

    def __open__(self):
        try:
            self.__connect = mysql.connector.connect(
                host=self.__host__, user=self.__user__, database=self.__database, password=self.__password__, pool_name='mypool', pool_size=30)
            self.__cursor = self.__connect.cursor()
        except mysql.connector.Error as e:
            print("Error %s" % (e))

    def __close__(self):
        self.__cursor.close()
        self.__connect.close()

    def __commit__(self):
        self.__connect.commit()

    def query_concert_time_table_by_my_calendar(self, start_day, end_day, private_calendar_id):
        member_calendar_event_query_sql = "select a.member_calendar_event_id , b.* from (select * from live_now.member_calendar_event where private_calendar_id = %s) a "
        member_calendar_event_query_sql += " inner join (select * from live_now.concert_time_table where concert_time_table_datetime between %s and %s) b"
        member_calendar_event_query_sql += " on a.concert_time_table_id = b.concert_time_table_id "

        query_sql = "select d.concert_info_name, d.concert_info_page_url, e.singer_info_name, f.concert_location_name, c.* from ( "
        query_sql += member_calendar_event_query_sql
        query_sql += ") c "
        query_sql += " inner join (select * from live_now.concert_info where concert_info_is_display = 'Y') d "
        query_sql += " on c.concert_info_id = d.concert_info_id "
        query_sql += " left join live_now.singer_info e "
        query_sql += " on d.concert_info_singer_id = e.singer_info_id "
        query_sql += " left join live_now.concert_location f "
        query_sql += " on d.concert_info_location_id = f.concert_location_id "
        query_sql += " order by c.concert_time_table_datetime desc "

        self.__open__()
        self.__cursor.execute(
            query_sql, (private_calendar_id, start_day, end_day, ))
        result = self.__cursor.fetchall()
       
        self.__close__();
        if result and len(result) > 0:
            list = [dict(zip(self.__cursor.column_names, row))
                    for row in result]
            return list

        return None

    def query_concert_time_table_with_private_calendar_id(self, start_day, end_day, private_calendar_id):
        concert_info_sql = "SELECT * FROM live_now.concert_info d "
        # concert_info_sql = "SELECT e.singer_info_name, f.concert_location_name, d.* FROM live_now.concert_info d "
        # concert_info_sql += " left join live_now.singer_info e"
        # concert_info_sql += " on d.concert_info_singer_id = e.singer_info_id"
        # concert_info_sql += " left join live_now.concert_location f"
        # concert_info_sql += " on d.concert_info_location_id = f.concert_location_id"
        concert_info_sql += " where d.concert_info_is_display = 'Y' "

        sql = "select g.member_calendar_event_id, b.concert_info_name, b.concert_info_page_url, e.singer_info_name, f.concert_location_name, a.* from "
        sql += " (select * from live_now.concert_time_table "
        sql += " where concert_time_table_datetime between %s and %s "
        sql += " ) a "
        sql += " inner join (" + concert_info_sql + " ) b "
        sql += " on a.concert_info_id = b.concert_info_id "
        sql += " left join live_now.singer_info e"
        sql += " on b.concert_info_singer_id = e.singer_info_id"
        sql += " left join live_now.concert_location f"
        sql += " on b.concert_info_location_id = f.concert_location_id"
        sql += " left join (select * from live_now.member_calendar_event where private_calendar_id = %s) g"
        sql += " on g.concert_time_table_id = a.concert_time_table_id"
        sql += " order by a.concert_info_id, a.concert_time_table_id "
        self.__open__()
        self.__cursor.execute(sql, (start_day, end_day, private_calendar_id, ))
        result = self.__cursor.fetchall()
        
        self.__close__()
        if result and len(result) > 0:
            list = [dict(zip(self.__cursor.column_names, row))
                    for row in result]
            return list

        return None

    def query_concert_time_table(self, start_day, end_day):
            concert_info_sql = "SELECT * FROM live_now.concert_info d "
            concert_info_sql += " where d.concert_info_is_display = 'Y' "

            sql = "select b.concert_info_name, b.concert_info_page_url, e.singer_info_name, f.concert_location_name, a.* from "
            sql += " (select * from live_now.concert_time_table "
            sql += " where concert_time_table_datetime between %s and %s "
            sql += " ) a "
            sql += " inner join (" + concert_info_sql + " ) b "
            sql += " on a.concert_info_id = b.concert_info_id "
            sql += " left join live_now.singer_info e"
            sql += " on b.concert_info_singer_id = e.singer_info_id"
            sql += " left join live_now.concert_location f"
            sql += " on b.concert_info_location_id = f.concert_location_id"
            sql += " order by a.concert_info_id, a.concert_time_table_id "
            self.__open__()
            self.__cursor.execute(sql, (start_day, end_day, ))
            result = self.__cursor.fetchall()
            
            self.__close__()
            if result and len(result) > 0:
                list = [dict(zip(self.__cursor.column_names, row))
                        for row in result]
                return list

            return None
