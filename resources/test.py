import json
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from g_variables import whoop_list


def socketio_emit(name: str, message: str) -> None:
    # 'from app' does not work
    from __main__ import socketio

    socketio.emit(name, message)


class Test(Resource):
    @classmethod
    @jwt_required()
    def get(self):

        user_dict = {"whoops": whoop_list}
        emitting_json = json.dumps(user_dict)

        print("----------------test api----------------")
        print(emitting_json)
        print("-------------test api - end-------------")

        socketio_emit("user_event", emitting_json)

        return emitting_json
