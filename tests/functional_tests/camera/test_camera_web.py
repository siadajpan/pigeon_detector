from typing import Tuple
from unittest import TestCase
from unittest.mock import MagicMock

import cv2
import numpy as np

from master_controller.camera.camera_web import CameraWeb


class TestCameraWeb(TestCase):
    def setUp(self) -> None:
        self.camera = CameraWeb()

    def tearDown(self) -> None:
        self.camera._cap.release()

    def test_init(self):
        self.assertIsInstance(self.camera._cap, cv2.VideoCapture)
        self.assertIsInstance(self.camera.frame_size, Tuple)

    def test_init_cap(self):
        # given
        self.camera._cap = MagicMock()
        self.camera._cap.read = MagicMock(
            return_value=(True, np.ones((10, 10, 3))))

        # when
        frame = self.camera.init_cap()

        # then
        self.camera._cap.read.assert_called()
        self.assertEqual(frame, (10, 10, 3))

    def test_run(self):
        # given
        self.camera.stop()
        self.camera.quit = MagicMock()

        # when
        self.camera.run()

        # then
        self.camera.quit.assert_called()

    def test_quit(self):
        # given
        self.camera._cap = MagicMock()
        self.camera._cap.release = MagicMock()

        # when
        self.camera.quit()

        # then
        self.camera._cap.release.assert_called()
