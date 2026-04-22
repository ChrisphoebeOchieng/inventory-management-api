from flask import request, jsonify
from app.extensions import db
from app.authentication.models.user_model import User
from flask_jwt_extended import create_access_token


def register_routes(app):

    # REGISTER
    @app.route("/register", methods=["POST"])
    def register():
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "User already exists"}), 400

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201


    # LOGIN
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

        # CREATE JWT TOKEN
        access_token = create_access_token(identity=user.id)

        return jsonify({
            "message": "Login successful",
            "access_token": access_token
        }), 200