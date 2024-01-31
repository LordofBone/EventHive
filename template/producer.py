import logging
import time

from event_hive_runner import EventActor
from template.custom_events import TestEvent, OtherTestEvent, PingTestEvent

logger = logging.getLogger(__name__)


class Producer(EventActor):
    def __init__(self, event_queue):
        super().__init__(event_queue)
        self.max_loop = 10
        self.loop_count = 0

        logger.debug(f"{self.__class__.__name__} Initialized")

    def get_event_handlers(self):
        # No event handlers for the Producer since it's not supposed to consume any events.
        return {}

    def get_consumable_events(self):
        # No consumable events for the Producer since it's not supposed to consume any events.
        return []

    def run(self):
        """
        This method is called when the thread is started.
        :return:
        """
        while self.loop_count < self.max_loop and self.is_running:
            logger.debug(f"{self.__class__.__name__} Producing...")
            if self.loop_count == 1:
                event = OtherTestEvent(["TEST_CONTENT"], 2)
            elif self.loop_count == 4:
                event = PingTestEvent(["PING"], 1)
            elif self.loop_count == 5:
                event = PingTestEvent(["PING", "FINAL PING"], 1)
            elif self.loop_count == self.max_loop - 1:
                event = TestEvent(["STOP"], 3)
            else:
                event = TestEvent(["TEST_CONTENT"], 2)
            if event is not None:
                self.produce_event(event)
            self.loop_count += 1
            # simulate some delay, seems to be at least 2 seconds or the queue can't keep up (some sort of race
            # condition?) todo: investigate
            time.sleep(2)
        logger.info(f"{self.__class__.__name__} Producer thread finished")
