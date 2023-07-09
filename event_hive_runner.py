import heapq
import queue
import threading
from abc import ABC, abstractmethod
from enum import Enum


class EventType(Enum):
    """
    Enum class for event types (examples included)
    """
    VISION_DETECT = 1
    MOVEMENT = 2


class Event(ABC):
    """
    Abstract class for events, allows creation of events by using this as a superclass
    """

    def __init__(self, event_type, content, priority):
        self.event_type = event_type
        self.content = content
        self.priority = priority

    @abstractmethod
    def get_event_type(self):
        pass


class VisionDetectEvent(Event):
    """
    Class for vision detect events (example)
    """

    def __init__(self, content, priority):
        super().__init__(EventType.VISION_DETECT, content, priority)

    def get_event_type(self):
        return self.event_type


class MovementEvent(Event):
    """
    Class for movement events (example)
    """

    def __init__(self, content, priority):
        super().__init__(EventType.MOVEMENT, content, priority)

    def get_event_type(self):
        return self.event_type


class EventQueue:
    def __init__(self):
        self.queue_lock = threading.Lock()
        self.priority_queue = list()  # ensure priority_queue is a list
        self.temp_queue = queue.PriorityQueue()
        self.tiebreaker = 0

    def queue_addition(self, event):
        with self.queue_lock:
            heapq.heappush(self.priority_queue, (event.priority, self.tiebreaker, event))
            self.tiebreaker += 1

    def get_latest_event(self, event_types):
        with self.queue_lock:
            if not self.priority_queue:
                return None
            priority, timestamp, event = self.priority_queue[0]  # peek at the first item
            while not isinstance(event, tuple(event_types)):
                if len(self.priority_queue) == 1:
                    # we have reached the end of the queue, so we return None
                    return None
                _, _, event = self.priority_queue[1]  # peek at the next item
                heapq.heapreplace(self.priority_queue, self.priority_queue[1])  # pop and push in one operation
            # the event at the head of the queue is of the desired type, so we pop it
            heapq.heappop(self.priority_queue)
            return priority, event


class EventActor(threading.Thread):
    def __init__(self, event_queue: EventQueue):
        super().__init__()
        self.event_queue = event_queue

    def run(self):
        raise NotImplementedError("You need to override the run method.")
