from threading import Thread
from unittest import TestCase
from unittest.mock import MagicMock

import numpy as np

from master_controller.detection_runners.detection_caller import \
    DetectionCaller


class TestDetectionCaller(TestCase):
    def setUp(self) -> None:
        self.process_function = MagicMock
        self.image_ = np.array((10, 20, 3))
        self.callback = MagicMock
        self.thread = DetectionCaller(self.process_function, [self.image_],
                                      self.callback)

    def test_init(self):
        self.assertIsInstance(self.thread, Thread)
        self.assertEqual(self.process_function,
                         self.thread.process_image_function)
        self.assertTrue(np.array_equal(self.image_, self.thread.arguments[0]))
        self.assertEqual(self.callback, self.thread.callback)

    def test_run(self):
        # given
        self.thread.process_image_function = MagicMock(return_value=True)
        self.thread.callback = MagicMock()

        # when
        self.thread.start()

        # then
        self.thread.process_image_function.assert_called_with(self.image_)
        self.thread.callback.assert_called_with(True)
