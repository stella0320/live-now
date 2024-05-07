from flask import Blueprint
from flask import request
from script.handler.my_artist_handler import MyArtistHandler
singer_info_route = Blueprint("singer_info_route", __name__)


@singer_info_route.route("/api/querySingerInfo")
def query_singer_info():
    member_token = request.args.get('memberToken')
    singer_name = request.args.get('singerName')
    my_artist_handler = MyArtistHandler()
    singer_info_list = my_artist_handler.query_singer_info(
        member_token, singer_name)
    return {
        'data': singer_info_list}


@singer_info_route.route("/api/toggleMemberSingerEvent")
def toggle_member_singer_event():
    member_token = request.args.get('memberToken')
    singer_info_hash_id = request.args.get('singerInfoHashId')

    my_artist_handler = MyArtistHandler()
    member_singer_event = my_artist_handler.toggle_member_calendar_event(
        member_token, singer_info_hash_id)

    return {
        'data': 'success'
    }
