import queue
import threading
from abc import ABC, abstractmethod
from enum import Enum


class EventType(Enum):
    """
    Enum class for event types
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
        self.priority_queue = queue.PriorityQueue()
        self.temp_queue = queue.PriorityQueue()
        self.tiebreaker = 0

    def queue_addition(self, event):
        """
        Adds an event to the queue
        :param event:
        :return:
        """
        with self.queue_lock:
            self.priority_queue.put((event.priority, self.tiebreaker, event))
            self.tiebreaker += 1

    def get_latest_event(self, event_types):
        """
        Gets the latest event from the queue
        :param event_types:
        :return:
        """
        with self.queue_lock:
            try:
                priority, timestamp, event = self.priority_queue.get_nowait()
                while not isinstance(event, tuple(event_types)):
                    self.temp_queue.put((priority, timestamp, event))
                    priority, timestamp, event = self.priority_queue.get_nowait()
                while not self.temp_queue.empty():
                    self.priority_queue.put(self.temp_queue.get())
                return priority, event
            except queue.Empty:
                return None
