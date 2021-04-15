from db import db
from typing import Dict, List, Union
from passlib.hash import pbkdf2_sha256 as sha256

# keys are string
# values are union
UserJSON = Dict[str, Union[int, str, str, str, str, str]]


class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    nick = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    # whoops = db.relationship(
    #     "Whoop", backref="user", cascade="all, delete, delete-orphan", lazy=True,
    # )

    def __init__(self, username: str, password: str, nick: str, name: str, surname: str, email: str):
        self.username = username
        self.password = password
        self.nick = nick
        self.name = name
        self.surname = surname
        self.email = email

    def json(self, name: str) -> UserJSON:
        return {
            "id": self.id,
            "nick": self.nick,
            "name": self.name,
            "surname": self.surname,
            "username": self.username,
            "email": self.email,
        }

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def return_all(cls) -> List["UserModel"]:
        def to_json(user):
            return {
                'username': user.username,
                'password': user.password,
                'nick': user.nick,
                'name': user.name,
                'surname': user.surname,
                'email': user.email,
            }

        return {'users': list(map(lambda user: to_json(user), UserModel.query.all()))}

    @classmethod
    def delete_all(cls) -> Dict[str, str]:
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()

            return {"message": "{} row(s) deleted".format(num_rows_deleted)}
        except:
            return {"message": "Something went wrong"}

    @staticmethod
    def generate_hash(password: str) -> str:
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password: str, hash: str) -> bool:
        return sha256.verify(password, hash)
