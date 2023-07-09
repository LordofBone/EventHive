import logging
import unittest

from template.runner import main


class ListHandler(logging.Handler):
    def __init__(self, log_list):
        super().__init__()
        self.log_list = log_list

    def emit(self, record):
        self.log_list.append(self.format(record))


class TestLogging(unittest.TestCase):
    def setUp(self):
        # Initialize list and handler
        self.log_list = []
        self.handler = ListHandler(self.log_list)

        # Configure logging level
        logging.basicConfig(level=logging.INFO, handlers=[self.handler])

    def tearDown(self):
        logging.getLogger().removeHandler(self.handler)

    def test_event_logging(self):
        # Run your main function here
        main()

        expected_logs = [
            "INFO:root:Producer Produced: ['TEST_CONTENT']",
            "INFO:root:Consumer Consumed: ['TEST_CONTENT']",
            "INFO:root:Producer Produced: ['PING']",
            "INFO:root:ConsumerProducer Consumed: ['PING']",
            "INFO:root:ConsumerProducer Produced: ['RETURN_TEST_CONTENT']",
            "INFO:root:ConsumerProducer2 Consumed: ['RETURN_TEST_CONTENT']",
            "INFO:root:ConsumerProducer2 Produced: ['RECEIVED']",
            "INFO:root:ConsumerProducer Consumed: ['RECEIVED']",
            "INFO:root:ConsumerProducer Produced: ['FINISHED']",
            "INFO:root:ConsumerProducer Consumer thread finished",
            "INFO:root:ConsumerProducer2 Consumed: ['FINISHED']",
            "INFO:root:ConsumerProducer2 Consumer thread finished",
            "INFO:root:Producer Produced: ['STOP']",
            "INFO:root:Consumer Consumer thread finished",
        ]

        # Check that each expected log message appears at least once
        for expected_log in expected_logs:
            with self.subTest(expected_log=expected_log):
                self.assertTrue(any(expected_log in actual_log for actual_log in self.log_list))


if __name__ == '__main__':
    unittest.main()
