from flask import *
import requests
from ..service.concert_info_service import ConcertInfoService
from ..service.concert_time_table_service import ConcertTimeTableService
from ..util.hash_id_service import HashIdService
from ..service.dbService import DbService
concert_info_route = Blueprint("concert_info_route", __name__)


@concert_info_route.route("/api/concert_info/<hash_id>")
def query_concert_info(hash_id):
    hash_id_service = HashIdService()
    id = hash_id_service.decode_id(hash_id)[0]
    concert_info_service = ConcertInfoService()
    concert_info = concert_info_service.query_concert_info_by_id(id)

    concert_info_id = concert_info['concert_info_id']
    sell_ticket_service = ConcertTimeTableService()
    sell_ticket_time_list = sell_ticket_service.query_concert_time_table_by_id_and_type(
        concert_info_id, '售票時間')
    concert_info['sell_ticket_time_list'] = sell_ticket_time_list

    concert_time_service = ConcertTimeTableService()
    concert_time_list = concert_time_service.query_concert_time_table_by_id_and_type(
        concert_info_id, '演出時間')
    concert_info['concert_time_list'] = concert_time_list

    # query_concert_time_table_by_id_and_type

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
