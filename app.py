from flask import *
import time
from script.route.concert_info_route import concert_info_route
from script.route.line_api_route import line_api_route
from script.api.line_login_api import LineLoginApi
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
    code = request.args.get("code", "")
    # 如果line登入發生錯誤error 要特別導到另一個畫面
    response = None
    if code:
        print("code:" + code)
        line_login_api_service = LineLoginApi()
        response = line_login_api_service.search_user_profile_by_code(code)
        return render_template('index.html', time=time.time(), code=code, line_api_response=json.dumps(response))

    return render_template('index.html', time=time.time(), code='google login success')


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
