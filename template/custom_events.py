from event_hive_runner import Event


class TestEvent(Event):
    def __init__(self, content, priority):
        super().__init__("TEST_EVENT", content, priority)

    def get_event_type(self):
        return self.__class__


class OtherTestEvent(Event):
    def __init__(self, content, priority):
        super().__init__("OTHER_TEST_EVENT", content, priority)

    def get_event_type(self):
        return self.__class__


class ReturnTestEvent(Event):
    def __init__(self, content, priority):
        super().__init__("RETURN_TEST_EVENT", content, priority)

    def get_event_type(self):
        return self.__class__


class PingTestEvent(Event):
    def __init__(self, content, priority):
        super().__init__("PING_TEST_EVENT", content, priority)

    def get_event_type(self):
        return self.__class__
