from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)

    # 🔗 RELATIONSHIP (NEW)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)