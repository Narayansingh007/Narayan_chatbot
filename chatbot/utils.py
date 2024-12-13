from flask import request
from config import JWT_SECRET_KEY

def validate_jwt_token():
    """Validate the JWT token from request headers."""
    token = request.headers.get('x-access-tokens')
    if not token:
        return  "`jwt_token` is missing"
    if token != JWT_SECRET_KEY:
        return  "`jwt_token` is invalid"
    # return token, None
