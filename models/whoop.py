from db import db
from typing import Dict, List, Union

# keys are string
# values are union
WhoopJSON = Dict[str, Union[int, str, int, float, float, int]]

class WhoopModel(db.Model):
    __tablename__ = "note"

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text)
    time = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, note: str, time: int, latitude: float, longitude: float, user_id: int):
        self.note = note
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.user_id = user_id

    def json(self) -> WhoopJSON:
        return {
            "id": self.id,
            "note": self.note,
            "time": self.time,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "user_id": self.user_id,
        }
