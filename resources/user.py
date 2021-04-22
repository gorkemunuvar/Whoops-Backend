import json
import datetime
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from models.user import UserModel
from models.revoken_token import RevokedTokenModel
from helpers.reqparse_helper import signin_parser, signup_parser


class UserSignup(Resource):
    @classmethod
    def post(cls):
        values = signup_parser.parse_args()

        if UserModel.find_by_email(values["email"]):
            return {"message": "A user with that email already exists."}, 400

        new_user = UserModel(
            email=values["email"],
            password=UserModel.generate_hash(values["password"]),
        )
        try:
            new_user.save_to_db()

            return {
                "message": "User {} was created".format(values["email"]),
            }, 201
        except:
            return {"message": "Something went wrong"}, 500


class UserSignin(Resource):
    @classmethod
    def post(cls):
        values = signin_parser.parse_args()
        current_user = UserModel.find_by_email(values["email"])

        if not current_user:
            return {"message": "User {} doesn't exist".format(values["email"])}, 404

        if UserModel.verify_hash(values["password"], current_user.password):
            access_token = create_access_token(
                identity=current_user.id,
                expires_delta=datetime.timedelta(minutes=60),
                fresh=True
            )
            refresh_token = create_refresh_token(identity=values["email"])

            return {
                "message": "Logged in as {}".format(current_user.email),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 201
        else:
            return {"message": "Wrong credentials"}, 401


class AllUsers(Resource):
    @classmethod
    def get(cls):
        return UserModel.return_all()

    @classmethod
    def delete(cls):
        return UserModel.delete_all()


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {"message": "User logged out and access token has been revoked."}
        except:
            return {"message": "Something went wrong"}, 500
