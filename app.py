from flask import *
import time
from script.db_service.members_service import MembersService
from script.route.concert_info_route import concert_info_route
from script.route.line_api_route import line_api_route
from script.route.singer_info_route import singer_info_route
from script.api.line_login_api import LineLoginApi
from script.api.google_login_api import GoogleLoginApi
from script.handler.login_handler import LoginHandler
from flask import request
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["JSON_AS_ASCII"] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

app.register_blueprint(concert_info_route)
app.register_blueprint(line_api_route)
app.register_blueprint(singer_info_route)


@app.route('/special/login', methods=['GET', 'POST'])
def special_login():
    member_token = None
    #### Line#####
    code = request.args.get("code", "")
    # 如果line登入發生錯誤error 要特別導到另一個畫面
    response = None
    if code:
        print("code:" + code)
        line_login_api_service = LineLoginApi()
        response = line_login_api_service.search_user_profile_by_code(code)

        if response['status'] == 200:
            user_info = response['data']
            print(user_info)
            line_login_handler = LoginHandler()
            line_member = line_login_handler.line_login(user_info)
            return render_template('index.html', time=time.time(), code=json.dumps(line_member))

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

        google_login_handler = LoginHandler()
        member_token = google_login_handler.google_login(user_info)
        return render_template('index.html', time=time.time(), code=member_token)

    # 身分驗證
    return render_template('index.html', time=time.time())

@app.route('/api/user/auth', methods = ['PUT'])
def userAuth():
    form = request.get_json()
    mail = form['mail']
    password = form['password']

    if not mail:
        return jsonify(error=True, message="登入失敗，需要填寫信箱"), 400
    
    if not password:
        return jsonify(error=True, message="登入失敗，需要填寫密碼"), 400

    members_service = MembersService()
    member = members_service.find_member_by_member_mail(member_mail=mail)

    if member:
        member_password_db = getattr(member, 'member_password')
        if member_password_db != password:
            return jsonify(error=True, message="登入失敗，密碼錯誤"), 400
        
        login_handler = LoginHandler()
        member_id = getattr(member, 'member_id')
        member_token = login_handler.encode_user_token(member_id, mail)
        return {
            'memberToken' : member_token
        }
    
    return jsonify(error=True, message="登入失敗，請先註冊信箱"), 400

@app.route("/api/user", methods = ['POST'])
def registrateNewUser():
    try:
        data = request.get_json()
        name = data['name']
        mail = data['mail']
        userPassword = data['password']
        if not name:
            return jsonify(error=True, message="註冊失敗，需要填寫姓名"), 400
        elif (len(name) > 50):
            return  jsonify(error=True, message="註冊失敗，姓名長度不能超過50個字"), 400

        if not mail:
            return jsonify(error=True, message="註冊失敗，需要填寫信箱"), 400
        elif (len(mail) > 50):
            return jsonify(error=True, message="註冊失敗，信箱長度不能超過50個字"), 400

        if not userPassword:
            return jsonify(error=True, message="註冊失敗，需要填寫密碼"), 400
        elif (len(userPassword) > 30):
            return jsonify(error=True, message="註冊失敗，密碼長度不能超過30個字"), 400

        members_service = MembersService()
        member = members_service.find_member_by_member_mail(mail)
        if not member:
            members_create_service = MembersService()
            
            member_info = {
                'member_mail': mail,
                'member_password':userPassword,
                'member_google_display_name': name
            }

            member_service = MembersService()
            member = member_service.create_or_update_member(member_info)
        else:
            return jsonify(error=True, message="註冊失敗，Email已經註冊帳戶"), 400
    except Exception as e:
        app.logger.error(str(e), exc_info=True)
        return jsonify(error=True, message=str(e)), 
    return "註冊成功，請登入系統";


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', time=time.time())

@app.route('/api/searchUserInfo')
def searchUserInfo():
    member_token = request.headers.get('Authorization')
    login_handler = LoginHandler()
    user_info = login_handler.user_info_handler(member_token)

    return {'data': user_info}


@app.route('/login')
def login():
    google_login_client_id = os.getenv('GOOGLE_LOGIN_CLIENT_ID')
    return render_template('login.html', time=time.time(), google_login_client_id=google_login_client_id)


@app.route('/myCalendar')
def myCalendar():
    return render_template('my-calendar.html', time=time.time())


@app.route('/myArtists')
def myArtists():
    return render_template('my-artists.html', time=time.time())


@app.route('/concert/<id>')
def concert(id):
    return render_template('concert.html', time=time.time(), id=id)

@app.route('/google216f494416c40ce0.html')
def read_html():
    return render_template('google216f494416c40ce0.html')



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3500)
