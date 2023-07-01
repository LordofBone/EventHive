import threading
import time

from custom_events import TestEvent


class Consumer(threading.Thread):
    def __init__(self, event_queue):
        threading.Thread.__init__(self)
        self.event_queue = event_queue

    def run(self):
        while True:
            event_data = self.event_queue.get_latest_event([TestEvent])
            if event_data is not None:  # check if event data is not None
                _, event = event_data
                if event.content == ["STOP"]:
                    break
                else:
                    print(f"{__class__} Consumed: ", event.content)
            time.sleep(1)  # simulate some delay
        print(f"{__class__} Consumer thread finished")
