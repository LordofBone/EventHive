# EventHive

EventHive is a priority-based, multithreaded event queue system in Python. It offers a robust solution for systems that
handle different types of events, where certain events have higher priority over others. EventHive ensures that
high-priority events are processed first and handles concurrent event producers and consumers in a thread-safe manner.

## Key Features

- **Priority-Based Queue:** Events with higher priority are processed first.
- **Multithreading Support:** EventHive allows for multiple event producers and consumers to operate concurrently.
- **Thread-Safety:** The queue is protected with locks to prevent race conditions.
- **Event Types:** Events are Python objects, so different event types can be easily created by subclassing the
  base `Event` class.

## Quick Start

There are a good number of examples under the templates directory. Additionally, the following is a quick start guide to
get you up and running.

1. Clone and set up the repository with your project:

```sh
git clone https://github.com/LordofBone/EventHive
```

2. Create a custom event type by subclassing the `Event` class and making, for example, a custom_events.py:

```python
from event_hive_runner import Event


class PingTestEvent(Event):
    def __init__(self, content, priority):
        super().__init__("PingTestEvent", content, priority)

    def get_event_type(self):
        return self.__class__


class ReturnTestEvent(Event):
    def __init__(self, content, priority):
        super().__init__("ReturnTestEvent", content, priority)

    def get_event_type(self):
        return self.__class__
```

3. Create a custom producer to kick off events by subclassing EventActor and overriding run, for example:

```python
import time

from event_hive_runner import EventActor
from template.custom_events import TestEvent, PingTestEvent


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
        while self.loop_count < self.max_loop and self.is_running:
            if self.loop_count == self.max_loop - 1:
                event = TestEvent(["STOP"], 3)
            elif self.loop_count == 2:
                event = PingTestEvent(["PING"], 1)
            else:
                event = PingTestEvent(["PING", "THIS IS A PING"], 1)
            if event is not None:
                self.produce_event(event)
            self.loop_count += 1
            time.sleep(2)
```

You can also see here that you can also add in extra data into the event content, which can be used by the consumer.

4. Create a custom producer and consumer by subclassing EventActor and override the necessary methods, for example:

```python
from event_hive_runner import EventActor
from template.custom_events import PingTestEvent, ReturnTestEvent


class ConsumerProducer(EventActor):
    def handle_received(self, event_type=None, event_data=None):
        self.produce_event(ReturnTestEvent(["FINISHED"], 3))
        return False  # Signal to break the loop

    def handle_ping(self, event_type=None, event_data=None):
        # can add additional data into the event and use it
        print(event_type)
        if event_data == "THIS IS A PING":
            print("This was a ping with extra data")
        self.produce_event(ReturnTestEvent(["RETURN_TEST_CONTENT"], 1))
        return True  # Continue the loop

    def get_event_handlers(self):
        return {
            "STOP": self.handle_received,
            "PING": self.handle_ping,
        }

    def get_consumable_events(self):
        return [PingTestEvent]
```

You can add your own logic within this method to handle the event data. In this example, the consumer checks if the
event content is `["RECEIVED"]` or `["PING"]` and produces a `ReturnTestEvent` with the appropriate content, but this of
course can be changed to do whatever you want.

You can also see how the producer can add in extra data into the event content, which can be used by the consumer;
so you could add in extra information for the function, such as a generate TTS function requiring text to convert.

Adding in event_type=None, event_data=None, allows an event without additional data to be passed in as well.

Functions can either be producers, consumers or both and can communicate with each other by adding and getting events
from the event queue.

5. Initialize the event queue, and start your producers and consumers; multiple separate queues can also be setup:

```python
from consumer_producer import ConsumerProducer
from producer import Producer
from event_hive_runner import EventQueue

event_queue = EventQueue()
producer = Producer(event_queue)
consumerproducer = ConsumerProducer(event_queue)

consumerproducer.start()
```

You can also call a shutdown on consumers and producers to stop them from running:

```consumerproducer.shutdown()```

## Testing

Unit tests are provided in tests and can be run using a test runner like pytest.

Each test can be run individually, for example:

```python tests/test_event_hive.py```
```python tests/test_multi_threading.py```
```python tests/test_integration.py```

or the entire test suite can be run:

```python test_suite.py```

Tests can be added and will be automatically picked up by the test runner. They just need to begin with 'test_', for
example:

```tests/test_new_event.py```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.