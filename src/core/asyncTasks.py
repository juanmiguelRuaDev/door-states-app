import datetime
import time
import serial
import sys
from src.utils.common import add_secs
from src.utils.common import app_logger


def nfc_target(nfc_object, callback):
    """
    Separated thread that implements the reading of a nfc connected to the raspberry
    :param nfc_object:
    :param callback:
    :return:
    """
    nfc_object.is_reading = True
    current_time = datetime.datetime.now().time()
    plus_seconds = add_secs(current_time, 30)
    kwargs = {"card_number": None, "action": "time_expired"}
    while nfc_object.is_reading:
        now = datetime.datetime.now().time()
        if plus_seconds < now:
            nfc_object.stop_read_nfc()

        card = nfc_object.read_card()
        if card:
            kwargs["card_number"] = card
            kwargs["action"] = "card_detected"
            nfc_object.stop_read_nfc()
        time.sleep(1)
    callback(**kwargs)


def usb_rs485_target(usb_object, callback):
    """
    Process that read any params from the antenna RS485
    :param usb_object:
    :param callback:
    :return:
    """
    usb_object.is_reading = True
    code_len = 24
    if not sys.platform.startswith("lin"):
        return
    ser = None
    try:
        ser = serial.Serial(usb_object.usb_port, 9600, timeout=1)
    except (FileNotFoundError, serial.serialutil.SerialException):
        app_logger(__name__).warning("antenna ' %s ' doesn't exist", usb_object.usb_port)
    if ser is None:
        return
    while usb_object.is_reading:
        str1 = ser.read(code_len)
        try:
            response = str1.decode('ascii')
        except UnicodeDecodeError:
            continue
        if response != '' and len(response) == code_len:
            booster_id = response[4:12]
            card_id = response[16:]
            callback_params = {
                "card_number": card_id.upper(),
                "booster_id": booster_id.upper(),
                "action": "card_detected"}
            callback(**callback_params)


def edge_falling_target(bucle_object, callback):
    """
    Implementation that runs the {callback} when a edge falling is detected
    :param bucle_object:
    :param callback:
    :return:
    """
    value_before = 0
    value_after = 0
    while bucle_object.is_listening is True:
        if not hasattr(bucle_object, 'GPIO'):
            #windows platform
            continue
        input_state = bucle_object.GPIO.input(bucle_object.gpiopin)
        value_before = value_after
        if not input_state:
            value_after = 1
        else:
            value_after = 0
        if value_before is 1 and value_after is 0:
            # Edge falling
            callback()
        time.sleep(0.05)


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


def icpg_barrier_open_by_signal(timeout_in_secs, callback):
    """
    Probably this method will be removed because this implementation is not used anywhere
    :param timeout_in_secs:
    :param callback:
    :return:
    """
    time.sleep(timeout_in_secs)
    callback()
