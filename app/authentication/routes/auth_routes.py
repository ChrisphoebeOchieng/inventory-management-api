from flask import request, jsonify
from app.extensions import db
from app.authentication.models.user_model import User
from app.authentication.schemas import user_schema
from flask_jwt_extended import create_access_token


def register_routes(app):

    # =========================
    # ✅ REGISTER
    # =========================
    @app.route("/register", methods=["POST"])
    def register():
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        # 🔥 FIX: schema returns object, not dict
        user_data = user_schema.load(data)

        # ✅ FIX HERE (use dot notation)
        existing_user = User.query.filter_by(email=user_data.email).first()

        if existing_user:
            return jsonify({"error": "User already exists"}), 400

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            role="user"
        )

        # password still comes from raw data
        new_user.set_password(data.get("password"))

        db.session.add(new_user)
        db.session.commit()

        return jsonify(user_schema.dump(new_user)), 201


    # =========================
    # ✅ LOGIN
    # =========================
    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401

        # ✅ JWT identity = string
        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            "user": user_schema.dump(user),
            "access_token": access_token
        }), 200