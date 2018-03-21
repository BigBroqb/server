# Start Flask server
from flask import Flask, request
app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True, port=3000)


# Add logging
import logging
from datetime import datetime
logging.basicConfig(filename="/var/www/bigapp/logs/" + datetime.now().strftime('bigapp_%Y_%m_%d_%H_%M.log'), level=logging.DEBUG)

@app.before_request
def log_request_info():
    logging.debug('Headers: %s', request.headers)
    logging.debug('Body: %s', request.get_data())


# Start MongoDB
import pymongo


# Connect to Facebook Graph
from facebook import GraphAPI
fb_key = ''
with open('/var/www/bigapp/key.txt', 'r') as f:
    fb_key  = f.read().replace('\n', '')
graph = GraphAPI(access_token=fb_key)


demo = {}
@app.route('/demo/<name>',methods=['GET'])
def class_demo(name):
    return demo[name]

def update(id, fields):
    if fields[0] != 'feed':
        print (id,fields)
        return
    content = graph.get_connections(id=id,connection_name='posts')
    message = content['data'][0]['message']
    name = graph.get_object(id=id,fields='last_name')['last_name']
    print(id,message)
    demo[name] = message


# Receive Webhooks + authorize API
@app.route('/facebook', methods=['GET', 'POST'])
def receive_webhook():
    if request.method == 'GET':
        return request.args['hub.challenge']
    else:
        content = request.get_json()
        for entry in content['entry']:
            id = entry['id']
            fields = entry['changed_fields']
            update(id,fields)
        return '', 200


# Test to make sure Flask server works. Just connecting to bigbro.ml will not use
# Flask server, need this route
@app.route('/test', methods=['GET'])
def index():
    return 'Test: OK'
