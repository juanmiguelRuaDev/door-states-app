from src.core.observer import Observer
from src.core.states.entry import EntryInitialState
from src.core.states.exit import ExitInitialState
from src.model.door import Door


class EntryContext(Observer):
    """
    This class is the glue among all entry-door states. This class is the
    context shared by every defined state, similarly, It is an
    observer that remains listening for any change detected in all
    Observable objects
    """

    def __init__(self, observable_list=[], config=None):
        super().__init__(observable_list)
        self.__init_peripherals()
        self.config = config
        self.state = EntryInitialState(self)
        self.data = None

    def __init_peripherals(self):
        # Defining barrier and registering the observer
        self.door = Door.new_entry_door('entry')
        self.door.register_observer(self)

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
        self.door = Door.new_exit_door('exit')
        self.door.register_observer(self)

    def perform_action(self, **kwargs):
        self.state.do_action(**kwargs)

    def notify(self, observable, *args, **kwargs):
        self.state.do_action(**kwargs)
