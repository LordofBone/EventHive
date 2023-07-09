import logging
import time

from template.custom_events import TestEvent, OtherTestEvent
from event_hive_runner import EventActor


class Consumer(EventActor):
    def __init__(self, event_queue):
        super().__init__(event_queue)

    def run(self):
        while True:
            logging.debug(f"{self.__class__.__name__} Consuming...")
            event_data = self.event_queue.get_latest_event([TestEvent, OtherTestEvent])
            if event_data is not None:  # check if event data is not None
                _, event = event_data
                if event.content == ["STOP"]:
                    break
                else:
                    logging.info(f"{self.__class__.__name__} Consumed: {event.content}")
            time.sleep(1)  # simulate some delay
        logging.info(f"{self.__class__.__name__} Consumer thread finished")
