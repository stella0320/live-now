from email import header
import os
from urllib import response
from dotenv import load_dotenv
from hashids import Hashids
import requests
import urllib.parse as parse

load_dotenv()


class LineLoginApi(object):

    def __init__(self):
        self.__login_channel_id__ = os.getenv('LINE_LOGIN_CHANNEL_ID')
        self.__login_channel_secrect__ = os.getenv(
            'LINE_LOGIN_CHANNEL_SECRECT')

    def search_user_profile_by_code(self, code):
        access_token_object = self.search_access_token(code)
        if access_token_object and access_token_object['status'] == 200:
            access_token = access_token_object['data']['access_token']
            url = 'https://api.line.me/v2/profile'
            header = {
                'Authorization': 'Bearer ' + access_token
            }

            response = requests.get(url, headers=header)
            status_code = response.status_code

            return {
                'status': status_code,
                'data': response.json()
            }

        return access_token_object

    def search_user_info_by_code(self, code):
        access_token_object = self.search_access_token(code)

        if access_token_object and access_token_object['status'] == 200:
            id_token = access_token_object['data']['id_token']
            url = 'https://api.line.me/oauth2/v2.1/verify'
            headers = {
                'alg': 'HS256',
                'type': 'JWT'
            }
            para = {
                'id_token': id_token,
                'client_id': self.__login_channel_id__
            }
            encode_para = parse.urlencode(para)
            response = requests.post(url, data=encode_para, headers=headers)
            status_code = response.status_code
            return {
                'status': status_code,
                'data': response.json()
            }

        return access_token_object

    def search_access_token(self, code):
        url = 'https://api.line.me/oauth2/v2.1/token'

        # https://developers.line.biz/en/reference/line-login/#issue-access-token
        para = {'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': 'https://live-now.jc-chen.online',
                'client_id': self.__login_channel_id__,
                'client_secret': self.__login_channel_secrect__}

        encode_para = parse.urlencode(para)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, data=encode_para, headers=headers)
        status_code = response.status_code
        data = response.json()

        return {
            'status': status_code,
            'data': data
        }
