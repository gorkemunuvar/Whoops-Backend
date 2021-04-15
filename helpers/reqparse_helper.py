from flask_restful import reqparse

BLANK_ERROR = "'{}' cannot be blank"

signin_parser = reqparse.RequestParser()
signup_parser = reqparse.RequestParser()
whoop_parser = reqparse.RequestParser()

signin_parser.add_argument("username", required=True, help=BLANK_ERROR.format('username'))
signin_parser.add_argument("password",  required=True, help=BLANK_ERROR.format('password'))

signup_parser.add_argument("username", required=True, help=BLANK_ERROR.format('username'))
signup_parser.add_argument("password", required=True, help=BLANK_ERROR.format('password'))
signup_parser.add_argument("nick", required=True, help=BLANK_ERROR.format('nick'))
signup_parser.add_argument("name", required=True, help=BLANK_ERROR.format('name'))
signup_parser.add_argument("surname", required=True, help=BLANK_ERROR.format('surname'))
signup_parser.add_argument("email", required=True, help=BLANK_ERROR.format('email'))


whoop_parser.add_argument("nick", required=True, help=BLANK_ERROR.format('nick'))
whoop_parser.add_argument("latitude", required=True, help=BLANK_ERROR.format('latitude'))
whoop_parser.add_argument("longitude", required=True, help=BLANK_ERROR.format('longitude'))
whoop_parser.add_argument("note", required=True, help=BLANK_ERROR.format('note'))
whoop_parser.add_argument("time", required=True, help=BLANK_ERROR.format('time'))
