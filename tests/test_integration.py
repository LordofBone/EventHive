import logging
import unittest

from template.runner import main


class ListHandler(logging.Handler):
    def __init__(self, log_list):
        super().__init__()
        self.log_list = log_list

    def emit(self, record):
        """
        Append the log message to the list
        :param record:
        :return:
        """
        self.log_list.append(self.format(record))


class TestFullIntegration(unittest.TestCase):
    """
    Test that the event queue can be accessed by multiple threads and that all events are processed and that
    different modules can communicate with each other via the event queue
    """

    def setUp(self):
        """
        Set up the test by creating a list to store log messages in and adding a handler to the root logger
        :return:
        """
        self.log_list = []
        self.handler = ListHandler(self.log_list)

        log_level = "debug"

        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f'Invalid log level: {log_level}')

        # get root logger
        logger = logging.getLogger()

        # set level for the logger
        logger.setLevel(numeric_level)

        # create console handler with a specific level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(numeric_level)

        # add the handler to the logger
        logger.addHandler(console_handler)
        logger.addHandler(self.handler)

    def tearDown(self):
        logging.getLogger().removeHandler(self.handler)

    def test_multi_module_integration(self):
        """
        Run the main function and check that all expected log messages appear; meaning that all modules worked
        through the queues and communicated with each other successfully :return:
        """
        main()

        expected_logs = [
            "Starting event hive runner",
            "Starting producer and consumer threads",
            "Producer Producing...",
            "Producer Produced: ['TEST_CONTENT']",
            "Consumer Consumed: ['TEST_CONTENT']",
            "Waiting for threads to finish",
            "Producer Producing...",
            "Producer Produced: ['TEST_CONTENT']",
            "Consumer Consumed: ['TEST_CONTENT']",
            "Producer Producing...",
            "Producer Produced: ['TEST_CONTENT']",
            "Consumer Consumed: ['TEST_CONTENT']",
            "Producer Producing...",
            "Producer Produced: ['TEST_CONTENT']",
            "Consumer Consumed: ['TEST_CONTENT']",
            "Producer Producing...",
            "Producer Produced: ['PING']",
            "ConsumerProducer Consumed: ['PING']",
            "Producer Producing...",
            "Producer Produced: ['PING', 'FINAL PING']",
            "ConsumerProducer Produced: ['RETURN_TEST_CONTENT']",
            "ConsumerProducer Consumed: ['PING', 'FINAL PING']",
            "ConsumerProducer2 Produced: ['RECEIVED']",
            "ConsumerProducer2 Consumed: ['RETURN_TEST_CONTENT']",
            "ConsumerProducer Produced: ['FINISHED']",
            "ConsumerProducer2 Consumed: ['FINISHED']",
            "ConsumerProducer Consumed: ['RECEIVED']",
            "ConsumerProducer2 Consumer thread finished",
            "ConsumerProducer Consumer thread finished",
            "Producer Producing...",
            "Producer Produced: ['TEST_CONTENT']",
            "Consumer Consumed: ['TEST_CONTENT']",
            "Producer Producing...",
            "Producer Produced: ['TEST_CONTENT']",
            "Consumer Consumed: ['TEST_CONTENT']",
            "Producer Producing...",
            "Producer Produced: ['TEST_CONTENT']",
            "Consumer Consumed: ['TEST_CONTENT']",
            "Producer Producing...",
            "Producer Produced: ['STOP']",
            "Consumer Consumed: ['STOP']",
            "Consumer Consumer thread finished",
            "Producer Producer thread finished",
        ]

        print(self.log_list)

        # Check that each expected log message appears at least once
        for expected_log in expected_logs:
            with self.subTest(expected_log=expected_log):
                self.assertTrue(any(expected_log in actual_log for actual_log in self.log_list))


if __name__ == '__main__':
    unittest.main()
