# Module-wide Dependencies
from flask import Flask, request
import logging
from datetime import datetime
# import pymongo

# Project Dependencies
import data_util


app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True, port=3000)


# Add logging
logging.basicConfig(filename="/var/www/bigapp/logs/" + datetime.now().strftime('bigapp_%Y_%m_%d_%H_%M.log'), level=logging.DEBUG)


@app.before_request
def log_request_info():
    logging.debug('Headers: %s', request.headers)
    logging.debug('Body: %s', request.get_data())


# Retrieve data on user given last_name
@app.route('/user/<last_name>', methods=['GET'])
def get_user_by_name(last_name):
    return 'N/A'


# Receive Webhooks + authorize API
@app.route('/facebook', methods=['GET', 'POST'])
def receive_webhook():
    # If Facebook is verifying the server, return challenge
    if request.method == 'GET':
        return request.args['hub.challenge']

    content = request.get_json()
    for entry in content['entry']:
        id = entry['id']
        fields = entry['changed_fields']
        print("Received a webhook for these fields:", fields)
        data_util.process(id, fields)
    return '', 200


# Test to make sure Flask server works. Just connecting to bigbro.ml will not use
# Flask server, need this route
@app.route('/test', methods=['GET'])
def index():
    return 'Test: OK'
