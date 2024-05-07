from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

# 宣告對映
Base = declarative_base()


class MemberPrivateCalendar(Base):
    __tablename__ = 'member_private_calendar'
    private_calendar_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    private_calendar_name: Mapped[str] = mapped_column(
        String(10), nullable=False)
    member_id: Mapped[int] = mapped_column(Integer, nullable=False)

    def __init__(self, private_calendar_name, member_id):
        self.private_calendar_name = private_calendar_name
        self.member_id = member_id

    def __repr__(self):
        return f"<MemberPrivateCalendar(private_calendar_id={self.private_calendar_id}, private_calendar_name={self.private_calendar_name}, member_id={self.member_id})>"
