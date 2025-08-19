
from SmartApi import SmartConnect
from pyotp import TOTP

# Authenticate with SmartAPI and return JWT and feed tokens

def authenticate(api_key: str, client_code: str, password: str, totp_key: str):
    obj = SmartConnect(api_key=api_key)
    session = obj.generateSession(client_code, password, TOTP(totp_key).now())
    jwt_token = session['data']['jwtToken']
    feed_token = obj.getfeedToken()
    return jwt_token, feed_token
