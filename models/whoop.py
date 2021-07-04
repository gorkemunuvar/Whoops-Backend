from models.user import User
from models.address import Address
from mongoengine import (DynamicDocument, StringField, EmbeddedDocumentField,
                         FloatField, IntField, ReferenceField, ListField, BooleanField, CASCADE)


class Whoop(DynamicDocument):
    title = StringField(required=True)
    latitude = FloatField(required=True)
    longitude = FloatField(required=True)
    time = IntField(required=True)
    is_active = BooleanField(required=True)
    date_created = StringField()
    starting_time = StringField(required=True)
    ending_time = StringField(required=True)
    tags = ListField()
    address = EmbeddedDocumentField(Address)

    user = ReferenceField(User, reverse_delete_rule=CASCADE)

    meta = {'allow_inheritance': True}

    def to_json(self) -> dict:
        whoop_json = {
            'title': self.title,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'time': self.time,
            'is_active': self.is_active,
            'date_created': self.date_created,
            'starting_time': self.starting_time,
            'ending_time': self.ending_time,
            'tags': self.tags,
            'address': self.address.to_json()
        }

        return whoop_json
