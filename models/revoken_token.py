from db import db
import typing


class RevokedTokenModel(db.Model):
    __tablename__ = "revoked_tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti) -> bool:
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
