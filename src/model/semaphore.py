"""
Here must be defined the appropriated classes to :Bucle concept
"""
from src.core.raspberry import GPIOOut


class Semaphore(GPIOOut):
    def __init__(self, name, gpio_pin=0):
        super().__init__(name, gpio_pin)
        self.__on = False

    def on(self):
        self.__on = True

    def off(self):
        self.__on = False

    def is_on(self):
        return self.__on

    @classmethod
    def new_red_semaphore(cls, name):
        return cls(name, gpio_pin=16)

    @classmethod
    def new_green_semaphore(cls, name):
        return cls(name, gpio_pin=23)

