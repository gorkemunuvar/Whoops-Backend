from passlib.hash import pbkdf2_sha256 as sha256
from mongoengine import Document, StringField


class User(Document):
    email = StringField(required=True, max_length=100)
    username = StringField(required=True, max_length=15)
    password = StringField(max_length=200)
    about_me = StringField(max_length=100)
    first_name = StringField(max_length=30)
    last_name = StringField(max_length=20)
    phone_number = StringField(max_length=15)
    twitter_username = StringField(max_length=20)
    instagram_username = StringField(max_length=20)
    facebook_username = StringField(max_length=20)

    @staticmethod
    def generate_hash(password: str) -> str:
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password: str, hash: str) -> bool:
        return sha256.verify(password, hash)

    def to_json(self):
        return {
            "id": str(self.pk),
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "about_me": self.about_me,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "twitter_username": self.twitter_username,
            "instagram_username": self.instagram_username,
            "facebook_username": self.facebook_username
        }
