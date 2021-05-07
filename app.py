import json
from db import db
from datetime import datetime
from flask import Flask, jsonify
from flask_socketio import SocketIO

from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from flask_jwt_extended import JWTManager

from helpers.task import scheduleTask
from models.revoken_token import RevokedTokenModel

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "appsecretkey"
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config["JWT_SECRET_KEY"] = "jwtsecretkey"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]


socketio = SocketIO(app, logger=True)
jwt = JWTManager(app)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


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
    from g_variables import user_list

    print("A user connected.")
    user_dict = {"notes": user_list}
    emitting_json = json.dumps(user_dict)
    socketio.emit("user_event", emitting_json)


def set_api():
    from resources.test import Test
    from resources.whoop import ShareWhoop
    from resources.token import TokenRefresh, TokenBlacklist
    from resources.user import (
        UserSignin,
        UserSignup,
        UserLogout,
        AllUsers,
    )

    # user resources
    api.add_resource(UserSignin, "/signin")
    api.add_resource(UserSignup, "/signup")
    api.add_resource(UserLogout, "/logout")
    api.add_resource(AllUsers, "/users")

    # test resources
    api.add_resource(Test, "/test")

    # whoop resources
    api.add_resource(ShareWhoop, "/whoop/share")

    # token resources
    api.add_resource(TokenRefresh, "/token/refresh")
    api.add_resource(TokenBlacklist, "/token/is_token_blacklisted")


if __name__ == "__main__":
    db.init_app(app)
    set_api()
    scheduler = APScheduler()

    scheduler.add_job(
        id="Scheduled Task", func=scheduleTask, trigger="interval", seconds=1
    )
    scheduler.start()
    socketio.run(app, debug=True, use_reloader=False)
