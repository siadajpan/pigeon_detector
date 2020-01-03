from typing import Callable, List

from detection.yolo_detector import YOLODetector
from master_controller.detection_runners.abstract_detection_runner import \
    AbstractDetectionRunner
from master_controller.detection_runners.detection_caller import \
    DetectionCaller


class LocalDetectionRunner(AbstractDetectionRunner):
    def __init__(self):
        super().__init__()
        self.yolo_detector = YOLODetector()

    def process_image(self):
        super().process_image()
        process_image_function = self.yolo_detector.detect_birds
        self.start_detection(process_image_function, [self.image])

    def init_detection_caller(self, process_function: Callable,
                              arguments: List):

        self.detection_caller = DetectionCaller(
            process_image_function=process_function,
            arguments=arguments,
            callback=self.update_detection_result
        )
