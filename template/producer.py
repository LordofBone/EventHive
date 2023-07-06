import logging
import time

from custom_events import TestEvent, OtherTestEvent, PingTestEvent
from event_hive_runner import EventActor


class Producer(EventActor):
    def __init__(self, event_queue):
        super().__init__(event_queue)
        self.max_loop = 10

    def run(self):
        for i in range(self.max_loop):
            logging.debug(f"{self.__class__.__name__} Producing...")
            if i == 1:
                event = OtherTestEvent(["TEST_CONTENT"], 2)
            elif i == 4:
                event = PingTestEvent(["PING"], 1)
            elif i == self.max_loop - 1:
                event = TestEvent(["STOP"], 3)
            else:
                event = TestEvent(["TEST_CONTENT"], 2)
            if event is not None:
                self.event_queue.queue_addition(event)
                logging.info(f"{self.__class__.__name__} Produced: {event.content}")
            time.sleep(2)  # simulate some delay, seems to be at least 2 seconds or the queue can't keep up
