from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.products.models.product_model import Product


def product_routes(app):

    # CREATE PRODUCT
    @app.route("/products", methods=["POST"])
    @jwt_required()
    def create_product():
        data = request.get_json()
        current_user = get_jwt_identity()

        if not data or not data.get("name") or not data.get("price"):
            return jsonify({"error": "Name and price required"}), 400

        user_id = int(current_user)

        product = Product(
            name=data.get("name"),
            description=data.get("description"),
            price=data.get("price"),
            quantity=data.get("quantity", 0),
            category_id=data.get("category_id"),
            user_id=user_id
        )

        db.session.add(product)
        db.session.commit()

        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price
        }), 201


    # GET PRODUCTS
    @app.route("/products", methods=["GET"])
    @jwt_required()
    def get_products():
        products = Product.query.all()

        return jsonify([
            {
                "id": p.id,
                "name": p.name,
                "price": p.price
            } for p in products
        ]), 200


    # UPDATE PRODUCT
    @app.route("/products/<int:id>", methods=["PUT"])
    @jwt_required()
    def update_product(id):
        data = request.get_json()
        current_user = get_jwt_identity()

        product = Product.query.get(id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        user_id = int(current_user)

        if product.user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403

        if data.get("name"):
            product.name = data.get("name")

        if data.get("description"):
            product.description = data.get("description")

        if data.get("price"):
            product.price = data.get("price")

        if data.get("quantity") is not None:
            product.quantity = data.get("quantity")

        if data.get("category_id"):
            product.category_id = data.get("category_id")

        db.session.commit()

        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price
        }), 200


    # DELETE PRODUCT
    @app.route("/products/<int:id>", methods=["DELETE"])
    @jwt_required()
    def delete_product(id):
        product = Product.query.get(id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        db.session.delete(product)
        db.session.commit()

        return jsonify({"message": "Product deleted"}), 200