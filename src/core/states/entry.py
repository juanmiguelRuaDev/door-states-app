from src.utils.wrappers import StateDoActionWrapper
from src.core.states.generic import GenericState


class EntryInitialState(GenericState):
    """
    output=\n
    * barrier : {opened: false, locked: xxx}
    * antennaNFC : on

     Destination states =\n
     * EntryEmergencyState
     * EntryBarrierOpenedState
     * ReadCardState
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
                self.context.state = EntryEmergencyState(self.context)

        elif action_type == "doors":
            if action == "open":
                self.context.state = EntryDoorOpenedState(self.context)
            elif action == "lock":
                self.context.door.lock()
            elif action == "unlock":
                self.context.door.unlock()


class EntryDoorOpenedState(GenericState):
    """
    output=\n
    * barrier : {opened:true, locked: xxx}
    Destination states =\n
     * EntryEmergencyState
     * EntryInitialState
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
                self.context.state = EntryEmergencyState(self.context)

        elif action_type == "doors":
            if action == "close":
                self.context.state = EntryInitialState(self.context)
            elif action == "lock":
                self.context.door.lock()
            elif action == "unlock":
                self.context.door.unlock()


class EntryEmergencyState(GenericState):
    """
    output=\n
    * barrier : {opened:true, locked: xxx}
    * antennaNFC: off
    Destination states =\n
     * EntryInitialState
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
            self.context.state = EntryInitialState(self.context)