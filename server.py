from flask import Flask, render_template, Response, jsonify
import pandas as pd
import datetime
import combine
import gfs
import json_response

server = Flask(__name__)

@server.route('/')
def serve():
    return render_template('app.html')

@server.route('/current.png')
def current():
    image = combine.image()
    return Response(image.getvalue(), mimetype='image/png')


@server.route('/data.json')
def json():
    df = gfs.get_data()

    start = pd.Timestamp(datetime.date.today())
    end = start + pd.Timedelta(hours=40)

    data = pd.DataFrame()
    for loc in df.keys():
        data[loc] = df[loc].loc[:end].ghi

    json_dict = json_response.dfHandle(data.reset_index())()
    return jsonify(json_dict)

if __name__ == '__main__':
    server.run(port=5000, debug=True)
