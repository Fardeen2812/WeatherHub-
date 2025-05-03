import jwt
import datetime
from datetime import timezone
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set!")

revoked_tokens = set()

def generate_token(username):
    payload = {
        'exp': datetime.datetime.now(timezone.utc) + datetime.timedelta(minutes=30),
        'exp': datetime.datetime.now(timezone.utc) + datetime.timedelta(minutes=30),
        'iss': 'your-app-name',
        'aud': 'your-app-users'
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS512")
    return token

def decode_token(token):
    if is_token_revoked(token):
        return {'error': 'Token has been revoked'}, 401
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS512"], audience='your-app-users')
        if payload.get('iss') != 'your-app-name':
            return {'error': 'Invalid issuer'}, 401
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}, 401
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}, 401
    except Exception as e:
        return {'error': f'An unexpected error occurred: {str(e)}'}, 400

def revoke_token(token):
    revoked_tokens.add(token)

def is_token_revoked(token):
    return token in revoked_tokens