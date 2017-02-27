from src.utils.wrappers import StateDoActionWrapper
from src.core.states.generic import GenericState
import datetime


class ExitInitialState(GenericState):
    """
    State ID = 0
    Sate name = "INITIAL"
    This is the main state, at this state every device is in default state

    output=\n
    * barrier : {opened:false, locked: false}
    * antennaNFC : off

    Destination states:\n
    * ExitReadCardState
    * ExitEmergencyState
    * ExitBarrierOpenedState
    """

    def __init__(self, context):
        super().__init__(context)
        self.__perform_state()

    def __perform_state(self):
        self.context.door.unlock()
        self.context.door.close()

    @StateDoActionWrapper.check_args
    def do_action(self, *args, **kwargs):
        action_type, action = kwargs['action_type'], kwargs['action']

        if action_type == "emergency":
            if action == "on":
                self.context.state = ExitEmergencyState(self.context)

        elif action_type == "doors":
            if action == "open":
                self.context.state = ExitDoorOpenedState(self.context)
            elif action == "lock":
                self.context.door.lock()
            elif action == "unlock":
                self.context.door.unlock()


class ExitDoorOpenedState(GenericState):
    """
    output=\n
    * barrier : {opened:true, locked: xx}
    * antennaNFC: off

    Destination states =\n
     * ExitEmergencyState
     * ExitInitialState
    """

    def __init__(self, context):
        super().__init__(context)
        self.__perform_state()

    def __perform_state(self):
        self.context.door.open()

    @StateDoActionWrapper.check_args
    def do_action(self, *args, **kwargs):
        action_type, action = kwargs['action_type'], kwargs['action']

        if action_type == "emergency":
            if action == "on":
                self.context.state = ExitEmergencyState(self.context)

        elif action_type == "doors":
            if action == "close":
                self.context.state = ExitInitialState(self.context)
            elif action == "lock":
                self.context.door.lock()
            elif action == "unlock":
                self.context.door.unlock()


class ExitEmergencyState(GenericState):
    """
    output=\n
    * barrier : {opened:true, locked: xx}
    * antennaNFC: off
    Destination states =\n
     * ExitInitialState
    """

    def __init__(self, context):
        super().__init__(context)
        self.__perform_state()

    def __perform_state(self):
        self.context.door.lock()
        self.context.door.open()

    @StateDoActionWrapper.check_args
    def do_action(self, *args, **kwargs):
        action_type, action = kwargs['action_type'], kwargs['action']

        if action_type != "emergency":
            return

        if action == 'off':
            self.context.state = ExitInitialState(self.context)
