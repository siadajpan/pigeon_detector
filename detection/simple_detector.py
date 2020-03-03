from typing import List, Optional

import cv2
import numpy as np

import settings
from master_controller.image_preprocessing.rectangle import Rectangle


class SimpleDetector:
    def __init__(self):
        self.max_size = settings.SimpleDetection.MAX_SIZE
        self.min_size = settings.SimpleDetection.MIN_SIZE
        self.mask: Optional[np.array] = None

    def _check_object_size_in_range(self, width, height):
        object_in_range = self.max_size > width > self.min_size \
                          and self.max_size > height > self.min_size

        return object_in_range

    def _check_and_append_box_to_list(self, object_boxes: List[Rectangle],
                                      object_box: Rectangle):
        height, width = object_box.height, object_box.width
        if self._check_object_size_in_range(width, height):
            object_boxes.append(object_box)

    def detect(self, image_: np.array, movements: List[Rectangle]) -> List[Rectangle]:
        object_boxes = []
        for movement in movements:
            self._check_and_append_box_to_list(object_boxes, movement)

        return object_boxes
