from ma import ma
from models.whoop import WhoopModel


class WhoopSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WhoopModel
        # model to dict
        dump_only = ('starting_time', 'ending_time',)
        # marshmallow-sqlalchemy will return UserModel obj instead of dict.
        load_instance = True
