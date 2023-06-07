import os
from functools import wraps

import requests
from flask import g, jsonify, make_response, request

from config import config_by_name

config = config_by_name[os.environ.get("FLASK_ENV", "dev")]


def verify_token():
    """
    To verify bearer token in request and to validate it from user management portal.
    :return:
    """

    def verify(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return make_response(jsonify({"msg": "Missing Authorization Header"}), 401)
            identity = requests.get(
                config["USER_MANAGEMENT_PORTAL_URL"] + "/auth/verify", headers={"Authorization": token}
            )
            if not identity.status_code == 200:
                return make_response(jsonify(identity.json()), identity.status_code)
            else:
                g.user = identity.json()
            return f(*args, **kwargs)

        return decorated

    return verify
