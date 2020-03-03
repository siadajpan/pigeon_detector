import time
from typing import List, Callable, Tuple

import cv2
import requests

import settings
from master_controller.detection_runners.abstract_detection_runner import \
    AbstractDetectionRunner
from master_controller.detection_runners.server_detection_caller import \
    ServerDetectionCaller
from master_controller.image_preprocessing.rectangle import Rectangle


class ServerDetectionRunner(AbstractDetectionRunner):
    def __init__(self):
        super().__init__()
        server_address = settings.Server.DETECTION_ADDRESS
        self.send_pic_address = server_address + \
            settings.Server.IMAGE_PROCESSING
        self.connection_check = server_address + \
            settings.Server.CONNECTION_CHECK
        self.connected = False
        self.last_connection_check = 0.

    def update_detection_result(self, result: Tuple[bool, List[Rectangle]]):
        connected, boxes = result
        if not connected:
            self.connected = False
            return

        super().update_detection_result(boxes)

    def _init_detection_caller(self, arguments: List):
        detection_caller = ServerDetectionCaller(
            process_image_function=requests.post,
            arguments=arguments,
            callback=self.update_detection_result
        )
        return detection_caller

    def send_image(self):
        super().send_image()
        _, image_encoded = cv2.imencode('.jpg', self.image)
        arguments = [self.send_pic_address, image_encoded.tostring()]

        caller = self._init_detection_caller(arguments)
        caller.start()

    def _last_connection_check_too_recent(self):
        return time.time() - self.last_connection_check < 60

    def check_connection(self):
        if self.connected:
            return True

        if self._last_connection_check_too_recent():
            return self.connected  # False
        try:
            self.last_connection_check = time.time()
            requests.get(self.connection_check, timeout=1)
            self.connected = True
        except requests.exceptions.ConnectionError:
            self.connected = False
        except requests.exceptions.Timeout:
            self.connected = False

        return self.connected
