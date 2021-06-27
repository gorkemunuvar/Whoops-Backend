from passlib.hash import pbkdf2_sha256 as sha256
from mongoengine import Document, DynamicDocument, StringField, FloatField, IntField, ReferenceField, connect, CASCADE


connect(
    host='mongodb+srv://whoops-database:whoops-database@whoops-cluster.sslk6.mongodb.net/whoops-database?retryWrites=true&w=majority',
)


class User(Document):
    email = StringField(required=True, max_length=100)
    password = StringField(max_length=200)

    @staticmethod
    def generate_hash(password: str) -> str:
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password: str, hash: str) -> bool:
        return sha256.verify(password, hash)


class Whoop(DynamicDocument):
    title = StringField(required=True)
    latitude = FloatField(required=True)
    longitude = FloatField(required=True)
    time = IntField(required=True)
    starting_time = StringField(required=True)
    ending_time = StringField(required=True)

    user = ReferenceField(User, reverse_delete_rule=CASCADE)

    meta = {'allow_inheritance': True}

    def to_json(self) -> dict:
        whoop_json = {
            'title': self.title,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'time': self.time,
            'starting_time': self.starting_time,
            'ending_time': self.ending_time,
        }

        return whoop_json


class RevokedTokenModel(Document):
    jti = StringField(max_length=150)

    @classmethod
    def is_jti_blacklisted(cls, jti) -> bool:
        query = cls.objects(jti=jti).first()
        return bool(query)
