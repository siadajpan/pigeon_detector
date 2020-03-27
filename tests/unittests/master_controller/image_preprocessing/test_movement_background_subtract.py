from unittest import TestCase
from unittest.mock import MagicMock, patch

import cv2

import settings
from master_controller.image_preprocessing.movement_background_subtract import \
    MovementDetectorBackgroundSubtract


class TestMovementDetectorBackgroundSubtract(TestCase):
    def setUp(self) -> None:
        self.movement = MovementDetectorBackgroundSubtract()

    def test___init__(self):
        self.assertEqual([], self.movement.movement_boxes)
        self.assertIsInstance(self.movement.background_subtractor,
                              cv2.BackgroundSubtractor)

    @patch('cv2.erode')
    @patch('cv2.dilate')
    @patch('cv2.findContours')
    def test_find_contours(self, contours_mock, dilate_mock, erode_mock):
        # given
        contours_mock.return_value = 'cnts', 'hierarchy'

        # when
        self.movement.find_contours(MagicMock())

        # then
        erode_mock.assert_called()
        dilate_mock.assert_called()
        contours_mock.assert_called()

    @patch('cv2.boundingRect')
    def test_analyze_contours_doesnt_output_contour_if_out_of_size(self,
                                                                   rect_mock):
        # given
        max_size = settings.PreProcessing.MAX_SIZE
        min_size = settings.PreProcessing.MIN_SIZE

        rect_mock.side_effect = [[0, 0, min_size - 1, min_size + 1],
                                 [0, 0, min_size + 1, min_size - 1],
                                 [0, 0, max_size + 1, min_size + 1],
                                 [0, 0, min_size + 1, max_size + 1]]

        # when
        result = self.movement.analyze_contours([1, 2, 3, 4])

        # then
        self.assertEqual([], result)

    @patch('cv2.boundingRect')
    @patch('master_controller.image_preprocessing.rectangles_connector.group_rectangles')
    def test_analyze_contours_groups_rectangles(self, connector_mock, rect_mock):
        # given
        min_size = settings.PreProcessing.MIN_SIZE

        rect_mock.return_value = [0, 0, min_size + 1, min_size + 1]
        connector_mock.return_value = 'rects'

        # when
        result = self.movement.analyze_contours([1, 2, 3, 4])

        # then
        connector_mock.assert_called()
        self.assertEqual('rects', result)

    def test_find_movement_boxes(self):
        # given
        self.movement.find_contours = MagicMock()
        self.movement.analyze_contours = MagicMock()

        # when
        self.movement.find_movement_boxes(MagicMock())

        # then
        self.movement.find_contours.assert_called()
        self.movement.analyze_contours.assert_called()

    def test_analyze_image(self):
        # given
        self.movement.background_subtractor = MagicMock()
        self.movement.find_movement_boxes = MagicMock(return_value='rects')

        # when
        result = self.movement.analyze_image(MagicMock())

        # then
        self.movement.background_subtractor.apply.assert_called()
        self.movement.find_movement_boxes.assert_called()
        self.assertEqual('rects', result)
