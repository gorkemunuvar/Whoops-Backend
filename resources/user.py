from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from models.user import UserModel
from helpers.reqparse_helper import signin_parser, signup_parser


class UserSignin(Resource):
    @classmethod
    def post(cls):
        values = signin_parser.parse_args()
        current_user = UserModel.find_by_username(values["username"])

        if not current_user:
            return {"message": "User {} doesn't exist".format(values["username"])}

        if UserModel.verify_hash(values["password"], current_user.password):
            access_token = create_access_token(
                identity=values["username"], expires_delta=False
            )
            refresh_token = create_refresh_token(identity=values["username"])

            return {
                "message": "Logged in as {}".format(current_user.username),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        else:
            return {"message": "Wrong credentials"}


class UserSignup(Resource):
    @classmethod
    def post(cls):
        values = signup_parser.parse_args()

        if UserModel.find_by_username(values["username"]):
            return {"message": "User {} already exists".format(values["username"])}

        new_user = UserModel(
            username=values["username"],
            password=UserModel.generate_hash(values["password"]),
            nick=values["nick"],
            name=values["name"],
            surname=values["surname"],
            email=values["email"],
        )

        try:
            new_user.save_to_db()

            access_token = create_access_token(
                identity=values["username"], expires_delta=False
            )
            refresh_token = create_refresh_token(identity=values["username"])

            return {
                "message": "User {} was created".format(values["username"]),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        except:
            return {"message": "Something went wrong"}, 500


class AllUsers(Resource):
    @classmethod
    def get(cls):
        return UserModel.return_all()

    @classmethod
    def delete(cls):
        return UserModel.delete_all()


# revoke -> iptal etmek
# Kullanıcı logout olduğunda token'ların blocklist'e eklenmesi gerekir.
# Access token blocklist'e eklenir.
class UserLogoutAccess(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()["jti"]
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {"message": "Access token has been revoked"}
        except:
            return {"message": "Something went wrong"}, 500


# Burada ise refresh token blacklist'e eklenir.
class UserLogoutRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        jti = get_jwt()["jti"]
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {"message": "Refresh token has been revoked"}
        except:
            return {"message": "Something went wrong"}, 500
