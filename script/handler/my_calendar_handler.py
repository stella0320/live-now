from ..db_service.member_private_calendar_service import MemberPrivateCalendarService
from ..db_service.member_calendar_event_service import MemberCalendarEventService


class MyCalendarHandler():

    def toggle_concert_event_to_private_calendar(self, member_id, concert_time_table_id):

        member_private_calendar_service = MemberPrivateCalendarService()

        private_calendar = member_private_calendar_service.find_or_create_private_calendar(
            'myCalendar', member_id)

        private_calendar_id = getattr(private_calendar, 'private_calendar_id')

        member_calendar_event_service = MemberCalendarEventService()

        member_calendar_event_service.create_or_delete_member_calendar_event(
            private_calendar_id, concert_time_table_id)
