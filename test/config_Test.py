import unittest
import os
from src.utils.common import Config


class ConfigTestCase(unittest.TestCase):

    def test_new_instance_successfully(self):
        base_dir = os.path.dirname(os.path.realpath(__name__))
        config = Config.instance(base_dir)
        self.assertIsNotNone(config)
        self.assertIsInstance(config['server']['ip'], str)
        config2 = Config.instance()
        self.assertIsNotNone(config2)
        self.assertIsInstance(config2['server']['ip'], str)
        self.assertEqual(config, config2)
