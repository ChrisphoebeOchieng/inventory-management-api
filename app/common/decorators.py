from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.authentication.models.user_model import User


def require_role(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            user_id = get_jwt_identity()

            user = User.query.get(int(user_id))

            if not user or user.role != role:
                return jsonify({"error": "Forbidden"}), 403

            return fn(*args, **kwargs)

        return decorated
    return wrapper