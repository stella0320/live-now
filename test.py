from calendar import c
from sqlalchemy import update
from jinja2 import select_autoescape
from script import service
from script.db_service.members_service import MembersService
from script.model.members import Members
import sqlalchemy
from sqlalchemy import MetaData, create_engine
from sqlalchemy import Table
from sqlalchemy import insert, select
from sqlalchemy.orm import sessionmaker
import json
from script.db_service.member_private_calendar_service import MemberPrivateCalendarService
from script.db_service.member_calendar_event_service import MemberCalendarEventService
from script.service.dbService import DbService


def session_insert_test():

    engine = create_engine(
        "mysql+pymysql://root:root@localhost/live_now", echo=True)
    Session = sessionmaker(engine)
    # https://docs.sqlalchemy.org/en/20/orm/session.html
    with Session() as session:
        result = None
        # member_obj = {
        #     'member_mail': 'jud40322@gmail.com'
        # }
        member = Members(member_id=1, member_mail='jud40322XXX@gmail.com')
        result = session.add(member)
        session.commit()
        print(result)


def insert_member():
    # https://docs.sqlalchemy.org/en/20/core/dml.html#sqlalchemy.sql.expression.insert
    engine = create_engine(
        "mysql+pymysql://root:root@localhost/live_now", echo=True)
    member_obj = {
        'member_mail': 'jud40322@gmail.com'
    }
    metadata_obj = MetaData()
    table = Table("members", metadata_obj, autoload_with=engine)
    with engine.connect() as conn:
        stmt = (
            insert(table)
            .values(member_obj)
        )
        result = conn.execute(stmt)
        conn.commit()
        id = result.inserted_primary_key
        print(id)


def select_member():
    engine = create_engine(
        "mysql+pymysql://root:root@localhost/live_now", echo=True)
    Session = sessionmaker(engine)
    with Session() as session:
        result = None
        # member = Members(member_id=1, member_mail='jud40322XXX@gmail.com')
        stmt = (select(Members).where(Members.member_id == 2))
        result = session.execute(stmt)
        for row in result:
            print(row)


def update_member():
    engine = create_engine(
        "mysql+pymysql://root:root@localhost/live_now", echo=True)
    Session = sessionmaker(engine)
    metadata_obj = MetaData()

    with Session() as session:
        members_table = Table("members", metadata_obj, autoload_with=engine)
        stmt = update(members_table).where(members_table.c.member_id == 6).values({
            'member_mail': 'jud40322@gmail.com',
            'member_line_user_id': 'jessie0320'
        })
        session.execute(stmt)
        session.commit()


def create_private_calendar_test():
    service = MemberPrivateCalendarService()
    calendar = service.create_private_calendar('myCalendar', 7)
    print(calendar)


if __name__ == "__main__":
    service = DbService()
    calendar_event = service.query_concert_time_table('2024-05-05', '2024-05-12')
    print(calendar_event)
