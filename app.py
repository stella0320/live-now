from flask import *
import time
from script.route.concert_info_route import concert_info_route
# from script.service.dbService import DbService
from flask import request

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

app.register_blueprint(concert_info_route)


@app.route('/')
def index():
    return render_template('index.html', time=time.time())


@app.route('/concert/<id>')
def concert(id):

    return render_template('concert.html', time=time.time(), id=id)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3500)
