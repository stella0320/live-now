import os
from dotenv import load_dotenv
from hashids import Hashids
import requests

load_dotenv()


class LineLoginApiService():

    def __init__(self):
        self.__login_channel_id__ = os.getenv('LINE_LOGIN_CHANNEL_ID')
        self.__login_channel_secrect__ = os.getenv(
            'LINE_LOGIN_CHANNEL_SECRECT')

    def getAccessToken(self, code):
        url = 'https://api.line.me/oauth2/v2.1/token'

        # https://developers.line.biz/en/reference/line-login/#issue-access-token
        para = {'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': 'https://live-now.jc-chen.online',
                'client_id': self.__login_channel_id__,
                'client_secret': self.__login_channel_secrect__}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, params=para, headers=headers)
        state = response.status_code
        print('state' + str(state))
        data = response.json()
        return data
