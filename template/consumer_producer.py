from event_hive_runner import EventActor, consumer_logger
from template.custom_events import PingTestEvent, ReturnTestEvent


class ConsumerProducer(EventActor):
    @consumer_logger
    def handle_received(self, event):
        """
        This method is called when the event type is "RECEIVED"
        :param event:
        :return:
        """
        self.produce_event(ReturnTestEvent(["FINISHED"], 3))
        return False  # Signal to break the loop

    @consumer_logger
    def handle_ping(self, event):
        """
        This method is called when the event type is "PING"
        :param event:
        :return:
        """
        self.produce_event(ReturnTestEvent(["RETURN_TEST_CONTENT"], 1))
        return True  # Continue the loop

    def get_event_handlers(self):
        """
        This method returns a dictionary of event handlers.
        :return:
        """
        return {
            ("RECEIVED",): self.handle_received,
            ("PING",): self.handle_ping,
        }

    def get_consumable_events(self):
        """
        This method returns a list of event types that this consumer can consume.
        :return:
        """
        return [PingTestEvent]
