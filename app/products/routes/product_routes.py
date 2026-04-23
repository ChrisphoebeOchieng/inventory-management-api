from flask import request, jsonify
from app.extensions import db
from app.products.models.product_model import Product
from app.products.schemas import product_schema, products_schema
from app.common.decorators import require_role
from flask_jwt_extended import jwt_required, get_jwt_identity


def product_routes(app):

    # =========================
    # ✅ CREATE PRODUCT (Admin only)
    # =========================
    @app.route("/products", methods=["POST"])
    @jwt_required()
    @require_role("admin")
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

        # ✅ FIX: get user id correctly from JWT
        current_user_id = int(get_jwt_identity())

        new_product = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            user_id=current_user_id
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({
            "message": "Product created successfully",
            "product": product_schema.dump(new_product)
        }), 201


    # =========================
    # ✅ GET ALL PRODUCTS (Public)
    # =========================
    @app.route("/products", methods=["GET"])
    def get_products():
        products = Product.query.all()
        return products_schema.jsonify(products), 200


    # =========================
    # ✅ GET SINGLE PRODUCT
    # =========================
    @app.route("/products/<int:product_id>", methods=["GET"])
    def get_product(product_id):
        product = Product.query.get(product_id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        return product_schema.jsonify(product), 200


    # =========================
    # ✅ UPDATE PRODUCT (Admin only)
    # =========================
    @app.route("/products/<int:product_id>", methods=["PUT"])
    @jwt_required()
    @require_role("admin")
    def update_product(product_id):
        product = Product.query.get(product_id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        product.name = data.get("name", product.name)
        product.description = data.get("description", product.description)
        product.price = data.get("price", product.price)
        product.quantity = data.get("quantity", product.quantity)

        db.session.commit()

        return jsonify({
            "message": "Product updated successfully",
            "product": product_schema.dump(product)
        }), 200


    # =========================
    # ✅ DELETE PRODUCT (Admin only)
    # =========================
    @app.route("/products/<int:product_id>", methods=["DELETE"])
    @jwt_required()
    @require_role("admin")
    def delete_product(product_id):
        product = Product.query.get(product_id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        db.session.delete(product)
        db.session.commit()

        return jsonify({"message": "Product deleted successfully"}), 200