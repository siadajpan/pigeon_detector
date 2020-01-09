from typing import Callable, List

import requests

from master_controller.detection_runners.detection_caller import \
    DetectionCaller


class ServerDetectionCaller(DetectionCaller):
    def __init__(self, process_image_function: Callable, arguments: List,
                 callback: Callable):
        super().__init__(process_image_function, arguments, callback)

    def run(self) -> None:
        try:
            response = self.process_image_function(*self.arguments)
            self.callback((True, response.json()))
        except requests.exceptions.ConnectionError:
            self.callback((False, False))
