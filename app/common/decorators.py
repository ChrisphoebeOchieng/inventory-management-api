from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.authentication.models.user_model import User


def require_role(role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):

            # ✅ get user id from token
            user_id = int(get_jwt_identity())

            # ✅ fetch user from DB
            user = User.query.get(user_id)

            if not user:
                return jsonify({"error": "User not found"}), 404

            # ✅ check role from DB
            if user.role != role:
                return jsonify({"error": "Access forbidden"}), 403

            return fn(*args, **kwargs)

        return wrapper
    return decorator