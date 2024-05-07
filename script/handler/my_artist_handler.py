
from ..handler.login_handler import LoginHandler
from ..service.singer_info_service import SingerInfoService
from ..util.hash_id_service import HashIdService
from ..db_service.member_singer_event_service import MemberSingerEventService


class MyArtistHandler():

    def query_user_info(self, member_token):
        login_handler = LoginHandler()
        member_id = login_handler.get_member_id_by_decode_user_token(
            member_token)
        return member_id

    def query_singer_info(self, member_token, singer_name):
        member_id = self.query_user_info(member_token)
        singer_info_service = SingerInfoService()

        singer_info_list = singer_info_service.query_singer_info(
            member_id, singer_name)
        if singer_info_list:

            for singer_info in singer_info_list:
                hash_id_service = HashIdService()
                singer_info__hash_id = hash_id_service.encode_id(
                    singer_info.get('singer_info_id'))
                singer_info['singer_info_id'] = singer_info__hash_id

        return singer_info_list

    def toggle_member_calendar_event(self, member_token, singer_info_hash_id):
        member_id = self.query_user_info(member_token)
        hash_id_service = HashIdService()
        singer_info_id = hash_id_service.decode_id(singer_info_hash_id)
        member_singer_event_service = MemberSingerEventService()
        member_singer_event = member_singer_event_service.create_or_delete_member_singer_event(
            member_id, singer_info_id)

        return member_singer_event
