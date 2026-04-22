from app.extensions import ma
from app.authentication.models.user_model import User
from marshmallow import fields


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password_hash",)

    # ✅ Add validation rules
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)