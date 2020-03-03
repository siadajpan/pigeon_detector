from typing import List

from detection.simple_detector import SimpleDetector
from master_controller.detection_runners.abstract_detection_runner import \
    AbstractDetectionRunner
from master_controller.detection_runners.detection_caller import \
    DetectionCaller


class LocalDetectionRunner(AbstractDetectionRunner):
    def __init__(self):
        self.simple_detector = SimpleDetector()
        super().__init__()

    def _init_detection_caller(self, arguments: List) -> DetectionCaller:
        detection_caller = DetectionCaller(
            process_image_function=self.simple_detector.detect,
            arguments=arguments,
            callback=self.update_detection_result
        )

        return detection_caller

    def send_image(self):
        super().send_image()
        caller = self._init_detection_caller([self.image, self.movement_boxes])
        caller.start()
