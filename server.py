from flask import Flask, render_template, Response
import combine

server = Flask(__name__)

@server.route('/')
def serve():
    return render_template('app.html')

@server.route('/current.png')
def current():
    image = combine.image()
    return Response(image.getvalue(), mimetype='image/png')

if __name__ == '__main__':
    server.run(port=5000, debug=True)