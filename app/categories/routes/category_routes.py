from flask import request, jsonify
from app.extensions import db
from app.categories.models.category_model import Category


def category_routes(app):

    # CREATE CATEGORY
    @app.route("/categories", methods=["POST"])
    def create_category():
        data = request.get_json()

        if not data or not data.get("name"):
            return jsonify({"error": "Name required"}), 400

        category = Category(name=data.get("name"))

        db.session.add(category)
        db.session.commit()

        return jsonify({
            "id": category.id,
            "name": category.name
        }), 201


    # GET ALL CATEGORIES
    @app.route("/categories", methods=["GET"])
    def get_categories():
        categories = Category.query.all()

        return jsonify([
            {"id": c.id, "name": c.name} for c in categories
        ]), 200


    # UPDATE CATEGORY
    @app.route("/categories/<int:id>", methods=["PUT"])
    def update_category(id):
        data = request.get_json()

        category = Category.query.get(id)

        if not category:
            return jsonify({"error": "Category not found"}), 404

        if not data or not data.get("name"):
            return jsonify({"error": "Name required"}), 400

        category.name = data.get("name")

        db.session.commit()

        return jsonify({
            "id": category.id,
            "name": category.name
        }), 200


    # DELETE CATEGORY
    @app.route("/categories/<int:id>", methods=["DELETE"])
    def delete_category(id):
        category = Category.query.get(id)

        if not category:
            return jsonify({"error": "Category not found"}), 404

        db.session.delete(category)
        db.session.commit()

        return jsonify({"message": "Category deleted"}), 200