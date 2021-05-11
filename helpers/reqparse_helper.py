from flask_restful import reqparse

BLANK_ERROR = "'{}' cannot be blank"

whoop_parser = reqparse.RequestParser()

whoop_parser.add_argument("whoop_title", required=True, help=BLANK_ERROR.format('note'))
whoop_parser.add_argument("latitude", required=True, help=BLANK_ERROR.format('latitude'))
whoop_parser.add_argument("longitude", required=True, help=BLANK_ERROR.format('longitude'))
whoop_parser.add_argument("time", required=True, help=BLANK_ERROR.format('time'))
