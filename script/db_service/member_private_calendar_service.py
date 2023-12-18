from operator import and_
from ..db_service.connect_mysql_db import ConnectDb
from ..model.member_private_calendar import MemberPrivateCalendar


class MemberPrivateCalendarService(object):

    def __init__(self):
        try:
            self.__connect_db__ = ConnectDb()
            self.__engine__ = self.__connect_db__.get_engine()
            self.__session__ = self.__connect_db__.get_session()
        except Exception as e:
            print(f'exception {e}')

    def find_or_create_private_calendar(self, private_calendar_name, member_id):
        calendar = None
        if member_id:
            try:

                calendar = self.__session__.query(MemberPrivateCalendar).filter(
                    and_(MemberPrivateCalendar.private_calendar_name == private_calendar_name,
                         MemberPrivateCalendar.member_id == member_id)).first()

                if not calendar:

                    #  查詢有返回
                    new_calendar = MemberPrivateCalendar(
                        private_calendar_name, member_id)
                    self.__session__.add(new_calendar)
                    self.__session__.commit()
                    calendar = self.__session__.query(MemberPrivateCalendar).filter(
                        and_(MemberPrivateCalendar.private_calendar_name == private_calendar_name,
                             MemberPrivateCalendar.member_id == member_id)).first()

            except Exception as e:
                self.__session__.rollback()
                print(f'exception {e}')

            finally:
                self.__session__.close()

        return calendar
