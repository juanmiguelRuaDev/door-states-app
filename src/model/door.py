"""
Here must be defined the appropriated classes to :Door concept
"""
import threading
from src.core.raspberry import GPIOOut
from src.utils.common import Config
from src.core.observer import Observable
from src.core.asyncTasks import door_timeout_target


class Door(GPIOOut, Observable):

    def __init__(self, name, gpio_pin=0):
        GPIOOut.__init__(self, name, gpio_pin)
        Observable.__init__(self)
        self.hilo = None
        self.__opened = False
        self.__locked = False

    def open(self):
        super().on()
        self.__opened = True
        if not self.is_locked():
            self.__set_timeout_to_close()

    def __set_timeout_to_close(self):
        """
        Set a time out to close the barrier after 30 minutes
        :return:
        """
        if not self.hilo or not self.hilo.is_alive():
            self.hilo = threading.Thread(target=door_timeout_target, args=(self, self.timeout_callback))
            self.hilo.daemon = True
            self.hilo.start()
        self.hilo.join(1)

    def timeout_callback(self):
        kwargs = {"action_type": "doors", "action": "close", "door_name": self.name}
        self.notify_observers(**kwargs)

    def close(self):
        super().off()
        self.__opened = False

    def lock(self):
        self.__locked = True

    def unlock(self):
        self.__locked = False
        if self.is_opened():
            self.__set_timeout_to_close()

    def is_locked(self):
        return self.__locked

    def is_opened(self):
        return self.__opened

    def __str__(self):
        return str(self.__dict__)

    @classmethod
    def new_entry_door(cls, name):
        config = Config.instance()
        gpio_pin = config['gpio.out.door.entry']['gpio_pin']
        return cls(name, gpio_pin=int(gpio_pin))

    @classmethod
    def new_exit_door(cls, name):
        config = Config.instance()
        gpio_pin = config['gpio.out.door.exit']['gpio_pin']
        return cls(name, gpio_pin=int(gpio_pin))
