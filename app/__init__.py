from flask import Flask
from app.extensions import db, jwt, ma


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    from app.authentication.routes.auth_routes import register_routes
    from app.products.routes.product_routes import product_routes
    from app.orders.routes.order_routes import order_routes
    from app.categories.routes.category_routes import category_routes


    register_routes(app)
    product_routes(app)
    order_routes(app)
    category_routes(app)

    return app