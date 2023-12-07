import os
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv

load_dotenv()


class GoogleLoginApi():

    def __init__(self):
        self.__client_id__ = os.getenv('GOOGLE_LOGIN_CLIENT_ID')

    def check_csrf_token(self, csrf_token_cookie, csrf_token_body):
        # https://developers.google.com/identity/gsi/web/guides/verify-google-id-token?hl=zh-tw
        if not csrf_token_cookie:
            return 'No CSRF token in Cookie.'

        if not csrf_token_body:
            return 'No CSRF token in post body.'

        if csrf_token_cookie != csrf_token_body:
            return 'Failed to verify double submit cookie.'

        return None

    def search_user_info(self, credential):
        user_info = None
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(
                credential, requests.Request(), self.__client_id__)

            # https://developers.google.com/identity/account-linking/oauth-with-sign-in-linking?hl=zh-tw#validate_and_decode_the_jwt_assertion
            if idinfo:
                user_info = {
                    'google_account_id': idinfo['sub'],
                    'google_server_id': idinfo['aud'],
                    'google_display_name': idinfo['name'],
                    'google_profile_pic_url': idinfo['picture'],
                    'google_email': idinfo['email'],
                    'google_token': credential
                }
            print(idinfo)

            # 驗證credential : https://developers.google.com/identity/gsi/web/guides/verify-google-id-token?hl=zh-tw

        except ValueError as e:
            print(str(e))

        return user_info
