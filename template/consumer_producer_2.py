import threading
import time

from custom_events import ReturnTestEvent, PingTestEvent


class ConsumerProducer2(threading.Thread):
    def __init__(self, event_queue):
        threading.Thread.__init__(self)
        self.event_queue = event_queue

    def run(self):
        while True:
            event_data = self.event_queue.get_latest_event([ReturnTestEvent])
            if event_data is not None:  # check if event data is not None
                _, event = event_data
                if event.content == ["FINISHED"]:
                    print(f"{__class__} Consumed: ", event.content)
                    break
                else:
                    print(f"{__class__} Consumed: ", event.content)
                    return_event = PingTestEvent(["RECEIVED"], 1)
                    self.event_queue.queue_addition(return_event)
            time.sleep(1)  # simulate some delay
        print(f"{__class__} Consumer thread finished")
