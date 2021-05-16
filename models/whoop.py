from db import db


class WhoopModel(db.Model):
    __tablename__ = "whoop"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    time = db.Column(db.Integer)
    starting_time = db.Column(db.Text)
    ending_time = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
