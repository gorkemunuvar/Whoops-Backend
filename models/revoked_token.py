from passlib.hash import pbkdf2_sha256 as sha256
from mongoengine import Document, StringField


class RevokedTokenModel(Document):
    jti = StringField(max_length=150)

    @classmethod
    def is_jti_blacklisted(cls, jti) -> bool:
        query = cls.objects(jti=jti).first()
        return bool(query)
