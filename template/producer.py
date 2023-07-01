import threading
import time

from custom_events import TestEvent, OtherTestEvent, PingTestEvent


class Producer(threading.Thread):
    def __init__(self, event_queue):
        threading.Thread.__init__(self)
        self.event_queue = event_queue
        self.max_loop = 10

    def run(self):
        for i in range(self.max_loop):
            if i == 1:
                event = OtherTestEvent(["OTHER_TEST_CONTENT"], 2)
            elif i == 4:
                event = PingTestEvent(["RECEIVED"], 1)
            elif i == self.max_loop - 1:
                event = TestEvent(["STOP"], 3)
            else:
                event = TestEvent(["TEST_CONTENT"], 2)
            self.event_queue.queue_addition(event)
            print(f"{__class__} Produced: ", event.content)
            time.sleep(1)  # simulate some delay
