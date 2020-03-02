import time
from abc import abstractmethod
from typing import Optional, List, Callable

import numpy as np

from master_controller.image_preprocessing.rectangle import Rectangle


class AbstractDetectionRunner:
    def __init__(self):
        self.image: Optional[np.array] = None
        self.processing: bool = False
        self.last_detections: Optional[List[Rectangle]] = None
        self.movement_boxes: Optional[List[Rectangle]] = None

    def update_image(self, image: np.array):
        self.image = image

    def update_movement_boxes(self, movements: List[Rectangle]):
        self.movement_boxes = movements

    def update_detection_result(self, detected_boxes: List[Rectangle]):
        self.last_detections = detected_boxes
        self.processing = False

    def send_image(self):
        if self.image is None:
            raise ValueError('There is no image to process')
        if self.movement_boxes is None:
            raise ValueError('There are no rectangles selected on picture')
        if self.processing:
            raise RuntimeError('Detector busy, cannot process another image')

        self.processing = True
