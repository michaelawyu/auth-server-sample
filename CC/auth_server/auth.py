import cryptography
import jwt
import time

ISSUER = 'sample-auth-server'
LIFE_SPAN = 1800

with open('private.pem', 'rb') as f:
  private_key = f.read()

def authenticate_client(client_id, client_secret):
  return True

def generate_access_token():
  payload = {
    "iss": ISSUER,
    "exp": time.time() + LIFE_SPAN,
  }

  access_token = jwt.encode(payload, private_key, algorithm = 'RS256').decode()

  return access_token
