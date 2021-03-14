import json
from datetime import datetime

def socketio_emit(name, message):
    # from app does not work
    from __main__ import socketio
    socketio.emit(name, message)
    
def scheduleTask():
    from g_variables import user_list

    for user in user_list:
        current_time = datetime.now()
        target_time = datetime.strptime(
            user['ending_time'], '%Y-%m-%d %H:%M:%S')

        if current_time >= target_time:
            print('comparing...')

            user_list.remove(user)
            print("Deleteted: ", user)

            user_dict = {'notes': user_list}
            emitting_json = json.dumps(user_dict)

            socketio_emit('user_event', emitting_json)
            
            print("----------------emitting json / task.py----------------")
            print(emitting_json)
            print("----------------emitting json----------------")
            

            
