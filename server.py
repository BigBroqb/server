# Module-wide Dependencies
from flask import Flask, request, jsonify
import logging
from datetime import datetime
from facebook import GraphAPI

# Project Dependencies
from user import User
import database as db
import config


graph = GraphAPI(access_token=config.FB_APP_SECRET)
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
    if fb == None or 'user_id' not in fb:
        return 'invalid token, may be expired'
        
    id = fb['user_id']
    args = {'id': id, 'fields': 'last_name, first_name, gender, birthday, location'}
    fb_data = graph.get_object(**args)    
    user = User(id, fb_data)

    if db.add_user_data(user) == 409: # HTTP code for conflict
        db.update_user_data(user)

    return jsonify(user.export_dict())


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