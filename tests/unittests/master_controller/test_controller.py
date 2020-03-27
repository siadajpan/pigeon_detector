from unittest import TestCase
from unittest.mock import MagicMock, patch

import requests

from master_controller.controller import Controller
from master_controller.detection_runners.local_detection_runner import \
    LocalDetectionRunner
from master_controller.detection_runners.server_detection_runner import \
    ServerDetectionRunner
from settings import NOISE_LENGTH


class TestController(TestCase):
    def setUp(self) -> None:
        self.camera = MagicMock()
        self.detector = MagicMock()
        self.music_player = MagicMock()
        self.video_recorder = MagicMock()

        self.controller = Controller(self.camera, self.detector,
                                     self.music_player, self.video_recorder)

    def test___init__(self):
        self.assertEqual(self.camera, self.controller._camera)
        self.assertEqual(self.detector, self.controller._movement_detector)
        self.assertEqual(self.music_player, self.controller._music_player)
        self.assertFalse(self.controller._playing_music)
        self.assertFalse(self.controller._picture_show)
        self.assertIsInstance(self.controller._local_detector,
                              LocalDetectionRunner)
        self.assertIsInstance(self.controller._server_detector,
                              ServerDetectionRunner)
        self.assertEqual(0, self.controller._last_detection_time)

    def test_start_camera(self):
        # given

        # when
        self.controller.start_camera()

        # then
        self.controller._camera.start.assert_called()

    def test_start_music_player(self):
        # given

        # when
        self.controller.start_music_player()

        # then
        self.controller._music_player.start.assert_called()
        self.assertTrue(self.controller._playing_music)

    def test_stop_music_player(self):
        # given

        # when
        self.controller.stop_music_player()

        # then
        self.controller._music_player.stop.assert_called()
        self.assertFalse(self.controller._playing_music)

    def test_start_recording(self):
        # given

        # when
        self.controller.start_recording(MagicMock(), 10)

        # then
        self.controller._video_recorder.init_recording.assert_called()

    def test_stop_recording(self):
        # given

        # when
        self.controller.stop_recording()

        # then
        self.controller._video_recorder.stop_recording.assert_called()

    def test_stop(self):
        # given
        self.controller.stop_music_player = MagicMock()
        self.controller.stop_recording = MagicMock()

        # when
        self.controller.stop()

        # then
        self.controller._camera.stop.assert_called()
        self.controller.stop_music_player.assert_called()
        self.controller.stop_recording.assert_called()

    @patch('requests.post')
    def test_start_movement(self, post_mock):
        # given

        # when
        self.controller.start_movement()

        # then
        post_mock.assert_called()

    @patch('requests.post')
    def test_start_movement_connection_error(self, post_mock):
        # given
        post_mock.side_effect = requests.exceptions.ConnectionError

        # when
        self.controller.start_movement()

        # then no raise
        post_mock.assert_called()

    @patch('requests.post')
    def test_start_movement_timeout_error(self, post_mock):
        # given
        post_mock.side_effect = requests.exceptions.Timeout

        # when
        self.controller.start_movement()

        # then no raise
        post_mock.assert_called()

    @patch('cv2.flip')
    def test_flip_image(self, flip_mock):
        # given
        flip_mock.return_value = 'flipped'

        # when
        result = self.controller.flip_image(MagicMock())

        # then
        flip_mock.assert_called()
        self.assertEqual('flipped', result)

    @patch('datetime.datetime')
    @patch('cv2.imwrite')
    def test_save_picture(self, image_write_mock, now_mock):
        # given
        now = MagicMock()
        now_mock.now = MagicMock(return_value=now)
        now.strftime = MagicMock(return_value='time')
        self.controller.get_image_with_movement = MagicMock()
        self.controller.flip_image = MagicMock(return_value='flipped')

        # when
        self.controller.save_picture('path')

        # then
        now_mock.now.assert_called()
        now.strftime.assert_called()
        self.controller.get_image_with_movement.assert_called()
        self.controller.flip_image.assert_called()
        image_write_mock.assert_called()

    @patch('time.time')
    def test_music_timeout(self, time_mock):
        # given
        self.controller._last_detection_time = 0
        time_mock.return_value = NOISE_LENGTH + 1

        # when
        result = self.controller.music_timeout()

        # then
        time_mock.assert_called()
        self.assertTrue(result)

    @patch('time.time')
    def test_music_timeout_not_yet(self, time_mock):
        # given
        self.controller._last_detection_time = 0
        time_mock.return_value = NOISE_LENGTH - 1

        # when
        result = self.controller.music_timeout()

        # then
        time_mock.assert_called()
        self.assertFalse(result)

    @patch('time.time')
    def test_check_detection_time_detection(self, time_mock):
        # given
        self.controller._detector_in_use.last_detection_time = 1
        self.controller._last_detection_time = 0
        time_mock.return_value = NOISE_LENGTH

        # when
        result = self.controller.check_detection_time()

        # then
        time_mock.assert_called()
        self.assertEqual(1, self.controller._last_detection_time)
        self.assertTrue(result)

    @patch('time.time')
    def test_check_detection_time(self, time_mock):
        # given
        self.controller._detector_in_use.last_detection_time = 1
        self.controller._last_detection_time = 0
        time_mock.return_value = NOISE_LENGTH + 2

        # when
        result = self.controller.check_detection_time()

        # then
        time_mock.assert_called()
        self.assertEqual(0, self.controller._last_detection_time)
        self.assertFalse(result)

    def test_check_music_timeout_timeout(self):
        # given
        self.controller.music_timeout = MagicMock(return_value=True)
        self.controller.stop_music_player = MagicMock()

        # when
        self.controller.check_music_timeout()

        # then
        self.controller.music_timeout.assert_called()
        self.controller.stop_music_player.assert_called()

    def test_check_music_timeout_no_timeout(self):
        # given
        self.controller.music_timeout = MagicMock(return_value=False)
        self.controller.stop_music_player = MagicMock()

        # when
        self.controller.check_music_timeout()

        # then
        self.controller.music_timeout.assert_called()
        self.controller.stop_music_player.assert_not_called()

    def test_get_image_with_movement_no_detections(self):
        # given
        curr_frame = MagicMock()
        self.controller._camera.get_current_frame = MagicMock(
            return_value=curr_frame)
        curr_frame.copy = MagicMock(
            return_value='image'
        )
        self.controller._detector_in_use.last_detections = None

        # when
        result = self.controller.get_image_with_movement()

        # then
        self.assertEqual('image', result)

    @patch('cv2.rectangle')
    def test_get_image_with_movement_detections(self, rectangle_mock):
        # given
        curr_frame = MagicMock()
        self.controller._camera.get_current_frame = MagicMock(
            return_value=curr_frame)
        curr_frame.copy = MagicMock(
            return_value='image'
        )
        self.controller._detector_in_use.last_detections = [MagicMock()]

        # when
        result = self.controller.get_image_with_movement()

        # then
        self.assertEqual('image', result)
        rectangle_mock.assert_called()

    @patch('cv2.imshow')
    @patch('cv2.waitKey')
    def test_show_picture(self, wait_key_mock, imshow_mock):
        # given
        self.controller.get_image_with_movement = MagicMock()
        wait_key_mock.return_value = ord('2')

        # when
        self.controller.show_picture()

        # then
        self.controller.get_image_with_movement.assert_called()
        imshow_mock.assert_called()
        wait_key_mock.assert_called()

    @patch('cv2.imshow')
    @patch('cv2.waitKey')
    def test_show_picture_pressed_q(self, wait_key_mock, imshow_mock):
        # given
        self.controller.get_image_with_movement = MagicMock()
        wait_key_mock.return_value = ord('q')

        # when
        self.assertRaises(KeyboardInterrupt, self.controller.show_picture)

        # then
        self.controller.get_image_with_movement.assert_called()
        imshow_mock.assert_called()
        wait_key_mock.assert_called()

    def test_check_detection_playing(self):
        # given
        self.controller._playing_music = True
        self.controller.check_music_timeout = MagicMock()

        # when
        self.controller.check_detection()

        # then
        self.controller.check_music_timeout.assert_called()

    def test_check_detection_no_detection(self):
        # given
        self.controller._playing_music = False
        self.controller.check_detection_time = MagicMock(return_value=False)

        # when
        self.controller.check_detection()

        # then
        self.controller.check_detection_time.assert_called()

    def test_check_detection(self):
        # given
        self.controller._playing_music = False
        self.controller.check_detection_time = MagicMock(return_value=True)
        self.controller.save_picture = MagicMock()
        self.controller.start_movement = MagicMock()
        self.controller.start_music_player = MagicMock()

        # when
        self.controller.check_detection()

        # then
        self.controller.check_detection_time.assert_called()
        self.controller.save_picture.assert_called()
        self.controller.start_movement.assert_called()
        self.controller.start_music_player.assert_called()

    def test_choose_detector_server(self):
        # given
        self.controller._server_detector.check_connection = MagicMock(
            return_value=True
        )

        # when
        self.controller.choose_detector()

        # then
        self.assertEqual(self.controller._server_detector,
                         self.controller._detector_in_use)

    def test_choose_detector_local(self):
        # given
        self.controller._server_detector.check_connection = MagicMock(
            return_value=False
        )

        # when
        self.controller.choose_detector()

        # then
        self.assertEqual(self.controller._local_detector,
                         self.controller._detector_in_use)

    def test_update_detector_if_not_processing(self):
        # given
        detector = MagicMock()
        detector.processing = False
        self.controller._detector_in_use = detector

        # when
        self.controller.send_update_to_detector('pic', 'mov')

        # then
        detector.update_image.assert_called()
        detector.update_movement_boxes.assert_called()
        detector.send_image.assert_called()

    def test_update_picture_to_detector_should_return_if_detector_processing(self):
        # given
        detector = MagicMock()
        detector.processing = True
        self.controller._detector_in_use = detector

        # when
        self.controller.update_picture_to_detector_if_not_processing(MagicMock())

        # then
        self.controller._movement_detector.analyze_image.assert_not_called()

    def test_update_picture_to_detector_should_return_if_movements_are_None(self):
        # given
        detector = MagicMock()
        detector.processing = False
        self.controller._detector_in_use = detector
        self.controller._movement_detector.analyze_image = MagicMock(return_value=None)
        self.controller.send_update_to_detector = MagicMock()

        # when
        self.controller.update_picture_to_detector_if_not_processing(MagicMock())

        # then
        self.controller._movement_detector.analyze_image.assert_called()
        self.controller.send_update_to_detector.assert_not_called()

    def test_update_picture_to_detector_should_send_update_to_detector(self):
        # given
        detector = MagicMock()
        detector.processing = False
        self.controller._detector_in_use = detector
        self.controller._movement_detector.analyze_image = MagicMock(return_value=['boxes'])
        self.controller.send_update_to_detector = MagicMock()

        # when
        self.controller.update_picture_to_detector_if_not_processing(MagicMock())

        # then
        self.controller.send_update_to_detector.assert_called()

    def test_process_detection(self):
        # given
        self.controller.choose_detector = MagicMock()
        self.controller.update_picture_to_detector_if_not_processing = \
            MagicMock()
        self.controller._picture_show = False
        self.controller.check_detection = MagicMock()

        # when
        self.controller.process_detection()

        # then
        self.controller.choose_detector.assert_called()
        self.controller.update_picture_to_detector_if_not_processing.\
            assert_called()
        self.controller.check_detection.assert_called()

    def test_process_detection_show_picture(self):
        # given
        self.controller.choose_detector = MagicMock()
        self.controller.update_picture_to_detector_if_not_processing = \
            MagicMock()
        self.controller._picture_show = True
        self.controller.show_picture = MagicMock()
        self.controller.check_detection = MagicMock()

        # when
        self.controller.process_detection()

        # then
        self.controller.choose_detector.assert_called()
        self.controller.update_picture_to_detector_if_not_processing.\
            assert_called()
        self.controller.check_detection.assert_called()
