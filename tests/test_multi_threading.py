import time
import unittest

from event_hive_runner import EventQueue, VisionDetectEvent, EventActor, consumer_logger


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

        self.consumer1 = Consumer(self.event_queue)
        self.consumer2 = Consumer(self.event_queue)

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
        self.consumer1.start()
        self.consumer2.start()

        # Wait for them to finish
        self.producer1.join()
        self.producer2.join()
        self.consumer1.join()
        self.consumer2.join()

        # Allow some time for consumer to process all events
        time.sleep(1)

        # Check that all events have been consumed
        self.assertEqual(len(self.event_queue.priority_queue), 0)


class Producer(EventActor):
    def __init__(self, event_queue):
        super().__init__(event_queue)
        self.max_loop = 10
        self.loop_count = 0

    def get_event_handlers(self):
        # No event handlers for the Producer since it's not supposed to consume any events.
        return {}

    def get_consumable_events(self):
        # No consumable events for the Producer since it's not supposed to consume any events.
        return []

    def run(self):
        """
        This method is called when the thread is started.
        :return:
        """
        while self.loop_count < self.max_loop:
            if self.loop_count == self.max_loop - 1:
                event = VisionDetectEvent(["EXIT"], 1)
            else:
                event = VisionDetectEvent(["TEST_CONTENT"], 2)
            if event is not None:
                self.produce_event(event)
            self.loop_count += 1
            time.sleep(2)  # simulate some delay, seems to be at least 2 seconds or the queue can't keep up


class Consumer(EventActor):
    """
    Consumer thread that consumes events from the event queue
    """

    @consumer_logger
    def handle_event(self, event):
        """
        Handle the event
        :param event:
        :return:
        """
        return True  # If the queue is not empty, continue the loop

    @consumer_logger
    def exit_event(self, event):
        """
        Handle the exit event, break the loop
        :param event:
        :return:
        """
        return False

    def get_event_handlers(self):
        """
        Return the event handlers
        :return:
        """
        return {
            ("TEST_CONTENT",): self.handle_event,
            ("EXIT",): self.exit_event
        }

    def get_consumable_events(self):
        """
        Return the consumable events
        :return:
        """
        return [VisionDetectEvent]


if __name__ == '__main__':
    unittest.main()
