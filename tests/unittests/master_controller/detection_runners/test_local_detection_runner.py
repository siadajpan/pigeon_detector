from unittest import TestCase
from unittest.mock import MagicMock, patch

import numpy as np

from detection.simple_detector import SimpleDetector
from master_controller.detection_runners.abstract_detection_runner import \
    AbstractDetectionRunner
from master_controller.detection_runners.detection_caller import DetectionCaller
from master_controller.detection_runners.local_detection_runner import \
    LocalDetectionRunner


class TestLocalDetecionRunner(TestCase):
    def setUp(self) -> None:
        self.local_runner = LocalDetectionRunner()

    def test_init(self):
        self.assertIsInstance(self.local_runner, AbstractDetectionRunner)
        self.assertIsInstance(self.local_runner.simple_detector, SimpleDetector)

    def test_init_detection_caller(self):
        # given

        # when
        result = self.local_runner._init_detection_caller([1, 2])

        # then
        self.assertIsInstance(result, DetectionCaller)

    @patch.object(AbstractDetectionRunner, 'send_image')
    def test_send_image(self, send_mock):
        # given
        caller = MagicMock()
        self.local_runner._init_detection_caller = MagicMock(
            return_value=caller)

        # when
        self.local_runner.send_image()

        # then
        send_mock.assert_called()
        caller.start.assert_called()
