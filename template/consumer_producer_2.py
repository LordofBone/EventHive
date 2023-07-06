import logging
import time

from custom_events import PingTestEvent, ReturnTestEvent
from event_hive_runner import EventActor


class ConsumerProducer2(EventActor):
    def __init__(self, event_queue):
        super().__init__(event_queue)

    def run(self):
        while True:
            logging.debug(f"{self.__class__.__name__} Consuming...")
            event_data = self.event_queue.get_latest_event([ReturnTestEvent])
            if event_data is not None:  # check if event data is not None
                _, event = event_data
                if event.content == ["FINISHED"]:
                    logging.info(f"{self.__class__.__name__} Consumed: {event.content}")
                    break
                elif event.content == ["RETURN_TEST_CONTENT"]:
                    logging.info(f"{self.__class__.__name__} Consumed: {event.content}")
                    return_event = PingTestEvent(["RECEIVED"], 1)
                    logging.info(f"{self.__class__.__name__} Produced: {return_event.content}")
                    self.event_queue.queue_addition(return_event)
            time.sleep(1)  # simulate some delay
        logging.info(f"{self.__class__.__name__} Consumer thread finished")
