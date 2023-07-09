# EventHive

EventHive is a priority-based, multithreaded event queue system in Python. It offers a robust solution for systems that handle different types of events, where certain events have higher priority over others. EventHive ensures that high-priority events are processed first and handles concurrent event producers and consumers in a thread-safe manner.

## Key Features

- **Priority-Based Queue:** Events with higher priority are processed first.
- **Multithreading Support:** EventHive allows for multiple event producers and consumers to operate concurrently.
- **Thread-Safety:** The queue is protected with locks to prevent race conditions.
- **Event Types:** Events are Python objects, so different event types can be easily created by subclassing the base `Event` class.

## Quick Start

There are a good number of examples under the templates directory. Additionally, the following is a quick start guide to get you up and running.

1. Clone and set up the repository with your project:

```sh
git clone https://github.com/LordofBone/EventHive
```

2. In your projects main code add the EventHive directory to your path:

```python
import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))

event_hive_dir = os.path.join(current_dir, '..', 'EventHive')

sys.path.append(event_hive_dir)
```

3. Create a custom event type by subclassing the `Event` class and making, for example, a custom_events.py:

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

4. Create a custom producer and consumer by subclassing ProducerTemplate and ConsumerTemplate, respectively, and override the necessary methods, for example:

```python
import logging
import time

from custom_events import PingTestEvent, ReturnTestEvent
from event_hive_runner import EventActor

class ConsumerProducer(EventActor):
    def __init__(self, event_queue):
        super().__init__(event_queue)

    def run(self):
        while True:
            logging.debug(f"{self.__class__.__name__} Consuming...")
            event_data = self.event_queue.get_latest_event([PingTestEvent])
            if event_data is not None:
                _, event = event_data
                if event.content == ["RECEIVED"]:
                    logging.info(f"{self.__class__.__name__} Consumed: {event.content}")
                    return_event = ReturnTestEvent(["FINISHED"], 3)
                    self.event_queue.queue_addition(return_event)
                    logging.info(f"{self.__class__.__name__} Produced: {return_event.content}")
                    break
                elif event.content == ["PING"]:
                    logging.info(f"{self.__class__.__name__} Consumed: {event.content}")
                    return_event = ReturnTestEvent(["RETURN_TEST_CONTENT"], 1)
                    logging.info(f"{self.__class__.__name__} Produced: {return_event.content}")
                    self.event_queue.queue_addition(return_event)
            time.sleep(1)  # simulate some delay
        logging.info(f"{self.__class__.__name__} Consumer thread finished")
```

You can add your own logic within this method to handle the event data. In this example, the consumer checks if the event content is `["RECEIVED"]` or `["PING"]` and produces a `ReturnTestEvent` with the appropriate content, but this of course can be changed to do whatever you want.

Functions can either be producers, consumers or both and can communicate with each other by adding and getting events from the event queue.

5. Initialize the event queue, and start your producers and consumers; multiple separate queues can also be setup:

```python
from consumer_producer import ConsumerProducer
from event_hive_runner import EventQueue

event_queue = EventQueue()
consumerproducer = ConsumerProducer(event_queue)

consumerproducer.start()
```

## Testing
Unit tests are provided in tests and can be run using a test runner like pytest.

Each test can be run individually, for example:

```python tests/test_event_hive.py```
```python tests/test_multi_threading.py```
```python tests/test_integration.py```

or the entire test suite can be run:

```python test_suite.py```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.