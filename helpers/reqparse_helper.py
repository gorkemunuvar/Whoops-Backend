from flask_restful import reqparse

signin_parser = reqparse.RequestParser()
signup_parser = reqparse.RequestParser()
whoop_parser = reqparse.RequestParser()

signin_parser.add_argument(
    'username', help='This field cannot be blank', required=True)
signin_parser.add_argument(
    'password', help='This field cannot be blank', required=True)

signup_parser.add_argument(
    'username', help='This field cannot be blank', required=True)
signup_parser.add_argument(
    'password', help='This field cannot be blank', required=True)
signup_parser.add_argument(
    'nick', help='This field cannot be blank', required=True)
signup_parser.add_argument(
    'name', help='This field cannot be blank', required=True)
signup_parser.add_argument(
    'surname', help='This field cannot be blank', required=True)
signup_parser.add_argument(
    'email', help='This field cannot be blank', required=True)

    
whoop_parser.add_argument(
    'nick', help='This field cannot be blank', required=True)
whoop_parser.add_argument(
    'latitude', help='This field cannot be blank', required=True)
whoop_parser.add_argument(
    'longitude', help='This field cannot be blank', required=True)
whoop_parser.add_argument(
    'note', help='This field cannot be blank', required=True)
whoop_parser.add_argument(
    'time', help='This field cannot be blank', required=True)