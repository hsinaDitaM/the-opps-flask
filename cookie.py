"""JWT implementation

Using discord tech yay
"""
from datetime import datetime, timedelta

import jwt
from jwt import PyJWTError

SECRET_KEY = "a_very_very_secure_secret_key"
ALGORITHM = "HS256"

def cookie_token_isvalid(cookies):
    try:
        token = cookies.get("token")
        return isinstance(get_token_payload(token), str)
    except ValueError:
        return False


def create_access_token(data: dict, days: int = None):
    if days is None:
        expires_delta = timedelta(days=999999)
    else:
        expires_delta = timedelta(days=days)

    to_encode = data.copy()
    to_encode.update({
        "exp": datetime.utcnow() + expires_delta,
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_token_payload(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], do_time_check=True)
        return payload
    except PyJWTError:
        return None