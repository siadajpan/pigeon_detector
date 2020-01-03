from typing import Callable, List

from detection.simple_detector import SimpleDetector
from master_controller.detection_runners.abstract_detection_runner import \
    AbstractDetectionRunner
from master_controller.detection_runners.detection_caller import \
    DetectionCaller


class LocalDetectionRunner(AbstractDetectionRunner):
    def __init__(self):
        super().__init__()
        self.simple_detector = SimpleDetector()

    def process_image(self):
        super().process_image()
        process_image_function = self.simple_detector.detect
        self.start_detection(process_image_function, [self.image])

    def init_detection_caller(self, process_function: Callable,
                              arguments: List):

        self.detection_caller = DetectionCaller(
            process_image_function=process_function,
            arguments=arguments,
            callback=self.update_detection_result
        )
