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


if __name__ == "__main__":
    member_obj = {
        'member_mail': 'jud40322@gmail.com',
        'member_google_display_name': '123'
    }
    if member_obj:
        mail = member_obj.get('member_mail')
        engine = create_engine(
            "mysql+pymysql://root:root@localhost/live_now", echo=True)
        Session = sessionmaker(engine)

    with Session() as session:
        try:
            if mail:
                #  查詢有返回
                member = session.query(Members).filter_by(
                    member_mail=mail).first()

            if member:
                # update
                # members_table = self.__table__
                member_id = getattr(member, 'member_id')
                # stmt = update(members_table).where(
                #     members_table.c.member_id == member_id).values()
                member_obj['member_id'] = member_id
                # session.execute(stmt)
                session.execute(update(Members), [member_obj], )
                session.commit()
                # pass
            else:
                session.add(Members(**member_obj))
                session.commit()
                member = session.query(Members).filter_by(
                    member_mail=mail).first()

        except Exception as e:
            session.rollback()
            print(f'exception {e}')
