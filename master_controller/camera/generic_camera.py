from threading import Thread
from typing import Optional

import numpy as np


class GenericCamera(Thread):
    def __init__(self):
        super().__init__()
        self.image = None  # type: Optional[np.array]
        self._stop_camera = False

    def stop(self):
        self._stop_camera = True

    def check_stop(self):
        return self._stop_camera

    def get_current_frame(self):
        return self.image
