from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

# 宣告對映
Base = declarative_base()


class MemberCalendarEvent(Base):

    __tablename__ = 'member_calendar_event'
    member_calendar_event_id: Mapped[int] = mapped_column(
        Integer, primary_key=True)
    private_calendar_id: Mapped[int] = mapped_column(Integer)
    concert_time_table_id: Mapped[int] = mapped_column(Integer)

    def __init__(self, private_calendar_id, concert_time_table_id):
        self.private_calendar_id = private_calendar_id
        self.concert_time_table_id = concert_time_table_id

    def __repr__(self):
        return f"<MemberCalendarEvent(member_calendar_event_id={self.member_calendar_event_id}, private_calendar_id={self.private_calendar_id}, concert_time_table_id={self.concert_time_table_id})>"
