import unittest
import os, sys
from src.model.antenna import AntennaUSB
from src.utils.common import Config


class AntennaUSBTestCase(unittest.TestCase):

    def setUp(self):
        base_dir = os.path.dirname(os.path.realpath(__name__))
        config = Config.instance(base_dir)
        self.config = config
        self.antenna = AntennaUSB.new_entry_instance()

    @unittest.skipUnless(sys.platform.startswith("lin"), "requires Linux")
    def test_new_instance_successfully(self):

        def callback(**kwargs):
            print(kwargs)

        self.antenna.start_to_listen(callback=callback)
        import time
        time.sleep(10)
        self.antenna.stop_to_listen()
