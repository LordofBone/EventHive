import threading
import time

from custom_events import ReturnTestEvent, PingTestEvent


class ConsumerProducer(threading.Thread):
    def __init__(self, event_queue):
        threading.Thread.__init__(self)
        self.event_queue = event_queue

    def run(self):
        while True:
            event_data = self.event_queue.get_latest_event([PingTestEvent])
            if event_data is not None:  # check if event data is not None
                _, event = event_data
                if event.content == ["RECEIVED"]:
                    print(f"{__class__} Consumed: ", event.content)
                    return_event = ReturnTestEvent(["FINISHED"], 3)
                    self.event_queue.queue_addition(return_event)
                    break
                else:
                    print(f"{__class__} Consumed: ", event.content)
                    return_event = ReturnTestEvent(["RETURN_TEST_CONTENT"], 1)
                    self.event_queue.queue_addition(return_event)
            time.sleep(1)  # simulate some delay
        print(f"{__class__} Consumer thread finished")
