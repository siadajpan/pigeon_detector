import numpy as np

import settings


class SimpleDetector:
    def __init__(self):
        self.max_size = settings.SimpleDetection.MAX_SIZE
        self.min_size = settings.SimpleDetection.MIN_SIZE

    def detect(self, image_: np.array) -> bool:
        width, height = image_.shape[:2]
        object_in_range = self.max_size > width > self.min_size \
            and self.max_size > height > self.min_size

        return object_in_range
