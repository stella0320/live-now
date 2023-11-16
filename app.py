from flask import *
import time
from service.dbService import DbService
from flask import request

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route('/')
def index():
    return render_template('index.html', time=time.time())


@app.route('/api/calendar/queryConcertTimeDataByTimePeriod')
def queryConcertTimeDataByTimePeriod():
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')

    db_connect = DbService()
    data = db_connect.query_concert_time_table(startDate, endDate)
    return {
        'data': data
    }


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3500)