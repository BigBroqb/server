import math
from facebook import GraphAPI


graph = None

def initFB():
    global graph
    # Connect to Facebook Graph
    fb_key = ''
    with open('/var/www/bigapp/key.txt', 'r') as f:
        fb_key = f.read().replace('\n', '')
    graph = GraphAPI(access_token=fb_key)


# Based on the field received from the Webhook, pull the updated data from Graph API
# @fields = ['feed', 'gender', ...]
# @id = user ID to pull data from
def process(id, fields):
    print('######## Processing')
    args = {'id': id, 'fields': 'last_name,first_name'}
    name = graph.get_object(**args)
    last_name = name['last_name']
    # first_name = name['first_name']
    print('Lastname:', last_name)
    for field in fields:
        print("Field:", field)
    content = graph.get_connections(id=id, connection_name='posts')
    print('Content:\n', content)
    # message = content['data']
    print('########')
