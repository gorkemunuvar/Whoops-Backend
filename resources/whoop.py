import json
from flask import request
from flask_restful import Resource
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine import DoesNotExist
from g_variables import whoop_list

from models.user import User
from models.whoop import Whoop, Address


def socketio_emit(name, message):
    # from app does not work
    from __main__ import socketio

    socketio.emit(name, message)


class ShareWhoop(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        whoop_json = request.get_json()
        print(whoop_json)

        add_second = whoop_json["time"]
        starting_time = datetime.now()
        # days, seconds, then other fields.
        ending_time = starting_time + timedelta(0, add_second)

        user_jwt_id = get_jwt_identity()

        try:
            # after the query current_user is the mongoengine User model
            loggedin_user = User.objects.get(pk=user_jwt_id)
        except DoesNotExist:
            return {"message": "(Share Whoop Resource) User doesn't exist"}, 404

        address = Address(**whoop_json['address'])
        whoop = Whoop(**whoop_json)

        whoop.is_active = True
        whoop.date_created = str(datetime.date(datetime.now()))
        whoop.starting_time = str(starting_time.strftime("%Y-%m-%d %H:%M:%S"))
        whoop.ending_time = str(ending_time.strftime("%Y-%m-%d %H:%M:%S"))

        whoop.address = address
        whoop.user = loggedin_user

        whoop.save()

        # list of whoop models
        whoop_list.append(whoop)

        # list of whoop model jsons
        whoop_json_list = [whoop.to_json() for whoop in whoop_list]

        emitting_json = json.dumps({"whoops": whoop_json_list})

        print("----------------emitting json / resources.py----------------")
        print(emitting_json)
        print("----------------emitting json----------------"),

        socketio_emit("user_event", emitting_json)
        print("Post request has been successed.")

        return {"message": "Post request has been successed."}, 200


class Whoops(Resource):
    @classmethod
    @jwt_required()
    def get(cls, user_id: str):
        user = User()
        try:
            user = User.objects.get(pk=user_id)
        except DoesNotExist:
            return {'message': 'User {user_id} not found!'}, 404

        whoops = Whoop.objects(user=user).all()
        whoops_json = [whoop.to_json() for whoop in whoops]

        return whoops_json, 200
