import time

import picamera
from picamera.array import PiRGBArray

from master_controller.camera.generic_camera import GenericCamera
from settings import CAMERA_RESOLUTION, CAMERA_FRAMERATE


class CameraPi(GenericCamera):
    def __init__(self):
        super().__init__()
        self._camera = picamera.PiCamera()
        self._camera.resolution = CAMERA_RESOLUTION
        self._camera.framerate = CAMERA_FRAMERATE

    def run(self):
        raw_capture = PiRGBArray(self._camera)

        # allow the camera to warmup
        time.sleep(1)

        # capture frames from the camera
        for frame in self._camera.capture_continuous(
                raw_capture, format="bgr", use_video_port=True
        ):
            # grab the raw NumPy array representing the image
            self.image = frame.array

            # clear the stream in preparation for the next frame
            raw_capture.truncate(0)

            if self.check_stop():
                break

    def stop(self):
        self._stop_camera = True
