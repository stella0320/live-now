from ..db_service.member_private_calendar_service import MemberPrivateCalendarService
from ..service.dbService import DbService


class CalendarHandler():

    def query_concert_time_table(self, member_id, start_day, end_day):
        member_private_calendar_service = MemberPrivateCalendarService()

        private_calendar = member_private_calendar_service.find_or_create_private_calendar(
            'myCalendar', member_id)

        private_calendar_id = getattr(private_calendar, 'private_calendar_id')

        db_service = DbService()
        data = db_service.query_concert_time_table(
            start_day, end_day, private_calendar_id)
        return data
