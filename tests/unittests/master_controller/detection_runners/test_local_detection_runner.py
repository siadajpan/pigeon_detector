from unittest import TestCase
from unittest.mock import MagicMock

import numpy as np

from detection.yolo_detector import YOLODetector
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
        self.assertIsInstance(self.local_runner.yolo_detector, YOLODetector)

    def test_process_image(self):
        # given
        self.local_runner.image = (np.array((100, 120, 3))).astype(np.uint8)
        self.local_runner.processing = False
        self.local_runner.start_detection = MagicMock()

        # when
        self.local_runner.process_image()

        # then
        self.local_runner.start_detection.assert_called()

    def test_init_detection_caller(self):
        # given

        # when
        self.local_runner.init_detection_caller(sum, [1, 2])

        # then
        self.assertIsInstance(self.local_runner.detection_caller,
                              DetectionCaller)

