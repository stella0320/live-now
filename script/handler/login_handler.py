from ..db_service.members_service import MembersService
from ..util.hash_id_service import HashIdService
import jwt
import os


class LoginHandler():

    def line_login(self, line_user_info):

        user_info = {
            'member_mail': line_user_info.get('email'),
            'member_line_user_id': line_user_info.get('sub'),
            'member_line_display_name': line_user_info.get('name'),
            'member_line_profile_pic_url': line_user_info.get('picture')
        }
        member_service = MembersService()

        member = member_service.create_or_update_member(user_info)

        return member

    def create_or_update_member(self, member_obj=None):
        member = None
        if member_obj:
            mail = member_obj.get('member_mail')
            engine = create_engine(
                "mysql+pymysql://root:root@localhost/live_now", echo=True)
            Session = sessionmaker(engine)
            # 把 DB engine 與 session 綁在一起
            Session = sessionmaker(bind=engine)
            with Session() as session:
                try:
                    if mail:
                        #  查詢有返回
                        member = session.query(Members).filter_by(
                            member_mail=mail).first()

                    if member:
                        # update
                        # members_table = self.__table__
                        member_id = getattr(member, 'member_id')
                        # stmt = update(members_table).where(
                        #     members_table.c.member_id == member_id).values()
                        member_obj['member_id'] = member_id
                        # session.execute(stmt)
                        session.execute(update(Members), [member_obj], )
                        session.commit()
                        # pass
                    else:
                        session.add(Members(**member_obj))
                        session.commit()
                        member = session.query(Members).filter_by(
                            member_mail=mail).first()

                except Exception as e:
                    session.rollback()
                    print(f'exception {e}')

        return member

    def google_login(self, google_user_info):
        user_info = {
            'member_mail': google_user_info.get('google_email'),
            'member_google_account_id': google_user_info.get('google_account_id'),
            'member_google_display_name': google_user_info.get('google_display_name'),
            'member_google_profile_pic_url': google_user_info.get('google_profile_pic_url'),
            'member_google_server_id': google_user_info.get('google_server_id')
        }

        member_service = MembersService()
        member = member_service.create_or_update_member(user_info)
        user_token = self.encode_user_token(
            member_id=member.member_id, member_mail=member.member_mail)
        return user_token

    def encode_user_token(self, member_id, member_mail):
        encoded = None
        if member_id and member_mail:
            jwt_key = os.getenv('JWT_KEY')
            jwt_algorithms = os.getenv('JWT_ALGORITHMS')
            data = {
                'member_id': member_id,
                'member_mail': member_mail
            }
            encoded = jwt.encode(data, jwt_key, algorithm=jwt_algorithms)

        return encoded

    def decode_user_token(self, token):
        if token:
            jwt_key = os.getenv('JWT_KEY')
            jwt_algorithms = os.getenv('JWT_ALGORITHMS')
            user_info = jwt.decode(token, jwt_key, algorithms=jwt_algorithms)
            member_id = user_info.get('member_id')
            if member_id:
                member_service = MembersService()
                member = member_service.find_member_by_member_id(member_id)
                return member

        return None

    def user_info_handler(self, member_token):
        member = self.decode_user_token(member_token)
        member_id = getattr(member, 'member_id')
        member_mail = getattr(member, 'member_mail')
        hash_id_service = HashIdService()
        member_hash_id = hash_id_service.encode_member_id(member_id)

        member_display_name = getattr(member, 'member_google_display_name')
        if not member_display_name:
            member_display_name = getattr(member, 'member_line_display_name')

        profile_pic_url = getattr(member, 'member_google_profile_pic_url')
        if not profile_pic_url:
            profile_pic_url = getattr(member, 'member_line_profile_pic_url')

        return {
            'member_hash_id': member_hash_id,
            'member_mail': member_mail,
            'member_display_name': member_display_name,
            'profile_pic_url': profile_pic_url
        }
