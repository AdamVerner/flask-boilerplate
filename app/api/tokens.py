from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import auth_tp


@bp.route('/tokens', methods=['DELETE'])
@auth_tp.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
