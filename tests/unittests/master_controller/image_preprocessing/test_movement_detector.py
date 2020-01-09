import time
from unittest import TestCase
from unittest.mock import MagicMock

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
        preprocessed = self.detector.preprocess_image(frame)

        # then
        self.assertTrue(np.array_equal(blurred, preprocessed))

    def test_update_base_frame(self):
        # given
        frame1 = (np.random.rand(100, 120, 3) * 255).astype(np.uint8)
        frame2 = (np.random.rand(100, 120, 3) * 255).astype(np.uint8)
        time_now = time.time()
        self.detector.preprocess_image = MagicMock(return_value=frame2)

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

    def test_find_contour_empty(self):
        # given
        test_array = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        test_array = np.array(test_array)

        # when
        indexes = self.detector.find_contour(test_array)

        # then
        self.assertIsNone(indexes)

    def test_find_contour(self):
        # given
        test_array = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 1]]
        test_array = np.array(test_array)

        # when
        x_0, y_0, x_width, y_height = \
            self.detector.find_contour(test_array).data

        # then
        self.assertEqual(x_0, 2)
        self.assertEqual(x_width, 2)
        self.assertEqual(y_0, 2)
        self.assertEqual(y_height, 1)

    def test_find_contour_bigger_array(self):
        # given
        test_array = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0],
                      [0, 0, 1, 1, 0],
                      [0, 0, 1, 1, 0],
                      [0, 0, 1, 1, 0]]
        test_array = np.array(test_array)

        # when
        x_0, y_0, x_width, y_height = \
            self.detector.find_contour(test_array).data

        # then
        self.assertEqual(x_0, 1)
        self.assertEqual(x_width, 3)
        self.assertEqual(y_0, 2)
        self.assertEqual(y_height, 4)

    def test_find_array_difference(self):
        # given
        base_frame = (np.random.rand(10, 12, 3) * 255).astype(np.uint8)
        frame = (np.random.rand(10, 12, 3) * 255).astype(np.uint8)
        frame_diff = cv2.absdiff(base_frame, frame)
        thresh = cv2.threshold(frame_diff, 55, 255, cv2.THRESH_BINARY)[1]
        diff = cv2.dilate(thresh, None, iterations=2)

        # when
        diff_calculated = self.detector.find_array_difference(base_frame, frame)

        # then
        self.assertTrue(np.array_equal(diff, diff_calculated))

    def test_select_movement_contours(self):
        # given
        frame1 = (np.random.rand(10, 12, 3) * 255).astype(np.uint8)
        frame2 = (np.random.rand(10, 12, 3) * 255).astype(np.uint8)
        frame3 = (np.random.rand(10, 12, 3) * 255).astype(np.uint8)

        self.detector.preprocess_image = MagicMock(return_value=frame2)
        self.detector.find_array_difference = MagicMock(return_value=frame3)
        self.detector.find_contour = MagicMock(
            return_value=Rectangle(1, 2, 3, 4)
        )

        # when
        self.detector.select_movement_contours(frame1)

        # then
        self.detector.preprocess_image.assert_called_with(frame1)
        self.detector.find_array_difference.assert_called_with(
            self.detector.base_frame, frame2
        )
        self.detector.find_contour.assert_called_with(frame3)
        self.assertTrue(np.array_equal(self.detector.movement_area.data,
                                       (1, 2, 3, 4)))

    def test_cut_frame_by_movement_no_area(self):
        # given
        frame = (np.random.rand(10, 12, 3) * 255).astype(np.uint8)
        self.detector.select_movement_contours = MagicMock()
        self.detector.movement_area = None

        # when
        out_frame = self.detector.cut_frame_by_movement(frame)

        # then
        self.assertIsNone(out_frame)

    def test_cut_frame_by_movement(self):
        # given
        frame = (np.random.rand(10, 12, 3) * 255).astype(np.uint8)
        self.detector.select_movement_contours = MagicMock()
        self.detector.movement_area = Rectangle(1, 2, 3, 4)

        # when
        out_frame = self.detector.cut_frame_by_movement(frame)

        # then
        self.assertTrue(np.array_equal(frame[2: 6, 1: 4], out_frame))

    def test_preprocess_frame_no_movement(self):
        # given
        curr_frame = (np.random.rand(40, 60, 3) * 255).astype(np.uint8)
        cut_frame = None
        self.detector.curr_frame = curr_frame
        self.detector.cut_frame_by_movement = MagicMock(
            return_value=cut_frame
        )

        # when
        self.detector.preprocess_frame()

        # then
        self.assertIsNone(self.detector.movement_frame)

    def test_preprocess_frame_small_movement(self):
        # given
        curr_frame = (np.random.rand(40, 60, 3) * 255).astype(np.uint8)
        cut_frame = (np.random.rand(1, 2, 3) * 255).astype(np.uint8)
        self.detector.curr_frame = curr_frame
        self.detector.cut_frame_by_movement = MagicMock(
            return_value=cut_frame
        )

        # when
        self.detector.preprocess_frame()

        # then
        self.assertIsNone(self.detector.movement_frame)

    def test_preprocess_frame(self):
        # given
        curr_frame = (np.random.rand(40, 60, 3) * 255).astype(np.uint8)
        cut_frame = (np.random.rand(30, 30, 3) * 255).astype(np.uint8)
        self.detector.curr_frame = curr_frame
        self.detector.cut_frame_by_movement = MagicMock(
            return_value=cut_frame
        )

        # when
        self.detector.preprocess_frame()

        # then
        self.assertTrue(np.array_equal(cut_frame, self.detector.movement_frame))

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
