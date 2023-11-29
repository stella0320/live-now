from flask import *
import requests
from ..service.concert_info_service import ConcertInfoService
from ..service.concert_time_table_service import ConcertTimeTableService
from ..service.hash_id_service import HashIdService
from ..service.dbService import DbService
concert_info_route = Blueprint("concert_info_route", __name__)


@concert_info_route.route("/api/concert_info/<hash_id>")
def query_concert_info(hash_id):
    hash_id_service = HashIdService()
    id = hash_id_service.decode_id(hash_id)[0]
    concert_info_service = ConcertInfoService()
    concert_info_list = concert_info_service.query_concert_info_by_id(id)

    # for concert_info in concert_info_list:
    # ConcertTimeTableService()

    return jsonify({'data': concert_info_list})


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
