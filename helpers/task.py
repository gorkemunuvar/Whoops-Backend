import json
from datetime import datetime
from models.whoop import Whoop


def socketio_emit(name, message):
    # from app does not work
    from __main__ import socketio

    socketio.emit(name, message)


def scheduleTask() -> None:
    from g_variables import whoop_list

    for whoop in whoop_list:
        whoop_json = whoop.to_json()

        current_time = datetime.now()
        target_time = datetime.strptime(
            whoop_json["ending_time"], "%Y-%m-%d %H:%M:%S")

        if current_time >= target_time:
            print("comparing...")

            whoop_list.remove(whoop)

            Whoop.objects(pk=whoop.pk).update(set__is_active = False)
            print("is_active field = false, deleted from the list: ", whoop_json)

            whoop_json_list = [whoop.to_json() for whoop in whoop_list]
            whoop_dict = {"whoops": whoop_json_list}
            emitting_json = json.dumps(whoop_dict)

            socketio_emit("user_event", emitting_json)

            print("----------------emitting json / task.py----------------")
            print(emitting_json)
            print("----------------emitting json----------------")
