import time
from typing import List, Callable, Tuple

import cv2
import requests

import settings
from master_controller.detection_runners.abstract_detection_runner import \
    AbstractDetectionRunner
from master_controller.detection_runners.server_detection_caller import \
    ServerDetectionCaller


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

    def process_image(self):
        super().process_image()
        process_image_function = requests.post
        _, image_encoded = cv2.imencode('.jpg', self.image)
        arguments = [self.send_pic_address, image_encoded.tostring()]

        self.start_detection(process_image_function, arguments)

    def update_detection_result(self, detected: Tuple[bool, bool]):
        connected, detection = detected
        self.connected = connected

        super().update_detection_result(detection)

    def init_detection_caller(self, process_function: Callable,
                              arguments: List):

        self.detection_caller = ServerDetectionCaller(
            process_image_function=process_function,
            arguments=arguments,
            callback=self.update_detection_result
        )

    def last_connection_check_too_recent(self):
        return time.time() - self.last_connection_check < 4

    def check_connection(self):
        if self.connected:
            return True

        if self.last_connection_check_too_recent():
            return self.connected  # False
        try:
            requests.get(self.connection_check)
            self.connected = True
        except requests.exceptions.ConnectionError:
            self.connected = False

        return self.connected
