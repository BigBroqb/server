from flask import Flask, request
import logging
from datetime import datetime
from cassandra.cluster import Cluster
# cluster = Cluster()
# session = cluster.connect()
 
logging.basicConfig(filename="/var/www/bigapp/logs/" + datetime.now().strftime('bigapp_%Y_%m_%d_%H_%M.log'), level=logging.DEBUG)
app = Flask(__name__)
 
from facebook import GraphAPI
graph = GraphAPI(access_token="216064342468691|KtxNEAMbJLhAs1kZTtw5Ym_YnYo")
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

@app.before_request
def log_request_info():
    logging.debug('Headers: %s', request.headers)
    logging.debug('Body: %s', request.get_data())

@app.route('/facebook', methods=['GET', 'POST'])
def handle_verification():
    if request.method == 'GET':
        return request.args['hub.challenge']
    else:
        content = request.get_json()
        for entry in content['entry']:
            id = entry['id']
            fields = entry['changed_fields']
            update(id,fields)
        return 'OK'

@app.route('/test', methods=['GET'])
def index():
    return 'Test: OK'

if __name__ == '__main__':
    app.run(debug=True, port=3000)
