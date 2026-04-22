from flask import request, jsonify
from app.extensions import db
from app.authentication.models.user_model import User
from app.authentication.schemas import user_schema
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError


def register_routes(app):

    # =========================
    # ✅ REGISTER USER
    # =========================
    @app.route("/register", methods=["POST"])
    def register():
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        try:
            # ✅ Validate input using schema
            user_data = user_schema.load(data)
        except ValidationError as err:
            return jsonify(err.messages), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=user_data["email"]).first()
        if existing_user:
            return jsonify({"error": "User already exists"}), 400

        # Create new user
        new_user = User(
            username=user_data["username"],
            email=user_data["email"]
        )
        new_user.set_password(user_data["password"])

        db.session.add(new_user)
        db.session.commit()

        return user_schema.jsonify(new_user), 201


    # =========================
    # ✅ LOGIN USER
    # =========================
    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401

        # 🔐 CREATE JWT TOKEN (with RBAC role)
        access_token = create_access_token(
            identity={
                "id": user.id,
                "role": user.role
            }
        )

        # ✅ RETURN USER + TOKEN
        return jsonify({
            "user": user_schema.dump(user),
            "access_token": access_token
        }), 200