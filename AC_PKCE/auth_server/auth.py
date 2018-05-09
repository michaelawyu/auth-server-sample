import base64
import cryptography
import hashlib
import json
import jwt
import secrets
import time

from cryptography.fernet import Fernet

#KEY = Fernet.generate_key()
KEY = b'YHD1m3rq3K-x6RxT1MtuGzvyLz4EWIJAEkRtBRycDHA='

ISSUER = 'sample-auth-server'
CODE_LIFE_SPAN = 600
JWT_LIFE_SPAN = 1800

authorization_codes = {}

f = Fernet(KEY)

with open('private.pem', 'rb') as file:
  private_key = file.read()

def authenticate_user_credentials(username, password):
  return True

def authenticate_client(client_id, client_secret):
  return True

def verify_client_info(client_id, redirect_url):
  return True

def generate_code_challenge(code_verifier):
  m = hashlib.sha256()
  m.update(code_verifier.encode())
  code_challenge = m.digest()
  return base64.b64encode(code_challenge, b'-_').decode().replace('=', '')

def generate_access_token():
  payload = {
    "iss": ISSUER,
    "exp": time.time() + JWT_LIFE_SPAN
  }

  access_token = jwt.encode(payload, private_key, algorithm = 'RS256').decode()

  return access_token

def generate_authorization_code(client_id, redirect_url, code_challenge):
  #f = Fernet(KEY)
  authorization_code = f.encrypt(json.dumps({
    "client_id": client_id,
    "redirect_url": redirect_url,
  }).encode())

  authorization_code = base64.b64encode(authorization_code, b'-_').decode().replace('=', '')

  expiration_date = time.time() + CODE_LIFE_SPAN

  authorization_codes[authorization_code] = {
    "client_id": client_id,
    "redirect_url": redirect_url,
    "exp": expiration_date,
    "code_challenge": code_challenge
  }

  return authorization_code

def verify_authorization_code(authorization_code, client_id, redirect_url,
                              code_verifier):
  #f = Fernet(KEY)
  record = authorization_codes.get(authorization_code)
  if not record:
    return False

  client_id_in_record = record.get('client_id')
  redirect_url_in_record = record.get('redirect_url')
  exp = record.get('exp')
  code_challenge_in_record = record.get('code_challenge')

  if client_id != client_id_in_record or \
     redirect_url != redirect_url_in_record:
    return False

  if exp < time.time():
    return False

  code_challenge = generate_code_challenge(code_verifier)
  if code_challenge != code_challenge_in_record:
    return False

  del authorization_codes[authorization_code]

  return True
