import logging
import time

from consumer import Consumer
from consumer_producer import ConsumerProducer
from consumer_producer_2 import ConsumerProducer2
from event_hive_runner import EventQueue
from producer import Producer

# Configure logging level
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    logging.debug("Starting event hive runner")
    event_queue = EventQueue()

    logging.debug("Starting producer and consumer threads")
    producer_process = Producer(event_queue)
    consumer_process = Consumer(event_queue)
    producer_consumer_process = ConsumerProducer(event_queue)
    producer_consumer_process_2 = ConsumerProducer2(event_queue)

    producer_process.start()
    consumer_process.start()
    producer_consumer_process.start()
    producer_consumer_process_2.start()

    logging.debug("Waiting for threads to finish")
    producer_process.join()
    consumer_process.join()
    producer_consumer_process.join()
    producer_consumer_process_2.join()

    # Allow some time for consumer to process all events
    time.sleep(1)
