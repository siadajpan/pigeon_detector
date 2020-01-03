from threading import Thread
from typing import Optional

import numpy as np


class DetectionClient(Thread):
    def __init__(self):
        super(DetectionClient, self).__init__()
        self.image: Optional[np.array] = None
        self.connection_status: bool = False
        self._stop_loop: bool = False
        self.bird_detected: bool = False

    def update_image(self, image: np.array):
        self.image = image

    def connect(self, server_address):
        # keep trying to connect every some seconds
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def send_image(self):
        raise NotImplementedError

    def parse_response(self, response):
        raise NotImplementedError

    def run(self):
        while not self._stop_loop:
            response = self.send_image()
            self.parse_response(response)

        self.disconnect()
