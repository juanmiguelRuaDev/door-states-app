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
                self.context.state = ExitBarrierOpenedState(self.context)
            elif action == "lock":
                self.context.door.lock()
            elif action == "unlock":
                self.context.door.unlock()


class ExitBarrierOpenedState(GenericState):
    """
    State ID = 1 \n
    State Name = "BARRIER_OPENED"\n
    At this state, the barrier will be opened and the semaphore put in on

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
    State ID = 3
    State Name = "EMERGENCY"
    This status is the most important. This status indicates that we are in emergency status. The only way
    to go to other status is receiving the emergency:off event.
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
