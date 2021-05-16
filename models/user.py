from db import db
from typing import List
from passlib.hash import pbkdf2_sha256 as sha256

from models.whoop import WhoopModel


class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    whoops = db.relationship(
        "WhoopModel", backref="user", cascade="all, delete, delete-orphan", lazy=True,
    )

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id: str) -> "UserModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls) -> List['UserModel']:
        return cls.query.all()

    @staticmethod
    def generate_hash(password: str) -> str:
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password: str, hash: str) -> bool:
        return sha256.verify(password, hash)
