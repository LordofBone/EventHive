import logging
import time

from template.custom_events import PingTestEvent, ReturnTestEvent
from event_hive_runner import EventActor


class ConsumerProducer(EventActor):
    def __init__(self, event_queue):
        super().__init__(event_queue)

    def run(self):
        while True:
            logging.debug(f"{self.__class__.__name__} Consuming...")
            event_data = self.event_queue.get_latest_event([PingTestEvent])
            if event_data is not None:  # check if event data is not None
                _, event = event_data
                if event.content == ["RECEIVED"]:
                    logging.info(f"{self.__class__.__name__} Consumed: {event.content}")
                    return_event = ReturnTestEvent(["FINISHED"], 3)
                    self.event_queue.queue_addition(return_event)
                    logging.info(f"{self.__class__.__name__} Produced: {return_event.content}")
                    break
                elif event.content == ["PING"]:
                    logging.info(f"{self.__class__.__name__} Consumed: {event.content}")
                    return_event = ReturnTestEvent(["RETURN_TEST_CONTENT"], 1)
                    logging.info(f"{self.__class__.__name__} Produced: {return_event.content}")
                    self.event_queue.queue_addition(return_event)
            time.sleep(1)  # simulate some delay
        logging.info(f"{self.__class__.__name__} Consumer thread finished")
