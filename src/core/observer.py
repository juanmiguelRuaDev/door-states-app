from abc import ABCMeta, abstractmethod
from src.utils.wrappers import StateDoActionWrapper


class Observable:
    """
    An Observable will store zero or many observers and every time that
    a triggers is ran, will be notified to every observer that have in its
    internal memory
    """
    def __init__(self):
        self.__observers = []

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self.__observers:
            observer.notify(self, *args, **kwargs)


class Observer(metaclass=ABCMeta):
    """
    This is an abstract class whose  only objective is receive the
    notifications sent by any observable object where is registered
    this current observer
    """

    def __init__(self, observable_list):
        for observable in observable_list:
            if not isinstance(observable, Observable):
                raise StateDoActionWrapper("%s is not instance of 'Observable'" % str(observable))
            observable.register_observer(self)

    @abstractmethod
    def notify(self, observable, *args, **kwargs):
        #TODO: Change the name of this method to observeOn (is more acurate)
        pass
