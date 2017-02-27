from functools import wraps
from src.utils.common import app_logger
from src.core.exception import StateException


class StateDoActionWrapper(Exception):

    @staticmethod
    def check_args(func):

        @wraps(func)
        def checker(*args, **kwargs):
            try:
                action_type, action = kwargs['action_type'], kwargs['action']
                obj = args[0]
                app_logger(__name__).info("%s:(%s -> %s)", obj.__class__.__name__, action_type, action)
            except KeyError:
                raise StateException("'action_type' and 'action' are mandatories")
            return func(*args, **kwargs)
        return checker
