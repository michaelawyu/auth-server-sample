import json
import requests
#import ssl

from flask import (Flask, make_response, render_template, redirect, request,
                   url_for)

AUTH_PATH = 'http://localhost:5001/auth'
RES_PATH = 'http://localhost:5002/users'

CLIENT_ID = 'sample-client-id'
CLIENT_SECRET = 'sample-client-secret'

app = Flask(__name__)

@app.before_request
def before_request():
  # Redirects user to the login page if access token is not present
  if request.endpoint not in ['login', 'request_token']:
    access_token = request.cookies.get('access_token')
    if access_token:
      pass
    else:
      return redirect(url_for('login'))

@app.route('/')
def main():
  # Retrieves a list of users
  access_token = request.cookies.get('access_token')
  r = requests.get(RES_PATH, headers = {
    'Authorization': 'Bearer {}'.format(access_token)
  })

  if r.status_code != 200:
    return json.dumps({
      'error': 'The resource server returns an error: \n{}'.format(
        r.text)
    }), 500

  contents = json.loads(r.text)
  users = contents.get('results')
  return render_template('users.html', users = users)

@app.route('/login')
def login():
  # Presents the login page
  return render_template('ROPC_login.html')

@app.route('/request_token', methods = ['POST'])
def request_token():
  # Requests access token from the authorization server
  username = request.form.get('username')
  password = request.form.get('password')
  r = requests.post(AUTH_PATH, data = {
    'grant_type': 'password',
    'username': username,
    'password': password,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
  })

  if r.status_code != 200:
    return json.dumps({
      'error': 'The authorization server returns an error: \n{}'.format(
        r.text)
    }), 500

  contents = json.loads(r.text)
  access_token = contents.get('access_token')

  # Writes access token to the cookie
  response = make_response(redirect(url_for('main')))
  response.set_cookie('access_token', access_token)
  
  return response

if __name__ == '__main__':
  #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  #context.load_cert_chain('domain.crt', 'domain.key')
  #app.run(port = 5000, debug = True, ssl_context = context)
  app.run(port = 5000, debug = True)
