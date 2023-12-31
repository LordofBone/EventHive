from event_hive_runner import EventActor
from template.custom_events import TestEvent, OtherTestEvent


class Consumer(EventActor):
    def handle_stop(self, event_type=None, event_data=None):
        """
        This method is called when the event type is "STOP"
        :param event_data:
        :param event_type:
        :return:
        """
        return False  # Signal to break the loop

    def handle_other(self, event_type=None, event_data=None):
        """
        This method is called when the event type is "OTHER_TEST_EVENT"
        :param event_data:
        :param event_type:
        :return:
        """
        return True  # Continue the loop

    def get_event_handlers(self):
        """
        This method returns a dictionary of event handlers.
        :return:
        """
        return {
            "STOP": self.handle_stop,
            "TEST_CONTENT": self.handle_other
        }

    def get_consumable_events(self):
        """
        This method returns a list of event types that this consumer can consume.
        :return:
        """
        return [TestEvent, OtherTestEvent]
