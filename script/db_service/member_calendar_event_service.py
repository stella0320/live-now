from operator import and_
from ..model.member_calendar_event import MemberCalendarEvent
from ..db_service.connect_mysql_db import ConnectDb


class MemberCalendarEventService(object):

    def __init__(self):
        try:
            self.__connect_db__ = ConnectDb()
            self.__engine__ = self.__connect_db__.get_engine()
            self.__session__ = self.__connect_db__.get_session()
        except Exception as e:
            print(f'exception {e}')

    def create_or_delete_member_calendar_event(self, private_calendar_id, concert_time_table_id):
        member_calendar_event = self.__session__.query(MemberCalendarEvent).filter(
            and_(MemberCalendarEvent.private_calendar_id == private_calendar_id,
                 MemberCalendarEvent.concert_time_table_id == concert_time_table_id)).first()
        try:
            if member_calendar_event:
                self.__session__.delete(member_calendar_event)
                self.__session__.commit()
            else:
                member_calendar_event = MemberCalendarEvent(
                    private_calendar_id, concert_time_table_id)
                self.__session__.add(member_calendar_event)
                self.__session__.commit()
                member_calendar_event = self.__session__.query(MemberCalendarEvent).filter(
                    and_(MemberCalendarEvent.private_calendar_id == private_calendar_id,
                         MemberCalendarEvent.concert_time_table_id == concert_time_table_id)).first()
        except Exception as e:
            print(f'exception {e}')
        finally:
            self.__session__.close()

        return member_calendar_event
