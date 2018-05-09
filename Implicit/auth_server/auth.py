import jwt
import time

ISSUER = 'sample-auth-server'
JWT_LIFE_SPAN = 1800

authorization_codes = {}

with open('private.pem', 'rb') as f:
  private_key = f.read()

def authenticate_user_credentials(username, password):
  return True

def verify_client_info(client_id, redirect_url):
  return True

def generate_access_token():
  payload = {
    "iss": ISSUER,
    "exp": time.time() + JWT_LIFE_SPAN
  }

  access_token = jwt.encode(payload, private_key, algorithm = 'RS256').decode()

  return access_token
