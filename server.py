# Module-wide Dependencies
from flask import Flask, request, jsonify
import logging
from datetime import datetime
from facebook import GraphAPI
from celery import Celery

# Project Dependencies
from user import User
import database as db
import config
import emails.send_email


graph = GraphAPI(access_token=config.FB_APP_SECRET)
app = Flask(__name__)
#app.config['CELERY_BROKER_URL'] = 'redis://:GSy5Nv2s2ekhbBxBE8ivRIAcfnpR0Oqm@redis-16637.c14.us-east-1-3.ec2.cloud.redislabs.com:16637'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://:GSy5Nv2s2ekhbBxBE8ivRIAcfnpR0Oqm@redis-16637.c14.us-east-1-3.ec2.cloud.redislabs.com:16637'

#celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
#celery.conf.update(app.config)

#@celery.task
#def send_async_email(user):
#    with app.app_context():
#        emails.send_email.send_email(user)

# # Add logging
# logging.basicConfig(filename="/var/www/bigapp/logs/" + datetime.now().strftime('bigapp_%Y_%m_%d_%H_%M.log'), level=logging.DEBUG)
# @app.before_request
# def log_request_info():
#     logging.debug('Headers: %s', request.headers)
#     logging.debug('Body: %s', request.get_data())

def get_user_from_fb(id):
    args = {'id': id, 'fields': 'last_name, first_name, gender, birthday, location'}
    fb_data = graph.get_object(**args)    
    user = User(id, fb_data)
    return user


# Retrieve data on user given facebook token
@app.route('/user/<token>', methods=['GET']) # reconsider using urls
def get_user_by_name(token):

    # authenticate
    fb = graph.request('debug_token', args={'input_token':token})['data']
    if fb == None or 'user_id' not in fb:
        return 'invalid token, may be expired'

    user = get_user_from_fb(fb['user_id'])

    if db.add_user_data(user) == 409: # HTTP code for conflict
        db.update_user_data(user)

    #send_async_email(user)

    return jsonify(user.export_dict())


# Receive Webhooks + authorize API
@app.route('/facebook', methods=['GET', 'POST'])
def receive_webhook():
    # If Facebook is verifying the server, return challenge
    if request.method == 'GET':
        return request.args['hub.challenge']

    content = request.get_json()
    for entry in content['entry']:
        print('Received webhook for',entry['id'])
        user = get_user_from_fb(entry['id'])
        if db.add_user_data(user) == 409: # HTTP code for conflict
            db.update_user_data(user)

    return '', 200


# Test to make sure Flask server works. Just connecting to bigbro.ml will not use
# Flask server, need this route
@app.route('/test', methods=['GET'])
def index():
    return 'Test: OK'


if __name__ == '__main__':
    app.run(debug=True, port=3000)
