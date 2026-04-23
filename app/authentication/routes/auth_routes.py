from flask import request, jsonify
from app.extensions import db
from app.authentication.models.user_model import User
from flask_jwt_extended import create_access_token


def register_routes(app):

    @app.route("/register", methods=["POST"])
    def register():
        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "user")

        if not username or not email or not password:
            return jsonify({"error": "All fields required"}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "User exists"}), 400

        user = User(username=username, email=email, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User created"}), 201


    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()

        user = User.query.filter_by(email=data.get("email")).first()

        if not user or not user.check_password(data.get("password")):
            return jsonify({"error": "Invalid credentials"}), 401

        token = create_access_token(identity=str(user.id))

        return jsonify({"access_token": token}), 200