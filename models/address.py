from mongoengine import StringField, EmbeddedDocument


class Address(EmbeddedDocument):
    amenity = StringField()
    road = StringField()
    neighbourhood = StringField()
    village = StringField()
    town = StringField()
    county = StringField()
    province = StringField()
    region = StringField()
    postcode = StringField()
    country = StringField()
    country_code = StringField()

    def to_json(self):
        address_json = {
            'amenity': self.amenity,
            'road': self.road,
            'neighbourhood': self.neighbourhood,
            'village': self.village,
            'town': self.town,
            'county': self.county,
            'province': self.province,
            'region': self.region,
            'postcode': self.postcode,
            'country': self.country,
            'country_code': self.country_code,
        }

        return address_json
