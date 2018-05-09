import json
import requests
#import ssl

from flask import (Flask, make_response, render_template, redirect, request,
                   url_for)

AUTH_PATH = 'http://localhost:5001/auth'
TOKEN_PATH = 'http://localhost:5001/token'
RES_PATH = 'http://localhost:5002/users'
REDIRECT_URL = 'http://localhost:5000/callback'

CLIENT_ID = 'sample-client-id'
CLIENT_SECRET = 'sample-client-secret'

app = Flask(__name__)

@app.before_request
def before_request():
  # Redirects user to the login page if access token is not present
  if request.endpoint not in ['login', 'callback']:
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

  users = json.loads(r.text).get('results')

  return render_template('users.html', users = users)

@app.route('/login')
def login():
  # Presents the login page
  return render_template('AC_login.html', 
                         dest = AUTH_PATH,
                         client_id = CLIENT_ID,
                         redirect_url = REDIRECT_URL)

@app.route('/callback')
def callback():
  # Accepts the authorization code and exchanges it for access token
  authorization_code = request.args.get('authorization_code')

  if not authorization_code:
    return json.dumps({
      'error': 'No authorization code is received.'
    }), 500

  r = requests.post(TOKEN_PATH, data = {
    "grant_type": "authorization_code",
    "authorization_code": authorization_code,
    "client_id" : CLIENT_ID,
    "client_secret" : CLIENT_SECRET,
    "redirect_url": REDIRECT_URL
  })
  
  if r.status_code != 200:
    return json.dumps({
      'error': 'The authorization server returns an error: \n{}'.format(
        r.text)
    }), 500
  
  access_token = json.loads(r.text).get('access_token')

  response = make_response(redirect(url_for('main')))
  response.set_cookie('access_token', access_token)
  return response


if __name__ == '__main__':
  #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  #context.load_cert_chain('domain.crt', 'domain.key')
  #app.run(port = 5000, debug = True, ssl_context = context)
  app.run(port = 5000, debug = True)