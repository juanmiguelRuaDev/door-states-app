from importlib import util as importlib_util


class GPIOOut(object):
    """
    Parent class that will deal with GPIO pins of RaspberryPi3
    """

    def __init__(self, name, gpio_pin):
        self.name = name
        self.gpiopin = gpio_pin
        try:
            gpio_spec = importlib_util.find_spec("RPi.GPIO")
            self.found_gpio = gpio_spec is not None
        except ImportError:
            self.found_gpio = False
        if self.found_gpio:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            self.GPIO.setmode(GPIO.BCM)
            self.GPIO.setup(self.gpiopin, GPIO.OUT)

    def on(self):
        if self.found_gpio:
            self.GPIO.output(self.gpiopin, 0)

    def off(self):
        if self.found_gpio:
            self.GPIO.output(self.gpiopin, 1)