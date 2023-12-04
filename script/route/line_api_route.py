from flask import Blueprint
import requests

line_api_route = Blueprint("line_api_route", __name__)


@line_api_route.route('/api/line/access/token/<code>')
def accessToken(code):
    url = 'https://api.line.me/oauth2/v2.1/token'

    # https://developers.line.biz/en/reference/line-login/#issue-access-token
    para = {'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'https://live-now.jc-chen.online',
            'client_id': '2001941861',
            'client_secret': '6e0c21c2d89688e0966e00d84095d587'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, params=para, headers=headers)
    data = response.json()
    return data
