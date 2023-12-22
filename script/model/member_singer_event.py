from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

Base = declarative_base()


class MemberSingerEvent(Base):

    __tablename__ = 'member_singer_event'
    member_singer_event_id: Mapped[int] = mapped_column(
        Integer, primary_key=True)
    member_id: Mapped[int] = mapped_column(
        Integer, nullable=True)
    singer_info_id: Mapped[int] = mapped_column(Integer, nullable=True)

    def __init__(self, member_id, singer_info_id):
        self.member_id = member_id
        self.singer_info_id = singer_info_id

    def __repr__(self):
        return f"<MemberSingerEvent(member_singer_event_id={self.member_singer_event_id}, member_id={self.member_id}, singer_info_id={self.singer_info_id})>"
