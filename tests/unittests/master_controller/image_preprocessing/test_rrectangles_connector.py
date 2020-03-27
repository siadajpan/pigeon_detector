from unittest import TestCase

import numpy as np

from master_controller.image_preprocessing.rectangles_connector import \
    group_rectangles


class TestRectanglesConnector(TestCase):
    def test_connecting_rectangles(self):
        image = np.zeros((60, 100, 3), dtype=np.uint8)
        temp_image = np.zeros(image.shape[:2], dtype=np.uint8)

        overlap_distance = 1

        rect1 = (10, 10, 20, 20)
        rect2 = (25, 27, 40, 45)
        rect3 = (8, 12, 25, 50)
        rect4 = (60, 10, 80, 40)

        rectangles = [rect1, rect2, rect3, rect4]

        # when
        rects = group_rectangles(rectangles)

        # then
        np.testing.assert_array_equal([[60, 10, 81, 41], [8, 10, 41, 51]],
                                      rects)
