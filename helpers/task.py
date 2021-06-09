import os
import json
from datetime import datetime


def socketio_emit(name, message):
    # from app does not work
    from app import socketio

    socketio.emit(name, message)


def scheduleTask() -> None:
    from g_variables import whoop_list

    for whoop in whoop_list:
        current_time = datetime.now()
        target_time = datetime.strptime(whoop["ending_time"], "%Y-%m-%d %H:%M:%S")

        if current_time >= target_time:
            print("comparing...")

            whoop_list.remove(whoop)
            print("Deleteted: ", whoop)

            whoop_dict = {"whoops": whoop_list}
            emitting_json = json.dumps(whoop_dict)

            socketio_emit("user_event", emitting_json)

            print("----------------emitting json / task.py----------------")
            print(emitting_json)
            print("----------------emitting json----------------")
