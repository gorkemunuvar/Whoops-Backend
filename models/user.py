from db import db
from typing import Dict, List, Union
from passlib.hash import pbkdf2_sha256 as sha256

# keys are string
# values are union
UserJSON = Dict[str, Union[int, str, str, str, str, str]]


class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # whoops = db.relationship(
    #     "Whoop", backref="user", cascade="all, delete, delete-orphan", lazy=True,
    # )

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def json(self) -> UserJSON:
        return {"email": self.email}

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id: str) -> "UserModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def return_all(cls) -> List["UserModel"]:
        def to_json(user):
            return {
                'email': user.email,
                'password': user.password,
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
