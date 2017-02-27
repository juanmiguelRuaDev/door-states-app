from importlib import util as importlib_util
from abc import ABCMeta, abstractmethod
import sys
import threading
import src.ext.pigpio as pigpio
from src.core.asyncTasks import edge_falling_target


class GPIOOut(object):
    """
    Parent class that will deal with GPIO pins of RaspberryPi2
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


class GPIOIn(object, metaclass=ABCMeta):
    """
    Parent class that will deal with GPIO IN pins of RaspberryPi2
    """

    def __init__(self, name, gpio_pin):
        self.name = name
        self.gpiopin = gpio_pin
        self.is_listening = False
        self.hilo = None
        try:
            gpio_spec = importlib_util.find_spec("RPi.GPIO")
            self.found_gpio = gpio_spec is not None
        except ImportError:
            self.found_gpio = False
        if self.found_gpio:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            self.GPIO.setmode(GPIO.BCM)
            self.GPIO.setup(self.gpiopin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def start_listening(self):
        self.is_listening = True
        if not self.hilo or not self.hilo.is_alive():
            self.hilo = threading.Thread(target=edge_falling_target, args=(self, self.gpio_callback))
            self.hilo.daemon = True
            self.hilo.start()
            self.hilo.join(1)


    def stop_listening(self):
        self.is_listening = False

    @abstractmethod
    def gpio_callback(self):
        pass





class USBRS485Object(object):
    """
    Parent class that will  deal with USB's in raspberryPi2
    """

    def __init__(self, usb_port=None):
        self.is_reading = False
        self.hilo = None
        self.usb_port = usb_port

    def start_read_card(self, callback):
        if not self.hilo or not self.hilo.is_alive():
            from src.core.asyncTasks import usb_rs485_target
            self.hilo = threading.Thread(target=usb_rs485_target, args=(self, callback))
            self.hilo.daemon = True
            self.hilo.start()
        self.hilo.join(1)

    def stop_read_card(self):
        self.is_reading = False


class NFCObject(object):
    """
    Parent class that will deal with the NFC readers in through USB connection
    in PC and raspberryPi2
    """

    def __init__(self):
        self.is_reading = False
        self.hilo = None

    def start_read_nfc(self, callback):
        if not self.hilo or not self.hilo.is_alive():
            from src.core.asyncTasks import nfc_target
            self.hilo = threading.Thread(target=nfc_target, args=(self, callback))
            self.hilo.daemon = True
            self.hilo.start()
        self.hilo.join(1)

    def stop_read_nfc(self):
        self.is_reading = False

    @staticmethod
    def read_card():
        import subprocess
        try:
            p = subprocess.Popen(['nfc-list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
        except FileNotFoundError:
            return None
        return NFCObject.get_card_id(str(out))

    @staticmethod
    def get_card_id(response_args):
        init_index = response_args.find("UID", 100)
        last_index = response_args.find('\n', init_index, init_index + 35)
        if init_index < 0:
            return None
        response = response_args[init_index:last_index - 1]
        init_index = response.find(':')
        if init_index < 0:
            return None
        response = response[init_index + 1:]
        resp_spliced = response.split('  ')
        return ''.join(resp_spliced).swapcase()[:9].strip()


class WiegandReader(object):
    def __init__(self, pi, gpio_0, gpio_1, bit_timeout=5):
        """
        Instantiate with the pi, gpio for 0 (green wire), the gpio for 1
        (white wire), the callback function, and the bit timeout in
        milliseconds which indicates the end of a code.

        The callback is passed the code length in bits and the value.
        """
        if sys.platform.startswith("lin"):
            self.pi = pi
            self.pi.set_mode(gpio_0, pigpio.INPUT)
            self.pi.set_mode(gpio_1, pigpio.INPUT)
            self.pi.set_pull_up_down(gpio_0, pigpio.PUD_UP)
            self.pi.set_pull_up_down(gpio_1, pigpio.PUD_UP)
        self.in_code = False
        self.bit_timeout = bit_timeout
        self.gpio_1 = gpio_1
        self.gpio_0 = gpio_0
        self.callback = None
        self.cb_0 = None
        self.cb_1 = None

    def start_read_card(self, callback):
        """
        Just start to read the code of any card detected
        :param callback:
        :return:
        """
        self.callback = callback
        if sys.platform.startswith("lin"):
            self.cb_0 = self.pi.callback(self.gpio_0, pigpio.FALLING_EDGE, self._cb)
            self.cb_1 = self.pi.callback(self.gpio_1, pigpio.FALLING_EDGE, self._cb)

    def _cb(self, gpio, level, tick):
        """
        Accumulate bits until both gpios 0 and 1 timeout.
        """
        if level < pigpio.TIMEOUT:

            if self.in_code is False:
                self.bits = 1
                self.num = 0
                self.in_code = True
                self.code_timeout = 0
                self.pi.set_watchdog(self.gpio_0, self.bit_timeout)
                self.pi.set_watchdog(self.gpio_1, self.bit_timeout)
            else:
                self.bits += 1
                self.num <<= 1

            if gpio == self.gpio_0:
                self.code_timeout &= 2  # clear gpio 0 timeout
            else:
                self.code_timeout &= 1  # clear gpio 1 timeout
                self.num |= 1

        else:

            if self.in_code:

                if gpio == self.gpio_0:
                    self.code_timeout |= 1  # timeout gpio 0
                else:
                    self.code_timeout |= 2  # timeout gpio 1

                if self.code_timeout == 3:  # both gpio's timed out
                    self.pi.set_watchdog(self.gpio_0, 0)
                    self.pi.set_watchdog(self.gpio_1, 0)
                    self.in_code = False
                    hexadecimal = hex(self.num >> 1)
                    hexa_int = int(hexadecimal, 16)
                    card_code = ("%x" % hexa_int)

                    if len(card_code) < 8:
                        pass

                    if len(card_code) > 8:
                        card_code = card_code[1:]
                    callback_params = {"card_number": card_code.upper(), "action": "card_detected"}
                    self.callback(**callback_params)

    def cancel(self):
        """
        Cancel the Wiegand decoder.
        """
        if self.cb_0 is not None and self.cb_1 is not None:
            self.cb_0.cancel()
            self.cb_1.cancel()
