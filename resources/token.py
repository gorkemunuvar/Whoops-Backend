from flask_restful import Resource, reqparse 
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jti, get_jwt

from models.user import User
from models.revoked_token import RevokedTokenModel

from mongoengine import DoesNotExist


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(self):
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(
            identity=current_user_id, fresh=False)

        return {"access_token": new_access_token}, 200

# This resource returns true if the user logged out before
# So mobile app can check if the user is logged out before


parser = reqparse.RequestParser()
parser.add_argument("access_token", required=True,
                    help='You need to fill access_token')


class TokenBlacklist(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()['jti']

        revoked_token = RevokedTokenModel(jti=jti)
        isTokenRevoked = revoked_token.is_jti_blacklisted(jti)

        if isTokenRevoked:
            return {"message": "Token is in blacklist"}, 200
        else:
            return {"message": "Token does not exist in blacklist"}, 404


# class TokenBlacklist(Resource):
#     @classmethod
#     @jwt_required()
#     def post(cls):
#         jti = get_jwt()['jti']

#         revoked_token = RevokedTokenModel(jti=jti)
#         isTokenRevoked = revoked_token.is_jti_blacklisted(jti)

#         if isTokenRevoked:
#             return {"message": "Token is in blacklist"}, 404
#         else:
#             user_jwt_id = get_jwt_identity()
#             user = User.objects(pk=user_jwt_id).first()
            
#             return user.to_json(), 200
            



