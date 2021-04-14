import json
from flask_restful import Resource
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required

from g_variables import user_list
from helpers.reqparse_helper import whoop_parser


def socketio_emit(name, message):
    # from app does not work
    from __main__ import socketio

    socketio.emit(name, message)


class ShareWhoop(Resource):
    # @jwt_required()
    def post(self):
        values = whoop_parser.parse_args()

        add_second = int(values["time"])
        starting_time = datetime.now()
        # days, seconds, then other fields.
        ending_time = starting_time + timedelta(0, add_second)

        print(values)

        user_json = {
            "nick": values["nick"],
            "latitude": values["latitude"],
            "longitude": values["longitude"],
            "note": values["note"],
            "time": values["time"],
            "starting_time": str(starting_time.strftime("%Y-%m-%d %H:%M:%S")),
            "ending_time": str(ending_time.strftime("%Y-%m-%d %H:%M:%S")),
        }

        user_list.append(user_json)
        emitting_json = json.dumps({"notes": user_list})

        print("----------------emitting json / resources.py----------------")
        print(emitting_json)
        print("----------------emitting json----------------"),

        socketio_emit("user_event", emitting_json)
        print("Post request has been successed.")

        return {"message": "Post request has been successed."}
