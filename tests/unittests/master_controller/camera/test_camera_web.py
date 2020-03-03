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
        return MagicMock(), MagicMock()

    def test_run_with_showing_image(self):
        # given
        self.camera_web.check_stop = MagicMock(side_effect=[False, True])
        self.cap.read.return_value = ('ret', 'frame')

        # when
        self.camera_web.run()
        
        # then
        self.cap.read.assert_called()
        self.assertEqual('frame', self.camera_web.image)

    def test_quit_not_showing_image(self):
        # given

        # when
        self.camera_web.quit()

        # then
        self.cap.release.assert_called()


