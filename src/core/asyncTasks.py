import datetime
import time
from src.utils.common import add_secs


def barrier_target(barrier_object, callback):
    """
    Independent process that close the barrier after an specific time define in the  barrier instance
    :param barrier_object:
    :param callback:
    :return:
    """
    current_time = datetime.datetime.now().time()
    # FIXME: Take the 30 seconds from config file or from barrier_object instead
    plus_seconds = add_secs(current_time, 30)
    while barrier_object.is_opened():
        now = datetime.datetime.now().time()
        if plus_seconds < now:
            if not barrier_object.is_locked():
                barrier_object.close()
                callback()
        time.sleep(1)
