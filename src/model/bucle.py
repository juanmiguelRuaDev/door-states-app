"""
Here must be defined the appropriated classes to :Bucle concept
"""
from src.core.observer import Observable
from src.core.raspberry import GPIOIn
from src.utils.common import Config


class Bucle(GPIOIn, Observable):

    INSIDE_TYPE = "inside"
    OUTSIDE_TYPE = "outside"

    def __init__(self, name, gpio_pin=0, bucle_type="inside"):
        self.bucle_type = bucle_type
        GPIOIn.__init__(self, name, gpio_pin)
        Observable.__init__(self)
        #if self.found_gpio:
        #    self.GPIO.add_event_detect(self.gpiopin, self.GPIO.RISING, callback=self.gpio_callback)

    def gpio_callback(self):
        kwargs = {
            "action_type": "bucle",
            "action": "edge_falling",
            "bucle_type": self.bucle_type
        }
        self.notify_observers(**kwargs)

    @classmethod
    def new_entry_bucle_outside(cls, name):
        config = Config.instance()
        gpio_pin = config['gpio.in.bucle.entry.outside']['gpio_pin']
        return cls(name, gpio_pin=int(gpio_pin), bucle_type="outside")

    @classmethod
    def new_entry_bucle_inside(cls, name):
        config = Config.instance()
        gpio_pin = config['gpio.in.bucle.entry.inside']['gpio_pin']
        return cls(name, gpio_pin=int(gpio_pin), bucle_type="inside")

    @classmethod
    def new_exit_bucle_inside(cls, name):
        config = Config.instance()
        gpio_pin = config['gpio.in.bucle.exit.inside']['gpio_pin']
        return cls(name, gpio_pin=int(gpio_pin), bucle_type="inside")

    @classmethod
    def new_exit_bucle_outside(cls, name):
        config = Config.instance()
        gpio_pin = config['gpio.in.bucle.exit.outside']['gpio_pin']
        return cls(name, gpio_pin=int(gpio_pin), bucle_type="outside")
