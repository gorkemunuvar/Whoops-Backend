import json
from flask import request
from flask_restful import Resource
from datetime import datetime, timedelta

from flask_jwt_extended import jwt_required, get_jwt_identity

from g_variables import whoop_list

from models.mongodb_models import User, Whoop


def socketio_emit(name, message):
    # from app does not work
    from app import socketio

    socketio.emit(name, message)


class MongoShareWhoop(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        whoop_json = request.get_json()
        #whoop = whoop_schema.load(whoop_json)

        add_second = whoop_json["time"]
        starting_time = datetime.now()
        # days, seconds, then other fields.
        ending_time = starting_time + timedelta(0, add_second)

        print(whoop_json)

        user_jwt_id = get_jwt_identity()
        user = User.objects(pk=user_jwt_id)

        if user is None:
            print("(Resource: ShareWhoop) User not found by id. ")
            print("Try to log out and login again.")

            return {"message": "User not found by id."}, 404

        #whoop.user_id = user.id

        whoop = Whoop()
        whoop.title = whoop_json['title']
        whoop.latitude = whoop_json['latitude']
        whoop.longitude = whoop_json['longitude']
        whoop.time = whoop_json['time']
        whoop.starting_time = str(starting_time.strftime("%Y-%m-%d %H:%M:%S"))
        whoop.ending_time = str(ending_time.strftime("%Y-%m-%d %H:%M:%S"))
        whoop.user = user

        whoop.save()

        print(user)

        #whoop_dict = whoop_schema.dump(whoop)
        whoop_list.append(whoop.to_json())

        emitting_json = json.dumps({"whoops": whoop_list})

        print("----------------emitting json / resources.py----------------")
        print(emitting_json)
        print("----------------emitting json----------------"),

        socketio_emit("user_event", emitting_json)
        print("Post request has been successed.")

        return {"message": "Post request has been successed."}, 200
