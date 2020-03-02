from unittest import TestCase
from unittest.mock import MagicMock, call

import settings
from detection.simple_detector import SimpleDetector
from master_controller.image_preprocessing.rectangle import Rectangle


class TestSimpleDetector(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        max_size = settings.SimpleDetection.MAX_SIZE
        min_size = settings.SimpleDetection.MIN_SIZE
        cls.too_small = min_size - 1
        cls.too_big = max_size + 1
        cls.good_size = int((min_size + max_size) / 2)

    def setUp(self) -> None:
        self.simple_detector = SimpleDetector()

    def test___init__(self):
        self.assertEqual(settings.SimpleDetection.MIN_SIZE,
                         self.simple_detector.min_size)
        self.assertEqual(settings.SimpleDetection.MAX_SIZE,
                         self.simple_detector.max_size)

    def test_check_object_size_in_range(self):
        # given
        self.simple_detector.max_size = 50
        self.simple_detector.min_size = 10

        # when
        result1 = self.simple_detector._check_object_size_in_range(20, 60)
        result2 = self.simple_detector._check_object_size_in_range(20, 5)
        result3 = self.simple_detector._check_object_size_in_range(60, 30)
        result4 = self.simple_detector._check_object_size_in_range(5, 60)
        result5 = self.simple_detector._check_object_size_in_range(15, 20)

        # then
        self.assertFalse(result1)
        self.assertFalse(result2)
        self.assertFalse(result3)
        self.assertFalse(result4)
        self.assertTrue(result5)

    def test_check_and_append_box_to_list(self):
        # given
        rect = Rectangle(1, 2, 3, 4)
        self.simple_detector._check_object_size_in_range = MagicMock(
            return_value=True)
        object_boxes = []

        # when
        self.simple_detector._check_and_append_box_to_list(object_boxes, rect)

        # then
        self.simple_detector._check_object_size_in_range.assert_called()
        self.assertEqual(object_boxes, [rect])

    def test_check_and_append_box_to_list_not(self):
        # given
        rect = Rectangle(1, 2, 3, 4)
        self.simple_detector._check_object_size_in_range = MagicMock(
            return_value=False)
        object_boxes = []

        # when
        self.simple_detector._check_and_append_box_to_list(object_boxes, rect)

        # then
        self.simple_detector._check_object_size_in_range.assert_called()
        self.assertEqual(object_boxes, [])

    def test_detect_good(self):
        # given
        self.simple_detector._check_and_append_box_to_list = MagicMock()
        rect1 = MagicMock()
        rect2 = MagicMock()
        movements = [rect1, rect2]

        # when
        result = self.simple_detector.detect(MagicMock(), movements)

        # then
        self.simple_detector._check_and_append_box_to_list.assert_has_calls([
            call([], rect1), call([], rect2)
        ])
        self.assertEqual([], result)
