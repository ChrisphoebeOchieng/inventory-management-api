from flask import request, jsonify
from app.extensions import db
from app.products.models.product_model import Product
from flask_jwt_extended import jwt_required
from app.common.decorators import require_role


def product_routes(app):

    # CREATE PRODUCT (Admin only)
    @jwt_required()
    @require_role("admin")
    @app.route("/products", methods=["POST"])
    def create_product():
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        name = data.get("name")
        description = data.get("description")
        price = data.get("price")
        quantity = data.get("quantity", 0)

        if not name or price is None:
            return jsonify({"error": "Name and price are required"}), 400

        new_product = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({"message": "Product created"}), 201


    # GET ALL PRODUCTS
    @jwt_required()
    @app.route("/products", methods=["GET"])
    def get_products():
        products = Product.query.all()

        result = []
        for p in products:
            result.append({
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": p.price,
                "quantity": p.quantity
            })

        return jsonify(result), 200


    # UPDATE PRODUCT (Admin only)
    @jwt_required()
    @require_role("admin")
    @app.route("/products/<int:id>", methods=["PUT"])
    def update_product(id):
        product = Product.query.get(id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        data = request.get_json()

        product.name = data.get("name", product.name)
        product.description = data.get("description", product.description)
        product.price = data.get("price", product.price)
        product.quantity = data.get("quantity", product.quantity)

        db.session.commit()

        return jsonify({"message": "Product updated"}), 200


    # DELETE PRODUCT (Admin only)
    @jwt_required()
    @require_role("admin")
    @app.route("/products/<int:id>", methods=["DELETE"])
    def delete_product(id):
        product = Product.query.get(id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        db.session.delete(product)
        db.session.commit()

        return jsonify({"message": "Product deleted"}), 200