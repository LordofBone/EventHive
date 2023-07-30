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
        logging.basicConfig(level=logging.DEBUG, handlers=[self.handler])

    def tearDown(self):
        logging.getLogger().removeHandler(self.handler)

    def test_multi_module_integration(self):
        """
        Run the main function and check that all expected log messages appear; meaning that all modules worked
        through the queues and communicated with each other successfully :return:
        """
        main()

        expected_logs = [
            "DEBUG:root:Producer Produced: ['TEST_CONTENT']",
            "DEBUG:root:Consumer Consumed: ['TEST_CONTENT']",
            "DEBUG:root:Producer Produced: ['PING']",
            "DEBUG:root:ConsumerProducer Consumed: ['PING']",
            "DEBUG:root:Producer Produced: ['PING', 'FINAL PING']",
            "DEBUG:root:ConsumerProducer Consumed: ['PING', 'FINAL PING']",
            "DEBUG:root:ConsumerProducer Produced: ['RETURN_TEST_CONTENT']",
            "DEBUG:root:ConsumerProducer2 Consumed: ['RETURN_TEST_CONTENT']",
            "DEBUG:root:ConsumerProducer2 Produced: ['RECEIVED']",
            "DEBUG:root:ConsumerProducer Consumed: ['RECEIVED']",
            "DEBUG:root:ConsumerProducer Produced: ['FINISHED']",
            "DEBUG:root:ConsumerProducer Consumer thread finished",
            "DEBUG:root:ConsumerProducer2 Consumed: ['FINISHED']",
            "DEBUG:root:ConsumerProducer2 Consumer thread finished",
            "DEBUG:root:Producer Produced: ['STOP']",
            "DEBUG:root:Consumer Consumer thread finished",
        ]

        # Check that each expected log message appears at least once
        for expected_log in expected_logs:
            with self.subTest(expected_log=expected_log):
                self.assertTrue(any(expected_log in actual_log for actual_log in self.log_list))


if __name__ == '__main__':
    unittest.main()
