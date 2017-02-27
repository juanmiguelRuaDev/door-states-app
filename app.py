from flask import Flask, jsonify, request
from src.core.contexts import EntryContext, ExitContext
from src.utils.common import Config, convert_to_card_list, Constants
from src.core.managers import AccessCardManager, PassManager
from datetime import datetime
from src.core.exception import ManagerException
import os
import json

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
    return '''<h1>Welcome to pgm-barrier-client-rasp</h1></br>
    RASP because this application will be allocated into a raspberryPi'''


"""
DEVICES
"""


@app.route("/devices/barriers/entry/actions/<action_id>", methods=['POST'])
def action_on_entry_barrier(action_id):
    barrier_type = "entry"
    kwargs = {"action_type": "barriers", "action": action_id, "barrier": barrier_type}
    entry_context.perform_action(**kwargs)
    object_response = {
        "barrierType": barrier_type,
        "opened": entry_context.barrier.is_opened(),
        "locked": entry_context.barrier.is_locked()
    }

    return jsonify(object_response)


@app.route("/devices/barriers/exit/actions/<action_id>", methods=['POST'])
def action_on_exit_barrier(action_id):
    barrier_type = "exit"
    kwargs = {"action_type": "barriers", "action": action_id, "barrier": barrier_type}
    exit_context.perform_action(**kwargs)
    object_response = {
        "barrierType": barrier_type,
        "opened": exit_context.barrier.is_opened(),
        "locked": exit_context.barrier.is_locked()
    }
    return jsonify(object_response)


@app.route("/devices/barriers/status", methods=['GET'])
def get_barriers_status():
    access = PassManager.instance().get_not_sent_to_server_passes()
    entry_barrier = {
        "opened": entry_context.barrier.is_opened(), "locked": entry_context.barrier.is_locked()
    }
    exit_barrier = {
        "opened": exit_context.barrier.is_opened(), "locked": exit_context.barrier.is_locked()
    }
    object_response = {"entry": entry_barrier, "exit": exit_barrier, "access": access}
    return jsonify(object_response)


@app.route("/devices/antenna/<antenna_type>/actions/card_detected", methods=['POST'])
def antenna_card_detected(antenna_type):
    card_id = request.args.get("card")
    booster_id = request.args.get("booster")
    if not card_id or not booster_id:
        return jsonify({"error": "define request parameters 'card' and 'booster'"})
    if antenna_type not in ['entry', 'exit']:
        return jsonify({"error": "<antenna_type> must be either 'entry' or 'exit'"})

    context = entry_context if antenna_type == 'entry' else exit_context
    kwargs = {"action_type": "antenna", "action": "card_detected", "card_number": card_id, "booster_id": booster_id}

    context.perform_action(**kwargs)
    return jsonify(kwargs)


@app.route("/devices/bucle/<entry_exit>/<bucle_type>/actions/<action_id>", methods=['POST'])
def bucle_edge_detected(entry_exit, bucle_type, action_id):
    if entry_exit not in ['entry', 'exit']:
        return jsonify({"error": "<entry_exit> must be either 'entry' or 'exit'"})
    if bucle_type not in ['inside', 'outside']:
        return jsonify({"error": "<bucle_type> must be either 'entry' or 'exit'"})
    if action_id not in ['rising', 'falling']:
        return jsonify({"error": "<action_id> must be either 'rising' or 'falling'"})

    context = entry_context if entry_exit == 'entry' else exit_context
    action = "edge_falling" if action_id == 'falling' else 'edge_rising'

    kwargs = {"action_type": "bucle", "bucle_type": bucle_type, "action": action}
    context.perform_action(**kwargs)
    return jsonify(kwargs)

    pass


@app.route("/devices/semaphores/entry/actions/<action_id>", methods=['POST'])
def action_on_entry_semaphore(action_id):
    semaphore_type = "entry"
    kwargs = {"action_type": "semaphores", "action": action_id, "semaphore": semaphore_type}
    entry_context.perform_action(**kwargs)
    return jsonify({"semaphoreType": semaphore_type, "actionId": action_id})


@app.route("/devices/semaphores/exit/actions/<action_id>", methods=['POST'])
def action_on_exit_semaphore(action_id):
    semaphore_type = "exit"
    kwargs = {"action_type": "semaphores", "action": action_id, "semaphore": semaphore_type}
    entry_context.perform_action(**kwargs)
    return jsonify({"semaphoreType": semaphore_type, "actionId": action_id})


"""
EMERGENCY
"""


@app.route("/emergency/<emergency_action>", methods=['POST'])
def emergency(emergency_action):
    kwargs = {"action_type": "emergency", "action": emergency_action}
    entry_context.perform_action(**kwargs)
    exit_context.perform_action(**kwargs)
    return jsonify({"emergency_action": emergency_action})


"""
CARDS
"""


@app.errorhandler(ManagerException)
def error_in_manager(error):
    return error.message, 500


@app.route("/cards/authorized", methods=['POST'])
def add_cards():
    content = request.get_json()
    manager = AccessCardManager.instance()
    cards_created = manager.add_authorize_card_list(content)
    return json.dumps(cards_created)


@app.route("/cards/authorized", methods=['PUT'])
def update_cards():
    content = request.get_json()
    manager = AccessCardManager.instance()
    cards_created = manager.update_authorized_card_list(content)
    return json.dumps(cards_created)


@app.route("/cards/authorized", methods=['GET'])
def get_cards():
    manager = AccessCardManager.instance()
    card_list = manager.get_authorized_card_list()
    as_json = json.dumps(card_list)
    return as_json


@app.route("/cards/authorized", methods=['DELETE'])
def delete_cards():
    content = request.get_json()
    manager = AccessCardManager.instance()
    cards_delete = manager.delete_authorized_card_list(content)
    return json.dumps(cards_delete)


@app.route("/cards/passing", methods=['GET'])
def get_passes():
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    start_date, end_date = None, None
    if start_date_str:
        start_date = datetime.strptime(start_date_str, Constants.DATE_FORMAT)
    if end_date_str:
        end_date = datetime.strptime(end_date_str, Constants.DATE_FORMAT)
    list_to_return = PassManager.instance().get_passing_between_dates(start_date, end_date)
    return json.dumps(list_to_return)


"""
STATES
"""


@app.route("/states/status", methods=['GET'])
def get_states_status():
    response = {"entry": entry_context.state.__class__.__name__,
                "exit": exit_context.state.__class__.__name__
                }
    return jsonify(response)

"""
CONFIG
"""


@app.route("/config/update", methods=['POST'])
def update_config():
    print("update_config", str(request.data.decode("utf-8")))
    return jsonify({"update": str(request.data.decode("utf-8"))})


if __name__ == '__main__':
    server_ip = config['server']['ip']
    server_port = int(config['server']['port'])
    app.run(host=server_ip, port=server_port, debug=False)
