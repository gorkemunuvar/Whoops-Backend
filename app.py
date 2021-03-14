import json
from flask import Flask
from task import scheduleTask
from datetime import datetime
from flask_restful import Api
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'

db = SQLAlchemy(app)

scheduler = APScheduler()
socketio = SocketIO(app, logger=True)


def handle_migration():
    # Unless models.py is not imported migration process
    # doesn't detect tables correctly.
    import models
    migrate = Migrate(app, db)


handle_migration()

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


#it is called every time when the clients try to access secured endpoints
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    import models
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


@socketio.on('connect')
def connect():
    from g_variables import user_list

    print('A user connected.')
    user_dict = {'notes': user_list}
    emitting_json = json.dumps(user_dict)
    socketio.emit('user_event', emitting_json)


def set_apis():
    import models
    import resources

    api.add_resource(resources.HomePage, '/')
    api.add_resource(resources.Test, '/test')
    api.add_resource(resources.UserRegistration, '/registration')
    api.add_resource(resources.UserLogin, '/login')
    api.add_resource(resources.ShareNote, '/sharenote')
    api.add_resource(resources.AllUsers, '/users')
    api.add_resource(resources.UserLogoutAccess, '/logout/access')
    api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
    api.add_resource(resources.TokenRefresh, '/token/refresh')


if __name__ == '__main__':
    set_apis()

    scheduler.add_job(id='Scheduled Task', func=scheduleTask,
                      trigger="interval", seconds=1)
    scheduler.start()
    socketio.run(app, debug=True, use_reloader=False)
