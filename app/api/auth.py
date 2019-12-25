from flask import g
from flask_httpauth import HTTPTokenAuth
from app.api.errors import error_response


auth_tp = HTTPTokenAuth()


@auth_tp.verify_token
def verify_token(token):
    return False


@auth_tp.error_handler
def token_auth_error():
    return error_response(401)
