from flask import Flask, render_template, Response, jsonify
from flask_cors import CORS
import pandas as pd
import datetime
import combine
import gfs
import json_response
import himawari
import io
import imageio

server = Flask(__name__)
CORS(server)

@server.route('/')
def serve():
    return render_template('app.html')

@server.route('/current.png')
def current():
    image = combine.image()
    return Response(image.getvalue(), mimetype='image/png')

@server.route('/satellite.png')
def satellite():
    sat = himawari.getimage()
    retval = io.BytesIO()
    imageio.imwrite(retval, sat, format="png")
    return Response(retval.getvalue(), mimetype='image/png')

@server.route('/data.json')
def json():
    df = gfs.get_data()

    start = pd.Timestamp(datetime.date.today(), tz="UTC")
    end = start + pd.Timedelta(hours=40)

    data = pd.DataFrame()
    for loc in df.keys():
        data[loc] = df[loc].loc[:end].ghi

    json_dict = json_response.dfHandle(data.reset_index())()
    return jsonify(json_dict)

if __name__ == '__main__':
    server.run(port=5000, debug=True, ssl_context='adhoc')
