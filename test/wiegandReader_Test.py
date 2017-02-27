import unittest
import os, sys
from src.core.raspberry import WiegandReader
from src.utils.common import Config


class WiegandReaderTestCase(unittest.TestCase):

    def setUp(self):
        base_dir = os.path.dirname(os.path.realpath(__name__))
        config = Config.instance(base_dir)
        self.config = config
        import src.ext.pigpio as pigpioext
        pi = pigpioext.pi()
        gpio_pin0 = config['antenna.entry']['gpio_0']
        gpio_pin1 = config['antenna.entry']['gpio_1']
        self.antenna = WiegandReader(pi, gpio_pin0, gpio_pin1)

    @unittest.skipUnless(sys.platform.startswith("lin"), "requires Linux")
    def test_new_instance_successfully(self):

        def callback(**kwargs):
            print(kwargs)

        self.antenna.start_read_card(callback)
        import time
        time.sleep(10)
        self.antenna.cancel()
