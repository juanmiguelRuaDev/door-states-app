from src.core.raspberry import NFCObject, WiegandReader, USBRS485Object
from src.core.observer import Observable
from src.utils.common import Config


class AntennaNFC(NFCObject, Observable):

    def __init__(self):
        NFCObject.__init__(self)
        Observable.__init__(self)
        self.is_reading = False

    def start_read_card(self):
        super().start_read_nfc(self.read_nfc_callback)

    def read_nfc_callback(self, **kwargs):
        card = kwargs['card_number']
        action = kwargs['action']
        notify_kwargs = {"action_type": "antenna", "action": action, "card_number": card}
        self.notify_observers(**notify_kwargs)

    @classmethod
    def new_instance(cls):
        return cls()


class AntennaUSB(USBRS485Object, Observable):
    """
    This class read the card code from antenna through USB-RS485 protocol
    """
    def __init__(self, usb_port=None):
        USBRS485Object.__init__(self, usb_port)
        Observable.__init__(self)

    def start_to_listen(self, callback=None):
        """
        As it said, this method start to listen the antenna to receive data and send data to its observer
        :return:
        """
        if callback is not None:
            super().start_read_card(callback)
        else:
            super().start_read_card(self.read_card_callback)

    def stop_to_listen(self):
        """
        This method stop to listen the antenna
        :return:
        """
        super().stop_read_card()

    def read_card_callback(self, **kwargs):
        """
        Callback that performs the action when a cardcode is detected.
        :param kwargs:
        :return:
        """
        card = kwargs['card_number']
        booster = kwargs['booster_id']
        action = kwargs['action']
        notify_kwargs = {"action_type": "antenna",
                         "action": action,
                         "card_number": card,
                         "booster_id": booster}
        self.notify_observers(**notify_kwargs)

    @classmethod
    def new_entry_instance(cls):
        config = Config.instance()
        usb_port = config['antenna.entry']['usb_port']
        return cls(usb_port)

    @classmethod
    def new_exit_instance(cls):
        config = Config.instance()
        usb_port = config['antenna.exit']['usb_port']
        return cls(usb_port)


class AntennaWiegand(WiegandReader, Observable):
    """
    This  read the card code from the Wiegand antenna
    """
    def __init__(self, gpio_pin0, gpio_pin1):
        import src.ext.pigpio as pigpioext
        pi = pigpioext.pi()
        WiegandReader.__init__(self, pi, gpio_pin0, gpio_pin1)
        Observable.__init__(self)

    def start_to_listen(self, callback=None):
        """
        As it said, this method start to listen the antenna to receive data and send data to its observer
        :return:
        """
        if callback is not None:
            super().start_read_card(callback)
        else:
            super().start_read_card(self.read_card_callback)
        
    def stop_to_listen(self):
        """
        This method stop to listen the antenna
        :return:
        """
        super().cancel()

    def read_card_callback(self, **kwargs):
        """
        Callback that performs the action when a cardcode is read.
        :param kwargs:
        :return:
        """
        card = kwargs['card_number']
        action = kwargs['action']
        notify_kwargs = {"action_type": "antenna", "action": action, "card_number": card}
        self.notify_observers(**notify_kwargs)

    @classmethod
    def new_instance(cls):
        from src.utils.common import Config
        config = Config.instance()
        gpio_pin0 = config['antenna.entry']['gpio_0']
        gpio_pin1 = config['antenna.entry']['gpio_1']
        return cls(int(gpio_pin0), int(gpio_pin1))
