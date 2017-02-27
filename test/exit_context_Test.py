import os
import unittest

from src.core.contexts import ExitContext
from src.core.states.exit import ExitInitialState, ExitDoorOpenedState, ExitEmergencyState
from src.utils.common import Config


class ExitContextTestCase(unittest.TestCase):

    def setUp(self):
        base_dir = os.path.dirname(os.path.realpath(__name__))
        config = Config.instance(base_dir)
        self.appContext = ExitContext(config=config)

    def test_changing_state(self):
        self.assertIsInstance(self.appContext.state, ExitInitialState)
        self.appContext.perform_action(action="open", action_type="doors")
        self.assertIsInstance(self.appContext.state, ExitDoorOpenedState)
        self.appContext.perform_action(action="close", action_type="doors")
        self.assertIsInstance(self.appContext.state, ExitInitialState)
        self.appContext.perform_action(action="on", action_type="emergency")
        self.assertIsInstance(self.appContext.state, ExitEmergencyState)
        self.appContext.perform_action(action="off", action_type="emergency")
        self.assertIsInstance(self.appContext.state, ExitInitialState)
        self.assertIsNotNone(self.appContext)

if __name__ == '__main__':
    unittest.main()
