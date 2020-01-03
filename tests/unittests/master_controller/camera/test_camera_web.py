from unittest import TestCase
from unittest.mock import MagicMock, patch

import cv2

from master_controller.camera.camera_web import CameraWeb


class TestCameraWeb(TestCase):
    @patch('time.sleep')
    @patch.object(cv2, 'VideoCapture')
    def setUp(self, video_capture_mock, time_mock) -> None:
        self.frame = MagicMock()
        self.cap = MagicMock()
        video_capture_mock.return_value = self.cap
        self.cap.read = MagicMock(return_value=(MagicMock(), self.frame))
        self.camera_web = CameraWeb()

    def test_init_cap(self):
        # given
        self.frame.shape = 'shape'
        
        # when
        shape = self.camera_web.init_cap()
        
        # then
        self.assertEqual('shape', shape)

    def _stop_loop(self):
        self.camera_web._stop_camera = True

    def test_run_with_showing_image(self):
        # given
        self.camera_web.showing_image = True
        self.camera_web.show_frame = MagicMock()
        # self.cap.read.side_effect = self._stop_loop
        
        # when
        self.camera_web.run()
        
        # then
        self.cap.read.assert_called()

    def test_quit(self):
        # given
        
        # when
        
        # then
        pass

