from flask import Flask, render_template

server = Flask(__name__)

@server.route('/')
def serve():
    return render_template('app.html')
    

if __name__ == '__main__':
    server.run(port=5000, debug=True)