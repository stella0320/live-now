from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
import json

# 宣告對映
Base = declarative_base()


class Members(Base):
    # https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#using-orm-declarative-forms-to-define-table-metadata
    __tablename__ = 'members'
    member_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_mail: Mapped[str] = mapped_column(String(256), nullable=False)
    member_line_user_id = mapped_column(String(300), nullable=True)
    member_line_display_name = mapped_column(String(300), nullable=True)
    member_line_profile_pic_url = mapped_column(String(2083), nullable=True)
    member_line_access_token = mapped_column(String(2000), nullable=True)
    member_line_id_token = mapped_column(String(2000), nullable=True)
    member_line_refresh_token = mapped_column(String(2000), nullable=True)
    member_google_account_id = mapped_column(String(300), nullable=True)
    member_google_display_name = mapped_column(String(300), nullable=True)
    member_google_profile_pic_url = mapped_column(String(2083), nullable=True)
    member_google_server_id = mapped_column(String(2000), nullable=True)

    def __repr__(self):
        return f"<members(member_id={self.member_id}, member_mail={self.member_mail})>"
