from app.extensions import ma
from app.authentication.models.user_model import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password_hash",)  # 🔥 never expose password


# Single user
user_schema = UserSchema()

# Multiple users (optional)
users_schema = UserSchema(many=True)