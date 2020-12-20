from app import db
from passlib.hash import pbkdf2_sha256 as sha256


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    nick = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    surname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    notes = db.relationship(
        "Note", backref="user", cascade="all, delete, delete-orphan", lazy=True
    )

    def __init__(self, username, password, nick, name, surname, email):
        self.username = username
        self.password = password
        self.nick = nick
        self.name = name
        self.surname = surname
        self.email = email

    def __repr__(self):
        return (
            f"<User id: %s nick: %s name: %s surname: %s username:: %s email: %s>"
            % self.id
            % self.nick
            % self.name
            % self.surname
            % self.username
            % self.email
        )

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password,
                'nick': x.nick,
                'name': x.name,
                'surname': x.surname,
                'email': x.email,
            }
        return {'users': list(map(lambda x: to_json(x), User.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class Note(db.Model):
    __tablename__ = "note"

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text)
    time = db.Column(db.Text)
    location = db.Column(db.Text)
    street = db.Column(db.Text)
    city = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, note, time, location, street, city, user_id):
        self.note = note
        self.time = time
        self.location = location
        self.street = street
        self.city = city
        self.user_id = user_id

    def __repr__(self):
        return (
            f"<Note id: %s note: %s time: %s location: %s street: %s city: %s user_id: %s>"
            % self.id
            % self.note
            % self.time
            % self.location
            % self.street
            % self.city
            % self.user_id
        )


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
