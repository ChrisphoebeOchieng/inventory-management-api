from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.orders.models.order_model import Order


def order_routes(app):

    # CREATE ORDER
    @app.route("/orders", methods=["POST"])
    @jwt_required()
    def create_order():
        data = request.get_json()
        current_user = get_jwt_identity()

        if not data or not data.get("total_price"):
            return jsonify({"error": "Total price required"}), 400

        user_id = int(current_user)

        order = Order(
            total_price=data.get("total_price"),
            user_id=user_id
        )

        db.session.add(order)
        db.session.commit()

        return jsonify({
            "id": order.id,
            "total_price": order.total_price
        }), 201


    # GET ORDERS
    @app.route("/orders", methods=["GET"])
    @jwt_required()
    def get_orders():
        orders = Order.query.all()

        return jsonify([
            {
                "id": o.id,
                "total_price": o.total_price,
                "user_id": o.user_id
            } for o in orders
        ]), 200


    # UPDATE ORDER
    @app.route("/orders/<int:id>", methods=["PUT"])
    @jwt_required()
    def update_order(id):
        data = request.get_json()
        current_user = get_jwt_identity()

        order = Order.query.get(id)

        if not order:
            return jsonify({"error": "Order not found"}), 404

        user_id = int(current_user)

        if order.user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403

        if not data or not data.get("total_price"):
            return jsonify({"error": "Total price required"}), 400

        order.total_price = data.get("total_price")

        db.session.commit()

        return jsonify({
            "id": order.id,
            "total_price": order.total_price
        }), 200


    # DELETE ORDER
    @app.route("/orders/<int:id>", methods=["DELETE"])
    @jwt_required()
    def delete_order(id):
        order = Order.query.get(id)

        if not order:
            return jsonify({"error": "Order not found"}), 404

        db.session.delete(order)
        db.session.commit()

        return jsonify({"message": "Order deleted"}), 200