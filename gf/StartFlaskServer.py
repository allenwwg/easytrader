from flask import Flask
import os

app = Flask(__name__)

@app.route('/start')
def start():
	os.system('StartFlaskServer.bat')

@app.route('/hello')
def hello():
	return 'I'm running'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,threaded=True,debug=True)