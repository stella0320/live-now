from flask import *
import time
from script.route.concert_info_route import concert_info_route
from script.route.line_api_route import line_api_route
from script.service.line_login_api_service import LineLoginApiService
from flask import request


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

app.register_blueprint(concert_info_route)
app.register_blueprint(line_api_route)


@app.route('/')
def index():
    code = request.args.get("code", "")
    response = None
    if code:
        print("code:" + code)
        line_login_api_service = LineLoginApiService()
        response = line_login_api_service.getAccessToken(code)
        print(response)

    return render_template('index.html', time=time.time(), code=code, line_api_response=json.dumps(response))


@app.route('/login')
def login():
    return render_template('login.html', time=time.time())


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
