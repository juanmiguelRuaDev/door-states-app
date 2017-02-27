from src.utils.wrappers import StateDoActionWrapper
from src.core.states.generic import GenericState
from src.bbdd.dao import AuthorizedDAO, PassDAO
from src.utils.common import app_logger
import datetime


class EntryInitialState(GenericState):
    """
    State ID = 0

    Sate name = "INITIAL"

    This is the main state, at this state every device is in default state

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
        self.context.barrier.unlock()
        self.context.barrier.close()
        self.context.antenna.start_to_listen()
        self.context.entry_bucle_inside.start_listening()

    def __card_detected_impl(self, card_id, booster_id):
        """
        Check that card_id is authorized to enter within entry_barrier to the test_facility.
        If the card_id is authorized, the next state is EntryBarrierOpenedState; else the next state is
        EntryInitialState
        :param card_id:
        :return:
        """
        if not card_id or not booster_id:
            return
        next_state = {"action_type": "authorization"}
        auth_dao = AuthorizedDAO()
        if auth_dao.is_tag_authorized(booster_id):
            self.context.data = {"tag_id": card_id, "booster_id": booster_id}
            next_state["action"] = "success"
        else:
            next_state["action"] = "rejected"

        self.do_action(**next_state)

    @StateDoActionWrapper.check_args
    def do_action(self, *args, **kwargs):
        action_type, action = kwargs['action_type'], kwargs['action']

        if action_type == "emergency":
            if action == "on":
                self.context.state = EntryEmergencyState(self.context)

        elif action_type == "barriers":
            if action == "open":
                self.context.state = EntryBarrierOpenedState(self.context)
            elif action == "lock":
                self.context.barrier.lock()
                # TODO: Pending to define the status workflow at this point
            elif action == "unlock":
                self.context.barrier.unlock()
                # TODO: Pending to define the status workflow at this point

        elif action_type == "antenna":
            if action == "card_detected":
                card = kwargs['card_number']
                booster = kwargs['booster_id']
                self.__card_detected_impl(card, booster)

        elif action_type == "authorization":
            if action == "success":
                if not self.context.barrier.is_locked():
                    self.context.state = EntryBarrierOpenedState(self.context)
            elif action == "rejected":
                self.context.state = self


class EntryBarrierOpenedState(GenericState):
    """
    State ID = 1

    State Name = "BARRIER_OPENED"

    output=\n
    * barrier : {opened:true, locked: xxx}
    * antennaNFC: off

    Destination states =\n
     * EntryEmergencyState
     * EntryInitialState
    """

    def __init__(self, context):
        super().__init__(context)
        self.__perform_state()

    def __perform_state(self):
        self.context.barrier.open()

    def __register_access(self):
        if self.context.data is not None:
            #FIXME: Change {barrier_id} value and the {result} column name
            pass_obj = {"tag_id": self.context.data["tag_id"],
                        "booster_id": self.context.data["booster_id"],
                        "pass_time": datetime.datetime.now(),
                        "barrier_id": self.context.barrier.gpiopin,
                        "pass_type": True}
            pass_dao = PassDAO()
            pass_dao.create(**pass_obj)
            self.context.data = None

    @StateDoActionWrapper.check_args
    def do_action(self, *args, **kwargs):
        action_type, action = kwargs['action_type'], kwargs['action']

        if action_type == "emergency":
            if action == "on":
                self.context.state = EntryEmergencyState(self.context)

        elif action_type == "barriers":
            if action == "close":
                self.context.state = EntryInitialState(self.context)
            elif action == "lock":
                self.context.barrier.lock()
            elif action == "unlock":
                self.context.barrier.unlock()

        elif action_type == "bucle":
            if action == "edge_falling":
                self.__register_access()
                self.context.state = EntryInitialState(self.context)


class EntryEmergencyState(GenericState):
    """
    State ID = 3

    State Name = "EMERGENCY"

    This status is the most important. This status indicates that we are in emergency status. The only way
    to go to other status is receiving the emergency:off event.

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
        self.context.antenna.stop_to_listen()
        self.context.barrier.lock()
        self.context.barrier.open()

    @StateDoActionWrapper.check_args
    def do_action(self, *args, **kwargs):
        action_type, action = kwargs['action_type'], kwargs['action']

        if action_type != "emergency":
            return

        if action == 'off':
            self.context.state = EntryInitialState(self.context)


class EntryReadCardState(GenericState):
    """
     State ID = 4 \n
     State Name = "READ_CARD"\n
     output=
     barrier : {opened:false, locked: xxx}
     antennaNFC : on
     This status have a timeout of 30 seconds which it will keep reading cards ID.
     If any card is not read return to :class:`EntryInitialState`   \n

     Destination states = \n
     * EntryInitialState
     * EntryBarrierOpenedState
     """
    #FIXME: This class must be deleted

    def __init__(self, context):
        super().__init__(context)
        self.__perform_state()

    def __perform_state(self):
        self.context.antenna.start_read_card()

    def __card_detected_impl(self, card_id):
        """
        Check that card_id is authorized to enter within entry_barrier to the test_facility.
        If the card_id is authorized, the next state is EntryBarrierOpenedState; else the next state is
        EntryInitialState
        :param card_id:
        :return:
        """
        if not card_id:
            return
        import datetime
        next_state = {"action_type": "authorization"}
        pass_obj = {"tag_id": card_id, "pass_time": datetime.datetime.now(), "barrier_id": self.context.barrier.gpiopin}
        auth_dao = AuthorizedDAO()
        if auth_dao.is_tag_authorized(card_id):
            pass_obj["result"] = True
            next_state["action"] = "success"
            next_state["card_number"] = card_id
        else:
            pass_obj["result"] = False
            next_state["action"] = "rejected"
        pass_dao = PassDAO()
        pass_dao.create(**pass_obj)
        self.do_action(**next_state)

    @StateDoActionWrapper.check_args
    def do_action(self, *args, **kwargs):
        action_type, action = kwargs['action_type'], kwargs['action']

        if action_type == "emergency":
            if action == "on":
                self.context.state = EntryEmergencyState(self.context)

        elif action_type == "antenna":
            if action == "card_detected":
                card = kwargs['card_number']
                self.__card_detected_impl(card)

            elif action == "time_expired":
                app_logger(__name__).info(" NOT card detected")
                self.context.state = EntryInitialState(self.context)

        elif action_type == "authorization":
            if action == "success":
                card = kwargs['card_number']
                self.context.state = EntryBarrierOpenedState(self.context)

            elif action == "rejected":
                self.context.state = EntryInitialState(self.context)

