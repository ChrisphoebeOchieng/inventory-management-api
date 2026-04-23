from flask import Flask
from app.extensions import db, ma, migrate
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)

    # =========================
    # CONFIGURATION
    # =========================
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 🔐 JWT Config
    app.config["JWT_SECRET_KEY"] = "super-secret-key-that-is-long-enough-123456"

    # =========================
    # INITIALIZE EXTENSIONS
    # =========================
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    # =========================
    # IMPORT MODELS (VERY IMPORTANT)
    # =========================
    from app.authentication.models.user_model import User
    from app.products.models.product_model import Product
    from app.products.models.category_model import Category

    # =========================
    # REGISTER ROUTES
    # =========================
    from app.authentication.routes.auth_routes import register_routes
    register_routes(app)

    from app.products.routes.product_routes import product_routes
    product_routes(app)

    # =========================
    # TEST ROUTE
    # =========================
    @app.route("/")
    def home():
        return {"message": "Inventory Management API is running!"}

    return app