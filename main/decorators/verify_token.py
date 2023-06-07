from functools import wraps
import requests
from flask import request, make_response, jsonify, g


def verify_token():
    """
    To verify bearer token in request and to validate it from user management portal.
    :return:
    """

    def verify(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return make_response(jsonify({
                    "msg": "Missing Authorization Header"
                }), 401)
            identity = requests.get("http://127.0.0.1:10001/auth/verify", headers={"Authorization": token})
            if not identity.status_code == 200:
                return make_response(jsonify(identity.json()), identity.status_code)
            else:
                g.user = identity
            return f(*args, **kwargs)

        return decorated

    return verify
