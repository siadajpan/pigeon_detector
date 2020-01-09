from unittest import TestCase
from unittest.mock import MagicMock

import settings
from detection.simple_detector import SimpleDetector


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

    def test_detect_too_small(self):
        # given
        image = MagicMock()
        image.shape = (self.too_small, self.too_small)

        # when
        in_range = self.simple_detector.detect(image)

        # then
        self.assertFalse(in_range)

    def test_detect_too_big(self):
        # given
        image = MagicMock()
        image.shape = (self.too_big, self.too_big)

        # when
        in_range = self.simple_detector.detect(image)

        # then
        self.assertFalse(in_range)

    def test_detect_good(self):
        # given
        image = MagicMock()
        image.shape = (self.good_size, self.good_size)

        # when
        in_range = self.simple_detector.detect(image)

        # then
        self.assertTrue(in_range)
