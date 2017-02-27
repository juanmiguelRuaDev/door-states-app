import unittest
import os, sys
from src.model.antenna import AntennaNFC
from src.utils.common import Config


class AntennaTestCase(unittest.TestCase):

    def setUp(self):
        base_dir = os.path.dirname(os.path.realpath(__name__))
        config = Config.instance(base_dir)
        self.config = config
        self.antenna = AntennaNFC()

    @unittest.skipUnless(sys.platform.startswith("lin"), "requires Linux")
    def test_new_instance_successfully(self):
        self.antenna.start_read_card()
        import time
        time.sleep(1000)
