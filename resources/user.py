from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

from models.user import User
from models.revoked_token import RevokedTokenModel

from mongoengine import DoesNotExist


class UserSignUp(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        #user = user_schema.load(user_json)

        # Mongo Engine
        if User.objects(email=user_json['email']):
            return {"message": "A user with that email already exists."}, 400

        user = User()
        user.email = user_json['email']
        user.username = user_json['username']
        user.password = User.generate_hash(user_json['password'])

        user.save()

        return {'messsage': 'User created successfully.'}, 201


class UserSignin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        # user_data is a UserModel object
        #user_data = user_schema.load(user_json)

        try:
            # after the query current_user is the mongoengine User model
            current_user = User.objects.get(email=user_json['email'])
        except DoesNotExist:
            return {"message": "User {} doesn't exist".format(user_json['email'])}, 404

        # Expire süresi False olmazsa client tarafında token expire olduğunda örneğin ShareWhoop
        # endpointine istek atıldığında auth. problemi oluyor. Böyle durumlarda tekrarda refresh
        # token yapılmalı.

        user_id = str(current_user.pk)

        # add 'and user.password'
        if User.verify_hash(user_json['password'], current_user.password):
            access_token = create_access_token(
                identity=user_id,
                expires_delta=False,
                fresh=True
            )
            refresh_token = create_refresh_token(identity=user_id)

            return {
                "message": "Logged in as {}".format(current_user.email),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 201
        else:
            return {"message": "Wrong credentials"}, 401


class UserResource(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        user_jwt_id = get_jwt_identity()

        try:
            user = User.objects.get(pk=user_jwt_id)
        except DoesNotExist:
            return {'message': 'User not found!'}, 404

        # This function also has to return all the whoops belongs to the related user.
        return user.to_json(), 200

    @classmethod
    @jwt_required()
    def delete(cls):
        user_jwt_id = get_jwt_identity()

        try:
            user = User.objects.get(pk=user_jwt_id)
        except DoesNotExist:
            return {'message': 'User not found!'}, 404

        user.delete()

        return {'message': 'User deleted.'}, 200

    @classmethod
    @jwt_required()
    def put(cls):
        user_json = request.get_json()

        user_jwt_id = get_jwt_identity()

        try:
            user = User.objects.get(pk=user_jwt_id)
        except DoesNotExist:
            return {'message': 'User not found!'}, 404

        User.objects(pk=user_jwt_id).update(**user_json)

        return {'message': 'User information updated successfully.'}, 200


class AllUsers(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        # return UserModel.return_all()
        # return {'users': users_schema.dump(UserModel.find_all())}, 200

        user_json = []

        # Use  user.to_json and mapping to return all the user list instead.
        for user in User.objects:
            user_dict = {
                'email': user.email,
                'username': user.username,
                'password': user.password
            }

            user_json.append(user_dict)

        return {'users': user_json}, 200


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        # jti is an identity for JWT
        jti = get_jwt()['jti']

        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.save()

            return {"message": "User logged out and access token has been revoked."}, 200
        except:
            return {"message": "Something went wrong"}, 500


class SetPassword(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def post(cls):
        # user_json = email and new password
        user_json = request.get_json()

        user_id = get_jwt_identity()

        try:
            user = User.objects.get(pk=user_id)
        except DoesNotExist:
            return {'message': 'User not found!'}, 404

        password_hash = User.generate_hash(user_json['password'])
        user.update(set__password=password_hash)

        return {'message': 'User password has been changed successfully.'}, 200
