from flask import Flask, jsonify
from src.core.contexts import EntryContext, ExitContext
from src.utils.common import Config
from src.core.exception import ManagerException
import os

'''init config '''
BASE_DIR = os.path.dirname(os.path.realpath(__name__))
config = Config.instance(BASE_DIR)

''' init contexts '''
entry_context = EntryContext(config=config)
exit_context = ExitContext(config=config)

''' init app from Flask '''
app = Flask(__name__)


@app.route('/')
def index():
    return '''<h1>Welcome door-states-app</h1></br>
    This application must be allocated into a raspberryPi v3'''
"""
DEVICES
"""


@app.route("/doors/entry/actions/<action_id>", methods=['POST'])
def action_on_entry_door(action_id):
    door_type = "entry"
    kwargs = {"action_type": "doors", "action": action_id, "barrier": door_type}
    entry_context.perform_action(**kwargs)
    object_response = {
        "doorType": door_type,
        "opened": entry_context.door.is_opened(),
        "locked": entry_context.door.is_locked()
    }

    return jsonify(object_response)


@app.route("/doors/exit/actions/<action_id>", methods=['POST'])
def action_on_exit_barrier(action_id):
    door_type = "exit"
    kwargs = {"action_type": "barriers", "action": action_id, "barrier": door_type}
    exit_context.perform_action(**kwargs)
    object_response = {
        "doorType": door_type,
        "opened": exit_context.door.is_opened(),
        "locked": exit_context.door.is_locked()
    }
    return jsonify(object_response)


@app.route("/devices/doors/status", methods=['GET'])
def get_doors_status():
    entry_door = {
        "opened": entry_context.door.is_opened(), "locked": entry_context.door.is_locked()
    }
    exit_door = {
        "opened": exit_context.door.is_opened(), "locked": exit_context.door.is_locked()
    }
    object_response = {"entry": entry_door, "exit": exit_door}
    return jsonify(object_response)


@app.route("/emergency/<emergency_action>", methods=['POST'])
def emergency(emergency_action):
    kwargs = {"action_type": "emergency", "action": emergency_action}
    entry_context.perform_action(**kwargs)
    exit_context.perform_action(**kwargs)
    return jsonify({"emergency_action": emergency_action})


@app.errorhandler(ManagerException)
def error_in_manager(error):
    return error.message, 500


"""
STATES
"""


@app.route("/states/status", methods=['GET'])
def get_states_status():
    response = {"entry": entry_context.state.__class__.__name__,
                "exit": exit_context.state.__class__.__name__
                }
    return jsonify(response)


if __name__ == '__main__':
    server_ip = config['server']['ip']
    server_port = int(config['server']['port'])
    app.run(host=server_ip, port=server_port, debug=False)
