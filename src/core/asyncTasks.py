import datetime
import time
from src.utils.common import add_secs


def door_timeout_target(door_object, callback):
    """
    Independent process that close the barrier after an specific time define in the  door instance
    :param door_object:
    :param callback:
    :return:
    """
    current_time = datetime.datetime.now().time()
    # FIXME: Take the 30 seconds from config file or from door_object instead
    plus_seconds = add_secs(current_time, 30)
    while door_object.is_opened():
        now = datetime.datetime.now().time()
        if plus_seconds < now:
            if not door_object.is_locked():
                door_object.close()
                callback()
        time.sleep(1)
