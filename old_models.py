from db import db

class Note(db.Model):
    __tablename__ = "note"

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text)
    time = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, note, time, latitude, longitude, user_id):
        self.note = note
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.user_id = user_id

    def __repr__(self):
        return (
            f"<Note id: %s note: %s time: %s latitude: %s longitude: %s city: %s user_id: %s>"
            % self.id
            % self.note
            % self.time
            % self.latitude
            % self.longitude
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
