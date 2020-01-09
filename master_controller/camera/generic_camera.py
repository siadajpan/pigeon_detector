from threading import Thread
from typing import Optional

import cv2
import numpy as np


class GenericCamera(Thread):
    def __init__(self, show_frame: bool = True):
        super().__init__()
        self.image = None  # type: Optional[np.array]
        self.showing_image = show_frame
        self._stop_camera = False
        self._running = True

    @property
    def running(self):
        return self._running

    def stop(self):
        self._stop_camera = True
        self._running = False

    def check_stop(self):
        return self._stop_camera

    def get_current_frame(self):
        return self.image

    def show_frame(self):
        cv2.imshow('current image', self.get_current_frame())
        if cv2.waitKey(1) == ord('q'):
            self.stop()

    @staticmethod
    def end_showing():
        cv2.destroyAllWindows()
