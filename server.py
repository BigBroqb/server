# Module-wide Dependencies
from flask import Flask, request
import logging
from datetime import datetime

# Project Dependencies
# import data_util
from user import User

from facebook import GraphAPI


FB_APP_SECRET = ''
FB_APP_ID = ''
graph = GraphAPI(access_token=FB_APP_SECRET)

app = Flask(__name__)


# # Add logging
# logging.basicConfig(filename="/var/www/bigapp/logs/" + datetime.now().strftime('bigapp_%Y_%m_%d_%H_%M.log'), level=logging.DEBUG)
# @app.before_request
# def log_request_info():
#     logging.debug('Headers: %s', request.headers)
#     logging.debug('Body: %s', request.get_data())


# Retrieve data on user given facebook token
@app.route('/user/<token>', methods=['GET']) # reconsider using urls
def get_user_by_name(token):

    # authenticate
    fb = graph.request('debug_token', args={'input_token':token})['data']
    if 'user_id' not in fb:
        return 'expired'

    id = fb['user_id']
    args = {'id': id, 'fields': 'last_name,first_name'}
    name = graph.get_object(**args)

    # check if user exists in database

        # if exists get user model from database

        # if not exists make user model and put in database

    #return user.export_json()
    return name['first_name'] + ' ' + name['last_name']


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


if __name__ == '__main__':
    app.run(debug=True, port=3000)