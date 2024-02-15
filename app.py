import os
import requests
import json
import logging
from bottle import route, run, hook, request, response

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log',  
                    filemode='a')  

OPA_SERVER = os.environ.get('OPA_SERVER', 'http://opa-service:8181')

DB = {
    'users': [
        'Salem',
        'Lena'
    ]
}

@route('/api/users/<user>', method=['GET', 'POST'])
def serv_users(user):
    logging.info(f"Handling {request.method} request for user: {user}")
    response.content_type = 'application/json'
    if request.method == 'POST':
        DB['users'].append(user)
        logging.info(f"Added user: {user}")
    elif request.method == 'DELETE':
        try:
            DB['users'].remove(user)
            logging.info(f"Removed user: {user}")
        except ValueError as e:
            logging.warning(f"Attempted to remove non-existent user: {user} - {e}")
    return json.dumps({'data': DB['users']})

@route('/error_401', method=['GET', 'POST'])
def error():
    logging.error("Unauthorized access attempt")
    response.body = json.dumps({'Error': 'Unauthorized'})
    response.status = 401
    return response

@hook('before_request')
def has_privs():
    try:
        user = get_user()
        resp = requests.post(OPA_SERVER + '/v1/data/bottle/allow', json={
            'input': {
                'user': user,
                'method': request.method,
            }
        })
        if resp.json()['result']:
            logging.info(f"Access granted for user: {user} with method {request.method}")
            return True
        logging.warning(f"Access denied for user: {user} with method {request.method}")
        request.environ['PATH_INFO'] = '/error_401'
    except Exception as e:
        logging.error(f"Error in access control: {e}")
        request.environ['PATH_INFO'] = '/error_401'
    return False

def get_user():
    return request.headers.get('X-Requesting-User', '')

if __name__ == '__main__':
    logging.info("Starting Bottle server on localhost:8000")
    run(host='localhost', port=8000)
