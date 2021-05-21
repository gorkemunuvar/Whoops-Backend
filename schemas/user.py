from ma import ma
from models.user import UserModel
from schemas.whoop import WhoopSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        ordered = True
        load_only = ('password',)
        dump_only = ('id', )
        # marshmallow-sqlalchemy will return UserModel obj instead of dict.
        load_instance = True

    whoops = ma.Nested(WhoopSchema(), many=True)

