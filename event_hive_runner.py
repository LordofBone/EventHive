import heapq
import logging
import queue
import threading
from abc import ABC, abstractmethod
from enum import Enum

logger = logging.getLogger(__name__)
logger.debug("Initialized")


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

    def is_event_queue_empty(self):
        with self.queue_lock:
            return len(self.priority_queue) == 0


class EventActor(ABC, threading.Thread):
    def __init__(self, event_queue: EventQueue, sleep_time=0):
        super().__init__()
        self.event_queue = event_queue
        self.is_running = True
        self.sleep_time = sleep_time

    @abstractmethod
    def get_event_handlers(self):
        """
        Returns a dictionary mapping the event content to the corresponding event handler.
        """
        pass

    @abstractmethod
    def get_consumable_events(self):
        """
        Returns a list of events that this actor can consume.
        """
        pass

    def produce_event(self, event):
        self.event_queue.queue_addition(event)
        logger.debug(f"{self.__class__.__name__} Produced: {event.content}")

    def run(self):
        event_handlers = self.get_event_handlers()
        continue_loop = True
        while continue_loop:
            event_data = self.event_queue.get_latest_event(self.get_consumable_events())
            if event_data is not None:
                _, event = event_data
                handler = event_handlers.get(event.content[0])
                if handler:
                    continue_loop = handler(*event.content)
                    logger.debug(f"{self.__class__.__name__} Consumed: {event.content}")
                else:
                    logger.warning(f"{self.__class__.__name__} Received unknown event: {event}")
        logger.debug(f"{self.__class__.__name__} Consumer thread finished")
