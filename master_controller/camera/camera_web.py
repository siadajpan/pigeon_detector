import time

import cv2

from master_controller.camera.generic_camera import GenericCamera


class CameraWeb(GenericCamera):
    def __init__(self, show_frame: bool = True):
        super().__init__(show_frame)
        self._cap = cv2.VideoCapture(0)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        time.sleep(1)
        self.frame_size = self.init_cap()

    def init_cap(self):
        ret, frame = self._cap.read()
        return frame.shape

    def run(self) -> None:
        while not self.check_stop():
            ret, frame = self._cap.read()
            self.image = frame
            if self.showing_image:
                self.show_frame()

        self.quit()

    def quit(self):
        if self.showing_image:
            self.end_showing()
        self._cap.release()
