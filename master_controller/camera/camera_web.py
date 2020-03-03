import time

import cv2

from master_controller.camera.generic_camera import GenericCamera


class CameraWeb(GenericCamera):
    def __init__(self):
        super().__init__()
        self._cap = cv2.VideoCapture(0)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.frame_size = self.init_cap()

    def init_cap(self):
        ret, frame = self._cap.read()
        return frame.shape

    def run(self) -> None:
        while not self.check_stop():
            ret, frame = self._cap.read()
            self.image = frame

        self.quit()

    def quit(self):
        self._cap.release()
