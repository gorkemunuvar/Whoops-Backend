import json
from db import db
from flask import Flask
from datetime import datetime
from flask_socketio import SocketIO

from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from flask_jwt_extended import JWTManager

from helpers.task import scheduleTask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


socketio = SocketIO(app, logger=True)
jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()


# it is called every time when clients try to access secured endpoints
@jwt.token_in_blocklist_loader
# i added 'self' to solve an error
def check_if_token_in_blacklist(self, decrypted_token):
    from models.revoken_token import RevokedTokenModel
    jti = decrypted_token['jti']

    return RevokedTokenModel.is_jti_blacklisted(jti)


@socketio.on('connect')
def connect():
    from g_variables import user_list

    print('A user connected.')
    user_dict = {'notes': user_list}
    emitting_json = json.dumps(user_dict)
    socketio.emit('user_event', emitting_json)


def set_api():
    from resources.test import Test
    from resources.token import TokenRefresh
    from resources.whoop import ShareWhoop
    from resources.user import (UserSignin,
                                UserSignup,
                                UserLogoutAccess,
                                UserLogoutRefresh,
                                AllUsers)

    api = Api(app)

    api.add_resource(UserSignin, '/signin')
    api.add_resource(UserSignup, '/signup')
    api.add_resource(UserLogoutAccess, '/logout/access')
    api.add_resource(UserLogoutRefresh, '/logout/refresh')
    api.add_resource(AllUsers, '/users')
    api.add_resource(Test, '/test')
    api.add_resource(ShareWhoop, '/sharewhoop')
    api.add_resource(TokenRefresh, '/token/refresh')


if __name__ == '__main__':
    db.init_app(app)
    set_api()
    scheduler = APScheduler()

    scheduler.add_job(id='Scheduled Task', func=scheduleTask,
                      trigger="interval", seconds=1)
    scheduler.start()
    socketio.run(app, debug=True, use_reloader=False)
