import unittest
import os, sys
from src.core.raspberry import USBRS485Object
from src.utils.common import Config


class USBReaderTestCase(unittest.TestCase):

    def setUp(self):
        base_dir = os.path.dirname(os.path.realpath(__name__))
        config = Config.instance(base_dir)
        self.config = config
        self.usb_reader = USBRS485Object()

    @unittest.skipUnless(sys.platform.startswith("lin"), "requires Linux")
    def test_new_instance_successfully(self):

        def callback(**kwargs):
            print(kwargs)

        self.usb_reader.start_read_card(callback)
        import time
        time.sleep(10)
        self.usb_reader.stop_read_card()
