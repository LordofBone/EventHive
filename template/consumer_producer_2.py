from event_hive_runner import EventActor, consumer_logger
from template.custom_events import PingTestEvent, ReturnTestEvent


class ConsumerProducer2(EventActor):
    @consumer_logger
    def handle_finished(self, event):
        """
        This method is called when the event type is "FINISHED"
        :return:
        """
        return False  # Signal to break the loop

    @consumer_logger
    def handle_return_test_content(self, event):
        """
        This method is called when the event type is "RETURN_TEST_CONTENT"
        :return:
        """
        self.produce_event(PingTestEvent(["RECEIVED"], 1))
        return True  # Continue the loop

    def get_event_handlers(self):
        """
        This method returns a dictionary of event handlers.
        :return:
        """
        return {
            ("FINISHED",): self.handle_finished,
            ("RETURN_TEST_CONTENT",): self.handle_return_test_content,
        }

    def get_consumable_events(self):
        """
        This method returns a list of event types that this consumer can consume.
        :return:
        """
        return [ReturnTestEvent]
