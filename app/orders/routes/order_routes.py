from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.orders.models.order_model import Order


def order_routes(app):

    # =========================
    # CREATE ORDER
    # =========================
    @app.route("/orders", methods=["POST"])
    @jwt_required()
    def create_order():
        data = request.get_json()

        if not data or not data.get("total_price"):
            return jsonify({"error": "Total price is required"}), 400

        # JWT gives user_id as string → convert
        user_id = int(get_jwt_identity())

        order = Order(
            total_price=data["total_price"],
            user_id=user_id
        )

        db.session.add(order)
        db.session.commit()

        return jsonify({
            "id": order.id,
            "total_price": order.total_price,
            "user_id": order.user_id
        }), 201

    # =========================
    # GET ORDERS
    # =========================
    @app.route("/orders", methods=["GET"])
    @jwt_required()
    def get_orders():
        orders = Order.query.all()

        result = []
        for order in orders:
            result.append({
                "id": order.id,
                "total_price": order.total_price,
                "user_id": order.user_id
            })

        return jsonify(result), 200