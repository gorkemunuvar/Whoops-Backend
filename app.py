#import eventlet

import json
from oa import oauth
from datetime import datetime

from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from flask_jwt_extended import JWTManager
#from flask_uploads import patch_request_class, configure_uploads

from mongoengine import connect as handle_connection

from dotenv import load_dotenv

from helpers.task import scheduleTask
#from helpers.image_helper import IMAGE_SET
#from models.revoken_token import RevokedTokenModel
from models.revoked_token import RevokedTokenModel

load_dotenv(".env", verbose=True)


app = Flask(__name__)

# load default configs from default_config.py
app.config.from_object("default_config")

app.config["MONGODB_DB"] = 'whoops-database'

app.config.from_envvar(
    "APPLICATION_SETTINGS"
)  # override with config.py (APPLICATION_SETTINGS points to config.py)

# 10 MB max image size upload
#patch_request_class(app, 10 * 1024 * 1024)
#configure_uploads(app, IMAGE_SET)

socketio = SocketIO(app, logger=True)
jwt = JWTManager(app)
api = Api(app)

# This methods called every time when clients try to access secured endpoints
# It will check if a token is blacklisted.


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    # jti means identity
    jti = jwt_payload["jti"]
    return RevokedTokenModel.is_jti_blacklisted(jti)


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401

# I'll use required fresh token func.
# on the Change Password Acreen


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@socketio.on("connect")
def connect():
    from g_variables import whoop_list

    print("A user connected.")
    user_dict = {"whoops": whoop_list}
    emitting_json = json.dumps(user_dict)
    socketio.emit("user_event", emitting_json)


def set_api():
    from resources.test import Test
    from resources.home import HomePage
    from resources.whoop import ShareWhoop
    from resources.token import TokenRefresh, TokenBlacklist
    # from resources.image import ImageUpload, Image, AvatarUpload, Avatar
    from resources.login_google import GoogleLogin, GoogleAuthorize
    from resources.login_facebook import FacebookLogin, FacebookAuthorize

    from resources.user import (
        UserSignUp, UserSignin, UserResource, AllUsers, UserLogout, SetPassword
    )

    from resources.whoop import ShareWhoop, Whoops, WhoopsByTitle, WhoopsByTag, WhoopsByUsername

    # mongo user resources
    api.add_resource(UserResource, '/user')
    api.add_resource(AllUsers, '/user/all')
    api.add_resource(UserSignUp, '/user/signup')
    api.add_resource(UserSignin, '/user/signin')
    api.add_resource(UserLogout, '/user/logout')
    api.add_resource(SetPassword, '/user/setpassword')

    # mongo whoop resources
    api.add_resource(ShareWhoop, '/whoop/share')
    api.add_resource(Whoops, '/whoops/<string:user_id>')
    api.add_resource(WhoopsByTitle, '/whoops/title/<string:title>')
    api.add_resource(WhoopsByTag, '/whoops/tag/<string:tag>')
    api.add_resource(WhoopsByUsername, '/whoops/username/<string:username>')

    # home page resources
    api.add_resource(HomePage, '/')

    # test resources
    api.add_resource(Test, '/test')

    # token resources
    api.add_resource(TokenRefresh, '/token/refresh')
    api.add_resource(TokenBlacklist, '/token/is_token_blacklisted')

    # image resources
    #api.add_resource(ImageUpload, '/upload/image')
    #api.add_resource(Image, '/image/<string:filename>')
    #api.add_resource(AvatarUpload, '/upload/avatar')
    #api.add_resource(Avatar, '/avatar/<int:user_id>')

    # google oauth resources
    api.add_resource(GoogleLogin, '/login/google')
    api.add_resource(GoogleAuthorize, '/login/google/authorized',
                     endpoint='google.authorized')

    # facebook oauth resources
    api.add_resource(FacebookLogin, '/login/facebook')
    api.add_resource(FacebookAuthorize, '/login/facebook/authorized',
                     endpoint='facebook.authorized')


# I moved all the script outside of the main func. because when I run
# the app on Heroku with gunicorn it only works like that.

# handle_connection(
#     host='mongodb+srv://whoops-database:whoops-database@whoops-cluster.sslk6.mongodb.net/whoops-database?retryWrites=true&w=majority',
# )

# oauth.init_app(app)
# set_api()

# scheduler = APScheduler()
# scheduler.add_job(
#     id="Scheduled Task", func=scheduleTask, trigger="interval", seconds=1
# )

# scheduler.start()

if __name__ == "__main__":
    handle_connection(
        host='mongodb+srv://whoops-database:whoops-database@whoops-cluster.sslk6.mongodb.net/whoops-database?retryWrites=true&w=majority',
    )

    oauth.init_app(app)
    set_api()

    scheduler = APScheduler()
    scheduler.add_job(
        id="Scheduled Task", func=scheduleTask, trigger="interval", seconds=1
    )

    scheduler.start()

    socketio.run(app, debug=True, use_reloader=False)
