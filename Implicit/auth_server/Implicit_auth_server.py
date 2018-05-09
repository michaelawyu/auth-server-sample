import json
#import ssl
import urllib.parse as urlparse

from auth import (authenticate_user_credentials, generate_access_token,  
                  verify_client_info, JWT_LIFE_SPAN)
from flask import Flask, redirect, render_template, request
from urllib.parse import urlencode

app = Flask(__name__)

@app.route('/auth')
def auth():
  # Describe the access request of the client and ask user for approval
  client_id = request.args.get('client_id')
  redirect_url = request.args.get('redirect_url')

  if None in [ client_id, redirect_url ]:
    return json.dumps({
      "error": "invalid_request"
    }), 400

  if not verify_client_info(client_id, redirect_url):
    return json.dumps({
      "error": "invalid_client"
    })

  return render_template('Implicit_grant_access.html',
                         client_id = client_id,
                         redirect_url = redirect_url)

def process_redirect_url(redirect_url, new_entries):
  # Prepare the redirect URL
  url_parts = list(urlparse.urlparse(redirect_url))
  queries = dict(urlparse.parse_qsl(url_parts[4]))
  queries.update(new_entries)
  url_parts[4] = urlencode(queries)
  url = urlparse.urlunparse(url_parts)
  return url

@app.route('/signin', methods = ['POST'])
def signin():
  # Issues authorization code
  username = request.form.get('username')
  password = request.form.get('password')
  client_id = request.form.get('client_id')
  redirect_url = request.form.get('redirect_url')

  if None in [username, password, client_id, redirect_url]:
    return json.dumps({
      "error": "invalid_request"
    }), 400

  if not verify_client_info(client_id, redirect_url):
    return json.dumps({
      "error": "invalid_client"
    })  

  if not authenticate_user_credentials(username, password):
    return json.dumps({
      'error': 'access_denied'
    }), 401

  access_token = generate_access_token()

  print(process_redirect_url(redirect_url, {"1":"2"}))

  return redirect(process_redirect_url(redirect_url, {
    'access_token': access_token,
    'token_type': 'JWT',
    'expires_in': JWT_LIFE_SPAN
    }), code = 303)


if __name__ == '__main__':
  #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  #context.load_cert_chain('domain.crt', 'domain.key')
  #app.run(port = 5000, debug = True, ssl_context = context)
  app.run(port = 5001, debug = True)