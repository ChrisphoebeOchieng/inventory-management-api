from flask import Flask
from app.extensions import db, ma, migrate
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)

    # =========================
    # CONFIG
    # =========================
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    # =========================
    # INIT EXTENSIONS
    # =========================
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    # =========================
    # IMPORT MODELS (IMPORTANT)
    # =========================
    from app.authentication.models.user_model import User
    from app.products.models.product_model import Product
    from app.products.models.category_model import Category
    from app.orders.models.order_model import Order   # ✅ NEW

    # =========================
    # REGISTER ROUTES
    # =========================
    from app.authentication.routes.auth_routes import register_routes
    register_routes(app)

    from app.products.routes.product_routes import product_routes
    product_routes(app)

    # =========================
    # HOME
    # =========================
    @app.route("/")
    def home():
        return {"message": "API running"}

    return app