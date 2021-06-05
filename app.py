from oa import oauth
from db import db
from ma import ma
import json
from datetime import datetime

from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from flask_jwt_extended import JWTManager
#from flask_uploads import patch_request_class, configure_uploads

from dotenv import load_dotenv
from marshmallow import ValidationError

from helpers.task import scheduleTask
#from helpers.image_helper import IMAGE_SET
from models.revoken_token import RevokedTokenModel

load_dotenv(".env", verbose=True)


app = Flask(__name__)

# load default configs from default_config.py
app.config.from_object("default_config")
app.config.from_envvar(
    "APPLICATION_SETTINGS"
)  # override with config.py (APPLICATION_SETTINGS points to config.py)

# 10 MB max image size upload
#patch_request_class(app, 10 * 1024 * 1024)
#configure_uploads(app, IMAGE_SET)

socketio = SocketIO(app, logger=True)
jwt = JWTManager(app)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation_error(err):
    return jsonify(err.messages), 400


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
    from resources.google_login import GoogleLogin, GoogleAuthorize
    from resources.facebook_login import FacebookLogin, FacebookAuthorize
    from resources.twitter_login import TwitterLogin, TwitterAuthorize
    from resources.user import (
        User,
        UserSignin,
        UserSignup,
        UserLogout,
        AllUsers,
        SetPassword
    )

    # home page resources
    api.add_resource(HomePage, '/')

    # user resources
    api.add_resource(User, '/user')
    api.add_resource(UserSignin, '/signin')
    api.add_resource(UserSignup, '/signup')
    api.add_resource(UserLogout, '/logout')
    api.add_resource(AllUsers, '/users')
    api.add_resource(SetPassword, '/user/set_password')

    # test resources
    api.add_resource(Test, '/test')

    # whoop resources
    api.add_resource(ShareWhoop, '/whoop/share')

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

    # twitter oauth resources
    api.add_resource(TwitterLogin, '/login/twitter')
    api.add_resource(TwitterAuthorize, '/login/twitter/authorized',
                     endpoint='twitter.authorized')


# I moved all the script outside of the main func. because when I run
# the app on Heroku with gunicorn it only works like that.
db.init_app(app)
ma.init_app(app)
oauth.init_app(app)

set_api()

scheduler = APScheduler()
scheduler.add_job(
    id="Scheduled Task", func=scheduleTask, trigger="interval", seconds=1
)
scheduler.start()

socketio.run(app, debug=True, use_reloader=False)


if __name__ == "__main__":
    pass
    # db.init_app(app)
    # ma.init_app(app)
    # oauth.init_app(app)

    # set_api()

    # scheduler = APScheduler()
    # scheduler.add_job(
    #     id="Scheduled Task", func=scheduleTask, trigger="interval", seconds=1
    # )
    # scheduler.start()

    # socketio.run(app, debug=True, use_reloader=False)
