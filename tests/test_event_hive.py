import unittest

from event_hive_runner import Event, EventQueue, VisionDetectEvent, MovementEvent


class TestEventQueue(unittest.TestCase):
    def setUp(self):
        self.event_queue = EventQueue()
        self.event_queue_1 = EventQueue()
        self.event_queue_2 = EventQueue()

    def test_add_and_get(self):
        event = VisionDetectEvent("TEST_CONTENT", 1)
        self.event_queue.queue_addition(event)

        ret_priority, ret_event = self.event_queue.get_latest_event([VisionDetectEvent])
        self.assertEqual(ret_event.content, event.content)
        self.assertEqual(ret_priority, event.priority)

    def test_get_empty(self):
        event = self.event_queue.get_latest_event([VisionDetectEvent])
        self.assertIsNone(event)

    def test_ordering(self):
        event1 = VisionDetectEvent("TEST_CONTENT 1", 1)
        event2 = VisionDetectEvent("TEST_CONTENT 2", 2)
        event3 = VisionDetectEvent("TEST_CONTENT 3", 3)

        self.event_queue.queue_addition(event3)
        self.event_queue.queue_addition(event2)
        self.event_queue.queue_addition(event1)

        ret_priority1, ret_event1 = self.event_queue.get_latest_event([VisionDetectEvent])
        ret_priority2, ret_event2 = self.event_queue.get_latest_event([VisionDetectEvent])
        ret_priority3, ret_event3 = self.event_queue.get_latest_event([VisionDetectEvent])

        self.assertEqual(ret_event1.content, event1.content)
        self.assertEqual(ret_priority1, event1.priority)
        self.assertEqual(ret_event2.content, event2.content)
        self.assertEqual(ret_priority2, event2.priority)
        self.assertEqual(ret_event3.content, event3.content)
        self.assertEqual(ret_priority3, event3.priority)

    def test_separate_queues(self):
        event1 = VisionDetectEvent("TEST_CONTENT 1", 1)
        event2 = MovementEvent("TEST_CONTENT 2", 2)

        self.event_queue_1.queue_addition(event1)
        self.event_queue_2.queue_addition(event2)

        ret_priority1, ret_event1 = self.event_queue_1.get_latest_event([VisionDetectEvent])
        ret_priority2, ret_event2 = self.event_queue_2.get_latest_event([MovementEvent])

        self.assertEqual(ret_event1.content, event1.content)
        self.assertEqual(ret_priority1, event1.priority)
        self.assertEqual(ret_event2.content, event2.content)
        self.assertEqual(ret_priority2, event2.priority)

        ret_event1 = self.event_queue_1.get_latest_event([MovementEvent])
        ret_event2 = self.event_queue_2.get_latest_event([VisionDetectEvent])

        self.assertIsNone(ret_event1)
        self.assertIsNone(ret_event2)

    def test_custom_event(self):
        class CustomEvent(Event):
            def __init__(self, content, priority):
                super().__init__("CUSTOM", content, priority)

            def get_event_type(self):
                return "CUSTOM"

        custom_event = CustomEvent("TEST_CONTENT", 1)
        self.event_queue.queue_addition(custom_event)

        ret_priority, ret_event = self.event_queue.get_latest_event([CustomEvent])
        self.assertEqual(ret_event.content, custom_event.content)
        self.assertEqual(ret_priority, custom_event.priority)


if __name__ == '__main__':
    unittest.main()
