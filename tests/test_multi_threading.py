import time
import unittest

from event_hive_runner import EventQueue, VisionDetectEvent, EventActor


class TestMultithreadAccess(unittest.TestCase):
    """
    Test that the event queue can be accessed by multiple threads without any issues
    """

    def setUp(self):
        self.event_queue = EventQueue()
        self.producer = Producer(self.event_queue)
        self.consumer = Consumer(self.event_queue)

        self.producer1 = Producer(self.event_queue)
        self.producer2 = Producer(self.event_queue)

    def test_multithread_access(self):
        """
        Test that the event queue can be accessed by multiple threads
        :return:
        """
        # Start the threads
        self.producer.start()
        self.consumer.start()

        # Wait for them to finish
        self.producer.join()
        self.consumer.join()

        # Allow some time for consumer to process all events
        time.sleep(1)

        # Check that all events have been consumed
        self.assertEqual(len(self.event_queue.priority_queue), 0)

    def test_multithread_access_2(self):
        """
        Test that the event queue can be accessed by multiple threads
        :return:
        """
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
        self.assertEqual(len(self.event_queue.priority_queue), 0)


class Producer(EventActor):
    """
    Producer thread that adds events to the event queue
    """

    def __init__(self, event_queue):
        super().__init__(event_queue)

    def run(self):
        """
        Add 10 events to the event queue
        :return:
        """
        for i in range(10):
            event = VisionDetectEvent("TEST_CONTENT", i)
            self.event_queue.queue_addition(event)


class Consumer(EventActor):
    """
    Consumer thread that consumes events from the event queue
    """

    def __init__(self, event_queue):
        super().__init__(event_queue)

    def run(self):
        """
        Consume all events from the event queue
        :return:
        """
        while True:
            event = self.event_queue.get_latest_event([VisionDetectEvent])
            if event is None:
                break
            else:
                _, event = event


if __name__ == '__main__':
    unittest.main()
