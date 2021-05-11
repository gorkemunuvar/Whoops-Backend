import json
import datetime
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,)

from models.user import UserModel
from models.revoken_token import RevokedTokenModel
from schemas.user import UserSchema

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

class UserSignup(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)
        
        if UserModel.find_by_email(user.email):
            return {"message": "A user with that email already exists."}, 400

        user.password = UserModel.generate_hash(user.password) 
        user.save_to_db()

        return {'messsage': 'Created successfully.'}, 201


class UserSignin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        # user_data is a UserModel object
        user_data = user_schema.load(user_json)
        current_user = UserModel.find_by_email(user_data.email)

        if not current_user:
            return {"message": "User {} doesn't exist".format(user_data.email)}, 404

        # Expire süresi False olmazsa client tarafında token expire olduğunda örneğin ShareWhoop
        # endpointine istek atıldığında auth. problemi oluyor. Böyle durumlarda tekrarda refresh
        # token yapılmalı.
        if UserModel.verify_hash(user_data.password, current_user.password):
            access_token = create_access_token(
                identity=current_user.id,
                expires_delta=False,
                fresh=True
            )
            refresh_token = create_refresh_token(identity=current_user.email)

            return {
                "message": "Logged in as {}".format(current_user.email),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 201
        else:
            return {"message": "Wrong credentials"}, 401

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found!'}, 404
        
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found!'}, 404
        
        user.delete()
        
        return {'message': 'User deleted.'}, 200

class AllUsers(Resource):
    @classmethod
    def get(cls):
        #return UserModel.return_all()
        return {'users': user_list_schema.dump(UserModel.find_all())}, 200


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        # jti is the identity for JWT
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {"message": "User logged out and access token has been revoked."}, 200
        except:
            return {"message": "Something went wrong"}, 500
