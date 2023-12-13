from unittest import result
from ..db_service.connect_mysql_db import ConnectDb
from ..model.members import Members
import logging
from sqlalchemy import insert, select, update, Table, MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload
# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


class MembersService(object):

    def __init__(self):
        try:
            self.__connect_db__ = ConnectDb()
            self.__engine__ = self.__connect_db__.get_engine()
            self.__session__ = self.__connect_db__.get_session()
            # metadata_obj = MetaData()
            # members_table = Table("members", metadata_obj,
            #                       autoload_with=self.__engine__)
            # self.__table__ = members_table
            pass
        except Exception as e:
            print(f'exception {e}')

    def find_member_by_member_id(self, member_id):
        if member_id:
            member = self.__session__.query(Members).filter_by(
                member_id=member_id).first()
            return member

    def insert_member(self, member_obj):
        result = None
        with self.__engine__.connect() as connect:
            stmt = insert(Members).values(
                member_obj).returning(Members.c.member_id)
            result = connect.execute(stmt)
            connect.commit()

        return result

    def create_or_update_member(self, member_obj=None):
        member = None
        if member_obj:
            mail = member_obj.get('member_mail')
            try:
                if mail:
                    #  查詢有返回
                    member = self.__session__.query(Members).filter_by(
                        member_mail=mail).first()

                if member:
                    # update
                    # members_table = self.__table__
                    member_id = getattr(member, 'member_id')
                    # stmt = update(members_table).where(
                    #     members_table.c.member_id == member_id).values()
                    member_obj['member_id'] = member_id
                    # session.execute(stmt)
                    self.__session__.execute(update(Members), [member_obj], )
                    self.__session__.commit()
                    member = self.__session__.query(Members).filter_by(
                        member_mail=mail).first()
                    # pass
                else:
                    self.__session__.add(Members(**member_obj))
                    self.__session__.commit()
                    member = self.__session__.query(Members).filter_by(
                        member_mail=mail).first()

            except Exception as e:
                self.__session__.rollback()
                print(f'exception {e}')

            finally:
                self.__session__.close()

        return member
