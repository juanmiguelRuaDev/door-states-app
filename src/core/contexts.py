from src.core.observer import Observer
from src.core.states.entry import EntryInitialState
from src.core.states.exit import ExitInitialState
from src.model.barrier import Barrier
from src.model.bucle import Bucle
from src.model.antenna import AntennaUSB


class EntryContext(Observer):
    """
    This class will be the glue in all states for entry barrier. This class is the
    context shared by every defined states and at the same time, will be an
    observer that will remain listening for any change detected in all
    Observable objects
    TODO: method ex: open_barrier, close_barrier,
    """

    def __init__(self, observable_list=[], config=None):
        super().__init__(observable_list)
        self.__init_peripherals()
        self.config = config
        self.state = EntryInitialState(self)
        self.data = None

    def __init_peripherals(self):
        # Defining barrier and registering the observer
        self.barrier = Barrier.new_entry_barrier('entry')
        self.barrier.register_observer(self)
        # Defining the bucle inside and registering the observer
        self.entry_bucle_inside = Bucle.new_entry_bucle_inside("entry_inside")
        self.entry_bucle_inside.register_observer(self)
        # Defining the antenna  and registering the observer
        self.antenna = AntennaUSB.new_entry_instance()
        self.antenna.register_observer(self)

    def perform_action(self,  **kwargs):
        self.state.do_action(**kwargs)

    def notify(self, observable, *args, **kwargs):
        self.state.do_action(**kwargs)


class ExitContext(Observer):
    """
    This is the context to handle the exit states. In function of the current state, the actions to do could be
     different between each other.
    """

    def __init__(self, observable_list=[], config=None):
        super().__init__(observable_list)
        self.__init_peripherals()
        self.config = config
        self.state = ExitInitialState(self)
        self.data = None

    def __init_peripherals(self):
        # Defining barrier and registering the observer
        self.barrier = Barrier.new_exit_barrier('exit')
        self.barrier.register_observer(self)
        # Defining the outside bucle and registering the observer
        self.exit_bucle_outside = Bucle.new_exit_bucle_outside("exit_outside")
        self.exit_bucle_outside.register_observer(self)
        # Defining the antenna and registering the observer
        self.antenna = AntennaUSB.new_exit_instance()
        self.antenna.register_observer(self)

    def perform_action(self, **kwargs):
        self.state.do_action(**kwargs)

    def notify(self, observable, *args, **kwargs):
        self.state.do_action(**kwargs)
