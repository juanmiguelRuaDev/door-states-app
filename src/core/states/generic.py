from abc import ABCMeta, abstractmethod

"""
TODO: Find out if is convenient make each state as singleton to avoid overloading in memory
"""


class GenericState(metaclass=ABCMeta):

    def __init__(self, context):
        self.context = context

    @abstractmethod
    def do_action(self, *args, **kwargs):
        """
        This method will be override by all states, where have to receive at least a
        parameter 'action' e.x(action='BARRIER_OPENED)
        :param args:
        :param kwargs:
        :return:
        """
        pass


