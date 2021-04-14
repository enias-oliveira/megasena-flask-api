from . import ma
from src.models.user_model import UserModel


class UserModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel()
        exclude = ("password_hash",)

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()


user_model_schema = UserModelSchema()
