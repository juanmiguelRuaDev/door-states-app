import os
import unittest

from src.core.contexts import EntryContext
from src.core.states.entry import EntryInitialState, EntryEmergencyState, EntryBarrierOpenedState
from src.utils.common import Config


class EntryContextTestCase(unittest.TestCase):

    def setUp(self):
        base_dir = os.path.dirname(os.path.realpath(__name__))
        config = Config.instance(base_dir)
        self.appContext = EntryContext(config=config)

    def test_changing_state(self):
        self.assertIsInstance(self.appContext.state, EntryInitialState)
        self.appContext.perform_action(action="open", action_type="doors")
        self.assertIsInstance(self.appContext.state, EntryBarrierOpenedState)
        self.appContext.perform_action(action="close", action_type="doors")
        self.assertIsInstance(self.appContext.state, EntryInitialState)
        self.appContext.perform_action(action="on", action_type="emergency")
        self.assertIsInstance(self.appContext.state, EntryEmergencyState)
        self.appContext.perform_action(action="off", action_type="emergency")
        self.assertIsInstance(self.appContext.state, EntryInitialState)
        self.assertIsNotNone(self.appContext)

if __name__ == '__main__':
    unittest.main()
