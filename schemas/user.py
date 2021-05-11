from ma import ma
from models.user import UserModel

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ('password',)
        dump_only = ('id', )
        # marshmallow-sqlalchemy will return UserModel obj instead of dict.
        load_instance=True