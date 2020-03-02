import time
from unittest import TestCase
from unittest.mock import MagicMock, patch

import cv2
import numpy as np

import settings
from master_controller.image_preprocessing.movement_detector import \
    MovementDetector
from master_controller.image_preprocessing.rectangle import Rectangle


class TestMovementDetector(TestCase):
    def setUp(self) -> None:
        # pass
        self.detector = MovementDetector()

    def tearDown(self) -> None:
        self.detector.stop()

    def test_stop(self):
        # given
        self.assertFalse(self.detector.stop_detector)

        # when
        self.detector.stop()

        # then
        self.assertTrue(self.detector.stop_detector)

    def test_add_frame(self):
        # given
        frame = np.array([1, 2])

        # when
        self.detector.add_frame(frame)

        # then
        self.assertTrue(np.array_equal(self.detector.curr_frame, frame))

    def test_preprocess_image(self):
        # given
        frame = (np.random.rand(100, 120, 3) * 255).astype(np.uint8)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (21, 21), 0)

        # when
        preprocessed = self.detector.pre_process_image(frame)

        # then
        self.assertTrue(np.array_equal(blurred, preprocessed))

    def test_update_base_frame(self):
        # given
        frame1 = (np.random.rand(100, 120, 3) * 255).astype(np.uint8)
        frame2 = (np.random.rand(100, 120, 3) * 255).astype(np.uint8)
        time_now = time.time()
        self.detector.pre_process_image = MagicMock(return_value=frame2)

        # when
        self.detector.update_base_frame(frame1)

        # then
        self.assertTrue(np.array_equal(self.detector.base_frame, frame2))
        self.assertAlmostEqual(self.detector.base_frame_time, time_now,
                               places=1)

    def test_cut_frame(self):
        # given
        frame = (np.random.rand(100, 120, 3) * 255).astype(np.uint8)
        rectangle = Rectangle(20, 30, 10, 20)
        cut_frame = frame[30: 50, 20: 30]

        # when
        frame = self.detector.cut_frame(frame, rectangle)

        # then
        self.assertTrue(np.array_equal(frame, cut_frame))

    def test_find_first_non_zero_row(self):
        # given
        test_array = [[0, 0, 1, 1]]

        # when
        first_row = self.detector.find_first_non_zero_row(test_array)

        # then
        self.assertEqual(first_row, 0)

    def test_find_first_non_zero_row_2d(self):
        # given
        test_array = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 1]]

        # when
        first_row = self.detector.find_first_non_zero_row(test_array)

        # then
        self.assertEqual(first_row, 2)

    @patch('cv2.findContours')
    @patch('cv2.boundingRect')
    def test_find_contour(self, box_mock, find_contours_mock):
        # given
        find_contours_mock.return_value = (['cnts'], 'hierarchy')
        box_mock.return_value = [1, 2, 3, 4]

        # when
        rectangles = self.detector.find_contour(MagicMock())

        # then
        find_contours_mock.assert_called()
        box_mock.assert_called()
        self.assertEqual([Rectangle(1, 2, 3, 4)], rectangles)

    @patch('cv2.absdiff')
    @patch('cv2.threshold')
    @patch('cv2.dilate')
    @patch('cv2.erode')
    def test_find_array_difference(self, erode_mock, dilate_mock, thresh_mock,
                                   absdiff_mock):
        # given
        dilate_mock.return_value = 'dilated'
        erode_mock.return_value = 'eroded'
        thresh_mock.return_value = ('_', 'thresh')
        absdiff_mock.return_value = 'absdiff'

        # when
        diff_calculated = self.detector.find_array_difference(MagicMock(),
                                                              MagicMock())

        # then
        absdiff_mock.assert_called()
        thresh_mock.assert_called()
        dilate_mock.assert_called()
        erode_mock.assert_called()
        self.assertEqual('eroded', diff_calculated)

    def test_select_movement_contours(self):
        # given
        self.detector.pre_process_image = MagicMock()
        self.detector.find_array_difference = MagicMock()
        self.detector.find_contour = MagicMock()

        # when
        self.detector.select_movement_contours()

        # then
        self.detector.pre_process_image.assert_called()
        self.detector.find_array_difference.assert_called()
        self.detector.find_contour.assert_called()

    def test_check_if_update_base_frame_yes(self):
        # given
        self.detector.base_frame_time = time.time() - settings.NEW_BASE_TIME - 1

        # when
        update = self.detector.check_if_update_base_frame()

        # then
        self.assertTrue(update)

    def test_check_if_update_base_frame_no(self):
        # given
        self.detector.base_frame_time = time.time() - settings.NEW_BASE_TIME + 1

        # when
        update = self.detector.check_if_update_base_frame()

        # then
        self.assertFalse(update)
