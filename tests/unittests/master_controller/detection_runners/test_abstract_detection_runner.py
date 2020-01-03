import time
from collections import Callable
from typing import List
from unittest import TestCase
from unittest.mock import MagicMock

from master_controller.detection_runners.abstract_detection_runner import \
    AbstractDetectionRunner


class AbstractDetectionRunnerImplementation(AbstractDetectionRunner):  \
        # pragma: no cover
    def __init__(self):
        super(AbstractDetectionRunnerImplementation, self).__init__()

    def process_image(self):
        pass

    def init_detection_caller(self, process_function: Callable,
                              arguments: List):
        pass


class TestAbstractDetectionRunner(TestCase):
    def setUp(self) -> None:
        self.detection_runner = AbstractDetectionRunnerImplementation()

    def test_init(self):
        self.assertIsNone(self.detection_runner.image)
        self.assertFalse(self.detection_runner.processing)
        self.assertEqual(0., self.detection_runner.last_detection_time)
        self.assertIsNone(self.detection_runner.detection_caller)

    def test_update_image(self):
        # given
        image = 'image'

        # when
        self.detection_runner.update_image(image)

        # then
        self.assertEqual(image, self.detection_runner.image)

    def test_update_detection_True(self):
        # given
        detection = True
        self.detection_runner.processing = True

        # when
        self.detection_runner.update_detection_result(detection)

        # then
        self.assertFalse(self.detection_runner.processing)
        self.assertAlmostEqual(time.time(),
                               self.detection_runner.last_detection_time,
                               places=3)

    def test_update_detection_False(self):
        # given
        detection = False
        self.detection_runner.processing = True

        # when
        self.detection_runner.update_detection_result(detection)

        # then
        self.assertFalse(self.detection_runner.processing)
        self.assertNotAlmostEqual(time.time(),
                                  self.detection_runner.last_detection_time,
                                  places=3)

    def test_start_detection(self):
        # given
        self.detection_runner.init_detection_caller = MagicMock()
        self.detection_runner.detection_caller = MagicMock()
        self.detection_runner.detection_caller.start = MagicMock()
        some_function = MagicMock()

        # when
        self.detection_runner.start_detection(some_function, [1])

        # then
        self.assertTrue(self.detection_runner.processing)
        self.detection_runner.init_detection_caller.assert_called_with(
            some_function, [1])
        self.detection_runner.detection_caller.start.assert_called()
