from src.utils.wrappers import StateDoActionWrapper
from src.core.states.generic import GenericState
from src.bbdd.dao import PassDAO
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
        self.context.barrier.unlock()
        self.context.barrier.close()
        self.context.antenna.start_to_listen()
        self.context.exit_bucle_outside.start_listening()

    def __card_detected_impl(self, card_id, booster_id):
        """
        Save the {card_id} and the {booster_id} in the context in order to it may
        be used for other sate
        :param card_id:
        :param booster_id:
        :return:
        """
        if not card_id or not booster_id:
            return
        self.context.data = {"tag_id": card_id, "booster_id": booster_id}

    @StateDoActionWrapper.check_args
    def do_action(self, *args, **kwargs):
        action_type, action = kwargs['action_type'], kwargs['action']

        if action_type == "emergency":
            if action == "on":
                self.context.state = ExitEmergencyState(self.context)

        elif action_type == "barriers":
            if action == "open":
                self.context.state = ExitBarrierOpenedState(self.context)
            elif action == "lock":
                self.context.barrier.lock()
            elif action == "unlock":
                self.context.barrier.unlock()

        elif action_type == "antenna":
            if action == "card_detected":
                if self.context.barrier.is_locked():
                    return
                card = kwargs['card_number']
                booster = kwargs['booster_id']
                self.__card_detected_impl(card, booster)
                self.context.state = ExitBarrierOpenedState(self.context)


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
        self.context.barrier.open()

    def __register_access(self):
        """
        Registering in database that the driver with {tag_id} and {booster_id}
        has leaved the proving ground
        :return:
        """
        if self.context.data is not None:
            #FIXME: Change {barrier_id} value and the {result} column name
            pass_obj = {"tag_id": self.context.data["tag_id"],
                        "booster_id": self.context.data["booster_id"],
                        "pass_time": datetime.datetime.now(),
                        "barrier_id": self.context.barrier.gpiopin,
                        "pass_type": False}
            pass_dao = PassDAO()
            pass_dao.create(**pass_obj)
            self.context.data = None

    @StateDoActionWrapper.check_args
    def do_action(self, *args, **kwargs):
        action_type, action = kwargs['action_type'], kwargs['action']

        if action_type == "emergency":
            if action == "on":
                self.context.state = ExitEmergencyState(self.context)

        elif action_type == "barriers":
            if action == "close":
                self.context.state = ExitInitialState(self.context)
            elif action == "lock":
                self.context.barrier.lock()
            elif action == "unlock":
                self.context.barrier.unlock()

        elif action_type == "bucle":
            if action == "edge_falling":
                self.__register_access()
                self.context.state = ExitInitialState(self.context)


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
        self.context.antenna.stop_to_listen()
        self.context.barrier.lock()
        self.context.barrier.open()

    @StateDoActionWrapper.check_args
    def do_action(self, *args, **kwargs):
        action_type, action = kwargs['action_type'], kwargs['action']

        if action_type != "emergency":
            return

        if action == 'off':
            self.context.state = ExitInitialState(self.context)
