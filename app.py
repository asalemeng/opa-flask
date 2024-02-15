import os
import requests
import json

from bottle import route, run, hook, request, response

OPA_SERVER = os.environ.get('OPA_SERVER', 'http://opa-service:8181')

DB = {
  'users':[
    'Salem',
    'Lena'
    ]
  }

@route('/users/<user>', method=['GET', 'POST', 'DELETE'])
def serv_users(user):
  response.content_type = 'application/json'
  if request.method == 'POST':
    DB['users'].append(user)
  elif request.method == 'DELETE':
    try:
      DB['users'].remove(user)
    except ValueError:
      pass
  return json.dumps({'data':DB['users']})

@route('/error_401', method=['GET', 'POST', 'DELETE'])
def error():
  response.body = json.dumps({'Error':'Unauthorized'})
  response.status = 401
  return response

@hook('before_request')
def has_privs():
  try:
    resp = requests.post(OPA_SERVER + '/v1/data/bottle/allow', json={
    'input':{
        'user':get_user(),
        'method':request.method,
      }
    })
    if resp.json()['result']:
     return True
    request.environ['PATH_INFO'] = '/error_401'
  except Exception as e:
    request.environ['PATH_INFO'] = '/error_401'
  return False

def get_user():
  return request.headers.get('X-Requesting-User', '')

if __name__ == '__main__':
  run(host='localhost', port=8000)