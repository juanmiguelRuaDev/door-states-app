import unittest
import os
from src.model.bucle import Bucle
from src.utils.common import Config


class BucleTestCase(unittest.TestCase):

    def setUp(self):
        base_dir = os.path.dirname(os.path.realpath(__name__))
        config = Config.instance(base_dir)
        self.config = config
        self.entry_bucle = Bucle.new_entry_bucle_outside('entry_bucle_test')

    def test_new_instance_successfully(self):
        self.assertIsNotNone(self.entry_bucle.gpiopin)
