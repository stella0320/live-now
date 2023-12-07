from flask import *
import time
from script.route.concert_info_route import concert_info_route
from script.route.line_api_route import line_api_route
from script.api.line_login_api import LineLoginApi
from script.api.google_login_api import GoogleLoginApi
from flask import request
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

app.register_blueprint(concert_info_route)
app.register_blueprint(line_api_route)


@app.route('/', methods=['GET', 'POST'])
def index():

    #### Line#####
    code = request.args.get("code", "")
    # 如果line登入發生錯誤error 要特別導到另一個畫面
    response = None
    if code:
        print("code:" + code)
        line_login_api_service = LineLoginApi()
        response = line_login_api_service.search_user_profile_by_code(code)

        if response['status'] == 200:
            return render_template('index.html', time=time.time(), code=code)

        else:
            return render_template('error.html', error_msg=response['data'])

    #### Google#####
    credential = request.form.get("credential", "")
    user_id = None
    if credential:
        google_login_api = GoogleLoginApi()

        csrf_token_cookie = request.cookies.get('g_csrf_token')
        csrf_token_body = request.form.get('g_csrf_token')

        error_msg = google_login_api.check_csrf_token(
            csrf_token_cookie, csrf_token_body)

        if error_msg:
            return render_template('error.html', error_msg=error_msg)

        user_info = google_login_api.search_user_info(credential)
        if not user_info:
            return render_template('error.html', error_msg='credential is invalid')
        return render_template('index.html', time=time.time(), code=user_info.get('google_account_id'))

    # 身分驗證

    return render_template('index.html', time=time.time(), code="null")


@app.route('/login')
def login():
    google_login_client_id = os.getenv('GOOGLE_LOGIN_CLIENT_ID')
    return render_template('login.html', time=time.time(), google_login_client_id=google_login_client_id)


@app.route('/calendar')
def calandar():
    return render_template('calendar.html')


@app.route('/myArtist')
def myArtist():
    return render_template('my-artist.html')


@app.route('/concert/<id>')
def concert(id):
    return render_template('concert.html', time=time.time(), id=id)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3500)
