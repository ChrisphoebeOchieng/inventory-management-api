from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def require_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            #  Ensure token is present
            verify_jwt_in_request()

            # Get user from token
            user = get_jwt_identity()

            if not user:
                return jsonify({"error": "Invalid token"}), 401

            # Check role
            if user.get("role") != role:
                return jsonify({"error": "Access denied"}), 403

            return func(*args, **kwargs)

        return wrapper
    return decorator