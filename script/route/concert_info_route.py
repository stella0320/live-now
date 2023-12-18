from flask import *
import requests
from ..service.concert_info_service import ConcertInfoService
from ..service.concert_time_table_service import ConcertTimeTableService
from ..db_service.member_private_calendar_service import MemberPrivateCalendarService
from ..util.hash_id_service import HashIdService
from ..service.dbService import DbService
from ..handler.login_handler import LoginHandler
from ..handler.my_calendar_handler import MyCalendarHandler
concert_info_route = Blueprint("concert_info_route", __name__)


@concert_info_route.route("/api/concert_info")
def query_concert_info():

    # concert info
    concert_info_hash_id = request.args.get('concert_info_hash_id')
    hash_id_service = HashIdService()
    id = hash_id_service.decode_id(concert_info_hash_id)[0]
    concert_info_service = ConcertInfoService()
    concert_info = concert_info_service.query_concert_info_by_id(id)
    concert_info_id = concert_info['concert_info_id']

    # member info
    member_token = request.args.get('member_token')
    login_handler = LoginHandler()
    member_id = login_handler.get_member_id_by_decode_user_token(member_token)

    member_private_calendar_service = MemberPrivateCalendarService()
    private_calendar = member_private_calendar_service.find_or_create_private_calendar(
        'myCalendar', member_id)
    private_calendar_id = None
    if private_calendar:
        private_calendar_id = getattr(private_calendar, 'private_calendar_id')
    if private_calendar_id:
        sell_ticket_service = ConcertTimeTableService()
        sell_ticket_time_list = sell_ticket_service.query_concert_time_table_by_id_and_type_and_calendar_id(
            concert_info_id, '售票時間', private_calendar_id)
        concert_info['sell_ticket_time_list'] = sell_ticket_time_list

        concert_time_service = ConcertTimeTableService()
        concert_time_list = concert_time_service.query_concert_time_table_by_id_and_type_and_calendar_id(
            concert_info_id, '演出時間', private_calendar_id)
        concert_info['concert_time_list'] = concert_time_list

    return jsonify({'data': concert_info})


@concert_info_route.route('/api/calendar/queryConcertTimeDataByTimePeriod')
def queryConcertTimeDataByTimePeriod():
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    db_connect = DbService()
    data = db_connect.query_concert_time_table(startDate, endDate)

    if data:
        for item in data:
            hash_id_service = HashIdService()
            concert_info_id = item.get('concert_info_id')
            if concert_info_id:
                concert_info_hash_id = hash_id_service.encode_id(
                    int(concert_info_id))
                item['concert_info_id'] = concert_info_hash_id

    return {
        'data': data
    }


@concert_info_route.route('/api/myCalendar/toggleConcertEventToPrivateCalendar')
def toggle_concert_event_to_private_calendar():

    member_token = request.args.get('member_token')
    login_handler = LoginHandler()
    member_id = login_handler.get_member_id_by_decode_user_token(member_token)
    if not member_id:
        return jsonify(error=True, message='會員期限已過期，請重新登入'), 500

    concert_time_table_id = request.args.get('concert_time_table_id')

    if not concert_time_table_id:
        return jsonify(error=True, message='Concert Time Table Id為空，請重新操作'), 500

    try:
        my_calendar_handler = MyCalendarHandler()
        my_calendar_handler.toggle_concert_event_to_private_calendar(
            member_id, concert_time_table_id)

        return {'data': concert_time_table_id}
    except Exception as e:
        return jsonify(error=True, message=str(e) + ', 請重新操作'), 500
