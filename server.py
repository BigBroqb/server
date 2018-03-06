from flask import Flask, request
import logging
from datetime import datetime
 
logging.basicConfig(filename="/var/www/bigapp/logs/" + datetime.now().strftime('bigapp_%H_%M_%d_%m_%Y.log'), level=logging.DEBUG)
app = Flask(__name__)
 
@app.before_request
def log_request_info():
    logging.debug('Headers: %s', request.headers)
    logging.debug('Body: %s', request.get_data())

@app.route('/verify', methods=['GET'])
def handle_verification():
    return request.args['hub.challenge']

if __name__ == '__main__':
    app.run(debug=True, port=3000)
