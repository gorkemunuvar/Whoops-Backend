from passlib.hash import pbkdf2_sha256 as sha256
from mongoengine import Document, StringField


class User(Document):
    email = StringField(required=True, max_length=100)
    password = StringField(max_length=200)

    @staticmethod
    def generate_hash(password: str) -> str:
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password: str, hash: str) -> bool:
        return sha256.verify(password, hash)
