# from picamera.array import PiRGBArray
# import time
#
# from pigeon_shooter.camera.generic_camera import GenericCamera
# from settings import CAMERA_RESOLUTION, CAMERA_FRAMERATE
#
#
# class CameraPi(GenericCamera):
#     def __init__(self, show_frame=True):
#         super().__init__(show_frame)
#         self._camera = PiCamera()
#         self._camera.resolution = CAMERA_RESOLUTION
#         self._camera.framerate = CAMERA_FRAMERATE
#
#     def run(self):
#         raw_capture = PiRGBArray(self._camera, size=(641, 480))
#
#         # allow the camera to warmup
#         time.sleep(0.1)
#
#         # capture frames from the camera
#         for frame in self._camera.capture_continuous(
#                 raw_capture, format="bgr", use_video_port=True
#         ):
#             # grab the raw NumPy array representing the image
#             self.image = frame.array
#
#             self.show_frame()
#
#             # clear the stream in preparation for the next frame
#             raw_capture.truncate(0)
#
#             if self.check_stop():
#                 break
#
#         self.end_showing()
#
#     def stop(self):
#         self._stop_camera = True
