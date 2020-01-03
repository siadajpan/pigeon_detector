import time
from abc import abstractmethod
from typing import Optional, Callable, List

import numpy as np
from master_controller.detection_runners.detection_caller import \
    DetectionCaller


class AbstractDetectionRunner:
    @abstractmethod
    def __init__(self):
        self.image: Optional[np.array] = None
        self.processing = False
        self.last_detection_time: float = 0.
        self.detection_caller: Optional[DetectionCaller] = None

    def update_image(self, image: np.array):
        self.image = image

    def update_detection_result(self, detected: bool):
        self.processing = False
        if detected:
            self.last_detection_time = time.time()

    def process_image(self):
        if self.image is None:
            raise ValueError('There is no image to process')
        if self.processing:
            raise RuntimeError('Detector busy, cannot process another image')

    @abstractmethod
    def init_detection_caller(self, process_function: Callable,
                              arguments: List):
        pass

    def start_detection(self, process_function: Callable, arguments: List):
        self.processing = True

        self.init_detection_caller(process_function, arguments)
        self.detection_caller.start()
