from flask import request, jsonify, g

from app import db

from app.api import bp
from app.api.auth import auth_tp
from app.api.errors import bad_request, error_response


@bp.route('/ping', methods=['GET'])
@auth_tp.login_required
def ping():
    """Ping server
    .. :quickref: Ping; verify connectivity and authorization

    verify if the server is up and running and the api-key is valid

    :reqheader Authorization: token to authenticate

    :statuscode 200: OK
    :statuscode 401: Unauthorized
    """
    return jsonify({'ping': 'pong'})