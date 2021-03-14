import json
from g_variables import user_list
from datetime import datetime, timedelta
from flask_restful import Resource, reqparse
from flask import make_response, render_template, current_app
from models import User, RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, get_jwt_identity, get_jwt)


user_parser = reqparse.RequestParser()
user_parser.add_argument(
    'username', help='This field cannot be blank', required=True)
user_parser.add_argument(
    'password', help='This field cannot be blank', required=True)
user_parser.add_argument(
    'nick', help='This field cannot be blank', required=True)
user_parser.add_argument(
    'name', help='This field cannot be blank', required=True)
user_parser.add_argument(
    'surname', help='This field cannot be blank', required=True)
user_parser.add_argument(
    'email', help='This field cannot be blank', required=True)


note_parser = reqparse.RequestParser()
note_parser.add_argument(
    'nick', help='This field cannot be blank', required=True)
note_parser.add_argument(
    'latitude', help='This field cannot be blank', required=True)
note_parser.add_argument(
    'longitude', help='This field cannot be blank', required=True)
note_parser.add_argument(
    'note', help='This field cannot be blank', required=True)
note_parser.add_argument(
    'time', help='This field cannot be blank', required=True)


def socketio_emit(name, message):
    # from app does not work
    from __main__ import socketio
    socketio.emit(name, message)


class Test(Resource):
    def get(self):
        
        user_dict = {'notes': user_list}
        emitting_json = json.dumps(user_dict)

        print("----------------test api----------------")
        print(emitting_json)
        print("-------------test api - end-------------")

        socketio_emit('user_event', emitting_json)

        return emitting_json

class ShareNote(Resource):
    #web browser tarafından post isteği yapabilmek için
    #pasif kalmalı. Çünkü token gerekiyor.
    #@jwt_required
    def post(self):
        #handle database
        values = note_parser.parse_args()

        add_second = int(values['time'])
        starting_time = datetime.now()
        # days, seconds, then other fields.
        ending_time = starting_time + timedelta(0, add_second)

        print(values)

        user_json = {
            'nick':  values['nick'],
            'latitude': values['latitude'],
            'longitude': values['longitude'],
            'note': values['note'],
            'time': values['time'],
            'starting_time': str(starting_time.strftime("%Y-%m-%d %H:%M:%S")),
            'ending_time': str(ending_time.strftime("%Y-%m-%d %H:%M:%S"))
        }

        user_list.append(user_json)
        emitting_json = json.dumps({'notes': user_list})

        print("----------------emitting json / resources.py----------------")
        print(emitting_json)
        print("----------------emitting json----------------")

        # I am using this line recently.
        # json = '{"notes": ' + str(user_list) + '}'

        socketio_emit('user_event', emitting_json)

        print('Post request has been successed.')
        return {'message': 'Post request has been successed.'}

    def get(self):
        return make_response(render_template('share_note.html'))

class HomePage(Resource):
    def get(self):
        return make_response(render_template('index.html'))

class UserRegistration(Resource):
    def post(self):
        data = user_parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = User(
            username=data['username'],
            password=User.generate_hash(data['password']),
            nick=data['nick'],
            name=data['name'],
            surname=data['surname'],
            email=data['email']
        )

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])

            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    @jwt_required
    def post(self):
        data = user_parser.parse_args()
        current_user = User.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])

            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


# revoke -> iptal etmek
# Kullanıcı logout olduğunda token'ların blocklist'e eklenmesi gerekir.
# Access token blacklist'e eklenir.
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

# Burada ise refresh token blacklist'e eklenir.
class UserLogoutRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        jti = get_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}

class AllUsers(Resource):
    def get(self):
        return User.return_all()

    def delete(self):
        return User.delete_all()
