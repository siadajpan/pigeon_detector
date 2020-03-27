from unittest import TestCase
from unittest.mock import MagicMock, patch

import cv2

from master_controller.video_recorder import VideoRecorder


class TestVideoRecorder(TestCase):
    def setUp(self) -> None:
        self.video_recorder = VideoRecorder()

    def test___init__(self):
        self.assertEqual(cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                         self.video_recorder.codec)
        self.assertIsNone(self.video_recorder.video_writer)

    @patch('os.path.exists')
    @patch('os.mkdir')
    def test_create_folder_doesnt_create_if_exists(self, mkdir_mock,
                                                   exists_mock):
        # given
        exists_mock.return_value = True

        # when
        self.video_recorder.create_folder_if_not_exists(MagicMock())

        # then
        mkdir_mock.assert_not_called()

    @patch('os.path.exists')
    @patch('os.mkdir')
    def test_create_folder_if_not_exists(self, mkdir_mock, exists_mock):
        # given
        exists_mock.return_value = False

        # when
        self.video_recorder.create_folder_if_not_exists(MagicMock())

        # then
        mkdir_mock.assert_called()

    @patch('os.path.join')
    def test_create_folder_structure(self, join_mock):
        # given
        self.video_recorder.create_folder_if_not_exists = MagicMock()

        # when
        self.video_recorder.create_folder_structure()

        # then
        self.video_recorder.create_folder_if_not_exists.assert_called()
        join_mock.assert_called()

    @patch('cv2.VideoWriter')
    def test_init_recording(self, writer_mock):
        # given
        frame = MagicMock()
        frame.shape = [1, 2]
        self.video_recorder.create_folder_structure = MagicMock()

        # when
        self.video_recorder.init_recording(frame, 10)

        # then
        self.video_recorder.create_folder_structure.assert_called()
        self.assertIsNotNone(self.video_recorder.video_writer)

    def test_update_frame(self):
        # given
        self.video_recorder.video_writer = MagicMock()

        # when
        self.video_recorder.update_frame(MagicMock())

        # then
        self.video_recorder.video_writer.write.assert_called()

    def test_stop_recording(self):
        # given
        self.video_recorder.video_writer = MagicMock()

        # when
        self.video_recorder.stop_recording()

        # then
        self.video_recorder.video_writer.release.assert_called()
