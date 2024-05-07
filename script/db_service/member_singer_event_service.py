from operator import and_
from ..model.member_singer_event import MemberSingerEvent
from ..db_service.connect_mysql_db import ConnectDb


class MemberSingerEventService(object):

    def __init__(self):
        try:
            self.__connect_db__ = ConnectDb()
            self.__engine__ = self.__connect_db__.get_engine()
            self.__session__ = self.__connect_db__.get_session()
        except Exception as e:
            print(f'exception {e}')

    def create_or_delete_member_singer_event(self, member_id, singer_info_id):
        member_singer_event = self.__session__.query(MemberSingerEvent).filter(
            and_(MemberSingerEvent.member_id == member_id, MemberSingerEvent.singer_info_id == singer_info_id)).first()
        try:
            if member_singer_event:
                # delete
                self.__session__.delete(member_singer_event)
                self.__session__.commit()
            else:
                member_singer_event = MemberSingerEvent(
                    member_id, singer_info_id)
                self.__session__.add(member_singer_event)
                self.__session__.commit()
                member_singer_event = self.__session__.query(MemberSingerEvent).filter(
                    and_(MemberSingerEvent.member_id == member_id, MemberSingerEvent.singer_info_id == singer_info_id)).first()
        except Exception as e:
            print(f'exception {e}')
        finally:
            self.__session__.close()

        return member_singer_event
