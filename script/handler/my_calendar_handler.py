from ..db_service.member_private_calendar_service import MemberPrivateCalendarService
from ..db_service.member_calendar_event_service import MemberCalendarEventService
from ..service.dbService import DbService


class MyCalendarHandler():

    def toggle_concert_event_to_private_calendar(self, member_id, concert_time_table_id):

        member_private_calendar_service = MemberPrivateCalendarService()

        private_calendar = member_private_calendar_service.find_or_create_private_calendar(
            'myCalendar', member_id)

        private_calendar_id = getattr(private_calendar, 'private_calendar_id')

        member_calendar_event_service = MemberCalendarEventService()

        member_calendar_event_service.create_or_delete_member_calendar_event(
            private_calendar_id, concert_time_table_id)

    def query_concert_time_table_by_my_calendar(self, member_id, start_day, end_day):
        member_private_calendar_service = MemberPrivateCalendarService()

        private_calendar = member_private_calendar_service.find_or_create_private_calendar(
            'myCalendar', member_id)

        private_calendar_id = getattr(private_calendar, 'private_calendar_id')

        db_service = DbService()
        data = db_service.query_concert_time_table_by_my_calendar(
            start_day, end_day, private_calendar_id)
        return data
