from event_hive_runner import EventActor, consumer_logger
from template.custom_events import TestEvent, OtherTestEvent


class Consumer(EventActor):
    @consumer_logger
    def handle_stop(self, event):
        """
        This method is called when the event type is "STOP"
        :return:
        """
        return False  # Signal to break the loop

    @consumer_logger
    def handle_other(self, event):
        """
        This method is called when the event type is "OTHER_TEST_EVENT"
        :return:
        """
        return True  # Continue the loop

    def get_event_handlers(self):
        """
        This method returns a dictionary of event handlers.
        :return:
        """
        return {
            ("STOP",): self.handle_stop,
            ("TEST_CONTENT",): self.handle_other
        }

    def get_consumable_events(self):
        """
        This method returns a list of event types that this consumer can consume.
        :return:
        """
        return [TestEvent, OtherTestEvent]
