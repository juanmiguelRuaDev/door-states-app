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
        self.appContext.perform_action(action="open", action_type="barriers")
        self.assertIsInstance(self.appContext.state, EntryBarrierOpenedState)
        self.appContext.perform_action(action="close", action_type="barriers")
        self.assertIsInstance(self.appContext.state, EntryInitialState)
        self.appContext.perform_action(action="on", action_type="emergency")
        self.assertIsInstance(self.appContext.state, EntryEmergencyState)
        self.appContext.perform_action(action="off", action_type="emergency")
        self.assertIsInstance(self.appContext.state, EntryInitialState)
        self.assertIsNotNone(self.appContext)

    def test_entry_bucle_outside(self):
        self.assertIsInstance(self.appContext.state, EntryInitialState)
        self.appContext.entry_bucle_inside.gpio_callback()
        self.assertIsInstance(self.appContext.state, EntryInitialState)

    def test_authorization_in_initial_state(self):
        """
        This tests the  AUTHORIZATION logical test
        :return:
        """
        # Iff barrier is not locked, the context will change to {EntryBarrerOpenedState} state
        self.assertEqual(self.appContext.barrier.is_locked(), False)
        self.appContext.perform_action(action_type="authorization", action="success")
        self.assertIsInstance(self.appContext.state, EntryBarrierOpenedState)
        self.appContext.perform_action(action_type="barriers", action="close")
        self.assertIsInstance(self.appContext.state, EntryInitialState)

        # If barrier is locked, The context will not change the state
        self.appContext.barrier.lock()
        self.assertEqual(self.appContext.barrier.is_locked(), True)
        self.appContext.perform_action(action_type="authorization", action="success")
        self.assertIsInstance(self.appContext.state, EntryInitialState)


if __name__ == '__main__':
    unittest.main()
