import threading
import time
import unittest

from event_hive_runner import EventQueue, VisionDetectEvent


class TestMultithreadAccess(unittest.TestCase):
    def setUp(self):
        self.event_queue = EventQueue()
        self.producer = Producer(self.event_queue)
        self.consumer = Consumer(self.event_queue)

        self.producer1 = Producer(self.event_queue)
        self.producer2 = Producer(self.event_queue)

    def test_multithread_access(self):
        # Start the threads
        self.producer.start()
        self.consumer.start()

        # Wait for them to finish
        self.producer.join()
        self.consumer.join()

        # Allow some time for consumer to process all events
        time.sleep(1)

        # Check that all events have been consumed
        self.assertTrue(self.event_queue.priority_queue.empty())

    def test_multithread_access_2(self):
        # Start the threads
        self.producer1.start()
        self.producer2.start()
        self.consumer.start()

        # Wait for them to finish
        self.producer1.join()
        self.producer2.join()
        self.consumer.join()

        # Allow some time for consumer to process all events
        time.sleep(1)

        # Check that all events have been consumed
        self.assertTrue(self.event_queue.priority_queue.empty())


class Producer(threading.Thread):
    def __init__(self, event_queue):
        threading.Thread.__init__(self)
        self.event_queue = event_queue

    def run(self):
        for i in range(10):
            event = VisionDetectEvent("TEST_CONTENT", i)
            self.event_queue.queue_addition(event)


class Consumer(threading.Thread):
    def __init__(self, event_queue):
        threading.Thread.__init__(self)
        self.event_queue = event_queue

    def run(self):
        while True:
            event = self.event_queue.get_latest_event([VisionDetectEvent])
            if event is None:
                break
            else:
                _, event = event
