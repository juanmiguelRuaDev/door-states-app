
class StateContext:
    def __init__(self):
        self.state = StateLowCase(self)

    def write_name(self, name):
        self.state.write_name(name)


class StateLike:

    def __init__(self, context):
        self.context = context

    def write_name(self, name):
        pass


class StateLowCase(StateLike):

    def __init__(self, context):
        super().__init__(context)

    def write_name(self, name):
        print(str(name).lower())
        self.context.state = StateMultipleUpperCase(self.context)


class StateMultipleUpperCase(StateLike):

    def __init__(self, context):
        super().__init__(context)
        self.count = 0

    def write_name(self, name):
        print(str(name).upper())
        self.count += 1
        if self.count > 1:
            self.context.state = StateLowCase(self.context)


if __name__ == "__main__":
    state_context = StateContext()
    state_context.write_name("Monday")
    state_context.write_name("Tuesday")
    state_context.write_name("Wednesday")
    state_context.write_name("Thursday")
    state_context.write_name("Friday")
    state_context.write_name("Saturday")
    state_context.write_name("Sunday")

